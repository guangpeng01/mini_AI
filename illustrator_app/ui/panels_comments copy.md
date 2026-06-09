# panels.py 逐行注释翻译

> 源文件路径：`C:\Users\77945\Desktop\新建文件夹\03\illustrator_app\ui\panels.py`
>
> 本文件对面板组件源代码进行逐行中文注释翻译，涵盖工具栏、属性面板、图层面板和色板面板四大模块。

---

```python
"""
```
# 文件开头的三引号字符串 —— 模块级文档字符串开始，描述本模块的整体功能

```python
面板组件 (Python 3.10+) —— 工具栏、属性面板、图层面板、色板
```
# 说明本模块包含四种面板组件，要求 Python 3.10 及以上版本

```python

```
# 空行，分隔文档字符串与后续内容

```python
架构优化:
```
# 描述本模块采用的架构优化策略小节标题

```python
- 使用 __slots__ 减少内存占用
```
# 优化策略一：通过 `__slots__` 类属性限制实例属性，避免动态属性字典 `__dict__` 以降低内存开销

```python
- 使用 X | None 替代 Optional[X]
```
# 优化策略二：使用 Python 3.10+ 引入的联合类型语法 `X | None` 替代 `typing.Optional[X]`，写法更简洁

```python
- 使用 match-case 替代 if-elif 链
```
# 优化策略三：使用 Python 3.10+ 引入的结构化模式匹配 `match-case` 语句替代传统的 `if-elif` 条件链

```python
"""
```
# 模块级文档字符串结束

```python

```
# 空行

```python
from __future__ import annotations
```
# 从 `__future__` 模块导入 `annotations` 特性，使所有类型注解都变为字符串形式（延迟求值），支持前向引用和 Python 3.10+ 语法在较低版本中也能运行

```python

```
# 空行

```python
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QRectF
```
# 从 PyQt5 的 QtCore 模块导入核心类：`Qt`（命名空间枚举）、`QSize`（尺寸类）、`pyqtSignal`（信号工厂函数）、`QRectF`（浮点矩形类）

```python
from PyQt5.QtGui import (
```
# 从 PyQt5 的 QtGui 模块导入图形相关类，使用多行括号格式

```python
    QColor, QPainter, QPen, QBrush, QFont, QCursor,
```
# 导入：`QColor`（颜色类）、`QPainter`（绘图工具）、`QPen`（画笔）、`QBrush`（画刷）、`QFont`（字体）、`QCursor`（光标）

```python
)
```
# 多行 import 语句结束

```python
from PyQt5.QtWidgets import (
```
# 从 PyQt5 的 QtWidgets 模块导入各种 UI 控件类

```python
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
```
# 导入基础控件：`QWidget`（控件基类）、`QVBoxLayout`（垂直布局）、`QHBoxLayout`（水平布局）、`QPushButton`（按钮）、`QLabel`（标签）

```python
    QListWidget, QListWidgetItem, QSlider, QSpinBox,
```
# 导入列表和数值控件：`QListWidget`（列表控件）、`QListWidgetItem`（列表条目）、`QSlider`（滑动条）、`QSpinBox`（整数微调框）

```python
    QDoubleSpinBox, QCheckBox, QColorDialog, QGroupBox,
```
# 导入高级控件：`QDoubleSpinBox`（浮点微调框）、`QCheckBox`（复选框）、`QColorDialog`（颜色对话框）、`QGroupBox`（分组框）

```python
    QToolBar, QAction, QFrame,
```
# 导入工具栏控件：`QToolBar`（工具栏）、`QAction`（动作类）、`QFrame`（框架类）

```python
    QLineEdit, QComboBox, QGridLayout,
```
# 导入输入控件：`QLineEdit`（单行输入框）、`QComboBox`（下拉组合框）、`QGridLayout`（网格布局）

```python
    QToolButton, QTextEdit, QMenu,
```
# 导入按钮和编辑控件：`QToolButton`（工具按钮）、`QTextEdit`（多行文本编辑框）、`QMenu`（弹出菜单）

```python
    QTreeWidget, QTreeWidgetItem, QHeaderView,
```
# 导入树形控件：`QTreeWidget`（树形列表）、`QTreeWidgetItem`（树节点）、`QHeaderView`（表头控件）

```python
)
```
# 多行 import 语句结束

```python

```
# 空行

```python
from ..core.graphics import (
```
# 从项目内部包 `core.graphics`（相对导入）导入图形核心类

```python
    GraphicItem, PathItem, RectangleItem, EllipseItem,
```
# 导入图形项类：`GraphicItem`（基类）、`PathItem`（路径）、`RectangleItem`（矩形）、`EllipseItem`（椭圆）

```python
    TextFrame, GroupItem, GraphicStyle, StrokeCap, StrokeJoin,
```
# 导入：`TextFrame`（文本框架）、`GroupItem`（群组）、`GraphicStyle`（图形样式）、`StrokeCap`（描边端点）、`StrokeJoin`（描边连接）

```python
    FillRule, CharacterAttributes, ParagraphAttributes, Justification,
```
# 导入排版类：`FillRule`（填充规则）、`CharacterAttributes`（字符属性）、`ParagraphAttributes`（段落属性）、`Justification`（对齐枚举）

```python
    Swatch,
```
# 导入 `Swatch`（色板类），表示一个命名的颜色样本

```python
)
```
# 多行 import 语句结束

```python
from ..core.document import Document, Layer
```
# 从 `core.document` 导入：`Document`（文档类）和 `Layer`（图层类）

```python
from ..core.tools import ToolType
```
# 从 `core.tools` 导入 `ToolType` 枚举，定义所有可用的工具类型

```python

```
# 空行

```python
# ── 工具栏 ────────────────────────────────────────────────
```
# 注释分隔线，标识"工具栏"模块的开始

```python

```
# 空行

```python
class ToolBar(QWidget):
```
# 定义 `ToolBar`（工具栏）类，继承自 `QWidget` 基类

```python
    """工具栏 —— 左侧工具面板
```
# 类文档字符串 —— 描述这是一个左侧工具面板

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
# 注意：PyQt5 QWidget 子类由于元对象系统限制不支持 `__slots__`

```python
    """
```
# 类文档字符串结束

```python

```
# 空行

```python
    tool_selected = pyqtSignal(ToolType)
```
# 定义 `tool_selected` 信号，参数为 `ToolType`（工具类型枚举），当用户选择新工具时发射

```python

```
# 空行

```python
    TOOLS: list[tuple[ToolType, str, str]] = [
```
# 定义类属性 `TOOLS`，类型为 `list[tuple[ToolType, str, str]]`，是工具类型、中文名、快捷键三元组的列表

```python
        (ToolType.SELECTION, "选择", "V"),
```
# 选择工具，中文名"选择"，快捷键 "V"

```python
        (ToolType.DIRECT_SELECT, "直接选择", "A"),
```
# 直接选择工具（选择锚点），中文名"直接选择"，快捷键 "A"

```python
        (ToolType.RECTANGLE, "矩形", "M"),
```
# 矩形工具，快捷键 "M"

```python
        (ToolType.ELLIPSE, "椭圆", "L"),
```
# 椭圆工具，快捷键 "L"

```python
        (ToolType.PEN, "钢笔", "P"),
```
# 钢笔工具，快捷键 "P"

```python
        (ToolType.TEXT, "文字", "T"),
```
# 文字工具，快捷键 "T"

```python
        (ToolType.HAND, "抓手", "H"),
```
# 抓手工具（平移画布），快捷键 "H"

```python
    ]
```
# 工具列表定义结束

```python

```
# 空行

```python
    def __init__(self, parent=None):
```
# 构造函数，接收可选的父控件参数，默认 None

```python
        super().__init__(parent)
```
# 调用父类 QWidget 构造函数，完成 Qt 对象树注册

```python
        self.setFixedWidth(48)
```
# 设置工具栏固定宽度为 48 像素

```python
        self._buttons: dict[ToolType, QToolButton] = {}
```
# 初始化私有属性 `_buttons`，类型为字典，将工具类型映射到对应的 QToolButton 控件

```python
        self._current_tool = ToolType.SELECTION
```
# 初始化当前工具为选择工具

```python
        self._init_ui()
```
# 调用 UI 初始化方法构建界面

```python

```
# 空行

```python
    def _init_ui(self):
```
# 定义私有方法 `_init_ui`，构建工具栏的所有 UI 控件

```python
        layout = QVBoxLayout(self)
```
# 创建垂直布局管理器作为主布局

```python
        layout.setContentsMargins(4, 8, 4, 8)
```
# 设置四周边距：左 4px、上 8px、右 4px、下 8px

```python
        layout.setSpacing(4)
```
# 设置控件间垂直间距为 4px

```python

```
# 空行

```python
        for tool_type, name, shortcut in self.TOOLS:
```
# 遍历 TOOLS 列表中每个工具三元组

```python
            btn = QToolButton()
```
# 创建工具按钮控件实例

```python
            btn.setToolTip(f"{name} ({shortcut})")
```
# 设置工具提示，格式为"名称 (快捷键)"

```python
            btn.setCheckable(True)
```
# 设为可切换状态，实现互斥选择的视觉反馈

```python
            btn.setFixedSize(40, 40)
```
# 设置固定尺寸 40×40 像素正方形

```python
            btn.setText(shortcut)
```
# 按钮显示快捷键字母

```python
            btn.setFont(QFont("Arial", 10, QFont.Bold))
```
# 设置字体为 Arial 10号粗体

```python
            btn.clicked.connect(lambda checked, t=tool_type: self._on_tool_clicked(t))
```
# 连接点击信号到 lambda，通过默认参数 `t=tool_type` 捕获循环变量避免闭包陷阱

```python
            self._buttons[tool_type] = btn
```
# 将按钮存入字典，以工具类型为键

```python
            layout.addWidget(btn, alignment=Qt.AlignCenter)
```
# 将按钮添加到布局中，水平居对齐

```python

```
# 空行

```python
        layout.addStretch()
```
# 添加弹性空白，将工具按钮推向顶部

```python
        self._buttons[ToolType.SELECTION].setChecked(True)
```
# 默认选中选择工具按钮

```python

```
# 空行

```python
        self.setStyleSheet("""
```
# 设置工具栏 QSS 样式表

```python
            QWidget { background-color: #3c3c3c; }
```
# 整体深灰背景 #3c3c3c

```python
            QToolButton { border: 1px solid #555; border-radius: 4px; background-color: #4a4a4a; color: #ddd; }
```
# 按钮默认样式：灰色边框、圆角、灰色背景、浅灰文字

```python
            QToolButton:hover { background-color: #5a5a5a; }
```
# 悬停时背景色变亮

```python
            QToolButton:checked { background-color: #0d6efd; border-color: #0b5ed7; color: white; }
```
# 选中状态：蓝色背景、白色文字

```python
        """)
```
# 样式表结束

```python

```
# 空行

```python
    def _on_tool_clicked(self, tool_type: ToolType):
```
# 私有方法，处理工具按钮点击事件

```python
        self._current_tool = tool_type
```
# 更新当前工具记录

```python
        for t, btn in self._buttons.items():
```
# 遍历所有工具按钮

```python
            btn.setChecked(t == tool_type)
```
# 只有被点击的工具按钮设为选中，其余取消选中（互斥）

```python
        self.tool_selected.emit(tool_type)
```
# 发射 tool_selected 信号通知外部

```python

```
# 空行

```python
    def set_current_tool(self, tool_type: ToolType):
```
# 公共方法，供外部程序化切换当前工具

```python
        if tool_type in self._buttons:
```
# 检查工具类型是否有效

```python
            self._buttons[tool_type].setChecked(True)
```
# 触发对应按钮的选中状态

```python
            self._current_tool = tool_type
```
# 更新内部当前工具记录

```python
            for t, btn in self._buttons.items():
```
# 遍历所有按钮

```python
                btn.setChecked(t == tool_type)
```
# 确保互斥：只有目标工具选中

```python

```
# 空行

```python

```
# 空行

```python
# ── 属性面板 ──────────────────────────────────────────────
```
# 注释分隔线，标识"属性面板"模块的开始

```python

```
# 空行

```python
class PropertiesPanel(QWidget):
```
# 定义 `PropertiesPanel`（属性面板）类，继承 QWidget

```python
    """属性面板 —— 显示和编辑选中图形的属性
```
# 类文档字符串

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
# 注意：不支持 `__slots__`

```python
    """
```
# 文档字符串结束

```python

```
# 空行

```python
    fill_color_changed = pyqtSignal(QColor)
```
# 信号：填充颜色变更，携带 QColor

```python
    stroke_color_changed = pyqtSignal(QColor)
```
# 信号：描边颜色变更，携带 QColor

```python
    stroke_width_changed = pyqtSignal(float)
```
# 信号：描边粗细变更，携带 float

```python
    opacity_changed = pyqtSignal(float)
```
# 信号：不透明度变更，携带 0.0~1.0 的 float

```python
    corner_radius_changed = pyqtSignal(float)
```
# 信号：圆角半径变更，携带 float

```python
    text_changed = pyqtSignal(str)
```
# 信号：文本内容变更，携带 str

```python
    font_size_changed = pyqtSignal(float)
```
# 信号：字号变更，携带 float

```python
    font_family_changed = pyqtSignal(str)
```
# 信号：字体系列变更，携带 str

```python
    bold_changed = pyqtSignal(bool)
```
# 信号：粗体状态变更，携带 bool

```python
    italic_changed = pyqtSignal(bool)
```
# 信号：斜体状态变更，携带 bool

```python
    alignment_changed = pyqtSignal(Justification)
```
# 信号：文本对齐方式变更，携带 Justification 枚举

```python
    order_front = pyqtSignal()
```
# 信号：请求将对象置顶，无参数

```python
    order_back = pyqtSignal()
```
# 信号：请求将对象置底

```python
    order_forward = pyqtSignal()
```
# 信号：请求将对象上移一层

```python
    order_backward = pyqtSignal()
```
# 信号：请求将对象下移一层

```python
    delete_requested = pyqtSignal()
```
# 信号：请求删除选中对象

```python

```
# 空行

```python
    def __init__(self, parent=None):
```
# 构造函数

```python
        super().__init__(parent)
```
# 调用父类构造函数

```python
        self._selected_items: list[GraphicItem] = []
```
# 初始化选中项列表，类型为 `list[GraphicItem]`，初始为空

```python
        self._init_ui()
```
# 调用 UI 初始化

```python

```
# 空行

```python
    def _init_ui(self):
```
# 私有方法，构建属性面板的完整界面

```python
        main_layout = QVBoxLayout(self)
```
# 创建垂直主布局

```python
        main_layout.setContentsMargins(8, 8, 8, 8)
```
# 设置四周边距各 8px

```python
        main_layout.setSpacing(8)
```
# 设置控件间距 8px

```python

```
# 空行

```python
        # ── 变换 ──
```
# 标记：开始构建"变换"属性组

```python
        transform_group = QGroupBox("变换")
```
# 创建"变换"分组框

```python
        transform_layout = QGridLayout(transform_group)
```
# 在分组框内创建网格布局

```python

```
# 空行

```python
        self._x_spin = self._make_spinbox(-9999, 9999, 1)
```
# 创建 X 坐标微调框，范围 -9999~9999，1位小数

```python
        self._y_spin = self._make_spinbox(-9999, 9999, 1)
```
# 创建 Y 坐标微调框

```python
        self._w_spin = self._make_spinbox(0, 99999, 1)
```
# 创建宽度微调框，范围 0~99999

```python
        self._h_spin = self._make_spinbox(0, 99999, 1)
```
# 创建高度微调框，范围 0~99999

```python

```
# 空行

```python
        for row, items in enumerate([
```
# 遍历两行配置，row 为行号，items 为每行的控件对

```python
            [("X:", self._x_spin), ("Y:", self._y_spin)],
```
# 第一行：X 标签+输入框，Y 标签+输入框

```python
            [("W:", self._w_spin), ("H:", self._h_spin)],
```
# 第二行：W 标签+输入框，H 标签+输入框

```python
        ]):
```
# 列表和 for 循环结束

```python
            (label0, widget0), (label1, widget1) = items
```
# 解构：提取两对标签和控件

```python
            transform_layout.addWidget(QLabel(label0), row, 0)
```
# 第一列标签添加到第 row 行第 0 列

```python
            transform_layout.addWidget(widget0, row, 1)
```
# 第一列输入框添加到第 row 行第 1 列

```python
            transform_layout.addWidget(QLabel(label1), row, 2)
```
# 第二列标签添加到第 row 行第 2 列

```python
            transform_layout.addWidget(widget1, row, 3)
```
# 第二列输入框添加到第 row 行第 3 列

```python

```
# 空行

```python
        transform_layout.addWidget(QLabel("旋转:"), 2, 0)
```
# 第 2 行第 0 列添加"旋转:"标签

```python
        self._rotate_spin = QDoubleSpinBox()
```
# 创建旋转角度浮点微调框

```python
        self._rotate_spin.setRange(-360, 360)
```
# 旋转范围 -360 到 360 度

```python
        transform_layout.addWidget(self._rotate_spin, 2, 1)
```
# 添加到第 2 行第 1 列

```python

```
# 空行

```python
        transform_layout.addWidget(QLabel("不透明度:"), 2, 2)
```
# 第 2 行第 2 列添加"不透明度:"标签

```python
        self._opacity_spin = QDoubleSpinBox()
```
# 创建不透明度浮点微调框

```python
        self._opacity_spin.setRange(0, 100)
```
# 范围 0~100（百分比）

```python
        self._opacity_spin.setValue(100)
```
# 初始值 100（完全不透明）

```python
        self._opacity_spin.setSuffix("%")
```
# 设置后缀为 "%"

```python
        self._opacity_spin.valueChanged.connect(lambda v: self.opacity_changed.emit(v / 100.0))
```
# 值变更时将百分比值除以 100 转为 0~1 后发射信号

```python
        transform_layout.addWidget(self._opacity_spin, 2, 3)
```
# 添加到第 2 行第 3 列

```python

```
# 空行

```python
        main_layout.addWidget(transform_group)
```
# 将变换分组框添加到主布局

```python

```
# 空行

```python
        # ── 外观 ──
```
# 标记：开始构建"外观"属性组

```python
        appearance_group = QGroupBox("外观")
```
# 创建"外观"分组框

```python
        appearance_layout = QVBoxLayout(appearance_group)
```
# 创建垂直布局

```python

```
# 空行

```python
        fill_layout = QHBoxLayout()
```
# 创建填充颜色水平布局

```python
        fill_layout.addWidget(QLabel("填充:"))
```
# 添加"填充:"标签

```python
        self._fill_btn = QPushButton()
```
# 创建填充颜色预览按钮（无文字）

```python
        self._fill_btn.setFixedSize(30, 30)
```
# 固定尺寸 30×30

```python
        self._fill_btn.setStyleSheet("background-color: #ccc; border: 1px solid #888;")
```
# 初始样式：浅灰背景、灰色边框

```python
        self._fill_btn.clicked.connect(self._on_fill_clicked)
```
# 点击连接到填充颜色选择方法

```python
        fill_layout.addWidget(self._fill_btn)
```
# 添加填充预览按钮

```python
        self._fill_none_btn = QPushButton("无")
```
# 创建"无"按钮（清除填充）

```python
        self._fill_none_btn.setFixedWidth(30)
```
# 固定宽度 30px

```python
        self._fill_none_btn.clicked.connect(self._on_fill_none)
```
# 点击连接到清除填充方法

```python
        fill_layout.addWidget(self._fill_none_btn)
```
# 添加"无"按钮

```python
        fill_layout.addStretch()
```
# 弹性空白

```python
        appearance_layout.addLayout(fill_layout)
```
# 将填充布局添加到外观布局

```python

```
# 空行

```python
        stroke_layout = QHBoxLayout()
```
# 创建描边颜色水平布局

```python
        stroke_layout.addWidget(QLabel("描边:"))
```
# 添加"描边:"标签

```python
        self._stroke_btn = QPushButton()
```
# 创建描边颜色预览按钮

```python
        self._stroke_btn.setFixedSize(30, 30)
```
# 固定尺寸 30×30

```python
        self._stroke_btn.setStyleSheet("background-color: #333; border: 1px solid #888;")
```
# 初始样式：深灰背景

```python
        self._stroke_btn.clicked.connect(self._on_stroke_clicked)
```
# 点击连接到描边颜色选择方法

```python
        stroke_layout.addWidget(self._stroke_btn)
```
# 添加描边预览按钮

```python
        self._stroke_none_btn = QPushButton("无")
```
# 创建描边"无"按钮

```python
        self._stroke_none_btn.setFixedWidth(30)
```
# 固定宽度 30px

```python
        self._stroke_none_btn.clicked.connect(self._on_stroke_none)
```
# 点击连接到清除描边方法

```python
        stroke_layout.addWidget(self._stroke_none_btn)
```
# 添加描边"无"按钮

```python
        stroke_layout.addWidget(QLabel("粗细:"))
```
# 添加"粗细:"标签

```python
        self._stroke_width = QDoubleSpinBox()
```
# 创建描边粗细微调框

```python
        self._stroke_width.setRange(0, 100)
```
# 范围 0~100

```python
        self._stroke_width.setValue(1)
```
# 初始值 1

```python
        self._stroke_width.valueChanged.connect(self.stroke_width_changed.emit)
```
# 值变更直接发射 stroke_width_changed 信号

```python
        stroke_layout.addWidget(self._stroke_width)
```
# 添加描边粗细微调框

```python
        appearance_layout.addLayout(stroke_layout)
```
# 将描边布局添加到外观布局

```python

```
# 空行

```python
        corner_layout = QHBoxLayout()
```
# 创建圆角半径水平布局

```python
        corner_layout.addWidget(QLabel("圆角:"))
```
# 添加"圆角:"标签

```python
        self._corner_spin = QDoubleSpinBox()
```
# 创建圆角微调框

```python
        self._corner_spin.setRange(0, 500)
```
# 范围 0~500

```python
        self._corner_spin.valueChanged.connect(self.corner_radius_changed.emit)
```
# 值变更直接发射 corner_radius_changed 信号

```python
        corner_layout.addWidget(self._corner_spin)
```
# 添加圆角微调框

```python
        corner_layout.addStretch()
```
# 弹性空白

```python
        appearance_layout.addLayout(corner_layout)
```
# 将圆角布局添加到外观布局

```python

```
# 空行

```python
        main_layout.addWidget(appearance_group)
```
# 将外观分组框添加到主布局

```python

```
# 空行

```python
        # ── 文字 ──
```
# 标记：开始构建"文字"属性组

```python
        text_group = QGroupBox("文字")
```
# 创建"文字"分组框

```python
        text_layout = QVBoxLayout(text_group)
```
# 创建垂直布局

```python

```
# 空行

```python
        font_layout = QHBoxLayout()
```
# 创建字体水平布局

```python
        self._font_family = QComboBox()
```
# 创建字体系列下拉框

```python
        self._font_family.setEditable(True)
```
# 设为可编辑模式（允许输入自定义字体名）

```python
        self._font_family.addItems([
```
# 添加预设字体选项

```python
            "Arial", "Helvetica", "Times New Roman", "Courier New",
```
# 常见西文字体

```python
            "Verdana", "Georgia", "微软雅黑", "宋体", "黑体",
```
# 更多西文字体和中文字体

```python
        ])
```
# 预设列表结束

```python
        self._font_family.currentTextChanged.connect(self.font_family_changed.emit)
```
# 文本变更直接发射 font_family_changed 信号

```python
        font_layout.addWidget(self._font_family)
```
# 添加字体下拉框

```python

```
# 空行

```python
        self._font_size = QDoubleSpinBox()
```
# 创建字号微调框

```python
        self._font_size.setRange(1, 999)
```
# 范围 1~999

```python
        self._font_size.setValue(24)
```
# 默认值 24

```python
        self._font_size.valueChanged.connect(self.font_size_changed.emit)
```
# 值变更直接发射 font_size_changed 信号

```python
        font_layout.addWidget(self._font_size)
```
# 添加字号微调框

```python
        text_layout.addLayout(font_layout)
```
# 将字体布局添加到文字布局

```python

```
# 空行

```python
        style_layout = QHBoxLayout()
```
# 创建样式（粗体/斜体）水平布局

```python
        self._bold_btn = QPushButton("B")
```
# 创建粗体按钮，显示 "B"

```python
        self._bold_btn.setCheckable(True)
```
# 设为可切换状态

```python
        self._bold_btn.setFont(QFont("Arial", 12, QFont.Bold))
```
# 字体为 Arial 12号粗体（视觉体现粗体效果）

```python
        self._bold_btn.setFixedSize(30, 30)
```
# 固定尺寸 30×30

```python
        self._bold_btn.toggled.connect(self.bold_changed.emit)
```
# 切换信号直接发射 bold_changed

```python
        style_layout.addWidget(self._bold_btn)
```
# 添加粗体按钮

```python

```
# 空行

```python
        self._italic_btn = QPushButton("I")
```
# 创建斜体按钮，显示 "I"

```python
        self._italic_btn.setCheckable(True)
```
# 设为可切换状态

```python
        self._italic_btn.setFont(QFont("Arial", 12, QFont.StyleItalic))
```
# 字体为 Arial 12号斜体（视觉体现斜体效果）

```python
        self._italic_btn.setFixedSize(30, 30)
```
# 固定尺寸 30×30

```python
        self._italic_btn.toggled.connect(self.italic_changed.emit)
```
# 切换信号直接发射 italic_changed

```python
        style_layout.addWidget(self._italic_btn)
```
# 添加斜体按钮

```python
        style_layout.addStretch()
```
# 弹性空白

```python
        text_layout.addLayout(style_layout)
```
# 将样式布局添加到文字布局

```python

```
# 空行

```python
        align_layout = QHBoxLayout()
```
# 创建对齐水平布局

```python
        self._align_left = QPushButton("左")
```
# 创建"左对齐"按钮

```python
        self._align_left.setCheckable(True)
```
# 可切换状态

```python
        self._align_left.clicked.connect(lambda: self.alignment_changed.emit(Justification.LEFT))
```
# 点击发射 alignment_changed 信号，传递左对齐枚举值

```python
        align_layout.addWidget(self._align_left)
```
# 添加左对齐按钮

```python

```
# 空行

```python
        self._align_center = QPushButton("中")
```
# 创建"居中对齐"按钮

```python
        self._align_center.setCheckable(True)
```
# 可切换状态

```python
        self._align_center.clicked.connect(lambda: self.alignment_changed.emit(Justification.CENTER))
```
# 点击发射居中对齐信号

```python
        align_layout.addWidget(self._align_center)
```
# 添加居中按钮

```python

```
# 空行

```python
        self._align_right = QPushButton("右")
```
# 创建"右对齐"按钮

```python
        self._align_right.setCheckable(True)
```
# 可切换状态

```python
        self._align_right.clicked.connect(lambda: self.alignment_changed.emit(Justification.RIGHT))
```
# 点击发射右对齐信号

```python
        align_layout.addWidget(self._align_right)
```
# 添加右对齐按钮

```python
        text_layout.addLayout(align_layout)
```
# 将对齐布局添加到文字布局

```python

```
# 空行

```python
        self._text_edit = QTextEdit()
```
# 创建多行文本编辑框

```python
        self._text_edit.setMaximumHeight(80)
```
# 最大高度 80px（防止占用过多空间）

```python
        self._text_edit.setPlaceholderText("输入文字内容...")
```
# 占位提示文本

```python
        self._text_edit.textChanged.connect(
```
# 文本变更信号连接到 lambda

```python
            lambda: self.text_changed.emit(self._text_edit.toPlainText()),
```
# 获取纯文本内容并发射 text_changed 信号

```python
        )
```
# 信号连接结束

```python
        text_layout.addWidget(self._text_edit)
```
# 添加文本编辑框

```python

```
# 空行

```python
        main_layout.addWidget(text_group)
```
# 将文字分组框添加到主布局

```python

```
# 空行

```python
        # ── 排列 ──
```
# 标记：开始构建"排列"属性组

```python
        arrange_group = QGroupBox("排列")
```
# 创建"排列"分组框

```python
        arrange_layout = QHBoxLayout(arrange_group)
```
# 创建水平布局

```python
        for text, signal in [
```
# 遍历按钮文本和对应信号的元组列表

```python
            ("置顶", self.order_front),
```
# "置顶"对应 order_front 信号

```python
            ("上移", self.order_forward),
```
# "上移"对应 order_forward 信号

```python
            ("下移", self.order_backward),
```
# "下移"对应 order_backward 信号

```python
            ("置底", self.order_back),
```
# "置底"对应 order_back 信号

```python
        ]:
```
# 列表和循环结束

```python
            btn = QPushButton(text)
```
# 创建按钮

```python
            btn.clicked.connect(signal.emit)
```
# 点击直接发射对应信号

```python
            arrange_layout.addWidget(btn)
```
# 添加到布局

```python
        main_layout.addWidget(arrange_group)
```
# 将排列分组框添加到主布局

```python

```
# 空行

```python
        # ── 删除 ──
```
# 标记：创建"删除"按钮

```python
        self._delete_btn = QPushButton("删除选中对象")
```
# 创建删除按钮

```python
        self._delete_btn.setStyleSheet("""
```
# 设置删除按钮的红色危险样式

```python
            QPushButton {
```
# QPushButton 样式开始

```python
                background-color: #dc3545; color: white; border: none;
```
# 红色背景、白色文字、无边框

```python
                padding: 8px; border-radius: 4px; font-weight: bold;
```
# 8px 内边距、4px 圆角、粗体

```python
            }
```
# 样式结束

```python
            QPushButton:hover { background-color: #c82333; }
```
# 悬停时更深红色

```python
        """)
```
# 样式表结束

```python
        self._delete_btn.clicked.connect(self.delete_requested.emit)
```
# 点击直接发射 delete_requested 信号

```python
        main_layout.addWidget(self._delete_btn)
```
# 将删除按钮添加到主布局

```python

```
# 空行

```python
        main_layout.addStretch()
```
# 主布局末尾添加弹性空白

```python

```
# 空行

```python
        self.setStyleSheet("""
```
# 设置属性面板整体 QSS 样式表

```python
            QGroupBox { font-weight: bold; border: 1px solid #555; border-radius: 4px; margin-top: 8px; padding-top: 12px; color: #ddd; }
```
# 分组框样式：粗体、灰色边框、圆角、上边距、浅灰文字

```python
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #ccc; }
```
# 分组框标题子控件样式

```python
            QLabel { color: #bbb; }
```
# 标签文字颜色

```python
            QDoubleSpinBox, QSpinBox, QComboBox { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; padding: 2px; }
```
# 微调框和下拉框样式

```python
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; padding: 4px 8px; border-radius: 3px; }
```
# 通用按钮样式

```python
            QPushButton:hover { background-color: #5a5a5a; }
```
# 按钮悬停样式

```python
            QPushButton:checked { background-color: #0d6efd; color: white; }
```
# 按钮选中样式

```python
            QTextEdit { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; }
```
# 文本编辑框样式

```python
        """)
```
# 样式表结束

```python
        self.setMinimumWidth(220)
```
# 设置面板最小宽度 220px

```python

```
# 空行

```python
    @staticmethod
```
# 静态方法装饰器，不接收 self

```python
    def _make_spinbox(min_val: float, max_val: float, decimals: int) -> QDoubleSpinBox:
```
# 静态工厂方法：创建配置好的浮点微调框，参数为最小值、最大值、小数位数

```python
        sb = QDoubleSpinBox()
```
# 创建微调框实例

```python
        sb.setRange(min_val, max_val)
```
# 设置数值范围

```python
        sb.setDecimals(decimals)
```
# 设置小数位数

```python
        return sb
```
# 返回配置好的微调框

```python

```
# 空行

```python
    def update_selection(self, items: list[GraphicItem]):
```
# 公共方法：当选中对象改变时更新属性面板显示

```python
        """更新选中项显示"""
```
# 方法文档字符串

```python
        self._selected_items = items
```
# 更新内部选中项列表

```python
        if not items:
```
# 如果没有选中任何对象

```python
            self.setEnabled(False)
```
# 禁用整个面板（控件变灰）

```python
            return
```
# 提前返回

```python

```
# 空行

```python
        try:
```
# 开始 try 块，捕获可能的异常

```python
            self.setEnabled(True)
```
# 启用面板

```python
            item = items[0]
```
# 取第一个选中对象作为显示参考

```python

```
# 空行

```python
            # 变换
```
# 开始更新变换属性

```python
            rect = item.bounding_rect()
```
# 获取对象边界矩形

```python
            for spin, val in [
```
# 遍历微调框和对应值的元组

```python
                (self._x_spin, rect.x()), (self._y_spin, rect.y()),
```
# X 对应 x 坐标，Y 对应 y 坐标

```python
                (self._w_spin, rect.width()), (self._h_spin, rect.height()),
```
# W 对应宽度，H 对应高度

```python
            ]:
```
# 列表和循环结束

```python
                spin.blockSignals(True)
```
# 阻塞信号（防止 setValue 触发循环更新）

```python
                spin.setValue(val)
```
# 设置显示值

```python
                spin.blockSignals(False)
```
# 恢复信号

```python

```
# 空行

```python
            # 不透明度
```
# 更新不透明度

```python
            self._opacity_spin.blockSignals(True)
```
# 阻塞信号

```python
            self._opacity_spin.setValue(item.opacity * 100)
```
# 将 0~1 的不透明度乘以 100 转为百分比

```python
            self._opacity_spin.blockSignals(False)
```
# 恢复信号

```python

```
# 空行

```python
            # 填充颜色
```
# 更新填充颜色显示

```python
            fc = item.style.fill_color
```
# 获取填充颜色

```python
            if fc is not None and fc.isValid():
```
# 如果颜色有效

```python
                self._fill_btn.setStyleSheet(
```
# 设置填充按钮样式为实色

```python
                    f"background-color: {fc.name()}; border: 1px solid #888;"
```
# 使用颜色的十六进制名称作为背景

```python
                )
```
# 调用结束

```python
            else:
```
# 如果颜色无效

```python
                self._fill_btn.setStyleSheet(
```
# 设置为无填充状态

```python
                    "background-color: transparent; border: 1px dashed #888;"
```
# 透明背景、虚线边框表示"无填充"

```python
                )
```
# 调用结束

```python

```
# 空行

```python
            # 描边颜色
```
# 更新描边颜色显示

```python
            sc = item.style.stroke_color
```
# 获取描边颜色

```python
            if sc is not None and sc.isValid():
```
# 如果颜色有效

```python
                self._stroke_btn.setStyleSheet(
```
# 设置描边按钮为实色

```python
                    f"background-color: {sc.name()}; border: 1px solid #888;"
```
# 使用颜色的十六进制名称

```python
                )
```
# 调用结束

```python
            else:
```
# 如果颜色无效

```python
                self._stroke_btn.setStyleSheet(
```
# 设置为无描边状态

```python
                    "background-color: transparent; border: 1px dashed #888;"
```
# 透明背景、虚线边框

```python
                )
```
# 调用结束

```python

```
# 空行

```python
            # 描边粗细
```
# 更新描边粗细

```python
            self._stroke_width.blockSignals(True)
```
# 阻塞信号

```python
            self._stroke_width.setValue(item.style.stroke_width)
```
# 设置实际描边宽度

```python
            self._stroke_width.blockSignals(False)
```
# 恢复信号

```python

```
# 空行

```python
            # 圆角
```
# 更新圆角半径

```python
            if isinstance(item, RectangleItem):
```
# 只有矩形才有圆角属性

```python
                self._corner_spin.setEnabled(True)
```
# 启用圆角微调框

```python
                self._corner_spin.blockSignals(True)
```
# 阻塞信号

```python
                self._corner_spin.setValue(item.corner_radius)
```
# 设置实际圆角值

```python
                self._corner_spin.blockSignals(False)
```
# 恢复信号

```python
            else:
```
# 非矩形对象

```python
                self._corner_spin.setEnabled(False)
```
# 禁用圆角微调框

```python

```
# 空行

```python
            # 文字属性
```
# 更新文字相关属性

```python
            is_text = isinstance(item, TextFrame)
```
# 检查是否为文本框架

```python
            for widget in [
```
# 遍历文字相关控件

```python
                self._font_family, self._font_size,
```
# 字体下拉框和字号微调框

```python
                self._bold_btn, self._italic_btn, self._text_edit,
```
# 粗体、斜体按钮和文本编辑框

```python
            ]:
```
# 列表结束

```python
                widget.setEnabled(is_text)
```
# 只有选中文本时才启用这些控件

```python

```
# 空行

```python
            if is_text:
```
# 如果是文本对象

```python
                self._font_family.blockSignals(True)
```
# 阻塞字体下拉框信号

```python
                self._font_family.setCurrentText(item.char_attrs.font_family)
```
# 设置当前字体名称

```python
                self._font_family.blockSignals(False)
```
# 恢复信号

```python

```
# 空行

```python
                self._font_size.blockSignals(True)
```
# 阻塞字号信号

```python
                self._font_size.setValue(item.char_attrs.font_size)
```
# 设置字号

```python
                self._font_size.blockSignals(False)
```
# 恢复信号

```python

```
# 空行

```python
                for btn, val in [
```
# 遍历粗体/斜体按钮和对应值

```python
                    (self._bold_btn, item.char_attrs.bold),
```
# 粗体按钮和粗体属性

```python
                    (self._italic_btn, item.char_attrs.italic),
```
# 斜体按钮和斜体属性

```python
                ]:
```
# 列表结束

```python
                    btn.blockSignals(True)
```
# 阻塞按钮信号

```python
                    btn.setChecked(val)
```
# 设置选中状态

```python
                    btn.blockSignals(False)
```
# 恢复信号

```python

```
# 空行

```python
                self._text_edit.blockSignals(True)
```
# 阻塞文本编辑框信号

```python
                self._text_edit.setPlainText(item.contents)
```
# 设置文本内容

```python
                self._text_edit.blockSignals(False)
```
# 恢复信号

```python
        except Exception as e:
```
# 捕获任意异常

```python
            import traceback
```
# 导入 traceback 模块（延迟导入）

```python
            traceback.print_exc()
```
# 打印完整异常堆栈到标准错误

```python
            print(f"[update_selection ERROR] {e}")
```
# 打印异常信息到标准输出

```python

```
# 空行

```python
    def _on_fill_clicked(self):
```
# 私有方法：填充颜色按钮点击处理

```python
        color = QColorDialog.getColor()
```
# 弹出系统颜色选择对话框

```python
        if color.isValid():
```
# 如果选择了有效颜色

```python
            self.fill_color_changed.emit(color)
```
# 发射填充颜色变更信号

```python
            self._fill_btn.setStyleSheet(
```
# 更新按钮样式

```python
                f"background-color: {color.name()}; border: 1px solid #888;"
```
# 设置为新颜色背景

```python
            )
```
# 调用结束

```python

```
# 空行

```python
    def _on_fill_none(self):
```
# 私有方法：填充"无"按钮点击处理

```python
        self.fill_color_changed.emit(QColor())
```
# 发射信号，传递无效的空 QColor（无填充）

```python
        self._fill_btn.setStyleSheet(
```
# 更新按钮为无填充样式

```python
            "background-color: transparent; border: 1px dashed #888;"
```
# 透明背景、虚线边框

```python
        )
```
# 调用结束

```python

```
# 空行

```python
    def _on_stroke_clicked(self):
```
# 私有方法：描边颜色按钮点击处理

```python
        color = QColorDialog.getColor()
```
# 弹出颜色选择对话框

```python
        if color.isValid():
```
# 如果选择了有效颜色

```python
            self.stroke_color_changed.emit(color)
```
# 发射描边颜色变更信号

```python
            self._stroke_btn.setStyleSheet(
```
# 更新按钮样式

```python
                f"background-color: {color.name()}; border: 1px solid #888;"
```
# 设置为新颜色背景

```python
            )
```
# 调用结束

```python

```
# 空行

```python
    def _on_stroke_none(self):
```
# 私有方法：描边"无"按钮点击处理

```python
        self.stroke_color_changed.emit(QColor())
```
# 发射信号，传递无效 QColor（无描边）

```python
        self._stroke_btn.setStyleSheet(
```
# 更新按钮为无描边样式

```python
            "background-color: transparent; border: 1px dashed #888;"
```
# 透明背景、虚线边框

```python
        )
```
# 调用结束

---

> **（以上为第 1~452 行，以下为第 453~1427 行，即图层面板类 LayersPanel 和色板面板类 SwatchesPanel。）**

---

```python

```
# 空行

```python

```
# 空行

```python
# ── 图层面板 ──────────────────────────────────────────────
```
# 注释分隔线，标识"图层面板"模块的开始

```python

```
# 空行

```python
class LayersPanel(QWidget):
```
# 定义 `LayersPanel`（图层面板）类，继承 QWidget，是功能最复杂的面板

```python
    """图层面板 —— 1:1 对照 Adobe Illustrator 图层面板
```
# 类文档字符串 —— 完整对照 Ai 图层面板

```python
    
```
# 空行

```python
    对照 PDF 功能（共 26 章）：
```
# 此面板对照 PDF 文档中描述的 26 个章节功能

```python
    第二章 - 图层面板组成：图层名称、展开箭头、可见性(眼睛)、锁定、目标圆圈、选择圆圈、彩色方块
```
# 第二章：图层面板组成元素

```python
    第三章 - 新建图层：Create New Layer 按钮 + 面板菜单 New Layer
```
# 第三章：新建图层的两种方法

```python
    第四章 - 重命名图层：双击图层名称
```
# 第四章：双击重命名

```python
    第五章 - 删除图层：点击垃圾桶图标 / 拖动到垃圾桶
```
# 第五章：删除图层的两种方法

```python
    第六章 - 复制图层：拖动图层到 Create New Layer 按钮
```
# 第六章：拖拽复制

```python
    第七章 - 显示与隐藏图层：眼睛图标切换
```
# 第七章：可见性切换

```python
    第八章 - 锁定与解锁图层：锁定区域切换
```
# 第八章：锁定切换

```python
    第九章 - 图层排序：拖动图层上下移动
```
# 第九章：拖拽排序

```python
    第十章 - 子图层：New Sublayer 创建层级结构
```
# 第十章：子图层

```python
    第十一章 - 展开与折叠图层：三角箭头展开/折叠
```
# 第十一章：展开/折叠

```python
    第十二章 - 对象层级管理：展开图层后拖动对象调整顺序
```
# 第十二章：对象层级管理

```python
    第十三章 - 移动对象到其他图层：拖动彩色方块跨图层移动
```
# 第十三章：跨图层移动对象

```python
    第十四章 - 选择整个图层：点击目标圆圈全选图层对象
```
# 第十四章：全选图层对象

```python
    第十五章 - 收集到新图层：Collect in New Layer
```
# 第十五章：收集到新图层

```python
    第十六章 - 释放到图层：Release to Layers (Sequence/Build)
```
# 第十六章：释放到图层（顺序/构建模式）

```python
    第十七章 - 合并图层：Merge Selected Layers
```
# 第十七章：合并图层

```python
    第十八章 - 拼合图稿：Flatten Artwork
```
# 第十八章：拼合图稿

```python
    第十九章 - 模板图层：Template Layer（自动锁定+降低透明度）
```
# 第十九章：模板图层

```python
    第二十章 - 图层颜色：设置图层识别颜色
```
# 第二十章：图层颜色标识

```python
    第二十一章 - 打印控制：控制图层是否参与打印
```
# 第二十一章：打印控制

```python
    第二十二章 - 预览模式：Preview(正常)/Outline(轮廓)
```
# 第二十二章：预览模式

```python
    第二十三章 - 查找对象：选中对象时图层面板自动定位
```
# 第二十三章：自动定位

```python
    第二十四章 - 目标对象(Target)：指定效果作用对象
```
# 第二十四章：目标对象

```python
    第二十五章 - 图层与外观系统：图层级效果（阴影、模糊、透明度）
```
# 第二十五章：图层与外观系统

```python
    第二十六章 - 图层最佳实践：命名规范、项目结构
```
# 第二十六章：最佳实践

```python
    
```
# 空行

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
# 注意：不支持 `__slots__`

```python
    """
```
# 类文档字符串结束

```python

```
# 空行

```python
    layer_selected = pyqtSignal(int)
```
# 信号：图层被选中，参数为图层索引

```python
    layer_visibility_changed = pyqtSignal(int, bool)
```
# 信号：图层可见性变更，参数为索引和布尔值

```python
    layer_locked_changed = pyqtSignal(int, bool)
```
# 信号：图层锁定变更，参数为索引和布尔值

```python
    layer_add_requested = pyqtSignal()
```
# 信号：请求添加新图层

```python
    layer_remove_requested = pyqtSignal(int)
```
# 信号：请求删除图层，参数为索引

```python
    layer_duplicate_requested = pyqtSignal(int)
```
# 信号：请求复制图层，参数为源索引

```python
    layer_rename_requested = pyqtSignal(int, str)
```
# 信号：请求重命名图层，参数为索引和新名称

```python
    layer_reorder_requested = pyqtSignal(int, int)  # from_index, to_index
```
# 信号：请求图层重排序，参数为源位置和目标位置

```python
    layer_merge_requested = pyqtSignal(list)  # list of indices
```
# 信号：请求合并图层，参数为索引列表

```python
    layer_flatten_requested = pyqtSignal()
```
# 信号：请求拼合图稿

```python
    layer_collect_requested = pyqtSignal()
```
# 信号：请求收集到新图层

```python
    layer_release_sequence_requested = pyqtSignal()
```
# 信号：请求按顺序释放到图层

```python
    layer_release_build_requested = pyqtSignal()
```
# 信号：请求按构建释放到图层

```python
    item_move_to_layer = pyqtSignal(int)  # target layer index
```
# 信号：请求移动对象到目标图层

```python
    layer_select_all_requested = pyqtSignal(int)  # 选择整个图层的所有对象
```
# 信号：请求选中整个图层的所有对象

```python
    layer_target_requested = pyqtSignal(int)  # 设置目标图层（效果作用）
```
# 信号：请求设置目标图层

```python
    layer_color_changed = pyqtSignal(int, QColor)  # 图层颜色变更
```
# 信号：图层标识颜色变更

```python
    layer_template_changed = pyqtSignal(int, bool)  # 模板模式变更
```
# 信号：图层模板模式变更

```python
    layer_printable_changed = pyqtSignal(int, bool)  # 打印状态变更
```
# 信号：图层打印状态变更

```python
    layer_preview_mode_changed = pyqtSignal(int, str)  # 预览模式变更
```
# 信号：图层预览模式变更

```python
    layer_opacity_changed = pyqtSignal(int, float)  # 图层不透明度变更
```
# 信号：图层不透明度变更

```python
    item_order_changed = pyqtSignal(int, int, int)  # layer_index, from_pos, to_pos
```
# 信号：图层内对象顺序变更

```python
    item_delete_requested = pyqtSignal(object)       # GraphicItem - 删除对象
```
# 信号：请求删除对象

```python
    item_duplicate_requested = pyqtSignal(object)    # GraphicItem - 复制对象
```
# 信号：请求复制对象

```python
    item_select_requested = pyqtSignal(object)       # GraphicItem - 选中画布上的对象
```
# 信号：请求在画布上选中对象

```python
    item_visibility_toggled = pyqtSignal(object, bool)  # 对象显隐切换
```
# 信号：对象可见性切换

```python
    item_locked_toggled = pyqtSignal(object, bool)     # 对象锁定切换
```
# 信号：对象锁定切换

```python
    item_bring_forward_requested = pyqtSignal(object)   # 对象上移一层
```
# 信号：请求对象上移一层

```python
    item_send_backward_requested = pyqtSignal(object)   # 对象下移一层
```
# 信号：请求对象下移一层

```python

```
# 空行

```python
    LAYER_COLORS = [
```
# 类属性：预设的图层标识颜色列表

```python
        QColor(0, 120, 215),    # 蓝色
```
# 蓝色 (R=0, G=120, B=215)

```python
        QColor(220, 50, 50),    # 红色
```
# 红色 (R=220, G=50, B=50)

```python
        QColor(0, 150, 80),     # 绿色
```
# 绿色 (R=0, G=150, B=80)

```python
        QColor(255, 140, 0),    # 橙色
```
# 橙色 (R=255, G=140, B=0)

```python
        QColor(150, 50, 200),   # 紫色
```
# 紫色 (R=150, G=50, B=200)

```python
        QColor(0, 180, 180),    # 青色
```
# 青色 (R=0, G=180, B=180)

```python
        QColor(200, 100, 150),  # 粉色
```
# 粉色 (R=200, G=100, B=150)

```python
        QColor(139, 90, 43),    # 棕色
```
# 棕色 (R=139, G=90, B=43)

```python
    ]
```
# 颜色列表结束

```python

```
# 空行

```python
    def __init__(self, parent=None):
```
# 构造函数

```python
        super().__init__(parent)
```
# 调用父类构造函数

```python
        self._current_index = 0
```
# 初始化当前图层索引为 0（第一个图层）

```python
        self._layers_data: list[Layer] = []
```
# 初始化图层数据列表，类型为 `list[Layer]`

```python
        self._editing_index = -1  # 正在编辑名称的图层索引
```
# 正在编辑的图层索引，-1 表示无编辑

```python
        self._trash_bin: QPushButton | None = None  # 垃圾桶按钮（拖拽删除）
```
# 垃圾桶按钮引用，使用 `X | None` 语法（Python 3.10+）

```python
        self._init_ui()
```
# 调用 UI 初始化

```python

```
# 空行

```python
    def _init_ui(self):
```
# 私有方法，构建图层面板界面

```python
        layout = QVBoxLayout(self)
```
# 创建垂直主布局

```python
        layout.setContentsMargins(4, 4, 4, 4)
```
# 四周边距各 4px

```python
        layout.setSpacing(4)
```
# 控件间距 4px

```python

```
# 空行

```python
        # ── 标题栏 ──
```
# 标记：构建标题栏

```python
        title_layout = QHBoxLayout()
```
# 创建水平布局

```python
        title_layout.addWidget(QLabel("图层"))
```
# 添加"图层"标题标签

```python
        title_layout.addStretch()
```
# 弹性空白（标题左对齐）

```python

```
# 空行

```python
        # 图层菜单按钮
```
# 添加图层菜单按钮

```python
        self._menu_btn = QPushButton("☰")
```
# 汉堡菜单图标按钮

```python
        self._menu_btn.setFixedSize(24, 24)
```
# 固定尺寸 24×24

```python
        self._menu_btn.setToolTip("图层菜单")
```
# 工具提示"图层菜单"

```python
        self._menu_btn.clicked.connect(self._show_layer_menu)
```
# 点击连接到显示图层菜单方法

```python
        title_layout.addWidget(self._menu_btn)
```
# 添加到标题栏

```python

```
# 空行

```python
        layout.addLayout(title_layout)
```
# 将标题栏添加到主布局

```python

```
# 空行

```python
        # ── 图层树（使用 QTreeWidget 支持层级、拖拽、彩色方块） ──
```
# 标记：创建图层树控件

```python
        self._tree = QTreeWidget()
```
# 创建树形控件

```python
        self._tree.setHeaderHidden(True)
```
# 隐藏列标题

```python
        self._tree.setIndentation(20)
```
# 节点缩进 20px

```python
        self._tree.setRootIsDecorated(True)
```
# 显示根节点展开/折叠箭头

```python
        self._tree.setAnimated(True)
```
# 启用展开/折叠动画

```python
        self._tree.setDragEnabled(True)
```
# 启用拖拽

```python
        self._tree.setAcceptDrops(True)
```
# 启用接收拖放

```python
        self._tree.setDropIndicatorShown(True)
```
# 显示拖放位置指示器

```python
        self._tree.setDragDropMode(self._tree.InternalMove)
```
# 拖放模式：仅内部移动

```python
        self._tree.setSelectionMode(self._tree.ExtendedSelection)
```
# 选择模式：扩展选择（Ctrl/Shift 多选）

```python
        self._tree.setContextMenuPolicy(Qt.CustomContextMenu)
```
# 右键菜单策略：自定义

```python
        self._tree.customContextMenuRequested.connect(self._on_context_menu)
```
# 右键菜单信号连接到 `_on_context_menu`

```python
        self._tree.currentItemChanged.connect(self._on_item_changed)
```
# 选中项变更信号连接到 `_on_item_changed`

```python
        self._tree.itemDoubleClicked.connect(self._on_item_double_clicked)
```
# 双击信号连接到重命名方法

```python
        self._tree.itemChanged.connect(self._on_item_changed_flag)
```
# 数据变更信号连接到 `_on_item_changed_flag`

```python
        self._tree.model().rowsMoved.connect(self._on_rows_moved)
```
# 底层模型行移动信号连接到拖拽排序处理

```python
        # 点击目标圆圈全选图层（第十四章）
```
# 点击事件用于目标圆圈功能

```python
        self._tree.itemClicked.connect(self._on_item_clicked)
```
# 单击信号连接到 `_on_item_clicked`（可见性/锁定/对象选中）

```python
        layout.addWidget(self._tree)
```
# 将树控件添加到主布局

```python

```
# 空行

```python
        # ── 底部按钮栏（对照 Ai：Create New Layer / 垃圾桶 / 子图层 / 收集） ──
```
# 标记：创建底部按钮栏

```python
        bottom_layout = QHBoxLayout()
```
# 创建水平布局

```python
        bottom_layout.setSpacing(4)
```
# 按钮间距 4px

```python

```
# 空行

```python
        # Create New Layer 按钮（第三章方法1 — 新建图层，第六章 — 拖拽复制）
```
# 新建按钮，支持点击新建和拖拽复制

```python
        self._add_btn = QPushButton("+")
```
# 创建"+"按钮

```python
        self._add_btn.setFixedSize(28, 28)
```
# 固定尺寸 28×28

```python
        self._add_btn.setToolTip("创建新图层\n拖拽图层到此按钮可复制")
```
# 多行工具提示

```python
        self._add_btn.clicked.connect(self.layer_add_requested.emit)
```
# 点击发射新建图层信号

```python
        self._add_btn.setAcceptDrops(True)
```
# 启用拖放接收

```python
        self._add_btn.dragEnterEvent = self._on_add_btn_drag_enter
```
# 替换拖拽进入事件为自定义方法

```python
        self._add_btn.dragMoveEvent = self._on_add_btn_drag_move
```
# 替换拖拽移动事件

```python
        self._add_btn.dropEvent = self._on_add_btn_drop
```
# 替换拖放事件

```python
        bottom_layout.addWidget(self._add_btn)
```
# 添加到布局

```python

```
# 空行

```python
        # 垃圾桶按钮（第五章 — 删除图层，支持拖拽到垃圾桶删除）
```
# 垃圾桶按钮，支持点击删除和拖拽删除

```python
        self._trash_bin = QPushButton("🗑")
```
# 创建垃圾桶按钮，显示垃圾桶 emoji

```python
        self._trash_bin.setFixedSize(28, 28)
```
# 固定尺寸 28×28

```python
        self._trash_bin.setToolTip("删除选定图层\n拖拽图层到此按钮可删除")
```
# 多行工具提示

```python
        self._trash_bin.clicked.connect(
```
# 连接点击信号到 lambda

```python
            lambda: self.layer_remove_requested.emit(self._current_index),
```
# 点击发射删除信号，传递当前图层索引

```python
        )
```
# 连接结束

```python
        self._trash_bin.setAcceptDrops(True)
```
# 启用拖放接收

```python
        self._trash_bin.dragEnterEvent = self._on_trash_drag_enter
```
# 替换拖拽进入事件

```python
        self._trash_bin.dragMoveEvent = self._on_trash_drag_move
```
# 替换拖拽移动事件

```python
        self._trash_bin.dropEvent = self._on_trash_drop
```
# 替换拖放事件

```python
        bottom_layout.addWidget(self._trash_bin)
```
# 添加到布局

```python

```
# 空行

```python
        bottom_layout.addSpacing(8)
```
# 添加 8px 水平间距

```python

```
# 空行

```python
        self._sublayer_btn = QPushButton("子图层")
```
# 创建"子图层"按钮

```python
        self._sublayer_btn.setToolTip("新建子图层（第十章）")
```
# 工具提示引用第十章

```python
        self._sublayer_btn.clicked.connect(self._on_add_sublayer)
```
# 点击连接到添加子图层方法

```python
        bottom_layout.addWidget(self._sublayer_btn)
```
# 添加到布局

```python

```
# 空行

```python
        self._collect_btn = QPushButton("收集")
```
# 创建"收集"按钮

```python
        self._collect_btn.setToolTip("收集到新图层（第十五章）")
```
# 工具提示引用第十五章

```python
        self._collect_btn.clicked.connect(self.layer_collect_requested.emit)
```
# 点击直接发射收集信号

```python
        bottom_layout.addWidget(self._collect_btn)
```
# 添加到布局

```python

```
# 空行

```python
        layout.addLayout(bottom_layout)
```
# 将底部布局添加到主布局

```python

```
# 空行

```python
        self.setStyleSheet("""
```
# 设置图层面板整体 QSS 样式表

```python
            QTreeWidget { background-color: #2d2d2d; color: #ddd; border: 1px solid #555; outline: none; }
```
# 树控件样式：深灰背景、浅灰文字、灰色边框、无焦点轮廓

```python
            QTreeWidget::item { padding: 3px 2px; border-bottom: 1px solid #3a3a3a; }
```
# 树节点项样式：内边距、底部分隔线

```python
            QTreeWidget::item:selected { background-color: #0d6efd; color: white; }
```
# 选中项样式：蓝色背景、白色文字

```python
            QTreeWidget::item:hover { background-color: #3a3a3a; }
```
# 悬停样式：稍亮灰色背景

```python
            QTreeWidget::branch:has-children:!has-siblings:closed,
```
# 分支选择器：有子节点无兄弟的关闭状态

```python
            QTreeWidget::branch:closed:has-children:has-siblings { border-image: none; }
```
# 分支选择器：有子节点有兄弟的关闭状态；两者都移除默认箭头装饰

```python
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; border-radius: 3px; font-weight: bold; padding: 2px 6px; }
```
# 通用按钮样式

```python
            QPushButton:hover { background-color: #5a5a5a; }
```
# 按钮悬停

```python
            QPushButton#trash_hover { background-color: #dc3545; border-color: #dc3545; }
```
# 垃圾桶悬停状态（通过对象 ID）

```python
            QPushButton#add_hover { background-color: #0d6efd; border-color: #0d6efd; }
```
# 新建按钮悬停状态（通过对象 ID）

```python
            QLineEdit { background-color: #3c3c3c; color: #ddd; border: 1px solid #0d6efd; padding: 2px; }
```
# 行编辑框样式（重命名时）

```python
        """)
```
# 样式表结束

```python

```
# 空行

```python
    # ── 更新图层列表 ──
```
# 标记：更新图层列表相关方法

```python

```
# 空行

```python
    def update_layers(self, layers: list[Layer], active_index: int):
```
# 公共方法：刷新图层面板显示，参数为图层列表和活跃图层索引

```python
        """更新图层树，显示图层及子图层的层级结构（对照第二章图层面板组成）"""
```
# 方法文档字符串

```python
        self._layers_data = layers
```
# 保存图层数据到内部属性

```python
        self._tree.blockSignals(True)
```
# 阻塞树控件信号（防止重建时触发事件）

```python
        self._tree.clear()
```
# 清空所有现有节点

```python

```
# 空行

```python
        for i, layer in enumerate(layers):
```
# 遍历图层列表

```python
            item = self._create_layer_item(layer, i)
```
# 为每个图层创建树节点

```python
            self._tree.addTopLevelItem(item)
```
# 添加为顶层节点

```python
            if i == active_index:
```
# 如果是活跃图层

```python
                self._tree.setCurrentItem(item)
```
# 设为当前选中项

```python
            # 展开/折叠（第十一章）
```
# 处理第十一章展开/折叠

```python
            item.setExpanded(layer.expanded)
```
# 根据 expanded 属性设置展开状态

```python

```
# 空行

```python
        self._tree.blockSignals(False)
```
# 恢复树控件信号

```python
        self._current_index = active_index
```
# 更新当前索引

```python
        
```
# 空行

```python
        # 第二十三章 - 查找对象：选中对象时图层面板自动定位到对应图层
```
# 实现第二十三章自动定位

```python
        if 0 <= active_index < len(layers):
```
# 确保索引有效

```python
            active_item = self._tree.topLevelItem(active_index)
```
# 获取活跃图层的树节点

```python
            if active_item:
```
# 如果节点存在

```python
                self._tree.scrollToItem(active_item, QTreeWidget.PositionAtCenter)
```
# 滚动到该节点并居中显示

```python

```
# 空行

```python
    def _create_layer_item(self, layer: Layer, index: int) -> QTreeWidgetItem:
```
# 私有方法：为单个图层创建树节点

```python
        """创建图层树节点，1:1 对照 Ai 图层面板
```
# 方法文档字符串

```python
        
```
# 空行

```python
        Ai 图层面板结构（从左到右）：
```
# Ai 面板结构说明

```python
        1. 展开箭头 (▶) — 展开/折叠图层内容（第十一章）
```
# 结构 1：展开箭头

```python
        2. 眼睛图标 (👁) — 可见性（第七章）
```
# 结构 2：可见性眼睛

```python
        3. 锁定区域 (🔒) — 锁定状态（第八章）
```
# 结构 3：锁定图标

```python
        4. 目标圆圈 (◎) — 效果作用目标（第二十四章）
```
# 结构 4：目标圆圈

```python
        5. 图层颜色方块 — 标识图层（第二十章）
```
# 结构 5：颜色方块

```python
        6. 图层名称 — 双击可重命名（第四章）
```
# 结构 6：图层名称

```python
        """
```
# 文档字符串结束

```python
        # 可见性图标（第七章）
```
# 生成可见性图标

```python
        eye = "👁" if layer.visible else "  "  # 不可见时留空（Ai 行为）
```
# 可见显示眼睛 emoji，不可见显示两个空格

```python
        # 锁定图标（第八章）
```
# 生成锁定图标

```python
        lock = "🔒" if layer.locked else "  "
```
# 已锁定显示锁 emoji，否则显示空格

```python
        # 模板图标（第十九章）
```
# 生成模板图标

```python
        template = "📐" if layer.is_template else " "
```
# 模板图层显示三角尺 emoji

```python
        # 预览模式标识（第二十二章）
```
# 生成预览模式标识

```python
        preview_indicator = "◉" if layer.preview_mode == "outline" else "◎"
```
# 轮廓模式显示实心圆，预览模式显示空心圆

```python
        # 打印状态（第二十一章）— 不可打印用斜体标识
```
# 生成打印状态标识

```python
        print_indicator = "" if layer.printable else "✕ "
```
# 不可打印显示叉号

```python
        
```
# 空行

```python
        name = layer.name
```
# 获取图层名称

```python
        
```
# 空行

```python
        # 显示对象数量
```
# 计算显示信息

```python
        item_count = len(layer.items)
```
# 获取对象数量

```python
        sub_count = len(layer.sublayers)
```
# 获取子图层数量

```python
        detail = f" ({item_count})" if item_count > 0 else ""
```
# 有对象时附加 " (数量)"

```python
        sub_detail = f" [{sub_count}]" if sub_count > 0 else ""
```
# 有子图层时附加 " [数量]"

```python
        
```
# 空行

```python
        # 拼合显示文本：眼睛 锁 目标 名称 数量
```
# 组合显示文本

```python
        display_text = f"{eye}{lock}{preview_indicator} {print_indicator}{name}{detail}{sub_detail}"
```
# 拼接完整显示文本

```python
        
```
# 空行

```python
        item = QTreeWidgetItem([display_text])
```
# 用显示文本创建树节点

```python
        item.setData(0, Qt.UserRole, index)
```
# 设置 UserRole 数据为图层索引

```python
        item.setData(0, Qt.UserRole + 1, "layer")
```
# UserRole+1 为 "layer"（标识节点类型）

```python
        item.setData(0, Qt.UserRole + 2, layer.id)
```
# UserRole+2 为图层唯一 ID

```python
        item.setData(0, Qt.UserRole + 4, layer.color.name() if layer.color else "")  # 彩色方块数据
```
# UserRole+4 为图层颜色名称（用于彩色方块）

```python

```
# 空行

```python
        # 图层颜色标识（第二十章）— 路径边框颜色
```
# 设置图层颜色标识

```python
        if layer.color:
```
# 如果有图层颜色

```python
            item.setForeground(0, layer.color)
```
# 文字颜色设为图层颜色

```python
        if layer.is_template:
```
# 如果是模板图层

```python
            # 模板图层灰色显示（第十九章）
```
# 模板图层灰色显示

```python
            item.setForeground(0, QColor(128, 128, 128))
```
# 覆盖为中灰色

```python
        if not layer.printable:
```
# 如果不可打印

```python
            # 不打印的图层用斜体显示（第二十一章）
```
# 斜体显示

```python
            font = item.font(0)
```
# 获取当前字体

```python
            font.setItalic(True)
```
# 设为斜体

```python
            item.setFont(0, font)
```
# 设置回节点

```python
        if layer.preview_mode == "outline":
```
# 如果是轮廓模式

```python
            # 轮廓模式用不同背景色提示（第二十二章）
```
# 特殊背景色

```python
            item.setBackground(0, QColor(50, 45, 40))
```
# 暗色背景

```python

```
# 空行

```python
        # 子图层（第十章）
```
# 添加子图层节点

```python
        for si, sub in enumerate(layer.sublayers):
```
# 遍历子图层

```python
            sub_item = self._create_sublayer_item(sub, index, si)
```
# 创建子图层节点

```python
            item.addChild(sub_item)
```
# 添加为子节点

```python

```
# 空行

```python
        # 对象列表（展开图层可查看路径、文字、图像等 — 第十一章、第十二章）
```
# 添加对象列表

```python
        if layer.expanded and layer.items:
```
# 如果图层已展开且有对象

```python
            for oi, obj in enumerate(layer.items):
```
# 遍历对象

```python
                obj_type = obj.item_type.replace("Item", "")
```
# 获取类型名（去掉 "Item" 后缀）

```python
                obj_name = obj.name or f"<{obj_type}>"
```
# 有名称用名称，否则用类型名
                
```python
                # 对象锁定图标
```
# 对象锁定图标

```python
                obj_lock = "🔒 " if obj.locked else ""
```
# 已锁定显示锁 emoji

```python
                # 对象类型图标
```
# 获取类型图标

```python
                type_icon = self._get_item_type_icon(obj)
```
# 调用方法获取类型图标

```python
                
```
# 空行

```python
                obj_item = QTreeWidgetItem([f"    {obj_lock}{type_icon} {obj_name}"])
```
# 创建对象节点，4空格缩进 + 图标 + 名称

```python
                obj_item.setData(0, Qt.UserRole, oi)
```
# UserRole 为对象索引

```python
                obj_item.setData(0, Qt.UserRole + 1, "object")
```
# UserRole+1 为 "object"

```python
                obj_item.setData(0, Qt.UserRole + 2, obj.id)
```
# UserRole+2 为对象 ID

```python
                obj_item.setData(0, Qt.UserRole + 3, index)  # 父图层索引
```
# UserRole+3 为父图层索引

```python
                
```
# 空行

```python
                # 对象使用图层颜色（第二十章）— 彩色方块
```
# 对象使用图层颜色

```python
                if layer.color:
```
# 如果图层有颜色

```python
                    obj_item.setForeground(0, QColor(
```
# 设置对象文字颜色（带透明度）

```python
                        layer.color.red(), layer.color.green(),
```
# 取图层颜色的红、绿分量

```python
                        layer.color.blue(), 180
```
# Alpha 设为 180（约 70% 不透明度），比图层名稍淡

```python
                    ))
```
# QColor 构造和 setForeground 结束

```python
                
```
# 空行

```python
                # 对象可拖拽排序（第十二章 — 对象层级管理）
```
# 启用对象拖拽排序

```python
                obj_item.setFlags(obj_item.flags() | Qt.ItemIsDragEnabled)
```
# 添加可拖拽标志

```python
                
```
# 空行

```python
                item.addChild(obj_item)
```
# 将对象节点添加为子节点

```python

```
# 空行

```python
        # 图层项可拖拽（第九章 — 图层排序）
```
# 启用图层拖拽排序

```python
        item.setFlags(item.flags() | Qt.ItemIsDragEnabled)
```
# 添加可拖拽标志

```python
        
```
# 空行

```python
        return item
```
# 返回创建完成的树节点

```python

```
# 空行

```python
    @staticmethod
```
# 静态方法装饰器

```python
    def _get_item_type_icon(obj) -> str:
```
# 根据图形对象类型返回 emoji 图标字符串

```python
        """获取对象类型图标（第十一章）"""
```
# 方法文档字符串

```python
        from ..core.graphics import PathItem, RectangleItem, EllipseItem, TextFrame, GroupItem
```
# 延迟导入（避免循环导入）

```python
        match obj:
```
# 使用 match-case 模式匹配

```python
            case PathItem():
```
# 匹配路径对象

```python
                return "✏"  # 路径
```
# 返回铅笔 emoji

```python
            case RectangleItem():
```
# 匹配矩形对象

```python
                return "▬"  # 矩形
```
# 返回实心矩形符号

```python
            case EllipseItem():
```
# 匹配椭圆对象

```python
                return "⬭"  # 椭圆
```
# 返回椭圆符号

```python
            case TextFrame():
```
# 匹配文本对象

```python
                return "T"  # 文字
```
# 返回字母 T

```python
            case GroupItem():
```
# 匹配群组对象

```python
                return "📁"  # 群组
```
# 返回文件夹 emoji

```python
            case _:
```
# 默认分支（通配符）

```python
                return "●"  # 默认
```
# 返回实心圆点

```python

```
# 空行

```python
    def _create_sublayer_item(self, sublayer: Layer, parent_idx: int, sub_idx: int) -> QTreeWidgetItem:
```
# 私有方法：为子图层创建树节点

```python
        """创建子图层树节点（第十章）"""
```
# 方法文档字符串

```python
        eye = "👁" if sublayer.visible else "  "
```
# 子图层可见性图标

```python
        lock = "🔒" if sublayer.locked else "  "
```
# 子图层锁定图标

```python
        preview_indicator = "◎"
```
# 预览标识默认为空心圆

```python
        
```
# 空行

```python
        item = QTreeWidgetItem([f"{eye}{lock}{preview_indicator} {sublayer.name}"])
```
# 创建子图层节点

```python
        item.setData(0, Qt.UserRole, sub_idx)
```
# UserRole 为子图层索引

```python
        item.setData(0, Qt.UserRole + 1, "sublayer")
```
# UserRole+1 为 "sublayer"

```python
        item.setData(0, Qt.UserRole + 2, sublayer.id)
```
# UserRole+2 为子图层 ID

```python
        item.setData(0, Qt.UserRole + 3, parent_idx)
```
# UserRole+3 为父图层索引

```python
        
```
# 空行

```python
        if sublayer.color:
```
# 如果子图层有颜色

```python
            item.setForeground(0, sublayer.color)
```
# 设置文字颜色

```python
        
```
# 空行

```python
        # 子图层也可拖拽排序
```
# 子图层支持拖拽排序

```python
        item.setFlags(item.flags() | Qt.ItemIsDragEnabled)
```
# 添加可拖拽标志

```python
        
```
# 空行

```python
        return item
```
# 返回子图层树节点

```python

```
# 空行

```python
    # ── 事件处理 ──
```
# 标记：事件处理方法区域

```python

```
# 空行

```python
    def _on_item_changed(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
```
# 处理树控件选中项变更事件

```python
        if current is None:
```
# 如果没有选中项

```python
            return
```
# 返回

```python
        item_type = current.data(0, Qt.UserRole + 1)
```
# 获取节点类型

```python
        if item_type == "layer":
```
# 如果是图层节点

```python
            index = current.data(0, Qt.UserRole)
```
# 获取图层索引

```python
            if index is not None:
```
# 索引有效

```python
                self._current_index = index
```
# 更新当前索引

```python
                self.layer_selected.emit(index)
```
# 发射图层选中信号

```python
        elif item_type == "sublayer":
```
# 如果是子图层节点

```python
            parent_idx = current.data(0, Qt.UserRole + 3)
```
# 获取父图层索引

```python
            if parent_idx is not None:
```
# 索引有效

```python
                self._current_index = parent_idx
```
# 更新当前索引为父图层

```python
                self.layer_selected.emit(parent_idx)
```
# 发射图层选中信号

```python

```
# 空行

```python
    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
```
# 处理树节点双击事件

```python
        """双击重命名图层（PDF 六）"""
```
# 方法文档字符串

```python
        item_type = item.data(0, Qt.UserRole + 1)
```
# 获取节点类型

```python
        if item_type in ("layer", "sublayer"):
```
# 图层或子图层才能重命名

```python
            index = item.data(0, Qt.UserRole)
```
# 获取索引

```python
            self._start_rename(item, item_type, index)
```
# 启动内联重命名

```python

```
# 空行

```python
    def _start_rename(self, item: QTreeWidgetItem, item_type: str, index: int):
```
# 私有方法：启动内联重命名编辑

```python
        """启动内联重命名"""
```
# 方法文档字符串

```python
        from PyQt5.QtWidgets import QLineEdit
```
# 延迟导入 QLineEdit

```python
        current_text = ""
```
# 初始化当前文本为空

```python
        if item_type == "layer" and index < len(self._layers_data):
```
# 图层类型且索引有效

```python
            current_text = self._layers_data[index].name
```
# 获取当前图层名称

```python
        elif item_type == "sublayer":
```
# 子图层类型

```python
            parent_idx = item.data(0, Qt.UserRole + 3)
```
# 获取父图层索引

```python
            if parent_idx is not None and parent_idx < len(self._layers_data):
```
# 父图层索引有效

```python
                parent = self._layers_data[parent_idx]
```
# 获取父图层对象

```python
                if index < len(parent.sublayers):
```
# 子图层索引有效

```python
                    current_text = parent.sublayers[index].name
```
# 获取子图层名称

```python

```
# 空行

```python
        editor = QLineEdit(current_text, self._tree)
```
# 创建行编辑框，初始文本为当前名称

```python
        editor.setFocus()
```
# 设置焦点

```python
        editor.selectAll()
```
# 全选文本

```python
        self._tree.setItemWidget(item, 0, editor)
```
# 将编辑框设为节点的内嵌控件

```python
        self._editing_index = index
```
# 记录正在编辑的索引

```python

```
# 空行

```python
        def finish_rename():
```
# 嵌套函数：完成重命名

```python
            new_name = editor.text().strip()
```
# 获取新名称（去除首尾空白）

```python
            try:
```
# try 块

```python
                # 检查 item 是否仍然有效
```
# 检查节点是否还存在

```python
                if item not in self._tree.findItems("", Qt.MatchContains | Qt.MatchRecursive, 0):
```
# 通过搜索判断节点是否仍存在于树中

```python
                    return
```
# 节点已删除则返回

```python
                self._tree.removeItemWidget(item, 0)
```
# 移除内嵌编辑控件

```python
            except RuntimeError:
```
# 捕获 C++ 对象已销毁的错误

```python
                return
```
# 返回

```python
            if new_name and new_name != current_text:
```
# 新名称非空且与旧名称不同

```python
                if item_type == "layer":
```
# 图层类型

```python
                    self.layer_rename_requested.emit(index, new_name)
```
# 发射图层重命名信号

```python
                elif item_type == "sublayer":
```
# 子图层类型

```python
                    self.layer_rename_requested.emit(-(index + 1), new_name)
```
# 用负数索引区分子图层重命名

```python

```
# 空行

```python
        editor.returnPressed.connect(finish_rename)
```
# 回车键确认重命名

```python
        editor.editingFinished.connect(lambda: None)  # 防止重复触发
```
# 空连接防止 editingFinished 重复触发

```python

```
# 空行

```python
    def _on_item_changed_flag(self, item: QTreeWidgetItem, column: int):
```
# 处理项目数据变更事件

```python
        """项目状态改变（预留）"""
```
# 预留接口

```python
        pass
```
# 空操作占位

```python

```
# 空行

```python
    def _on_rows_moved(self, parent, start, end, dest, row):
```
# 处理拖拽排序完成事件

```python
        """拖拽排序图层（第九章）或对象排序（第十二章）"""
```
# 方法文档字符串

```python
        if start != row:
```
# 如果位置确实发生变化

```python
            # 判断是图层排序还是对象排序
```
# 需区分图层和对象排序

```python
            item = self._tree.topLevelItem(start) if start < self._tree.topLevelItemCount() else None
```
# 根据起始行获取顶层节点

```python
            if item:
```
# 如果节点存在

```python
                item_type = item.data(0, Qt.UserRole + 1)
```
# 获取节点类型

```python
                if item_type == "layer":
```
# 图层排序

```python
                    self.layer_reorder_requested.emit(start, row)
```
# 发射图层重排序信号

```python
                elif item_type == "object":
```
# 对象排序

```python
                    # 对象层级管理（第十二章）
```
# 第十二章功能

```python
                    layer_idx = item.data(0, Qt.UserRole + 3)
```
# 获取所属图层索引

```python
                    if layer_idx is not None:
```
# 索引有效

```python
                        self.item_order_changed.emit(layer_idx, start, row)
```
# 发射对象顺序变更信号

```python

```
# 空行

```python
    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
```
# 处理树节点单击事件（核心交互方法）

```python
        """点击图层项处理
```
# 方法文档字符串

```python
        
```
# 空行

```python
        核心功能（实际生效）：
```
# 核心功能列表

```python
        - 点击 👁 眼睛区域 → 切换图层/对象可见性
```
# 功能 1：切换可见性

```python
        - 点击 🔒 锁定区域 → 切换图层/对象锁定状态  
```
# 功能 2：切换锁定

```python
        - 点击对象名称 → 选中画布上的对应对象
```
# 功能 3：选中画布对象

```python
        - 点击图层行 → 设置目标图层
```
# 功能 4：设置目标图层

```python
        """
```
# 文档字符串结束

```python
        item_type = item.data(0, Qt.UserRole + 1)
```
# 获取节点类型

```python
        
```
# 空行

```python
        # 获取点击位置（相对于 tree item 的局部坐标）
```
# 获取点击的相对位置

```python
        # 使用 QCursor.pos() 获取当前全局鼠标位置，避免依赖 mousePressEvent
```
# 说明使用 QCursor 获取全局位置

```python
        pos = self._tree.mapFromGlobal(QCursor.pos())
```
# 全局坐标转为树控件局部坐标

```python
        item_rect = self._tree.visualItemRect(item)
```
# 获取节点的视觉矩形区域

```python
        click_x = pos.x() - item_rect.x()
```
# 计算相对于节点左边缘的水平偏移

```python
        # 眼睛图标和锁定图标在前面的固定宽度区域
```
# 图标区域说明

```python
        # 缩进 + 眼睛(~16px) + 锁定(~16px) = 约 52px 范围内为图标区
```
# 图标区域宽度计算

```python
        indent = 20 if item.parent() else 0  # 子节点有额外缩进
```
# 子节点缩进 20px，顶层为 0

```python
        eye_lock_region = indent + 36  # 眼睛+锁定图标的总宽度
```
# 图标区域总宽度 = 缩进 + 36px

```python
        
```
# 空行

```python
        if item_type == "layer":
```
# 点击的是图层节点

```python
            index = item.data(0, Qt.UserRole)
```
# 获取图层索引

```python
            if index is None or not (0 <= index < len(self._layers_data)):
```
# 索引无效检查

```python
                return
```
# 返回

```python
            layer = self._layers_data[index]
```
# 获取图层对象

```python
            
```
# 空行

```python
            if click_x <= eye_lock_region:
```
# 点击在图标区域内

```python
                # 判断是点眼睛还是锁定区域
```
# 区分眼睛和锁定

```python
                if click_x <= indent + 18:
```
# 点击在左半区域（眼睛图标）

```python
                    # 眼睛区域 → 切换可见性
```
# 切换可见性

```python
                    layer.visible = not layer.visible
```
# 取反可见性

```python
                    self.layer_visibility_changed.emit(index, layer.visible)
```
# 发射可见性变更信号

```python
                    self._refresh_display()
```
# 刷新显示

```python
                else:
```
# 点击在右半区域（锁定图标）

```python
                    # 锁定区域 → 切换锁定
```
# 切换锁定

```python
                    layer.locked = not layer.locked
```
# 取反锁定状态

```python
                    self.layer_locked_changed.emit(index, layer.locked)
```
# 发射锁定变更信号

```python
                    self._refresh_display()
```
# 刷新显示

```python
            else:
```
# 点击在名称区域

```python
                # 点击名称区域 → 设置目标图层
```
# 设置目标图层

```python
                self.layer_target_requested.emit(index)
```
# 发射目标图层信号

```python
                
```
# 空行

```python
        elif item_type == "object":
```
# 点击的是对象节点

```python
            obj_index = item.data(0, Qt.UserRole)
```
# 获取对象索引

```python
            layer_index = item.data(0, Qt.UserRole + 3)
```
# 获取所属图层索引

```python
            if layer_index is None or not (0 <= layer_index < len(self._layers_data)):
```
# 图层索引无效检查

```python
                return
```
# 返回

```python
            layer = self._layers_data[layer_index]
```
# 获取图层对象

```python
            if obj_index is None or not (0 <= obj_index < len(layer.items)):
```
# 对象索引无效检查

```python
                return
```
# 返回

```python
            obj = layer.items[obj_index]
```
# 获取图形对象

```python
            
```
# 空行

```python
            if click_x <= eye_lock_region:
```
# 点击在图标区域

```python
                if click_x <= indent + 18:
```
# 点击在眼睛区域

```python
                    # 眼睛区域 → 切换对象可见性
```
# 切换对象可见性

```python
                    obj.visible = not obj.visible
```
# 取反可见性

```python
                    self.item_visibility_toggled.emit(obj, obj.visible)
```
# 发射对象可见性切换信号

```python
                    self._refresh_display()
```
# 刷新显示

```python
                else:
```
# 点击在锁定区域

```python
                    # 锁定区域 → 切换对象锁定
```
# 切换对象锁定

```python
                    obj.locked = not obj.locked
```
# 取反锁定

```python
                    self.item_locked_toggled.emit(obj, obj.locked)
```
# 发射对象锁定切换信号

```python
                    self._refresh_display()
```
# 刷新显示

```python
            else:
```
# 点击在名称区域

```python
                # 点击对象名称 → 选中画布上的该对象
```
# 选中画布上的对象

```python
                self.item_select_requested.emit(obj)
```
# 发射对象选中请求信号

```python

```
# 空行

```python
    def _refresh_display(self):
```
# 私有方法：刷新图层面板显示

```python
        """刷新图层面板显示"""
```
# 方法文档字符串

```python
        self.update_layers(self._layers_data, self._current_index)
```
# 用当前数据重新调用 update_layers 刷新

```python

```
# 空行

```python
    def mousePressEvent(self, event):
```
# 重写鼠标按下事件

```python
        """记录鼠标按下位置，供 _on_item_clicked 使用"""
```
# 方法文档字符串

```python
        self._cursor_pos = self._tree.mapToGlobal(event.pos())
```
# 局部坐标转全局坐标并保存

```python
        super().mousePressEvent(event)
```
# 调用父类默认处理

```python

```
# 空行

```python
    # ── 拖拽到垃圾桶删除（第五章方法2） ──
```
# 标记：拖拽到垃圾桶删除功能

```python

```
# 空行

```python
    def _on_trash_drag_enter(self, event):
```
# 垃圾桶按钮拖拽进入事件

```python
        """拖拽到垃圾桶时的视觉反馈"""
```
# 提供视觉反馈

```python
        if self._trash_bin:
```
# 如果垃圾桶按钮存在

```python
            self._trash_bin.setStyleSheet("""
```
# 设置红色高亮样式

```python
                QPushButton { background-color: #dc3545; color: white; 
```
# 红色背景、白色文字

```python
                border: 2px solid #ff4444; border-radius: 3px; font-weight: bold; }
```
# 红色边框、圆角、粗体

```python
            """)
```
# 样式表结束

```python

```
# 空行

```python
    def _on_trash_drag_move(self, event):
```
# 垃圾桶按钮拖拽移动事件

```python
        event.accept()
```
# 接受拖拽移动

```python

```
# 空行

```python
    def _on_trash_drop(self, event):
```
# 垃圾桶按钮拖放完成事件

```python
        """拖拽图层到垃圾桶删除（第五章方法2）"""
```
# 方法文档字符串

```python
        if self._trash_bin:
```
# 如果垃圾桶存在

```python
            self._trash_bin.setStyleSheet("")
```
# 清除高亮样式，恢复默认

```python
        # 获取当前选中的图层
```
# 获取待删除图层

```python
        idx = self._current_index
```
# 当前选中图层索引

```python
        if 0 <= idx < len(self._layers_data):
```
# 索引有效

```python
            self.layer_remove_requested.emit(idx)
```
# 发射删除请求信号

```python
        event.accept()
```
# 接受拖放事件

```python

```
# 空行

```python
    # ── 拖拽到新建按钮复制（第六章） ──
```
# 标记：拖拽到新建按钮复制功能

```python

```
# 空行

```python
    def _on_add_btn_drag_enter(self, event):
```
# 新建按钮拖拽进入事件

```python
        """拖拽到新建按钮时的视觉反馈"""
```
# 提供视觉反馈

```python
        if self._add_btn:
```
# 如果新建按钮存在

```python
            self._add_btn.setStyleSheet("""
```
# 设置蓝色高亮样式

```python
                QPushButton { background-color: #0d6efd; color: white; 
```
# 蓝色背景、白色文字

```python
                border: 2px solid #4da3ff; border-radius: 3px; font-weight: bold; }
```
# 浅蓝边框、圆角、粗体

```python
            """)
```
# 样式表结束

```python

```
# 空行

```python
    def _on_add_btn_drag_move(self, event):
```
# 新建按钮拖拽移动事件

```python
        event.accept()
```
# 接受拖拽

```python

```
# 空行

```python
    def _on_add_btn_drop(self, event):
```
# 新建按钮拖放完成事件

```python
        """拖拽图层到新建按钮复制（第六章）"""
```
# 方法文档字符串

```python
        if self._add_btn:
```
# 如果按钮存在

```python
            self._add_btn.setStyleSheet("")
```
# 清除高亮样式

```python
        idx = self._current_index
```
# 当前图层索引

```python
        if 0 <= idx < len(self._layers_data):
```
# 索引有效

```python
            self.layer_duplicate_requested.emit(idx)
```
# 发射复制请求信号

```python
        event.accept()
```
# 接受拖放

```python

```
# 空行

```python
    # ── 右键菜单（完整对照 Ai 图层面板菜单） ──
```
# 标记：右键菜单功能

```python

```
# 空行

```python
    def _on_context_menu(self, pos):
```
# 处理右键菜单事件

```python
        """右键菜单：完整图层和对象操作
```
# 方法文档字符串

```python
        
```
# 空行

```python
        图层操作：新建/复制/删除/重命名/合并/拼合等
```
# 支持的图层操作

```python
        对象操作：选中/删除/复制/显隐/锁定/上下移动
```
# 支持的对象操作

```python
        """
```
# 文档字符串结束

```python
        item = self._tree.itemAt(pos)
```
# 根据坐标获取右键点击的节点（空白区域为 None）

```python
        menu = QMenu(self)
```
# 创建弹出菜单

```python
        menu.setStyleSheet("""
```
# 设置菜单 QSS 样式

```python
            QMenu { background-color: #3c3c3c; color: #ddd; border: 1px solid #555; padding: 4px; }
```
# 菜单背景、文字、边框样式

```python
            QMenu::item { padding: 6px 24px; }
```
# 菜单项内边距

```python
            QMenu::item:selected { background-color: #0d6efd; }
```
# 菜单项选中样式

```python
            QMenu::separator { height: 1px; background: #555; margin: 4px 8px; }
```
# 分隔线样式

```python
        """)
```
# 样式表结束

```python

```
# 空行

```python
        idx = self._current_index
```
# 当前图层索引

```python
        layer = self._layers_data[idx] if 0 <= idx < len(self._layers_data) else None
```
# 获取当前图层对象（无效则为 None）

```python

```
# 空行

```python
        item_type = item.data(0, Qt.UserRole + 1) if item else None
```
# 获取节点类型（无节点则为 None）

```python

```
# 空行

```python
        if item_type == "object":
```
# 右键点击对象节点 → 对象级菜单

```python
            # ── 对象级右键菜单 ──
```
# 构建对象级右键菜单

```python
            obj_index = item.data(0, Qt.UserRole)
```
# 对象索引

```python
            layer_index = item.data(0, Qt.UserRole + 3)
```
# 所属图层索引

```python
            if (layer_index is not None and 0 <= layer_index < len(self._layers_data)
```
# 验证图层索引有效（条件开始）

```python
                    and obj_index is not None and 0 <= obj_index < len(self._layers_data[layer_index].items)):
```
# 验证对象索引有效（条件继续）

```python
                obj = self._layers_data[layer_index].items[obj_index]
```
# 获取图形对象

```python
                obj_name = obj.name or f"<{obj.item_type.replace('Item', '')}>"
```
# 获取对象名称（无名称则用类型名）
                
```python
                # 选中对象
```
# 菜单项：选中对象

```python
                sel_action = menu.addAction(f"  选中「{obj_name}」")
```
# 添加"选中"菜单项

```python
                sel_action.triggered.connect(lambda: self.item_select_requested.emit(obj))
```
# 触发时发射对象选中信号
                
```python
                menu.addSeparator()
```
# 添加分隔线
                
```python
                # 删除对象
```
# 菜单项：删除对象

```python
                del_action = menu.addAction(f"  删除「{obj_name}」")
```
# 添加"删除"菜单项

```python
                del_action.triggered.connect(lambda: self.item_delete_requested.emit(obj))
```
# 触发时发射对象删除信号
                
```python
                # 复制对象
```
# 菜单项：复制对象

```python
                dup_action = menu.addAction(f"  复制「{obj_name}」")
```
# 添加"复制"菜单项

```python
                dup_action.triggered.connect(lambda: self.item_duplicate_requested.emit(obj))
```
# 触发时发射对象复制信号
                
```python
                menu.addSeparator()
```
# 添加分隔线
                
```python
                # 显隐切换
```
# 菜单项：显隐切换

```python
                vis_text = f"  隐藏「{obj_name}」" if obj.visible else f"  显示「{obj_name}」"
```
# 根据当前可见性生成菜单文本

```python
                vis_action = menu.addAction(vis_text)
```
# 添加显隐菜单项

```python
                vis_action.triggered.connect(lambda: self.item_visibility_toggled.emit(obj, not obj.visible))
```
# 触发时切换可见性
                
```python
                # 锁定切换
```
# 菜单项：锁定切换

```python
                lock_text = f"  锁定「{obj_name}」" if not obj.locked else f"  解锁「{obj_name}」"
```
# 根据当前锁定状态生成菜单文本

```python
                lock_action = menu.addAction(lock_text)
```
# 添加锁定菜单项

```python
                lock_action.triggered.connect(lambda: self.item_locked_toggled.emit(obj, not obj.locked))
```
# 触发时切换锁定
                
```python
                menu.addSeparator()
```
# 添加分隔线
                
```python
                # 上移一层
```
# 菜单项：上移一层

```python
                up_action = menu.addAction("  上移一层 (Bring Forward)")
```
# 添加"上移一层"菜单项

```python
                up_action.triggered.connect(lambda: self.item_bring_forward_requested.emit(obj))
```
# 触发时发射对象上移信号
                
```python
                # 下移一层
```
# 菜单项：下移一层

```python
                down_action = menu.addAction("  下移一层 (Send Backward)")
```
# 添加"下移一层"菜单项

```python
                down_action.triggered.connect(lambda: self.item_send_backward_requested.emit(obj))
```
# 触发时发射对象下移信号
                
```python
                # 置顶
```
# 菜单项：置顶

```python
                front_action = menu.addAction("  置顶 (Bring to Front)")
```
# 添加"置顶"菜单项

```python
                front_action.triggered.connect(lambda: self._on_item_bring_to_front(obj, layer_index))
```
# 触发时调用置顶方法
                
```python
                # 置底
```
# 菜单项：置底

```python
                back_action = menu.addAction("  置底 (Send to Back)")
```
# 添加"置底"菜单项

```python
                back_action.triggered.connect(lambda: self._on_item_send_to_back(obj, layer_index))
```
# 触发时调用置底方法

```python

```
# 空行

```python
        elif item_type in ("layer", "sublayer"):
```
# 右键点击图层/子图层节点 → 图层级菜单

```python
            # ── 图层级右键菜单（原有功能）──
```
# 构建图层级右键菜单

```python
            # 新建图层（第三章方法2）
```
# 菜单项：新建图层

```python
            new_layer_action = menu.addAction("  新建图层")
```
# 添加"新建图层"

```python
            new_layer_action.triggered.connect(self.layer_add_requested.emit)
```
# 触发时发射新建信号

```python

```
# 空行

```python
            # 新建子图层（第十章）
```
# 菜单项：新建子图层

```python
            new_sublayer_action = menu.addAction("  新建子图层")
```
# 添加"新建子图层"

```python
            new_sublayer_action.triggered.connect(self._on_add_sublayer)
```
# 触发时调用添加子图层方法

```python

```
# 空行

```python
            menu.addSeparator()
```
# 添加分隔线

```python

```
# 空行

```python
            if layer is not None:
```
# 如果有当前图层

```python
                # 复制图层（第六章）
```
# 菜单项：复制图层

```python
                dup_action = menu.addAction(f"  复制 \"{layer.name}\"")
```
# 添加"复制图层名"

```python
                dup_action.triggered.connect(lambda: self.layer_duplicate_requested.emit(idx))
```
# 触发时发射复制信号

```python

```
# 空行

```python
                # 删除图层（第五章方法1）
```
# 菜单项：删除图层

```python
                del_action = menu.addAction(f"  删除 \"{layer.name}\"")
```
# 添加"删除图层名"

```python
                del_action.triggered.connect(lambda: self.layer_remove_requested.emit(idx))
```
# 触发时发射删除信号

```python

```
# 空行

```python
                menu.addSeparator()
```
# 添加分隔线

```python

```
# 空行

```python
                # 当前图层的选项...
```
# 菜单项：图层选项对话框

```python
                options_action = menu.addAction(f"  \"{layer.name}\" 的选项...")
```
# 添加"图层名 的选项..."

```python
                options_action.triggered.connect(lambda: self._show_layer_options_dialog(idx))
```
# 触发时打开图层选项对话框

```python

```
# 空行

```python
                menu.addSeparator()
```
# 添加分隔线

```python

```
# 空行

```python
                # 收集到新图层（第十五章）
```
# 菜单项：收集到新图层

```python
                collect_action = menu.addAction("  收集到新图层")
```
# 添加"收集到新图层"

```python
                collect_action.triggered.connect(self.layer_collect_requested.emit)
```
# 触发时发射收集信号

```python

```
# 空行

```python
                # 释放到图层（第十六章）
```
# 菜单项：释放到图层（带子菜单）

```python
                release_menu = menu.addMenu("  释放到图层")
```
# 创建子菜单"释放到图层"

```python
                seq_action = release_menu.addAction("顺序 (Sequence)")
```
# 子菜单项"顺序"

```python
                seq_action.triggered.connect(self.layer_release_sequence_requested.emit)
```
# 触发时发射顺序释放信号

```python
                build_action = release_menu.addAction("构建 (Build)")
```
# 子菜单项"构建"

```python
                build_action.triggered.connect(self.layer_release_build_requested.emit)
```
# 触发时发射构建释放信号

```python

```
# 空行

```python
                menu.addSeparator()
```
# 添加分隔线

```python

```
# 空行

```python
                # 合并图层（第十七章）
```
# 菜单项：合并图层

```python
                merge_action = menu.addAction("  合并选定图层")
```
# 添加"合并选定图层"

```python
                merge_action.triggered.connect(lambda: self.layer_merge_requested.emit([idx]))
```
# 触发时发射合并信号（传递索引列表）

```python

```
# 空行

```python
                # 拼合图稿（第十八章）
```
# 菜单项：拼合图稿

```python
                flatten_action = menu.addAction("  拼合图稿")
```
# 添加"拼合图稿"

```python
                flatten_action.triggered.connect(self.layer_flatten_requested.emit)
```
# 触发时发射拼合信号

```python

```
# 空行

```python
                menu.addSeparator()
```
# 添加分隔线

```python

```
# 空行

```python
                # 隐藏/显示其他图层
```
# 菜单项：隐藏其他图层

```python
                if layer.visible:
```
# 如果当前图层可见

```python
                    hide_others = menu.addAction("  隐藏其他图层")
```
# 添加"隐藏其他图层"

```python
                    hide_others.triggered.connect(lambda: self._hide_other_layers(idx))
```
# 触发时隐藏除当前图层外的所有图层

```python

```
# 空行

```python
                # 锁定其他图层
```
# 菜单项：锁定其他图层

```python
                if not layer.locked:
```
# 如果当前图层未锁定

```python
                    lock_others = menu.addAction("  锁定其他图层")
```
# 添加"锁定其他图层"

```python
                    lock_others.triggered.connect(lambda: self._lock_other_layers(idx))
```
# 触发时锁定除当前图层外的所有图层

```python

```
# 空行

```python
                # 显示所有图层
```
# 菜单项：显示所有图层

```python
                show_all = menu.addAction("  显示所有图层")
```
# 添加"显示所有图层"

```python
                show_all.triggered.connect(self._show_all_layers)
```
# 触发时显示所有图层

```python

```
# 空行

```python
                # 解锁所有图层
```
# 菜单项：解锁所有图层

```python
                unlock_all = menu.addAction("  解锁所有图层")
```
# 添加"解锁所有图层"

```python
                unlock_all.triggered.connect(self._unlock_all_layers)
```
# 触发时解锁所有图层

```python

```
# 空行

```python
        else:
```
# 右键点击空白区域 → 基础菜单

```python
            # 空白区域右键 → 基础菜单
```
# 空白区域右键菜单

```python
            new_layer_action = menu.addAction("  新建图层")
```
# 添加"新建图层"

```python
            new_layer_action.triggered.connect(self.layer_add_requested.emit)
```
# 触发时发射新建信号
            
```python
            show_all = menu.addAction("  显示所有图层")
```
# 添加"显示所有图层"

```python
            show_all.triggered.connect(self._show_all_layers)
```
# 触发时显示所有
            
```python
            unlock_all = menu.addAction("  解锁所有图层")
```
# 添加"解锁所有图层"

```python
            unlock_all.triggered.connect(self._unlock_all_layers)
```
# 触发时解锁所有

```python

```
# 空行

```python
        menu.addSeparator()
```
# 添加最终分隔线

```python

```
# 空行

```python
        # 面板选项
```
# 菜单项：面板选项

```python
        panel_opts = menu.addAction("  面板选项...")
```
# 添加"面板选项..."

```python
        panel_opts.triggered.connect(self._show_panel_options)
```
# 触发时打开面板选项对话框

```python

```
# 空行

```python
        menu.exec_(self._tree.mapToGlobal(pos))
```
# 将局部坐标转为全局坐标并在该位置显示菜单

```python

```
# 空行

```python
    def _on_item_bring_to_front(self, obj, layer_index: int):
```
# 私有方法：将对象置顶

```python
        """对象置顶"""
```
# 方法文档字符串

```python
        if 0 <= layer_index < len(self._layers_data):
```
# 图层索引有效

```python
            self._layers_data[layer_index].bring_to_front(obj)
```
# 调用图层的 bring_to_front 方法将对象移到最前面

```python
            self._refresh_display()
```
# 刷新显示

```python

```
# 空行

```python
    def _on_item_send_to_back(self, obj, layer_index: int):
```
# 私有方法：将对象置底

```python
        """对象置底"""
```
# 方法文档字符串

```python
        if 0 <= layer_index < len(self._layers_data):
```
# 图层索引有效

```python
            self._layers_data[layer_index].send_to_back(obj)
```
# 调用图层的 send_to_back 方法将对象移到最后面

```python
            self._refresh_display()
```
# 刷新显示

```python

```
# 空行

```python
    def _hide_other_layers(self, except_idx: int):
```
# 私有方法：隐藏除指定图层外的所有图层

```python
        """隐藏除指定图层外的所有图层"""
```
# 方法文档字符串

```python
        for i, layer in enumerate(self._layers_data):
```
# 遍历所有图层

```python
            if i != except_idx:
```
# 排除指定图层

```python
                layer.visible = False
```
# 设为不可见

```python
                self.layer_visibility_changed.emit(i, False)
```
# 发射可见性变更信号

```python

```
# 空行

```python
    def _lock_other_layers(self, except_idx: int):
```
# 私有方法：锁定除指定图层外的所有图层

```python
        """锁定除指定图层外的所有图层"""
```
# 方法文档字符串

```python
        for i, layer in enumerate(self._layers_data):
```
# 遍历所有图层

```python
            if i != except_idx:
```
# 排除指定图层

```python
                layer.locked = True
```
# 设为锁定

```python
                self.layer_locked_changed.emit(i, True)
```
# 发射锁定变更信号

```python

```
# 空行

```python
    def _show_all_layers(self):
```
# 私有方法：显示所有图层

```python
        """显示所有图层"""
```
# 方法文档字符串

```python
        for i, layer in enumerate(self._layers_data):
```
# 遍历所有图层

```python
            if not layer.visible:
```
# 如果图层当前不可见

```python
                layer.visible = True
```
# 设为可见

```python
                self.layer_visibility_changed.emit(i, True)
```
# 发射可见性变更信号

```python

```
# 空行

```python
    def _unlock_all_layers(self):
```
# 私有方法：解锁所有图层

```python
        """解锁所有图层"""
```
# 方法文档字符串

```python
        for i, layer in enumerate(self._layers_data):
```
# 遍历所有图层

```python
            if layer.locked:
```
# 如果图层当前已锁定

```python
                layer.locked = False
```
# 设为解锁

```python
                self.layer_locked_changed.emit(i, False)
```
# 发射锁定变更信号

```python

```
# 空行

```python
    def _show_layer_options_dialog(self, index: int):
```
# 私有方法：显示图层选项对话框

```python
        """图层选项对话框
```
# 方法文档字符串

```python
        
```
# 空行

```python
        对照 Ai 图层选项对话框（第三章 + 第十九-二十二章）：
```
# 对照 Ai 的图层选项对话框功能

```python
        - 名称 (Name) — 第四章
```
# 名称编辑

```python
        - 颜色 (Color) — 第二十章
```
# 颜色选择

```python
        - 模板 (Template) — 第十九章
```
# 模板模式

```python
        - 打印 (Print) — 第二十一章
```
# 打印控制

```python
        - 预览 (Preview) — 第二十二章
```
# 预览模式

```python
        - 锁定 (Lock) — 第八章
```
# 锁定状态

```python
        - 显示 (Show) — 第七章
```
# 可见性

```python
        - 变暗图像至 (Dim Images) — 第十九章扩展
```
# 变暗图像（扩展功能）

```python
        """
```
# 文档字符串结束

```python
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
```
# 延迟导入对话框相关控件
        
```python
        if not (0 <= index < len(self._layers_data)):
```
# 索引有效性检查

```python
            return
```
# 无效则返回

```python
        layer = self._layers_data[index]
```
# 获取图层对象
        
```python
        dlg = QDialog(self)
```
# 创建对话框

```python
        dlg.setWindowTitle("图层选项")
```
# 设置标题"图层选项"

```python
        dlg.setMinimumWidth(320)
```
# 最小宽度 320px

```python
        dlg.setStyleSheet("""
```
# 设置对话框 QSS 样式

```python
            QDialog { background-color: #3c3c3c; color: #ddd; }
```
# 对话框背景和文字颜色

```python
            QLabel { color: #bbb; }
```
# 标签颜色

```python
            QLineEdit { background-color: #2d2d2d; color: #ddd; border: 1px solid #555; padding: 4px; }
```
# 输入框样式

```python
            QComboBox { background-color: #2d2d2d; color: #ddd; border: 1px solid #555; padding: 4px; }
```
# 下拉框样式

```python
            QCheckBox { color: #bbb; }
```
# 复选框样式

```python
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; padding: 6px 16px; border-radius: 3px; }
```
# 按钮样式

```python
            QPushButton:hover { background-color: #5a5a5a; }
```
# 按钮悬停

```python
        """)
```
# 样式表结束
        
```python
        layout = QFormLayout(dlg)
```
# 创建表单布局
        
```python
        # 名称
```
# 名称控件

```python
        name_edit = QLineEdit(layer.name)
```
# 创建名称输入框，初始值为当前图层名

```python
        name_edit.selectAll()
```
# 全选文本

```python
        layout.addRow("名称(&N):", name_edit)
```
# 添加到表单布局（&N 表示快捷键 Alt+N）
        
```python
        # 颜色（第二十章）
```
# 颜色控件

```python
        color_combo = QComboBox()
```
# 创建颜色下拉框

```python
        color_combo.addItem("无", None)
```
# 添加"无"选项，数据为 None

```python
        for ci, c in enumerate(self.LAYER_COLORS):
```
# 遍历预设颜色列表

```python
            color_combo.addItem(f"颜色 {ci + 1}", c)
```
# 添加颜色选项（数据为 QColor 对象）

```python
            color_combo.setItemData(ci + 1, c, Qt.BackgroundRole)
```
# 设置选项的背景色数据（用于显示颜色预览）
        
```python
        # 选择当前颜色
```
# 选择当前图层颜色

```python
        if layer.color:
```
# 如果图层有颜色

```python
            for ci, c in enumerate(self.LAYER_COLORS):
```
# 遍历预设颜色

```python
                if layer.color.name() == c.name():
```
# 如果匹配当前颜色

```python
                    color_combo.setCurrentIndex(ci + 1)
```
# 设为当前选中项

```python
                    break
```
# 找到后退出循环

```python
        layout.addRow("颜色(&C):", color_combo)
```
# 添加颜色控件到表单（&C 快捷键 Alt+C）
        
```python
        # 模板（第十九章）
```
# 模板复选框

```python
        template_check = QCheckBox("模板(&T)")
```
# 创建模板复选框（&T 快捷键 Alt+T）

```python
        template_check.setChecked(layer.is_template)
```
# 设为当前模板状态

```python
        layout.addRow("", template_check)
```
# 添加到表单
        
```python
        # 打印（第二十一章）
```
# 打印复选框

```python
        print_check = QCheckBox("打印(&P)")
```
# 创建打印复选框（&P 快捷键 Alt+P）

```python
        print_check.setChecked(layer.printable)
```
# 设为当前打印状态

```python
        layout.addRow("", print_check)
```
# 添加到表单
        
```python
        # 预览（第二十二章）
```
# 预览复选框

```python
        preview_check = QCheckBox("预览(&V)")
```
# 创建预览复选框（&V 快捷键 Alt+V）

```python
        preview_check.setChecked(layer.preview_mode == "preview")
```
# 根据当前模式设置选中状态

```python
        layout.addRow("", preview_check)
```
# 添加到表单
        
```python
        # 锁定（第八章）
```
# 锁定复选框

```python
        lock_check = QCheckBox("锁定(&L)")
```
# 创建锁定复选框（&L 快捷键 Alt+L）

```python
        lock_check.setChecked(layer.locked)
```
# 设为当前锁定状态

```python
        layout.addRow("", lock_check)
```
# 添加到表单
        
```python
        # 显示（第七章）
```
# 显示复选框

```python
        show_check = QCheckBox("显示(&S)")
```
# 创建显示复选框（&S 快捷键 Alt+S）

```python
        show_check.setChecked(layer.visible)
```
# 设为当前可见性

```python
        layout.addRow("", show_check)
```
# 添加到表单
        
```python
        # 按钮
```
# 对话框按钮

```python
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
```
# 创建确定/取消按钮框

```python
        buttons.accepted.connect(dlg.accept)
```
# 确定按钮连接到对话框接受

```python
        buttons.rejected.connect(dlg.reject)
```
# 取消按钮连接到对话框拒绝

```python
        layout.addRow(buttons)
```
# 添加到表单
        
```python
        if dlg.exec_() == QDialog.Accepted:
```
# 如果用户点击确定

```python
            new_name = name_edit.text().strip()
```
# 获取新名称

```python
            if new_name and new_name != layer.name:
```
# 名称有变化

```python
                layer.name = new_name
```
# 更新图层名称

```python
                self.layer_rename_requested.emit(index, new_name)
```
# 发射重命名信号
            
```python
            # 颜色
```
# 处理颜色变更

```python
            new_color = color_combo.currentData()
```
# 获取新颜色

```python
            if new_color != layer.color:
```
# 颜色有变化

```python
                layer.color = new_color
```
# 更新图层颜色

```python
                self.layer_color_changed.emit(index, new_color)
```
# 发射颜色变更信号
            
```python
            # 模板
```
# 处理模板变更

```python
            if template_check.isChecked() != layer.is_template:
```
# 模板状态有变化

```python
                layer.is_template = template_check.isChecked()
```
# 更新模板状态

```python
                self.layer_template_changed.emit(index, layer.is_template)
```
# 发射模板变更信号
            
```python
            # 打印
```
# 处理打印变更

```python
            if print_check.isChecked() != layer.printable:
```
# 打印状态有变化

```python
                layer.printable = print_check.isChecked()
```
# 更新打印状态

```python
                self.layer_printable_changed.emit(index, layer.printable)
```
# 发射打印变更信号
            
```python
            # 预览
```
# 处理预览变更

```python
            new_mode = "preview" if preview_check.isChecked() else "outline"
```
# 根据复选框确定新模式

```python
            if new_mode != layer.preview_mode:
```
# 预览模式有变化

```python
                layer.preview_mode = new_mode
```
# 更新预览模式

```python
                self.layer_preview_mode_changed.emit(index, new_mode)
```
# 发射预览模式变更信号
            
```python
            # 锁定
```
# 处理锁定变更

```python
            if lock_check.isChecked() != layer.locked:
```
# 锁定状态有变化

```python
                layer.locked = lock_check.isChecked()
```
# 更新锁定状态

```python
                self.layer_locked_changed.emit(index, layer.locked)
```
# 发射锁定变更信号
            
```python
            # 显示
```
# 处理可见性变更

```python
            if show_check.isChecked() != layer.visible:
```
# 可见性有变化

```python
                layer.visible = show_check.isChecked()
```
# 更新可见性

```python
                self.layer_visibility_changed.emit(index, layer.visible)
```
# 发射可见性变更信号

```python

```
# 空行

```python
    def _show_panel_options(self):
```
# 私有方法：显示面板选项对话框

```python
        """面板选项对话框"""
```
# 方法文档字符串

```python
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
```
# 延迟导入对话框控件
        
```python
        dlg = QDialog(self)
```
# 创建对话框

```python
        dlg.setWindowTitle("图层面板选项")
```
# 设置标题

```python
        dlg.setMinimumWidth(280)
```
# 最小宽度 280px

```python
        dlg.setStyleSheet("""
```
# 设置样式

```python
            QDialog { background-color: #3c3c3c; color: #ddd; }
```
# 对话框背景和文字

```python
            QCheckBox { color: #bbb; }
```
# 复选框颜色

```python
            QPushButton { background-color: #4a4a4a; color: #ddd; border: 1px solid #555; padding: 6px 16px; border-radius: 3px; }
```
# 按钮样式

```python
        """)
```
# 样式表结束
        
```python
        layout = QFormLayout(dlg)
```
# 创建表单布局
        
```python
        thumb_check = QCheckBox("仅显示图层")
```
# "仅显示图层"复选框

```python
        thumb_check.setChecked(False)
```
# 默认不选中

```python
        layout.addRow("", thumb_check)
```
# 添加到表单
        
```python
        small_check = QCheckBox("小行高")
```
# "小行高"复选框

```python
        layout.addRow("", small_check)
```
# 添加到表单
        
```python
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
```
# 确定/取消按钮

```python
        buttons.accepted.connect(dlg.accept)
```
# 确定连接到接受

```python
        buttons.rejected.connect(dlg.reject)
```
# 取消连接到拒绝

```python
        layout.addRow(buttons)
```
# 添加到表单
        
```python
        dlg.exec_()
```
# 执行对话框（模态显示）

```python

```
# 空行

```python
    def _on_add_sublayer(self):
```
# 私有方法：添加子图层

```python
        """添加子图层"""
```
# 方法文档字符串

```python
        idx = self._current_index
```
# 当前图层索引

```python
        if 0 <= idx < len(self._layers_data):
```
# 索引有效

```python
            layer = self._layers_data[idx]
```
# 获取图层对象

```python
            layer.add_sublayer()
```
# 调用图层方法添加子图层

```python
            self.update_layers(self._layers_data, idx)
```
# 刷新图层面板

```python

```
# 空行

```python
    def _set_layer_color(self, index: int, color: QColor):
```
# 私有方法：设置图层颜色

```python
        if 0 <= index < len(self._layers_data):
```
# 索引有效

```python
            self._layers_data[index].color = color
```
# 更新图层颜色

```python

```
# 空行

```python
    def _toggle_template(self, index: int):
```
# 私有方法：切换模板模式

```python
        if 0 <= index < len(self._layers_data):
```
# 索引有效

```python
            layer = self._layers_data[index]
```
# 获取图层

```python
            layer.is_template = not layer.is_template
```
# 取反模板状态

```python

```
# 空行

```python
    def _toggle_printable(self, index: int):
```
# 私有方法：切换打印状态

```python
        if 0 <= index < len(self._layers_data):
```
# 索引有效

```python
            layer = self._layers_data[index]
```
# 获取图层

```python
            layer.printable = not layer.printable
```
# 取反打印状态

```python

```
# 空行

```python
    def _toggle_preview_mode(self, index: int):
```
# 私有方法：切换预览模式

```python
        if 0 <= index < len(self._layers_data):
```
# 索引有效

```python
            layer = self._layers_data[index]
```
# 获取图层

```python
            layer.preview_mode = "outline" if layer.preview_mode == "preview" else "preview"
```
# 在 preview 和 outline 之间切换

```python

```
# 空行

```python
    def _show_layer_menu(self):
```
# 私有方法：点击☰按钮显示图层菜单

```python
        """点击☰按钮显示图层菜单（PDF 二十五）"""
```
# 方法文档字符串，引用第二十五章

```python
        self._on_context_menu(
```
# 复用右键菜单方法

```python
            self._tree.visualItemRect(self._tree.currentItem() or self._tree.topLevelItem(0)).topLeft()
```
# 获取当前选中节点（或第一个节点）的顶部左角位置作为菜单显示位置

```python
            if self._tree.topLevelItemCount() > 0 else self._tree.rect().topLeft()
```
# 如果树为空则使用树控件的左上角位置

```python
        )
```
# 方法调用结束

```python

```
# 空行

```python

```
# 空行

```python
# ── 色板面板 ──────────────────────────────────────────────
```
# 注释分隔线，标识"色板面板"模块的开始

```python

```
# 空行

```python
class SwatchesPanel(QWidget):
```
# 定义 `SwatchesPanel`（色板面板）类，继承 QWidget

```python
    """色板面板
```
# 类文档字符串

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
# 注意：不支持 `__slots__`

```python
    """
```
# 文档字符串结束

```python

```
# 空行

```python
    color_selected = pyqtSignal(QColor)
```
# 信号：选中颜色，携带 QColor

```python

```
# 空行

```python
    def __init__(self, parent=None):
```
# 构造函数

```python
        super().__init__(parent)
```
# 调用父类构造函数

```python
        self._init_ui()
```
# 调用 UI 初始化

```python

```
# 空行

```python
    def _init_ui(self):
```
# 私有方法，构建色板面板界面

```python
        layout = QVBoxLayout(self)
```
# 创建垂直主布局

```python
        layout.setContentsMargins(4, 4, 4, 4)
```
# 四周边距各 4px

```python
        layout.addWidget(QLabel("色板"))
```
# 添加"色板"标题标签

```python

```
# 空行

```python
        self._grid = QGridLayout()
```
# 创建网格布局（用于以网格形式排列色块）

```python
        self._grid.setSpacing(2)
```
# 色块间距 2px

```python
        layout.addLayout(self._grid)
```
# 将网格布局添加到主布局

```python
        layout.addStretch()
```
# 末尾添加弹性空白

```python

```
# 空行

```python
    def update_swatches(self, swatches: list[Swatch]):
```
# 公共方法：更新色板面板显示，参数为 Swatch 列表

```python
        while self._grid.count():
```
# 循环直到网格中没有控件（逐个清除）

```python
            item = self._grid.takeAt(0)
```
# 取出网格中的第一个布局项

```python
            if item.widget():
```
# 如果该项是控件（而非布局/间距）

```python
                item.widget().deleteLater()
```
# 延迟删除该控件（安全释放 Qt 资源）

```python

```
# 空行

```python
        cols = 4
```
# 每行显示 4 个色块

```python
        for i, swatch in enumerate(swatches):
```
# 遍历色板列表

```python
            btn = QPushButton()
```
# 创建色块按钮

```python
            btn.setFixedSize(28, 28)
```
# 固定尺寸 28×28

```python
            btn.setToolTip(swatch.name)
```
# 工具提示显示色板名称

```python
            btn.setStyleSheet(f"""
```
# 设置色块按钮的 QSS 样式

```python
                QPushButton {{
```
# 按钮样式开始（双花括号 `{{` 转义为 f-string 的字面 `{`）

```python
                    background-color: {swatch.color.name()};
```
# 背景色为色板的颜色值

```python
                    border: 1px solid #666;
```
# 1px 灰色边框

```python
                    border-radius: 2px;
```
# 2px 圆角

```python
                }}
```
# 按钮样式结束（`}}` 转义为 `}`）

```python
                QPushButton:hover {{ border: 2px solid #0d6efd; }}
```
# 悬停时蓝色边框加粗（`{{`/`}}` 转义）

```python
            """)
```
# f-string 样式表结束

```python
            btn.clicked.connect(lambda checked, c=swatch.color: self.color_selected.emit(c))
```
# 点击时发射 color_selected 信号，通过默认参数 `c=swatch.color` 捕获当前色板颜色

```python
            self._grid.addWidget(btn, i // cols, i % cols)
```
# 将色块添加到网格：行号 = i 整除 4，列号 = i 取模 4

---

> **以上为 `panels.py` 全部 1427 行源代码的完整逐行中文注释翻译。**
>
> 文件结构总览：
> - **第 1~8 行**：模块文档字符串（架构优化说明）
> - **第 10~33 行**：import 导入语句（PyQt5、core.graphics、core.document、core.tools）
> - **第 36~100 行**：`ToolBar` 类（工具栏 —— 左侧工具面板）
> - **第 102~452 行**：`PropertiesPanel` 类（属性面板 —— 变换/外观/文字/排列/删除）
> - **第 454~1380 行**：`LayersPanel` 类（图层面板 —— 完整对照 Ai 26 章功能）
> - **第 1382~1427 行**：`SwatchesPanel` 类（色板面板 —— 网格色块展示）

