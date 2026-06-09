# panels.py 中文注解翻译

```python
"""
```
# 三引号字符串开始

```python
面板组件 (Python 3.10+) —— 工具栏、属性面板、图层面板、色板
```
# 面板组件（要求 Python 3.10 及以上版本）—— 包含工具栏、属性面板、图层面板和色板


```python
架构优化:
```
# 架构优化说明：

```python
- 使用 __slots__ 减少内存占用
```
# —— 使用 __slots__（槽位机制）减少内存占用

```python
- 使用 X | None 替代 Optional[X]
```
# —— 使用 X | None 语法替代 Optional[X] 类型注解

```python
- 使用 match-case 替代 if-elif 链
```
# —— 使用 match-case 模式匹配替代 if-elif 条件链

```python
"""
```
# 三引号字符串结束


```python
from __future__ import annotations
```
# from __future__ import annotations


```python
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QRectF
```
# from PyQt5.QtCore import Qt, QSize, pyqtSignal, QRectF

```python
from PyQt5.QtGui import (
```
# 从 PyQt5 的核心模块导入：Qt（枚举常量）、QSize（尺寸类）、pyqtSignal（信号机制）、QRectF（矩形浮点类）

```python
    QColor, QPainter, QPen, QBrush, QFont,
```
# 从 PyQt5 的图形界面模块导入以下类：

```python
)
```
#     QColor（颜色类）、QPainter（绘图器）、QPen（画笔）、QBrush（画刷）、QFont（字体类）

```python
from PyQt5.QtWidgets import (
```
# 导入语句结束括号

```python
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
```
# 从 PyQt5 的控件模块导入以下控件类：

```python
    QListWidget, QListWidgetItem, QSlider, QSpinBox,
```
#     QWidget（基础部件）、QVBoxLayout（垂直布局）、QHBoxLayout（水平布局）、QPushButton（按钮）、QLabel（标签）

```python
    QDoubleSpinBox, QCheckBox, QColorDialog, QGroupBox,
```
#     QListWidget（列表控件）、QListWidgetItem（列表项）、QSlider（滑动条）、QSpinBox（整数旋转框）

```python
    QToolBar, QAction, QFrame,
```
#     QDoubleSpinBox（浮点旋转框）、QCheckBox（复选框）、QColorDialog（颜色选择对话框）、QGroupBox（分组框）

```python
    QLineEdit, QComboBox, QGridLayout,
```
#     QToolBar（工具栏控件）、QAction（动作）、QFrame（框架）

```python
    QToolButton, QTextEdit, QMenu,
```
#     QLineEdit（单行文本输入框）、QComboBox（下拉组合框）、QGridLayout（网格布局）

```python
    QTreeWidget, QTreeWidgetItem, QHeaderView,
```
#     QToolButton（工具按钮）、QTextEdit（多行文本编辑框）、QMenu（菜单）

```python
)
```
#     QTreeWidget（树控件）、QTreeWidgetItem（树节点项）、QHeaderView（表头视图）


```python
from ..core.graphics import (
```
# from ..core.graphics import (

```python
    GraphicItem, PathItem, RectangleItem, EllipseItem,
```
# 从上层核心图形模块导入以下图形类：

```python
    TextFrame, GroupItem, GraphicStyle, StrokeCap, StrokeJoin,
```
#     GraphicItem（图形项基类）、PathItem（路径项）、RectangleItem（矩形项）、EllipseItem（椭圆项）

```python
    FillRule, CharacterAttributes, ParagraphAttributes, Justification,
```
#     TextFrame（文本框架）、GroupItem（群组项）、GraphicStyle（图形样式）、StrokeCap（线帽样式）、StrokeJoin（线连接样式）

```python
    Swatch,
```
#     FillRule（填充规则）、CharacterAttributes（字符属性）、ParagraphAttributes（段落属性）、Justification（对齐方式）

```python
)
```
#     Swatch（色板）

```python
from ..core.document import Document, Layer
```
# 导入语句结束括号

```python
from ..core.tools import ToolType
```
# 从上层核心文档模块导入：Document（文档类）、Layer（图层类）



```python
# ── 工具栏 ────────────────────────────────────────────────
```
# # ── 工具栏 ────────────────────────────────────────────────


```python
class ToolBar(QWidget):
```
# class ToolBar(QWidget):

```python
    """工具栏 —— 左侧工具面板
```
# 定义工具栏类（继承自 Qt 部件类 QWidget）

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
#     类文档字符串：工具栏 —— 位于界面左侧的工具面板

```python
    """
```
#     注意事项：PyQt5 的 QWidget 子类不能使用 __slots__ 槽位机制。


```python
    tool_selected = pyqtSignal(ToolType)
```
#     tool_selected = pyqtSignal(ToolType)    选中工具 = pyqtSignal(工具类型)


```python
    TOOLS: list[tuple[ToolType, str, str]] = [
```
#     TOOLS: list[tuple[ToolType, str, str]] = [

```python
        (ToolType.SELECTION, "选择", "V"),
```
#     定义工具列表类属性（类型为列表，元素为元组：工具类型、名称字符串、快捷键字符串）

```python
        (ToolType.DIRECT_SELECT, "直接选择", "A"),
```
#         （选择工具，显示名称"选择"，快捷键"V"）

```python
        (ToolType.RECTANGLE, "矩形", "M"),
```
#         （直接选择工具，显示名称"直接选择"，快捷键"A"）

```python
        (ToolType.ELLIPSE, "椭圆", "L"),
```
#         （矩形工具，显示名称"矩形"，快捷键"M"）

```python
        (ToolType.PEN, "钢笔", "P"),
```
#         （椭圆工具，显示名称"椭圆"，快捷键"L"）

```python
        (ToolType.TEXT, "文字", "T"),
```
#         （钢笔工具，显示名称"钢笔"，快捷键"P"）

```python
        (ToolType.HAND, "抓手", "H"),
```
#         （文字工具，显示名称"文字"，快捷键"T"）

```python
    ]
```
#         （抓手工具，显示名称"抓手"，快捷键"H"）


```python
    def __init__(self, parent=None):
```
#     def __init__(self, parent=None):

```python
        super().__init__(parent)
```
#     定义初始化方法（接收自身引用 self、父部件参数 parent：默认为空）

```python
        self.setFixedWidth(48)
```
#         调用父类 QWidget 的初始化方法，传入父部件参数

```python
        self._buttons: dict[ToolType, QToolButton] = {}
```
#         设置工具栏固定宽度为 48 像素

```python
        self._current_tool = ToolType.SELECTION
```
#         定义私有属性 _buttons：工具按钮字典（键为工具类型，值为工具按钮控件），初始为空字典

```python
        self._init_ui()
```
#         定义私有属性 _current_tool：当前选中的工具，默认为选择工具


```python
    def _init_ui(self):
```
#     def _init_ui(self):

```python
        layout = QVBoxLayout(self)
```
#     定义私有界面初始化方法（构建工具栏界面布局）

```python
        layout.setContentsMargins(4, 8, 4, 8)
```
#         创建垂直布局管理器，以自身（工具栏）为父部件

```python
        layout.setSpacing(4)
```
#         设置布局内容边距（左 4、上 8、右 4、下 8 像素）


```python
        for tool_type, name, shortcut in self.TOOLS:
```
#         for tool_type, name, shortcut in self.TOOLS:

```python
            btn = QToolButton()
```
#         遍历工具列表，每次取出工具类型、名称、快捷键

```python
            btn.setToolTip(f"{name} ({shortcut})")
```
#             创建工具按钮实例

```python
            btn.setCheckable(True)
```
#             设置按钮提示文本（显示名称加括号内的快捷键）

```python
            btn.setFixedSize(40, 40)
```
#             设置按钮为可选中状态（支持切换选中/未选中）

```python
            btn.setText(shortcut)
```
#             设置按钮固定尺寸为 40×40 像素

```python
            btn.setFont(QFont("Arial", 10, QFont.Bold))
```
#             设置按钮显示文本为快捷键字母

```python
            btn.clicked.connect(lambda checked, t=tool_type: self._on_tool_clicked(t))
```
#             设置按钮字体为 Arial、大小 10、粗体

```python
            self._buttons[tool_type] = btn
```
#             连接按钮点击信号到匿名回调（使用默认参数 t 捕获当前工具类型，调用工具点击处理方法）

```python
            layout.addWidget(btn, alignment=Qt.AlignCenter)
```
#             将按钮存入按钮字典，以工具类型为键


```python
        layout.addStretch()
```
#         layout.addStretch()

```python
        self._buttons[ToolType.SELECTION].setChecked(True)
```
#         在布局末尾添加弹性拉伸空间，将按钮推到顶部


```python
        self.setStyleSheet("""
```
#         self.setStyleSheet("""

```python
            QWidget { background-color: #3c3c3c; }
```
#         设置工具栏样式表（暗色主题）

```python
            QToolButton { border: 1px solid #555; border-radius: 4px; background-color: #4a4a4a; color: #ddd; }
```
#         部件背景色为深灰色 #3c3c3c

```python
            QToolButton:hover { background-color: #5a5a5a; }
```
#         工具按钮样式：1像素 #555 边框、4像素圆角、#4a4a4a 背景色、#ddd 文字颜色

```python
            QToolButton:checked { background-color: #0d6efd; border-color: #0b5ed7; color: white; }
```
#         工具按钮悬停时背景色变为 #5a5a5a

```python
        """)
```
#         工具按钮选中时背景色为蓝色 #0d6efd、边框色 #0b5ed7、文字为白色


```python
    def _on_tool_clicked(self, tool_type: ToolType):
```
#     def _on_tool_clicked(self, tool_type: ToolType):

```python
        self._current_tool = tool_type
```
#     定义工具按钮点击处理方法（接收自身引用、工具类型参数）

```python
        for t, btn in self._buttons.items():
```
#         将当前工具设置为传入的工具类型

```python
            btn.setChecked(t == tool_type)
```
#         遍历按钮字典的所有键值对（工具类型、按钮）

```python
        self.tool_selected.emit(tool_type)
```
#             将按钮设为选中状态（仅当按钮对应的工具类型与传入工具类型相同时选中）


```python
    def set_current_tool(self, tool_type: ToolType):
```
#     def set_current_tool(self, tool_type: ToolType):

```python
        if tool_type in self._buttons:
```
#     定义设置当前工具的公开方法（接收自身引用、工具类型参数）

```python
            self._buttons[tool_type].setChecked(True)
```
#         如果传入的工具类型存在于按钮字典中

```python
            self._current_tool = tool_type
```
#             将对应按钮设为选中状态

```python
            for t, btn in self._buttons.items():
```
#             更新当前工具记录

```python
                btn.setChecked(t == tool_type)
```
#             遍历按钮字典所有键值对



```python
# ── 属性面板 ──────────────────────────────────────────────
```
# # ── 属性面板 ──────────────────────────────────────────────


```python
class PropertiesPanel(QWidget):
```
# class PropertiesPanel(QWidget):

```python
    """属性面板 —— 显示和编辑选中图形的属性
```
# 定义属性面板类（继承自 Qt 部件类 QWidget）

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
#     类文档字符串：属性面板 —— 用于显示和编辑选中图形的各项属性

```python
    """
```
#     注意事项：PyQt5 的 QWidget 子类不能使用 __slots__ 槽位机制。


```python
    fill_color_changed = pyqtSignal(QColor)
```
#     fill_color_changed = pyqtSignal(QColor)

```python
    stroke_color_changed = pyqtSignal(QColor)
```
#     定义填充颜色变更信号（参数类型为 QColor 颜色类）

```python
    stroke_width_changed = pyqtSignal(float)
```
#     定义描边颜色变更信号（参数类型为 QColor 颜色类）

```python
    opacity_changed = pyqtSignal(float)
```
#     定义描边粗细变更信号（参数类型为浮点数）

```python
    corner_radius_changed = pyqtSignal(float)
```
#     定义不透明度变更信号（参数类型为浮点数）

```python
    text_changed = pyqtSignal(str)
```
#     定义圆角半径变更信号（参数类型为浮点数）

```python
    font_size_changed = pyqtSignal(float)
```
#     定义文本内容变更信号（参数类型为字符串）

```python
    font_family_changed = pyqtSignal(str)
```
#     定义字体大小变更信号（参数类型为浮点数）

```python
    bold_changed = pyqtSignal(bool)
```
#     定义字体族变更信号（参数类型为字符串）

```python
    italic_changed = pyqtSignal(bool)
```
#     定义粗体状态变更信号（参数类型为布尔值）

```python
    alignment_changed = pyqtSignal(Justification)
```
#     定义斜体状态变更信号（参数类型为布尔值）

```python
    order_front = pyqtSignal()
```
#     定义对齐方式变更信号（参数类型为对齐方式枚举 Justification）

```python
    order_back = pyqtSignal()
```
#     定义置顶信号（无参数）

```python
    order_forward = pyqtSignal()
```
#     定义置底信号（无参数）

```python
    order_backward = pyqtSignal()
```
#     定义上移一层信号（无参数）

```python
    delete_requested = pyqtSignal()
```
#     定义下移一层信号（无参数）


```python
    def __init__(self, parent=None):
```
#     def __init__(self, parent=None):

```python
        super().__init__(parent)
```
#     定义初始化方法（接收自身引用 self、父部件参数 parent：默认为空）

```python
        self._selected_items: list[GraphicItem] = []
```
#         调用父类 QWidget 的初始化方法，传入父部件参数

```python
        self._init_ui()
```
#         定义私有属性 _selected_items：当前选中的图形项列表，初始为空列表


```python
    def _init_ui(self):
```
#     def _init_ui(self):

```python
        main_layout = QVBoxLayout(self)
```
#     定义私有界面初始化方法（构建属性面板界面）

```python
        main_layout.setContentsMargins(8, 8, 8, 8)
```
#         创建主垂直布局管理器，以自身为父部件

```python
        main_layout.setSpacing(8)
```
#         设置主布局内容边距（上、下、左、右各 8 像素）


```python
        # ── 变换 ──
```
#         # ── 变换 ──

```python
        transform_group = QGroupBox("变换")
```
#         ── 变换区域注释 ──

```python
        transform_layout = QGridLayout(transform_group)
```
#         创建分组框，标题为"变换"


```python
        self._x_spin = self._make_spinbox(-9999, 9999, 1)
```
#         self._x_spin = self._make_spinbox(-9999, 9999, 1)

```python
        self._y_spin = self._make_spinbox(-9999, 9999, 1)
```
#         创建 X 坐标旋转框（范围 -9999 到 9999，小数位数 1 位）

```python
        self._w_spin = self._make_spinbox(0, 99999, 1)
```
#         创建 Y 坐标旋转框（范围 -9999 到 9999，小数位数 1 位）

```python
        self._h_spin = self._make_spinbox(0, 99999, 1)
```
#         创建宽度旋转框（范围 0 到 99999，小数位数 1 位）


```python
        for row, items in enumerate([
```
#         for row, items in enumerate([

```python
            [("X:", self._x_spin), ("Y:", self._y_spin)],
```
#         遍历以下二维列表，同时获取行索引和该行的控件对：

```python
            [("W:", self._w_spin), ("H:", self._h_spin)],
```
#             第一行：X 标签和 X 旋转框、Y 标签和 Y 旋转框

```python
        ]):
```
#             第二行：W 标签和宽度旋转框、H 标签和高度旋转框

```python
            (label0, widget0), (label1, widget1) = items
```
#         列表结束并进入循环体

```python
            transform_layout.addWidget(QLabel(label0), row, 0)
```
#             解构当前行的两组标签和控件

```python
            transform_layout.addWidget(widget0, row, 1)
```
#             将第一个标签添加到网格布局的（当前行、第 0 列）

```python
            transform_layout.addWidget(QLabel(label1), row, 2)
```
#             将第一个控件添加到网格布局的（当前行、第 1 列）

```python
            transform_layout.addWidget(widget1, row, 3)
```
#             将第二个标签添加到网格布局的（当前行、第 2 列）


```python
        transform_layout.addWidget(QLabel("旋转:"), 2, 0)
```
#         transform_layout.addWidget(QLabel("旋转:"), 2, 0)

```python
        self._rotate_spin = QDoubleSpinBox()
```
#         将"旋转:"标签添加到网格布局的第 2 行第 0 列

```python
        self._rotate_spin.setRange(-360, 360)
```
#         创建旋转角度浮点旋转框

```python
        transform_layout.addWidget(self._rotate_spin, 2, 1)
```
#         设置旋转角度范围为 -360 到 360 度


```python
        transform_layout.addWidget(QLabel("不透明度:"), 2, 2)
```
#         transform_layout.addWidget(QLabel("不透明度:"), 2, 2)

```python
        self._opacity_spin = QDoubleSpinBox()
```
#         将"不透明度:"标签添加到网格布局的第 2 行第 2 列

```python
        self._opacity_spin.setRange(0, 100)
```
#         创建不透明度浮点旋转框

```python
        self._opacity_spin.setValue(100)
```
#         设置不透明度范围为 0 到 100

```python
        self._opacity_spin.setSuffix("%")
```
#         设置不透明度默认值为 100（完全不透明）

```python
        self._opacity_spin.valueChanged.connect(lambda v: self.opacity_changed.emit(v / 100.0))
```
#         设置旋转框后缀为百分号"%"

```python
        transform_layout.addWidget(self._opacity_spin, 2, 3)
```
#         连接不透明度值变更信号到匿名回调（将百分比值除以 100 转为小数后发射信号）


```python
        main_layout.addWidget(transform_group)
```
#         main_layout.addWidget(transform_group)


```python
        # ── 外观 ──
```
#         # ── 外观 ──

```python
        appearance_group = QGroupBox("外观")
```
#         ── 外观区域注释 ──

```python
        appearance_layout = QVBoxLayout(appearance_group)
```
#         创建分组框，标题为"外观"


```python
        fill_layout = QHBoxLayout()
```
#         fill_layout = QHBoxLayout()

```python
        fill_layout.addWidget(QLabel("填充:"))
```
#         创建填充颜色水平布局

```python
        self._fill_btn = QPushButton()
```
#         在填充布局中添加"填充:"标签

```python
        self._fill_btn.setFixedSize(30, 30)
```
#         创建填充颜色按钮

```python
        self._fill_btn.setStyleSheet("background-color: #ccc; border: 1px solid #888;")
```
#         设置填充按钮固定尺寸为 30×30 像素

```python
        self._fill_btn.clicked.connect(self._on_fill_clicked)
```
#         设置填充按钮样式（浅灰色背景 #ccc、#888 边框）

```python
        fill_layout.addWidget(self._fill_btn)
```
#         连接填充按钮点击信号到填充点击处理方法

```python
        self._fill_none_btn = QPushButton("无")
```
#         将填充按钮添加到填充布局中

```python
        self._fill_none_btn.setFixedWidth(30)
```
#         创建"无"按钮（用于清除填充颜色）

```python
        self._fill_none_btn.clicked.connect(self._on_fill_none)
```
#         设置无填充按钮固定宽度为 30 像素

```python
        fill_layout.addWidget(self._fill_none_btn)
```
#         连接无填充按钮点击信号到无填充处理方法

```python
        fill_layout.addStretch()
```
#         将无填充按钮添加到填充布局中

```python
        appearance_layout.addLayout(fill_layout)
```
#         在填充布局末尾添加弹性拉伸空间


```python
        stroke_layout = QHBoxLayout()
```
#         stroke_layout = QHBoxLayout()

```python
        stroke_layout.addWidget(QLabel("描边:"))
```
#         创建描边水平布局

```python
        self._stroke_btn = QPushButton()
```
#         在描边布局中添加"描边:"标签

```python
        self._stroke_btn.setFixedSize(30, 30)
```
#         创建描边颜色按钮

```python
        self._stroke_btn.setStyleSheet("background-color: #333; border: 1px solid #888;")
```
#         设置描边按钮固定尺寸为 30×30 像素

```python
        self._stroke_btn.clicked.connect(self._on_stroke_clicked)
```
#         设置描边按钮样式（深灰色背景 #333、#888 边框）

```python
        stroke_layout.addWidget(self._stroke_btn)
```
#         连接描边按钮点击信号到描边点击处理方法

```python
        self._stroke_none_btn = QPushButton("无")
```
#         将描边按钮添加到描边布局中

```python
        self._stroke_none_btn.setFixedWidth(30)
```
#         创建描边"无"按钮（用于清除描边颜色）

```python
        self._stroke_none_btn.clicked.connect(self._on_stroke_none)
```
#         设置无描边按钮固定宽度为 30 像素

```python
        stroke_layout.addWidget(self._stroke_none_btn)
```
#         连接无描边按钮点击信号到无描边处理方法

```python
        stroke_layout.addWidget(QLabel("粗细:"))
```
#         将无描边按钮添加到描边布局中

```python
        self._stroke_width = QDoubleSpinBox()
```
#         在描边布局中添加"粗细:"标签

```python
        self._stroke_width.setRange(0, 100)
```
#         创建描边粗细浮点旋转框

```python
        self._stroke_width.setValue(1)
```
#         设置描边粗细范围为 0 到 100

```python
        self._stroke_width.valueChanged.connect(self.stroke_width_changed.emit)
```
#         设置描边粗细默认值为 1

```python
        stroke_layout.addWidget(self._stroke_width)
```
#         连接描边粗细值变更信号直接发射描边粗细变更信号

```python
        appearance_layout.addLayout(stroke_layout)
```
#         将描边粗细旋转框添加到描边布局中


```python
        corner_layout = QHBoxLayout()
```
#         corner_layout = QHBoxLayout()

```python
        corner_layout.addWidget(QLabel("圆角:"))
```
#         创建圆角水平布局

```python
        self._corner_spin = QDoubleSpinBox()
```
#         在圆角布局中添加"圆角:"标签

```python
        self._corner_spin.setRange(0, 500)
```
#         创建圆角半径浮点旋转框

```python
        self._corner_spin.valueChanged.connect(self.corner_radius_changed.emit)
```
#         设置圆角半径范围为 0 到 500

```python
        corner_layout.addWidget(self._corner_spin)
```
#         连接圆角值变更信号直接发射圆角半径变更信号

```python
        corner_layout.addStretch()
```
#         将圆角旋转框添加到圆角布局中

```python
        appearance_layout.addLayout(corner_layout)
```
#         在圆角布局末尾添加弹性拉伸空间


```python
        main_layout.addWidget(appearance_group)
```
#         main_layout.addWidget(appearance_group)


```python
        # ── 文字 ──
```
#         # ── 文字 ──

```python
        text_group = QGroupBox("文字")
```
#         ── 文字区域注释 ──

```python
        text_layout = QVBoxLayout(text_group)
```
#         创建分组框，标题为"文字"


```python
        font_layout = QHBoxLayout()
```
#         font_layout = QHBoxLayout()

```python
        self._font_family = QComboBox()
```
#         创建字体选择水平布局

```python
        self._font_family.setEditable(True)
```
#         创建字体族下拉组合框

```python
        self._font_family.addItems([
```
#         设置字体族组合框为可编辑模式（允许手动输入字体名）

```python
            "Arial", "Helvetica", "Times New Roman", "Courier New",
```
#             Arial、Helvetica、Times New Roman、Courier New

```python
            "Verdana", "Georgia", "微软雅黑", "宋体", "黑体",
```
#             Verdana、Georgia、微软雅黑、宋体、黑体

```python
        ])
```
#         字体列表结束

```python
        self._font_family.currentTextChanged.connect(self.font_family_changed.emit)
```
#         连接字体族文本变更信号直接发射字体族变更信号

```python
        font_layout.addWidget(self._font_family)
```
#         将字体族组合框添加到字体布局中


```python
        self._font_size = QDoubleSpinBox()
```
#         创建字体大小浮点旋转框

```python
        self._font_size.setRange(1, 999)
```
#         设置字体大小范围为 1 到 999

```python
        self._font_size.setValue(24)
```
#         设置字体大小默认值为 24

```python
        self._font_size.valueChanged.connect(self.font_size_changed.emit)
```
#         连接字体大小值变更信号直接发射字体大小变更信号

```python
        font_layout.addWidget(self._font_size)
```
#         将字体大小旋转框添加到字体布局中

```python
        text_layout.addLayout(font_layout)
```
#         将字体布局添加到文字布局中


```python
        style_layout = QHBoxLayout()
```
#         创建样式（粗体/斜体）水平布局

```python
        self._bold_btn = QPushButton("B")
```
#         创建粗体按钮（显示字母"B"）

```python
        self._bold_btn.setCheckable(True)
```
#         设置粗体按钮为可选中状态（切换粗体）

```python
        self._bold_btn.setFont(QFont("Arial", 12, QFont.Bold))
```
#         设置粗体按钮字体为 Arial、大小 12、粗体

```python
        self._bold_btn.setFixedSize(30, 30)
```
#         设置粗体按钮固定尺寸为 30×30 像素

```python
        self._bold_btn.toggled.connect(self.bold_changed.emit)
```
#         连接粗体按钮切换信号直接发射粗体变更信号

```python
        style_layout.addWidget(self._bold_btn)
```
#         将粗体按钮添加到样式布局中


```python
        self._italic_btn = QPushButton("I")
```
#         创建斜体按钮（显示字母"I"）

```python
        self._italic_btn.setCheckable(True)
```
#         设置斜体按钮为可选中状态（切换斜体）

```python
        self._italic_btn.setFont(QFont("Arial", 12, QFont.StyleItalic))
```
#         设置斜体按钮字体为 Arial、大小 12、斜体

```python
        self._italic_btn.setFixedSize(30, 30)
```
#         设置斜体按钮固定尺寸为 30×30 像素

```python
        self._italic_btn.toggled.connect(self.italic_changed.emit)
```
#         连接斜体按钮切换信号直接发射斜体变更信号

```python
        style_layout.addWidget(self._italic_btn)
```
#         将斜体按钮添加到样式布局中

```python
        style_layout.addStretch()
```
#         在样式布局末尾添加弹性拉伸空间

```python
        text_layout.addLayout(style_layout)
```
#         将样式布局添加到文字布局中


```python
        align_layout = QHBoxLayout()
```
#         创建对齐方式水平布局

```python
        self._align_left = QPushButton("左")
```
#         创建左对齐按钮（显示"左"）

```python
        self._align_left.setCheckable(True)
```
#         设置左对齐按钮为可选中状态

```python
        self._align_left.clicked.connect(lambda: self.alignment_changed.emit(Justification.LEFT))
```
#         连接左对齐按钮点击信号到匿名回调（发射对齐方式变更信号，传入左对齐枚举值）

```python
        align_layout.addWidget(self._align_left)
```
#         将左对齐按钮添加到对齐布局中


```python
        self._align_center = QPushButton("中")
```
#         创建居中对齐按钮（显示"中"）

```python
        self._align_center.setCheckable(True)
```
#         设置居中对齐按钮为可选中状态

```python
        self._align_center.clicked.connect(lambda: self.alignment_changed.emit(Justification.CENTER))
```
#         连接居中对齐按钮点击信号到匿名回调（发射对齐方式变更信号，传入居中对齐枚举值）

```python
        align_layout.addWidget(self._align_center)
```
#         将居中对齐按钮添加到对齐布局中


```python
        self._align_right = QPushButton("右")
```
#         创建右对齐按钮（显示"右"）

```python
        self._align_right.setCheckable(True)
```
#         设置右对齐按钮为可选中状态

```python
        self._align_right.clicked.connect(lambda: self.alignment_changed.emit(Justification.RIGHT))
```
#         连接右对齐按钮点击信号到匿名回调（发射对齐方式变更信号，传入右对齐枚举值）

```python
        align_layout.addWidget(self._align_right)
```
#         将右对齐按钮添加到对齐布局中

```python
        text_layout.addLayout(align_layout)
```
#         将对齐布局添加到文字布局中


```python
        self._text_edit = QTextEdit()
```
#         创建多行文本编辑框

```python
        self._text_edit.setMaximumHeight(80)
```
#         设置文本编辑框最大高度为 80 像素

```python
        self._text_edit.setPlaceholderText("输入文字内容...")
```
#         设置文本编辑框占位提示文本为"输入文字内容..."

```python
        self._text_edit.textChanged.connect(
```
#         连接文本编辑框文本变更信号到匿名回调函数：

```python
            lambda: self.text_changed.emit(self._text_edit.toPlainText()),
```
#             获取纯文本内容并发射文本变更信号

```python
        )
```
#         匿名回调函数定义结束

```python
        text_layout.addWidget(self._text_edit)
```
#         将文本编辑框添加到文字布局中


```python
        main_layout.addWidget(text_group)
```
#         将文字分组框添加到主布局中


```python
        # ── 排列 ──
```
#         ── 排列区域注释 ──

```python
        arrange_group = QGroupBox("排列")
```
#         创建分组框，标题为"排列"

```python
        arrange_layout = QHBoxLayout(arrange_group)
```
#         创建水平布局管理器，以排列分组框为父部件

```python
        for text, signal in [
```
#         遍历以下排列按钮列表（按钮文本、对应信号）：

```python
            ("置顶", self.order_front),
```
#             （"置顶"文本，置顶信号）

```python
            ("上移", self.order_forward),
```
#             （"上移"文本，上移一层信号）

```python
            ("下移", self.order_backward),
```
#             （"下移"文本，下移一层信号）

```python
            ("置底", self.order_back),
```
#             （"置底"文本，置底信号）

```python
        ]:
```
#         列表结束并进入循环体

```python
            btn = QPushButton(text)
```
#             创建按钮，显示对应文本

```python
            btn.clicked.connect(signal.emit)
```
#             连接按钮点击信号直接发射对应排列信号

```python
            arrange_layout.addWidget(btn)
```
#             将按钮添加到排列布局中

```python
        main_layout.addWidget(arrange_group)
```
#         将排列分组框添加到主布局中


```python
        # ── 删除 ──
```
#         ── 删除区域注释 ──

```python
        self._delete_btn = QPushButton("删除选中对象")
```
#         创建"删除选中对象"按钮

```python
        self._delete_btn.setStyleSheet("""
```
#         设置删除按钮样式表：

```python
            QPushButton {
```
#         按钮默认样式：红色背景 #dc3545、白色文字、无边框

```python
                background-color: #dc3545; color: white; border: none;
```
#         内边距 8 像素、4 像素圆角、粗体字

```python
                padding: 8px; border-radius: 4px; font-weight: bold;
```
#         按钮默认样式结束

```python
            }
```
#         按钮悬停时背景色变为深红色 #c82333

```python
            QPushButton:hover { background-color: #c82333; }
```
#         样式表字符串结束

```python
        """)
```
#         连接删除按钮点击信号直接发射删除请求信号

```python
        self._delete_btn.clicked.connect(self.delete_requested.emit)
```
#         将删除按钮添加到主布局中

```python
        main_layout.addWidget(self._delete_btn)
```
#         main_layout.addWidget(self._delete_btn)


```python
        main_layout.addStretch()
```
#         main_layout.addStretch()


```python
        self.setStyleSheet("""
```
#         分组框样式：粗体、#555 边框、4像素圆角、上边距 8 像素、上内边距 12 像素、#ddd 文字颜色

```python
            QGroupBox { font-weight: bold; border: 1px solid #555; border-radius: 4px; margin-top: 8px; padding-top: 12px; color: #ddd; }
```
#         分组框标题样式：基于边距定位、左侧 10 像素、水平内边距 5 像素、#ccc 颜色

```python
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #ccc; }
```
#         标签文字颜色为 #bbb

```python
            QLabel { color: #bbb; }
```
#         旋转框和组合框样式：#3c3c3c 背景色、#ddd 文字色、#555 边框、2像素内边距

```python
            QDoubleSpinBox, QSpinBox, QComboBox { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; padding: 2px; }
```
#         按钮样式：#4a4a4a 背景色、#ddd 文字色、#555 边框、4×8像素内边距、3像素圆角

```python
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; padding: 4px 8px; border-radius: 3px; }
```
#         按钮悬停时背景色为 #5a5a5a

```python
            QPushButton:hover { background-color: #5a5a5a; }
```
#         按钮选中时背景色为蓝色 #0d6efd、文字为白色

```python
            QPushButton:checked { background-color: #0d6efd; color: white; }
```
#         文本编辑框样式：#3c3c3c 背景色、#ddd 文字色、#555 边框

```python
            QTextEdit { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; }
```
#         样式表字符串结束

```python
        """)
```
#         设置属性面板最小宽度为 220 像素

```python
        self.setMinimumWidth(220)
```
#         self.setMinimumWidth(220)


```python
    @staticmethod
```
#     定义创建浮点旋转框的私有静态方法（接收最小值、最大值、小数位数参数，返回浮点旋转框）

```python
    def _make_spinbox(min_val: float, max_val: float, decimals: int) -> QDoubleSpinBox:
```
#         创建浮点旋转框实例

```python
        sb = QDoubleSpinBox()
```
#         设置旋转框数值范围为最小值到最大值

```python
        sb.setRange(min_val, max_val)
```
#         设置旋转框小数位数为指定值

```python
        sb.setDecimals(decimals)
```
#         返回创建好的旋转框

```python
        return sb
```
#         return sb


```python
    def update_selection(self, items: list[GraphicItem]):
```
#         方法文档字符串：更新选中项的属性面板显示

```python
        """更新选中项显示"""
```
#         将传入的图形项列表保存到私有属性

```python
        self._selected_items = items
```
#         如果没有选中任何图形项

```python
        if not items:
```
#             禁用属性面板（禁用所有控件交互）

```python
            self.setEnabled(False)
```
#             直接返回，不执行后续操作

```python
            return
```
#             return


```python
        try:
```
#             启用属性面板

```python
            self.setEnabled(True)
```
#             获取选中项列表中的第一个图形项

```python
            item = items[0]
```
#             item = items[0]


```python
            # 变换
```
#             获取图形项的边界矩形

```python
            rect = item.bounding_rect()
```
#             遍历以下旋转框和对应值的列表：

```python
            for spin, val in [
```
#                 （X 旋转框，矩形 X 坐标）、（Y 旋转框，矩形 Y 坐标）

```python
                (self._x_spin, rect.x()), (self._y_spin, rect.y()),
```
#                 （宽度旋转框，矩形宽度）、（高度旋转框，矩形高度）

```python
                (self._w_spin, rect.width()), (self._h_spin, rect.height()),
```
#             列表结束并进入循环体

```python
            ]:
```
#                 临时阻塞旋转框的信号发射（防止设置值时触发信号）

```python
                spin.blockSignals(True)
```
#                 设置旋转框的值为对应属性值

```python
                spin.setValue(val)
```
#                 恢复旋转框的信号发射

```python
                spin.blockSignals(False)
```
#                 spin.blockSignals(False)


```python
            # 不透明度
```
#             临时阻塞不透明度旋转框的信号发射

```python
            self._opacity_spin.blockSignals(True)
```
#             设置不透明度旋转框的值（将 0-1 的小数值乘以 100 转为百分比）

```python
            self._opacity_spin.setValue(item.opacity * 100)
```
#             恢复不透明度旋转框的信号发射

```python
            self._opacity_spin.blockSignals(False)
```
#             self._opacity_spin.blockSignals(False)


```python
            # 填充颜色
```
#             获取图形项样式的填充颜色

```python
            fc = item.style.fill_color
```
#             如果填充颜色不为空且有效

```python
            if fc is not None and fc.isValid():
```
#             设置填充按钮的样式表：背景色为填充颜色值、1像素 #888 边框

```python
                self._fill_btn.setStyleSheet(
```
#             样式表设置结束

```python
                    f"background-color: {fc.name()}; border: 1px solid #888;"
```
#             如果填充颜色为空或无效

```python
                )
```
#             设置填充按钮的样式表为无填充状态：背景色透明、1像素虚线 #888 边框

```python
            else:
```
#             样式表设置结束

```python
                self._fill_btn.setStyleSheet(
```
#                 self._fill_btn.setStyleSheet(

```python
                    "background-color: transparent; border: 1px dashed #888;"
```
#             更新描边颜色部分

```python
                )
```
#             获取图形项样式的描边颜色


```python
            # 描边颜色
```
#             设置描边按钮的样式表：背景色为描边颜色值、1像素 #888 边框

```python
            sc = item.style.stroke_color
```
#             样式表设置结束

```python
            if sc is not None and sc.isValid():
```
#             如果描边颜色为空或无效

```python
                self._stroke_btn.setStyleSheet(
```
#             设置描边按钮的样式表为无描边状态：背景色透明、1像素虚线 #888 边框

```python
                    f"background-color: {sc.name()}; border: 1px solid #888;"
```
#             样式表设置结束

```python
                )
```
#                 )

```python
            else:
```
#             更新描边粗细部分

```python
                self._stroke_btn.setStyleSheet(
```
#             临时阻塞描边粗细旋转框的信号发射

```python
                    "background-color: transparent; border: 1px dashed #888;"
```
#             设置描边粗细旋转框的值为图形项样式的描边粗细

```python
                )
```
#             恢复描边粗细旋转框的信号发射


```python
            # 描边粗细
```
#             更新圆角部分

```python
            self._stroke_width.blockSignals(True)
```
#             如果当前图形项是矩形项实例

```python
            self._stroke_width.setValue(item.style.stroke_width)
```
#                 启用圆角旋转框

```python
            self._stroke_width.blockSignals(False)
```
#                 临时阻塞圆角旋转框的信号发射


```python
            # 圆角
```
#                 恢复圆角旋转框的信号发射

```python
            if isinstance(item, RectangleItem):
```
#             如果当前图形项不是矩形项

```python
                self._corner_spin.setEnabled(True)
```
#                 禁用圆角旋转框（非矩形不支持圆角）

```python
                self._corner_spin.blockSignals(True)
```
#                 self._corner_spin.blockSignals(True)

```python
                self._corner_spin.setValue(item.corner_radius)
```
#             更新文字属性部分

```python
                self._corner_spin.blockSignals(False)
```
#             判断当前图形项是否为文本框架实例

```python
            else:
```
#             遍历以下文字相关控件列表：

```python
                self._corner_spin.setEnabled(False)
```
#                 字体族组合框、字体大小旋转框


```python
            # 文字属性
```
#             列表结束并进入循环体

```python
            is_text = isinstance(item, TextFrame)
```
#                 根据是否为文本项启用或禁用控件

```python
            for widget in [
```
#             for widget in [

```python
                self._font_family, self._font_size,
```
#             如果当前图形项是文本框架

```python
                self._bold_btn, self._italic_btn, self._text_edit,
```
#                 临时阻塞字体族组合框的信号发射

```python
            ]:
```
#                 设置字体族组合框的当前文本为文本项字符属性中的字体族

```python
                widget.setEnabled(is_text)
```
#                 恢复字体族组合框的信号发射


```python
            if is_text:
```
#                 临时阻塞字体大小旋转框的信号发射

```python
                self._font_family.blockSignals(True)
```
#                 设置字体大小旋转框的值为文本项字符属性中的字体大小

```python
                self._font_family.setCurrentText(item.char_attrs.font_family)
```
#                 恢复字体大小旋转框的信号发射

```python
                self._font_family.blockSignals(False)
```
#                 self._font_family.blockSignals(False)


```python
                self._font_size.blockSignals(True)
```
#                     （粗体按钮，文本项字符属性中的粗体状态）

```python
                self._font_size.setValue(item.char_attrs.font_size)
```
#                     （斜体按钮，文本项字符属性中的斜体状态）

```python
                self._font_size.blockSignals(False)
```
#                 列表结束并进入循环体


```python
                for btn, val in [
```
#                     设置按钮的选中状态为对应值

```python
                    (self._bold_btn, item.char_attrs.bold),
```
#                     恢复按钮的信号发射

```python
                    (self._italic_btn, item.char_attrs.italic),
```
#                     (self._italic_btn, item.char_attrs.italic),

```python
                ]:
```
#                 临时阻塞文本编辑框的信号发射

```python
                    btn.blockSignals(True)
```
#                 设置文本编辑框的纯文本内容为文本项的内容

```python
                    btn.setChecked(val)
```
#                 恢复文本编辑框的信号发射

```python
                    btn.blockSignals(False)
```
#         捕获所有异常，将异常对象赋值给变量 e


```python
                self._text_edit.blockSignals(True)
```
#             打印完整的异常堆栈跟踪信息

```python
                self._text_edit.setPlainText(item.contents)
```
#             打印更新选中项失败的错误信息

```python
                self._text_edit.blockSignals(False)
```
#                 self._text_edit.blockSignals(False)

```python
        except Exception as e:
```
#     定义填充按钮点击处理方法

```python
            import traceback
```
#         打开颜色选择对话框，获取用户选择的颜色

```python
            traceback.print_exc()
```
#         如果选择的颜色有效

```python
            print(f"[update_selection ERROR] {e}")
```
#             发射填充颜色变更信号，携带选择的颜色


```python
    def _on_fill_clicked(self):
```
#         样式表设置结束

```python
        color = QColorDialog.getColor()
```
#         color = QColorDialog.getColor()

```python
        if color.isValid():
```
#     定义无填充按钮点击处理方法

```python
            self.fill_color_changed.emit(color)
```
#         发射填充颜色变更信号，携带空的 QColor（表示无填充）

```python
            self._fill_btn.setStyleSheet(
```
#         更新填充按钮的样式表为无填充状态：背景色透明、1像素虚线 #888 边框

```python
                f"background-color: {color.name()}; border: 1px solid #888;"
```
#         样式表设置结束

```python
            )
```
#             )


```python
    def _on_fill_none(self):
```
#         打开颜色选择对话框，获取用户选择的颜色

```python
        self.fill_color_changed.emit(QColor())
```
#         如果选择的颜色有效

```python
        self._fill_btn.setStyleSheet(
```
#             发射描边颜色变更信号，携带选择的颜色

```python
            "background-color: transparent; border: 1px dashed #888;"
```
#             更新描边按钮的样式表：背景色为选择的颜色值、1像素 #888 边框

```python
        )
```
#         样式表设置结束


```python
    def _on_stroke_clicked(self):
```
#     定义无描边按钮点击处理方法

```python
        color = QColorDialog.getColor()
```
#         发射描边颜色变更信号，携带空的 QColor（表示无描边）

```python
        if color.isValid():
```
#         更新描边按钮的样式表为无描边状态：背景色透明、1像素虚线 #888 边框

```python
            self.stroke_color_changed.emit(color)
```
#         样式表设置结束

```python
            self._stroke_btn.setStyleSheet(
```
#             self._stroke_btn.setStyleSheet(

```python
                f"background-color: {color.name()}; border: 1px solid #888;"
```
#                 f"background-color: {color.name()}; border: 1px solid #888;"

```python
            )
```
#             )


```python
    def _on_stroke_none(self):
```
#     def _on_stroke_none(self):

```python
        self.stroke_color_changed.emit(QColor())
```
#         self.stroke_color_changed.emit(QColor())

```python
        self._stroke_btn.setStyleSheet(
```
#         self._stroke_btn.setStyleSheet(

```python
            "background-color: transparent; border: 1px dashed #888;"
```
#             "background-color: transparent; border: 1px dashed #888;"

```python
        )
```
#         )



```python
# ── 图层面板 ──────────────────────────────────────────────
```
# # ── 图层面板 ──────────────────────────────────────────────


```python
class LayersPanel(QWidget):
```
# ── 图层面板部分分隔线 ──

```python
    """图层面板 —— 1:1 对照 Adobe Illustrator 图层面板
```
#     """图层面板 —— 1:1 对照 Adobe Illustrator 图层面板


```python
    对照 PDF 功能（共 26 章）：
```
#     类文档字符串：图层面板 —— 一对一对照 Adobe Illustrator 的图层面板

```python
    第二章 - 图层面板组成：图层名称、展开箭头、可见性(眼睛)、锁定、目标圆圈、选择圆圈、彩色方块
```
#     对照 PDF 参考文档的功能列表（共 26 章）：

```python
    第三章 - 新建图层：Create New Layer 按钮 + 面板菜单 New Layer
```
#     第二章 - 图层面板组成说明：包含图层名称、展开箭头、可见性(眼睛图标)、锁定、目标圆圈、选择圆圈、彩色方块

```python
    第四章 - 重命名图层：双击图层名称
```
#     第三章 - 新建图层：通过"创建新图层"按钮或面板菜单中的"新建图层"选项

```python
    第五章 - 删除图层：点击垃圾桶图标 / 拖动到垃圾桶
```
#     第四章 - 重命名图层：双击图层名称进行编辑

```python
    第六章 - 复制图层：拖动图层到 Create New Layer 按钮
```
#     第五章 - 删除图层：点击垃圾桶图标或拖动图层到垃圾桶

```python
    第七章 - 显示与隐藏图层：眼睛图标切换
```
#     第六章 - 复制图层：拖动图层到"创建新图层"按钮

```python
    第八章 - 锁定与解锁图层：锁定区域切换
```
#     第七章 - 显示与隐藏图层：通过眼睛图标切换可见性

```python
    第九章 - 图层排序：拖动图层上下移动
```
#     第八章 - 锁定与解锁图层：通过锁定区域切换锁定状态

```python
    第十章 - 子图层：New Sublayer 创建层级结构
```
#     第九章 - 图层排序：通过拖动图层来调整上下顺序

```python
    第十一章 - 展开与折叠图层：三角箭头展开/折叠
```
#     第十章 - 子图层：通过"新建子图层"创建层级结构

```python
    第十二章 - 对象层级管理：展开图层后拖动对象调整顺序
```
#     第十一章 - 展开与折叠图层：通过三角箭头展开或折叠图层内容

```python
    第十三章 - 移动对象到其他图层：拖动彩色方块跨图层移动
```
#     第十二章 - 对象层级管理：展开图层后通过拖动对象来调整顺序

```python
    第十四章 - 选择整个图层：点击目标圆圈全选图层对象
```
#     第十三章 - 移动对象到其他图层：通过拖动彩色方块将对象跨图层移动

```python
    第十五章 - 收集到新图层：Collect in New Layer
```
#     第十四章 - 选择整个图层：点击目标圆圈全选该图层中的所有对象

```python
    第十六章 - 释放到图层：Release to Layers (Sequence/Build)
```
#     第十五章 - 收集到新图层：将选中对象收集到新建图层中

```python
    第十七章 - 合并图层：Merge Selected Layers
```
#     第十六章 - 释放到图层：将对象释放到图层（顺序模式/构建模式）

```python
    第十八章 - 拼合图稿：Flatten Artwork
```
#     第十七章 - 合并图层：合并选中的图层

```python
    第十九章 - 模板图层：Template Layer（自动锁定+降低透明度）
```
#     第十八章 - 拼合图稿：将所有图层合并为一个图层

```python
    第二十章 - 图层颜色：设置图层识别颜色
```
#     第十九章 - 模板图层：模板图层功能（自动锁定并降低透明度）

```python
    第二十一章 - 打印控制：控制图层是否参与打印
```
#     第二十章 - 图层颜色：设置图层的识别颜色标识

```python
    第二十二章 - 预览模式：Preview(正常)/Outline(轮廓)
```
#     第二十一章 - 打印控制：控制图层是否参与打印输出

```python
    第二十三章 - 查找对象：选中对象时图层面板自动定位
```
#     第二十二章 - 预览模式：预览模式(正常显示)/轮廓模式(轮廓显示)

```python
    第二十四章 - 目标对象(Target)：指定效果作用对象
```
#     第二十三章 - 查找对象：选中对象时图层面板自动定位到对应图层

```python
    第二十五章 - 图层与外观系统：图层级效果（阴影、模糊、透明度）
```
#     第二十四章 - 目标对象(Target)：指定效果作用的目标图层

```python
    第二十六章 - 图层最佳实践：命名规范、项目结构
```
#     第二十五章 - 图层与外观系统：图层级别的外观效果（阴影、模糊、透明度）


```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
#     注意事项：PyQt5 的 QWidget 子类不能使用 __slots__ 槽位机制。

```python
    """
```
#     类文档字符串结束


```python
    layer_selected = pyqtSignal(int)
```
#     定义图层选中信号（参数类型为整数，表示图层索引）

```python
    layer_visibility_changed = pyqtSignal(int, bool)
```
#     定义图层可见性变更信号（参数为图层索引、可见性布尔值）

```python
    layer_locked_changed = pyqtSignal(int, bool)
```
#     定义图层锁定状态变更信号（参数为图层索引、锁定布尔值）

```python
    layer_add_requested = pyqtSignal()
```
#     定义添加图层请求信号（无参数）

```python
    layer_remove_requested = pyqtSignal(int)
```
#     定义删除图层请求信号（参数为要删除的图层索引）

```python
    layer_duplicate_requested = pyqtSignal(int)
```
#     定义复制图层请求信号（参数为要复制的图层索引）

```python
    layer_rename_requested = pyqtSignal(int, str)
```
#     定义重命名图层请求信号（参数为图层索引、新名称字符串）

```python
    layer_reorder_requested = pyqtSignal(int, int)  # from_index, to_index
```
#     定义图层排序请求信号（参数为源索引、目标索引）

```python
    layer_merge_requested = pyqtSignal(list)  # list of indices
```
#     定义图层合并请求信号（参数为要合并的图层索引列表）

```python
    layer_flatten_requested = pyqtSignal()
```
#     定义拼合图稿请求信号（无参数，将所有图层合并）

```python
    layer_collect_requested = pyqtSignal()
```
#     定义收集到新图层请求信号（无参数）

```python
    layer_release_sequence_requested = pyqtSignal()
```
#     定义按顺序释放到图层请求信号（无参数）

```python
    layer_release_build_requested = pyqtSignal()
```
#     定义按构建方式释放到图层请求信号（无参数）

```python
    item_move_to_layer = pyqtSignal(int)  # target layer index
```
#     定义对象移动到图层信号（参数为目标图层索引）

```python
    layer_select_all_requested = pyqtSignal(int)  # 选择整个图层的所有对象
```
#     定义选择整个图层请求信号（参数为图层索引，选中该图层所有对象）

```python
    layer_target_requested = pyqtSignal(int)  # 设置目标图层（效果作用）
```
#     定义设置目标图层信号（参数为图层索引，用于指定效果作用目标）

```python
    layer_color_changed = pyqtSignal(int, QColor)  # 图层颜色变更
```
#     定义图层颜色变更信号（参数为图层索引、新的颜色值）

```python
    layer_template_changed = pyqtSignal(int, bool)  # 模板模式变更
```
#     定义模板模式变更信号（参数为图层索引、模板状态布尔值）

```python
    layer_printable_changed = pyqtSignal(int, bool)  # 打印状态变更
```
#     定义打印状态变更信号（参数为图层索引、可打印布尔值）

```python
    layer_preview_mode_changed = pyqtSignal(int, str)  # 预览模式变更
```
#     定义预览模式变更信号（参数为图层索引、预览模式字符串）

```python
    layer_opacity_changed = pyqtSignal(int, float)  # 图层不透明度变更
```
#     定义图层不透明度变更信号（参数为图层索引、不透明度浮点值）

```python
    item_order_changed = pyqtSignal(int, int, int)  # layer_index, from_pos, to_pos
```
#     定义对象排序变更信号（参数为图层索引、原位置、新位置）


```python
    LAYER_COLORS = [
```
#     定义图层颜色列表类属性（预设的图层标识颜色）：

```python
        QColor(0, 120, 215),    # 蓝色
```
#         蓝色（RGB 值 0, 120, 215）

```python
        QColor(220, 50, 50),    # 红色
```
#         红色（RGB 值 220, 50, 50）

```python
        QColor(0, 150, 80),     # 绿色
```
#         绿色（RGB 值 0, 150, 80）

```python
        QColor(255, 140, 0),    # 橙色
```
#         橙色（RGB 值 255, 140, 0）

```python
        QColor(150, 50, 200),   # 紫色
```
#         紫色（RGB 值 150, 50, 200）

```python
        QColor(0, 180, 180),    # 青色
```
#         青色（RGB 值 0, 180, 180）

```python
        QColor(200, 100, 150),  # 粉色
```
#         粉色（RGB 值 200, 100, 150）

```python
        QColor(139, 90, 43),    # 棕色
```
#         棕色（RGB 值 139, 90, 43）

```python
    ]
```
#     图层颜色列表结束


```python
    def __init__(self, parent=None):
```
#     定义初始化方法（接收自身引用 self、父部件参数 parent：默认为空）

```python
        super().__init__(parent)
```
#         调用父类 QWidget 的初始化方法，传入父部件参数

```python
        self._current_index = 0
```
#         定义私有属性 _current_index：当前选中图层的索引，默认为 0

```python
        self._layers_data: list[Layer] = []
```
#         定义私有属性 _layers_data：图层数据列表，初始为空列表

```python
        self._editing_index = -1  # 正在编辑名称的图层索引
```
#         定义私有属性 _editing_index：正在编辑名称的图层索引，-1 表示未在编辑

```python
        self._trash_bin: QPushButton | None = None  # 垃圾桶按钮（拖拽删除）
```
#         定义私有属性 _trash_bin：垃圾桶按钮引用，初始为空（用于拖拽删除功能）

```python
        self._init_ui()
```
#         调用界面初始化方法


```python
    def _init_ui(self):
```
#     定义私有界面初始化方法（构建图层面板界面）

```python
        layout = QVBoxLayout(self)
```
#         创建垂直布局管理器，以自身为父部件

```python
        layout.setContentsMargins(4, 4, 4, 4)
```
#         设置布局内容边距（上、下、左、右各 4 像素）

```python
        layout.setSpacing(4)
```
#         设置布局中控件之间的间距为 4 像素


```python
        # ── 标题栏 ──
```
#         ── 标题栏区域注释 ──

```python
        title_layout = QHBoxLayout()
```
#         创建标题栏水平布局

```python
        title_layout.addWidget(QLabel("图层"))
```
#         在标题栏中添加"图层"标签

```python
        title_layout.addStretch()
```
#         在标题栏末尾添加弹性拉伸空间（将标签推到左侧）


```python
        # 图层菜单按钮
```
#         图层菜单按钮注释

```python
        self._menu_btn = QPushButton("☰")
```
#         创建菜单按钮（显示汉堡菜单图标 ☰）

```python
        self._menu_btn.setFixedSize(24, 24)
```
#         设置菜单按钮固定尺寸为 24×24 像素

```python
        self._menu_btn.setToolTip("图层菜单")
```
#         设置菜单按钮提示文本为"图层菜单"

```python
        self._menu_btn.clicked.connect(self._show_layer_menu)
```
#         连接菜单按钮点击信号到显示图层菜单方法

```python
        title_layout.addWidget(self._menu_btn)
```
#         将菜单按钮添加到标题栏布局中


```python
        layout.addLayout(title_layout)
```
#         layout.addLayout(title_layout)


```python
        # ── 图层树（使用 QTreeWidget 支持层级、拖拽、彩色方块） ──
```
#         创建树控件实例（用于显示图层层级结构）

```python
        self._tree = QTreeWidget()
```
#         隐藏树控件的表头

```python
        self._tree.setHeaderHidden(True)
```
#         设置树控件缩进距离为 20 像素

```python
        self._tree.setIndentation(20)
```
#         设置根节点显示展开/折叠装饰箭头

```python
        self._tree.setRootIsDecorated(True)
```
#         启用树控件展开/折叠动画效果

```python
        self._tree.setAnimated(True)
```
#         启用树控件拖拽功能

```python
        self._tree.setDragEnabled(True)
```
#         启用树控件接收拖放功能

```python
        self._tree.setAcceptDrops(True)
```
#         启用拖放指示器显示

```python
        self._tree.setDropIndicatorShown(True)
```
#         设置拖放模式为内部移动（仅在同一控件内移动）

```python
        self._tree.setDragDropMode(self._tree.InternalMove)
```
#         设置选择模式为扩展选择（支持多选）

```python
        self._tree.setSelectionMode(self._tree.ExtendedSelection)
```
#         设置上下文菜单策略为自定义菜单（允许右键菜单）

```python
        self._tree.setContextMenuPolicy(Qt.CustomContextMenu)
```
#         连接自定义上下文菜单请求信号到右键菜单处理方法

```python
        self._tree.customContextMenuRequested.connect(self._on_context_menu)
```
#         连接当前项变更信号到项目变更处理方法

```python
        self._tree.currentItemChanged.connect(self._on_item_changed)
```
#         连接项目双击信号到双击处理方法

```python
        self._tree.itemDoubleClicked.connect(self._on_item_double_clicked)
```
#         连接项目状态变更信号到状态变更处理方法

```python
        self._tree.itemChanged.connect(self._on_item_changed_flag)
```
#         连接模型行移动信号到行移动处理方法（用于拖拽排序）

```python
        self._tree.model().rowsMoved.connect(self._on_rows_moved)
```
#         点击目标圆圈全选图层功能（对照第十四章）

```python
        # 点击目标圆圈全选图层（第十四章）
```
#         连接项目点击信号到项目点击处理方法

```python
        self._tree.itemClicked.connect(self._on_item_clicked)
```
#         将树控件添加到主布局中

```python
        layout.addWidget(self._tree)
```
#         layout.addWidget(self._tree)


```python
        # ── 底部按钮栏（对照 Ai：Create New Layer / 垃圾桶 / 子图层 / 收集） ──
```
#         创建底部水平布局

```python
        bottom_layout = QHBoxLayout()
```
#         设置底部布局中控件间距为 4 像素

```python
        bottom_layout.setSpacing(4)
```
#         bottom_layout.setSpacing(4)


```python
        # Create New Layer 按钮（第三章方法1 — 新建图层，第六章 — 拖拽复制）
```
#         创建新建图层按钮（显示"+"号）

```python
        self._add_btn = QPushButton("+")
```
#         设置新建按钮固定尺寸为 28×28 像素

```python
        self._add_btn.setFixedSize(28, 28)
```
#         设置新建按钮提示文本（创建新图层/拖拽图层到此按钮可复制）

```python
        self._add_btn.setToolTip("创建新图层\n拖拽图层到此按钮可复制")
```
#         连接新建按钮点击信号直接发射添加图层请求信号

```python
        self._add_btn.clicked.connect(self.layer_add_requested.emit)
```
#         设置新建按钮接受拖放操作

```python
        self._add_btn.setAcceptDrops(True)
```
#         将新建按钮的拖入事件替换为自定义拖入处理方法

```python
        self._add_btn.dragEnterEvent = self._on_add_btn_drag_enter
```
#         将新建按钮的拖动事件替换为自定义拖动处理方法

```python
        self._add_btn.dragMoveEvent = self._on_add_btn_drag_move
```
#         将新建按钮的放下事件替换为自定义放下处理方法

```python
        self._add_btn.dropEvent = self._on_add_btn_drop
```
#         将新建按钮添加到底部布局中

```python
        bottom_layout.addWidget(self._add_btn)
```
#         bottom_layout.addWidget(self._add_btn)


```python
        # 垃圾桶按钮（第五章 — 删除图层，支持拖拽到垃圾桶删除）
```
#         创建垃圾桶按钮（显示垃圾桶图标 🗑）

```python
        self._trash_bin = QPushButton("🗑")
```
#         设置垃圾桶按钮固定尺寸为 28×28 像素

```python
        self._trash_bin.setFixedSize(28, 28)
```
#         设置垃圾桶按钮提示文本（删除选定图层/拖拽图层到此按钮可删除）

```python
        self._trash_bin.setToolTip("删除选定图层\n拖拽图层到此按钮可删除")
```
#         连接垃圾桶按钮点击信号到匿名回调：发射删除图层请求信号，携带当前图层索引

```python
        self._trash_bin.clicked.connect(
```
#         匿名回调函数结束

```python
            lambda: self.layer_remove_requested.emit(self._current_index),
```
#         设置垃圾桶按钮接受拖放操作

```python
        )
```
#         将垃圾桶按钮的拖入事件替换为自定义拖入处理方法

```python
        self._trash_bin.setAcceptDrops(True)
```
#         将垃圾桶按钮的拖动事件替换为自定义拖动处理方法

```python
        self._trash_bin.dragEnterEvent = self._on_trash_drag_enter
```
#         将垃圾桶按钮的放下事件替换为自定义放下处理方法

```python
        self._trash_bin.dragMoveEvent = self._on_trash_drag_move
```
#         将垃圾桶按钮添加到底部布局中

```python
        self._trash_bin.dropEvent = self._on_trash_drop
```
#         self._trash_bin.dropEvent = self._on_trash_drop

```python
        bottom_layout.addWidget(self._trash_bin)
```
#         在底部布局中添加 8 像素的间距


```python
        bottom_layout.addSpacing(8)
```
#         创建"子图层"按钮


```python
        self._sublayer_btn = QPushButton("子图层")
```
#         连接子图层按钮点击信号到添加子图层处理方法

```python
        self._sublayer_btn.setToolTip("新建子图层（第十章）")
```
#         将子图层按钮添加到底部布局中

```python
        self._sublayer_btn.clicked.connect(self._on_add_sublayer)
```
#         self._sublayer_btn.clicked.connect(self._on_add_sublayer)

```python
        bottom_layout.addWidget(self._sublayer_btn)
```
#         创建"收集"按钮


```python
        self._collect_btn = QPushButton("收集")
```
#         连接收集按钮点击信号直接发射收集请求信号

```python
        self._collect_btn.setToolTip("收集到新图层（第十五章）")
```
#         将收集按钮添加到底部布局中

```python
        self._collect_btn.clicked.connect(self.layer_collect_requested.emit)
```
#         self._collect_btn.clicked.connect(self.layer_collect_requested.emit)

```python
        bottom_layout.addWidget(self._collect_btn)
```
#         将底部布局添加到主布局中


```python
        layout.addLayout(bottom_layout)
```
#         设置图层面板样式表（暗色主题）：


```python
        self.setStyleSheet("""
```
#         树控件项目样式：3×2 像素内边距、1像素 #3a3a3a 底部边框

```python
            QTreeWidget { background-color: #2d2d2d; color: #ddd; border: 1px solid #555; outline: none; }
```
#         树控件选中项目样式：蓝色 #0d6efd 背景、白色文字

```python
            QTreeWidget::item { padding: 3px 2px; border-bottom: 1px solid #3a3a3a; }
```
#         树控件悬停项目样式：#3a3a3a 背景色

```python
            QTreeWidget::item:selected { background-color: #0d6efd; color: white; }
```
#         树控件分支样式（有子项且无兄弟项的关闭状态）

```python
            QTreeWidget::item:hover { background-color: #3a3a3a; }
```
#         树控件分支样式（有子项且有兄弟项的关闭状态）：无边框图像

```python
            QTreeWidget::branch:has-children:!has-siblings:closed,
```
#         按钮样式：#4a4a4a 背景色、#ddd 文字色、#555 边框、3像素圆角、粗体、2×6像素内边距

```python
            QTreeWidget::branch:closed:has-children:has-siblings { border-image: none; }
```
#         按钮悬停时背景色为 #5a5a5a

```python
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; border-radius: 3px; font-weight: bold; padding: 2px 6px; }
```
#         垃圾桶按钮悬停样式：红色 #dc3545 背景和边框

```python
            QPushButton:hover { background-color: #5a5a5a; }
```
#         新建按钮悬停样式：蓝色 #0d6efd 背景和边框

```python
            QPushButton#trash_hover { background-color: #dc3545; border-color: #dc3545; }
```
#         单行文本框样式：#3c3c3c 背景、#ddd 文字色、蓝色 #0d6efd 边框、2像素内边距

```python
            QPushButton#add_hover { background-color: #0d6efd; border-color: #0d6efd; }
```
#         样式表字符串结束

```python
            QLineEdit { background-color: #3c3c3c; color: #ddd; border: 1px solid #0d6efd; padding: 2px; }
```
#             QLineEdit { background-color: #3c3c3c; color: #ddd; border: 1px solid #0d6efd; padding: 2px; }

```python
        """)
```
#     ── 更新图层列表部分注释 ──


```python
    # ── 更新图层列表 ──
```
#     定义更新图层列表方法（接收自身引用、图层数据列表、当前活动图层索引参数）


```python
    def update_layers(self, layers: list[Layer], active_index: int):
```
#         保存传入的图层数据列表到私有属性

```python
        """更新图层树，显示图层及子图层的层级结构（对照第二章图层面板组成）"""
```
#         临时阻塞树控件的所有信号发射

```python
        self._layers_data = layers
```
#         清空树控件中的所有项目

```python
        self._tree.blockSignals(True)
```
#         self._tree.blockSignals(True)

```python
        self._tree.clear()
```
#         遍历图层列表，同时获取索引和图层对象


```python
        for i, layer in enumerate(layers):
```
#             将树节点项添加为树的顶层项

```python
            item = self._create_layer_item(layer, i)
```
#             如果当前索引等于活动图层索引

```python
            self._tree.addTopLevelItem(item)
```
#                 将该节点设为当前选中项

```python
            if i == active_index:
```
#             设置展开/折叠状态（对照第十一章）

```python
                self._tree.setCurrentItem(item)
```
#             根据图层的展开属性设置节点的展开/折叠状态

```python
            # 展开/折叠（第十一章）
```
#             # 展开/折叠（第十一章）

```python
            item.setExpanded(layer.expanded)
```
#         恢复树控件的信号发射


```python
        self._tree.blockSignals(False)
```
#         查找对象功能（对照第二十三章）：选中对象时图层面板自动定位到对应图层

```python
        self._current_index = active_index
```
#         如果活动索引在有效范围内


```python
        # 第二十三章 - 查找对象：选中对象时图层面板自动定位到对应图层
```
#             如果活动节点项存在

```python
        if 0 <= active_index < len(layers):
```
#                 滚动树控件使活动节点项居中显示

```python
            active_item = self._tree.topLevelItem(active_index)
```
#             active_item = self._tree.topLevelItem(active_index)

```python
            if active_item:
```
#     定义创建图层树节点方法（接收自身引用、图层对象、索引参数，返回树节点项）

```python
                self._tree.scrollToItem(active_item, QTreeWidget.PositionAtCenter)
```
#         方法文档字符串：创建图层树节点，一对一对照 Ai 图层面板


```python
    def _create_layer_item(self, layer: Layer, index: int) -> QTreeWidgetItem:
```
#         1. 展开箭头 (▶) —— 展开/折叠图层内容（对照第十一章）

```python
        """创建图层树节点，1:1 对照 Ai 图层面板
```
#         2. 眼睛图标 (👁) —— 可见性控制（对照第七章）


```python
        Ai 图层面板结构（从左到右）：
```
#         4. 目标圆圈 (◎) —— 效果作用目标（对照第二十四章）

```python
        1. 展开箭头 (▶) — 展开/折叠图层内容（第十一章）
```
#         5. 图层颜色方块 —— 图层标识颜色（对照第二十章）

```python
        2. 眼睛图标 (👁) — 可见性（第七章）
```
#         6. 图层名称 —— 双击可重命名（对照第四章）

```python
        3. 锁定区域 (🔒) — 锁定状态（第八章）
```
#         方法文档字符串结束

```python
        4. 目标圆圈 (◎) — 效果作用目标（第二十四章）
```
#         可见性图标注释（对照第七章）

```python
        5. 图层颜色方块 — 标识图层（第二十章）
```
#         设置眼睛图标：可见时显示 👁，不可见时留空（模拟 Ai 行为）

```python
        6. 图层名称 — 双击可重命名（第四章）
```
#         锁定图标注释（对照第八章）

```python
        """
```
#         设置锁定图标：锁定时显示 🔒，未锁定时留空

```python
        # 可见性图标（第七章）
```
#         模板图标注释（对照第十九章）

```python
        eye = "👁" if layer.visible else "  "  # 不可见时留空（Ai 行为）
```
#         设置模板图标：模板图层显示 📐，否则留空格

```python
        # 锁定图标（第八章）
```
#         预览模式标识注释（对照第二十二章）

```python
        lock = "🔒" if layer.locked else "  "
```
#         设置预览模式标识：轮廓模式显示 ◉，预览模式显示 ◎

```python
        # 模板图标（第十九章）
```
#         打印状态注释（对照第二十一章）—— 不可打印用斜体标识

```python
        template = "📐" if layer.is_template else " "
```
#         设置打印标识：可打印时为空，不可打印时显示 ✕

```python
        # 预览模式标识（第二十二章）
```
#         获取图层名称

```python
        preview_indicator = "◉" if layer.preview_mode == "outline" else "◎"
```
#         显示对象数量注释

```python
        # 打印状态（第二十一章）— 不可打印用斜体标识
```
#         获取图层中的对象数量

```python
        print_indicator = "" if layer.printable else "✕ "
```
#         获取图层中的子图层数量


```python
        name = layer.name
```
#         生成子图层数量详情文本（有子图层时显示方括号内的数量，否则为空）


```python
        # 显示对象数量
```
#         拼合完整的显示文本字符串

```python
        item_count = len(layer.items)
```
#         创建树节点项，显示文本为拼合的字符串

```python
        sub_count = len(layer.sublayers)
```
#         将图层索引存储到节点数据（角色：用户角色）

```python
        detail = f" ({item_count})" if item_count > 0 else ""
```
#         将节点类型"layer"存储到节点数据（角色：用户角色+1）

```python
        sub_detail = f" [{sub_count}]" if sub_count > 0 else ""
```
#         将图层 ID 存储到节点数据（角色：用户角色+2）


```python
        # 拼合显示文本：眼睛 锁 目标 名称 数量
```
#         # 拼合显示文本：眼睛 锁 目标 名称 数量

```python
        display_text = f"{eye}{lock}{preview_indicator} {print_indicator}{name}{detail}{sub_detail}"
```
#         图层颜色标识注释（对照第二十章）—— 路径边框颜色


```python
        item = QTreeWidgetItem([display_text])
```
#             将节点的前景文字颜色设为图层颜色

```python
        item.setData(0, Qt.UserRole, index)
```
#         如果图层是模板图层

```python
        item.setData(0, Qt.UserRole + 1, "layer")
```
#             模板图层灰色显示（对照第十九章）

```python
        item.setData(0, Qt.UserRole + 2, layer.id)
```
#             将节点的前景文字颜色设为灰色（模板图层标识）

```python
        item.setData(0, Qt.UserRole + 4, layer.color.name() if layer.color else "")  # 彩色方块数据
```
#         如果图层不可打印


```python
        # 图层颜色标识（第二十章）— 路径边框颜色
```
#             获取节点的当前字体

```python
        if layer.color:
```
#             将字体设为斜体

```python
            item.setForeground(0, layer.color)
```
#             将斜体字体应用到节点

```python
        if layer.is_template:
```
#         如果图层预览模式为轮廓模式

```python
            # 模板图层灰色显示（第十九章）
```
#             轮廓模式用不同背景色提示（对照第二十二章）

```python
            item.setForeground(0, QColor(128, 128, 128))
```
#             将节点的背景色设为深褐色（轮廓模式标识）

```python
        if not layer.printable:
```
#         if not layer.printable:

```python
            # 不打印的图层用斜体显示（第二十一章）
```
#         子图层注释（对照第十章）

```python
            font = item.font(0)
```
#         遍历图层的子图层列表，同时获取子图层索引和子图层对象

```python
            font.setItalic(True)
```
#             为当前子图层创建子节点项

```python
            item.setFont(0, font)
```
#             将子节点项添加为当前图层节点的子节点

```python
        if layer.preview_mode == "outline":
```
#         if layer.preview_mode == "outline":

```python
            # 轮廓模式用不同背景色提示（第二十二章）
```
#         对象列表注释（展开图层可查看路径、文字、图像等，对照第十一、十二章）

```python
            item.setBackground(0, QColor(50, 45, 40))
```
#         如果图层处于展开状态且包含对象


```python
        # 子图层（第十章）
```
#                 获取对象类型名称（去掉"Item"后缀）

```python
        for si, sub in enumerate(layer.sublayers):
```
#                 获取对象名称（无名称时用尖括号包裹的类型名代替）

```python
            sub_item = self._create_sublayer_item(sub, index, si)
```
#                 对象锁定图标注释

```python
            item.addChild(sub_item)
```
#                 设置对象锁定图标：锁定时显示 🔒 加空格，否则为空


```python
        # 对象列表（展开图层可查看路径、文字、图像等 — 第十一章、第十二章）
```
#                 调用方法获取对象对应的类型图标

```python
        if layer.expanded and layer.items:
```
#                 创建对象树节点项（前缀 4 个空格缩进 + 锁定图标 + 类型图标 + 对象名称）

```python
            for oi, obj in enumerate(layer.items):
```
#                 将对象索引存储到节点数据

```python
                obj_type = obj.item_type.replace("Item", "")
```
#                 将节点类型"object"存储到节点数据

```python
                obj_name = obj.name or f"<{obj_type}>"
```
#                 将对象 ID 存储到节点数据


```python
                # 对象锁定图标
```
#                 对象使用图层颜色注释（对照第二十章）—— 彩色方块

```python
                obj_lock = "🔒 " if obj.locked else ""
```
#                 如果图层设置了颜色

```python
                # 对象类型图标
```
#                     将对象节点的前景文字颜色设为带透明度的图层颜色

```python
                type_icon = self._get_item_type_icon(obj)
```
#                 对象可拖拽排序注释（对照第十二章——对象层级管理）


```python
                obj_item = QTreeWidgetItem([f"    {obj_lock}{type_icon} {obj_name}"])
```
#                 将对象节点添加为图层节点的子节点

```python
                obj_item.setData(0, Qt.UserRole, oi)
```
#                 obj_item.setData(0, Qt.UserRole, oi)

```python
                obj_item.setData(0, Qt.UserRole + 1, "object")
```
#         图层项可拖拽注释（对照第九章——图层排序）

```python
                obj_item.setData(0, Qt.UserRole + 2, obj.id)
```
#         为图层节点启用拖拽标志

```python
                obj_item.setData(0, Qt.UserRole + 3, index)  # 父图层索引
```
#         返回创建好的图层树节点项


```python
                # 对象使用图层颜色（第二十章）— 彩色方块
```
#     静态方法装饰器（不依赖实例属性）

```python
                if layer.color:
```
#     定义获取对象类型图标的私有静态方法（接收对象参数，返回图标字符串）

```python
                    obj_item.setForeground(0, QColor(
```
#         方法文档字符串：获取对象类型图标（对照第十一章）

```python
                        layer.color.red(), layer.color.green(),
```
#         从上层核心图形模块导入各图形项类型

```python
                        layer.color.blue(), 180
```
#         使用模式匹配匹配对象类型：

```python
                    ))
```
#             如果对象是路径项：返回铅笔图标 ✏（路径）


```python
                # 对象可拖拽排序（第十二章 — 对象层级管理）
```
#             如果对象是椭圆项：返回椭圆图标 ⬭（椭圆）

```python
                obj_item.setFlags(obj_item.flags() | Qt.ItemIsDragEnabled)
```
#             如果对象是文本框架：返回字母 T（文字）


```python
                item.addChild(obj_item)
```
#             如果对象不匹配以上任何类型：返回实心圆点图标 ●（默认）


```python
        # 图层项可拖拽（第九章 — 图层排序）
```
#     定义创建子图层树节点方法（接收自身引用、子图层对象、父图层索引、子图层索引参数，返回树节点项）

```python
        item.setFlags(item.flags() | Qt.ItemIsDragEnabled)
```
#         方法文档字符串：创建子图层树节点（对照第十章）


```python
        return item
```
#         设置子图层锁定图标：锁定时显示 🔒，未锁定时留空


```python
    @staticmethod
```
#         创建子图层树节点项（显示文本：眼睛图标 + 锁定图标 + 目标圆圈 + 子图层名称）

```python
    def _get_item_type_icon(obj) -> str:
```
#         将子图层索引存储到节点数据

```python
        """获取对象类型图标（第十一章）"""
```
#         将节点类型"sublayer"存储到节点数据

```python
        from ..core.graphics import PathItem, RectangleItem, EllipseItem, TextFrame, GroupItem
```
#         将子图层 ID 存储到节点数据

```python
        match obj:
```
#         将父图层索引存储到节点数据

```python
            case PathItem():
```
#         如果子图层设置了颜色

```python
                return "✏"  # 路径
```
#             将节点的前景文字颜色设为子图层颜色

```python
            case RectangleItem():
```
#         子图层也可拖拽排序注释

```python
                return "▬"  # 矩形
```
#         为子图层节点启用拖拽标志

```python
            case EllipseItem():
```
#         返回创建好的子图层树节点项

```python
                return "⬭"  # 椭圆
```
#                 return "⬭"  # 椭圆

```python
            case TextFrame():
```
#     ── 事件处理部分注释 ──

```python
                return "T"  # 文字
```
#                 return "T"  # 文字

```python
            case GroupItem():
```
#     定义树节点项变更处理方法（接收当前节点、前一节点参数）

```python
                return "📁"  # 群组
```
#         如果当前节点为空

```python
            case _:
```
#             直接返回

```python
                return "●"  # 默认
```
#         从当前节点数据中获取节点类型


```python
    def _create_sublayer_item(self, sublayer: Layer, parent_idx: int, sub_idx: int) -> QTreeWidgetItem:
```
#             获取图层索引

```python
        """创建子图层树节点（第十章）"""
```
#             如果索引不为空

```python
        eye = "👁" if sublayer.visible else "  "
```
#                 更新当前图层索引

```python
        lock = "🔒" if sublayer.locked else "  "
```
#                 发射图层选中信号

```python
        preview_indicator = "◎"
```
#         如果节点类型为"sublayer"（子图层）


```python
        item = QTreeWidgetItem([f"{eye}{lock}{preview_indicator} {sublayer.name}"])
```
#             如果父图层索引不为空

```python
        item.setData(0, Qt.UserRole, sub_idx)
```
#                 更新当前图层索引为父图层索引

```python
        item.setData(0, Qt.UserRole + 1, "sublayer")
```
#                 发射图层选中信号（携带父图层索引）

```python
        item.setData(0, Qt.UserRole + 2, sublayer.id)
```
#         item.setData(0, Qt.UserRole + 2, sublayer.id)

```python
        item.setData(0, Qt.UserRole + 3, parent_idx)
```
#     定义节点双击处理方法（接收树节点项、列号参数）


```python
        if sublayer.color:
```
#         从节点数据中获取节点类型

```python
            item.setForeground(0, sublayer.color)
```
#         如果节点类型为图层或子图层


```python
        # 子图层也可拖拽排序
```
#             调用启动重命名方法

```python
        item.setFlags(item.flags() | Qt.ItemIsDragEnabled)
```
#         item.setFlags(item.flags() | Qt.ItemIsDragEnabled)


```python
        return item
```
#         方法文档字符串：启动内联重命名


```python
    # ── 事件处理 ──
```
#         定义当前文本变量，初始为空字符串


```python
    def _on_item_changed(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
```
#             获取当前图层的名称

```python
        if current is None:
```
#         如果节点类型为子图层

```python
            return
```
#             从节点数据中获取父图层索引

```python
        item_type = current.data(0, Qt.UserRole + 1)
```
#             如果父图层索引有效

```python
        if item_type == "layer":
```
#                 获取父图层对象

```python
            index = current.data(0, Qt.UserRole)
```
#                 如果子图层索引在有效范围内

```python
            if index is not None:
```
#                     获取当前子图层的名称

```python
                self._current_index = index
```
#                 self._current_index = index

```python
                self.layer_selected.emit(index)
```
#         创建单行文本编辑框（以当前名称为初始文本，父部件为树控件）

```python
        elif item_type == "sublayer":
```
#         将焦点设置到编辑框

```python
            parent_idx = current.data(0, Qt.UserRole + 3)
```
#         选中编辑框中的全部文本

```python
            if parent_idx is not None:
```
#         将编辑框设置为树节点项的内联编辑控件（第 0 列）

```python
                self._current_index = parent_idx
```
#         记录当前正在编辑的索引

```python
                self.layer_selected.emit(parent_idx)
```
#                 self.layer_selected.emit(parent_idx)


```python
    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
```
#             获取编辑框中的文本并去除首尾空格

```python
        """双击重命名图层（PDF 六）"""
```
#             开始异常捕获块

```python
        item_type = item.data(0, Qt.UserRole + 1)
```
#             检查节点项是否仍然有效

```python
        if item_type in ("layer", "sublayer"):
```
#             如果节点项不在树控件中（已被移除）

```python
            index = item.data(0, Qt.UserRole)
```
#                 直接返回

```python
            self._start_rename(item, item_type, index)
```
#             移除节点项的内联编辑控件


```python
    def _start_rename(self, item: QTreeWidgetItem, item_type: str, index: int):
```
#                 直接返回

```python
        """启动内联重命名"""
```
#             如果新名称非空且与原名称不同

```python
        from PyQt5.QtWidgets import QLineEdit
```
#                 如果节点类型为图层

```python
        current_text = ""
```
#                     发射图层重命名请求信号（携带索引和新名称）

```python
        if item_type == "layer" and index < len(self._layers_data):
```
#                 如果节点类型为子图层

```python
            current_text = self._layers_data[index].name
```
#                     发射子图层重命名请求信号（使用负索引标识子图层）

```python
        elif item_type == "sublayer":
```
#         elif item_type == "sublayer":

```python
            parent_idx = item.data(0, Qt.UserRole + 3)
```
#         连接编辑框回车键信号到完成重命名函数

```python
            if parent_idx is not None and parent_idx < len(self._layers_data):
```
#         连接编辑完成信号到空操作（防止重复触发 finish_rename）

```python
                parent = self._layers_data[parent_idx]
```
#                 parent = self._layers_data[parent_idx]

```python
                if index < len(parent.sublayers):
```
#     定义节点状态变更处理方法（接收树节点项、列号参数）

```python
                    current_text = parent.sublayers[index].name
```
#         方法文档字符串：项目状态改变处理（预留接口）


```python
        editor = QLineEdit(current_text, self._tree)
```
#         editor = QLineEdit(current_text, self._tree)

```python
        editor.setFocus()
```
#     定义行移动处理方法（接收父节点、起始行、结束行、目标父节点、目标行参数）

```python
        editor.selectAll()
```
#         方法文档字符串：拖拽排序图层（对照第九章）或对象排序（对照第十二章）

```python
        self._tree.setItemWidget(item, 0, editor)
```
#         如果起始行与目标行不同（发生了实际移动）

```python
        self._editing_index = index
```
#             判断是图层排序还是对象排序


```python
        def finish_rename():
```
#             如果节点项存在

```python
            new_name = editor.text().strip()
```
#                 从节点数据中获取节点类型

```python
            try:
```
#                 如果节点类型为图层

```python
                # 检查 item 是否仍然有效
```
#                     发射图层排序请求信号（源位置、目标位置）

```python
                if item not in self._tree.findItems("", Qt.MatchContains | Qt.MatchRecursive, 0):
```
#                 如果节点类型为对象

```python
                    return
```
#                     对象层级管理（对照第十二章）

```python
                self._tree.removeItemWidget(item, 0)
```
#                     从节点数据中获取父图层索引

```python
            except RuntimeError:
```
#                     如果父图层索引不为空

```python
                return
```
#                         发射对象排序变更信号（图层索引、原位置、新位置）

```python
            if new_name and new_name != current_text:
```
#             if new_name and new_name != current_text:

```python
                if item_type == "layer":
```
#     定义节点点击处理方法（接收树节点项、列号参数）

```python
                    self.layer_rename_requested.emit(index, new_name)
```
#         方法文档字符串：点击图层项处理

```python
                elif item_type == "sublayer":
```
#         第十四章 - 选择整个图层：点击目标圆圈 ◎ 区域全选图层对象

```python
                    self.layer_rename_requested.emit(-(index + 1), new_name)
```
#         第二十四章 - 目标对象：点击目标圆圈设置效果作用目标


```python
        editor.returnPressed.connect(finish_rename)
```
#         从节点数据中获取节点类型

```python
        editor.editingFinished.connect(lambda: None)  # 防止重复触发
```
#         如果节点类型为图层


```python
    def _on_item_changed_flag(self, item: QTreeWidgetItem, column: int):
```
#             如果索引不为空

```python
        """项目状态改变（预留）"""
```
#                 检查点击位置是否在目标圆圈区域

```python
        pass
```
#                 获取节点的显示文本


```python
    def _on_rows_moved(self, parent, start, end, dest, row):
```
#                 发射设置目标图层信号（携带图层索引）

```python
        """拖拽排序图层（第九章）或对象排序（第十二章）"""
```
#         """拖拽排序图层（第九章）或对象排序（第十二章）"""

```python
        if start != row:
```
#     ── 拖拽到垃圾桶删除功能注释（对照第五章方法二） ──

```python
            # 判断是图层排序还是对象排序
```
#             # 判断是图层排序还是对象排序

```python
            item = self._tree.topLevelItem(start) if start < self._tree.topLevelItemCount() else None
```
#     定义垃圾桶拖入事件处理方法（接收拖拽事件参数）

```python
            if item:
```
#         方法文档字符串：拖拽到垃圾桶时的视觉反馈

```python
                item_type = item.data(0, Qt.UserRole + 1)
```
#         如果垃圾桶按钮存在

```python
                if item_type == "layer":
```
#         设置垃圾桶按钮的高亮样式表：红色背景 #dc3545、白色文字、红色边框

```python
                    self.layer_reorder_requested.emit(start, row)
```
#         样式表字符串结束

```python
                elif item_type == "object":
```
#                 elif item_type == "object":

```python
                    # 对象层级管理（第十二章）
```
#     定义垃圾桶拖动事件处理方法（接收拖拽事件参数）

```python
                    layer_idx = item.data(0, Qt.UserRole + 3)
```
#         接受拖拽事件（允许继续拖动）

```python
                    if layer_idx is not None:
```
#                     if layer_idx is not None:

```python
                        self.item_order_changed.emit(layer_idx, start, row)
```
#     定义垃圾桶放下事件处理方法（接收拖拽事件参数）


```python
    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
```
#         如果垃圾桶按钮存在

```python
        """点击图层项处理
```
#             清除垃圾桶按钮的高亮样式（恢复正常外观）


```python
        第十四章 - 选择整个图层：点击目标圆圈 ◎ 区域全选图层对象
```
#         获取当前图层索引

```python
        第二十四章 - 目标对象：点击目标圆圈设置效果目标
```
#         如果索引在有效范围内

```python
        """
```
#             发射删除图层请求信号

```python
        item_type = item.data(0, Qt.UserRole + 1)
```
#         接受拖放事件

```python
        if item_type == "layer":
```
#         if item_type == "layer":

```python
            index = item.data(0, Qt.UserRole)
```
#     ── 拖拽到新建按钮复制功能注释（对照第六章） ──

```python
            if index is not None:
```
#             if index is not None:

```python
                # 检查点击位置是否在目标圆圈区域
```
#     定义新建按钮拖入事件处理方法（接收拖拽事件参数）

```python
                text = item.text(0)
```
#         方法文档字符串：拖拽到新建按钮时的视觉反馈

```python
                # 目标圆圈 ◎ 在文本中，点击即表示选择目标图层
```
#         如果新建按钮存在

```python
                self.layer_target_requested.emit(index)
```
#         设置新建按钮的高亮样式表：蓝色背景 #0d6efd、白色文字、蓝色边框


```python
    # ── 拖拽到垃圾桶删除（第五章方法2） ──
```
#     # ── 拖拽到垃圾桶删除（第五章方法2） ──


```python
    def _on_trash_drag_enter(self, event):
```
#         接受拖拽事件

```python
        """拖拽到垃圾桶时的视觉反馈"""
```
#         """拖拽到垃圾桶时的视觉反馈"""

```python
        if self._trash_bin:
```
#     定义新建按钮放下事件处理方法（接收拖拽事件参数）

```python
            self._trash_bin.setStyleSheet("""
```
#         方法文档字符串：拖拽图层到新建按钮复制（对照第六章）

```python
                QPushButton { background-color: #dc3545; color: white;
```
#         如果新建按钮存在

```python
                border: 2px solid #ff4444; border-radius: 3px; font-weight: bold; }
```
#             清除新建按钮的高亮样式

```python
            """)
```
#         获取当前图层索引


```python
    def _on_trash_drag_move(self, event):
```
#             发射复制图层请求信号

```python
        event.accept()
```
#         接受拖放事件


```python
    def _on_trash_drop(self, event):
```
#     ── 右键菜单部分注释（完整对照 Ai 图层面板菜单） ──

```python
        """拖拽图层到垃圾桶删除（第五章方法2）"""
```
#         """拖拽图层到垃圾桶删除（第五章方法2）"""

```python
        if self._trash_bin:
```
#     定义右键菜单处理方法（接收位置坐标参数）

```python
            self._trash_bin.setStyleSheet("")
```
#         方法文档字符串：右键菜单——完整的图层操作

```python
        # 获取当前选中的图层
```
#         对照 Ai 图层面板菜单：

```python
        idx = self._current_index
```
#         - 新建图层（对照第三章方法二）

```python
        if 0 <= idx < len(self._layers_data):
```
#         - 新建子图层（对照第十章）

```python
            self.layer_remove_requested.emit(idx)
```
#         - 复制图层（对照第六章）

```python
        event.accept()
```
#         - 删除图层（对照第五章）


```python
    # ── 拖拽到新建按钮复制（第六章） ──
```
#         - 收集到新图层（对照第十五章）


```python
    def _on_add_btn_drag_enter(self, event):
```
#         - 合并选定图层（对照第十七章）

```python
        """拖拽到新建按钮时的视觉反馈"""
```
#         - 拼合图稿（对照第十八章）

```python
        if self._add_btn:
```
#         - 隐藏/显示其他图层

```python
            self._add_btn.setStyleSheet("""
```
#         - 锁定其他图层

```python
                QPushButton { background-color: #0d6efd; color: white;
```
#         - 粘贴时记住图层

```python
                border: 2px solid #4da3ff; border-radius: 3px; font-weight: bold; }
```
#         - 面板选项...

```python
            """)
```
#         方法文档字符串结束


```python
    def _on_add_btn_drag_move(self, event):
```
#         创建右键菜单实例，以自身为父部件

```python
        event.accept()
```
#         设置菜单样式表：暗色主题（#3c3c3c 背景、#ddd 文字、分隔线样式）


```python
    def _on_add_btn_drop(self, event):
```
#     def _on_add_btn_drop(self, event):

```python
        """拖拽图层到新建按钮复制（第六章）"""
```
#         获取当前图层索引

```python
        if self._add_btn:
```
#         获取当前图层对象（索引有效时获取，否则为空）

```python
            self._add_btn.setStyleSheet("")
```
#             self._add_btn.setStyleSheet("")

```python
        idx = self._current_index
```
#         新建图层菜单项（对照第三章方法二）

```python
        if 0 <= idx < len(self._layers_data):
```
#         添加"新建图层"菜单项

```python
            self.layer_duplicate_requested.emit(idx)
```
#         连接菜单项触发信号到添加图层请求信号

```python
        event.accept()
```
#         event.accept()


```python
    # ── 右键菜单（完整对照 Ai 图层面板菜单） ──
```
#         添加"新建子图层"菜单项


```python
    def _on_context_menu(self, pos):
```
#     def _on_context_menu(self, pos):

```python
        """右键菜单：完整图层操作
```
#         添加菜单分隔线


```python
        对照 Ai 图层面板菜单：
```
#         如果当前图层对象不为空（有选中的图层）

```python
        - 新建图层（第三章方法2）
```
#             复制图层菜单项（对照第六章）

```python
        - 新建子图层（第十章）
```
#             添加"复制 图层名"菜单项

```python
        - 复制图层（第六章）
```
#             连接菜单项触发信号到复制图层请求信号

```python
        - 删除图层（第五章）
```
#         - 删除图层（第五章）

```python
        - 当前图层的选项...（图层选项对话框）
```
#             删除图层菜单项（对照第五章方法一）

```python
        - 收集到新图层（第十五章）
```
#             添加"删除 图层名"菜单项

```python
        - 释放到图层 Sequence/Build（第十六章）
```
#             连接菜单项触发信号到删除图层请求信号

```python
        - 合并选定图层（第十七章）
```
#         - 合并选定图层（第十七章）

```python
        - 拼合图稿（第十八章）
```
#             添加菜单分隔线

```python
        - 隐藏/显示其他图层
```
#         - 隐藏/显示其他图层

```python
        - 锁定其他图层
```
#             图层选项菜单项注释（对照第四、十九、二十、二十一、二十二章）

```python
        - 粘贴时记住图层
```
#             添加"图层名 的选项..."菜单项

```python
        - 面板选项...
```
#             连接菜单项触发信号到显示图层选项对话框方法

```python
        """
```
#         """

```python
        item = self._tree.itemAt(pos)
```
#             添加菜单分隔线

```python
        menu = QMenu(self)
```
#         menu = QMenu(self)

```python
        menu.setStyleSheet("""
```
#             收集到新图层菜单项（对照第十五章）

```python
            QMenu { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; padding: 4px; }
```
#             添加"收集到新图层"菜单项

```python
            QMenu::item { padding: 6px 24px; }
```
#             连接菜单项触发信号到收集请求信号

```python
            QMenu::item:selected { background-color: #0d6efd; }
```
#             QMenu::item:selected { background-color: #0d6efd; }

```python
            QMenu::separator { height: 1px; background: #555; margin: 4px 8px; }
```
#             释放到图层的子菜单（对照第十六章）

```python
        """)
```
#             添加"释放到图层"子菜单


```python
        idx = self._current_index
```
#             连接菜单项触发信号到按顺序释放请求信号

```python
        layer = self._layers_data[idx] if 0 <= idx < len(self._layers_data) else None
```
#             在子菜单中添加"构建 (Build)"菜单项


```python
        # 新建图层（第三章方法2）
```
#         # 新建图层（第三章方法2）

```python
        new_layer_action = menu.addAction("  新建图层")
```
#             添加菜单分隔线

```python
        new_layer_action.triggered.connect(self.layer_add_requested.emit)
```
#         new_layer_action.triggered.connect(self.layer_add_requested.emit)


```python
        # 新建子图层（第十章）
```
#             添加"合并选定图层"菜单项

```python
        new_sublayer_action = menu.addAction("  新建子图层")
```
#             连接菜单项触发信号到合并图层请求信号

```python
        new_sublayer_action.triggered.connect(self._on_add_sublayer)
```
#         new_sublayer_action.triggered.connect(self._on_add_sublayer)


```python
        menu.addSeparator()
```
#             添加"拼合图稿"菜单项


```python
        if layer is not None:
```
#         if layer is not None:

```python
            # 复制图层（第六章）
```
#             添加菜单分隔线

```python
            dup_action = menu.addAction(f"  复制 \"{layer.name}\"")
```
#             dup_action = menu.addAction(f"  复制 \"{layer.name}\"")

```python
            dup_action.triggered.connect(lambda: self.layer_duplicate_requested.emit(idx))
```
#             隐藏其他图层菜单项


```python
            # 删除图层（第五章方法1）
```
#                 添加"隐藏其他图层"菜单项

```python
            del_action = menu.addAction(f"  删除 \"{layer.name}\"")
```
#                 连接菜单项触发信号到隐藏其他图层方法

```python
            del_action.triggered.connect(lambda: self.layer_remove_requested.emit(idx))
```
#             del_action.triggered.connect(lambda: self.layer_remove_requested.emit(idx))


```python
            menu.addSeparator()
```
#             如果当前图层未锁定


```python
            # 当前图层的选项...（图层选项对话框：第四章、第十九章、第二十、二十一、二十二章）
```
#                 连接菜单项触发信号到锁定其他图层方法

```python
            options_action = menu.addAction(f"  \"{layer.name}\" 的选项...")
```
#             options_action = menu.addAction(f"  \"{layer.name}\" 的选项...")

```python
            options_action.triggered.connect(lambda: self._show_layer_options_dialog(idx))
```
#             显示所有图层菜单项


```python
            menu.addSeparator()
```
#             连接菜单项触发信号到显示所有图层方法


```python
            # 收集到新图层（第十五章）
```
#             解锁所有图层菜单项

```python
            collect_action = menu.addAction("  收集到新图层")
```
#             添加"解锁所有图层"菜单项

```python
            collect_action.triggered.connect(self.layer_collect_requested.emit)
```
#             连接菜单项触发信号到解锁所有图层方法


```python
            # 释放到图层（第十六章）
```
#         添加菜单分隔线

```python
            release_menu = menu.addMenu("  释放到图层")
```
#             release_menu = menu.addMenu("  释放到图层")

```python
            seq_action = release_menu.addAction("顺序 (Sequence)")
```
#         面板选项菜单项

```python
            seq_action.triggered.connect(self.layer_release_sequence_requested.emit)
```
#         添加"面板选项..."菜单项

```python
            build_action = release_menu.addAction("构建 (Build)")
```
#         连接菜单项触发信号到显示面板选项方法

```python
            build_action.triggered.connect(self.layer_release_build_requested.emit)
```
#             build_action.triggered.connect(self.layer_release_build_requested.emit)


```python
            menu.addSeparator()
```
#             menu.addSeparator()


```python
            # 合并图层（第十七章）
```
#         方法文档字符串：隐藏除指定图层外的所有图层

```python
            merge_action = menu.addAction("  合并选定图层")
```
#         遍历所有图层，同时获取索引和图层对象

```python
            merge_action.triggered.connect(lambda: self.layer_merge_requested.emit([idx]))
```
#             如果当前索引不等于排除索引


```python
            # 拼合图稿（第十八章）
```
#                 发射图层可见性变更信号（携带索引和 False）

```python
            flatten_action = menu.addAction("  拼合图稿")
```
#             flatten_action = menu.addAction("  拼合图稿")

```python
            flatten_action.triggered.connect(self.layer_flatten_requested.emit)
```
#     定义锁定其他图层方法（接收排除索引参数）


```python
            menu.addSeparator()
```
#         遍历所有图层，同时获取索引和图层对象


```python
            # 隐藏/显示其他图层
```
#                 将图层设为锁定

```python
            if layer.visible:
```
#                 发射图层锁定状态变更信号（携带索引和 True）

```python
                hide_others = menu.addAction("  隐藏其他图层")
```
#                 hide_others = menu.addAction("  隐藏其他图层")

```python
                hide_others.triggered.connect(lambda: self._hide_other_layers(idx))
```
#     定义显示所有图层方法


```python
            # 锁定其他图层
```
#         遍历所有图层，同时获取索引和图层对象

```python
            if not layer.locked:
```
#             如果当前图层不可见

```python
                lock_others = menu.addAction("  锁定其他图层")
```
#                 将图层设为可见

```python
                lock_others.triggered.connect(lambda: self._lock_other_layers(idx))
```
#                 发射图层可见性变更信号（携带索引和 True）


```python
            # 显示所有图层
```
#     定义解锁所有图层方法

```python
            show_all = menu.addAction("  显示所有图层")
```
#         方法文档字符串：解锁所有图层

```python
            show_all.triggered.connect(self._show_all_layers)
```
#         遍历所有图层，同时获取索引和图层对象


```python
            # 解锁所有图层
```
#                 将图层设为解锁

```python
            unlock_all = menu.addAction("  解锁所有图层")
```
#                 发射图层锁定状态变更信号（携带索引和 False）

```python
            unlock_all.triggered.connect(self._unlock_all_layers)
```
#             unlock_all.triggered.connect(self._unlock_all_layers)


```python
        menu.addSeparator()
```
#         方法文档字符串：图层选项对话框


```python
        # 面板选项
```
#         - 名称 —— 对照第四章

```python
        panel_opts = menu.addAction("  面板选项...")
```
#         - 颜色 —— 对照第二十章

```python
        panel_opts.triggered.connect(self._show_panel_options)
```
#         - 模板 —— 对照第十九章


```python
        menu.exec_(self._tree.mapToGlobal(pos))
```
#         - 预览 —— 对照第二十二章


```python
    def _hide_other_layers(self, except_idx: int):
```
#         - 显示 —— 对照第七章

```python
        """隐藏除指定图层外的所有图层"""
```
#         - 变暗图像至 —— 对照第十九章扩展功能

```python
        for i, layer in enumerate(self._layers_data):
```
#         方法文档字符串结束

```python
            if i != except_idx:
```
#         局部导入：对话框类、表单布局类、对话框按钮盒类

```python
                layer.visible = False
```
#                 layer.visible = False

```python
                self.layer_visibility_changed.emit(i, False)
```
#         如果索引不在有效范围内


```python
    def _lock_other_layers(self, except_idx: int):
```
#         获取指定索引的图层对象

```python
        """锁定除指定图层外的所有图层"""
```
#         """锁定除指定图层外的所有图层"""

```python
        for i, layer in enumerate(self._layers_data):
```
#         创建对话框实例，以自身为父部件

```python
            if i != except_idx:
```
#         设置对话框窗口标题为"图层选项"

```python
                layer.locked = True
```
#         设置对话框最小宽度为 320 像素

```python
                self.layer_locked_changed.emit(i, True)
```
#         设置对话框样式表（暗色主题）


```python
    def _show_all_layers(self):
```
#     def _show_all_layers(self):

```python
        """显示所有图层"""
```
#         创建表单布局管理器，以对话框为父部件

```python
        for i, layer in enumerate(self._layers_data):
```
#         for i, layer in enumerate(self._layers_data):

```python
            if not layer.visible:
```
#         名称输入注释

```python
                layer.visible = True
```
#         创建名称单行文本框，初始值为图层当前名称

```python
                self.layer_visibility_changed.emit(i, True)
```
#         选中文本框中的全部文本


```python
    def _unlock_all_layers(self):
```
#     def _unlock_all_layers(self):

```python
        """解锁所有图层"""
```
#         颜色选择注释（对照第二十章）

```python
        for i, layer in enumerate(self._layers_data):
```
#         创建颜色下拉组合框

```python
            if layer.locked:
```
#         添加"无"选项（颜色值为空）

```python
                layer.locked = False
```
#         遍历预设图层颜色列表，同时获取颜色索引和颜色值

```python
                self.layer_locked_changed.emit(i, False)
```
#             添加颜色选项（显示"颜色 N"，数据为颜色值）


```python
    def _show_layer_options_dialog(self, index: int):
```
#     def _show_layer_options_dialog(self, index: int):

```python
        """图层选项对话框
```
#         选择当前颜色注释


```python
        对照 Ai 图层选项对话框（第三章 + 第十九-二十二章）：
```
#             遍历预设图层颜色列表

```python
        - 名称 (Name) — 第四章
```
#                 如果图层颜色与预设颜色匹配

```python
        - 颜色 (Color) — 第二十章
```
#                     设置组合框的当前索引为对应颜色（+1 因为第 0 项是"无"）

```python
        - 模板 (Template) — 第十九章
```
#                     跳出循环

```python
        - 打印 (Print) — 第二十一章
```
#         在表单布局中添加"颜色(&C):"标签和颜色组合框一行

```python
        - 预览 (Preview) — 第二十二章
```
#         - 预览 (Preview) — 第二十二章

```python
        - 锁定 (Lock) — 第八章
```
#         模板复选框注释（对照第十九章）

```python
        - 显示 (Show) — 第七章
```
#         创建"模板(&T)"复选框

```python
        - 变暗图像至 (Dim Images) — 第十九章扩展
```
#         设置复选框选中状态为图层的模板状态

```python
        """
```
#         在表单布局中添加模板复选框（无标签）

```python
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
```
#         from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox


```python
        if not (0 <= index < len(self._layers_data)):
```
#         创建"打印(&P)"复选框

```python
            return
```
#         设置复选框选中状态为图层的可打印状态

```python
        layer = self._layers_data[index]
```
#         在表单布局中添加打印复选框（无标签）


```python
        dlg = QDialog(self)
```
#         预览复选框注释（对照第二十二章）

```python
        dlg.setWindowTitle("图层选项")
```
#         创建"预览(&V)"复选框

```python
        dlg.setMinimumWidth(320)
```
#         设置复选框选中状态（预览模式时选中）

```python
        dlg.setStyleSheet("""
```
#         在表单布局中添加预览复选框（无标签）

```python
            QDialog { background-color: #3c3c3c; color: #ddd; }
```
#             QDialog { background-color: #3c3c3c; color: #ddd; }

```python
            QLabel { color: #bbb; }
```
#         锁定复选框注释（对照第八章）

```python
            QLineEdit { background-color: #2d2d2d; color: #ddd; border: 1px solid #555; padding: 4px; }
```
#         创建"锁定(&L)"复选框

```python
            QComboBox { background-color: #2d2d2d; color: #ddd; border: 1px solid #555; padding: 4px; }
```
#         设置复选框选中状态为图层的锁定状态

```python
            QCheckBox { color: #bbb; }
```
#         在表单布局中添加锁定复选框（无标签）

```python
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; padding: 6px 16px; border-radius: 3px; }
```
#             QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; padding: 6px 16px; border-radius: 3px; }

```python
            QPushButton:hover { background-color: #5a5a5a; }
```
#         显示复选框注释（对照第七章）

```python
        """)
```
#         创建"显示(&S)"复选框


```python
        layout = QFormLayout(dlg)
```
#         在表单布局中添加显示复选框（无标签）


```python
        # 名称
```
#         按钮注释

```python
        name_edit = QLineEdit(layer.name)
```
#         创建对话框按钮盒（包含确定和取消按钮）

```python
        name_edit.selectAll()
```
#         连接确定按钮到对话框的接受操作

```python
        layout.addRow("名称(&N):", name_edit)
```
#         连接取消按钮到对话框的拒绝操作


```python
        # 颜色（第二十章）
```
#         # 颜色（第二十章）

```python
        color_combo = QComboBox()
```
#         如果用户点击了确定按钮（对话框返回接受状态）

```python
        color_combo.addItem("无", None)
```
#             获取新名称（去除首尾空格）

```python
        for ci, c in enumerate(self.LAYER_COLORS):
```
#             如果新名称非空且与原名称不同

```python
            color_combo.addItem(f"颜色 {ci + 1}", c)
```
#                 更新图层的名称

```python
            color_combo.setItemData(ci + 1, c, Qt.BackgroundRole)
```
#                 发射图层重命名请求信号


```python
        # 选择当前颜色
```
#             颜色变更处理

```python
        if layer.color:
```
#             获取组合框当前选中项的数据（颜色值）

```python
            for ci, c in enumerate(self.LAYER_COLORS):
```
#             如果新颜色与原颜色不同

```python
                if layer.color.name() == c.name():
```
#                 更新图层的颜色

```python
                    color_combo.setCurrentIndex(ci + 1)
```
#                 发射图层颜色变更信号

```python
                    break
```
#                     break

```python
        layout.addRow("颜色(&C):", color_combo)
```
#             模板状态变更处理


```python
        # 模板（第十九章）
```
#                 更新图层的模板状态

```python
        template_check = QCheckBox("模板(&T)")
```
#                 发射模板模式变更信号

```python
        template_check.setChecked(layer.is_template)
```
#         template_check.setChecked(layer.is_template)

```python
        layout.addRow("", template_check)
```
#             打印状态变更处理


```python
        # 打印（第二十一章）
```
#                 更新图层的可打印状态

```python
        print_check = QCheckBox("打印(&P)")
```
#                 发射打印状态变更信号

```python
        print_check.setChecked(layer.printable)
```
#         print_check.setChecked(layer.printable)

```python
        layout.addRow("", print_check)
```
#             预览模式变更处理


```python
        # 预览（第二十二章）
```
#             如果新预览模式与原模式不同

```python
        preview_check = QCheckBox("预览(&V)")
```
#                 更新图层的预览模式

```python
        preview_check.setChecked(layer.preview_mode == "preview")
```
#                 发射预览模式变更信号

```python
        layout.addRow("", preview_check)
```
#         layout.addRow("", preview_check)


```python
        # 锁定（第八章）
```
#             如果锁定复选框状态与原状态不同

```python
        lock_check = QCheckBox("锁定(&L)")
```
#                 更新图层的锁定状态

```python
        lock_check.setChecked(layer.locked)
```
#                 发射锁定状态变更信号

```python
        layout.addRow("", lock_check)
```
#         layout.addRow("", lock_check)


```python
        # 显示（第七章）
```
#             如果显示复选框状态与原状态不同

```python
        show_check = QCheckBox("显示(&S)")
```
#                 更新图层的可见状态

```python
        show_check.setChecked(layer.visible)
```
#                 发射图层可见性变更信号

```python
        layout.addRow("", show_check)
```
#         layout.addRow("", show_check)


```python
        # 按钮
```
#         方法文档字符串：面板选项对话框

```python
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
```
#         局部导入对话框相关类

```python
        buttons.accepted.connect(dlg.accept)
```
#         buttons.accepted.connect(dlg.accept)

```python
        buttons.rejected.connect(dlg.reject)
```
#         创建对话框实例，以自身为父部件

```python
        layout.addRow(buttons)
```
#         设置对话框窗口标题为"图层面板选项"


```python
        if dlg.exec_() == QDialog.Accepted:
```
#         设置对话框样式表（暗色主题）

```python
            new_name = name_edit.text().strip()
```
#         样式表字符串结束

```python
            if new_name and new_name != layer.name:
```
#             if new_name and new_name != layer.name:

```python
                layer.name = new_name
```
#         创建表单布局管理器，以对话框为父部件

```python
                self.layer_rename_requested.emit(index, new_name)
```
#                 self.layer_rename_requested.emit(index, new_name)


```python
            # 颜色
```
#         设置复选框默认为未选中

```python
            new_color = color_combo.currentData()
```
#         在表单布局中添加（无标签）

```python
            if new_color != layer.color:
```
#             if new_color != layer.color:

```python
                layer.color = new_color
```
#         创建"小行高"复选框

```python
                self.layer_color_changed.emit(index, new_color)
```
#         在表单布局中添加（无标签）


```python
            # 模板
```
#         创建对话框按钮盒（包含确定和取消按钮）

```python
            if template_check.isChecked() != layer.is_template:
```
#         连接确定按钮到对话框的接受操作

```python
                layer.is_template = template_check.isChecked()
```
#         连接取消按钮到对话框的拒绝操作

```python
                self.layer_template_changed.emit(index, layer.is_template)
```
#         在表单布局中添加按钮盒


```python
            # 打印
```
#         执行对话框（显示并等待用户操作）

```python
            if print_check.isChecked() != layer.printable:
```
#             if print_check.isChecked() != layer.printable:

```python
                layer.printable = print_check.isChecked()
```
#     定义添加子图层方法

```python
                self.layer_printable_changed.emit(index, layer.printable)
```
#         方法文档字符串：添加子图层


```python
            # 预览
```
#         如果当前索引在有效范围内

```python
            new_mode = "preview" if preview_check.isChecked() else "outline"
```
#             获取当前图层对象

```python
            if new_mode != layer.preview_mode:
```
#             调用图层的添加子图层方法

```python
                layer.preview_mode = new_mode
```
#             刷新图层树显示

```python
                self.layer_preview_mode_changed.emit(index, new_mode)
```
#                 self.layer_preview_mode_changed.emit(index, new_mode)


```python
            # 锁定
```
#         如果索引在有效范围内

```python
            if lock_check.isChecked() != layer.locked:
```
#             将图层的颜色设置为指定颜色

```python
                layer.locked = lock_check.isChecked()
```
#                 layer.locked = lock_check.isChecked()

```python
                self.layer_locked_changed.emit(index, layer.locked)
```
#     定义切换模板状态方法（接收图层索引参数）


```python
            # 显示
```
#             获取当前图层对象

```python
            if show_check.isChecked() != layer.visible:
```
#             切换图层的模板状态（取反）

```python
                layer.visible = show_check.isChecked()
```
#                 layer.visible = show_check.isChecked()

```python
                self.layer_visibility_changed.emit(index, layer.visible)
```
#     定义切换打印状态方法（接收图层索引参数）


```python
    def _show_panel_options(self):
```
#             获取当前图层对象

```python
        """面板选项对话框"""
```
#             切换图层的可打印状态（取反）

```python
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
```
#         from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox


```python
        dlg = QDialog(self)
```
#         如果索引在有效范围内

```python
        dlg.setWindowTitle("图层面板选项")
```
#             获取当前图层对象

```python
        dlg.setMinimumWidth(280)
```
#             切换图层的预览模式（预览模式和轮廓模式互换）

```python
        dlg.setStyleSheet("""
```
#         dlg.setStyleSheet("""

```python
            QDialog { background-color: #3c3c3c; color: #ddd; }
```
#     定义显示图层菜单方法

```python
            QCheckBox { color: #bbb; }
```
#         方法文档字符串：点击☰按钮显示图层菜单（对照 PDF 第二十五章）

```python
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; padding: 6px 16px; border-radius: 3px; }
```
#         计算当前选中项或第一个顶层项的视觉矩形左上角位置

```python
        """)
```
#         如果树中无项目则使用树的左上角位置


```python
        layout = QFormLayout(dlg)
```
#         layout = QFormLayout(dlg)


```python
        thumb_check = QCheckBox("仅显示图层")
```
# ── 色板面板部分分隔线 ──

```python
        thumb_check.setChecked(False)
```
#         thumb_check.setChecked(False)

```python
        layout.addRow("", thumb_check)
```
# 定义色板面板类（继承自 Qt 部件类 QWidget）


```python
        small_check = QCheckBox("小行高")
```
#     注意事项：PyQt5 的 QWidget 子类不能使用 __slots__ 槽位机制。

```python
        layout.addRow("", small_check)
```
#     类文档字符串结束


```python
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
```
#     定义颜色选中信号（参数类型为 QColor 颜色类）

```python
        buttons.accepted.connect(dlg.accept)
```
#         buttons.accepted.connect(dlg.accept)

```python
        buttons.rejected.connect(dlg.reject)
```
#     定义初始化方法（接收自身引用 self、父部件参数 parent：默认为空）

```python
        layout.addRow(buttons)
```
#         调用父类 QWidget 的初始化方法，传入父部件参数


```python
        dlg.exec_()
```
#         dlg.exec_()


```python
    def _on_add_sublayer(self):
```
#         创建垂直布局管理器，以自身为父部件

```python
        """添加子图层"""
```
#         设置布局内容边距（上、下、左、右各 4 像素）

```python
        idx = self._current_index
```
#         在布局中添加"色板"标签

```python
        if 0 <= idx < len(self._layers_data):
```
#         创建网格布局管理器（用于排列色板色块）

```python
            layer = self._layers_data[idx]
```
#         设置网格布局中控件间距为 2 像素

```python
            layer.add_sublayer()
```
#         将网格布局添加到主布局中

```python
            self.update_layers(self._layers_data, idx)
```
#         在主布局末尾添加弹性拉伸空间


```python
    def _set_layer_color(self, index: int, color: QColor):
```
#     定义更新色板显示方法（接收色板列表参数）

```python
        if 0 <= index < len(self._layers_data):
```
#         当网格布局中还有控件时循环

```python
            self._layers_data[index].color = color
```
#             取出网格布局中的第一个控件项


```python
    def _toggle_template(self, index: int):
```
#                 延迟删除该控件（安全释放内存）

```python
        if 0 <= index < len(self._layers_data):
```
#         设置色板网格每行显示 4 列

```python
            layer = self._layers_data[index]
```
#         遍历色板列表，同时获取索引和色板对象

```python
            layer.is_template = not layer.is_template
```
#             创建按钮实例（作为色板色块）


```python
    def _toggle_printable(self, index: int):
```
#             设置色块提示文本为色板名称

```python
        if 0 <= index < len(self._layers_data):
```
#             设置色块样式表：背景色为色板颜色值、#666 边框、2像素圆角、悬停时蓝色边框

```python
            layer = self._layers_data[index]
```
#             连接色块点击信号到匿名回调（使用默认参数 c 捕获当前颜色，发射颜色选中信号）

```python
            layer.printable = not layer.printable
```
#             将色块添加到网格布局中（行号=索引整除列数，列号=索引对列数取余）


```python
    def _toggle_preview_mode(self, index: int):
```
#     def _toggle_preview_mode(self, index: int):

```python
        if 0 <= index < len(self._layers_data):
```
#         if 0 <= index < len(self._layers_data):

```python
            layer = self._layers_data[index]
```
#             layer = self._layers_data[index]

```python
            layer.preview_mode = "outline" if layer.preview_mode == "preview" else "preview"
```
#             layer.preview_mode = "outline" if layer.preview_mode == "preview" else "preview"


```python
    def _show_layer_menu(self):
```
#     def _show_layer_menu(self):

```python
        """点击☰按钮显示图层菜单（PDF 二十五）"""
```
#         """点击☰按钮显示图层菜单（PDF 二十五）"""

```python
        self._on_context_menu(
```
#         self._on_context_menu(

```python
            self._tree.visualItemRect(self._tree.currentItem() or self._tree.topLevelItem(0)).topLeft()
```
#             self._tree.visualItemRect(self._tree.currentItem() or self._tree.topLevelItem(0)).topLeft()

```python
            if self._tree.topLevelItemCount() > 0 else self._tree.rect().topLeft()
```
#             if self._tree.topLevelItemCount() > 0 else self._tree.rect().topLeft()

```python
        )
```
#         )



```python
# ── 色板面板 ──────────────────────────────────────────────
```
# # ── 色板面板 ──────────────────────────────────────────────


```python
class SwatchesPanel(QWidget):
```
# class SwatchesPanel(QWidget):

```python
    """色板面板
```
#     """色板面板

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
#     注意: PyQt5 QWidget 子类不能使用 __slots__。

```python
    """
```
#     """


```python
    color_selected = pyqtSignal(QColor)
```
#     color_selected = pyqtSignal(QColor)


```python
    def __init__(self, parent=None):
```
#     def __init__(self, parent=None):

```python
        super().__init__(parent)
```
#         super().__init__(parent)

```python
        self._init_ui()
```
#         self._init_ui()


```python
    def _init_ui(self):
```
#     def _init_ui(self):

```python
        layout = QVBoxLayout(self)
```
#         layout = QVBoxLayout(self)

```python
        layout.setContentsMargins(4, 4, 4, 4)
```
#         layout.setContentsMargins(4, 4, 4, 4)

```python
        layout.addWidget(QLabel("色板"))
```
#         layout.addWidget(QLabel("色板"))


```python
        self._grid = QGridLayout()
```
#         self._grid = QGridLayout()

```python
        self._grid.setSpacing(2)
```
#         self._grid.setSpacing(2)

```python
        layout.addLayout(self._grid)
```
#         layout.addLayout(self._grid)

```python
        layout.addStretch()
```
#         layout.addStretch()


```python
    def update_swatches(self, swatches: list[Swatch]):
```
#     def update_swatches(self, swatches: list[Swatch]):

```python
        while self._grid.count():
```
#         while self._grid.count():

```python
            item = self._grid.takeAt(0)
```
#             item = self._grid.takeAt(0)

```python
            if item.widget():
```
#             if item.widget():

```python
                item.widget().deleteLater()
```
#                 item.widget().deleteLater()


```python
        cols = 4
```
#         cols = 4

```python
        for i, swatch in enumerate(swatches):
```
#         for i, swatch in enumerate(swatches):

```python
            btn = QPushButton()
```
#             btn = QPushButton()

```python
            btn.setFixedSize(28, 28)
```
#             btn.setFixedSize(28, 28)

```python
            btn.setToolTip(swatch.name)
```
#             btn.setToolTip(swatch.name)

```python
            btn.setStyleSheet(f"""
```
#             btn.setStyleSheet(f"""

```python
                QPushButton {{
```
#                 QPushButton {{

```python
                    background-color: {swatch.color.name()};
```
#                     background-color: {swatch.color.name()};

```python
                    border: 1px solid #666;
```
#                     border: 1px solid #666;

```python
                    border-radius: 2px;
```
#                     border-radius: 2px;

```python
                }}
```
#                 }}

```python
                QPushButton:hover {{ border: 2px solid #0d6efd; }}
```
#                 QPushButton:hover {{ border: 2px solid #0d6efd; }}

```python
            """)
```
#             """)

```python
            btn.clicked.connect(lambda checked, c=swatch.color: self.color_selected.emit(c))
```
#             btn.clicked.connect(lambda checked, c=swatch.color: self.color_selected.emit(c))

```python
            self._grid.addWidget(btn, i // cols, i % cols)
```
#             self._grid.addWidget(btn, i // cols, i % cols)
