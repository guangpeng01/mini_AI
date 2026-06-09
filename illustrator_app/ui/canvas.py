"""
画布组件 (Python 3.10+) —— 主绘图区域

负责渲染所有图形项和处理鼠标/键盘交互

架构优化:
- 使用 __slots__ 减少内存占用
- 使用 X | None 替代 Optional[X]
- 使用 match-case 进行类型分发
"""

from __future__ import annotations

from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal
from PyQt5.QtGui import (
    QPainter, QPen, QBrush, QColor, QFont, QPainterPath,
    QCursor, QPixmap, QWheelEvent, QMouseEvent,
    QKeyEvent, QPaintEvent,
)
from PyQt5.QtWidgets import QWidget, QLineEdit

from ..core.graphics import (
    GraphicItem, PathItem, RectangleItem, EllipseItem,
    TextFrame, GroupItem, GraphicStyle, TextType,
    StrokeCap, StrokeJoin, Gradient, GradientType, AnchorPoint,
    Justification, MoveItemsCommand,
)
from ..core.document import Document, Layer
from ..core.tools import (
    BaseTool, ToolType, SelectionTool, DirectSelectTool,
    RectangleTool, EllipseTool, PenTool, TextTool, HandTool,
    AddAnchorPointTool, DeleteAnchorPointTool, ConvertAnchorPointTool,
)


class CanvasWidget(QWidget):
    """画布控件
    注意: PyQt5 QWidget 子类不能使用 __slots__。
    """

    # 信号
    item_selected = pyqtSignal(list)
    item_modified = pyqtSignal()
    tool_changed = pyqtSignal(ToolType)
    mouse_position_changed = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._document: Document | None = None
        self._current_tool: BaseTool = SelectionTool()
        self._tools: dict[ToolType, BaseTool] = {}
        self._init_tools()

        # 视图变换
        self._zoom: float = 1.0
        self._pan_offset = QPointF(0, 0)
        self._is_panning: bool = False
        self._pan_start = QPointF(0, 0)

        # 交互设置
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(400, 300)
        self._update_cursor()  # 初始光标根据默认工具（选择工具=箭头）设置

        # 背景
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor(55, 55, 55))
        self.setPalette(pal)

        # 编辑状态
        self._editing_text: TextFrame | None = None
        self._text_editor: QLineEdit | None = None  # 现场文本编辑器

    def _init_tools(self):
        """初始化所有工具"""
        self._tools = {
            ToolType.SELECTION: SelectionTool(),
            ToolType.DIRECT_SELECT: DirectSelectTool(),
            ToolType.RECTANGLE: RectangleTool(),
            ToolType.ELLIPSE: EllipseTool(),
            ToolType.PEN: PenTool(),
            ToolType.ADD_ANCHOR: AddAnchorPointTool(),
            ToolType.DELETE_ANCHOR: DeleteAnchorPointTool(),
            ToolType.CONVERT_ANCHOR: ConvertAnchorPointTool(),
            ToolType.TEXT: TextTool(),
            ToolType.HAND: HandTool(),
        }

    # ── 属性 ──

    @property
    def document(self) -> Document | None:
        return self._document

    @document.setter
    def document(self, doc: Document):
        self._document = doc
        for tool in self._tools.values():
            tool.set_document(doc)
        self.update()

    @property
    def current_tool_type(self) -> ToolType:
        return self._current_tool.tool_type

    @property
    def zoom(self) -> float:
        return self._zoom

    # ── 工具切换 ──

    def set_tool(self, tool_type: ToolType):
        """切换工具"""
        if tool_type in self._tools:
            self._current_tool.cancel()
            self._current_tool = self._tools[tool_type]
            self._current_tool.set_document(self._document)
            self.tool_changed.emit(tool_type)
            self._update_cursor()
            self.update()

    def _update_cursor(self):
        """根据当前工具更新光标"""
        # 钢笔工具：根据悬停状态动态切换光标
        if self._current_tool.tool_type == ToolType.PEN:
            hover = getattr(self._current_tool, '_hover_state', 0)
            from ..core.tools import PenTool
            pen_cursors = {
                PenTool.PEN_DEFAULT: Qt.CrossCursor,
                PenTool.PEN_PLUS: Qt.CrossCursor,       # Pen+
                PenTool.PEN_MINUS: Qt.CrossCursor,       # Pen-
                PenTool.PEN_CLOSE: Qt.CrossCursor,       # Pen○
                PenTool.PEN_CONTINUE: Qt.CrossCursor,    # Pen/
            }
            self.setCursor(QCursor(pen_cursors.get(hover, Qt.CrossCursor)))
            return

        cursor = {
            ToolType.SELECTION: Qt.ArrowCursor,
            ToolType.DIRECT_SELECT: Qt.ArrowCursor,
            ToolType.RECTANGLE: Qt.CrossCursor,
            ToolType.ELLIPSE: Qt.CrossCursor,
            ToolType.ADD_ANCHOR: Qt.CrossCursor,
            ToolType.DELETE_ANCHOR: Qt.CrossCursor,
            ToolType.CONVERT_ANCHOR: Qt.CrossCursor,
            ToolType.TEXT: Qt.IBeamCursor,
            ToolType.HAND: Qt.OpenHandCursor,
            ToolType.ZOOM: Qt.CrossCursor,
        }.get(self._current_tool.tool_type, Qt.ArrowCursor)
        self.setCursor(QCursor(cursor))

    # ── 坐标转换 ──

    def _to_doc_coords(self, pos: QPointF) -> QPointF:
        center = QPointF(self.width() / 2, self.height() / 2)
        return (pos - center - self._pan_offset) / self._zoom

    def _to_screen_coords(self, pos: QPointF) -> QPointF:
        center = QPointF(self.width() / 2, self.height() / 2)
        return pos * self._zoom + center + self._pan_offset
        # 将文档坐标乘以缩放比例，再加上中心点和平移偏移量，得到屏幕坐标

    # ── 鼠标事件 ──

    def mousePressEvent(self, event: QMouseEvent):
        # 鼠标按下事件
        try:
            # 如果正在文本编辑，检查是否点击在编辑器外
            if self._editing_text and self._text_editor:
                if not self._text_editor.geometry().contains(event.pos()):
                    self._finish_text_edit()
                    # 继续处理本次点击（可能选择其他对象）

            doc_pos = self._to_doc_coords(QPointF(event.pos()))

            # 中键平移或抓手工具
            if event.button() == Qt.MiddleButton or self._current_tool.tool_type == ToolType.HAND:
                self._is_panning = True
                self._pan_start = QPointF(event.pos())
                self.setCursor(Qt.ClosedHandCursor)
                return

            self._current_tool.mouse_press(doc_pos, event.modifiers())
            self.update()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[mousePressEvent ERROR] {e}")

    def mouseMoveEvent(self, event: QMouseEvent):
        # 定义鼠标移动事件
        try:
            doc_pos = self._to_doc_coords(QPointF(event.pos()))
            self.mouse_position_changed.emit(doc_pos.x(), doc_pos.y())

            if self._is_panning:
                delta = QPointF(event.pos()) - self._pan_start
                self._pan_offset += delta
                self._pan_start = QPointF(event.pos())
                self.update()
                return
            # 将鼠标移动事件和修饰键传递给当前工具处理
            self._current_tool.mouse_move(doc_pos, event.modifiers())
            
            # 钢笔工具：动态更新光标以反映悬停状态
            if self._current_tool.tool_type == ToolType.PEN:
                self._update_cursor()
            
            # 选择工具/直接选择工具拖拽移动/旋转时，实时发射 item_selected 信号刷新属性面板
            if (self._current_tool.tool_type in (ToolType.SELECTION, ToolType.DIRECT_SELECT)
                    and self._document
                    and getattr(self._current_tool, '_drag_start', None) is not None):
                sel = self._document.get_selection()
                if sel:
                    self.item_selected.emit(sel)
            
            self.update()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[mouseMoveEvent ERROR] {e}")

    def mouseReleaseEvent(self, event: QMouseEvent):
        try:
            if event.button() == Qt.MiddleButton or self._is_panning:
                self._is_panning = False
                self._update_cursor()
                return
            # 将鼠标时间的屏幕坐标转换为文档坐标
            doc_pos = self._to_doc_coords(QPointF(event.pos()))
            # 将鼠标释放事件和修饰键传递给当前工具处理
            self._current_tool.mouse_release(doc_pos, event.modifiers())

            # 文本工具点击已有文本框后，进入编辑状态
            entered_text_edit = False
            if self._current_tool.tool_type == ToolType.TEXT:
                text_tool = self._current_tool
                if hasattr(text_tool, 'consume_pending_edit_item'):
                    pending = text_tool.consume_pending_edit_item()
                else:
                    pending = getattr(text_tool, 'pending_edit_item', None)
                    if hasattr(text_tool, '_pending_edit_item'):
                        text_tool._pending_edit_item = None
                if pending is not None:
                    self._start_text_edit(pending)
                    entered_text_edit = True

            # 如果进入了文本编辑状态，不发射 item_selected 信号（避免属性面板重置选中状态）
            if not entered_text_edit and self._document:
                sel = self._document.get_selection()
                # 发射图形项被选中信号，携带选中列表
                self.item_selected.emit(sel)

            self.update()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[mouseReleaseEvent ERROR] {e}")

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        doc_pos = self._to_doc_coords(QPointF(event.pos()))
        self._current_tool.mouse_double_click(doc_pos, event.modifiers())

        # 选择工具双击文本框 → 自动切换至文本工具并进入编辑状态
        if self._current_tool.tool_type == ToolType.SELECTION and self._document:
            item = self._document.get_item_at(doc_pos.x(), doc_pos.y())
            if isinstance(item, TextFrame):
                # 进入编辑状态前先取消所有选中，避免绘制选中边框
                self._document.clear_selection()
                item.selected = False
                # 自动切换至文本工具（Illustrator 标准行为）
                self.set_tool(ToolType.TEXT)
                self._start_text_edit(item)
                self.item_modified.emit()

        self.update()

    def wheelEvent(self, event: QWheelEvent):
        """滚轮缩放"""
        zoom_factor = 1.1
        if event.angleDelta().y() > 0:
            self._zoom *= zoom_factor
        else:
            self._zoom /= zoom_factor
        self._zoom = max(0.05, min(20.0, self._zoom))
        self.update()

    # ── 键盘事件 ──

    def keyPressEvent(self, event: QKeyEvent):
        try:
            key = event.key()
            mods = event.modifiers()

            # 如果正在文本编辑，按 Esc 结束编辑
            if self._editing_text and key == Qt.Key_Escape:
                self._finish_text_edit()
                return

            # 工具快捷键
            shortcuts = {
                Qt.Key_V: ToolType.SELECTION,
                Qt.Key_A: ToolType.DIRECT_SELECT,
                Qt.Key_M: ToolType.RECTANGLE,
                Qt.Key_L: ToolType.ELLIPSE,
                Qt.Key_P: ToolType.PEN,
                Qt.Key_T: ToolType.TEXT,
                Qt.Key_H: ToolType.HAND,
            }

            # Shift+C → 转换锚点工具
            if key == Qt.Key_C and (mods & Qt.ShiftModifier):
                self.set_tool(ToolType.CONVERT_ANCHOR)
                return

            if key in shortcuts:
                self.set_tool(shortcuts[key])
                return

            # 方向键微调选中元素（选择工具/直接选择工具模式下）
            if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                if self._document and self._current_tool.tool_type in (
                    ToolType.SELECTION, ToolType.DIRECT_SELECT,
                ):
                    sel = self._document.get_selection()
                    if sel:
                        # Shift 加速：每次移动 10px，否则 1px
                        step = 10.0 if (mods & Qt.ShiftModifier) else 1.0
                        dx = dy = 0.0
                        if key == Qt.Key_Left:
                            dx = -step
                        elif key == Qt.Key_Right:
                            dx = step
                        elif key == Qt.Key_Up:
                            dy = -step
                        elif key == Qt.Key_Down:
                            dy = step

                        # 记录移动命令用于撤销（通过 execute_command 统一入口）
                        # MoveItemsCommand.execute() 内部执行实际移动
                        cmd = MoveItemsCommand(
                            self._document, list(sel), dx, dy,
                        )
                        self._document.execute_command(cmd)

                        self.item_selected.emit(sel)
                        self.item_modified.emit()
                        self.update()
                return

            # Delete 删除选中项 或 删除锚点（直接选择工具/钢笔工具）
            if key in (Qt.Key_Delete, Qt.Key_Backspace):
                if self._document:
                    # 直接选择工具/钢笔工具下：删除锚点
                    if self._current_tool.tool_type in (ToolType.DIRECT_SELECT, ToolType.PEN):
                        self._current_tool.key_press(key, mods)
                        self.item_modified.emit()
                        self.update()
                        return
                    for item in list(self._document.get_selection()):
                        self._document.remove_item(item)
                    self.item_selected.emit([])
                    self.update()
                return

            # Ctrl+Shift+G 取消编组（必须在 Ctrl+G 之前检测）
            if key == Qt.Key_G and (mods & Qt.ControlModifier) and (mods & Qt.ShiftModifier):
                if self._document:
                    for item in list(self._document.get_selection()):
                        self._document.ungroup(item)
                    self.item_selected.emit([])
                    self.update()
                return

            # Ctrl+G 编组
            if key == Qt.Key_G and (mods & Qt.ControlModifier):
                if self._document:
                    group = self._document.group_selection()
                    if group:
                        self.item_selected.emit([group])
                        self.update()
                return

            # Ctrl+A 全选
            if key == Qt.Key_A and (mods & Qt.ControlModifier):
                if self._document:
                    self._document.select_all()
                    self.item_selected.emit(self._document.get_selection())
                    self.update()
                return

            # +/- 添加锚点（直接选择工具）
            if key in (Qt.Key_Plus, Qt.Key_Equal, Qt.Key_Minus):
                if self._current_tool.tool_type == ToolType.DIRECT_SELECT:
                    self._current_tool.key_press(key, mods)
                    self.item_modified.emit()
                    self.update()
                    return

            # 传递给当前工具；将末尾处理的按键事件传递给当前工具
            self._current_tool.key_press(key, mods)
            self.update()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[keyPressEvent ERROR] {e}")

    def keyReleaseEvent(self, event: QKeyEvent):
        """键盘释放事件 —— 处理修饰键释放时的光标更新"""
        try:
            key = event.key()
            # Alt/Ctrl/Shift 释放时更新光标（钢笔工具悬停状态可能改变）
            if key in (Qt.Key_Alt, Qt.Key_Control, Qt.Key_Shift, Qt.Key_Space):
                if self._current_tool.tool_type == ToolType.PEN:
                    self._update_cursor()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[keyReleaseEvent ERROR] {e}")

    # ── 文字编辑 ──

    def _start_text_edit(self, text_frame: TextFrame):
        """开始文字编辑 —— 创建现场文本编辑器覆盖在文本框上"""
        # 清除所有选中状态，确保编辑中的文本框不显示选中边框
        if self._document:
            self._document.clear_selection()
        text_frame.selected = False
        self._editing_text = text_frame

        # 创建现场文本编辑器
        self._create_text_editor(text_frame)
        self.item_modified.emit()

    def _create_text_editor(self, text_frame: TextFrame):
        """在画布上创建覆盖文本框的 QLineEdit 编辑器"""
        # 如果已有编辑器，先销毁
        self._destroy_text_editor()

        editor = QLineEdit(self)
        editor.setText(text_frame.contents)

        # 计算文本框在屏幕上的位置
        screen_rect = self._text_frame_to_screen_rect(text_frame)
        editor.setGeometry(screen_rect.toRect())

        # 设置字体匹配文本框（★ 按缩放比例调整，使编辑器文字与画布渲染一致）
        font = text_frame.char_attrs.to_qfont()
        if self._zoom != 1.0:
            font.setPointSizeF(font.pointSizeF() * self._zoom * 0.7)
        editor.setFont(font)

        # 设置样式：透明背景，匹配文本颜色
        color = text_frame.char_attrs.fill_color or QColor(0, 0, 0)
        editor.setStyleSheet(f"""
            QLineEdit {{
                background-color: transparent;
                color: {color.name()};
                border: none;
                padding: 0px;
            }}
        """)

        # 文本变化时同步到 TextFrame
        editor.textChanged.connect(self._on_editor_text_changed)
        # 失去焦点或按回车时结束编辑
        editor.editingFinished.connect(self._finish_text_edit)

        editor.show()
        editor.setFocus()
        editor.selectAll()

        self._text_editor = editor

    def _destroy_text_editor(self):
        """销毁现场文本编辑器"""
        if self._text_editor:
            self._text_editor.deleteLater()
            self._text_editor = None

    def _on_editor_text_changed(self, text: str):
        """编辑器文本变化时同步到 TextFrame 并自动调整大小"""
        if self._editing_text:
            self._editing_text.contents = text
            self._auto_resize_text_frame(self._editing_text)
            if self._document:
                self._document.modified = True
            self.item_modified.emit()
            self.update()

    def _auto_resize_text_frame(self, text_frame: TextFrame):
        """根据文本内容自动调整文本框大小"""
        from PyQt5.QtGui import QFontMetrics
        font = text_frame.char_attrs.to_qfont()
        # ★ 按缩放比例调整字体，使计算出的尺寸与屏幕编辑器一致
        if self._zoom != 1.0:
            font.setPointSizeF(font.pointSizeF() * self._zoom)
        metrics = QFontMetrics(font)
        text = text_frame.contents

        # 计算文本所需宽度（考虑换行）
        lines = text.split('\n')
        max_width = 0
        total_height = 0
        for line in lines:
            line_width = metrics.horizontalAdvance(line)
            max_width = max(max_width, line_width)
            total_height += metrics.height()

        # 最小宽度和高度（文档坐标）
        min_width = 50
        min_height = metrics.height()

        # 计算结果在屏幕像素，需转回文档坐标
        zoom = self._zoom if self._zoom != 1.0 else 1.0
        new_width = max(min_width, max_width + 10) / zoom
        new_height = max(min_height, total_height + 4) / zoom

        rect = text_frame.rect
        # 只扩展，不缩小（避免编辑时文本框跳动）
        if new_width > rect.width() or new_height > rect.height():
            text_frame.rect = QRectF(
                rect.x(), rect.y(),
                max(rect.width(), new_width),
                max(rect.height(), new_height),
            )

    def _text_frame_to_screen_rect(self, text_frame: TextFrame) -> QRectF:
        """将文本框的文档坐标转换为屏幕坐标（用于定位 QLineEdit）"""
        rect = text_frame.rect
        # 应用文本框的变换矩阵
        tl = text_frame._transform.map(rect.topLeft())
        br = text_frame._transform.map(rect.bottomRight())
        # 转换为屏幕坐标
        screen_tl = self._to_screen_coords(tl)
        screen_br = self._to_screen_coords(br)
        return QRectF(screen_tl, screen_br)

    def _finish_text_edit(self):
        """结束文字编辑，保存内容并销毁编辑器"""
        if self._text_editor and self._editing_text:
            self._editing_text.contents = self._text_editor.text()
            self._auto_resize_text_frame(self._editing_text)

        self._destroy_text_editor()
        self._editing_text = None
        if self._document:
            self._document.modified = True
        self.item_modified.emit()
        self.update()

    def edit_selected_text(self, new_text: str):
        if self._editing_text:
            self._editing_text.contents = new_text
            if self._document:
                self._document.modified = True
            self.item_modified.emit()
            self.update()

    def finish_text_edit(self):
        self._finish_text_edit()

    # ── 视图操作 ──

    def zoom_in(self):
        self._zoom = min(20.0, self._zoom * 1.25)
        self.update()

    def zoom_out(self):
        self._zoom = max(0.05, self._zoom / 1.25)
        self.update()

    def zoom_to_fit(self):
        if self._document:
            self._zoom = min(
                self.width() / self._document.width,
                self.height() / self._document.height,
            ) * 0.9
            self._pan_offset = QPointF(0, 0)
            self.update()

    def zoom_100(self):
        self._zoom = 1.0
        self._pan_offset = QPointF(0, 0)
        self.update()

    # ── 绘制 ──

    def paintEvent(self, event: QPaintEvent):
        """绘制事件 — 集成 Dirty Flag 增量渲染优化

        对照 AI 渲染管线：
        1. 检查 Dirty Flag，决定全量重绘还是增量更新
        2. 按 Z-Order（由底向上）深度优先遍历 Layer 树
        3. 对每个可见节点应用 CTM → Tessellate → GPU Draw
        4. 最后绘制工具预览层
        """
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)

            painter.fillRect(self.rect(), QColor(55, 55, 55))

            if not self._document:
                painter.end()
                return

            # ── Dirty Flag 检测：非脏且非系统触发 → 可跳过部分渲染 ──
            # 每次 paintEvent 完成后清除脏标记
            was_dirty = self._document.dirty_flag.is_dirty

            painter.save()
            center = QPointF(self.width() / 2, self.height() / 2)
            painter.translate(center + self._pan_offset)
            painter.scale(self._zoom, self._zoom)

            # 画板
            self._draw_artboard(painter)

            # ── 深度优先遍历 Scene Graph 渲染（对照 AI Painter's Algorithm）──
            # 所有图层（正序绘制：layers[0]先绘制=底层，layers[-1]后绘制=顶层）
            for layer in self._document.layers:
                if layer.visible:
                    self._draw_layer_recursive(painter, layer)

            # 工具预览（在文档坐标系下绘制，与图形项保持一致）
            self._current_tool.draw_preview(painter, editing_text=self._editing_text)
            painter.restore()  # 恢复到屏幕坐标系（用于 overlay 等）
            painter.end()

            # ── 绘制完成后清除脏标记 ──
            if was_dirty:
                self._document.dirty_flag.clear()

            # 更新现场文本编辑器的位置（跟随画布平移/缩放）
            if self._editing_text and self._text_editor:
                screen_rect = self._text_frame_to_screen_rect(self._editing_text)
                self._text_editor.setGeometry(screen_rect.toRect())
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[paintEvent ERROR] {e}")

    def _draw_layer_recursive(self, painter: QPainter, layer, parent_opacity: float = 1.0):
        """递归绘制图层及其子图层、对象（对照 AI 深度优先遍历）

        Args:
            painter: QPainter 实例
            layer: Layer 对象
            parent_opacity: 父级累积不透明度
        """
        if not layer.visible:
            return

        # 合成不透明度（对照 AI：parentOpacity * (node.opacity / 100)）
        global_opacity = parent_opacity * layer.opacity
        painter.save()
        painter.setOpacity(global_opacity)

        # 轮廓预览模式（对照 AI LayerNode.previewMode === 'outline'）
        if layer.preview_mode == "outline":
            painter.setPen(QPen(Qt.gray, 0.5))
            painter.setBrush(Qt.NoBrush)

        # 模板图层额外降低透明度（对照 AI LayerNode.isTemplate + dimPercent）
        if layer.is_template:
            painter.setOpacity(global_opacity * 0.5)

        # 绘制本图层对象（反序：items[0]=面板上方=后绘制=视觉顶层）
        # ★ 关键：reversed() 确保 items[0]（视觉顶层）最后绘制，覆盖其他元素
        # 当用户拖拽对象改变顺序后，此绘制顺序自动反映新的层级关系
        for item in reversed(list(layer.items)):
            if item.visible:
                self._draw_item(painter, item)

        # 递归绘制子图层（正序遍历：先创建的在底层）
        for sub in layer.sublayers:
            self._draw_layer_recursive(painter, sub, global_opacity)

        painter.restore()

    def _draw_artboard(self, painter: QPainter):
        doc = self._document
        # 画板阴影
        shadow_rect = QRectF(-2, -2, doc.width + 4, doc.height + 4)
        painter.fillRect(shadow_rect, QColor(0, 0, 0, 60))

        # 画板背景
        artboard_rect = QRectF(0, 0, doc.width, doc.height)
        painter.fillRect(artboard_rect, Qt.white)

        # 画板边框
        pen = QPen(QColor(180, 180, 180), 1)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(artboard_rect)

    def _draw_item(self, painter: QPainter, item: GraphicItem):
        # 定义私有方法绘制图形项
        """使用 match-case (Python 3.10+) 进行类型分发"""
        painter.save()
        # 使用 combine=True 将 item 的局部变换与 painter 当前的世界坐标系变换合并
        painter.setTransform(item._transform, True)
        painter.setOpacity(item.opacity)

        match item:
            case GroupItem():
                for sub in item.items:
                    if sub.visible:
                        self._draw_item(painter, sub)
            case TextFrame():
                self._draw_text(painter, item)
            case PathItem():
                self._draw_shape(painter, item.style, item.painter_path())
            case RectangleItem():
                self._draw_shape(painter, item.style, item.painter_path())
            case EllipseItem():
                self._draw_shape(painter, item.style, item.painter_path())
            case _:
                path = item.painter_path()
                # 调用私有方法绘制形状，传入样式和绘制路径
                self._draw_shape(painter, item.style, path)

        if item.selected:
            # 调用私有方法绘制选中手柄
            self._draw_selection_handle(painter, item)

        painter.restore()

    def _draw_shape(self, painter: QPainter, style: GraphicStyle, path: QPainterPath):
        # 接收绘制器参数
        """绘制通用形状（支持纯色和渐变填充）"""
        if style.has_fill():
            if style.fill_gradient:
                rect = path.boundingRect()
                # 将渐变对象转换为Qt渐变对象
                gradient = style.fill_gradient.to_qgradient(rect)
                brush = QBrush(gradient)
            else:
                brush = style.to_qbrush()
            painter.fillPath(path, brush)
        
        if style.stroke_color and style.stroke_width > 0:
            pen = style.to_qpen()
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)

    def _draw_text(self, painter: QPainter, item: TextFrame):
        """绘制文字"""
        rect = item.rect
        font = item.char_attrs.to_qfont()
        color = item.char_attrs.fill_color or QColor(0, 0, 0)

        painter.setFont(font)
        painter.setPen(QPen(color))

        # 对齐 (使用 match-case)
        align = Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap
        match item.para_attrs.justification:
            case Justification.CENTER:
                align = Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWordWrap
            case Justification.RIGHT:
                align = Qt.AlignRight | Qt.AlignVCenter | Qt.TextWordWrap
            case _:
                pass  # LEFT 默认

        # 如果正在现场编辑此文本框，不绘制文字内容（由 QLineEdit 显示）
        if item == self._editing_text and self._text_editor:
            # 只绘制虚线边框表示编辑状态
            pen = QPen(QColor(0, 120, 215), 1, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(rect)
        else:
            painter.drawText(rect, align, item.contents)

    def _draw_selection_handle(self, painter: QPainter, item: GraphicItem):
        """绘制选中边框（缩放手柄由 SelectionTool.draw_preview 负责）

        注意：当文本框处于编辑状态时，不绘制选中边框（Illustrator 标准行为）

        重要：此函数在 _draw_item 内部被调用，此时 painter 已经应用了 item._transform。
        因此必须使用局部坐标（而非变换后的世界坐标）来绘制边框，
        否则会导致双重变换，使选择框位置和大小都错误。
        """
        # 文本框编辑状态不绘制选中边框
        if isinstance(item, TextFrame) and item == self._editing_text:
            return

        # 使用 painter_path().boundingRect() 获取局部坐标矩形
        #（painter 已应用 item._transform，会自动处理旋转/缩放）
        local_rect = item.painter_path().boundingRect()

        # 使用 cosmetic pen 保持线宽为屏幕像素不变，不受变换影响
        pen = QPen(QColor(0, 120, 215), 1.5)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(local_rect)
