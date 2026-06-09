"""
面板组件 (Python 3.10+) —— 工具栏、属性面板、图层面板、色板

架构优化:
- 使用 __slots__ 减少内存占用
- 使用 X | None 替代 Optional[X]
- 使用 match-case 替代 if-elif 链
"""

from __future__ import annotations

from PyQt5.QtCore import Qt, QSize, QPoint, pyqtSignal, QRectF
from PyQt5.QtGui import (
    QColor, QPainter, QPen, QBrush, QFont, QCursor,
)
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QSlider, QSpinBox,
    QDoubleSpinBox, QCheckBox, QColorDialog, QGroupBox,
    QToolBar, QAction, QFrame,
    QLineEdit, QComboBox, QGridLayout,
    QToolButton, QTextEdit, QMenu,
    QTreeWidget, QTreeWidgetItem, QHeaderView, QStyle,
)

from ..core.graphics import (
    GraphicItem, PathItem, RectangleItem, EllipseItem,
    TextFrame, GroupItem, GraphicStyle, StrokeCap, StrokeJoin,
    FillRule, CharacterAttributes, ParagraphAttributes, Justification,
    Swatch,
)
from ..core.document import Document, Layer
from ..core.tools import ToolType


# ── 工具栏 ────────────────────────────────────────────────

class ToolBar(QWidget):
    """工具栏 —— 左侧工具面板
    注意: PyQt5 QWidget 子类不能使用 __slots__。
    类文档字符串:工具栏 —— 左侧工具面板
    """

    tool_selected = pyqtSignal(ToolType)

    TOOLS: list[tuple[ToolType, str, str]] = [
        (ToolType.SELECTION, "选择", "V"),
        (ToolType.DIRECT_SELECT, "直接选择", "A"),
        (ToolType.RECTANGLE, "矩形", "M"),
        (ToolType.ELLIPSE, "椭圆", "L"),
        (ToolType.PEN, "钢笔", "P"),
        (ToolType.TEXT, "文字", "T"),
        (ToolType.HAND, "抓手", "H"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(48)
        self._buttons: dict[ToolType, QToolButton] = {}
        self._current_tool = ToolType.SELECTION
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 8, 4, 8)
        layout.setSpacing(4)

        for tool_type, name, shortcut in self.TOOLS:
            btn = QToolButton()
            btn.setToolTip(f"{name} ({shortcut})")
            btn.setCheckable(True)
            btn.setFixedSize(40, 40)
            # 按钮显示快捷键字母
            btn.setText(shortcut)
            btn.setFont(QFont("Arial", 10, QFont.Bold))
            # 链接点击信号到lambda，通过默认参数捕获循环变量避免闭包陷阱
            btn.clicked.connect(lambda checked, t=tool_type: self._on_tool_clicked(t))
            self._buttons[tool_type] = btn
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        layout.addStretch()
        self._buttons[ToolType.SELECTION].setChecked(True)

        self.setStyleSheet("""
            QWidget { background-color: #3c3c3c; }
            QToolButton { border: 1px solid #555; border-radius: 4px; background-color: #4a4a4a; color: #ddd; }
            QToolButton:hover { background-color: #5a5a5a; }
            QToolButton:checked { background-color: #0d6efd; border-color: #0b5ed7; color: white; }
        """)

    def _on_tool_clicked(self, tool_type: ToolType):
        self._current_tool = tool_type
        for t, btn in self._buttons.items():
            btn.setChecked(t == tool_type)
        self.tool_selected.emit(tool_type)
        # 发射 tool_selected 信号通知外部

    def set_current_tool(self, tool_type: ToolType):
        # 设置当前工具
        if tool_type in self._buttons:
            self._buttons[tool_type].setChecked(True)
            self._current_tool = tool_type
            for t, btn in self._buttons.items():
                btn.setChecked(t == tool_type)


# ── 属性面板 ──────────────────────────────────────────────

class PropertiesPanel(QWidget):
    """属性面板 —— 显示和编辑选中图形的属性
    注意: PyQt5 QWidget 子类不能使用 __slots__。
    """

    fill_color_changed = pyqtSignal(QColor)
    stroke_color_changed = pyqtSignal(QColor)
    stroke_width_changed = pyqtSignal(float)
    opacity_changed = pyqtSignal(float)
    corner_radius_changed = pyqtSignal(float)
    text_changed = pyqtSignal(str)
    font_size_changed = pyqtSignal(float)
    font_family_changed = pyqtSignal(str)
    bold_changed = pyqtSignal(bool)
    italic_changed = pyqtSignal(bool)
    alignment_changed = pyqtSignal(Justification)
    # 变换参数变化信号
    position_changed = pyqtSignal(float, float)  # x, y
    size_changed = pyqtSignal(float, float)      # width, height
    rotation_changed = pyqtSignal(float)         # angle

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_items: list[GraphicItem] = []
        self._init_ui()

    def _init_ui(self):
        # 私有方法，构造属性面板的完整界面
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # ── 变换 ──
        transform_group = QGroupBox("变换")
        transform_layout = QGridLayout(transform_group)

        self._x_spin = self._make_spinbox(-9999, 9999, 1)
        self._y_spin = self._make_spinbox(-9999, 9999, 1)
        self._w_spin = self._make_spinbox(0, 99999, 1)
        self._h_spin = self._make_spinbox(0, 99999, 1)

        # 连接变换参数变化信号
        self._x_spin.valueChanged.connect(self._on_transform_changed)
        self._y_spin.valueChanged.connect(self._on_transform_changed)
        self._w_spin.valueChanged.connect(self._on_transform_changed)
        self._h_spin.valueChanged.connect(self._on_transform_changed)

        for row, items in enumerate([
            [("X:", self._x_spin), ("Y:", self._y_spin)],
            [("W:", self._w_spin), ("H:", self._h_spin)],
        ]):
            (label0, widget0), (label1, widget1) = items
            transform_layout.addWidget(QLabel(label0), row, 0)
            transform_layout.addWidget(widget0, row, 1)
            transform_layout.addWidget(QLabel(label1), row, 2)
            transform_layout.addWidget(widget1, row, 3)

        transform_layout.addWidget(QLabel("旋转:"), 2, 0)
        self._rotate_spin = QDoubleSpinBox()
        self._rotate_spin.setRange(-360, 360)
        self._rotate_spin.valueChanged.connect(self.rotation_changed.emit)
        transform_layout.addWidget(self._rotate_spin, 2, 1)

        transform_layout.addWidget(QLabel("不透明度:"), 2, 2)
        self._opacity_spin = QDoubleSpinBox()
        self._opacity_spin.setRange(0, 100)
        self._opacity_spin.setValue(100)
        self._opacity_spin.setSuffix("%")
        self._opacity_spin.valueChanged.connect(lambda v: self.opacity_changed.emit(v / 100.0))
        transform_layout.addWidget(self._opacity_spin, 2, 3)

        main_layout.addWidget(transform_group)

        # ── 外观 ──
        appearance_group = QGroupBox("外观")
        appearance_layout = QVBoxLayout(appearance_group)

        fill_layout = QHBoxLayout()
        fill_layout.addWidget(QLabel("填充:"))
        self._fill_btn = QPushButton()
        self._fill_btn.setFixedSize(30, 30)
        self._fill_btn.setStyleSheet("background-color: #ccc; border: 1px solid #888;")
        self._fill_btn.clicked.connect(self._on_fill_clicked)
        fill_layout.addWidget(self._fill_btn)
        self._fill_none_btn = QPushButton("无")
        self._fill_none_btn.setFixedWidth(30)
        self._fill_none_btn.clicked.connect(self._on_fill_none)
        fill_layout.addWidget(self._fill_none_btn)
        fill_layout.addStretch()
        appearance_layout.addLayout(fill_layout)

        stroke_layout = QHBoxLayout()
        stroke_layout.addWidget(QLabel("描边:"))
        self._stroke_btn = QPushButton()
        self._stroke_btn.setFixedSize(30, 30)
        self._stroke_btn.setStyleSheet("background-color: #333; border: 1px solid #888;")
        self._stroke_btn.clicked.connect(self._on_stroke_clicked)
        stroke_layout.addWidget(self._stroke_btn)
        self._stroke_none_btn = QPushButton("无")
        self._stroke_none_btn.setFixedWidth(30)
        self._stroke_none_btn.clicked.connect(self._on_stroke_none)
        stroke_layout.addWidget(self._stroke_none_btn)
        stroke_layout.addWidget(QLabel("粗细:"))
        self._stroke_width = QDoubleSpinBox()
        self._stroke_width.setRange(0, 100)
        self._stroke_width.setValue(1)
        self._stroke_width.valueChanged.connect(self.stroke_width_changed.emit)
        stroke_layout.addWidget(self._stroke_width)
        appearance_layout.addLayout(stroke_layout)

        corner_layout = QHBoxLayout()
        corner_layout.addWidget(QLabel("圆角:"))
        self._corner_spin = QDoubleSpinBox()
        self._corner_spin.setRange(0, 500)
        self._corner_spin.valueChanged.connect(self.corner_radius_changed.emit)
        corner_layout.addWidget(self._corner_spin)
        corner_layout.addStretch()
        appearance_layout.addLayout(corner_layout)

        main_layout.addWidget(appearance_group)

        # ── 文字 ──
        text_group = QGroupBox("文字")
        text_layout = QVBoxLayout(text_group)

        font_layout = QHBoxLayout()
        self._font_family = QComboBox()
        self._font_family.setEditable(True)
        self._font_family.addItems([
            "Arial", "Helvetica", "Times New Roman", "Courier New",
            "Verdana", "Georgia", "微软雅黑", "宋体", "黑体",
        ])
        self._font_family.currentTextChanged.connect(self.font_family_changed.emit)
        font_layout.addWidget(self._font_family)

        self._font_size = QDoubleSpinBox()
        self._font_size.setRange(1, 999)
        self._font_size.setValue(24)
        self._font_size.valueChanged.connect(self.font_size_changed.emit)
        font_layout.addWidget(self._font_size)
        text_layout.addLayout(font_layout)

        style_layout = QHBoxLayout()
        self._bold_btn = QPushButton("B")
        self._bold_btn.setCheckable(True)
        self._bold_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self._bold_btn.setFixedSize(30, 30)
        self._bold_btn.toggled.connect(self.bold_changed.emit)
        style_layout.addWidget(self._bold_btn)

        self._italic_btn = QPushButton("I")
        self._italic_btn.setCheckable(True)
        self._italic_btn.setFont(QFont("Arial", 12, QFont.StyleItalic))
        self._italic_btn.setFixedSize(30, 30)
        self._italic_btn.toggled.connect(self.italic_changed.emit)
        style_layout.addWidget(self._italic_btn)
        style_layout.addStretch()
        text_layout.addLayout(style_layout)

        align_layout = QHBoxLayout()
        self._align_left = QPushButton("左")
        self._align_left.setCheckable(True)
        self._align_left.clicked.connect(lambda: self.alignment_changed.emit(Justification.LEFT))
        align_layout.addWidget(self._align_left)

        self._align_center = QPushButton("中")
        self._align_center.setCheckable(True)
        self._align_center.clicked.connect(lambda: self.alignment_changed.emit(Justification.CENTER))
        align_layout.addWidget(self._align_center)

        self._align_right = QPushButton("右")
        self._align_right.setCheckable(True)
        self._align_right.clicked.connect(lambda: self.alignment_changed.emit(Justification.RIGHT))
        align_layout.addWidget(self._align_right)
        text_layout.addLayout(align_layout)

        self._text_edit = QTextEdit()
        self._text_edit.setMaximumHeight(80)
        self._text_edit.setPlaceholderText("输入文字内容...")
        self._text_edit.textChanged.connect(
            lambda: self.text_changed.emit(self._text_edit.toPlainText()),
        )
        text_layout.addWidget(self._text_edit)

        main_layout.addWidget(text_group)

        main_layout.addStretch()

        self.setStyleSheet("""
            QGroupBox { font-weight: bold; border: 1px solid #555; border-radius: 4px; margin-top: 8px; padding-top: 12px; color: #ddd; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #ccc; }
            QLabel { color: #bbb; }
            QDoubleSpinBox, QSpinBox, QComboBox { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; padding: 2px; }
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; padding: 4px 8px; border-radius: 3px; }
            QPushButton:hover { background-color: #5a5a5a; }
            QPushButton:checked { background-color: #0d6efd; color: white; }
            QTextEdit { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; }
        """)
        self.setMinimumWidth(220)

    @staticmethod
    def _make_spinbox(min_val: float, max_val: float, decimals: int) -> QDoubleSpinBox:
        sb = QDoubleSpinBox()
        sb.setRange(min_val, max_val)
        sb.setDecimals(decimals)
        return sb

    def update_selection(self, items: list[GraphicItem]):
        """更新选中项显示"""
        self._selected_items = items
        if not items:
            self.setEnabled(False)
            return

        try:
            self.setEnabled(True)
            item = items[0]

            # 变换；获取对象边界矩形
            rect = item.bounding_rect()
            for spin, val in [
                (self._x_spin, rect.x()), (self._y_spin, rect.y()),
                (self._w_spin, rect.width()), (self._h_spin, rect.height()),
            ]:
                spin.blockSignals(True)
                spin.setValue(val)
                spin.blockSignals(False)

            # 旋转角度 —— 从变换矩阵中提取当前旋转角度
            import math
            m11 = item._transform.m11()
            m12 = item._transform.m12()
            current_rotation = math.degrees(math.atan2(m12, m11))
            self._rotate_spin.blockSignals(True)
            self._rotate_spin.setValue(round(current_rotation, 2))
            self._rotate_spin.blockSignals(False)

            # 不透明度
            self._opacity_spin.blockSignals(True)
            self._opacity_spin.setValue(item.opacity * 100)
            self._opacity_spin.blockSignals(False)

            # 填充颜色
            fc = item.style.fill_color
            if fc is not None and fc.isValid():
                self._fill_btn.setStyleSheet(
                    f"background-color: {fc.name()}; border: 1px solid #888;"
                )
            else:
                self._fill_btn.setStyleSheet(
                    "background-color: transparent; border: 1px dashed #888;"
                )

            # 描边颜色
            sc = item.style.stroke_color
            if sc is not None and sc.isValid():
                self._stroke_btn.setStyleSheet(
                    f"background-color: {sc.name()}; border: 1px solid #888;"
                )
            else:
                self._stroke_btn.setStyleSheet(
                    "background-color: transparent; border: 1px dashed #888;"
                )

            # 描边粗细
            self._stroke_width.blockSignals(True)
            self._stroke_width.setValue(item.style.stroke_width)
            self._stroke_width.blockSignals(False)

            # 圆角
            if isinstance(item, RectangleItem):
                self._corner_spin.setEnabled(True)
                self._corner_spin.blockSignals(True)
                self._corner_spin.setValue(item.corner_radius)
                self._corner_spin.blockSignals(False)
            else:
                self._corner_spin.setEnabled(False)

            # 文字属性
            is_text = isinstance(item, TextFrame)
            for widget in [
                self._font_family, self._font_size,
                self._bold_btn, self._italic_btn, self._text_edit,
            ]:
                widget.setEnabled(is_text)

            if is_text:
                self._font_family.blockSignals(True)
                self._font_family.setCurrentText(item.char_attrs.font_family)
                self._font_family.blockSignals(False)

                self._font_size.blockSignals(True)
                self._font_size.setValue(item.char_attrs.font_size)
                self._font_size.blockSignals(False)

                for btn, val in [
                    (self._bold_btn, item.char_attrs.bold),
                    (self._italic_btn, item.char_attrs.italic),
                ]:
                    btn.blockSignals(True)
                    btn.setChecked(val)
                    btn.blockSignals(False)

                self._text_edit.blockSignals(True)
                self._text_edit.setPlainText(item.contents)
                self._text_edit.blockSignals(False)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[update_selection ERROR] {e}")

    def _on_transform_changed(self):
        """变换参数变化时发射位置和大小信号"""
        x = self._x_spin.value()
        y = self._y_spin.value()
        w = self._w_spin.value()
        h = self._h_spin.value()
        self.position_changed.emit(x, y)
        self.size_changed.emit(w, h)

    def _on_fill_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.fill_color_changed.emit(color)
            self._fill_btn.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid #888;"
            )

    def _on_fill_none(self):
        self.fill_color_changed.emit(QColor())
        self._fill_btn.setStyleSheet(
            "background-color: transparent; border: 1px dashed #888;"
        )

    def _on_stroke_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.stroke_color_changed.emit(color)
            self._stroke_btn.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid #888;"
            )

    def _on_stroke_none(self):
        self.stroke_color_changed.emit(QColor())
        self._stroke_btn.setStyleSheet(
            "background-color: transparent; border: 1px dashed #888;"
        )


# ── 图层面板 ──────────────────────────────────────────────

class LayersPanel(QWidget):
    """图层面板 —— 1:1 对照 Adobe Illustrator 图层面板
    
    对照 PDF 功能（共 26 章）：
    第二章 - 图层面板组成：图层名称、展开箭头、可见性(眼睛)、锁定、目标圆圈、选择圆圈、彩色方块
    第三章 - 新建图层：Create New Layer 按钮 + 面板菜单 New Layer
    第四章 - 重命名图层：双击图层名称
    第五章 - 删除图层：点击垃圾桶图标 / 拖动到垃圾桶
    第六章 - 复制图层：拖动图层到 Create New Layer 按钮
    第七章 - 显示与隐藏图层：眼睛图标切换
    第八章 - 锁定与解锁图层：锁定区域切换
    第九章 - 图层排序：拖动图层上下移动
    第十章 - 子图层：New Sublayer 创建层级结构
    第十一章 - 展开与折叠图层：三角箭头展开/折叠
    第十二章 - 对象层级管理：展开图层后拖动对象调整顺序
    第十三章 - 移动对象到其他图层：拖动彩色方块跨图层移动
    第十四章 - 选择整个图层：点击目标圆圈全选图层对象
    第十五章 - 收集到新图层：Collect in New Layer
    第十六章 - 释放到图层：Release to Layers (Sequence/Build)
    第十七章 - 合并图层：Merge Selected Layers
    第十八章 - 拼合图稿：Flatten Artwork
    第十九章 - 模板图层：Template Layer（自动锁定+降低透明度）
    第二十章 - 图层颜色：设置图层识别颜色
    第二十一章 - 打印控制：控制图层是否参与打印
    第二十二章 - 预览模式：Preview(正常)/Outline(轮廓)
    第二十三章 - 查找对象：选中对象时图层面板自动定位
    第二十四章 - 目标对象(Target)：指定效果作用对象
    第二十五章 - 图层与外观系统：图层级效果（阴影、模糊、透明度）
    第二十六章 - 图层最佳实践：命名规范、项目结构
    
    注意: PyQt5 QWidget 子类不能使用 __slots__。
    """

    layer_selected = pyqtSignal(int)
    layer_visibility_changed = pyqtSignal(int, bool)
    layer_locked_changed = pyqtSignal(int, bool)
    layer_add_requested = pyqtSignal()
    layer_remove_requested = pyqtSignal(int)
    layer_duplicate_requested = pyqtSignal(int)
    layer_rename_requested = pyqtSignal(int, str)
    layer_reorder_requested = pyqtSignal(int, int)  # from_index, to_index
    layer_merge_requested = pyqtSignal(list)  # list of indices
    layer_flatten_requested = pyqtSignal()
    layer_collect_requested = pyqtSignal()
    layer_release_sequence_requested = pyqtSignal()
    layer_release_build_requested = pyqtSignal()
    item_move_to_layer = pyqtSignal(int)  # target layer index
    layer_select_all_requested = pyqtSignal(int)  # 选择整个图层的所有对象
    layer_target_requested = pyqtSignal(int)  # 设置目标图层（效果作用）
    layer_color_changed = pyqtSignal(int, QColor)  # 图层颜色变更
    layer_template_changed = pyqtSignal(int, bool)  # 模板模式变更
    layer_printable_changed = pyqtSignal(int, bool)  # 打印状态变更
    layer_preview_mode_changed = pyqtSignal(int, str)  # 预览模式变更
    layer_opacity_changed = pyqtSignal(int, float)  # 图层不透明度变更
    item_order_changed = pyqtSignal(int, int, int, object)  # layer_index, from_pos, to_pos, parent_item
    item_delete_requested = pyqtSignal(object)       # GraphicItem - 删除对象
    item_duplicate_requested = pyqtSignal(object)    # GraphicItem - 复制对象
    item_select_requested = pyqtSignal(int, int)     # layer_index, item_index - 选中画布上的对象
    item_visibility_toggled = pyqtSignal(object, bool)  # 对象显隐切换
    item_locked_toggled = pyqtSignal(object, bool)     # 对象锁定切换
    item_bring_forward_requested = pyqtSignal(object)   # 对象上移一层
    item_send_backward_requested = pyqtSignal(object)   # 对象下移一层
    # 排列按钮信号（从属性面板移入）
    order_front = pyqtSignal()
    order_back = pyqtSignal()
    order_forward = pyqtSignal()
    order_backward = pyqtSignal()
    delete_requested = pyqtSignal()

    LAYER_COLORS = [
        QColor(0, 120, 215),    # 蓝色
        QColor(220, 50, 50),    # 红色
        QColor(0, 150, 80),     # 绿色
        QColor(255, 140, 0),    # 橙色
        QColor(150, 50, 200),   # 紫色
        QColor(0, 180, 180),    # 青色
        QColor(200, 100, 150),  # 粉色
        QColor(139, 90, 43),    # 棕色
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_index = 0
        self._layers_data: list[Layer] = []
        self._editing_index = -1  # 正在编辑名称的图层索引
        self._trash_bin: QPushButton | None = None  # 垃圾桶按钮（拖拽删除）
        self._last_click_pos: QPoint | None = None  # 记录最近一次在树控件上的点击坐标（viewport坐标）
        self._init_ui()

    def _init_ui(self):
        # 私有方法，构建图层面板界面
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # ── 标题栏 ──
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("图层"))
        title_layout.addStretch()

        # 图层菜单按钮
        self._menu_btn = QPushButton("☰")
        self._menu_btn.setFixedSize(24, 24)
        self._menu_btn.setToolTip("图层菜单")
        self._menu_btn.clicked.connect(self._show_layer_menu)
        title_layout.addWidget(self._menu_btn)

        layout.addLayout(title_layout)

        # ── 图层树（使用 QTreeWidget 支持层级、拖拽、彩色方块） ──
        self._tree = QTreeWidget()
        self._tree.setHeaderHidden(True)
        self._tree.setIndentation(20)
        self._tree.setRootIsDecorated(True)
        self._tree.setAnimated(True)
        self._tree.setDragEnabled(True)
        self._tree.setAcceptDrops(True)
        self._tree.setDropIndicatorShown(True)
        self._tree.setDragDropMode(self._tree.InternalMove)
        self._tree.setSelectionMode(self._tree.ExtendedSelection)
        self._tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self._tree.customContextMenuRequested.connect(self._on_context_menu)
        self._tree.currentItemChanged.connect(self._on_item_changed)
        self._tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        self._tree.itemChanged.connect(self._on_item_changed_flag)
        self._tree.model().rowsMoved.connect(self._on_rows_moved)
        # 点击目标圆圈全选图层（第十四章）
        self._tree.itemClicked.connect(self._on_item_clicked)
        # ★ 安装事件过滤器到树控件的 viewport，精确捕获每次点击坐标
        self._tree.viewport().installEventFilter(self)
        layout.addWidget(self._tree)
        # 将树控件添加到主布局

        # ── 排列按钮栏（从属性面板移入）──
        arrange_layout = QHBoxLayout()
        arrange_layout.setSpacing(4)
        for text, signal in [
            ("置顶", self.order_front),
            ("上移", self.order_forward),
            ("下移", self.order_backward),
            ("置底", self.order_back),
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(signal.emit)
            arrange_layout.addWidget(btn)
        layout.addLayout(arrange_layout)

        # ── 删除按钮（从属性面板移入）──
        self._delete_btn = QPushButton("删除选中对象")
        self._delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545; color: white; border: none;
                padding: 8px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #c82333; }
        """)
        self._delete_btn.clicked.connect(self.delete_requested.emit)
        layout.addWidget(self._delete_btn)

        # ── 底部按钮栏（对照 Ai：Create New Layer / 垃圾桶 / 子图层 / 收集） ──
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(4)

        # Create New Layer 按钮（第三章方法1 — 新建图层，第六章 — 拖拽复制）
        self._add_btn = QPushButton("+")
        self._add_btn.setFixedSize(28, 28)
        self._add_btn.setToolTip("创建新图层\n拖拽图层到此按钮可复制")
        self._add_btn.clicked.connect(self.layer_add_requested.emit)
        self._add_btn.setAcceptDrops(True)
        self._add_btn.dragEnterEvent = self._on_add_btn_drag_enter
        self._add_btn.dragMoveEvent = self._on_add_btn_drag_move
        self._add_btn.dropEvent = self._on_add_btn_drop
        bottom_layout.addWidget(self._add_btn)

        # 垃圾桶按钮（第五章 — 删除图层，支持拖拽到垃圾桶删除）
        self._trash_bin = QPushButton("🗑")
        self._trash_bin.setFixedSize(28, 28)
        self._trash_bin.setToolTip("删除选定图层\n拖拽图层到此按钮可删除")
        self._trash_bin.clicked.connect(
            lambda: self.layer_remove_requested.emit(self._current_index),
        )
        self._trash_bin.setAcceptDrops(True)
        self._trash_bin.dragEnterEvent = self._on_trash_drag_enter
        self._trash_bin.dragMoveEvent = self._on_trash_drag_move
        self._trash_bin.dropEvent = self._on_trash_drop
        bottom_layout.addWidget(self._trash_bin)

        bottom_layout.addSpacing(8)

        self._sublayer_btn = QPushButton("子图层")
        self._sublayer_btn.setToolTip("新建子图层（第十章）")
        self._sublayer_btn.clicked.connect(self._on_add_sublayer)
        bottom_layout.addWidget(self._sublayer_btn)

        self._collect_btn = QPushButton("收集")
        self._collect_btn.setToolTip("收集到新图层（第十五章）")
        self._collect_btn.clicked.connect(self.layer_collect_requested.emit)
        bottom_layout.addWidget(self._collect_btn)

        layout.addLayout(bottom_layout)

        self.setStyleSheet("""
            QTreeWidget { background-color: #2d2d2d; color: #ddd; border: 1px solid #555; outline: none; }
            QTreeWidget::item { padding: 3px 2px; border-bottom: 1px solid #3a3a3a; }
            QTreeWidget::item:selected { background-color: #0d6efd; color: white; }
            QTreeWidget::item:hover { background-color: #3a3a3a; }
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings { border-image: none; }
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; border-radius: 3px; font-weight: bold; padding: 2px 6px; }
            QPushButton:hover { background-color: #5a5a5a; }
            QPushButton#trash_hover { background-color: #dc3545; border-color: #dc3545; }
            QPushButton#add_hover { background-color: #0d6efd; border-color: #0d6efd; }
            QLineEdit { background-color: #3c3c3c; color: #ddd; border: 1px solid #0d6efd; padding: 2px; }
        """)

    # ── 更新图层列表 ──

    def update_layers(self, layers: list[Layer], active_index: int):
        """更新图层树，显示图层及子图层的层级结构（对照第二章图层面板组成）"""
        self._layers_data = layers
        self._tree.blockSignals(True)
        self._tree.clear()

        # 反序显示图层：layers[-1](最新/顶层)在面板上方，layers[0](最早/底层)在面板下方
        # reversed() 使最新的图层显示在面板顶部
        for i, layer in enumerate(reversed(layers)):
            real_index = len(layers) - 1 - i
            item = self._create_layer_item(layer, real_index)
            # 为每个图层创建树节点
            self._tree.addTopLevelItem(item)
            if real_index == active_index:
                self._tree.setCurrentItem(item)
            # 展开/折叠（第十一章）
            item.setExpanded(layer.expanded)

        self._tree.blockSignals(False)
        self._current_index = active_index
        
        # 第二十三章 - 查找对象：选中对象时图层面板自动定位到对应图层；
        if 0 <= active_index < len(layers):
        # 确保索引有效
            # 面板反序显示，数据索引需转换为树索引：tree_index = total - 1 - data_index
            tree_index = len(layers) - 1 - active_index
            active_item = self._tree.topLevelItem(tree_index)
            # 获取活跃图层的树节点
            if active_item:
                self._tree.scrollToItem(active_item, QTreeWidget.PositionAtCenter)

    def _create_layer_item(self, layer: Layer, index: int) -> QTreeWidgetItem:
        # 为单个图层创建树节点
        """创建图层树节点，1:1 对照 Ai 图层面板
        
        Ai 图层面板结构（从左到右）：
        1. 展开箭头 (▶) — 展开/折叠图层内容（第十一章）
        2. 眼睛图标 (👁) — 可见性（第七章）
        3. 锁定区域 (🔒) — 锁定状态（第八章）
        4. 目标圆圈 (◎) — 效果作用目标（第二十四章）
        5. 图层颜色方块 — 标识图层（第二十章）
        6. 图层名称 — 双击可重命名（第四章）
        """
        # 锁定图标（第八章）— 放在最前面，周围加空格增大点击区域
        lock = " 🔒 " if layer.locked else " 🔓 "
        # 预览模式标识（第二十二章）
        preview_indicator = "◉" if layer.preview_mode == "outline" else "◎"
        # 模板图标（第十九章）
        template = "📐" if layer.is_template else " "
        # 打印状态（第二十一章）— 不可打印用斜体标识
        print_indicator = "" if layer.printable else "✕ "
        # 可见性图标（第七章）— 放在最后面，周围加空格增大点击区域
        # ★ 不可见时用 ◌ 占位（确保点击区域始终存在，避免第二次点击无法切换回来）
        eye = " 👁 " if layer.visible else " ◌  "
        
        name = layer.name
        
        # 显示对象数量
        item_count = len(layer.items)
        sub_count = len(layer.sublayers)
        detail = f" ({item_count})" if item_count > 0 else ""
        sub_detail = f" [{sub_count}]" if sub_count > 0 else ""
        
        # 拼合显示文本：锁 目标 名称 数量 眼睛（眼睛在最后）
        display_text = f"{lock}{preview_indicator} {print_indicator}{name}{detail}{sub_detail}{eye}"
        # 用显示文本创建树节点
        item = QTreeWidgetItem([display_text])
        item.setData(0, Qt.UserRole, index)
        item.setData(0, Qt.UserRole + 1, "layer")
        item.setData(0, Qt.UserRole + 2, layer.id)
        item.setData(0, Qt.UserRole + 4, layer.color.name() if layer.color else "")  # 彩色方块数据

        # 图层颜色标识（第二十章）— 路径边框颜色
        if layer.color:
            item.setForeground(0, layer.color)
        # 如果是模版图层
        if layer.is_template:
            # 模板图层灰色显示（第十九章）
            item.setForeground(0, QColor(128, 128, 128))
        if not layer.printable:
            # 不打印的图层用斜体显示（第二十一章）
            font = item.font(0)
            font.setItalic(True)
            item.setFont(0, font)
        if layer.preview_mode == "outline":
            # 轮廓模式用不同背景色提示（第二十二章）
            item.setBackground(0, QColor(50, 45, 40))

        # 子图层（第十章）；添加子图层节点
        for si, sub in enumerate(layer.sublayers):
            sub_item = self._create_sublayer_item(sub, index, si)
            item.addChild(sub_item)

        # 对象列表（展开图层可查看路径、文字、图像等 — 第十一章、第十二章）
        # 正序显示：items[0] 在面板最上方 = 视觉顶层 = 后绘制
        # items[-1] 在面板最下方 = 视觉底层 = 先绘制
        # 
        # 对照 AI：图层面板列出所有对象(Path/Text/Group…)，不只是 Layer
        # GroupItem 递归展开显示内部元素
        if layer.expanded and layer.items:
            for oi, obj in enumerate(layer.items):
                self._add_object_tree_item(item, obj, oi, index, layer)

        # 图层项可拖拽（第九章 — 图层排序）
        item.setFlags(item.flags() | Qt.ItemIsDragEnabled)
        
        return item

    def _add_object_tree_item(
        self, parent_item: QTreeWidgetItem, obj, obj_index: int,
        layer_index: int, layer, depth: int = 0,
    ):
        """递归添加对象到树节点（支持 GroupItem 内部元素展开）

        对照 AI：图层面板是 Scene Graph 的 Outline View，列出 Layer/SubLayer/Group/Path/Text 等所有节点

        Args:
            parent_item: 父级树节点
            obj: GraphicItem 对象
            obj_index: 对象在父列表中的索引
            layer_index: 所属图层索引
            layer: 所属图层对象
            depth: 嵌套深度（用于缩进）
        """
        from ..core.graphics import GroupItem

        obj_type = obj.item_type.replace("Item", "")
        obj_name = obj.name or f"<{obj_type}>"
        indent = "  " * depth  # 嵌套缩进

        # 对象锁定图标 — 放在最前面，周围加空格增大点击区域
        obj_lock = " 🔒 " if obj.locked else " 🔓 "
        # 对象类型图标
        type_icon = self._get_item_type_icon(obj)
        # 对象可见性图标（第七章扩展 - 对象级显隐）— 放在最后面，周围加空格
        # ★ 不可见时用 ◌ 占位（确保点击区域始终存在）
        obj_eye = " 👁 " if getattr(obj, 'visible', True) else " ◌  "

        obj_item = QTreeWidgetItem([f"{indent}{obj_lock}{type_icon} {obj_name}{obj_eye}"])
        obj_item.setData(0, Qt.UserRole, obj_index)
        obj_item.setData(0, Qt.UserRole + 1, "object")
        obj_item.setData(0, Qt.UserRole + 2, obj.id)
        obj_item.setData(0, Qt.UserRole + 3, layer_index)  # 父图层索引

        # 对象使用图层颜色（第二十章）— 彩色方块
        if layer.color:
            obj_item.setForeground(0, QColor(
                layer.color.red(), layer.color.green(),
                layer.color.blue(), 180
            ))

        # 对象可拖拽排序（第十二章 — 对象层级管理）
        obj_item.setFlags(obj_item.flags() | Qt.ItemIsDragEnabled)

        parent_item.addChild(obj_item)

        # ── 对照 AI：GroupItem 递归展开内部元素 ──
        if isinstance(obj, GroupItem) and obj.items:
            obj_item.setFlags(obj_item.flags() | Qt.ItemIsDragEnabled)
            for gi, group_child in enumerate(obj.items):
                self._add_object_tree_item(
                    obj_item, group_child, gi, layer_index, layer, depth + 1,
                )

    @staticmethod
    def _get_item_type_icon(obj) -> str:
        """获取对象类型图标（第十一章）"""
        from ..core.graphics import PathItem, RectangleItem, EllipseItem, TextFrame, GroupItem
        match obj:
            case PathItem():
                return "✏"  # 路径
            case RectangleItem():
                return "▬"  # 矩形
            case EllipseItem():
                return "⬭"  # 椭圆
            case TextFrame():
                return "T"  # 文字
            case GroupItem():
                return "📁"  # 群组
            case _:
                return "●"  # 默认

    def _create_sublayer_item(self, sublayer: Layer, parent_idx: int, sub_idx: int) -> QTreeWidgetItem:
        """创建子图层树节点（第十章）"""
        # 为子图层创建树节点 — 锁在最前，眼睛在最后，周围加空格
        lock = " 🔒 " if sublayer.locked else " 🔓 "
        preview_indicator = "◎"
        # ★ 不可见时用 ◌ 占位（确保点击区域始终存在）
        eye = " 👁 " if sublayer.visible else " ◌  "
        
        item = QTreeWidgetItem([f"{lock}{preview_indicator} {sublayer.name}{eye}"])
        item.setData(0, Qt.UserRole, sub_idx)
        item.setData(0, Qt.UserRole + 1, "sublayer")
        item.setData(0, Qt.UserRole + 2, sublayer.id)
        item.setData(0, Qt.UserRole + 3, parent_idx)
        
        if sublayer.color:
            item.setForeground(0, sublayer.color)
        
        # 子图层也可拖拽排序
        item.setFlags(item.flags() | Qt.ItemIsDragEnabled)
        
        return item

    # ── 事件处理 ──

    def _on_item_changed(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        # 处理树控件选中项变更事件
        if current is None:
            return
        item_type = current.data(0, Qt.UserRole + 1)
        if item_type == "layer":
            # ★ 关键修复：使用辅助方法实时计算 data index
            index = self._get_layer_data_index(current)
            if index is not None and 0 <= index < len(self._layers_data):
                self._current_index = index
                self.layer_selected.emit(index)
        elif item_type == "sublayer":
            # ★ 修复：实时计算 sublayer 的 parent_idx
            _, parent_idx = self._get_sublayer_data_indices(current)
            if parent_idx is not None:
                self._current_index = parent_idx
                self.layer_selected.emit(parent_idx)

    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """双击重命名图层（PDF 六）"""
        # 方法文档字符串
        item_type = item.data(0, Qt.UserRole + 1)
        if item_type in ("layer", "sublayer"):
            # ★ 修复：使用辅助方法实时计算 index
            if item_type == "layer":
                index = self._get_layer_data_index(item)
            else:
                index, _ = self._get_sublayer_data_indices(item)
            if index is not None:
                self._start_rename(item, item_type, index)

    def _start_rename(self, item: QTreeWidgetItem, item_type: str, index: int):
        """启动内联重命名"""
        from PyQt5.QtWidgets import QLineEdit
        current_text = ""
        if item_type == "layer" and index < len(self._layers_data):
            current_text = self._layers_data[index].name
        elif item_type == "sublayer":
            parent_idx = item.data(0, Qt.UserRole + 3)
            if parent_idx is not None and parent_idx < len(self._layers_data):
                parent = self._layers_data[parent_idx]
                if index < len(parent.sublayers):
                    current_text = parent.sublayers[index].name
        # 创建行编辑框，初始化文本为当前名称
        editor = QLineEdit(current_text, self._tree)
        editor.setFocus()
        editor.selectAll()
        self._tree.setItemWidget(item, 0, editor)
        # 将编辑框设为节点的内嵌控件
        self._editing_index = index
        # 记录正在编辑的索引

        def finish_rename():
            # 嵌套函数：完成重命名
            new_name = editor.text().strip()
            try:
                # 检查 item 是否仍然有效
                if item not in self._tree.findItems("", Qt.MatchContains | Qt.MatchRecursive, 0):
                    return
                self._tree.removeItemWidget(item, 0)
            except RuntimeError:
                return
            if new_name and new_name != current_text:
                if item_type == "layer":
                    self.layer_rename_requested.emit(index, new_name)
                elif item_type == "sublayer":
                    self.layer_rename_requested.emit(-(index + 1), new_name)
        # 回车键确认重命名
        editor.returnPressed.connect(finish_rename)
        editor.editingFinished.connect(lambda: None)  # 防止重复触发
    # 处理项目数据变更事实
    def _on_item_changed_flag(self, item: QTreeWidgetItem, column: int):
        """项目状态改变（预留）"""
        pass

    def _on_rows_moved(self, parent, start, end, dest, row):
        # 处理拖拽排序完成事件
        """拖拽排序图层（第九章）或对象排序（第十二章）
        
        QTreeWidget InternalMove 在信号发出前已完成节点的物理移动，
        因此 start/row 对应移动前后的树索引。
        
        关键区分：
        - parent 无效（QModelIndex() 或 is_valid()==False）→ 拖拽的是顶层图层
        - parent 有效 → 拖拽的是某节点下的子对象
        
        ★ 关键修复：移除 QTimer.singleShot 延迟，直接在 rowsMoved 中同步处理。
        原因：拖拽操作会启动嵌套事件循环，QTimer.singleShot(0) 在嵌套循环中
        可能永不触发或严重延迟，导致信号根本不发射 → 画布不更新。
        改为同步处理：立即发射信号 → main_window 收到后立刻 reorder_layer + repaint。
        """
        if start == row:
            return

        # ── 判断是图层拖拽（顶层）还是对象拖拽（子节点） ──
        if not parent.isValid():
            # === 图层拖拽：topLevelItem ===
            total = self._tree.topLevelItemCount()
            if start >= total or row >= total:
                return
            item = self._tree.topLevelItem(row)
            if item is None:
                return
            item_type = item.data(0, Qt.UserRole + 1)
            if item_type != "layer":
                return

            # 面板反序显示：树第0行 = layers[-1]（顶层），树最后行 = layers[0]（底层）
            # 转换：data_index = total - 1 - tree_index
            data_start = total - 1 - start
            data_row = total - 1 - row

            # ★ 同步更新 _layers_data（避免在信号处理期间处于过时状态）
            if 0 <= data_start < len(self._layers_data):
                moved_layer = self._layers_data.pop(data_start)
                # 移除后列表长度减1，目标索引需要 clamp
                target_idx = max(0, min(data_row, len(self._layers_data)))
                self._layers_data.insert(target_idx, moved_layer)
                self._current_index = target_idx

            layer_name = item.data(0, Qt.UserRole + 3) or f"图层{data_start}"
            layer_count = len(self._layers_data)
            print(f"[图层拖拽] 图层「{layer_name}」: 面板位置 {start}→{row}, 数据索引 {data_start}→{data_row}, 总图层数 {layer_count}")
            print(f"  → 拖拽后图层顺序: {[ly.name for ly in reversed(self._layers_data)]}")

            # ★ 同步发射信号（无延迟），确保 main_window 立即收到并更新画布
            self.layer_reorder_requested.emit(data_start, data_row)

        else:
            # === 对象拖拽：子节点 ===
            # parent 是 QModelIndex，指向父 QTreeWidgetItem（图层或 GroupItem）
            parent_item = self._tree.itemFromIndex(parent)
            if parent_item is None:
                return

            # 从父节点取子项：子项在 QTreeWidget InternalMove 后已按新顺序排列
            child_count = parent_item.childCount()
            # ★ 关键修复：允许 row == child_count（拖到末尾），只拒绝 row > child_count
            if start >= child_count or row > child_count:
                return

            # ★ 关键修复：Qt moveRows 语义——同一父节点内向下拖时，
            # destinationRow > sourceStart，实际插入位置 = destinationRow - 1
            # 因为先移除 sourceStart 后列表缩短，再插入到 destinationRow
            data_from = start
            if row > start:
                data_to = row - 1
            else:
                data_to = row

            # 验证目标位置在有效范围内
            if data_to < 0 or data_to >= child_count:
                return

            moved_child = parent_item.child(data_to)
            if moved_child is None:
                return

            item_type = moved_child.data(0, Qt.UserRole + 1)
            if item_type != "object":
                return

            # 获取所属图层索引（递归向上查找图层节点）
            layer_idx = self._find_parent_layer_index(parent_item)
            if layer_idx is None:
                print(f"[对象拖拽] ❌ 无法找到父图层索引，parent_item={parent_item}")
                return

            # ★ 面板正序显示：树 child(0) = items[0] = 视觉顶层
            # 行号直接对应 items 索引，无需转换

            # ★ 详细调试日志
            moved_name = moved_child.text(0).strip()[:30] if moved_child.text(0) else "?"
            print(f"\n[对象拖拽] ═══════════════════════════════════")
            print(f"[对象拖拽] 名称={moved_name}, 图层={layer_idx}")
            print(f"[对象拖拽] 树位置: start={start} → row={row}")
            print(f"[对象拖拽] 数据位置: from={data_from} → to={data_to}")
            print(f"[对象拖拽] 子项总数={child_count}")
            # 打印拖拽后所有子项（验证树状态）
            child_names = []
            for ci in range(min(child_count, 20)):
                ch = parent_item.child(ci)
                child_names.append(ch.text(0).strip()[:20] if ch and ch.text(0) else "?")
            print(f"[对象拖拽] 树中子项顺序: {child_names}")

            # ★ 同步发射信号（无延迟），传递 parent_item 以支持 GroupItem 内部拖拽
            self.item_order_changed.emit(layer_idx, data_from, data_to, parent_item)

    def _get_icon_click_regions(self, item: QTreeWidgetItem) -> tuple[int, int, int, int]:
        """精确计算眼睛和锁图标的像素点击区域（0 容差）

        逐字符累加像素宽度，确保只有精确点击到 👁 或 🔒/🔓 图标时
        才触发对应操作。

        QFontMetrics.horizontalAdvance 在某些字体下对 emoji 返回 0 宽度
        （如 SimSun 不支持 🔒），因此改为逐字符累加并使用回退宽度。

        注意：返回的坐标是相对于 item 文本起始位置的像素偏移，
        调用方需要将 click_x 也对齐到同一坐标系（减去 visualItemRect 中
        非文本部分的偏移，即缩进 + 展开按钮宽度）。

        Returns:
            (eye_start, eye_end, lock_start, lock_end) — 像素坐标（相对文本起点）
        """
        from PyQt5.QtGui import QFontMetrics

        text = item.text(0)
        fm = QFontMetrics(self._tree.font())

        # emoji 回退宽度：当 QFontMetrics 返回 0 时使用此值
        # averageCharWidth 通常是英文字符宽度（约 6px），emoji 通常为 2 倍
        emoji_fallback = max(fm.averageCharWidth() * 2, 12)

        # 逐字符累加宽度，找到每个字符的像素边界
        # widths[i] = 字符 text[i] 的起始像素位置
        widths = [0]
        for ch in text:
            char_w = fm.horizontalAdvance(ch)
            if char_w <= 0:
                # QFontMetrics 不支持该字符（如 emoji），使用回退宽度
                char_w = emoji_fallback
            widths.append(widths[-1] + char_w)

        # 在文本中找到眼睛和锁的字符索引
        # 新格式：锁在最前，眼睛在最后
        # 图层/子图层: "🔒◎ ...👁"  或  "  🔒● ...👁"（对象）
        # 锁可能是 🔒（已锁定）或 🔓（未锁定）
        # ★ 眼睛可能是 👁（可见）或 ◌（不可见占位符）
        eye_idx = -1
        lock_idx = -1

        for i, ch in enumerate(text):
            if ch in ('🔒', '🔓') and lock_idx == -1:
                lock_idx = i
            elif ch in ('👁', '◌') and eye_idx == -1:
                eye_idx = i
            # 继续遍历，因为眼睛可能在锁之后很远的位置

        if eye_idx == -1 or lock_idx == -1:
            return (0, 0, 0, 0)

        eye_start = widths[eye_idx]
        eye_end = widths[eye_idx + 1]
        lock_start = widths[lock_idx]
        lock_end = widths[lock_idx + 1]

        return (eye_start, eye_end, lock_start, lock_end)

    def _get_text_x_offset_in_item_rect(self, item: QTreeWidgetItem) -> int:
        """计算 item 文本在 visualItemRect 内的起始 x 偏移。

        使用 QTreeWidget 的 viewport 坐标系：
        - visualItemRect(item) 返回 item 在 viewport 中的完整矩形
        - 该矩形左边界包含：margin + 展开按钮 + 树缩进
        - 文本实际渲染位置需要通过 QStyle 的 SE_ItemViewItemText 获取

        更可靠的方法：利用 QTreeWidget 的 visualRect 和 itemDelegate 的
        text 位置，或者直接计算文本在 item 矩形中的偏移。

        这里使用实测法：比较 item 文本第一个非空格字符的 visual 位置
        和 item 矩形的左边界，得到文本起始偏移。
        """
        # 方法：使用 QStyle 获取 item view 的文本矩形
        # 通过构造一个 QStyleOptionViewItem 并查询 subElementRect
        from PyQt5.QtWidgets import QStyleOptionViewItem
        from PyQt5.QtCore import QModelIndex

        # 获取 item 在模型中的索引
        index = self._tree.indexFromItem(item)
        if not index.isValid():
            return 0

        # 构造 style option
        option = QStyleOptionViewItem()
        option.rect = self._tree.visualRect(index)
        option.state = QStyle.State_Enabled | QStyle.State_Active
        if item == self._tree.currentItem():
            option.state |= QStyle.State_Selected
        option.viewItemPosition = QStyleOptionViewItem.Middle

        # 获取文本矩形
        style = self._tree.style()
        text_rect = style.subElementRect(
            QStyle.SE_ItemViewItemText, option, self._tree
        )

        # 文本矩形相对于 item 矩形的偏移
        text_offset = text_rect.x() - option.rect.x()

        # 兜底：如果计算失败（offset <= 0），使用经验值
        if text_offset <= 0:
            # 计算深度
            depth = 0
            parent = item.parent()
            while parent:
                depth += 1
                parent = parent.parent()
            tree_indent = self._tree.indentation() * depth
            expand_btn = style.pixelMetric(QStyle.PM_IndicatorWidth, None, self._tree) + 4
            text_offset = tree_indent + expand_btn

        return text_offset

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """点击图层项处理

        核心功能（实际生效）：
        - 点击 🔒 锁定区域（锁+前后空格） → 切换图层/对象锁定状态
        - 点击 👁/◌ 眼睛区域（眼睛+前后空格） → 切换图层/对象可见性
        - 点击对象名称 → 选中画布上的对应对象
        - 点击图层行 → 设置目标图层

        锁和眼睛周围已加空格增大点击区域（约 28px），并增加 ±4px 容差。
        
        ★ 坐标获取策略（按优先级）：
        1. self._last_click_pos — 由 eventFilter 在每次 viewport MouseButtonPress 时更新
        2. QCursor.pos() — 兜底方案（仅在 eventFilter 未触发时使用）
        """
        item_type = item.data(0, Qt.UserRole + 1)

        # ★ 使用 eventFilter 记录的 viewport 坐标系点击位置
        if self._last_click_pos is not None:
            pos = self._last_click_pos
        else:
            # 兜底：使用当前鼠标位置（映射到 viewport 坐标系）
            pos = self._tree.viewport().mapFromGlobal(QCursor.pos())

        item_rect = self._tree.visualItemRect(item)

        # 计算文本在 item 矩形中的起始 x 偏移
        text_x_offset = self._get_text_x_offset_in_item_rect(item)
        click_x = pos.x() - item_rect.x() - text_x_offset

        # 计算眼睛和锁的像素区域（相对于文本起点）
        eye_start, eye_end, lock_start, lock_end = self._get_icon_click_regions(item)

        # ★ 增加 ±4px 容差，确保更容易命中图标区域
        TOLERANCE = 4
        hit_eye = (eye_start - TOLERANCE) <= click_x < (eye_end + TOLERANCE)
        hit_lock = (lock_start - TOLERANCE) <= click_x < (lock_end + TOLERANCE)

        # ★ 调试日志（可在稳定后移除）
        # print(f"[_on_item_clicked] type={item_type} click_x={click_x:.0f} "
        #       f"eye=({eye_start:.0f},{eye_end:.0f}) lock=({lock_start:.0f},{lock_end:.0f}) "
        #       f"hit_eye={hit_eye} hit_lock={hit_lock}")

        if item_type == "layer":
            # ★ 从树位置实时计算数据索引，避免拖拽后使用过时的 Qt.UserRole
            index = self._get_layer_data_index(item)
            if index is None or not (0 <= index < len(self._layers_data)):
                return
            layer = self._layers_data[index]

            if hit_eye:
                layer.visible = not layer.visible
                self.layer_visibility_changed.emit(index, layer.visible)
                self._refresh_display()
            elif hit_lock:
                layer.locked = not layer.locked
                self.layer_locked_changed.emit(index, layer.locked)
                self._refresh_display()
            else:
                self.layer_target_requested.emit(index)

        elif item_type == "object":
            # ★ 从树位置实时计算对象索引和图层索引
            obj_index, layer_index = self._get_object_data_indices(item)
            if layer_index is None or obj_index is None:
                return
            if not (0 <= layer_index < len(self._layers_data)):
                return
            layer = self._layers_data[layer_index]
            if obj_index is None or not (0 <= obj_index < len(layer.items)):
                return
            obj = layer.items[obj_index]

            if hit_eye:
                obj.visible = not obj.visible
                self.item_visibility_toggled.emit(obj, obj.visible)
                self._refresh_display()
            elif hit_lock:
                obj.locked = not obj.locked
                self.item_locked_toggled.emit(obj, obj.locked)
                self._refresh_display()
            else:
                self.item_select_requested.emit(layer_index, obj_index)

        elif item_type == "sublayer":
            # ★ 从树位置实时计算子图层索引和父图层索引
            sub_idx, parent_idx = self._get_sublayer_data_indices(item)
            if parent_idx is None or sub_idx is None:
                return
            if not (0 <= parent_idx < len(self._layers_data)):
                return
            parent_layer = self._layers_data[parent_idx]
            if sub_idx is None or not (0 <= sub_idx < len(parent_layer.sublayers)):
                return
            sublayer = parent_layer.sublayers[sub_idx]

            if hit_eye:
                sublayer.visible = not sublayer.visible
                self.layer_visibility_changed.emit(parent_idx, sublayer.visible)
                self._refresh_display()
            elif hit_lock:
                sublayer.locked = not sublayer.locked
                self.layer_locked_changed.emit(parent_idx, sublayer.locked)
                self._refresh_display()

    def _refresh_display(self):
        """刷新图层面板显示"""
        self.update_layers(self._layers_data, self._current_index)

    def eventFilter(self, obj, event):
        """事件过滤器：精确捕获 QTreeWidget viewport 上的鼠标点击坐标
        
        这是解决"第二次点击无法触发"问题的核心机制。
        QTreeWidget 是 LayersPanel 的子控件，其 viewport 的鼠标事件
        不会冒泡到 LayersPanel.mousePressEvent。通过安装事件过滤器，
        我们在事件到达 viewport 之前拦截并记录精确坐标。
        """
        from PyQt5.QtCore import QEvent
        if obj is self._tree.viewport() and event.type() == QEvent.MouseButtonPress:
            # 记录 viewport 坐标系中的点击位置
            self._last_click_pos = event.pos()
        return super().eventFilter(obj, event)

    # ── 拖拽到垃圾桶删除（第五章方法2） ──

    def _on_trash_drag_enter(self, event):
        """拖拽到垃圾桶时的视觉反馈"""
        if self._trash_bin:
            self._trash_bin.setStyleSheet("""
                QPushButton { background-color: #dc3545; color: white; 
                border: 2px solid #ff4444; border-radius: 3px; font-weight: bold; }
            """)

    def _on_trash_drag_move(self, event):
        # 垃圾桶按钮拖拽移动事件
        event.accept()

    def _on_trash_drop(self, event):
        """拖拽图层到垃圾桶删除（第五章方法2）"""
        if self._trash_bin:
            self._trash_bin.setStyleSheet("")
        # 获取当前选中的图层
        idx = self._current_index
        if 0 <= idx < len(self._layers_data):
            self.layer_remove_requested.emit(idx)
        event.accept()

    # ── 拖拽到新建按钮复制（第六章） ──

    def _on_add_btn_drag_enter(self, event):
        """拖拽到新建按钮时的视觉反馈"""
        if self._add_btn:
            self._add_btn.setStyleSheet("""
                QPushButton { background-color: #0d6efd; color: white; 
                border: 2px solid #4da3ff; border-radius: 3px; font-weight: bold; }
            """)

    def _on_add_btn_drag_move(self, event):
        # 新建按钮拖拽移动事件
        event.accept()

    def _on_add_btn_drop(self, event):
        """拖拽图层到新建按钮复制（第六章）"""
        if self._add_btn:
            self._add_btn.setStyleSheet("")
        idx = self._current_index
        if 0 <= idx < len(self._layers_data):
            self.layer_duplicate_requested.emit(idx)
        event.accept()

    # ── 右键菜单（完整对照 Ai 图层面板菜单） ──

    def _on_context_menu(self, pos):
        """右键菜单：完整图层和对象操作
        
        图层操作：新建/复制/删除/重命名/合并/拼合等
        对象操作：选中/删除/复制/显隐/锁定/上下移动
        """
        # 根据右键点击的节点(空白区域为none)
        item = self._tree.itemAt(pos)
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; padding: 4px; }
            QMenu::item { padding: 6px 24px; }
            QMenu::item:selected { background-color: #0d6efd; }
            QMenu::separator { height: 1px; background: #555; margin: 4px 8px; }
        """)
        # 当前图层索引
        idx = self._current_index
        layer = self._layers_data[idx] if 0 <= idx < len(self._layers_data) else None
        # 获取当前图层对象
        item_type = item.data(0, Qt.UserRole + 1) if item else None
        # 获取节点类型
        if item_type == "object":
            # ── 对象级右键菜单 ──
            obj_index = item.data(0, Qt.UserRole)
            layer_index = item.data(0, Qt.UserRole + 3)
            if (layer_index is not None and 0 <= layer_index < len(self._layers_data)
                    and obj_index is not None and 0 <= obj_index < len(self._layers_data[layer_index].items)):
                obj = self._layers_data[layer_index].items[obj_index]
                obj_name = obj.name or f"<{obj.item_type.replace('Item', '')}>"
                
                # 选中对象
                sel_action = menu.addAction(f"  选中「{obj_name}」")
                sel_action.triggered.connect(lambda: self.item_select_requested.emit(layer_index, obj_index))
                
                menu.addSeparator()
                
                # 删除对象
                del_action = menu.addAction(f"  删除「{obj_name}」")
                del_action.triggered.connect(lambda: self.item_delete_requested.emit(obj))
                
                # 复制对象
                dup_action = menu.addAction(f"  复制「{obj_name}」")
                dup_action.triggered.connect(lambda: self.item_duplicate_requested.emit(obj))
                
                menu.addSeparator()
                
                # 显隐切换
                vis_text = f"  隐藏「{obj_name}」" if obj.visible else f"  显示「{obj_name}」"
                vis_action = menu.addAction(vis_text)
                vis_action.triggered.connect(lambda: self.item_visibility_toggled.emit(obj, not obj.visible))
                
                # 锁定切换
                lock_text = f"  锁定「{obj_name}」" if not obj.locked else f"  解锁「{obj_name}」"
                lock_action = menu.addAction(lock_text)
                lock_action.triggered.connect(lambda: self.item_locked_toggled.emit(obj, not obj.locked))
                
                menu.addSeparator()
                
                # 上移一层
                up_action = menu.addAction("  上移一层 (Bring Forward)")
                up_action.triggered.connect(lambda: self.item_bring_forward_requested.emit(obj))
                
                # 下移一层
                down_action = menu.addAction("  下移一层 (Send Backward)")
                down_action.triggered.connect(lambda: self.item_send_backward_requested.emit(obj))
                
                # 置顶
                front_action = menu.addAction("  置顶 (Bring to Front)")
                front_action.triggered.connect(lambda: self._on_item_bring_to_front(obj, layer_index))
                
                # 置底
                back_action = menu.addAction("  置底 (Send to Back)")
                back_action.triggered.connect(lambda: self._on_item_send_to_back(obj, layer_index))

        elif item_type in ("layer", "sublayer"):
            # ── 图层级右键菜单（原有功能）──
            # 新建图层（第三章方法2）
            new_layer_action = menu.addAction("  新建图层")
            new_layer_action.triggered.connect(self.layer_add_requested.emit)

            # 新建子图层（第十章）
            new_sublayer_action = menu.addAction("  新建子图层")
            new_sublayer_action.triggered.connect(self._on_add_sublayer)

            menu.addSeparator()

            if layer is not None:
                # 复制图层（第六章）
                dup_action = menu.addAction(f"  复制 \"{layer.name}\"")
                dup_action.triggered.connect(lambda: self.layer_duplicate_requested.emit(idx))

                # 删除图层（第五章方法1）
                del_action = menu.addAction(f"  删除 \"{layer.name}\"")
                del_action.triggered.connect(lambda: self.layer_remove_requested.emit(idx))

                menu.addSeparator()

                # 当前图层的选项...
                options_action = menu.addAction(f"  \"{layer.name}\" 的选项...")
                options_action.triggered.connect(lambda: self._show_layer_options_dialog(idx))

                menu.addSeparator()

                # 收集到新图层（第十五章）
                collect_action = menu.addAction("  收集到新图层")
                collect_action.triggered.connect(self.layer_collect_requested.emit)

                # 释放到图层（第十六章）
                release_menu = menu.addMenu("  释放到图层")
                seq_action = release_menu.addAction("顺序 (Sequence)")
                seq_action.triggered.connect(self.layer_release_sequence_requested.emit)
                build_action = release_menu.addAction("构建 (Build)")
                build_action.triggered.connect(self.layer_release_build_requested.emit)

                menu.addSeparator()

                # 合并图层（第十七章）
                merge_action = menu.addAction("  合并选定图层")
                merge_action.triggered.connect(lambda: self.layer_merge_requested.emit([idx]))

                # 拼合图稿（第十八章）
                flatten_action = menu.addAction("  拼合图稿")
                flatten_action.triggered.connect(self.layer_flatten_requested.emit)

                menu.addSeparator()

                # 隐藏/显示其他图层
                if layer.visible:
                    hide_others = menu.addAction("  隐藏其他图层")
                    hide_others.triggered.connect(lambda: self._hide_other_layers(idx))

                # 锁定其他图层
                if not layer.locked:
                    lock_others = menu.addAction("  锁定其他图层")
                    lock_others.triggered.connect(lambda: self._lock_other_layers(idx))

                # 显示所有图层
                show_all = menu.addAction("  显示所有图层")
                show_all.triggered.connect(self._show_all_layers)

                # 解锁所有图层
                unlock_all = menu.addAction("  解锁所有图层")
                unlock_all.triggered.connect(self._unlock_all_layers)

        else:
            # 空白区域右键 → 基础菜单
            new_layer_action = menu.addAction("  新建图层")
            new_layer_action.triggered.connect(self.layer_add_requested.emit)
            
            show_all = menu.addAction("  显示所有图层")
            show_all.triggered.connect(self._show_all_layers)
            
            unlock_all = menu.addAction("  解锁所有图层")
            unlock_all.triggered.connect(self._unlock_all_layers)

        menu.addSeparator()

        # 面板选项
        panel_opts = menu.addAction("  面板选项...")
        panel_opts.triggered.connect(self._show_panel_options)

        menu.exec_(self._tree.mapToGlobal(pos))

    def _on_item_bring_to_front(self, obj, layer_index: int):
        """对象置顶"""
        if 0 <= layer_index < len(self._layers_data):
            self._layers_data[layer_index].bring_to_front(obj)
            self._refresh_display()

    def _on_item_send_to_back(self, obj, layer_index: int):
        """对象置底"""
        if 0 <= layer_index < len(self._layers_data):
            self._layers_data[layer_index].send_to_back(obj)
            self._refresh_display()

    def _hide_other_layers(self, except_idx: int):
        """隐藏除指定图层外的所有图层"""
        # 隐藏除指定图层外的所有图层
        for i, layer in enumerate(self._layers_data):
            if i != except_idx:
                layer.visible = False
                self.layer_visibility_changed.emit(i, False)

    def _lock_other_layers(self, except_idx: int):
        """锁定除指定图层外的所有图层"""
        for i, layer in enumerate(self._layers_data):
            if i != except_idx:
                layer.locked = True
                self.layer_locked_changed.emit(i, True)

    def _show_all_layers(self):
        """显示所有图层"""
        for i, layer in enumerate(self._layers_data):
            if not layer.visible:
                layer.visible = True
                self.layer_visibility_changed.emit(i, True)

    def _unlock_all_layers(self):
        """解锁所有图层"""
        for i, layer in enumerate(self._layers_data):
            if layer.locked:
                layer.locked = False
                self.layer_locked_changed.emit(i, False)

    def _show_layer_options_dialog(self, index: int):
        """图层选项对话框
        
        对照 Ai 图层选项对话框（第三章 + 第十九-二十二章）：
        - 名称 (Name) — 第四章
        - 颜色 (Color) — 第二十章
        - 模板 (Template) — 第十九章
        - 打印 (Print) — 第二十一章
        - 预览 (Preview) — 第二十二章
        - 锁定 (Lock) — 第八章
        - 显示 (Show) — 第七章
        - 变暗图像至 (Dim Images) — 第十九章扩展
        对话框、表单布局、对话框按钮组件
        """
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
        
        if not (0 <= index < len(self._layers_data)):
            return
        layer = self._layers_data[index]
        
        dlg = QDialog(self)
        dlg.setWindowTitle("图层选项")
        dlg.setMinimumWidth(320)
        dlg.setStyleSheet("""
            QDialog { background-color: #3c3c3c; color: #ddd; }
            QLabel { color: #bbb; }
            QLineEdit { background-color: #2d2d2d; color: #ddd; border: 1px solid #555; padding: 4px; }
            QComboBox { background-color: #2d2d2d; color: #ddd; border: 1px solid #555; padding: 4px; }
            QCheckBox { color: #bbb; }
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; padding: 6px 16px; border-radius: 3px; }
            QPushButton:hover { background-color: #5a5a5a; }
        """)
        
        layout = QFormLayout(dlg)
        
        # 名称
        name_edit = QLineEdit(layer.name)
        name_edit.selectAll()
        layout.addRow("名称(&N):", name_edit)
        
        # 颜色（第二十章）
        color_combo = QComboBox()
        color_combo.addItem("无", None)
        for ci, c in enumerate(self.LAYER_COLORS):
            color_combo.addItem(f"颜色 {ci + 1}", c)
            # 设置项目的背景颜色数据
            color_combo.setItemData(ci + 1, c, Qt.BackgroundRole)
        
        # 选择当前颜色
        if layer.color:
            for ci, c in enumerate(self.LAYER_COLORS):
                if layer.color.name() == c.name():
                    color_combo.setCurrentIndex(ci + 1)
                    break
        layout.addRow("颜色(&C):", color_combo)
        
        # 模板（第十九章）
        template_check = QCheckBox("模板(&T)")
        template_check.setChecked(layer.is_template)
        layout.addRow("", template_check)
        
        # 打印（第二十一章）
        print_check = QCheckBox("打印(&P)")
        print_check.setChecked(layer.printable)
        layout.addRow("", print_check)
        
        # 预览（第二十二章）
        preview_check = QCheckBox("预览(&V)")
        preview_check.setChecked(layer.preview_mode == "preview")
        layout.addRow("", preview_check)
        
        # 锁定（第八章）
        lock_check = QCheckBox("锁定(&L)")
        lock_check.setChecked(layer.locked)
        layout.addRow("", lock_check)
        
        # 显示（第七章）
        show_check = QCheckBox("显示(&S)")
        show_check.setChecked(layer.visible)
        layout.addRow("", show_check)
        
        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addRow(buttons)
        
        if dlg.exec_() == QDialog.Accepted:
            new_name = name_edit.text().strip()
            if new_name and new_name != layer.name:
                layer.name = new_name
                self.layer_rename_requested.emit(index, new_name)
            
            # 颜色
            new_color = color_combo.currentData()
            if new_color != layer.color:
                layer.color = new_color
                self.layer_color_changed.emit(index, new_color)
            
            # 模板
            if template_check.isChecked() != layer.is_template:
                layer.is_template = template_check.isChecked()
                self.layer_template_changed.emit(index, layer.is_template)
            
            # 打印
            if print_check.isChecked() != layer.printable:
                layer.printable = print_check.isChecked()
                self.layer_printable_changed.emit(index, layer.printable)
            
            # 预览
            new_mode = "preview" if preview_check.isChecked() else "outline"
            if new_mode != layer.preview_mode:
                layer.preview_mode = new_mode
                self.layer_preview_mode_changed.emit(index, new_mode)
            
            # 锁定
            if lock_check.isChecked() != layer.locked:
                layer.locked = lock_check.isChecked()
                self.layer_locked_changed.emit(index, layer.locked)
            
            # 显示
            if show_check.isChecked() != layer.visible:
                layer.visible = show_check.isChecked()
                self.layer_visibility_changed.emit(index, layer.visible)

    def _show_panel_options(self):
        """面板选项对话框"""
        # 对话框、表单布局、对话框按钮组
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
        
        dlg = QDialog(self)
        dlg.setWindowTitle("图层面板选项")
        dlg.setMinimumWidth(280)
        dlg.setStyleSheet("""
            QDialog { background-color: #3c3c3c; color: #ddd; }
            QCheckBox { color: #bbb; }
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; padding: 6px 16px; border-radius: 3px; }
        """)
        
        layout = QFormLayout(dlg)
        
        thumb_check = QCheckBox("仅显示图层")
        thumb_check.setChecked(False)
        layout.addRow("", thumb_check)
        
        small_check = QCheckBox("小行高")
        layout.addRow("", small_check)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addRow(buttons)
        
        dlg.exec_()

    def _on_add_sublayer(self):
        """添加子图层"""
        idx = self._current_index
        if 0 <= idx < len(self._layers_data):
            layer = self._layers_data[idx]
            layer.add_sublayer()
            self.update_layers(self._layers_data, idx)

    def _set_layer_color(self, index: int, color: QColor):
        if 0 <= index < len(self._layers_data):
            self._layers_data[index].color = color

    def _toggle_template(self, index: int):
        if 0 <= index < len(self._layers_data):
            layer = self._layers_data[index]
            layer.is_template = not layer.is_template

    def _toggle_printable(self, index: int):
        if 0 <= index < len(self._layers_data):
            layer = self._layers_data[index]
            layer.printable = not layer.printable

    def _toggle_preview_mode(self, index: int):
        if 0 <= index < len(self._layers_data):
            layer = self._layers_data[index]
            layer.preview_mode = "outline" if layer.preview_mode == "preview" else "preview"

    def highlight_object(self, layer_index: int, item_index: int):
        """根据 layer_index + item_index 在树控件中高亮对应的对象节点（第二十三章）
        
        当从画布选中对象时，调用此方法同步高亮图层面板中的对应节点
        
        支持：
        - 面板反序显示（图层数据索引 → 树索引转换）
        - GroupItem 内部元素的递归查找
        """
        # 面板反序显示：数据索引需转换为树索引
        total = self._tree.topLevelItemCount()
        tree_layer_index = total - 1 - layer_index if total > 0 else -1

        if 0 <= tree_layer_index < total:
            layer_item = self._tree.topLevelItem(tree_layer_index)
            # 确保图层展开
            layer_item.setExpanded(True)
            # 递归遍历该图层的所有后代节点找到匹配的对象
            found = self._find_object_in_tree(layer_item, layer_index, item_index)
            if found:
                self._tree.setCurrentItem(found)
                self._tree.scrollToItem(found, QTreeWidget.PositionAtCenter)
                return
            # 如果没找到对象，至少选中父图层
            self._tree.setCurrentItem(layer_item)
            self._tree.scrollToItem(layer_item, QTreeWidget.PositionAtCenter)

    def _emit_reorder_with_log(self, data_start: int, data_row: int, layer_name: str):
        """发射图层重排序信号并记录日志
        
        Args:
            data_start: 拖拽前数据索引
            data_row: 拖拽后数据索引
            layer_name: 图层名称
        """
        import time
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        print(f"[{timestamp}] 图层重排信号发射: {layer_name} → 目标位置 {data_row}")
        self.layer_reorder_requested.emit(data_start, data_row)

    def _get_layer_data_index(self, item: QTreeWidgetItem) -> int | None:
        """从树位置实时计算图层的数据索引（不依赖 Qt.UserRole）
        
        面板反序显示：树第0行 = layers[-1]（顶层），树最后行 = layers[0]（底层）
        data_index = total - 1 - tree_index
        """
        tree_index = self._tree.indexOfTopLevelItem(item)
        total = self._tree.topLevelItemCount()
        if 0 <= tree_index < total:
            return total - 1 - tree_index
        return None

    def _get_object_data_indices(self, item: QTreeWidgetItem) -> tuple[int | None, int | None]:
        """从树位置实时计算对象的 obj_index 和所属 layer_index
        
        对象在正序树下：child(0) = items[0] = 视觉顶层
        
        Returns:
            (obj_index, layer_index) — obj_index 在父级 children 中的位置，
            layer_index 通过向上查找图层节点获得
        """
        parent_item = item.parent()
        if parent_item is None:
            # 尝试从 UserRole 回退读取
            return (item.data(0, Qt.UserRole), None)

        # 对象在父节点中的位置直接映射到 items 索引
        obj_index = parent_item.indexOfChild(item)
        if obj_index < 0:
            return (None, None)

        # 向上查找图层索引
        layer_index = self._find_parent_layer_index(parent_item)
        return (obj_index, layer_index)

    def _get_sublayer_data_indices(self, item: QTreeWidgetItem) -> tuple[int | None, int | None]:
        """从树位置实时计算子图层的 sub_idx 和所属 parent_layer_index"""
        parent_item = item.parent()
        if parent_item is None:
            return (None, None)

        sub_idx = parent_item.indexOfChild(item)
        if sub_idx < 0:
            return (None, None)

        layer_index = self._find_parent_layer_index(parent_item)
        return (sub_idx, layer_index)

    def _find_parent_layer_index(self, item: QTreeWidgetItem) -> int | None:
        """递归向上查找树节点所属的图层索引
        
        从对象节点向上遍历父节点链，直到找到类型为 'layer' 的顶层节点。
        ★ 关键修复：使用树位置实时计算 layer index，
        避免拖拽后 Qt.UserRole 过时导致读取错误的图层索引。
        """
        current = item
        while current is not None:
            item_type = current.data(0, Qt.UserRole + 1)
            if item_type == "layer":
                # ★ 从树位置实时计算，不使用可能过时的 Qt.UserRole
                return self._get_layer_data_index(current)
            current = current.parent()
        return None

    def _find_object_in_tree(
        self, parent_item: QTreeWidgetItem, layer_index: int, item_index: int,
    ) -> QTreeWidgetItem | None:
        """递归在树中查找匹配的对象节点（支持 GroupItem 嵌套）"""
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            child_type = child.data(0, Qt.UserRole + 1)
            if child_type == "object":
                obj_idx = child.data(0, Qt.UserRole)
                lyr_idx = child.data(0, Qt.UserRole + 3)
                if obj_idx == item_index and lyr_idx == layer_index:
                    return child
            # 递归查找子节点（处理 GroupItem 展开的情况）
            if child.childCount() > 0:
                found = self._find_object_in_tree(child, layer_index, item_index)
                if found:
                    return found
        return None

    def _show_layer_menu(self):
        """点击☰按钮显示图层菜单（PDF 二十五）"""
        self._on_context_menu(
            self._tree.visualItemRect(self._tree.currentItem() or self._tree.topLevelItem(0)).topLeft()
            if self._tree.topLevelItemCount() > 0 else self._tree.rect().topLeft()
        )


# ── 色板面板 ──────────────────────────────────────────────

class SwatchesPanel(QWidget):
    """色板面板
    注意: PyQt5 QWidget 子类不能使用 __slots__。
    """

    color_selected = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addWidget(QLabel("色板"))

        self._grid = QGridLayout()
        self._grid.setSpacing(2)
        layout.addLayout(self._grid)
        layout.addStretch()

    def update_swatches(self, swatches: list[Swatch]):
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cols = 4
        for i, swatch in enumerate(swatches):
            btn = QPushButton()
            btn.setFixedSize(28, 28)
            btn.setToolTip(swatch.name)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {swatch.color.name()};
                    border: 1px solid #666;
                    border-radius: 2px;
                }}
                QPushButton:hover {{ border: 2px solid #0d6efd; }}
            """)
            btn.clicked.connect(lambda checked, c=swatch.color: self.color_selected.emit(c))
            self._grid.addWidget(btn, i // cols, i % cols)
