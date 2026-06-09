# main_window.py 逐行中文注解翻译

---

```python
"""
```
# 模块文档字符串开始

```python
主窗口 (Python 3.10+) —— 组合所有组件，处理菜单、快捷键和面板交互
```
# 模块功能说明：主窗口（要求 Python 3.10 及以上版本）—— 组合所有组件，处理菜单、快捷键和面板交互

```python

```
# 空行

```python
集成 DeepSeek AI 助手 —— 交互式对话生成矢量文本海报
```
# 功能说明：集成 DeepSeek AI 助手 —— 通过交互式对话生成矢量文本海报

```python

```
# 空行

```python
架构优化:
```
# 架构优化说明：

```python
- 使用 __slots__ 减少内存占用
```
#   - 使用 `__slots__`（槽位）减少内存占用

```python
- 使用 X | None 替代 Optional[X]
```
#   - 使用 `X | None` 语法替代 `Optional[X]`（更简洁的可选类型写法）

```python
- 使用 match-case 进行类型分发
```
#   - 使用 `match-case`（模式匹配）进行类型分发

```python
"""
```
# 模块文档字符串结束

```python

```
# 空行

```python
from __future__ import annotations
```
# 从 `__future__` 模块导入注解特性（允许在类型注解中使用尚未定义的类型名，延迟求值）

```python

```
# 空行

```python
import traceback
```
# 导入 `traceback`（堆栈跟踪）模块，用于异常处理时输出详细的调用栈信息

```python

```
# 空行

```python
from PyQt5.QtCore import Qt, QPointF
```
# 从 PyQt5 的核心模块导入 `Qt`（Qt 命名空间枚举）和 `QPointF`（二维浮点坐标点类）

```python
from PyQt5.QtGui import (
```
# 从 PyQt5 的图形界面模块导入以下类：

```python
    QKeySequence, QColor, QPainter, QPixmap, QPainterPath,
```
#   `QKeySequence`（快捷键序列）、`QColor`（颜色）、`QPainter`（绘图器）、`QPixmap`（像素图像）、`QPainterPath`（绘图路径）

```python
)
```
# 导入语句结束

```python
from PyQt5.QtWidgets import (
```
# 从 PyQt5 的控件模块导入以下类：

```python
    QMainWindow, QVBoxLayout, QHBoxLayout,
```
#   `QMainWindow`（主窗口）、`QVBoxLayout`（垂直布局）、`QHBoxLayout`（水平布局）

```python
    QMenuBar, QMenu, QAction, QToolBar, QStatusBar, QLabel,
```
#   `QMenuBar`（菜单栏）、`QMenu`（菜单）、`QAction`（操作动作）、`QToolBar`（工具栏）、`QStatusBar`（状态栏）、`QLabel`（标签）

```python
    QFileDialog, QMessageBox, QDockWidget,
```
#   `QFileDialog`（文件对话框）、`QMessageBox`（消息对话框）、`QDockWidget`（可停靠窗口/停靠面板）

```python
    QApplication,
```
#   `QApplication`（应用程序）

```python
)
```
# 导入语句结束

```python
from PyQt5.QtCore import Qt as QtCore_Qt  # 避免与 panel 中的 Qt 冲突
```
# 从 PyQt5 核心模块再次导入 `Qt`，别名为 `QtCore_Qt`，避免与面板（panel）模块中的 `Qt` 命名冲突

```python

```
# 空行

```python
from ..logging_config import get_logger
```
# 从上级包的日志配置模块导入 `get_logger`（获取日志记录器的工厂函数）

```python
from ..core.graphics import (
```
# 从上级核心包的图形模块导入以下类：

```python
    GraphicItem, PathItem, RectangleItem, EllipseItem,
```
#   `GraphicItem`（图形项基类）、`PathItem`（路径项）、`RectangleItem`（矩形项）、`EllipseItem`（椭圆项）

```python
    TextFrame, GroupItem, GraphicStyle, Swatch, Justification,
```
#   `TextFrame`（文本框）、`GroupItem`（编组项）、`GraphicStyle`（图形样式）、`Swatch`（色板）、`Justification`（对齐方式枚举）

```python
    Gradient, GradientType, GradientStop, AnchorPoint,
```
#   `Gradient`（渐变）、`GradientType`（渐变类型）、`GradientStop`（渐变停靠点）、`AnchorPoint`（锚点）

```python
)
```
# 导入语句结束

```python
from ..core.document import Document, Layer
```
# 从上级核心包的文档模块导入 `Document`（文档类）和 `Layer`（图层类）

```python
from ..core.tools import ToolType
```
# 从上级核心包的工具模块导入 `ToolType`（工具类型枚举）

```python
from .canvas import CanvasWidget
```
# 从当前包的画布模块导入 `CanvasWidget`（画布控件类）

```python
from .panels import ToolBar, PropertiesPanel, LayersPanel, SwatchesPanel
```
# 从当前包的面板模块导入 `ToolBar`（工具栏面板）、`PropertiesPanel`（属性面板）、`LayersPanel`（图层面板）、`SwatchesPanel`（色板面板）

```python
from .collapsible_panel import PanelContainer
```
# 从当前包的可折叠面板模块导入 `PanelContainer`（面板容器类）

```python
from ..ai.chat_panel import ChatPanel
```
# 从上级 AI 包的聊天面板模块导入 `ChatPanel`（AI 聊天面板类）

```python

```
# 空行

```python
logger = get_logger(__name__)
```
# 获取当前模块专属的日志记录器实例，`__name__` 为模块的完整名称

```python

```
# 空行

```python

```
# 空行

```python
class MainWindow(QMainWindow):
```
# 定义 `主窗口` 类，继承自 PyQt5 的 `QMainWindow`（Qt 主窗口基类）

```python
    """主窗口
```
#     类文档字符串：主窗口

```python
    注意: PyQt5 的 QWidget/QMainWindow 子类不能使用 __slots__，
```
#     注意说明：PyQt5 的 QWidget/QMainWindow 子类不能使用 `__slots__`（槽位机制），

```python
    否则 sip wrapper 内部状态会异常，导致应用闪退。
```
#     否则 sip 包装器（PyQt5 内部 C++ 绑定层）的内部状态会异常，导致应用程序闪退。

```python
    """
```
#     类文档字符串结束

```python

```
#     空行

```python
    def __init__(self):
```
#     定义初始化方法（构造函数），接收自身引用参数 `self`

```python
        super().__init__()
```
#         调用父类 `QMainWindow` 的初始化方法，完成基类初始化

```python
        self._document: Document | None = None
```
#         声明私有实例属性 `_document`（文档），类型为 `文档` 或 `None`，初始值为 `None`

```python
        self._current_file: str | None = None
```
#         声明私有实例属性 `_current_file`（当前文件路径），类型为 `字符串` 或 `None`，初始值为 `None`

```python
        self._clipboard: list[GraphicItem] = []
```
#         声明私有实例属性 `_clipboard`（剪贴板），类型为 `图形项` 列表，初始值为空列表

```python
        self._init_document()
```
#         调用私有方法 `_init_document`（初始化文档）

```python
        self._init_ui()
```
#         调用私有方法 `_init_ui`（初始化用户界面）

```python
        self._connect_signals()
```
#         调用私有方法 `_connect_signals`（连接信号与槽）

```python

```
#     空行

```python
    def _init_document(self):
```
#     定义私有方法 `_init_document`（初始化文档），接收自身引用参数

```python
        self._document = Document(800, 600, name="未命名-1")
```
#         创建一个 `Document`（文档）实例，宽度 800、高度 600，名称为 "未命名-1"，赋值给 `_document`

```python
        logger.info("主窗口初始化完成")
```
#         通过日志记录器输出信息级别日志："主窗口初始化完成"

```python

```
#     空行

```python
    # ── UI 初始化 ──
```
#     分隔注释：── 用户界面初始化 ──

```python

```
#     空行

```python
    def _init_ui(self):
```
#     定义私有方法 `_init_ui`（初始化用户界面），接收自身引用参数

```python
        self.setWindowTitle("简易 Illustrator — 未命名-1")
```
#         设置窗口标题为 "简易 Illustrator — 未命名-1"

```python
        self.resize(1280, 800)
```
#         设置窗口初始大小为宽度 1280 像素、高度 800 像素

```python

```
#         空行

```python
        self.setStyleSheet("""
```
#         设置全局样式表（层叠样式），内容开始：

```python
            QMainWindow { background-color: #2d2d2d; }
```
#             主窗口背景色为深灰色（#2d2d2d）

```python
            QMenuBar { background-color: #3c3c3c; color: #ddd; border-bottom: 1px solid #555; }
```
#             菜单栏背景色 #3c3c3c，文字颜色浅灰色 #ddd，底部边框 1px 实线 #555

```python
            QMenuBar::item:selected { background-color: #0d6efd; }
```
#             菜单栏项目选中时背景色为蓝色（#0d6efd）

```python
            QMenu { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; }
```
#             下拉菜单背景色 #3c3c3c，文字颜色 #ddd，边框 1px 实线 #555

```python
            QMenu::item:selected { background-color: #0d6efd; }
```
#             下拉菜单项目选中时背景色为蓝色（#0d6efd）

```python
            QStatusBar { background-color: #007acc; color: white; }
```
#             状态栏背景色为蓝色（#007acc），文字颜色白色

```python
            QDockWidget { color: #ddd; titlebar-close-icon: none; }
```
#             停靠面板文字颜色 #ddd，隐藏标题栏关闭按钮图标

```python
            QDockWidget::title { background-color: #3c3c3c; padding: 4px; }
```
#             停靠面板标题栏背景色 #3c3c3c，内边距 4 像素

```python
        """)
```
#         样式表字符串结束

```python

```
#         空行

```python
        self._canvas = CanvasWidget()
```
#         创建 `画布控件` 实例，赋值给 `_canvas`（画布）

```python
        self._canvas.document = self._document
```
#         将当前 `_document`（文档）赋值给画布的文档属性，使画布绑定到该文档

```python
        self.setCentralWidget(self._canvas)
```
#         将画布控件设置为主窗口的中央部件（主内容区域）

```python

```
#         空行

```python
        self._create_menus()
```
#         调用 `_create_menus`（创建菜单栏）方法

```python
        self._create_toolbar()
```
#         调用 `_create_toolbar`（创建工具栏）方法

```python
        self._create_panels()
```
#         调用 `_create_panels`（创建面板）方法

```python

```
#         空行

```python
        self._status_bar = QStatusBar()
```
#         创建 `状态栏` 实例，赋值给 `_status_bar`

```python
        self.setStatusBar(self._status_bar)
```
#         将状态栏设置为主窗口的底部状态栏

```python
        self._zoom_label = QLabel("100%")
```
#         创建缩放比例标签，初始显示 "100%"，赋值给 `_zoom_label`（缩放标签）

```python
        self._pos_label = QLabel("X: 0  Y: 0")
```
#         创建坐标位置标签，初始显示 "X: 0  Y: 0"，赋值给 `_pos_label`（位置标签）

```python
        self._tool_label = QLabel("选择工具")
```
#         创建当前工具名称标签，初始显示 "选择工具"，赋值给 `_tool_label`（工具标签）

```python
        self._status_bar.addPermanentWidget(self._tool_label)
```
#         将工具标签以永久控件方式添加到状态栏右侧

```python
        self._status_bar.addPermanentWidget(self._pos_label)
```
#         将位置标签以永久控件方式添加到状态栏右侧

```python
        self._status_bar.addPermanentWidget(self._zoom_label)
```
#         将缩放标签以永久控件方式添加到状态栏右侧

```python

```
#     空行

```python
    def _create_menus(self):
```
#     定义私有方法 `_create_menus`（创建菜单栏），接收自身引用参数

```python
        menubar = self.menuBar()
```
#         获取主窗口的菜单栏对象，赋值给 `menubar`（菜单栏）

```python

```
#         空行

```python
        # ── 文件菜单 ──
```
#         分隔注释：── 文件菜单 ──

```python
        file_menu = menubar.addMenu("文件(&F)")
```
#         在菜单栏添加 "文件(&F)" 菜单（&F 表示快捷键 Alt+F），赋值给 `file_menu`（文件菜单）

```python

```
#         空行

```python
        for label, shortcut, slot in [
```
#         遍历以下 "新建" 和 "打开" 操作的配置列表（标签、快捷键、槽函数）：

```python
            ("新建(&N)", QKeySequence.New, self._on_new),
```
#             标签 "新建(&N)"，快捷键为标准新建快捷键（Ctrl+N），槽函数为 `_on_new`（处理新建）

```python
            ("打开(&O)...", QKeySequence.Open, self._on_open),
```
#             标签 "打开(&O)..."，快捷键为标准打开快捷键（Ctrl+O），槽函数为 `_on_open`（处理打开）

```python
        ]:
```
#         配置列表结束

```python
            action = QAction(label, self)
```
#             创建 `操作动作` 实例，标签为 `label`，父对象为 `self`（主窗口）

```python
            action.setShortcut(shortcut)
```
#             为该操作动作设置快捷键为 `shortcut`

```python
            action.triggered.connect(slot)
```
#             将该操作动作的触发信号连接到槽函数 `slot`

```python
            file_menu.addAction(action)
```
#             将该操作动作添加到文件菜单中

```python

```
#         空行

```python
        file_menu.addSeparator()
```
#         在文件菜单中添加分隔线

```python

```
#         空行

```python
        save_action = QAction("保存(&S)", self)
```
#         创建 "保存(&S)" 操作动作，父对象为 `self`

```python
        save_action.setShortcut(QKeySequence.Save)
```
#         为保存操作设置标准保存快捷键（Ctrl+S）

```python
        save_action.triggered.connect(self._on_save)
```
#         将保存操作的触发信号连接到 `_on_save`（处理保存）槽函数

```python
        file_menu.addAction(save_action)
```
#         将保存操作添加到文件菜单中

```python

```
#         空行

```python
        save_as_action = QAction("另存为(&A)...", self)
```
#         创建 "另存为(&A)..." 操作动作，父对象为 `self`

```python
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
```
#         为另存为操作设置快捷键为 Ctrl+Shift+S

```python
        save_as_action.triggered.connect(self._on_save_as)
```
#         将另存为操作的触发信号连接到 `_on_save_as`（处理另存为）槽函数

```python
        file_menu.addAction(save_as_action)
```
#         将另存为操作添加到文件菜单中

```python

```
#         空行

```python
        file_menu.addSeparator()
```
#         在文件菜单中添加分隔线

```python

```
#         空行

```python
        export_action = QAction("导出为 PNG...", self)
```
#         创建 "导出为 PNG..." 操作动作，父对象为 `self`

```python
        export_action.setShortcut(QKeySequence("Ctrl+Shift+E"))
```
#         为导出操作设置快捷键为 Ctrl+Shift+E

```python
        export_action.triggered.connect(self._on_export)
```
#         将导出操作的触发信号连接到 `_on_export`（处理导出）槽函数

```python
        file_menu.addAction(export_action)
```
#         将导出操作添加到文件菜单中

```python

```
#         空行

```python
        file_menu.addSeparator()
```
#         在文件菜单中添加分隔线

```python

```
#         空行

```python
        exit_action = QAction("退出(&X)", self)
```
#         创建 "退出(&X)" 操作动作，父对象为 `self`

```python
        exit_action.setShortcut(QKeySequence("Alt+F4"))
```
#         为退出操作设置快捷键为 Alt+F4

```python
        exit_action.triggered.connect(self.close)
```
#         将退出操作的触发信号连接到主窗口的 `close`（关闭）方法

```python
        file_menu.addAction(exit_action)
```
#         将退出操作添加到文件菜单中

```python

```
#         空行

```python
        # ── 编辑菜单 ──
```
#         分隔注释：── 编辑菜单 ──

```python
        edit_menu = menubar.addMenu("编辑(&E)")
```
#         在菜单栏添加 "编辑(&E)" 菜单，赋值给 `edit_menu`（编辑菜单）

```python

```
#         空行

```python
        self._undo_action = QAction("撤销(&U)", self)
```
#         创建 "撤销(&U)" 操作动作，赋值给 `_undo_action`（撤销操作），父对象为 `self`

```python
        self._undo_action.setShortcut(QKeySequence.Undo)
```
#         为撤销操作设置标准撤销快捷键（Ctrl+Z）

```python
        self._undo_action.triggered.connect(self._on_undo)
```
#         将撤销操作的触发信号连接到 `_on_undo`（处理撤销）槽函数

```python
        self._undo_action.setEnabled(False)
```
#         初始状态下将撤销操作设为禁用（不可点击）

```python
        edit_menu.addAction(self._undo_action)
```
#         将撤销操作添加到编辑菜单中

```python

```
#         空行

```python
        self._redo_action = QAction("重做(&R)", self)
```
#         创建 "重做(&R)" 操作动作，赋值给 `_redo_action`（重做操作），父对象为 `self`

```python
        self._redo_action.setShortcut(QKeySequence.Redo)
```
#         为重做操作设置标准重做快捷键（Ctrl+Y）

```python
        self._redo_action.triggered.connect(self._on_redo)
```
#         将重做操作的触发信号连接到 `_on_redo`（处理重做）槽函数

```python
        self._redo_action.setEnabled(False)
```
#         初始状态下将重做操作设为禁用（不可点击）

```python
        edit_menu.addAction(self._redo_action)
```
#         将重做操作添加到编辑菜单中

```python

```
#         空行

```python
        edit_menu.addSeparator()
```
#         在编辑菜单中添加分隔线

```python

```
#         空行

```python
        for label, shortcut, slot in [
```
#         遍历以下 "复制" 和 "粘贴" 操作的配置列表：

```python
            ("复制(&C)", QKeySequence.Copy, self._on_copy),
```
#             标签 "复制(&C)"，快捷键为标准复制快捷键（Ctrl+C），槽函数为 `_on_copy`（处理复制）

```python
            ("粘贴(&V)", QKeySequence.Paste, self._on_paste),
```
#             标签 "粘贴(&V)"，快捷键为标准粘贴快捷键（Ctrl+V），槽函数为 `_on_paste`（处理粘贴）

```python
        ]:
```
#         配置列表结束

```python
            action = QAction(label, self)
```
#             创建操作动作，标签为 `label`，父对象为 `self`

```python
            action.setShortcut(shortcut)
```
#             为该操作动作设置快捷键

```python
            action.triggered.connect(slot)
```
#             将该操作动作的触发信号连接到槽函数

```python
            edit_menu.addAction(action)
```
#             将该操作动作添加到编辑菜单中

```python

```
#         空行

```python
        edit_menu.addSeparator()
```
#         在编辑菜单中添加分隔线

```python

```
#         空行

```python
        delete_action = QAction("删除(&D)", self)
```
#         创建 "删除(&D)" 操作动作，父对象为 `self`

```python
        delete_action.setShortcut(QKeySequence.Delete)
```
#         为删除操作设置标准删除快捷键（Delete 键）

```python
        delete_action.triggered.connect(self._on_delete)
```
#         将删除操作的触发信号连接到 `_on_delete`（处理删除）槽函数

```python
        edit_menu.addAction(delete_action)
```
#         将删除操作添加到编辑菜单中

```python

```
#         空行

```python
        select_all_action = QAction("全选(&A)", self)
```
#         创建 "全选(&A)" 操作动作，父对象为 `self`

```python
        select_all_action.setShortcut(QKeySequence.SelectAll)
```
#         为全选操作设置标准全选快捷键（Ctrl+A）

```python
        select_all_action.triggered.connect(self._on_select_all)
```
#         将全选操作的触发信号连接到 `_on_select_all`（处理全选）槽函数

```python
        edit_menu.addAction(select_all_action)
```
#         将全选操作添加到编辑菜单中

```python

```
#         空行

```python
        edit_menu.addSeparator()
```
#         在编辑菜单中添加分隔线

```python

```
#         空行

```python
        group_action = QAction("编组(&G)", self)
```
#         创建 "编组(&G)" 操作动作，父对象为 `self`

```python
        group_action.setShortcut(QKeySequence("Ctrl+G"))
```
#         为编组操作设置快捷键为 Ctrl+G

```python
        group_action.triggered.connect(self._on_group)
```
#         将编组操作的触发信号连接到 `_on_group`（处理编组）槽函数

```python
        edit_menu.addAction(group_action)
```
#         将编组操作添加到编辑菜单中

```python

```
#         空行

```python
        ungroup_action = QAction("取消编组", self)
```
#         创建 "取消编组" 操作动作，父对象为 `self`

```python
        ungroup_action.setShortcut(QKeySequence("Ctrl+Shift+G"))
```
#         为取消编组操作设置快捷键为 Ctrl+Shift+G

```python
        ungroup_action.triggered.connect(self._on_ungroup)
```
#         将取消编组操作的触发信号连接到 `_on_ungroup`（处理取消编组）槽函数

```python
        edit_menu.addAction(ungroup_action)
```
#         将取消编组操作添加到编辑菜单中

```python

```
#         空行

```python
        # ── 对象菜单 ──
```
#         分隔注释：── 对象菜单 ──

```python
        object_menu = menubar.addMenu("对象(&O)")
```
#         在菜单栏添加 "对象(&O)" 菜单，赋值给 `object_menu`（对象菜单）

```python

```
#         空行

```python
        for label, shortcut, slot in [
```
#         遍历以下图层排列操作的配置列表：

```python
            ("置于顶层", "Ctrl+Shift+]", self._on_bring_front),
```
#             "置于顶层"，快捷键 Ctrl+Shift+]，槽函数为 `_on_bring_front`（处理置于顶层）

```python
            ("上移一层", "Ctrl+]", self._on_bring_forward),
```
#             "上移一层"，快捷键 Ctrl+]，槽函数为 `_on_bring_forward`（处理上移一层）

```python
            ("下移一层", "Ctrl+[", self._on_send_backward),
```
#             "下移一层"，快捷键 Ctrl+[，槽函数为 `_on_send_backward`（处理下移一层）

```python
            ("置于底层", "Ctrl+Shift+[", self._on_send_to_back),
```
#             "置于底层"，快捷键 Ctrl+Shift+[，槽函数为 `_on_send_to_back`（处理置于底层）

```python
        ]:
```
#         配置列表结束

```python
            action = QAction(label, self)
```
#             创建操作动作，标签为 `label`，父对象为 `self`

```python
            action.setShortcut(QKeySequence(shortcut))
```
#             为该操作动作设置快捷键

```python
            action.triggered.connect(slot)
```
#             将该操作动作的触发信号连接到槽函数

```python
            object_menu.addAction(action)
```
#             将该操作动作添加到对象菜单中

```python

```
#         空行

```python
        object_menu.addSeparator()
```
#         在对象菜单中添加分隔线

```python

```
#         空行

```python
        # 对齐子菜单
```
#         注释：对齐子菜单

```python
        align_menu = object_menu.addMenu("对齐")
```
#         在对象菜单下添加 "对齐" 子菜单，赋值给 `align_menu`（对齐菜单）

```python
        for label, mode in [
```
#         遍历以下对齐方式配置列表（标签、模式标识）：

```python
            ("左对齐", "left"), ("水平居中", "center_h"), ("右对齐", "right"),
```
#             "左对齐"（左）、"水平居中"（水平居中）、"右对齐"（右）

```python
            ("顶部对齐", "top"), ("垂直居中", "center_v"), ("底部对齐", "bottom"),
```
#             "顶部对齐"（顶部）、"垂直居中"（垂直居中）、"底部对齐"（底部）

```python
        ]:
```
#         配置列表结束

```python
            action = QAction(label, self)
```
#             创建操作动作，标签为 `label`，父对象为 `self`

```python
            action.triggered.connect(lambda checked, m=mode: self._on_align(m))
```
#             将该操作的触发信号连接到匿名函数，调用 `_on_align`（处理对齐）并传入对齐模式 `m`

```python
            align_menu.addAction(action)
```
#             将该操作动作添加到对齐子菜单中

```python
            if mode == "right":
```
#             如果当前对齐模式为 "right"（右对齐）

```python
                align_menu.addSeparator()
```
#                 在对齐菜单中添加分隔线（水平对齐与垂直对齐之间的分隔）

```python

```
#         空行

```python
        object_menu.addSeparator()
```
#         在对象菜单中添加分隔线

```python

```
#         空行

```python
        # 路径查找器子菜单
```
#         注释：路径查找器子菜单

```python
        pathfinder_menu = object_menu.addMenu("路径查找器")
```
#         在对象菜单下添加 "路径查找器" 子菜单，赋值给 `pathfinder_menu`（路径查找器菜单）

```python
        for label, mode in [
```
#         遍历以下布尔运算配置列表：

```python
            ("合并（联集）", "union"),
```
#             "合并（联集）"，模式标识 "union"（联集/并集）

```python
            ("交集", "intersect"),
```
#             "交集"，模式标识 "intersect"（交集）

```python
            ("减去顶层", "subtract"),
```
#             "减去顶层"，模式标识 "subtract"（差集）

```python
        ]:
```
#         配置列表结束

```python
            action = QAction(label, self)
```
#             创建操作动作，标签为 `label`，父对象为 `self`

```python
            action.triggered.connect(lambda checked, m=mode: self._on_pathfinder(m))
```
#             将该操作的触发信号连接到匿名函数，调用 `_on_pathfinder`（处理路径查找器）并传入运算模式 `m`

```python
            pathfinder_menu.addAction(action)
```
#             将该操作动作添加到路径查找器子菜单中

```python

```
#         空行

```python
        # ── 图层菜单（完整对照 Ai 图层菜单） ──
```
#         分隔注释：── 图层菜单（完整对照 Adobe Illustrator 图层菜单） ──

```python
        layer_menu = menubar.addMenu("图层(&L)")
```
#         在菜单栏添加 "图层(&L)" 菜单，赋值给 `layer_menu`（图层菜单）

```python
        
```
#         空行（含缩进空格）

```python
        # 新建图层（第三章方法2）
```
#         注释：新建图层（第三章方法2）

```python
        new_layer_action = QAction("新建图层(&N)", self)
```
#         创建 "新建图层(&N)" 操作动作，父对象为 `self`

```python
        new_layer_action.setShortcut(QKeySequence("Ctrl+L"))
```
#         为新建图层操作设置快捷键为 Ctrl+L

```python
        new_layer_action.triggered.connect(self._on_add_layer)
```
#         将新建图层操作的触发信号连接到 `_on_add_layer`（处理添加图层）槽函数

```python
        layer_menu.addAction(new_layer_action)
```
#         将新建图层操作添加到图层菜单中

```python
        
```
#         空行

```python
        # 新建子图层（第十章）
```
#         注释：新建子图层（第十章功能）

```python
        new_sublayer_action = QAction("新建子图层(&S)", self)
```
#         创建 "新建子图层(&S)" 操作动作，父对象为 `self`

```python
        new_sublayer_action.triggered.connect(lambda: self._layers_panel._on_add_sublayer())
```
#         将新建子图层操作的触发信号连接到匿名函数，调用图层面板的 `_on_add_sublayer`（处理新建子图层）方法

```python
        layer_menu.addAction(new_sublayer_action)
```
#         将新建子图层操作添加到图层菜单中

```python
        
```
#         空行

```python
        layer_menu.addSeparator()
```
#         在图层菜单中添加分隔线

```python
        
```
#         空行

```python
        # 复制图层（第六章）
```
#         注释：复制图层（第六章功能）

```python
        dup_layer_action = QAction("复制图层(&D)", self)
```
#         创建 "复制图层(&D)" 操作动作，父对象为 `self`

```python
        dup_layer_action.triggered.connect(
```
#         将复制图层操作的触发信号连接到以下匿名函数：

```python
            lambda: self._on_duplicate_layer(self._document.active_layer_index) if self._document else None
```
#             如果文档存在，调用 `_on_duplicate_layer`（处理复制图层）并传入当前活动图层索引；否则返回 None

```python
        )
```
#         匿名函数结束

```python
        layer_menu.addAction(dup_layer_action)
```
#         将复制图层操作添加到图层菜单中

```python
        
```
#         空行

```python
        # 删除图层（第五章）
```
#         注释：删除图层（第五章功能）

```python
        del_layer_action = QAction("删除图层", self)
```
#         创建 "删除图层" 操作动作，父对象为 `self`

```python
        del_layer_action.triggered.connect(
```
#         将删除图层操作的触发信号连接到以下匿名函数：

```python
            lambda: self._on_remove_layer(self._document.active_layer_index) if self._document else None
```
#             如果文档存在，调用 `_on_remove_layer`（处理删除图层）并传入当前活动图层索引；否则返回 None

```python
        )
```
#         匿名函数结束

```python
        layer_menu.addAction(del_layer_action)
```
#         将删除图层操作添加到图层菜单中

```python
        
```
#         空行

```python
        layer_menu.addSeparator()
```
#         在图层菜单中添加分隔线

```python
        
```
#         空行

```python
        # 当前图层的选项...（图层选项对话框）
```
#         注释：当前图层的选项...（打开图层选项对话框）

```python
        layer_opts_action = QAction("当前图层的选项...", self)
```
#         创建 "当前图层的选项..." 操作动作，父对象为 `self`

```python
        layer_opts_action.triggered.connect(
```
#         将图层选项操作的触发信号连接到以下匿名函数：

```python
            lambda: self._layers_panel._show_layer_options_dialog(
```
#             如果文档存在，调用图层面板的 `_show_layer_options_dialog`（显示图层选项对话框）方法：

```python
                self._document.active_layer_index
```
#                 传入当前活动图层索引

```python
            ) if self._document else None
```
#             否则返回 None

```python
        )
```
#         匿名函数结束

```python
        layer_menu.addAction(layer_opts_action)
```
#         将图层选项操作添加到图层菜单中

```python
        
```
#         空行

```python
        layer_menu.addSeparator()
```
#         在图层菜单中添加分隔线

```python
        
```
#         空行

```python
        # 选择整个图层（第十四章）
```
#         注释：选择整个图层（第十四章功能）

```python
        select_layer_action = QAction("选择当前图层所有对象", self)
```
#         创建 "选择当前图层所有对象" 操作动作，父对象为 `self`

```python
        select_layer_action.triggered.connect(
```
#         将选择图层操作的触发信号连接到以下匿名函数：

```python
            lambda: self._on_select_all_in_layer(self._document.active_layer_index) if self._document else None
#             如果文档存在，调用 `_on_select_all_in_layer` 并传入当前活动图层索引；否则返回 None

```python
        )
```
#         匿名函数结束

```python
        layer_menu.addAction(select_layer_action)
```
#         将选择图层操作添加到图层菜单中

```python
        
```
#         空行

```python
        # 隐藏/显示其他图层
```
#         注释：隐藏/显示其他图层

```python
        hide_others_action = QAction("隐藏其他图层", self)
```
#         创建 "隐藏其他图层" 操作动作，父对象为 `self`

```python
        hide_others_action.triggered.connect(
```
#         将隐藏其他图层操作的触发信号连接到以下匿名函数：

```python
            lambda: self._layers_panel._hide_other_layers(self._document.active_layer_index) if self._document else None
```
#             如果文档存在，调用图层面板的 `_hide_other_layers`（隐藏其他图层）方法并传入当前活动图层索引；否则返回 None

```python
        )
```
#         匿名函数结束

```python
        layer_menu.addAction(hide_others_action)
```
#         将隐藏其他图层操作添加到图层菜单中

```python
        
```
#         空行

```python
        # 锁定其他图层
```
#         注释：锁定其他图层

```python
        lock_others_action = QAction("锁定其他图层", self)
```
#         创建 "锁定其他图层" 操作动作，父对象为 `self`

```python
        lock_others_action.triggered.connect(
```
#         将锁定其他图层操作的触发信号连接到以下匿名函数：

```python
            lambda: self._layers_panel._lock_other_layers(self._document.active_layer_index) if self._document else None
```
#             如果文档存在，调用图层面板的 `_lock_other_layers`（锁定其他图层）方法并传入当前活动图层索引；否则返回 None

```python
        )
```
#         匿名函数结束

```python
        layer_menu.addAction(lock_others_action)
```
#         将锁定其他图层操作添加到图层菜单中

```python
        
```
#         空行

```python
        layer_menu.addSeparator()
```
#         在图层菜单中添加分隔线

```python        
```
#         空行

```python
        # 收集到新图层（第十五章）
```
#         注释：收集到新图层（第十五章功能）

```python
        collect_action = QAction("收集到新图层(&C)", self)
```
#         创建 "收集到新图层(&C)" 操作动作，父对象为 `self`

```python
        collect_action.triggered.connect(self._on_collect_layer)
```
#         将收集操作到新图层的触发信号连接到 `_on_collect_layer`（处理收集到新图层）槽函数

```python
        layer_menu.addAction(collect_action)
```
#         将收集到新图层操作添加到图层菜单中

```python
        
```
#         空行

```python
        # 释放到图层（第十六章）
```
#         注释：释放到图层（第十六章功能）

```python
        release_menu = layer_menu.addMenu("释放到图层")
```
#         在图层菜单下添加 "释放到图层" 子菜单，赋值给 `release_menu`（释放到图层菜单）

```python
        release_seq = QAction("顺序 (Sequence)", self)
```
#         创建 "顺序 (Sequence)" 操作动作，父对象为 `self`

```python
        release_seq.triggered.connect(self._on_release_sequence)
```
#         将顺序释放操作的触发信号连接到 `_on_release_sequence`（处理按顺序释放到图层）槽函数

```python
        release_menu.addAction(release_seq)
```
#         将顺序释放操作添加到释放到图层子菜单中

```python
        release_build = QAction("构建 (Build)", self)
```
#         创建 "构建 (Build)" 操作动作，父对象为 `self`

```python
        release_build.triggered.connect(self._on_release_build)
```
#         将构建释放操作的触发信号连接到 `_on_release_build`（处理按构建释放到图层）槽函数

```python
        release_menu.addAction(release_build)
```
#         将构建释放操作添加到释放到图层子菜单中

```python
        
```
#         空行

```python
        layer_menu.addSeparator()
```
#         在图层菜单中添加分隔线

```python        
```
#         空行

```python
        # 合并选定图层（第十七章）
```
#         注释：合并选定图层（第十七章功能）

```python
        merge_action = QAction("合并选定图层(&M)", self)
```
#         创建 "合并选定图层(&M)" 操作动作，父对象为 `self`

```python
        merge_action.triggered.connect(
```
#         将合并图层操作的触发信号连接到以下匿名函数：

```python
            lambda: self._on_merge_layers([self._document.active_layer_index]) if self._document else None
```
#             如果文档存在，调用 `_on_merge_layers` 并传入包含当前活动图层索引的列表；否则返回 None

```python
        )
```
#         匿名函数结束

```python
        layer_menu.addAction(merge_action)
```
#         将合并图层操作添加到图层菜单中

```python        
```
#         空行

```python
        # 拼合图稿（第十八章）
```
#         注释：拼合图稿（第十八章功能）

```python
        flatten_action = QAction("拼合图稿(&F)", self)
```
#         创建 "拼合图稿(&F)" 操作动作，父对象为 `self`

```python
        flatten_action.triggered.connect(self._on_flatten)
```
#         将拼合图稿操作的触发信号连接到 `_on_flatten`（处理拼合图稿）槽函数

```python
        layer_menu.addAction(flatten_action)
```
#         将拼合图稿操作添加到图层菜单中

```python

```
#         空行

```python
        # ── 视图菜单 ──
```
#         分隔注释：── 视图菜单 ──

```python
        view_menu = menubar.addMenu("视图(&V)")
```
#         在菜单栏添加 "视图(&V)" 菜单，赋值给 `view_menu`（视图菜单）

```python
        for label, shortcut, slot in [
```
#         遍历以下视图缩放操作配置列表：

```python
            ("放大", "Ctrl++", self._canvas.zoom_in),
```
#             "放大"，快捷键 Ctrl++，槽函数为画布的 `zoom_in`（放大）方法

```python
            ("缩小", "Ctrl+-", self._canvas.zoom_out),
```
#             "缩小"，快捷键 Ctrl+-，槽函数为画布的 `zoom_out`（缩小）方法

```python
            ("适合窗口", "Ctrl+0", self._canvas.zoom_to_fit),
```
#             "适合窗口"，快捷键 Ctrl+0，槽函数为画布的 `zoom_to_fit`（适合窗口）方法

```python
            ("100%", "Ctrl+1", self._canvas.zoom_100),
```
#             "100%"，快捷键 Ctrl+1，槽函数为画布的 `zoom_100`（100%缩放）方法

```python
        ]:
```
#         配置列表结束

```python
            action = QAction(label, self)
```
#             创建操作动作，标签为 `label`，父对象为 `self`

```python
            action.setShortcut(QKeySequence(shortcut))
```
#             为该操作动作设置快捷键

```python
            action.triggered.connect(slot)
```
#             将该操作动作的触发信号连接到槽函数

```python
            view_menu.addAction(action)
```
#             将该操作动作添加到视图菜单中

```python

```
#     空行

```python
    def _create_toolbar(self):
```
#     定义私有方法 `_create_toolbar`（创建工具栏），接收自身引用参数

```python
        toolbar = QToolBar("快速操作")
```
#         创建 `工具栏` 实例，标题为 "快速操作"，赋值给 `toolbar`

```python
        toolbar.setMovable(False)
```
#         将工具栏设为不可移动（固定位置）

```python
        self.addToolBar(toolbar)
```
#         将工具栏添加到主窗口中

```python

```
#         空行

```python
        for name, slot in [
```
#         遍历以下快速操作按钮配置列表（按钮名称、槽函数）：

```python
            ("新建", self._on_new), ("打开", self._on_open), ("保存", self._on_save),
```
#             "新建"→`_on_new`、"打开"→`_on_open`、"保存"→`_on_save`

```python
        ]:
```
#         配置列表结束

```python
            action = QAction(name, self)
```
#             创建操作动作，名称为 `name`，父对象为 `self`

```python
            action.triggered.connect(slot)
```
#             将该操作动作的触发信号连接到槽函数

```python
            toolbar.addAction(action)
```
#             将该操作动作添加到工具栏中

```python

```
#         空行

```python
        toolbar.addSeparator()
```
#         在工具栏中添加分隔线

```python
        toolbar.addWidget(QLabel(" 缩放: "))
```
#         在工具栏中添加一个标签控件，显示 " 缩放: "

```python

```
#         空行

```python
        toolbar.setStyleSheet("""
```
#         设置工具栏样式表：

```python
            QToolBar { background-color: #3c3c3c; border-bottom: 1px solid #555; spacing: 4px; padding: 2px; }
```
#             工具栏背景色 #3c3c3c，底部边框 1px 实线 #555，元素间距 4px，内边距 2px

```python
            QToolBar QAction { color: #ddd; padding: 4px 8px; }
```
#             工具栏中的操作按钮文字颜色 #ddd，内边距上下 4px、左右 8px

```python
            QToolBar QAction:hover { background-color: #5a5a5a; }
```
#             工具栏中的操作按钮悬停时背景色 #5a5a5a

```python
        """)
```
#         样式表字符串结束

```python

```
#     空行

```python
    def _create_panels(self):
```
#     定义私有方法 `_create_panels`（创建面板），接收自身引用参数

```python
        self._properties_panel = PropertiesPanel()
```
#         创建 `属性面板` 实例，赋值给 `_properties_panel`

```python
        self._layers_panel = LayersPanel()
```
#         创建 `图层面板` 实例，赋值给 `_layers_panel`

```python
        self._swatches_panel = SwatchesPanel()
```
#         创建 `色板面板` 实例，赋值给 `_swatches_panel`

```python
        self._chat_panel = ChatPanel()
```
#         创建 `AI聊天面板` 实例，赋值给 `_chat_panel`

```python

```
#         空行

```python
        container = PanelContainer()
```
#         创建 `面板容器` 实例（可折叠面板），赋值给 `container`

```python
        container.add_section("🤖 AI 助手", self._chat_panel, expanded=True)
```
#         在面板容器中添加 "🤖 AI 助手" 分区，内容为 AI 聊天面板，默认展开

```python
        container.add_section("属性", self._properties_panel, expanded=True)
```
#         在面板容器中添加 "属性" 分区，内容为属性面板，默认展开

```python
        container.add_section("图层", self._layers_panel, expanded=True)
```
#         在面板容器中添加 "图层" 分区，内容为图层面板，默认展开

```python
        container.add_section("色板", self._swatches_panel, expanded=False)
```
#         在面板容器中添加 "色板" 分区，内容为色板面板，默认折叠

```python

```
#         空行

```python
        right_dock = QDockWidget("面板", self)
```
#         创建右侧 `停靠窗口` 实例，标题为 "面板"，父对象为 `self`

```python
        right_dock.setWidget(container)
```
#         将面板容器设置为右侧停靠窗口的内容控件

```python
        right_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
```
#         将右侧停靠窗口设为不可拖拽、不可浮动、不可关闭（固定面板）

```python
        self.addDockWidget(Qt.RightDockWidgetArea, right_dock)
```
#         将右侧停靠窗口添加到主窗口的右侧停靠区域

```python

```
#         空行

```python
        self._tool_bar = ToolBar()
```
#         创建左侧 `工具栏面板` 实例，赋值给 `_tool_bar`

```python
        tools_dock = QDockWidget("工具", self)
```
#         创建左侧 `停靠窗口` 实例，标题为 "工具"，父对象为 `self`

```python
        tools_dock.setWidget(self._tool_bar)
```
#         将工具栏面板设置为左侧停靠窗口的内容控件

```python
        tools_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
```
#         将左侧停靠窗口设为不可拖拽、不可浮动、不可关闭（固定面板）

```python
        tools_dock.setFixedWidth(56)
```
#         将左侧停靠窗口的宽度固定为 56 像素

```python
        self.addDockWidget(Qt.LeftDockWidgetArea, tools_dock)
```
#         将左侧停靠窗口添加到主窗口的左侧停靠区域

```python

```
#     空行

```python
    # ── 信号连接 ──
```
#     分隔注释：── 信号连接 ──

```python

```
#     空行

```python
    def _connect_signals(self):
```
#     定义私有方法 `_connect_signals`（连接信号与槽），接收自身引用参数

```python
        self._tool_bar.tool_selected.connect(self._canvas.set_tool)
```
#         将工具栏的 `tool_selected`（工具选中）信号连接到画布的 `set_tool`（设置工具）方法

```python

```
#         空行

```python
        self._canvas.item_selected.connect(self._on_selection_changed)
```
#         将画布的 `item_selected`（图元选中）信号连接到 `_on_selection_changed`（处理选中变更）方法

```python
        self._canvas.mouse_position_changed.connect(self._on_mouse_move)
```
#         将画布的 `mouse_position_changed`（鼠标位置变更）信号连接到 `_on_mouse_move`（处理鼠标移动）方法

```python
        self._canvas.tool_changed.connect(self._on_tool_changed)
```
#         将画布的 `tool_changed`（工具变更）信号连接到 `_on_tool_changed`（处理工具变更）方法

```python
        self._canvas.item_modified.connect(self._update_all)
```
#         将画布的 `item_modified`（图元修改）信号连接到 `_update_all`（更新全部）方法

```python

```
#         空行

```python
        self._properties_panel.fill_color_changed.connect(self._on_fill_color)
```
#         将属性面板的 `fill_color_changed`（填充色变更）信号连接到 `_on_fill_color`（处理填充色）方法

```python
        self._properties_panel.stroke_color_changed.connect(self._on_stroke_color)
```
#         将属性面板的 `stroke_color_changed`（描边色变更）信号连接到 `_on_stroke_color`（处理描边色）方法

```python
        self._properties_panel.stroke_width_changed.connect(self._on_stroke_width)
```
#         将属性面板的 `stroke_width_changed`（描边宽度变更）信号连接到 `_on_stroke_width`（处理描边宽度）方法

```python
        self._properties_panel.opacity_changed.connect(self._on_opacity)
```
#         将属性面板的 `opacity_changed`（不透明度变更）信号连接到 `_on_opacity`（处理不透明度）方法

```python
        self._properties_panel.corner_radius_changed.connect(self._on_corner_radius)
```
#         将属性面板的 `corner_radius_changed`（圆角半径变更）信号连接到 `_on_corner_radius`（处理圆角半径）方法

```python
        self._properties_panel.text_changed.connect(self._on_text_changed)
```
#         将属性面板的 `text_changed`（文本变更）信号连接到 `_on_text_changed`（处理文本变更）方法

```python
        self._properties_panel.font_size_changed.connect(self._on_font_size)
```
#         将属性面板的 `font_size_changed`（字体大小变更）信号连接到 `_on_font_size`（处理字体大小）方法

```python
        self._properties_panel.font_family_changed.connect(self._on_font_family)
```
#         将属性面板的 `font_family_changed`（字体族变更）信号连接到 `_on_font_family`（处理字体族）方法

```python
        self._properties_panel.bold_changed.connect(self._on_bold)
```
#         将属性面板的 `bold_changed`（粗体变更）信号连接到 `_on_bold`（处理粗体）方法

```python
        self._properties_panel.italic_changed.connect(self._on_italic)
```
#         将属性面板的 `italic_changed`（斜体变更）信号连接到 `_on_italic`（处理斜体）方法

```python
        self._properties_panel.alignment_changed.connect(self._on_alignment)
```
#         将属性面板的 `alignment_changed`（对齐方式变更）信号连接到 `_on_alignment`（处理对齐方式）方法

```python
        self._properties_panel.order_front.connect(self._on_bring_front)
```
#         将属性面板的 `order_front`（置于顶层）信号连接到 `_on_bring_front`（处理置于顶层）方法

```python
        self._properties_panel.order_back.connect(self._on_send_to_back)
```
#         将属性面板的 `order_back`（置于底层）信号连接到 `_on_send_to_back`（处理置于底层）方法

```python
        self._properties_panel.order_forward.connect(self._on_bring_forward)
```
#         将属性面板的 `order_forward`（上移一层）信号连接到 `_on_bring_forward`（处理上移一层）方法

```python
        self._properties_panel.order_backward.connect(self._on_send_backward)
```
#         将属性面板的 `order_backward`（下移一层）信号连接到 `_on_send_backward`（处理下移一层）方法

```python
        self._properties_panel.delete_requested.connect(self._on_delete)
```
#         将属性面板的 `delete_requested`（请求删除）信号连接到 `_on_delete`（处理删除）方法

```python

```
#         空行

```python
        self._layers_panel.layer_selected.connect(self._on_layer_selected)
```
#         将图层面板的 `layer_selected`（图层选中）信号连接到 `_on_layer_selected`（处理图层选中）方法

```python
        self._layers_panel.layer_add_requested.connect(self._on_add_layer)
```
#         将图层面板的 `layer_add_requested`（请求添加图层）信号连接到 `_on_add_layer`（处理添加图层）方法

```python
        self._layers_panel.layer_remove_requested.connect(self._on_remove_layer)
```
#         将图层面板的 `layer_remove_requested`（请求删除图层）信号连接到 `_on_remove_layer`（处理删除图层）方法

```python
        self._layers_panel.layer_visibility_changed.connect(self._on_layer_visibility)
```
#         将图层面板的 `layer_visibility_changed`（图层可见性变更）信号连接到 `_on_layer_visibility`（处理图层可见性）方法

```python
        self._layers_panel.layer_locked_changed.connect(self._on_layer_locked)
```
#         将图层面板的 `layer_locked_changed`（图层锁定变更）信号连接到 `_on_layer_locked`（处理图层锁定）方法

```python
        self._layers_panel.layer_duplicate_requested.connect(self._on_duplicate_layer)
```
#         将图层面板的 `layer_duplicate_requested`（请求复制图层）信号连接到 `_on_duplicate_layer`（处理复制图层）方法

```python
        self._layers_panel.layer_rename_requested.connect(self._on_rename_layer)
```
#         将图层面板的 `layer_rename_requested`（请求重命名图层）信号连接到 `_on_rename_layer`（处理重命名图层）方法

```python
        self._layers_panel.layer_reorder_requested.connect(self._on_reorder_layer)
```
#         将图层面板的 `layer_reorder_requested`（请求重排图层）信号连接到 `_on_reorder_layer`（处理图层重排）方法

```python
        self._layers_panel.layer_merge_requested.connect(self._on_merge_layers)
```
#         将图层面板的 `layer_merge_requested`（请求合并图层）信号连接到 `_on_merge_layers`（处理合并图层）方法

```python
        self._layers_panel.layer_flatten_requested.connect(self._on_flatten)
```
#         将图层面板的 `layer_flatten_requested`（请求拼合图稿）信号连接到 `_on_flatten`（处理拼合图稿）方法

```python
        self._layers_panel.layer_collect_requested.connect(self._on_collect_layer)
```
#         将图层面板的 `layer_collect_requested`（请求收集到新图层）信号连接到 `_on_collect_layer`（处理收集到新图层）方法

```python
        self._layers_panel.layer_release_sequence_requested.connect(self._on_release_sequence)
```
#         将图层面板的 `layer_release_sequence_requested`（请求按顺序释放）信号连接到 `_on_release_sequence`（处理顺序释放）方法

```python
        self._layers_panel.layer_release_build_requested.connect(self._on_release_build)
```
#         将图层面板的 `layer_release_build_requested`（请求按构建释放）信号连接到 `_on_release_build`（处理构建释放）方法

```python
        # 新增信号（第十四章、第二十-二十五章）
```
#         注释：新增信号连接（第十四章、第二十至二十五章功能）

```python
        self._layers_panel.layer_select_all_requested.connect(self._on_select_all_in_layer)
```
#         将图层面板的 `layer_select_all_requested`（请求选择图层全部）信号连接到 `_on_select_all_in_layer`（处理选择图层全部对象）方法

```python
        self._layers_panel.layer_target_requested.connect(self._on_target_layer)
```
#         将图层面板的 `layer_target_requested`（请求设置目标图层）信号连接到 `_on_target_layer`（处理设置目标图层）方法

```python
        self._layers_panel.layer_color_changed.connect(self._on_layer_color)
```
#         将图层面板的 `layer_color_changed`（图层颜色变更）信号连接到 `_on_layer_color`（处理图层颜色变更）方法

```python
        self._layers_panel.layer_template_changed.connect(self._on_layer_template)
```
#         将图层面板的 `layer_template_changed`（图层模板模式变更）信号连接到 `_on_layer_template`（处理图层模板模式）方法

```python
        self._layers_panel.layer_printable_changed.connect(self._on_layer_printable)
```
#         将图层面板的 `layer_printable_changed`（图层可打印状态变更）信号连接到 `_on_layer_printable`（处理图层可打印状态）方法

```python
        self._layers_panel.layer_preview_mode_changed.connect(self._on_layer_preview_mode)
```
#         将图层面板的 `layer_preview_mode_changed`（图层预览模式变更）信号连接到 `_on_layer_preview_mode`（处理图层预览模式）方法

```python
        self._layers_panel.layer_opacity_changed.connect(self._on_layer_opacity)
```
#         将图层面板的 `layer_opacity_changed`（图层不透明度变更）信号连接到 `_on_layer_opacity`（处理图层不透明度）方法

```python
        self._layers_panel.item_order_changed.connect(self._on_item_order)
```
#         将图层面板的 `item_order_changed`（对象层级顺序变更）信号连接到 `_on_item_order`（处理对象层级调整）方法

```python
        self._layers_panel.item_move_to_layer.connect(self._on_move_item_to_layer)
```
#         将图层面板的 `item_move_to_layer`（对象移动到图层）信号连接到 `_on_move_item_to_layer`（处理移动对象到图层）方法

```python

```
#         空行

```python
        self._swatches_panel.color_selected.connect(self._on_swatch_selected)
```
#         将色板面板的 `color_selected`（颜色选中）信号连接到 `_on_swatch_selected`（处理色板选中）方法

```python

```
#         空行

```python
        self._chat_panel.poster_generated.connect(self._on_ai_poster_generated)
```
#         将 AI 聊天面板的 `poster_generated`（海报已生成）信号连接到 `_on_ai_poster_generated`（处理 AI 海报生成）方法

```python
        self._chat_panel.set_document(self._document)
```
#         将当前文档设置到 AI 聊天面板中

```python

```
#         空行

```python
        self._update_layers()
```
#         调用 `_update_layers`（更新图层列表）方法

```python
        self._swatches_panel.update_swatches(self._document.swatches)
```
#         调用色板面板的 `update_swatches`（更新色板列表）方法，传入文档的色板集合

```python

```
#     空行

```python
    # ── 事件处理 ──
```
#     分隔注释：── 事件处理 ──

```python

```
#     空行

```python
    def _on_selection_changed(self, items: list[GraphicItem]):
```
#     定义私有方法 `_on_selection_changed`（处理选中变更），接收自身引用和 `items`（选中的图形项列表）参数

```python
        try:
```
#         开始异常捕获：

```python
            self._properties_panel.update_selection(items)
```
#             调用属性面板的 `update_selection`（更新选中内容）方法，传入选中的图元列表

```python
            self._update_undo_state()
```
#             调用 `_update_undo_state`（更新撤销/重做状态）方法

```python
        except Exception as e:
```
#         捕获所有异常，赋值给 `e`（异常对象）：

```python
            logger.error(f"选择变更处理失败: {e}", exc_info=True)
```
#             通过日志记录器输出错误日志："选择变更处理失败"，附带异常堆栈信息

```python

```
#     空行

```python
    def _on_mouse_move(self, x: float, y: float):
```
#     定义私有方法 `_on_mouse_move`（处理鼠标移动），接收自身引用和 `x`（横坐标）、`y`（纵坐标）参数

```python
        self._pos_label.setText(f"X: {x:.1f}  Y: {y:.1f}")
```
#         更新位置标签文本，显示鼠标坐标，保留一位小数

```python

```
#     空行

```python
    def _on_tool_changed(self, tool_type: ToolType):
```
#     定义私有方法 `_on_tool_changed`（处理工具变更），接收自身引用和 `tool_type`（工具类型）参数

```python
        names = {
```
#         创建工具名称映射字典：

```python
            ToolType.SELECTION: "选择工具",
```
#             选择工具类型 → "选择工具"

```python
            ToolType.DIRECT_SELECT: "直接选择工具",
```
#             直接选择工具类型 → "直接选择工具"

```python
            ToolType.RECTANGLE: "矩形工具",
```
#             矩形工具类型 → "矩形工具"

```python
            ToolType.ELLIPSE: "椭圆工具",
```
#             椭圆工具类型 → "椭圆工具"

```python
            ToolType.PEN: "钢笔工具",
```
#             钢笔工具类型 → "钢笔工具"

```python
            ToolType.TEXT: "文字工具",
```
#             文字工具类型 → "文字工具"

```python
            ToolType.HAND: "抓手工具",
```
#             抓手工具类型 → "抓手工具"

```python
        }
```
#         工具名称映射字典结束

```python
        self._tool_label.setText(names.get(tool_type, "未知工具"))
```
#         更新工具标签文本，从映射字典中查找工具名称，找不到则显示 "未知工具"

```python
        self._tool_bar.set_current_tool(tool_type)
```
#         调用工具栏面板的 `set_current_tool`（设置当前工具）方法，同步高亮对应工具按钮

```python

```
#     空行

```python
    def _update_all(self):
```
#     定义私有方法 `_update_all`（更新全部界面状态），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            self._update_layers()
```
#             调用 `_update_layers`（更新图层列表）

```python
            self._update_undo_state()
```
#             调用 `_update_undo_state`（更新撤销/重做状态）

```python
            self._canvas.update()
```
#             调用画布的 `update`（重绘）方法

```python
            self._update_title()
```
#             调用 `_update_title`（更新窗口标题）方法

```python

```
#     空行

```python
    def _update_layers(self):
```
#     定义私有方法 `_update_layers`（更新图层列表），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            self._layers_panel.update_layers(
```
#             调用图层面板的 `update_layers`（更新图层显示）方法：

```python
                self._document.layers, self._document.active_layer_index,
```
#                 传入文档的所有图层列表和当前活动图层索引

```python
            )
```
#             方法调用结束

```python

```
#     空行

```python
    def _update_title(self):
```
#     定义私有方法 `_update_title`（更新窗口标题），接收自身引用参数

```python
        modified = "*" if self._document and self._document.modified else ""
```
#         判断文档是否已修改，若已修改则 `modified` 为 "*"，否则为空字符串

```python
        name = self._document.name if self._document else "未命名"
```
#         获取文档名称，若文档不存在则为 "未命名"

```python
        self.setWindowTitle(f"简易 Illustrator — {modified}{name}")
```
#         设置窗口标题，格式为 "简易 Illustrator — *文档名"（有修改标记时）

```python

```
#     空行

```python
    # ── 属性修改 ──
```
#     分隔注释：── 属性修改 ──

```python
    def _apply_to_selection(self, func):
```
#     定义私有方法 `_apply_to_selection`（对选中对象应用操作），接收自身引用和 `func`（操作函数）参数

```python
        try:
```
#         开始异常捕获：

```python
            if self._document:
```
#             如果文档存在：

```python
                for item in list(self._document.get_selection()):
```
#                 遍历文档中所有选中的图元（转换为列表副本以避免迭代中修改）：

```python
                    func(item)
```
#                     对每个图元执行 `func`（传入的操作函数）

```python
                self._document.modified = True
```
#                 将文档标记为已修改

```python
                self._canvas.update()
```
#                 重绘画布

```python
        except Exception as e:
```
#         捕获所有异常，赋值给 `e`：

```python
            logger.error(f"属性应用失败: {e}", exc_info=True)
```
#             通过日志记录器输出错误日志："属性应用失败"，附带异常堆栈信息

```python
    def _on_fill_color(self, color: QColor):
```
#     定义私有方法 `_on_fill_color`（处理填充色变更），接收自身引用和 `color`（颜色）参数

```python
        self._apply_to_selection(
```
#         调用 `_apply_to_selection`（对选中对象应用操作），传入以下匿名函数：

```python
            lambda item: setattr(item.style, 'fill_color',
```
#             对每个图元的样式属性设置填充色：

```python
                                 color if color.isValid() else None)
```
#                 如果颜色有效则使用该颜色，否则设为 None（无填充）

```python
        )
```
#         方法调用结束

```python
    def _on_stroke_color(self, color: QColor):
```
#     定义私有方法 `_on_stroke_color`（处理描边色变更），接收自身引用和 `color`（颜色）参数

```python
        self._apply_to_selection(
```
#         调用 `_apply_to_selection`，传入以下匿名函数：

```python
            lambda item: setattr(item.style, 'stroke_color',
```
#             对每个图元的样式属性设置描边色：

```python
                                 color if color.isValid() else None)
```
#                 如果颜色有效则使用该颜色，否则设为 None（无描边）

```python
        )
```
#         方法调用结束

```python
    def _on_stroke_width(self, width: float):
```
#     定义私有方法 `_on_stroke_width`（处理描边宽度变更），接收自身引用和 `width`（宽度值）参数

```python
        self._apply_to_selection(lambda item: setattr(item.style, 'stroke_width', width))
```
#         调用 `_apply_to_selection`，对每个图元设置描边宽度为 `width`

```python
    def _on_opacity(self, opacity: float):
```
#     定义私有方法 `_on_opacity`（处理不透明度变更），接收自身引用和 `opacity`（不透明度值）参数

```python
        self._apply_to_selection(lambda item: setattr(item, 'opacity', opacity))
```
#         调用 `_apply_to_selection`，对每个图元直接设置不透明度为 `opacity`

```python
    def _on_corner_radius(self, radius: float):
```
#     定义私有方法 `_on_corner_radius`（处理圆角半径变更），接收自身引用和 `radius`（圆角半径值）参数

```python
        self._apply_to_selection(
```
#         调用 `_apply_to_selection`，传入以下条件表达式：

```python
            lambda item: setattr(item, 'corner_radius', radius)
```
#             对图元设置圆角半径为 `radius`

```python
            if isinstance(item, RectangleItem) else None
```
#             仅当图元是 `矩形项` 实例时执行，否则返回 None

```python
        )
```
#         方法调用结束

```python
    def _on_text_changed(self, text: str):
```
#     定义私有方法 `_on_text_changed`（处理文本内容变更），接收自身引用和 `text`（新文本）参数

```python
        self._apply_to_selection(
```
#         调用 `_apply_to_selection`，传入以下条件表达式：

```python
            lambda item: setattr(item, 'contents', text)
```
#             对图元设置内容为 `text`

```python
            if isinstance(item, TextFrame) else None
```
#             仅当图元是 `文本框` 实例时执行，否则返回 None

```python
        )
```
#         方法调用结束

```python
    def _on_font_size(self, size: float):
```
#     定义私有方法 `_on_font_size`（处理字体大小变更），接收自身引用和 `size`（字体大小值）参数

```python
        self._apply_to_selection(
```
#         调用 `_apply_to_selection`，传入以下条件表达式：

```python
            lambda item: setattr(item.char_attrs, 'font_size', size)
```
#             对图元的字符属性设置字体大小为 `size`

```python
            if isinstance(item, TextFrame) else None
```
#             仅当图元是 `文本框` 实例时执行，否则返回 None

```python
        )
```
#         方法调用结束

```python
    def _on_font_family(self, family: str):
```
#     定义私有方法 `_on_font_family`（处理字体族变更），接收自身引用和 `family`（字体族名称）参数

```python
        self._apply_to_selection(
```
#         调用 `_apply_to_selection`，传入以下条件表达式：

```python
            lambda item: setattr(item.char_attrs, 'font_family', family)
```
#             对图元的字符属性设置字体族为 `family`

```python
            if isinstance(item, TextFrame) else None
```
#             仅当图元是 `文本框` 实例时执行，否则返回 None

```python
        )
```
#         方法调用结束

```python
    def _on_bold(self, bold: bool):
```
#     定义私有方法 `_on_bold`（处理粗体变更），接收自身引用和 `bold`（是否粗体，布尔值）参数

```python
        self._apply_to_selection(
```
#         调用 `_apply_to_selection`，传入以下条件表达式：

```python
            lambda item: setattr(item.char_attrs, 'bold', bold)
```
#             对图元的字符属性设置粗体为 `bold`

```python
            if isinstance(item, TextFrame) else None
```
#             仅当图元是 `文本框` 实例时执行，否则返回 None

```python
        )
```
#         方法调用结束

```python
    def _on_italic(self, italic: bool):
```
#     定义私有方法 `_on_italic`（处理斜体变更），接收自身引用和 `italic`（是否斜体，布尔值）参数

```python
        self._apply_to_selection(
```
#         调用 `_apply_to_selection`，传入以下条件表达式：

```python
            lambda item: setattr(item.char_attrs, 'italic', italic)
```
#             对图元的字符属性设置斜体为 `italic`

```python
            if isinstance(item, TextFrame) else None
```
#             仅当图元是 `文本框` 实例时执行，否则返回 None

```python
        )
```
#         方法调用结束

```python
    def _on_alignment(self, justification: Justification):
```
#     定义私有方法 `_on_alignment`（处理对齐方式变更），接收自身引用和 `justification`（对齐方式枚举值）参数

```python
        self._apply_to_selection(
```
#         调用 `_apply_to_selection`，传入以下条件表达式：

```python
            lambda item: setattr(item.para_attrs, 'justification', justification)
```
#             对图元的段落属性设置对齐方式为 `justification`

```python
            if isinstance(item, TextFrame) else None
```
#             仅当图元是 `文本框` 实例时执行，否则返回 None

```python
        )
```
#         方法调用结束

```python
    def _on_swatch_selected(self, color: QColor):
```
#     定义私有方法 `_on_swatch_selected`（处理色板选中），接收自身引用和 `color`（选中的颜色）参数

```python
        self._on_fill_color(color)
```
#         调用 `_on_fill_color`（处理填充色变更），将选中色板的颜色应用到选中对象的填充色

```python

```
#     空行

```python
    # ── 图层操作 ──
```
#     分隔注释：── 图层操作 ──

```python
    def _on_layer_selected(self, index: int):
```
#     定义私有方法 `_on_layer_selected`（处理图层选中），接收自身引用和 `index`（图层索引）参数

```python
        if self._document:
```
#         如果文档存在：

```python
            self._document.active_layer_index = index
```
#             将文档的活动图层索引设置为 `index`

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_add_layer(self):
```
#     定义私有方法 `_on_add_layer`（处理添加图层），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            self._document.add_layer()
```
#             调用文档的 `add_layer`（添加图层）方法

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_remove_layer(self, index: int):
```
#     定义私有方法 `_on_remove_layer`（处理删除图层），接收自身引用和 `index`（图层索引）参数

```python
        if self._document and len(self._document.layers) > 1:
```
#         如果文档存在且图层数量大于 1（至少保留一个图层）：

```python
            layer = self._document.layers[index]
```
#             根据索引获取目标图层对象

```python
            self._document.remove_layer(layer)
```
#             调用文档的 `remove_layer`（删除图层）方法，删除该图层

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_layer_visibility(self, index: int, visible: bool):
```
#     定义私有方法 `_on_layer_visibility`（处理图层可见性切换），接收自身引用、`index`（图层索引）和 `visible`（是否可见）参数

```python
        """切换图层可见性（PDF 八）"""
```
#         文档字符串：切换图层可见性（PDF 第八节）

```python
        if self._document and 0 <= index < len(self._document.layers):
```
#         如果文档存在且索引在有效范围内：

```python
            self._document.layers[index].visible = visible
```
#             将该图层的可见性设置为 `visible`

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_layer_locked(self, index: int, locked: bool):
```
#     定义私有方法 `_on_layer_locked`（处理图层锁定切换），接收自身引用、`index`（图层索引）和 `locked`（是否锁定）参数

```python
        """切换图层锁定（PDF 九）"""
```
#         文档字符串：切换图层锁定（PDF 第九节）

```python
        if self._document and 0 <= index < len(self._document.layers):
```
#         如果文档存在且索引在有效范围内：

```python
            self._document.layers[index].locked = locked
```
#             将该图层的锁定状态设置为 `locked`

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_duplicate_layer(self, index: int):
```
#     定义私有方法 `_on_duplicate_layer`（处理复制图层），接收自身引用和 `index`（图层索引）参数

```python
        """复制图层（PDF 五）"""
```
#         文档字符串：复制图层（PDF 第五节）

```python
        if self._document and 0 <= index < len(self._document.layers):
```
#         如果文档存在且索引在有效范围内：

```python
            self._document.duplicate_layer(self._document.layers[index])
```
#             调用文档的 `duplicate_layer`（复制图层）方法，复制指定图层

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_rename_layer(self, index: int, new_name: str):
```
#     定义私有方法 `_on_rename_layer`（处理重命名图层），接收自身引用、`index`（图层索引）和 `new_name`（新名称）参数

```python
        """重命名图层（PDF 六）"""
```
#         文档字符串：重命名图层（PDF 第六节）

```python
        if self._document:
```
#         如果文档存在：

```python
            if new_name:
```
#             如果新名称不为空：

```python
                if index >= 0 and index < len(self._document.layers):
```
#                 如果索引在有效范围内：

```python
                    self._document.layers[index].name = new_name
```
#                     将该图层的名称设置为 `new_name`

```python
                    self._document.modified = True
```
#                     标记文档为已修改

```python
            # 空名称表示需要启动重命名（已在面板中处理）
```
#             注释：空名称表示需要启动重命名编辑（已在面板中处理）

```python
            self._update_layers()
```
#             更新图层列表显示

```python
    def _on_reorder_layer(self, from_index: int, to_index: int):
```
#     定义私有方法 `_on_reorder_layer`（处理图层重排），接收自身引用、`from_index`（源索引）和 `to_index`（目标索引）参数

```python
        """调整图层顺序（PDF 十）"""
```
#         文档字符串：调整图层顺序（PDF 第十节）

```python
        if self._document and 0 <= from_index < len(self._document.layers):
```
#         如果文档存在且源索引在有效范围内：

```python
            layer = self._document.layers[from_index]
```
#             获取源索引处的图层对象

```python
            self._document.reorder_layer(layer, to_index)
```
#             调用文档的 `reorder_layer`（重排图层）方法，将该图层移动到目标位置

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_merge_layers(self, indices: list[int]):
```
#     定义私有方法 `_on_merge_layers`（处理合并图层），接收自身引用和 `indices`（图层索引列表）参数

```python
        """合并选定图层（PDF 十八）"""
```
#         文档字符串：合并选定图层（PDF 第十八节）

```python
        if self._document:
```
#         如果文档存在：

```python
            layers = [self._document.layers[i] for i in indices if 0 <= i < len(self._document.layers)]
```
#             根据索引列表获取有效的图层对象列表（过滤无效索引）

```python
            if len(layers) >= 2:
```
#             如果有效图层数量大于等于 2（至少两个图层才能合并）：

```python
                self._document.merge_layers(layers)
```
#                 调用文档的 `merge_layers`（合并图层）方法

```python
                self._update_layers()
```
#                 更新图层列表显示

```python
                self._canvas.update()
```
#                 重绘画布

```python
    def _on_flatten(self):
```
#     定义私有方法 `_on_flatten`（处理拼合图稿），接收自身引用参数

```python
        """拼合图稿（PDF 十九）"""
```
#         文档字符串：拼合图稿（PDF 第十九节）

```python
        if self._document:
```
#         如果文档存在：

```python
            self._document.flatten_artwork()
```
#             调用文档的 `flatten_artwork`（拼合图稿）方法，将所有图层合并为一个

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_collect_layer(self):
```
#     定义私有方法 `_on_collect_layer`（处理收集到新图层），接收自身引用参数

```python
        """收集到新图层（PDF 十六）"""
```
#         文档字符串：收集到新图层（PDF 第十六节）

```python
        if self._document:
```
#         如果文档存在：

```python
            sel = self._document.get_selection()
```
#             获取当前选中的所有图元，赋值给 `sel`

```python
            if sel:
```
#             如果有选中的图元：

```python
                self._document.collect_in_new_layer(sel)
```
#                 调用文档的 `collect_in_new_layer`（收集到新图层）方法

```python
                self._update_layers()
```
#                 更新图层列表显示

```python
                self._canvas.update()
```
#                 重绘画布

```python
    def _on_release_sequence(self):
```
#     定义私有方法 `_on_release_sequence`（处理按顺序释放到图层），接收自身引用参数

```python
        """释放到图层 - 顺序模式（PDF 十七）"""
```
#         文档字符串：释放到图层 - 顺序模式（PDF 第十七节）

```python
        if self._document:
```
#         如果文档存在：

```python
            sel = self._document.get_selection()
```
#             获取当前选中的所有图元

```python
            for item in sel:
```
#             遍历选中的图元：

```python
                if isinstance(item, GroupItem):
```
#                 如果图元是 `编组项` 实例：

```python
                    self._document.release_to_layers_sequence(item)
```
#                     调用文档的 `release_to_layers_sequence`（按顺序释放到图层）方法

```python
                    self._update_layers()
```
#                     更新图层列表显示

```python
                    self._canvas.update()
```
#                     重绘画布

```python
                    return
```
#                     处理完毕后立即返回（只处理第一个编组）

```python
    def _on_release_build(self):
```
#     定义私有方法 `_on_release_build`（处理按构建释放到图层），接收自身引用参数

```python
        """释放到图层 - 构建模式（PDF 十七）"""
```
#         文档字符串：释放到图层 - 构建模式（PDF 第十七节）

```python
        if self._document:
```
#         如果文档存在：

```python
            sel = self._document.get_selection()
```
#             获取当前选中的所有图元

```python
            for item in sel:
```
#             遍历选中的图元：

```python
                if isinstance(item, GroupItem):
```
#                 如果图元是 `编组项` 实例：

```python
                    self._document.release_to_layers_build(item)
```
#                     调用文档的 `release_to_layers_build`（按构建释放到图层）方法

```python
                    self._update_layers()
```
#                     更新图层列表显示

```python
                    self._canvas.update()
```
#                     重绘画布

```python
                    return
```
#                     处理完毕后立即返回

```python
    def _on_select_all_in_layer(self, index: int):
```
#     定义私有方法 `_on_select_all_in_layer`（处理选择图层全部对象），接收自身引用和 `index`（图层索引）参数

```python
        """选择整个图层的所有对象（第十四章）
```
#         文档字符串第一行：选择整个图层的所有对象（第十四章功能）

```python
        对照 Ai 行为：点击图层右侧目标区域，一次性选中图层全部对象
```
#         对照 Adobe Illustrator 行为：点击图层右侧目标区域，一次性选中图层的全部对象

```python
        包括子图层中的对象
```
#         包括子图层中的对象

```python
        """
```
#         文档字符串结束

```python
        if self._document and 0 <= index < len(self._document.layers):
```
#         如果文档存在且索引在有效范围内：

```python
            self._document.clear_selection()
```
#             调用文档的 `clear_selection`（清除选中）方法，先清空当前选中

```python
            layer = self._document.layers[index]
```
#             获取目标图层对象

```python
            # 使用 all_items_recursive 获取所有嵌套对象
```
#             注释：使用 `all_items_recursive`（递归获取所有项）属性来获取所有嵌套对象

```python
            for item in layer.all_items_recursive:
```
#             遍历图层中递归获取的所有图元：

```python
                if not item.locked:
```
#                 如果图元未被锁定：

```python
                    item.selected = True
```
#                     将该图元设为选中状态

```python
            self._document.active_layer_index = index
```
#             将该图层设为活动图层

```python
            self._canvas.update()
```
#             重绘画布

```python
            self._status_bar.showMessage(f"已选择图层「{layer.name}」的全部对象", 2000)
```
#             在状态栏显示临时消息 "已选择图层「图层名」的全部对象"，持续 2000 毫秒

```python
    def _on_target_layer(self, index: int):
```
#     定义私有方法 `_on_target_layer`（处理设置目标图层），接收自身引用和 `index`（图层索引）参数

```python
        """设置目标图层（第二十四章 — Target）"""
```
#         文档字符串：设置目标图层（第二十四章 — 目标功能）

```python
        if self._document and 0 <= index < len(self._document.layers):
```
#         如果文档存在且索引在有效范围内：

```python
            self._document.active_layer_index = index
```
#             将该图层设为活动图层（即目标图层）

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            layer = self._document.layers[index]
```
#             获取目标图层对象

```python
            self._status_bar.showMessage(f"目标图层: {layer.name}（效果将应用于此图层）", 2000)
```
#             在状态栏显示临时消息 "目标图层: 图层名（效果将应用于此图层）"，持续 2000 毫秒

```python
    def _on_layer_color(self, index: int, color: QColor):
```
#     定义私有方法 `_on_layer_color`（处理图层颜色变更），接收自身引用、`index`（图层索引）和 `color`（颜色）参数

```python
        """图层颜色变更（第二十章）"""
```
#         文档字符串：图层颜色变更（第二十章功能）

```python
        if self._document and 0 <= index < len(self._document.layers):
```
#         如果文档存在且索引在有效范围内：

```python
            self._document.layers[index].color = color
```
#             将该图层的标识颜色设置为 `color`

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_layer_template(self, index: int, is_template: bool):
```
#     定义私有方法 `_on_layer_template`（处理图层模板模式变更），接收自身引用、`index`（图层索引）和 `is_template`（是否为模板）参数

```python
        """模板模式变更（第十九章）"""
```
#         文档字符串：模板模式变更（第十九章功能）

```python
        if self._document and 0 <= index < len(self._document.layers):
```
#         如果文档存在且索引在有效范围内：

```python
            self._document.layers[index].is_template = is_template
```
#             将该图层的模板模式设置为 `is_template`

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_layer_printable(self, index: int, printable: bool):
```
#     定义私有方法 `_on_layer_printable`（处理图层可打印状态变更），接收自身引用、`index`（图层索引）和 `printable`（是否可打印）参数

```python
        """打印状态变更（第二十一章）"""
```
#         文档字符串：打印状态变更（第二十一章功能）

```python
        if self._document and 0 <= index < len(self._document.layers):
```
#         如果文档存在且索引在有效范围内：

```python
            self._document.layers[index].printable = printable
```
#             将该图层的可打印状态设置为 `printable`

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_layer_preview_mode(self, index: int, mode: str):
```
#     定义私有方法 `_on_layer_preview_mode`（处理图层预览模式变更），接收自身引用、`index`（图层索引）和 `mode`（预览模式名称）参数

```python
        """预览模式变更（第二十二章）"""
```
#         文档字符串：预览模式变更（第二十二章功能）

```python
        if self._document and 0 <= index < len(self._document.layers):
```
#         如果文档存在且索引在有效范围内：

```python
            self._document.layers[index].preview_mode = mode
```
#             将该图层的预览模式设置为 `mode`

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_layer_opacity(self, index: int, opacity: float):
```
#     定义私有方法 `_on_layer_opacity`（处理图层不透明度变更），接收自身引用、`index`（图层索引）和 `opacity`（不透明度值）参数

```python
        """图层不透明度变更（第二十五章 — 图层级透明度效果）"""
```
#         文档字符串：图层不透明度变更（第二十五章 — 图层级透明度效果）

```python
        if self._document and 0 <= index < len(self._document.layers):
```
#         如果文档存在且索引在有效范围内：

```python
            self._document.layers[index].opacity = opacity
```
#             将该图层的不透明度设置为 `opacity`

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_item_order(self, layer_index: int, from_pos: int, to_pos: int):
```
#     定义私有方法 `_on_item_order`（处理对象层级顺序变更），接收自身引用、`layer_index`（图层索引）、`from_pos`（原始位置）和 `to_pos`（目标位置）参数

```python
        """对象层级管理 - 拖动调整对象前后顺序（第十二章）"""
```
#         文档字符串：对象层级管理 - 拖动调整对象前后顺序（第十二章功能）

```python
        if self._document and 0 <= layer_index < len(self._document.layers):
```
#         如果文档存在且图层索引在有效范围内：

```python
            layer = self._document.layers[layer_index]
```
#             获取目标图层对象

```python
            if 0 <= from_pos < len(layer.items) and 0 <= to_pos < len(layer.items):
```
#             如果原始位置和目标位置都在图层对象列表的有效范围内：

```python
                item = layer.items.pop(from_pos)
```
#                 从原始位置弹出（移除）该对象

```python
                layer.items.insert(to_pos, item)
```
#                 将该对象插入到目标位置

```python
                self._document.modified = True
```
#                 标记文档为已修改

```python
                self._update_layers()
```
#                 更新图层列表显示

```python
                self._canvas.update()
```
#                 重绘画布

```python
    def _on_move_item_to_layer(self, target_index: int):
```
#     定义私有方法 `_on_move_item_to_layer`（处理移动对象到其他图层），接收自身引用和 `target_index`（目标图层索引）参数

```python
        """移动选中对象到其他图层（第十三章 — 拖动彩色方块）"""
```
#         文档字符串：移动选中对象到其他图层（第十三章功能 — 拖动彩色方块到目标图层）

```python
        if self._document and 0 <= target_index < len(self._document.layers):
```
#         如果文档存在且目标图层索引在有效范围内：

```python
            sel = self._document.get_selection()
```
#             获取当前选中的所有图元

```python
            target_layer = self._document.layers[target_index]
```
#             获取目标图层对象

```python
            for item in sel:
```
#             遍历选中的图元：

```python
                # 从原图层移除
```
#                 注释：从原图层移除

```python
                for layer in self._document.layers:
```
#                 遍历文档中的所有图层：

```python
                    if item in layer.items:
```
#                     如果该图元在当前图层的对象列表中：

```python
                        layer.remove_item(item)
```
#                         从当前图层中移除该图元

```python
                        break
```
#                         跳出内层循环（已找到并移除）

```python
                # 添加到目标图层
```
#                 注释：添加到目标图层

```python
                target_layer.add_item(item)
```
#                 将该图元添加到目标图层

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._update_layers()
```
#             更新图层列表显示

```python
            self._canvas.update()
```
#             重绘画布

```python
            self._status_bar.showMessage(
```
#             在状态栏显示临时消息：

```python
                f"已将 {len(sel)} 个对象移动到图层「{target_layer.name}」", 2000
```
#                 "已将 N 个对象移动到图层「图层名」"，持续 2000 毫秒

```python
            )
```
#             消息显示调用结束

```python

```
#     空行

```python
    # ── 排列操作 ──
```
#     分隔注释：── 排列操作 ──

```python
    def _on_bring_front(self):
```
#     定义私有方法 `_on_bring_front`（处理置于顶层），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            for item in self._document.get_selection():
```
#             遍历选中的图元：

```python
                (item._layer or self._document.active_layer).bring_to_front(item)
```
#                 获取图元所属图层（若为 None 则使用活动图层），调用其 `bring_to_front`（置于顶层）方法

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_send_to_back(self):
```
#     定义私有方法 `_on_send_to_back`（处理置于底层），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            for item in self._document.get_selection():
```
#             遍历选中的图元：

```python
                (item._layer or self._document.active_layer).send_to_back(item)
```
#                 获取图元所属图层，调用其 `send_to_back`（置于底层）方法

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_bring_forward(self):
```
#     定义私有方法 `_on_bring_forward`（处理上移一层），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            for item in self._document.get_selection():
```
#             遍历选中的图元：

```python
                (item._layer or self._document.active_layer).bring_forward(item)
```
#                 获取图元所属图层，调用其 `bring_forward`（上移一层）方法

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_send_backward(self):
```
#     定义私有方法 `_on_send_backward`（处理下移一层），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            for item in self._document.get_selection():
```
#             遍历选中的图元：

```python
                (item._layer or self._document.active_layer).send_backward(item)
```
#                 获取图元所属图层，调用其 `send_backward`（下移一层）方法

```python
            self._document.modified = True
```
#             标记文档为已修改

```python
            self._canvas.update()
```
#             重绘画布

```python

```
#     空行

```python
    # ── 编辑操作 ──
```
#     分隔注释：── 编辑操作 ──

```python
    def _on_delete(self):
```
#     定义私有方法 `_on_delete`（处理删除操作），接收自身引用参数

```python
        try:
```
#         开始异常捕获：

```python
            if self._document:
```
#             如果文档存在：

```python
                for item in list(self._document.get_selection()):
```
#                 遍历选中的图元（转为列表副本以避免迭代中修改）：

```python
                    self._document.remove_item(item)
```
#                     调用文档的 `remove_item`（移除图元）方法删除该图元

```python
                self._properties_panel.update_selection([])
```
#                 更新属性面板的选中内容为空列表

```python
                self._canvas.update()
```
#                 重绘画布

```python
                self._update_title()
```
#                 更新窗口标题

```python
        except Exception as e:
```
#         捕获所有异常，赋值给 `e`：

```python
            logger.error(f"删除操作失败: {e}", exc_info=True)
```
#             通过日志记录器输出错误日志："删除操作失败"，附带异常堆栈信息

```python
    def _on_select_all(self):
```
#     定义私有方法 `_on_select_all`（处理全选操作），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            self._document.select_all()
```
#             调用文档的 `select_all`（全选）方法，选中所有图元

```python
            self._properties_panel.update_selection(self._document.get_selection())
```
#             更新属性面板的选中内容为所有选中的图元

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_group(self):
```
#     定义私有方法 `_on_group`（处理编组操作），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            group = self._document.group_selection()
```
#             调用文档的 `group_selection`（编组选中）方法，将选中图元编组，返回编组对象

```python
            if group:
```
#             如果编组成功（返回了编组对象）：

```python
                self._properties_panel.update_selection([group])
```
#                 更新属性面板的选中内容为该编组对象

```python
                self._canvas.update()
```
#                 重绘画布

```python
                self._update_title()
```
#                 更新窗口标题

```python
    def _on_ungroup(self):
```
#     定义私有方法 `_on_ungroup`（处理取消编组操作），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            for item in list(self._document.get_selection()):
```
#             遍历选中的图元（转为列表副本）：

```python
                self._document.ungroup(item)
```
#                 调用文档的 `ungroup`（取消编组）方法，取消该图元的编组

```python
            self._properties_panel.update_selection([])
```
#             更新属性面板的选中内容为空列表

```python
            self._canvas.update()
```
#             重绘画布

```python
            self._update_title()
```
#             更新窗口标题

```python

```
#     空行

```python
    # ── 撤销/重做 ──
```
#     分隔注释：── 撤销/重做 ──

```python
    def _on_undo(self):
```
#     定义私有方法 `_on_undo`（处理撤销操作），接收自身引用参数

```python
        if self._document and self._document.undo():
```
#         如果文档存在且撤销操作成功（`undo` 返回 True）：

```python
            self._update_undo_state()
```
#             更新撤销/重做按钮状态

```python
            self._update_all()
```
#             更新全部界面状态

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _on_redo(self):
```
#     定义私有方法 `_on_redo`（处理重做操作），接收自身引用参数

```python
        if self._document and self._document.redo():
```
#         如果文档存在且重做操作成功（`redo` 返回 True）：

```python
            self._update_undo_state()
```
#             更新撤销/重做按钮状态

```python
            self._update_all()
```
#             更新全部界面状态

```python
            self._canvas.update()
```
#             重绘画布

```python
    def _update_undo_state(self):
```
#     定义私有方法 `_update_undo_state`（更新撤销/重做按钮状态），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            self._undo_action.setEnabled(self._document.can_undo)
```
#             根据文档是否可以撤销，启用或禁用撤销按钮

```python
            self._redo_action.setEnabled(self._document.can_redo)
```
#             根据文档是否可以重做，启用或禁用重做按钮

```python
            if self._document.can_undo:
```
#             如果可以撤销：

```python
                self._undo_action.setText(f"撤销 {self._document.history.undo_description}")
```
#                 设置撤销按钮文本为 "撤销 操作描述"

```python
            else:
```
#             否则：

```python
                self._undo_action.setText("撤销(&U)")
```
#                 恢复撤销按钮默认文本为 "撤销(&U)"

```python
            if self._document.can_redo:
```
#             如果可以重做：

```python
                self._redo_action.setText(f"重做 {self._document.history.redo_description}")
```
#                 设置重做按钮文本为 "重做 操作描述"

```python
            else:
```
#             否则：

```python
                self._redo_action.setText("重做(&R)")
```
#                 恢复重做按钮默认文本为 "重做(&R)"

```python

```
#     空行

```python
    # ── 复制/粘贴 ──
```
#     分隔注释：── 复制/粘贴 ──

```python
    def _on_copy(self):
```
#     定义私有方法 `_on_copy`（处理复制操作），接收自身引用参数

```python
        if self._document:
```
#         如果文档存在：

```python
            sel = self._document.get_selection()
```
#             获取当前选中的所有图元

```python
            if sel:
```
#             如果有选中的图元：

```python
                self._clipboard = [
```
#                 更新剪贴板内容为以下列表：

```python
                    GraphicItem.from_dict(item.to_dict()) for item in sel
```
#                     对每个选中图元，先序列化为字典再反序列化，生成深拷贝副本

```python
                ]
```
#                 列表推导式结束

```python
                self._status_bar.showMessage(f"已复制 {len(sel)} 个对象", 2000)
```
#                 在状态栏显示临时消息 "已复制 N 个对象"，持续 2000 毫秒

```python
    def _on_paste(self):
```
#     定义私有方法 `_on_paste`（处理粘贴操作），接收自身引用参数

```python
        if not self._clipboard or not self._document:
```
#         如果剪贴板为空或文档不存在：

```python
            return
```
#             直接返回，不执行粘贴

```python
        self._document.clear_selection()
```
#         清除文档中的当前选中

```python
        for item in self._clipboard:
```
#         遍历剪贴板中的每个图元：

```python
            data = item.to_dict()
```
#             将图元序列化为字典

```python
            cloned = GraphicItem.from_dict(data)
```
#             从字典反序列化创建图元的克隆副本

```python
            cloned.move_by(20, 20)
```
#             将克隆图元向右下方偏移 20 像素（避免与原图元完全重叠）

```python
            cloned.selected = True
```
#             将克隆图元设为选中状态

```python
            self._document.add_item(cloned)
```
#             将克隆图元添加到文档中

```python
        self._update_all()
```
#         更新全部界面状态

```python
        self._canvas.update()
```
#         重绘画布

```python
        self._status_bar.showMessage(f"已粘贴 {len(self._clipboard)} 个对象", 2000)
```
#         在状态栏显示临时消息 "已粘贴 N 个对象"，持续 2000 毫秒

```python

```
#     空行

```python
    # ── 对齐 ──
```
#     分隔注释：── 对齐 ──

```python
    def _on_align(self, mode: str):
```
#     定义私有方法 `_on_align`（处理对齐操作），接收自身引用和 `mode`（对齐模式字符串）参数

```python
        sel = self._document.get_selection() if self._document else []
```
#         获取文档的选中图元列表，若文档不存在则为空列表

```python
        if len(sel) < 2:
```
#         如果选中图元少于 2 个：

```python
            return
```
#             直接返回（至少需要两个对象才能对齐）

```python
        all_rects = [item.bounding_rect() for item in sel]
```
#         获取所有选中图元的边界矩形列表

```python
        total_rect = all_rects[0]
```
#         取第一个边界矩形作为总包围矩形的初始值

```python
        for r in all_rects[1:]:
```
#         遍历剩余的边界矩形：

```python
            total_rect = total_rect.united(r)
```
#             逐一合并，计算所有图元的总包围矩形

```python
        for item in sel:
```
#         遍历选中的图元：

```python
            rect = item.bounding_rect()
```
#             获取该图元的边界矩形

```python
            match mode:
```
#             使用模式匹配根据 `mode` 执行不同对齐操作：

```python
                case "left":
```
#                 匹配到 "left"（左对齐）：

```python
                    item.move_by(total_rect.left() - rect.left(), 0)
```
#                     水平移动图元使其左边缘与总包围矩形的左边缘对齐

```python
                case "center_h":
```
#                 匹配到 "center_h"（水平居中）：

```python
                    item.move_by(total_rect.center().x() - rect.center().x(), 0)
```
#                     水平移动图元使其水平中心与总包围矩形的水平中心对齐

```python
                case "right":
```
#                 匹配到 "right"（右对齐）：

```python
                    item.move_by(total_rect.right() - rect.right(), 0)
```
#                     水平移动图元使其右边缘与总包围矩形的右边缘对齐

```python
                case "top":
```
#                 匹配到 "top"（顶部对齐）：

```python
                    item.move_by(0, total_rect.top() - rect.top())
```
#                     垂直移动图元使其顶边缘与总包围矩形的顶边缘对齐

```python
                case "center_v":
```
#                 匹配到 "center_v"（垂直居中）：

```python
                    item.move_by(0, total_rect.center().y() - rect.center().y())
```
#                     垂直移动图元使其垂直中心与总包围矩形的垂直中心对齐

```python
                case "bottom":
```
#                 匹配到 "bottom"（底部对齐）：

```python
                    item.move_by(0, total_rect.bottom() - rect.bottom())
```
#                     垂直移动图元使其底边缘与总包围矩形的底边缘对齐

```python
        self._document.modified = True
```
#         标记文档为已修改

```python
        self._canvas.update()
```
#         重绘画布


```python
        # 获取文档对象
        doc = self._document
        # 画布宽度
        canvas_w = doc.width
        # 画布高度
        canvas_h = doc.height
        # 画布矩形范围：左上角坐标(0,0)，右下角坐标(画布宽,画布高)
        canvas_rect = QRectF(0, 0, canvas_w, canvas_h)

        # 遍历所有图元项
        for item in items:
            # 获取当前图元的外接矩形
            rect = item.bounding_rect()
            # 根据对齐方向分支处理
            match direction:
                # 左对齐
                case "left":
                    item.move_by(canvas_rect.left() - rect.left(), 0)
                # 水平居中对齐
                case "center_h":
                    item.move_by(canvas_rect.center().x() - rect.center().x(), 0)
                # 右对齐
                case "right":
                    item.move_by(canvas_rect.right() - rect.right(), 0)
                # 顶部对齐
                case "top":
                    item.move_by(0, canvas_rect.top() - rect.top())
                # 垂直居中对齐
                case "center_v":
                    item.move_by(0, canvas_rect.center().y() - rect.center().y())
                # 底部对齐
                case "bottom":
                    item.move_by(0, canvas_rect.bottom() - rect.bottom())

        # 标记文档已修改
        self._document.modified = True
        # 刷新更新画布
        self._canvas.update()
```


```
        全部矩形 = [项目.获取包围矩形() for 项目 in 项目列表]
        总包围矩形 = 全部矩形[0]
        for 单个矩形 in 全部矩形[1:]:
            总包围矩形 = 总包围矩形.合并(单个矩形)

        for 项目 in 项目列表:
            单个矩形 = 项目.获取包围矩形()
            match 对齐方向:
                case "left":
                    项目.偏移移动(总包围矩形.左边界() - 单个矩形.左边界(), 0)
                case "center_h":
                    项目.偏移移动(总包围矩形.中心点().横坐标() - 单个矩形.中心点().横坐标(), 0)
                case "right":
                    项目.偏移移动(总包围矩形.右边界() - 单个矩形.右边界(), 0)
                case "top":
                    项目.偏移移动(0, 总包围矩形.上边界() - 单个矩形.上边界())
                case "center_v":
                    项目.偏移移动(0, 总包围矩形.中心点().纵坐标() - 单个矩形.中心点().纵坐标())
                case "bottom":
                    项目.偏移移动(0, 总包围矩形.下边界() - 单个矩形.下边界())

        self._文档.已修改 = True
        self._画布.刷新()
```


```python

```
#     空行

```python
    # ── 路径查找器（布尔运算） ──
```
#     分隔注释：── 路径查找器（布尔运算） ──

```python
    def _on_pathfinder(self, mode: str):
```
#     定义私有方法 `_on_pathfinder`（处理路径查找器布尔运算），接收自身引用和 `mode`（运算模式字符串）参数

```python
        if not self._document:
```
#         如果文档不存在：

```python
            return
```
#             直接返回

```python
        sel = self._document.get_selection()
```
#         获取当前选中的所有图元

```python
        if len(sel) < 2:
```
#         如果选中图元少于 2 个：

```python
            self._status_bar.showMessage("请至少选择2个对象进行布尔运算", 3000)
```
#             在状态栏显示提示消息 "请至少选择2个对象进行布尔运算"，持续 3000 毫秒

```python
            return
```
#             直接返回

```python
        paths: list[QPainterPath] = []
```
#         声明绘图路径列表 `paths`，初始为空列表

```python
        for item in sel:
```
#         遍历选中的图元：

```python
            if hasattr(item, 'painter_path'):
```
#             如果图元具有 `painter_path`（绘图路径）属性/方法：

```python
                p = item.painter_path()
```
#                 获取该图元的绘图路径

```python
                if item._transform and not item._transform.isIdentity():
```
#                 如果图元有变换矩阵且不是单位矩阵（有实际变换）：

```python
                    p = item._transform.map(p)
```
#                     对绘图路径应用变换矩阵

```python
                paths.append(p)
```
#                 将变换后的路径添加到路径列表中

```python
        if len(paths) < 2:
```
#         如果有效路径少于 2 个：

```python
            return
```
#             直接返回（无法进行布尔运算）

```python
        result_path = QPainterPath(paths[0])
```
#         以第一个路径为基准，创建结果路径对象

```python
        match mode:
```
#         使用模式匹配根据 `mode` 执行不同布尔运算：

```python
            case "union":
```
#             匹配到 "union"（联集/并集）：

```python
                for p in paths[1:]:
```
#                 遍历后续所有路径：

```python
                    result_path = result_path.united(p)
```
#                     将结果路径与当前路径取并集（合并）

```python
            case "intersect":
```
#             匹配到 "intersect"（交集）：

```python
                for p in paths[1:]:
```
#                 遍历后续所有路径：

```python
                    result_path = result_path.intersected(p)
```
#                     将结果路径与当前路径取交集

```python
            case "subtract":
```
#             匹配到 "subtract"（减去顶层/差集）：

```python
                for p in paths[1:]:
```
#                 遍历后续所有路径：

```python
                    result_path = result_path.subtracted(p)
```
#                     从结果路径中减去当前路径

```python
        result_item = PathItem()
```
#         创建 `路径项` 实例，作为布尔运算的结果对象

```python
        result_item._path = result_path
```
#         将运算结果路径赋值给结果对象的 `_path` 属性

```python
        result_item.style = sel[0].style.copy()
```
#         复制第一个选中图元的样式，赋值给结果对象

```python
        result_item.selected = True
```
#         将结果对象设为选中状态

```python
        for item in sel:
```
#         遍历所有参与运算的原始图元：

```python
            self._document.remove_item(item)
```
#             从文档中移除该图元

```python
        self._document.add_item(result_item)
```
#         将结果对象添加到文档中

```python
        self._update_all()
```
#         更新全部界面状态

```python
        self._canvas.update()
```
#         重绘画布

```python
        self._status_bar.showMessage(f"布尔运算({mode})完成", 2000)
```
#         在状态栏显示临时消息 "布尔运算(模式)完成"，持续 2000 毫秒

```python

```
#     空行

```python
    # ── AI 海报生成 ──
```
#     分隔注释：── AI 海报生成 ──

```python
    def _on_ai_poster_generated(self, params: dict):
```
#     定义私有方法 `_on_ai_poster_generated`（处理 AI 海报生成完成），接收自身引用和 `params`（生成参数字典）参数

```python
        if not self._document:
```
#         如果文档不存在：

```python
            return
```
#             直接返回

```python
        from ..ai.deepseek_client import POSTER_TEMPLATES
```
#         从 AI 包的 DeepSeek 客户端模块导入 `POSTER_TEMPLATES`（海报模板字典）

```python
        template = params.get("template", "social_media")
```
#         从参数字典中获取 "template"（模板类型）键，默认为 "social_media"（社交媒体）

```python
        tmpl = POSTER_TEMPLATES.get(template)
```
#         从海报模板字典中查找对应的模板配置

```python
        if tmpl:
```
#         如果找到模板配置：

```python
            self._document.width = tmpl["width"]
```
#             根据模板设置文档宽度

```python
            self._document.height = tmpl["height"]
```
#             根据模板设置文档高度

```python
        self._update_all()
```
#         更新全部界面状态

```python
        self._update_layers()
```
#         更新图层列表显示

```python
        self._swatches_panel.update_swatches(self._document.swatches)
```
#         更新色板面板中的色板列表

```python
        self._canvas.zoom_to_fit()
```
#         调用画布的 `zoom_to_fit`（适合窗口）方法，自动调整缩放以适应新尺寸

```python
        title = params.get("title", "新海报")
```
#         从参数字典中获取 "title"（标题）键，默认为 "新海报"

```python
        self._status_bar.showMessage(f"AI 已生成海报: {title}", 5000)
```
#         在状态栏显示临时消息 "AI 已生成海报: 标题"，持续 5000 毫秒

```python

```
#     空行

```python
    # ── 文件操作 ──
```
#     分隔注释：── 文件操作 ──

```python
    def _on_new(self):
```
#     定义私有方法 `_on_new`（处理新建文档操作），接收自身引用参数

```python
        if self._document and self._document.modified:
```
#         如果文档存在且已修改（有未保存的更改）：

```python
            ret = QMessageBox.question(
```
#             弹出确认对话框，询问用户操作：

```python
                self, "未保存的更改",
```
#                 父窗口为 `self`，标题 "未保存的更改"

```python
                "是否保存当前文档的更改？",
```
#                 消息内容 "是否保存当前文档的更改？"

```python
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
```
#                 提供 "保存"、"放弃"、"取消" 三个按钮

```python
            )
```
#             对话框调用结束，返回值赋值给 `ret`

```python
            match ret:
```
#             使用模式匹配根据用户选择执行不同操作：

```python
                case QMessageBox.Save:
```
#                 用户选择 "保存"：

```python
                    if self._document.file_path:
```
#                     如果文档已有文件路径（之前保存过）：

```python
                        self._document.save(self._document.file_path)
```
#                         直接保存到原文件路径

```python
                    else:
```
#                     否则（尚未保存过）：

```python
                        file_path, _ = QFileDialog.getSaveFileName(
```
#                         弹出另存为文件对话框：

```python
                            self, "另存为", "未命名.ai.json",
```
#                             标题 "另存为"，默认文件名 "未命名.ai.json"

```python
                            "Illustrator JSON (*.ai.json);;所有文件 (*.*)",
```
#                             文件类型过滤器：Illustrator JSON 格式或所有文件

```python
                        )
```
#                         对话框调用结束

```python
                        if file_path:
```
#                         如果用户选择了文件路径：

```python
                            self._document.save(file_path)
```
#                             保存到该路径

```python
                        else:
```
#                         否则（用户取消了对话框）：

```python
                            return  # 用户取消保存
```
#                             直接返回，取消新建操作

```python
                case QMessageBox.Cancel:
```
#                 用户选择 "取消"：

```python
                    return
```
#                     直接返回，取消新建操作

```python
        self._document = Document(800, 600, name="未命名-1")
```
#         创建新的文档实例，宽度 800、高度 600，名称 "未命名-1"

```python
        self._canvas.document = self._document
```
#         将新文档绑定到画布

```python
        self._chat_panel.set_document(self._document)
```
#         将新文档设置到 AI 聊天面板

```python
        self._swatches_panel.update_swatches(self._document.swatches)
```
#         更新色板面板为新文档的色板

```python
        self._update_all()
```
#         更新全部界面状态

```python
    def _on_open(self):
```
#     定义私有方法 `_on_open`（处理打开文件操作），接收自身引用参数

```python
        file_path, _ = QFileDialog.getOpenFileName(
```
#         弹出打开文件对话框：

```python
            self, "打开文件", "",
```
#             标题 "打开文件"，无默认路径

```python
            "Illustrator JSON (*.ai.json);;所有文件 (*.*)",
```
#             文件类型过滤器：Illustrator JSON 格式或所有文件

```python
        )
```
#         对话框调用结束

```python
        if file_path:
```
#         如果用户选择了文件路径：

```python
            try:
```
#             开始异常捕获：

```python
                self._document = Document.load(file_path)
```
#                 调用文档的 `load`（加载）方法从文件加载文档

```python
                self._canvas.document = self._document
```
#                 将加载的文档绑定到画布

```python
                self._chat_panel.set_document(self._document)
```
#                 将加载的文档设置到 AI 聊天面板

```python
                self._swatches_panel.update_swatches(self._document.swatches)
```
#                 更新色板面板

```python
                self._update_all()
```
#                 更新全部界面状态

```python
            except Exception as e:
```
#             捕获所有异常，赋值给 `e`：

```python
                logger.error(f"打开文件失败: {file_path} - {e}", exc_info=True)
```
#                 通过日志记录器输出错误日志："打开文件失败"，附带文件路径和异常堆栈信息

```python
                QMessageBox.critical(self, "错误", f"无法打开文件：{e}")
```
#                 弹出错误消息框，显示 "无法打开文件：错误详情"

```python
    def _on_save(self):
```
#     定义私有方法 `_on_save`（处理保存操作），接收自身引用参数

```python
        if not self._document:
```
#         如果文档不存在：

```python
            return
```
#             直接返回

```python
        if self._document.file_path:
```
#         如果文档已有文件路径（之前保存过）：

```python
            self._document.save(self._document.file_path)
```
#             直接保存到原文件路径

```python
            self._update_title()
```
#             更新窗口标题（移除修改标记）

```python
        else:
```
#         否则（尚未保存过）：

```python
            self._on_save_as()
```
#             调用 `_on_save_as`（处理另存为）方法

```python
    def _on_save_as(self):
```
#     定义私有方法 `_on_save_as`（处理另存为操作），接收自身引用参数

```python
        if not self._document:
```
#         如果文档不存在：

```python
            return
```
#             直接返回

```python
        file_path, _ = QFileDialog.getSaveFileName(
```
#         弹出另存为文件对话框：

```python
            self, "另存为", "未命名.ai.json",
```
#             标题 "另存为"，默认文件名 "未命名.ai.json"

```python
            "Illustrator JSON (*.ai.json);;所有文件 (*.*)",
```
#             文件类型过滤器

```python
        )
```
#         对话框调用结束

```python
        if file_path:
```
#         如果用户选择了文件路径：

```python
            self._document.save(file_path)
```
#             保存到该路径

```python
            self._update_title()
```
#             更新窗口标题（移除修改标记）

```python
    def _on_export(self):
```
#     定义私有方法 `_on_export`（处理导出 PNG 操作），接收自身引用参数

```python
        if not self._document:
```
#         如果文档不存在：

```python
            return
```
#             直接返回

```python
        file_path, _ = QFileDialog.getSaveFileName(
```
#         弹出另存为文件对话框：

```python
            self, "导出 PNG", "未命名.png", "PNG 图片 (*.png)",
```
#             标题 "导出 PNG"，默认文件名 "未命名.png"，文件类型为 PNG 图片

```python
        )
```
#         对话框调用结束

```python
        if file_path:
```
#         如果用户选择了文件路径：

```python
            pixmap = QPixmap(
```
#             创建 `像素图像` 实例：

```python
                int(self._document.width),
```
#                 宽度为文档宽度（转为整数）

```python
                int(self._document.height),
```
#                 高度为文档高度（转为整数）

```python
            )
```
#             像素图像创建完成

```python
            pixmap.fill(Qt.white)
```
#             将像素图像填充为白色背景

```python
            painter = QPainter(pixmap)
```
#             创建 `绘图器` 实例，以像素图像为绘图设备

```python
            painter.setRenderHint(QPainter.Antialiasing)
```
#             设置渲染提示为抗锯齿（使图形边缘平滑）

```python
            for layer in self._document.layers:
```
#             遍历文档中的所有图层：

```python
                if layer.visible:
```
#                 如果图层可见：

```python
                    painter.setOpacity(layer.opacity)
```
#                     设置绘图器的不透明度为图层的不透明度

```python
                    for item in layer.items:
```
#                     遍历图层中的所有图元：

```python
                        if item.visible:
```
#                         如果图元可见：

```python
                            self._canvas._draw_item(painter, item)
```
#                             调用画布的私有方法 `_draw_item`（绘制图元），将该图元绘制到像素图像上

```python
            painter.end()
```
#             结束绘图器（释放资源）

```python
            pixmap.save(file_path, "PNG")
```
#             将像素图像以 PNG 格式保存到指定文件路径

```python
            QMessageBox.information(self, "导出成功", f"已导出到：{file_path}")
```
#             弹出信息对话框，显示 "导出成功" 和导出路径

```python
    def keyPressEvent(self, event):
```
#     重写 `keyPressEvent`（按键事件处理）方法，接收自身引用和 `event`（按键事件对象）参数

```python
        """主窗口快捷键 —— F7 打开图层面板（PDF 快捷键表）"""
```
#         文档字符串：主窗口快捷键 —— F7 打开图层面板（PDF 快捷键表）

```python
        if event.key() == Qt.Key_F7:
```
#         如果按下的是 F7 键：

```python
            # 切换图层面板可见性
```
#             注释：切换图层面板可见性

```python
            for dock in self.findChildren(QDockWidget):
```
#             查找主窗口下所有 `停靠窗口` 子对象，遍历它们：

```python
                w = dock.widget()
```
#                 获取停靠窗口的内容控件

```python
                if w and hasattr(w, '_layers_data'):
```
#                 如果内容控件存在且具有 `_layers_data` 属性（标识为图层面板）：

```python
                    dock.setVisible(not dock.isVisible())
```
#                     切换该停靠窗口的可见性（可见变为隐藏，隐藏变为可见）

```python
                    return
```
#                     处理完毕后返回，不传递给父类

```python
        super().keyPressEvent(event)
```
#         调用父类的按键事件处理方法（处理其他按键）

```python
    def closeEvent(self, event):
```
#     重写 `closeEvent`（关闭事件处理）方法，接收自身引用和 `event`（关闭事件对象）参数

```python
        logger.info("应用程序正在关闭")
```
#         通过日志记录器输出信息日志："应用程序正在关闭"

```python
        if self._document and self._document.modified:
```
#         如果文档存在且已修改（有未保存的更改）：

```python
            ret = QMessageBox.question(
```
#             弹出确认对话框：

```python
                self, "未保存的更改",
```
#                 标题 "未保存的更改"

```python
                "是否保存当前文档的更改？",
```
#                 消息 "是否保存当前文档的更改？"

```python
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
```
#                 提供 "保存"、"放弃"、"取消" 三个按钮

```python
            )
```
#             对话框调用结束

```python
            match ret:
```
#             使用模式匹配根据用户选择执行不同操作：

```python
                case QMessageBox.Save:
```
#                 用户选择 "保存"：

```python
                    # 如果文档有路径直接保存，否则弹出另存为对话框
```
#                     注释：如果文档有路径直接保存，否则弹出另存为对话框

```python
                    if self._document.file_path:
```
#                     如果文档已有文件路径：

```python
                        self._document.save(self._document.file_path)
```
#                         直接保存到原文件路径

```python
                        event.accept()
```
#                         接受关闭事件（允许窗口关闭）

```python
                    else:
```
#                     否则（尚未保存过）：

```python
                        # 另存为对话框，用户可能取消
```
#                         注释：另存为对话框，用户可能取消

```python
                        file_path, _ = QFileDialog.getSaveFileName(
```
#                         弹出另存为文件对话框

```python
                            self, "另存为", "未命名.ai.json",
```
#                             标题 "另存为"，默认文件名 "未命名.ai.json"

```python
                            "Illustrator JSON (*.ai.json);;所有文件 (*.*)",
```
#                             文件类型过滤器

```python
                        )
```
#                         对话框调用结束

```python
                        if file_path:
```
#                         如果用户选择了文件路径：

```python
                            self._document.save(file_path)
```
#                             保存到该路径

```python
                            event.accept()
```
#                             接受关闭事件

```python
                        else:
```
#                         否则（用户取消）：

```python
                            event.ignore()
```
#                             忽略关闭事件（阻止窗口关闭）

```python
                case QMessageBox.Discard:
```
#                 用户选择 "放弃"：

```python
                    event.accept()
```
#                     接受关闭事件（允许窗口关闭，不保存更改）

```python
                case _:
```
#                 其他情况（如用户选择 "取消"）：

```python
                    event.ignore()
```
#                     忽略关闭事件（阻止窗口关闭）

```python
        else:
```
#         否则（文档不存在或无未保存更改）：

```python
            event.accept()
```
#             接受关闭事件（允许窗口关闭）
