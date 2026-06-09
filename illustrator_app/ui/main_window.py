"""
主窗口 (Python 3.10+) —— 组合所有组件，处理菜单、快捷键和面板交互

集成 DeepSeek AI 助手 —— 交互式对话生成矢量文本海报

架构优化:
- 使用 __slots__ 减少内存占用
- 使用 X | None 替代 Optional[X]
- 使用 match-case 进行类型分发
"""
# 允许在类型注解中使用
from __future__ import annotations

import math
import traceback

from PyQt5.QtCore import Qt, QPointF, QRectF, QSize
from PyQt5.QtGui import (
    QKeySequence, QColor, QPainter, QPixmap, QPainterPath,
)
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QAction, QToolBar, QStatusBar, QLabel,
    QFileDialog, QMessageBox, QDockWidget,
    QApplication,
)
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtCore import Qt as QtCore_Qt  # 避免与 panel 中的 Qt 冲突

from ..logging_config import get_logger
from ..core.graphics import (
    GraphicItem, PathItem, RectangleItem, EllipseItem,
    TextFrame, GroupItem, GraphicStyle, Swatch, Justification,
    Gradient, GradientType, GradientStop, AnchorPoint,
    CompoundPathfinderCommand,
)
from ..core.document import Document, Layer
from ..core.tools import ToolType
from .canvas import CanvasWidget
from .panels import ToolBar, PropertiesPanel, LayersPanel, SwatchesPanel
from .collapsible_panel import PanelContainer
from ..ai.chat_panel import ChatPanel

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """主窗口
    注意: PyQt5 的 QWidget/QMainWindow 子类不能使用 __slots__，
    否则 sip wrapper 内部状态会异常，导致应用闪退。
    """

    def __init__(self):
        super().__init__()
        self._document: Document | None = None
        self._current_file: str | None = None
        self._clipboard: list[GraphicItem] = []
        self._init_document()
        self._init_ui()
        self._connect_signals()

    def _init_document(self):
        self._document = Document(800, 600, name="未命名-1")
        logger.info("主窗口初始化完成")

    # ── UI 初始化 ──

    def _init_ui(self):
        self.setWindowTitle("简易 Illustrator — 未命名-1")
        self.resize(1280, 800)

        self.setStyleSheet("""
            QMainWindow { background-color: #2d2d2d; }
            QMenuBar { background-color: #3c3c3c; color: #ddd; border-bottom: 1px solid #555; }
            QMenuBar::item:selected { background-color: #0d6efd; }
            QMenu { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; }
            QMenu::item:selected { background-color: #0d6efd; }
            QStatusBar { background-color: #007acc; color: white; }
            QDockWidget { color: #ddd; titlebar-close-icon: none; }
            QDockWidget::title { background-color: #3c3c3c; padding: 4px; }
        """)

        self._canvas = CanvasWidget()
        self._canvas.document = self._document
        self.setCentralWidget(self._canvas)

        self._create_menus()
        self._create_toolbar()
        self._create_panels()

        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._zoom_label = QLabel("100%")
        self._pos_label = QLabel("X: 0  Y: 0")
        self._tool_label = QLabel("选择工具")
        self._status_bar.addPermanentWidget(self._tool_label)
        self._status_bar.addPermanentWidget(self._pos_label)
        self._status_bar.addPermanentWidget(self._zoom_label)

    def _create_menus(self):
        menubar = self.menuBar()

        # ── 文件菜单 ──
        file_menu = menubar.addMenu("文件(&F)")

        for label, shortcut, slot in [
            ("新建(&N)", QKeySequence.New, self._on_new),
            ("打开(&O)...", QKeySequence.Open, self._on_open),
        ]:
            action = QAction(label, self)
            action.setShortcut(shortcut)
            action.triggered.connect(slot)
            file_menu.addAction(action)

        file_menu.addSeparator()

        save_action = QAction("保存(&S)", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self._on_save)
        file_menu.addAction(save_action)

        # ── 另存为子菜单 ──
        save_as_menu = file_menu.addMenu("另存为(&A)...")

        # 项目文件（原有功能）
        save_as_project = QAction("项目文件 (*.ai.json)...", self)
        save_as_project.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_project.triggered.connect(self._on_save_as)
        save_as_menu.addAction(save_as_project)

        save_as_menu.addSeparator()

        for label, shortcut, slot in [
            ("另存为 PNG...",   "Ctrl+Shift+P", self._on_export_png),
            ("另存为 JPEG...",  "Ctrl+Shift+J", self._on_export_jpeg),
            ("另存为 PDF...",   "Ctrl+Shift+F", self._on_export_pdf),
        ]:
            action = QAction(label, self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(slot)
            save_as_menu.addAction(action)

        file_menu.addSeparator()

        # ── 导出子菜单 ──
        export_menu = file_menu.addMenu("导出(&E)")

        for label, shortcut, slot in [
            ("导出为 PNG...",   "Ctrl+Shift+P", self._on_export_png),
            ("导出为 JPEG...",  "Ctrl+Shift+J", self._on_export_jpeg),
            ("导出为 PDF...",   "Ctrl+Shift+F", self._on_export_pdf),
            ("导出为 SVG...",   "Ctrl+Shift+G", self._on_export_svg),
        ]:
            action = QAction(label, self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(slot)
            export_menu.addAction(action)

        file_menu.addSeparator()

        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut(QKeySequence("Alt+F4"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # ── 编辑菜单 ──
        edit_menu = menubar.addMenu("编辑(&E)")

        self._undo_action = QAction("撤销(&U)", self)
        self._undo_action.setShortcut(QKeySequence.Undo)
        self._undo_action.triggered.connect(self._on_undo)
        self._undo_action.setEnabled(False)
        edit_menu.addAction(self._undo_action)

        self._redo_action = QAction("重做(&R)", self)
        self._redo_action.setShortcut(QKeySequence.Redo)
        self._redo_action.triggered.connect(self._on_redo)
        self._redo_action.setEnabled(False)
        edit_menu.addAction(self._redo_action)

        edit_menu.addSeparator()

        for label, shortcut, slot in [
            ("复制(&C)", QKeySequence.Copy, self._on_copy),
            ("粘贴(&V)", QKeySequence.Paste, self._on_paste),
        ]:
            action = QAction(label, self)
            action.setShortcut(shortcut)
            action.triggered.connect(slot)
            edit_menu.addAction(action)

        edit_menu.addSeparator()

        delete_action = QAction("删除(&D)", self)
        delete_action.setShortcut(QKeySequence.Delete)
        delete_action.triggered.connect(self._on_delete)
        edit_menu.addAction(delete_action)

        select_all_action = QAction("全选(&A)", self)
        select_all_action.setShortcut(QKeySequence.SelectAll)
        select_all_action.triggered.connect(self._on_select_all)
        edit_menu.addAction(select_all_action)

        edit_menu.addSeparator()

        group_action = QAction("编组(&G)", self)
        group_action.setShortcut(QKeySequence("Ctrl+G"))
        group_action.triggered.connect(self._on_group)
        edit_menu.addAction(group_action)

        ungroup_action = QAction("取消编组", self)
        ungroup_action.setShortcut(QKeySequence("Ctrl+Shift+G"))
        ungroup_action.triggered.connect(self._on_ungroup)
        edit_menu.addAction(ungroup_action)

        # ── 对象菜单 ──
        object_menu = menubar.addMenu("对象(&O)")

        for label, shortcut, slot in [
            ("置于顶层", "Ctrl+Shift+]", self._on_bring_front),
            ("上移一层", "Ctrl+]", self._on_bring_forward),
            ("下移一层", "Ctrl+[", self._on_send_backward),
            ("置于底层", "Ctrl+Shift+[", self._on_send_to_back),
        ]:
            action = QAction(label, self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(slot)
            object_menu.addAction(action)

        object_menu.addSeparator()

        # 对齐子菜单
        align_menu = object_menu.addMenu("对齐")

        # ── 对象间对齐 ──
        align_to_selection_menu = align_menu.addMenu("对齐所选对象")
        for label, mode in [
            ("左对齐", "left"), ("水平居中", "center_h"), ("右对齐", "right"),
            ("顶部对齐", "top"), ("垂直居中", "center_v"), ("底部对齐", "bottom"),
        ]:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, m=mode: self._on_align(m))
            align_to_selection_menu.addAction(action)

        align_menu.addSeparator()

        # ── 对齐到画布 ──
        align_to_canvas_menu = align_menu.addMenu("对齐到画布")
        for label, mode in [
            ("左对齐到画布", "canvas_left"),
            ("水平居中到画布", "canvas_center_h"),
            ("右对齐到画布", "canvas_right"),
            ("顶部对齐到画布", "canvas_top"),
            ("垂直居中到画布", "canvas_center_v"),
            ("底部对齐到画布", "canvas_bottom"),
        ]:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, m=mode: self._on_align(m))
            align_to_canvas_menu.addAction(action)

        object_menu.addSeparator()

        # 路径查找器子菜单
        pathfinder_menu = object_menu.addMenu("路径查找器")
        for label, mode in [
            ("合并（联集）", "union"),
            ("减去顶层", "subtract"),
            ("交集", "intersect"),
            ("差集（异或）", "exclude"),
        ]:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, m=mode: self._on_pathfinder(m))
            pathfinder_menu.addAction(action)

        # ── 图层菜单（完整对照 Ai 图层菜单） ──
        layer_menu = menubar.addMenu("图层(&L)")
        
        # 新建图层（第三章方法2）
        new_layer_action = QAction("新建图层(&N)", self)
        new_layer_action.setShortcut(QKeySequence("Ctrl+L"))
        new_layer_action.triggered.connect(self._on_add_layer)
        layer_menu.addAction(new_layer_action)
        
        # 新建子图层（第十章）
        new_sublayer_action = QAction("新建子图层(&S)", self)
        new_sublayer_action.triggered.connect(lambda: self._layers_panel._on_add_sublayer())
        layer_menu.addAction(new_sublayer_action)
        
        layer_menu.addSeparator()
        
        # 复制图层（第六章）
        dup_layer_action = QAction("复制图层(&D)", self)
        dup_layer_action.triggered.connect(
            lambda: self._on_duplicate_layer(self._document.active_layer_index) if self._document else None
        )
        layer_menu.addAction(dup_layer_action)
        
        # 删除图层（第五章）
        del_layer_action = QAction("删除图层", self)
        del_layer_action.triggered.connect(
            lambda: self._on_remove_layer(self._document.active_layer_index) if self._document else None
        )
        layer_menu.addAction(del_layer_action)
        
        layer_menu.addSeparator()
        
        # 当前图层的选项...（图层选项对话框）
        layer_opts_action = QAction("当前图层的选项...", self)
        layer_opts_action.triggered.connect(
            lambda: self._layers_panel._show_layer_options_dialog(
                self._document.active_layer_index
            ) if self._document else None
        )
        layer_menu.addAction(layer_opts_action)
        
        layer_menu.addSeparator()
        
        # 选择整个图层（第十四章）
        select_layer_action = QAction("选择当前图层所有对象", self)
        select_layer_action.triggered.connect(
            lambda: self._on_select_all_in_layer(self._document.active_layer_index) if self._document else None
        )
        layer_menu.addAction(select_layer_action)
        
        # 隐藏/显示其他图层
        hide_others_action = QAction("隐藏其他图层", self)
        hide_others_action.triggered.connect(
            lambda: self._layers_panel._hide_other_layers(self._document.active_layer_index) if self._document else None
        )
        layer_menu.addAction(hide_others_action)
        
        # 锁定其他图层
        lock_others_action = QAction("锁定其他图层", self)
        lock_others_action.triggered.connect(
            lambda: self._layers_panel._lock_other_layers(self._document.active_layer_index) if self._document else None
        )
        layer_menu.addAction(lock_others_action)
        
        layer_menu.addSeparator()
        
        # 收集到新图层（第十五章）
        collect_action = QAction("收集到新图层(&C)", self)
        collect_action.triggered.connect(self._on_collect_layer)
        layer_menu.addAction(collect_action)
        
        # 释放到图层（第十六章）
        release_menu = layer_menu.addMenu("释放到图层")
        release_seq = QAction("顺序 (Sequence)", self)
        release_seq.triggered.connect(self._on_release_sequence)
        release_menu.addAction(release_seq)
        release_build = QAction("构建 (Build)", self)
        release_build.triggered.connect(self._on_release_build)
        release_menu.addAction(release_build)
        
        layer_menu.addSeparator()
        
        # 合并选定图层（第十七章）
        merge_action = QAction("合并选定图层(&M)", self)
        merge_action.triggered.connect(
            lambda: self._on_merge_layers([self._document.active_layer_index]) if self._document else None
        )
        layer_menu.addAction(merge_action)
        
        # 拼合图稿（第十八章）
        flatten_action = QAction("拼合图稿(&F)", self)
        flatten_action.triggered.connect(self._on_flatten)
        layer_menu.addAction(flatten_action)

        # ── 视图菜单 ──
        view_menu = menubar.addMenu("视图(&V)")
        for label, shortcut, slot in [
            ("放大", "Ctrl++", self._canvas.zoom_in),
            ("缩小", "Ctrl+-", self._canvas.zoom_out),
            ("适合窗口", "Ctrl+0", self._canvas.zoom_to_fit),
            ("100%", "Ctrl+1", self._canvas.zoom_100),
        ]:
            action = QAction(label, self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(slot)
            view_menu.addAction(action)

    def _create_toolbar(self):
        toolbar = QToolBar("快速操作")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        for name, slot in [
            ("新建", self._on_new), ("打开", self._on_open), ("保存", self._on_save),
        ]:
            action = QAction(name, self)
            action.triggered.connect(slot)
            toolbar.addAction(action)

        toolbar.addSeparator()
        toolbar.addWidget(QLabel(" 缩放: "))

        toolbar.setStyleSheet("""
            QToolBar { background-color: #3c3c3c; border-bottom: 1px solid #555; spacing: 4px; padding: 2px; }
            QToolBar QAction { color: #ddd; padding: 4px 8px; }
            QToolBar QAction:hover { background-color: #5a5a5a; }
        """)

    def _create_panels(self):
        # 定义私有方法，接收自身引用参数
        self._properties_panel = PropertiesPanel()
        self._layers_panel = LayersPanel()
        self._swatches_panel = SwatchesPanel()
        self._chat_panel = ChatPanel()

        container = PanelContainer()
        container.add_section("🤖 AI 助手", self._chat_panel, expanded=True)
        container.add_section("属性", self._properties_panel, expanded=True)
        container.add_section("图层", self._layers_panel, expanded=True)
        container.add_section("色板", self._swatches_panel, expanded=False)

        right_dock = QDockWidget("面板", self)
        right_dock.setWidget(container)
        right_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, right_dock)
        # 创建左侧工具栏面板，创建左侧停靠窗口
        self._tool_bar = ToolBar()
        tools_dock = QDockWidget("工具", self)
        tools_dock.setWidget(self._tool_bar)
        tools_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        tools_dock.setFixedWidth(56)
        self.addDockWidget(Qt.LeftDockWidgetArea, tools_dock)

    # ── 信号连接 ──

    def _connect_signals(self):
        self._tool_bar.tool_selected.connect(self._canvas.set_tool)

        self._canvas.item_selected.connect(self._on_selection_changed)
        self._canvas.mouse_position_changed.connect(self._on_mouse_move)
        self._canvas.tool_changed.connect(self._on_tool_changed)
        self._canvas.item_modified.connect(self._update_all)

        self._properties_panel.fill_color_changed.connect(self._on_fill_color)
        self._properties_panel.stroke_color_changed.connect(self._on_stroke_color)
        self._properties_panel.stroke_width_changed.connect(self._on_stroke_width)
        self._properties_panel.opacity_changed.connect(self._on_opacity)
        self._properties_panel.corner_radius_changed.connect(self._on_corner_radius)
        self._properties_panel.text_changed.connect(self._on_text_changed)
        self._properties_panel.font_size_changed.connect(self._on_font_size)
        self._properties_panel.font_family_changed.connect(self._on_font_family)
        self._properties_panel.bold_changed.connect(self._on_bold)
        self._properties_panel.italic_changed.connect(self._on_italic)
        self._properties_panel.alignment_changed.connect(self._on_alignment)
        # 变换参数信号连接
        self._properties_panel.position_changed.connect(self._on_position_changed)
        self._properties_panel.size_changed.connect(self._on_size_changed)
        self._properties_panel.rotation_changed.connect(self._on_rotation_changed)
        self._layers_panel.order_front.connect(self._on_bring_front)
        self._layers_panel.order_back.connect(self._on_send_to_back)
        self._layers_panel.order_forward.connect(self._on_bring_forward)
        self._layers_panel.order_backward.connect(self._on_send_backward)
        self._layers_panel.delete_requested.connect(self._on_delete)

        self._layers_panel.layer_selected.connect(self._on_layer_selected)
        self._layers_panel.layer_add_requested.connect(self._on_add_layer)
        self._layers_panel.layer_remove_requested.connect(self._on_remove_layer)
        self._layers_panel.layer_visibility_changed.connect(self._on_layer_visibility)
        self._layers_panel.layer_locked_changed.connect(self._on_layer_locked)
        self._layers_panel.layer_duplicate_requested.connect(self._on_duplicate_layer)
        self._layers_panel.layer_rename_requested.connect(self._on_rename_layer)
        self._layers_panel.layer_reorder_requested.connect(self._on_reorder_layer)
        self._layers_panel.layer_merge_requested.connect(self._on_merge_layers)
        self._layers_panel.layer_flatten_requested.connect(self._on_flatten)
        self._layers_panel.layer_collect_requested.connect(self._on_collect_layer)
        self._layers_panel.layer_release_sequence_requested.connect(self._on_release_sequence)
        self._layers_panel.layer_release_build_requested.connect(self._on_release_build)
        # 新增信号（第十四章、第二十-二十五章）
        self._layers_panel.layer_select_all_requested.connect(self._on_select_all_in_layer)
        self._layers_panel.layer_target_requested.connect(self._on_target_layer)
        self._layers_panel.layer_color_changed.connect(self._on_layer_color)
        self._layers_panel.layer_template_changed.connect(self._on_layer_template)
        self._layers_panel.layer_printable_changed.connect(self._on_layer_printable)
        self._layers_panel.layer_preview_mode_changed.connect(self._on_layer_preview_mode)
        self._layers_panel.layer_opacity_changed.connect(self._on_layer_opacity)
        self._layers_panel.item_order_changed.connect(self._on_item_order)
        self._layers_panel.item_move_to_layer.connect(self._on_move_item_to_layer)
        # 对象级操作信号（图层面板中的对象操作）
        self._layers_panel.item_delete_requested.connect(self._on_item_delete_from_panel)
        self._layers_panel.item_duplicate_requested.connect(self._on_item_duplicate_from_panel)
        self._layers_panel.item_select_requested.connect(self._on_item_select_from_panel)
        self._layers_panel.item_visibility_toggled.connect(self._on_item_visibility_from_panel)
        self._layers_panel.item_locked_toggled.connect(self._on_item_locked_from_panel)
        self._layers_panel.item_bring_forward_requested.connect(self._on_item_bring_forward_from_panel)
        self._layers_panel.item_send_backward_requested.connect(self._on_item_send_backward_from_panel)

        self._swatches_panel.color_selected.connect(self._on_swatch_selected)

        self._chat_panel.poster_generated.connect(self._on_ai_poster_generated)
        self._chat_panel.set_document(self._document)

        self._update_layers()
        self._swatches_panel.update_swatches(self._document.swatches)

    # ── 事件处理 ──

    def _on_selection_changed(self, items: list[GraphicItem]):
        try:
            self._properties_panel.update_selection(items)
            self._update_undo_state()
            # 问题1修复：当选中对象时，同步高亮图层面板中对应的对象节点
            if items and self._document:
                selected_item = items[0]
                # 查找该对象所属的图层和索引
                for layer_idx, layer in enumerate(self._document.layers):
                    if selected_item in layer.items:
                        item_index = layer.items.index(selected_item)
                        # 调用图层面板的高亮方法
                        self._layers_panel.highlight_object(layer_idx, item_index)
                        break
        except Exception as e:
            logger.error(f"选择变更处理失败: {e}", exc_info=True)

    def _on_mouse_move(self, x: float, y: float):
        self._pos_label.setText(f"X: {x:.1f}  Y: {y:.1f}")

    def _on_tool_changed(self, tool_type: ToolType):
        names = {
            ToolType.SELECTION: "选择工具",
            ToolType.DIRECT_SELECT: "直接选择工具",
            ToolType.RECTANGLE: "矩形工具",
            ToolType.ELLIPSE: "椭圆工具",
            ToolType.PEN: "钢笔工具",
            ToolType.TEXT: "文字工具",
            ToolType.HAND: "抓手工具",
        }
        self._tool_label.setText(names.get(tool_type, "未知工具"))
        self._tool_bar.set_current_tool(tool_type)

    def _update_all(self):
        if self._document:
            self._update_layers()
            self._update_undo_state()
            self._canvas.update()
            self._update_title()

    def _update_layers(self):
        if self._document:
            self._layers_panel.update_layers(
                self._document.layers, self._document.active_layer_index,
            )

    def _update_title(self):
        modified = "*" if self._document and self._document.modified else ""
        name = self._document.name if self._document else "未命名"
        self.setWindowTitle(f"简易 Illustrator — {modified}{name}")

    # ── 属性修改 ──

    def _apply_to_selection(self, func):
        try:
            if self._document:
                for item in list(self._document.get_selection()):
                    func(item)
                self._document.modified = True
                self._canvas.update()
        except Exception as e:
            logger.error(f"属性应用失败: {e}", exc_info=True)

    def _on_fill_color(self, color: QColor):
        self._apply_to_selection(
            lambda item: setattr(item.style, 'fill_color',
                                 color if color.isValid() else None)
        )

    def _on_stroke_color(self, color: QColor):
        self._apply_to_selection(
            lambda item: setattr(item.style, 'stroke_color',
                                 color if color.isValid() else None)
        )

    def _on_stroke_width(self, width: float):
        self._apply_to_selection(lambda item: setattr(item.style, 'stroke_width', width))

    def _on_opacity(self, opacity: float):
        self._apply_to_selection(lambda item: setattr(item, 'opacity', opacity))

    def _on_corner_radius(self, radius: float):
        self._apply_to_selection(
            lambda item: setattr(item, 'corner_radius', radius)
            if isinstance(item, RectangleItem) else None
        )

    def _on_text_changed(self, text: str):
        self._apply_to_selection(
            lambda item: setattr(item, 'contents', text)
            if isinstance(item, TextFrame) else None
        )

    def _on_font_size(self, size: float):
        self._apply_to_selection(
            lambda item: setattr(item.char_attrs, 'font_size', size)
            if isinstance(item, TextFrame) else None
        )

    def _on_font_family(self, family: str):
        self._apply_to_selection(
            lambda item: setattr(item.char_attrs, 'font_family', family)
            if isinstance(item, TextFrame) else None
        )

    def _on_bold(self, bold: bool):
        self._apply_to_selection(
            lambda item: setattr(item.char_attrs, 'bold', bold)
            if isinstance(item, TextFrame) else None
        )

    def _on_italic(self, italic: bool):
        self._apply_to_selection(
            lambda item: setattr(item.char_attrs, 'italic', italic)
            if isinstance(item, TextFrame) else None
        )

    def _on_alignment(self, justification: Justification):
        self._apply_to_selection(
            lambda item: setattr(item.para_attrs, 'justification', justification)
            if isinstance(item, TextFrame) else None
        )

    def _on_position_changed(self, x: float, y: float):
        """属性面板 X/Y 变化时更新选中对象位置"""
        if not self._document:
            return
        for item in list(self._document.get_selection()):
            rect = item.bounding_rect()
            # 计算需要移动的偏移量
            dx = x - rect.x()
            dy = y - rect.y()
            item.move_by(dx, dy)
        self._document.modified = True
        self._canvas.update()

    def _on_size_changed(self, width: float, height: float):
        """属性面板 W/H 变化时更新选中对象大小"""
        if not self._document:
            return
        for item in list(self._document.get_selection()):
            rect = item.bounding_rect()
            # 避免除以零
            old_w = max(rect.width(), 0.001)
            old_h = max(rect.height(), 0.001)
            scale_x = width / old_w
            scale_y = height / old_h

            match item:
                case RectangleItem() | EllipseItem() | TextFrame():
                    # 对于基于 rect 的图形，直接设置新 rect
                    item.rect = QRectF(rect.x(), rect.y(), width, height)
                case PathItem():
                    # 对于路径，缩放锚点坐标
                    ref_x = rect.x()
                    ref_y = rect.y()
                    for anchor in item.anchors:
                        anchor.x = ref_x + (anchor.x - ref_x) * scale_x
                        anchor.y = ref_y + (anchor.y - ref_y) * scale_y
                        if anchor.handle_in:
                            anchor.handle_in = QPointF(
                                anchor.handle_in.x() * scale_x,
                                anchor.handle_in.y() * scale_y,
                            )
                        if anchor.handle_out:
                            anchor.handle_out = QPointF(
                                anchor.handle_out.x() * scale_x,
                                anchor.handle_out.y() * scale_y,
                            )
                case GroupItem():
                    # 对于编组，缩放变换矩阵
                    item.scale(scale_x, scale_y, rect.topLeft())
                case _:
                    pass
        self._document.modified = True
        self._canvas.update()

    def _on_rotation_changed(self, angle: float):
        """属性面板旋转角度变化时更新选中对象旋转"""
        if not self._document:
            return
        for item in list(self._document.get_selection()):
            # 获取当前变换的旋转角度
            current_angle = math.degrees(math.atan2(item._transform.m12(), item._transform.m11()))
            # 计算需要旋转的增量
            delta = angle - current_angle
            if abs(delta) > 0.01:
                rect = item.bounding_rect()
                center = QPointF(rect.x() + rect.width() / 2, rect.y() + rect.height() / 2)
                item.rotate(delta, center)
        self._document.modified = True
        self._canvas.update()

    def _on_swatch_selected(self, color: QColor):
        self._on_fill_color(color)

    # ── 图层操作 ──

    def _on_layer_selected(self, index: int):
        if self._document:
            self._document.active_layer_index = index
            self._canvas.update()

    def _on_add_layer(self):
        if self._document:
            self._document.add_layer()
            self._update_layers()
            self._canvas.update()

    def _on_remove_layer(self, index: int):
        if self._document and len(self._document.layers) > 1:
            layer = self._document.layers[index]
            self._document.remove_layer(layer)
            self._update_layers()
            self._canvas.update()

    def _on_layer_visibility(self, index: int, visible: bool):
        """切换图层可见性（PDF 八）"""
        if self._document and 0 <= index < len(self._document.layers):
            self._document.layers[index].visible = visible
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_layer_locked(self, index: int, locked: bool):
        """切换图层锁定（PDF 九）"""
        if self._document and 0 <= index < len(self._document.layers):
            self._document.layers[index].locked = locked
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_duplicate_layer(self, index: int):
        """复制图层（PDF 五）"""
        if self._document and 0 <= index < len(self._document.layers):
            self._document.duplicate_layer(self._document.layers[index])
            self._update_layers()
            self._canvas.update()

    def _on_rename_layer(self, index: int, new_name: str):
        """重命名图层（PDF 六）"""
        if self._document:
            if new_name:
                if index >= 0 and index < len(self._document.layers):
                    self._document.layers[index].name = new_name
                    self._document.modified = True
            # 空名称表示需要启动重命名（已在面板中处理）
            self._update_layers()

    def _on_reorder_layer(self, from_index: int, to_index: int):
        """调整图层顺序（PDF 十）—— 实时同步画布渲染顺序
        
        渲染顺序规则：
        - layers[0] = 最底层 = 最先绘制
        - layers[-1] = 最顶层 = 最后绘制（覆盖其他图层）
        - 画布 paintEvent 正序遍历 layers，所以 reorder 后顺序直接决定视觉层级
        
        ★ 此方法现在由 panels._on_rows_moved 同步调用（已移除 QTimer 延迟），
        确保信号在拖拽操作完成时立即触发，画布实时更新。
        """
        if not self._document or not (0 <= from_index < len(self._document.layers)):
            return
            
        layer = self._document.layers[from_index]
        old_order = [ly.name for ly in self._document.layers]

        print(f"\n{'='*60}")
        print(f"[图层拖拽] 图层「{layer.name}」顺序调整（同步触发）")
        print(f"  拖拽前绘制顺序（底层→顶层）: {old_order}")
        print(f"  源索引: {from_index} → 目标索引: {to_index}")

        self._document.reorder_layer(layer, to_index)

        new_order = [ly.name for ly in self._document.layers]
        print(f"  拖拽后绘制顺序（底层→顶层）: {new_order}")
        print(f"  图层「{layer.name}」的新索引: {self._document.layers.index(layer)}")
        print(f"{'='*60}\n")

        # ★ 关键：先更新 document，再刷新画布
        # mark_dirty 标记 + repaint 强制立即重绘，确保视觉顺序实时同步
        self._document.mark_dirty()
        self._update_layers()
        self._canvas.repaint()
        logger.info(
            f"图层重排完成: {layer.name} 从索引 {from_index} → {to_index}, "
            f"新绘制顺序: {new_order}"
        )

    def _on_merge_layers(self, indices: list[int]):
        """合并选定图层（PDF 十八）"""
        if self._document:
            layers = [self._document.layers[i] for i in indices if 0 <= i < len(self._document.layers)]
            if len(layers) >= 2:
                self._document.merge_layers(layers)
                self._update_layers()
                self._canvas.update()

    def _on_flatten(self):
        """拼合图稿（PDF 十九）"""
        if self._document:
            self._document.flatten_artwork()
            self._update_layers()
            self._canvas.update()

    def _on_collect_layer(self):
        """收集到新图层（PDF 十六）"""
        if self._document:
            sel = self._document.get_selection()
            if sel:
                self._document.collect_in_new_layer(sel)
                self._update_layers()
                self._canvas.update()

    def _on_release_sequence(self):
        """释放到图层 - 顺序模式（PDF 十七）"""
        if self._document:
            sel = self._document.get_selection()
            for item in sel:
                if isinstance(item, GroupItem):
                    self._document.release_to_layers_sequence(item)
                    self._update_layers()
                    self._canvas.update()
                    return

    def _on_release_build(self):
        """释放到图层 - 构建模式（PDF 十七）"""
        if self._document:
            sel = self._document.get_selection()
            for item in sel:
                if isinstance(item, GroupItem):
                    self._document.release_to_layers_build(item)
                    self._update_layers()
                    self._canvas.update()
                    return

    def _on_select_all_in_layer(self, index: int):
        """选择整个图层的所有对象（第十四章）
        
        对照 Ai 行为：点击图层右侧目标区域，一次性选中图层全部对象
        包括子图层中的对象
        """
        if self._document and 0 <= index < len(self._document.layers):
            self._document.clear_selection()
            layer = self._document.layers[index]
            # 使用 all_items_recursive 获取所有嵌套对象
            for item in layer.all_items_recursive:
                if not item.locked:
                    item.selected = True
            self._document.active_layer_index = index
            self._canvas.update()
            self._status_bar.showMessage(f"已选择图层「{layer.name}」的全部对象", 2000)

    def _on_target_layer(self, index: int):
        """设置目标图层（第二十四章 — Target）"""
        if self._document and 0 <= index < len(self._document.layers):
            self._document.active_layer_index = index
            self._update_layers()
            layer = self._document.layers[index]
            self._status_bar.showMessage(f"目标图层: {layer.name}（效果将应用于此图层）", 2000)

    def _on_layer_color(self, index: int, color: QColor):
        """图层颜色变更（第二十章）"""
        if self._document and 0 <= index < len(self._document.layers):
            self._document.layers[index].color = color
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_layer_template(self, index: int, is_template: bool):
        """模板模式变更（第十九章）"""
        if self._document and 0 <= index < len(self._document.layers):
            self._document.layers[index].is_template = is_template
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_layer_printable(self, index: int, printable: bool):
        """打印状态变更（第二十一章）"""
        if self._document and 0 <= index < len(self._document.layers):
            self._document.layers[index].printable = printable
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_layer_preview_mode(self, index: int, mode: str):
        """预览模式变更（第二十二章）"""
        if self._document and 0 <= index < len(self._document.layers):
            self._document.layers[index].preview_mode = mode
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_layer_opacity(self, index: int, opacity: float):
        """图层不透明度变更（第二十五章 — 图层级透明度效果）"""
        if self._document and 0 <= index < len(self._document.layers):
            self._document.layers[index].opacity = opacity
            self._document.modified = True
            self._canvas.update()

    def _on_item_order(self, layer_index: int, from_pos: int, to_pos: int, parent_item=None):
        """对象层级管理 - 拖动调整对象前后顺序（第十二章）
        
        处理场景：
        1. 图层直接子对象拖拽：from_pos/to_pos 对应 layer.items 索引
        2. GroupItem 内部子对象拖拽：parent_item 为 GroupItem 的树节点
        
        关键映射关系：
        - 面板正序显示：子项第0行 = items[0] = 视觉顶层 = 后绘制
        - 画布反序绘制：reversed(items)，items[0] 最后绘制 = 视觉顶层
        - 因此面板索引 from_pos/to_pos 直接对应 layer.items 索引
        """
        print(f"\n[_on_item_order] ═══ 收到对象拖拽信号 ═══")
        print(f"[_on_item_order] layer_index={layer_index}, from_pos={from_pos}, to_pos={to_pos}")
        print(f"[_on_item_order] parent_item={'有' if parent_item else '无'}")
        
        if not self._document or not (0 <= layer_index < len(self._document.layers)):
            print(f"[_on_item_order] ❌ 无效参数: document={'有' if self._document else '无'}, layer_index={layer_index}, total_layers={len(self._document.layers) if self._document else 0}")
            return
            
        layer = self._document.layers[layer_index]
        print(f"[_on_item_order] 图层「{layer.name}」，当前 items 数量={len(layer.items)}")
        
        # 记录拖拽前的对象顺序（用于日志验证）
        old_order = [it.name or f"<{it.item_type}>" for it in layer.items]
        print(f"[_on_item_order] 拖拽前 items 顺序: {old_order}")

        # ── 1. GroupItem 内部拖拽 ──
        if parent_item is not None:
            from PyQt5.QtCore import Qt
            parent_type = parent_item.data(0, Qt.UserRole + 1)
            if parent_type == "object":
                print(f"[_on_item_order] → 进入 GroupItem 内部拖拽分支")
                from .core.graphics import GroupItem
                parent_obj_id = parent_item.data(0, Qt.UserRole + 2)
                for direct_item in layer.items:
                    if isinstance(direct_item, GroupItem) and direct_item.id == parent_obj_id:
                        if 0 <= from_pos < len(direct_item.items) and 0 <= to_pos < len(direct_item.items):
                            item = direct_item.items.pop(from_pos)
                            direct_item.items.insert(to_pos, item)
                            print(f"[_on_item_order] ✓ GroupItem 内部拖拽完成: {item.name or item.item_type} 从 {from_pos} → {to_pos}")
                            self._document.modified = True
                            self._document.mark_dirty()
                            self._update_layers()
                            self._canvas.repaint()
                            return
                        break

        # ── 2. 图层直接子对象拖拽 ──
        # ★ 关键修复：允许 to_pos == len(layer.items)（插入到末尾）
        print(f"[_on_item_order] → 检查图层直接子对象拖拽: from={from_pos}/{len(layer.items)}, to={to_pos}/{len(layer.items)}")
        if 0 <= from_pos < len(layer.items) and 0 <= to_pos <= len(layer.items):
            item = layer.items.pop(from_pos)
            # clamp 目标位置到 pop 后的有效范围
            to_pos = max(0, min(to_pos, len(layer.items)))
            layer.items.insert(to_pos, item)
            
            new_order = [it.name or f"<{it.item_type}>" for it in layer.items]
            print(f"\n[对象拖拽] 图层「{layer.name}」对象顺序已更新:")
            print(f"  拖拽前: {old_order}")
            print(f"  拖拽后: {new_order}")
            print(f"  画布绘制顺序（底层→顶层）: {list(reversed(new_order))}")
            
            self._document.modified = True
            self._document.mark_dirty()
            self._update_layers()
            self._canvas.repaint()  # ★ 强制立即重绘，确保画布实时更新
            return

        # ── 3. 回退：尝试在 GroupItem 内部查找 ──
        print(f"[_on_item_order] → 回退查找 GroupItem 内部...")
        found = False
        for direct_item in layer.items:
            if isinstance(direct_item, GroupItem):
                if self._reorder_in_group(direct_item, from_pos, to_pos):
                    found = True
                    self._document.modified = True
                    self._document.mark_dirty()
                    self._update_layers()
                    self._canvas.repaint()  # ★ 强制立即重绘
                    break
        if not found:
            print(f"[_on_item_order] ❌ 未找到匹配的对象！items 顺序未改变")
            # ★ 关键回退：即使找不到匹配对象，也要强制 _update_layers 同步树和画布
            # 确保树的视觉状态与数据一致
            new_order = [it.name or f"<{it.item_type}>" for it in layer.items]
            print(f"[_on_item_order] 当前 items: {new_order}")
            self._update_layers()
            self._canvas.repaint()

    def _reorder_in_group(self, group, from_pos: int, to_pos: int) -> bool:
        """在 GroupItem 内部递归查找并重排子对象"""
        from .core.graphics import GroupItem
        if 0 <= from_pos < len(group.items) and 0 <= to_pos < len(group.items):
            item = group.items.pop(from_pos)
            group.items.insert(to_pos, item)
            return True
        for sub in group.items:
            if isinstance(sub, GroupItem):
                if self._reorder_in_group(sub, from_pos, to_pos):
                    return True
        return False

    def _on_move_item_to_layer(self, target_index: int):
        """移动选中对象到其他图层（第十三章 — 拖动彩色方块）"""
        if self._document and 0 <= target_index < len(self._document.layers):
            sel = self._document.get_selection()
            target_layer = self._document.layers[target_index]
            for item in sel:
                # 从原图层移除
                for layer in self._document.layers:
                    if item in layer.items:
                        layer.remove_item(item)
                        break
                # 添加到目标图层
                target_layer.add_item(item)
            self._document.modified = True
            self._update_layers()
            self._canvas.update()
            self._status_bar.showMessage(
                f"已将 {len(sel)} 个对象移动到图层「{target_layer.name}」", 2000
            )

    # ── 图层面板中的对象级操作 ──

    def _on_item_delete_from_panel(self, item: GraphicItem):
        """从图层面板删除指定对象（接收 GraphicItem 对象）"""
        if self._document and item:
            self._document.remove_item(item)
            self._canvas.update()
            self._update_title()

    def _on_item_duplicate_from_panel(self, item: GraphicItem):
        """从图层面板复制指定对象（接收 GraphicItem 对象）"""
        if self._document and item:
            cloned = item.deep_copy()
            cloned.move_by(10, 10)
            self._document.add_item(cloned)
            self._update_layers()
            self._canvas.update()

    def _on_item_select_from_panel(self, layer_index: int, item_index: int):
        """从图层面板选中指定对象"""
        if self._document and 0 <= layer_index < len(self._document.layers):
            layer = self._document.layers[layer_index]
            if 0 <= item_index < len(layer.items):
                item = layer.items[item_index]
                self._document.clear_selection()
                item.selected = True
                self._document.active_layer_index = layer_index
                self._canvas.update()
                self._properties_panel.update_selection([item])

    def _on_item_visibility_from_panel(self, item: GraphicItem, visible: bool):
        """从图层面板切换对象可见性（信号：item_visibility_toggled(object, bool)）"""
        if self._document and item:
            item.visible = visible
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_item_locked_from_panel(self, item: GraphicItem, locked: bool):
        """从图层面板切换对象锁定（信号：item_locked_toggled(object, bool)）"""
        if self._document and item:
            item.locked = locked
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_item_bring_forward_from_panel(self, item: GraphicItem):
        """从图层面板上移一层（接收对象引用）"""
        if self._document and item:
            layer = item._layer or self._document.active_layer
            if layer:
                layer.bring_forward(item)
                self._document.modified = True
                self._update_layers()
                self._canvas.update()

    def _on_item_send_backward_from_panel(self, item: GraphicItem):
        """从图层面板下移一层（接收对象引用）"""
        if self._document and item:
            layer = item._layer or self._document.active_layer
            if layer:
                layer.send_backward(item)
                self._document.modified = True
                self._update_layers()
                self._canvas.update()

    # ── 排列操作 ──

    def _on_bring_front(self):
        if self._document:
            for item in self._document.get_selection():
                (item._layer or self._document.active_layer).bring_to_front(item)
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_send_to_back(self):
        if self._document:
            for item in self._document.get_selection():
                (item._layer or self._document.active_layer).send_to_back(item)
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_bring_forward(self):
        if self._document:
            for item in self._document.get_selection():
                (item._layer or self._document.active_layer).bring_forward(item)
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    def _on_send_backward(self):
        if self._document:
            for item in self._document.get_selection():
                (item._layer or self._document.active_layer).send_backward(item)
            self._document.modified = True
            self._update_layers()
            self._canvas.update()

    # ── 编辑操作 ──

    def _on_delete(self):
        try:
            if self._document:
                for item in list(self._document.get_selection()):
                    self._document.remove_item(item)
                self._properties_panel.update_selection([])
                self._canvas.update()
                self._update_title()
        except Exception as e:
            logger.error(f"删除操作失败: {e}", exc_info=True)

    def _on_select_all(self):
        if self._document:
            self._document.select_all()
            self._properties_panel.update_selection(self._document.get_selection())
            self._canvas.update()

    def _on_group(self):
        if self._document:
            group = self._document.group_selection()
            if group:
                self._properties_panel.update_selection([group])
                self._canvas.update()
                self._update_title()

    def _on_ungroup(self):
        if self._document:
            for item in list(self._document.get_selection()):
                self._document.ungroup(item)
            self._properties_panel.update_selection([])
            self._canvas.update()
            self._update_title()

    # ── 撤销/重做 ──

    def _on_undo(self):
        if self._document and self._document.undo():
            self._update_undo_state()
            self._update_all()
            self._canvas.update()

    def _on_redo(self):
        if self._document and self._document.redo():
            self._update_undo_state()
            self._update_all()
            self._canvas.update()

    def _update_undo_state(self):
        if self._document:
            self._undo_action.setEnabled(self._document.can_undo)
            self._redo_action.setEnabled(self._document.can_redo)
            if self._document.can_undo:
                self._undo_action.setText(f"撤销 {self._document.history.undo_description}")
            else:
                self._undo_action.setText("撤销(&U)")
            if self._document.can_redo:
                self._redo_action.setText(f"重做 {self._document.history.redo_description}")
            else:
                self._redo_action.setText("重做(&R)")

    # ── 复制/粘贴 ──

    def _on_copy(self):
        if self._document:
            sel = self._document.get_selection()
            if sel:
                self._clipboard = [item.deep_copy() for item in sel]
                self._status_bar.showMessage(f"已复制 {len(sel)} 个对象", 2000)

    def _on_paste(self):
        if not self._clipboard or not self._document:
            return
        self._document.clear_selection()
        for item in self._clipboard:
            cloned = item.deep_copy()
            cloned.move_by(20, 20)
            cloned.selected = True
            self._document.add_item(cloned)
        self._update_all()
        self._canvas.update()
        self._status_bar.showMessage(f"已粘贴 {len(self._clipboard)} 个对象", 2000)

    # ── 对齐 ──

    def _on_align(self, mode: str):
        """对齐操作 —— 支持画布对齐和对象间对齐

        mode 格式:
          - "left" / "center_h" / "right" / "top" / "center_v" / "bottom"
            → 以选中对象的总包围矩形为基准对齐（需至少2个对象）
          - "canvas_left" / "canvas_center_h" / "canvas_right" /
            "canvas_top" / "canvas_center_v" / "canvas_bottom"
            → 以画布为基准对齐（单个对象也可用）
        """
        if not self._document:
            return
        sel = self._document.get_selection()
        if not sel:
            return

        # 判断是对齐到画布还是对象间对齐
        is_canvas_align = mode.startswith("canvas_")
        # 提取实际对齐方向；若为画布对齐模式，则对齐方向 = 模式名称去掉前缀“canvas_”，否则对齐方向 = 模式名称
        align_direction = mode.replace("canvas_", "") if is_canvas_align else mode

        if is_canvas_align:
            # ── 对齐到画布 ──
            self._align_to_canvas(sel, align_direction)
        else:
            # ── 对象间对齐（以选中对象的总包围矩形为基准） ──
            if len(sel) < 2:
                # 只有1个对象时，自动转为画布对齐
                self._align_to_canvas(sel, align_direction)
                return
            self._align_to_selection(sel, align_direction)

    def _align_to_canvas(self, items: list[GraphicItem], direction: str):
        """将选中对象对齐到画布（以画布矩形区域为基准）"""
        doc = self._document
        canvas_w = doc.width
        canvas_h = doc.height
        # 画布矩形：从(0,0)到(width,height)
        canvas_rect = QRectF(0, 0, canvas_w, canvas_h)

        for item in items:
            rect = item.bounding_rect()
            match direction:
                case "left":
                    item.move_by(canvas_rect.left() - rect.left(), 0)
                case "center_h":
                    item.move_by(canvas_rect.center().x() - rect.center().x(), 0)
                case "right":
                    item.move_by(canvas_rect.right() - rect.right(), 0)
                case "top":
                    item.move_by(0, canvas_rect.top() - rect.top())
                case "center_v":
                    item.move_by(0, canvas_rect.center().y() - rect.center().y())
                case "bottom":
                    item.move_by(0, canvas_rect.bottom() - rect.bottom())

        self._document.modified = True
        self._canvas.update()

    def _align_to_selection(self, items: list[GraphicItem], direction: str):
        """将选中对象以选中总包围矩形为基准对齐（对象间对齐）"""
        all_rects = [item.bounding_rect() for item in items]
        total_rect = all_rects[0]
        for r in all_rects[1:]:
            total_rect = total_rect.united(r)

        for item in items:
            rect = item.bounding_rect()
            match direction:
                case "left":
                    item.move_by(total_rect.left() - rect.left(), 0)
                case "center_h":
                    item.move_by(total_rect.center().x() - rect.center().x(), 0)
                case "right":
                    item.move_by(total_rect.right() - rect.right(), 0)
                case "top":
                    item.move_by(0, total_rect.top() - rect.top())
                case "center_v":
                    item.move_by(0, total_rect.center().y() - rect.center().y())
                case "bottom":
                    item.move_by(0, total_rect.bottom() - rect.bottom())

        self._document.modified = True
        self._canvas.update()

    # ── 路径查找器（布尔运算） ──

    def _on_pathfinder(self, mode: str):
        """路径查找器布尔运算

        对照 Adobe Illustrator 行为：
        - 合并（联集）：所有路径的并集
        - 交集：所有路径的交集
        - 减去顶层：从最底层对象减去所有顶层对象的并集

        关键语义：items[0]=视觉顶层, items[-1]=视觉底层
        - get_selection() 按遍历顺序返回：items[0]→items[-1]，即视觉顶层→视觉底层
        - 对于 subtract，需要反转顺序：以 items[-1]（底层）为被减数，items[0..-2]（顶层）为减数
        """
        if not self._document:
            return

        sel = self._document.get_selection()
        if len(sel) < 2:
            self._status_bar.showMessage("请至少选择2个对象进行布尔运算", 3000)
            return

        # 提取变换后的世界坐标路径
        paths: list[QPainterPath] = []
        for item in sel:
            if hasattr(item, 'painter_path'):
                p = item.painter_path()
                if item._transform and not item._transform.isIdentity():
                    p = item._transform.map(p)
                paths.append(p)

        if len(paths) < 2:
            return

        # ── 根据 mode 决定运算顺序 ──
        if mode == "subtract":
            # 减去顶层：从视觉底层（paths[-1]）减去所有视觉顶层（paths[0..-2]）
            # 视觉底层（先绘制）作为被减数，视觉顶层（后绘制）作为减数
            result_path = QPainterPath(paths[-1])
            for p in paths[:-1]:
                result_path = result_path.subtracted(p)
        elif mode == "union":
            result_path = QPainterPath(paths[0])
            for p in paths[1:]:
                result_path = result_path.united(p)
        elif mode == "intersect":
            result_path = QPainterPath(paths[0])
            for p in paths[1:]:
                result_path = result_path.intersected(p)
        elif mode == "exclude":
            # 差集（异或）：先求并集，再减去交集
            union_path = QPainterPath(paths[0])
            for p in paths[1:]:
                union_path = union_path.united(p)
            intersect_path = QPainterPath(paths[0])
            for p in paths[1:]:
                intersect_path = intersect_path.intersected(p)
            result_path = union_path.subtracted(intersect_path)
        else:
            return

        # ── 检查结果路径是否为空 ──
        if result_path.isEmpty():
            self._status_bar.showMessage(
                f"布尔运算({mode})结果为空，操作取消", 3000)
            return

        # ── 创建结果对象 ──
        result_item = PathItem()
        result_item._path = result_path.simplified()  # 简化冗余控制点

        # 对于 subtract：继承底层对象样式
        # 对于 union/intersect：继承第一个（视觉顶层）对象样式
        style_source = sel[-1] if mode == "subtract" else sel[0]
        result_item.style = style_source.style.copy()
        result_item.selected = True

        # ── 通过 Command 模式执行，支持一步撤销 ──
        # 记录所有原始对象及其所在图层，用于撤销
        old_items: list[tuple[GraphicItem, object]] = []
        for item in sel:
            for layer in self._document._layers:
                if item in layer.items:
                    old_items.append((item, layer))
                    break

        # 创建复合命令
        cmd = CompoundPathfinderCommand(
            self._document, old_items, result_item, mode)
        self._document.execute_command(cmd)

        self._update_all()
        self._canvas.update()
        self._status_bar.showMessage(f"布尔运算({mode})完成", 2000)

    # ── AI 海报生成 ──

    def _on_ai_poster_generated(self, params: dict):
        # 定义私有方法，用于处理海报生成完成事件
        if not self._document:
            # 如果文档不存在，则不做任何处理
            return
        # 导入AI海报生成模块
        from ..ai.deepseek_client import POSTER_TEMPLATES
        template = params.get("template", "social_media")
        tmpl = POSTER_TEMPLATES.get(template)
        if tmpl:
            self._document.width = tmpl["width"]
            self._document.height = tmpl["height"]

        self._update_all()
        self._update_layers()
        self._swatches_panel.update_swatches(self._document.swatches)
        self._canvas.zoom_to_fit()

        title = params.get("title", "新海报")
        self._status_bar.showMessage(f"AI 已生成海报: {title}", 5000)

    # ── 文件操作 ──

    def _on_new(self):
        # 定义私有方法，用于处理新建文件事件
        if self._document and self._document.modified:
            ret = QMessageBox.question(
                self, "未保存的更改",
                "是否保存当前文档的更改？",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            )
            match ret:
                case QMessageBox.Save:
                    if self._document.file_path:
                        self._document.save(self._document.file_path)
                    else:
                        file_path, _ = QFileDialog.getSaveFileName(
                            self, "另存为", "未命名.ai.json",
                            "Illustrator JSON (*.ai.json);;所有文件 (*.*)",
                        )
                        if file_path:
                            self._document.save(file_path)
                        else:
                            return  # 用户取消保存
                case QMessageBox.Cancel:
                    return

        self._document = Document(800, 600, name="未命名-1")
        self._canvas.document = self._document
        self._chat_panel.set_document(self._document)
        self._swatches_panel.update_swatches(self._document.swatches)
        self._update_all()

    def _on_open(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "",
            "Illustrator JSON (*.ai.json);;所有文件 (*.*)",
        )
        if file_path:
            try:
                self._document = Document.load(file_path)
                self._canvas.document = self._document
                self._chat_panel.set_document(self._document)
                self._swatches_panel.update_swatches(self._document.swatches)
                self._update_all()
            except Exception as e:
                logger.error(f"打开文件失败: {file_path} - {e}", exc_info=True)
                QMessageBox.critical(self, "错误", f"无法打开文件：{e}")

    def _on_save(self):
        # 定义私有方法，处理保存操作
        if not self._document:
            return
        if self._document.file_path:
            self._document.save(self._document.file_path)
            self._update_title()
        else:
            self._on_save_as()

    def _on_save_as(self):
        if not self._document:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "另存为", "未命名.ai.json",
            "Illustrator JSON (*.ai.json);;所有文件 (*.*)",
        )
        if file_path:
            self._document.save(file_path)
            self._update_title()

    # ── 通用导出渲染器 ──────────────────────────────────────────────
    # 将画布中所有可见内容渲染到 QPainter 上（画板 + 递归图层）
    # painter 应已完成 translate（原点置于画布中心）和/或 scale

    def _render_document(self, painter: QPainter):
        """将文档完整内容渲染到 painter 上（画板 + 递归图层）。
        
        坐标系：输出设备的 (0,0) 直接对应画板左上角，
        无需额外平移。_draw_artboard 从 (0,0) 开始绘制，
        各 item 通过 _transform 定位到文档坐标系。
        
        与 paintEvent 的区别：paintEvent 需要 translate(center+pan_offset)
        使画板居中显示在窗口中；导出时输出设备尺寸=文档尺寸，
        画板自然填满整个输出区域。
        """
        doc = self._document
        if not doc:
            return
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # 画板（从文档坐标原点 (0,0) 开始）
        self._canvas._draw_artboard(painter)

        # 递归遍历所有图层（含子图层、编组）
        for layer in doc.layers:
            if layer.visible:
                self._canvas._draw_layer_recursive(painter, layer)

    # ── 导出为 PNG ──

    def _on_export_png(self):
        if not self._document:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出为 PNG", "未命名.png", "PNG 图片 (*.png)",
        )
        if not file_path:
            return
        self._export_to_pixmap(file_path, "PNG")

    # ── 导出为 JPEG ──

    def _on_export_jpeg(self):
        if not self._document:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出为 JPEG", "未命名.jpg",
            "JPEG 图片 (*.jpg *.jpeg);;所有文件 (*.*)",
        )
        if not file_path:
            return
        self._export_to_pixmap(file_path, "JPEG", quality=95)

    def _export_to_pixmap(self, file_path: str, fmt: str, quality: int = -1):
        """通用位图导出：渲染文档到 QPixmap → 保存为 PNG / JPEG"""
        doc = self._document
        pixmap = QPixmap(int(doc.width), int(doc.height))

        painter = QPainter(pixmap)
        # ★ 不需要 translate：输出设备(0,0)=画布原点(0,0)，画板自动填满
        self._render_document(painter)
        painter.end()

        if quality > 0:
            pixmap.save(file_path, fmt, quality)
        else:
            pixmap.save(file_path, fmt)
        QMessageBox.information(self, "导出成功", f"已导出到：\n{file_path}")

    # ── 导出为 PDF ──

    def _on_export_pdf(self):
        if not self._document:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出为 PDF", "未命名.pdf", "PDF 文件 (*.pdf)",
        )
        if not file_path:
            return

        doc = self._document
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_path)
        printer.setPageSizeMM(doc.width * 0.264583, doc.height * 0.264583)
        printer.setPageMargins(0, 0, 0, 0, QPrinter.Point)

        painter = QPainter(printer)
        # ★ 不需要 translate：PDF 页面(0,0)=画布原点(0,0)
        self._render_document(painter)
        painter.end()
        QMessageBox.information(self, "导出成功", f"已导出到：\n{file_path}")

    # ── 导出为 SVG ──

    def _on_export_svg(self):
        if not self._document:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出为 SVG", "未命名.svg", "SVG 文件 (*.svg)",
        )
        if not file_path:
            return

        doc = self._document
        generator = QSvgGenerator()
        generator.setFileName(file_path)
        generator.setSize(QSize(int(doc.width), int(doc.height)))
        generator.setViewBox(QRectF(0, 0, doc.width, doc.height))
        generator.setTitle("Mini Illustrator")
        generator.setDescription("由简易 Illustrator 生成")

        painter = QPainter(generator)
        # ★ 不需要 translate：SVG viewBox(0,0)=画布原点(0,0)
        self._render_document(painter)
        painter.end()
        QMessageBox.information(self, "导出成功", f"已导出到：\n{file_path}")

    def keyPressEvent(self, event):
        """主窗口快捷键 —— F7 打开图层面板（PDF 快捷键表）"""
        if event.key() == Qt.Key_F7:
            # 切换图层面板可见性
            for dock in self.findChildren(QDockWidget):
                w = dock.widget()
                if w and hasattr(w, '_layers_data'):
                    dock.setVisible(not dock.isVisible())
                    return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        logger.info("应用程序正在关闭")
        if self._document and self._document.modified:
            ret = QMessageBox.question(
                self, "未保存的更改",
                "是否保存当前文档的更改？",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            )
            match ret:
                case QMessageBox.Save:
                    # 如果文档有路径直接保存，否则弹出另存为对话框
                    if self._document.file_path:
                        self._document.save(self._document.file_path)
                        event.accept()
                    else:
                        # 另存为对话框，用户可能取消
                        file_path, _ = QFileDialog.getSaveFileName(
                            self, "另存为", "未命名.ai.json",
                            "Illustrator JSON (*.ai.json);;所有文件 (*.*)",
                        )
                        if file_path:
                            self._document.save(file_path)
                            event.accept()
                        else:
                            event.ignore()
                case QMessageBox.Discard:
                    event.accept()
                case _:
                    event.ignore()
        else:
            event.accept()
