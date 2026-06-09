# collapsible_panel.py 中文注解翻译

---

```python
"""
```
# 模块级文档字符串开始

```python
可折叠面板组件 (Python 3.10+) —— 手风琴式折叠展开面板
```
# 可折叠面板组件（要求 Python 3.10 及以上版本）—— 手风琴式折叠展开面板

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
# - 使用 `__slots__` 机制减少内存占用

```python
- 使用 X | None 替代 Optional[X]
```
# - 使用 `X | None` 语法替代 `Optional[X]` 进行类型注解

```python
- 使用 match-case 替代 if-elif
```
# - 使用 `match-case` 语法替代 `if-elif` 条件分支

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
# 从 `__future__` 模块导入 `annotations`，启用延迟注解求值（允许在类型注解中使用尚未定义的类型）

```python

```
# 空行

```python
from PyQt5.QtCore import Qt, pyqtSignal, QPointF
```
# 从 `PyQt5.QtCore` 模块导入：`Qt`（全局枚举常量）、`pyqtSignal`（信号机制）、`QPointF`（二维浮点坐标点）

```python
from PyQt5.QtGui import QColor, QFont, QPainter, QPolygonF
```
# 从 `PyQt5.QtGui` 模块导入：`QColor`（颜色类）、`QFont`（字体类）、`QPainter`（绘图工具类）、`QPolygonF`（浮点多边形类）

```python
from PyQt5.QtWidgets import (
```
# 从 `PyQt5.QtWidgets` 模块导入以下部件类：

```python
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
```
#     `QWidget`（基础部件类）、`QVBoxLayout`（垂直布局）、`QHBoxLayout`（水平布局）、`QPushButton`（按钮）、`QLabel`（文本标签）

```python
    QScrollArea, QFrame,
```
#     `QScrollArea`（滚动区域）、`QFrame`（框架容器）

```python
)
```
# 导入语句结束

```python

```
# 空行

```python

```
# 空行

```python
class ArrowIcon(QWidget):
```
# 定义箭头图标类（继承自Qt基础部件类），用于绘制折叠/展开指示箭头

```python
    """折叠/展开 三角箭头
```
#     文档字符串：折叠/展开三角箭头图标

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
#     注意：PyQt5 的 QWidget 子类不能使用 `__slots__` 优化。

```python
    """
```
#     文档字符串结束

```python

```
#     空行

```python
    def __init__(self, expanded: bool = True, parent=None):
```
#     定义构造方法（接收自身引用、展开状态标志，默认为已展开；父部件参数，默认为空）

```python
        super().__init__(parent)
```
#         调用父类 `QWidget` 的构造方法，传入父部件参数

```python
        self._expanded = expanded
```
#         初始化私有属性 `_expanded`（展开状态），保存传入的展开标志

```python
        self.setFixedSize(12, 12)
```
#         设置固定尺寸为 12×12 像素

```python

```
#     空行

```python
    def set_expanded(self, expanded: bool):
```
#     定义设置展开状态方法（接收自身引用和展开状态布尔值）

```python
        self._expanded = expanded
```
#         更新私有属性 `_expanded`（展开状态）为传入的布尔值

```python
        self.update()
```
#         触发部件重绘，刷新箭头图标显示

```python

```
#     空行

```python
    def paintEvent(self, event):
```
#     定义绘制事件处理方法（接收自身引用和绘制事件对象），用于自定义箭头图标渲染

```python
        painter = QPainter(self)
```
#         创建绘图工具实例，以当前部件为绘图设备

```python
        painter.setRenderHint(QPainter.Antialiasing)
```
#         设置渲染提示为抗锯齿，使箭头边缘更平滑

```python
        painter.setPen(Qt.NoPen)
```
#         设置画笔为无（不绘制轮廓线条）

```python
        painter.setBrush(QColor("#bbb"))
```
#         设置画刷颜色为灰色（十六进制值 #bbb）

```python

```
#         空行

```python
        points = [(2, 4), (6, 8), (10, 4)] if self._expanded else [(4, 2), (4, 10), (8, 6)]
```
#         根据展开状态选择三角形顶点坐标：已展开时为向下箭头，收起时为向右箭头

```python
        painter.drawPolygon(QPolygonF([QPointF(x, y) for x, y in points]))
```
#         使用坐标点列表构建浮点多边形，并绘制填充三角形箭头

```python

```
# 空行

```python

```
# 空行

```python
class CollapsibleSection(QWidget):
```
# 定义可折叠区域类（继承自Qt基础部件类），表示面板中一个可折叠的独立区域

```python
    """单个可折叠区域
```
#     文档字符串：单个可折叠区域组件

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
#     注意：PyQt5 的 QWidget 子类不能使用 `__slots__` 优化。

```python
    """
```
#     文档字符串结束

```python

```
#     空行

```python
    toggled = pyqtSignal(bool)
```
#     定义名为 `toggled` 的信号，信号参数为布尔类型，用于通知外部折叠状态变化

```python

```
#     空行

```python
    def __init__(self, title: str, parent=None, expanded: bool = True):
```
#     定义构造方法（接收自身引用、区域标题字符串、父部件默认为空、展开状态默认为已展开）

```python
        super().__init__(parent)
```
#         调用父类 `QWidget` 的构造方法，传入父部件参数

```python
        self._title = title
```
#         初始化私有属性 `_title`（区域标题），保存传入的标题字符串

```python
        self._expanded = expanded
```
#         初始化私有属性 `_expanded`（展开状态），保存传入的展开标志

```python
        self._content_widget: QWidget | None = None
```
#         初始化私有属性 `_content_widget`（内容部件），类型注解为Qt部件或空，默认为空

```python
        self._init_ui()
```
#         调用内部界面初始化方法

```python

```
#     空行

```python
    def _init_ui(self):
```
#     定义内部界面初始化方法（接收自身引用），负责构建标题栏和内容容器的布局

```python
        layout = QVBoxLayout(self)
```
#         创建垂直布局实例，以当前部件为父容器

```python
        layout.setContentsMargins(0, 0, 0, 0)
```
#         设置布局四边边距（左、上、右、下）均为 0

```python
        layout.setSpacing(0)
```
#         设置子部件之间间距为 0

```python

```
#         空行

```python
        # 标题栏 - 使用 eventFilter 替代直接赋值 mousePressEvent
```
#         注释：标题栏 —— 使用事件过滤器替代直接重写鼠标按下事件

```python
        self._header = QFrame()
```
#         创建框架容器 `_header`（标题栏框架）

```python
        self._header.setFixedHeight(32)
```
#         设置标题栏固定高度为 32 像素

```python
        self._header.setCursor(Qt.PointingHandCursor)
```
#         设置标题栏鼠标光标样式为手指指针（提示可点击）

```python
        self._header.installEventFilter(self)
```
#         为标题栏安装事件过滤器，由当前可折叠区域实例处理事件

```python

```
#         空行

```python
        header_layout = QHBoxLayout(self._header)
```
#         创建水平布局实例，以标题栏框架为父容器

```python
        header_layout.setContentsMargins(8, 0, 8, 0)
```
#         设置标题栏布局四边边距（左 8、上 0、右 8、下 0）

```python
        header_layout.setSpacing(4)
```
#         设置标题栏内子部件间距为 4 像素

```python

```
#         空行

```python
        self._arrow = ArrowIcon(expanded=self._expanded)
```
#         创建箭头图标实例 `_arrow`，传入当前展开状态

```python
        header_layout.addWidget(self._arrow)
```
#         将箭头图标添加到标题栏布局中

```python

```
#         空行

```python
        title_label = QLabel(self._title)
```
#         创建文本标签 `title_label`，显示区域标题

```python
        title_label.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
```
#         设置标签字体为"微软雅黑"，大小 9，加粗

```python
        title_label.setStyleSheet("color: #ccc;")
```
#         设置标签样式表，文字颜色为浅灰色（十六进制值 #ccc）

```python
        header_layout.addWidget(title_label, 1)
```
#         将标题标签添加到标题栏布局中，拉伸因子为 1（占据剩余空间）

```python

```
#         空行

```python
        self._header.setStyleSheet("""
```
#         设置标题栏框架样式表：

```python
            QFrame { background-color: #3a3a3a; border-bottom: 1px solid #4a4a4a; }
```
#             框架背景色为深灰色，底部边框为 1 像素灰色实线

```python
            QFrame:hover { background-color: #444; }
```
#             鼠标悬停时背景色变为稍亮灰色

```python
        """)
```
#         样式表字符串结束

```python
        layout.addWidget(self._header)
```
#         将标题栏框架添加到主垂直布局中

```python

```
#         空行

```python
        # 内容容器
```
#         注释：内容容器区域

```python
        self._content_frame = QFrame()
```
#         创建框架容器 `_content_frame`（内容区域框架）

```python
        self._content_frame.setStyleSheet("background-color: #2d2d2d;")
```
#         设置内容区域背景色为更深的灰色

```python
        self._content_layout = QVBoxLayout(self._content_frame)
```
#         创建垂直布局实例 `_content_layout`，以内容框架为父容器

```python
        self._content_layout.setContentsMargins(0, 0, 0, 0)
```
#         设置内容布局四边边距均为 0

```python
        self._content_layout.setSpacing(0)
```
#         设置内容区域内子部件间距为 0

```python

```
#         空行

```python
        if not self._expanded:
```
#         如果当前为收起状态：

```python
            self._content_frame.setVisible(False)
```
#             隐藏内容框架

```python
            self._content_frame.setMaximumHeight(0)
```
#             设置内容框架最大高度为 0（使其不占用空间）

```python

```
#         空行

```python
        layout.addWidget(self._content_frame)
```
#         将内容框架添加到主垂直布局中

```python

```
#     空行

```python
    def set_content(self, widget: QWidget):
```
#     定义设置内容方法（接收自身引用和要设置的Qt部件），用于替换或设置折叠区域中的内容

```python
        if self._content_widget:
```
#         如果已存在内容部件：

```python
            self._content_layout.removeWidget(self._content_widget)
```
#             从内容布局中移除旧内容部件

```python
            self._content_widget.deleteLater()
```
#             延迟删除旧内容部件（安全释放资源）

```python
        self._content_widget = widget
```
#         保存新的内容部件引用到私有属性 `_content_widget`

```python
        self._content_layout.addWidget(widget)
```
#         将新部件添加到内容布局中

```python

```
#     空行

```python
    def eventFilter(self, obj, event):
```
#     定义事件过滤器方法（接收自身引用、被监视对象和事件对象），用于拦截标题栏点击事件

```python
        """事件过滤器 —— 处理标题栏点击"""
```
#         文档字符串：事件过滤器 —— 处理标题栏点击

```python
        from PyQt5.QtCore import QEvent
```
#         从 `PyQt5.QtCore` 导入 `QEvent` 事件类型枚举（局部导入以避免循环引用）

```python
        if obj is self._header and event.type() == QEvent.MouseButtonPress:
```
#         如果事件来源是标题栏且事件类型为鼠标按下：

```python
            self.toggle()
```
#             调用折叠/展开切换方法

```python
            return True
```
#             返回真，表示事件已处理（阻止进一步传播）

```python
        return super().eventFilter(obj, event)
```
#         否则调用父类的事件过滤器进行默认处理

```python

```
#     空行

```python
    def toggle(self):
```
#     定义切换折叠状态方法（接收自身引用），将当前状态取反

```python
        self.set_expanded(not self._expanded)
```
#         调用设置展开状态方法，传入当前状态的反值

```python

```
#     空行

```python
    def set_expanded(self, expanded: bool):
```
#     定义设置展开状态方法（接收自身引用和展开状态布尔值），更新折叠区域的视觉状态

```python
        if self._expanded == expanded:
```
#         如果当前展开状态与目标状态一致（无需变化）：

```python
            return
```
#             直接返回，不执行任何操作

```python
        self._expanded = expanded
```
#         更新私有属性 `_expanded` 为目标展开状态

```python
        self._arrow.set_expanded(expanded)
```
#         同步更新箭头图标的展开方向

```python

```
#         空行

```python
        if expanded:
```
#         如果目标状态为展开：

```python
            self._content_frame.setVisible(True)
```
#             显示内容框架

```python
            self._content_frame.setMaximumHeight(16777215)
```
#             移除内容框架最大高度限制（设置为 Qt 允许的最大值）

```python
            if self._content_widget:
```
#             如果存在内容部件：

```python
                self._content_widget.setVisible(True)
```
#                 显示内容部件

```python
        else:
```
#         否则（目标状态为收起）：

```python
            self._content_frame.setMaximumHeight(0)
```
#             将内容框架最大高度设为 0（折叠）

```python
            self._content_frame.setVisible(False)
```
#             隐藏内容框架

```python
            if self._content_widget:
```
#             如果存在内容部件：

```python
                self._content_widget.setVisible(False)
```
#                 隐藏内容部件

```python

```
#         空行

```python
        self.toggled.emit(expanded)
```
#         发射 `toggled` 信号，传递当前展开状态布尔值

```python

```
#     空行

```python
    @property
```
#     属性装饰器，将方法转为只读属性访问

```python
    def expanded(self) -> bool:
```
#     定义展开状态只读属性（接收自身引用），返回布尔类型

```python
        return self._expanded
```
#         返回当前展开状态私有属性的值

```python

```
# 空行

```python

```
# 空行

```python
class PanelContainer(QWidget):
```
# 定义面板容器类（继承自Qt基础部件类），用于管理多个可折叠区域的容器

```python
    """右侧折叠面板容器
```
#     文档字符串：右侧折叠面板容器

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
#     注意：PyQt5 的 QWidget 子类不能使用 `__slots__` 优化。

```python
    """
```
#     文档字符串结束

```python

```
#     空行

```python
    def __init__(self, parent=None):
```
#     定义构造方法（接收自身引用和父部件参数，默认为空）

```python
        super().__init__(parent)
```
#         调用父类 `QWidget` 的构造方法，传入父部件参数

```python
        self._sections: list[CollapsibleSection] = []
```
#         初始化私有属性 `_sections`（可折叠区域列表），类型注解为可折叠区域列表，默认为空列表

```python
        self._init_ui()
```
#         调用内部界面初始化方法

```python

```
#     空行

```python
    def _init_ui(self):
```
#     定义内部界面初始化方法（接收自身引用），负责构建带滚动条的面板容器布局

```python
        layout = QVBoxLayout(self)
```
#         创建垂直布局实例，以当前部件为父容器

```python
        layout.setContentsMargins(0, 0, 0, 0)
```
#         设置布局四边边距均为 0

```python
        layout.setSpacing(0)
```
#         设置子部件之间间距为 0

```python

```
#         空行

```python
        self._scroll = QScrollArea()
```
#         创建滚动区域实例 `_scroll`

```python
        self._scroll.setWidgetResizable(True)
```
#         启用滚动区域内容自动调整大小（随容器缩放）

```python
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
```
#         设置水平滚动条策略为始终关闭（禁止水平滚动）

```python
        self._scroll.setStyleSheet("""
```
#         设置滚动区域样式表：

```python
            QScrollArea { border: none; background-color: #2d2d2d; }
```
#             滚动区域无边框，背景色为深灰色

```python
            QScrollBar:vertical { background: #2d2d2d; width: 6px; margin: 0; }
```
#             垂直滚动条背景色为深灰色，宽度 6 像素，外边距为 0

```python
            QScrollBar::handle:vertical { background: #555; border-radius: 3px; min-height: 30px; }
```
#             垂直滚动条滑块背景色为中灰色，圆角 3 像素，最小高度 30 像素

```python
            QScrollBar::handle:vertical:hover { background: #777; }
```
#             垂直滚动条滑块悬停时背景色变亮

```python
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
```
#             隐藏垂直滚动条的上下箭头按钮（高度设为 0）

```python
        """)
```
#         样式表字符串结束

```python

```
#         空行

```python
        self._sections_container = QWidget()
```
#         创建部件实例 `_sections_container`（所有可折叠区域的容器部件）

```python
        self._sections_layout = QVBoxLayout(self._sections_container)
```
#         创建垂直布局实例 `_sections_layout`，以区域容器为父布局

```python
        self._sections_layout.setContentsMargins(0, 0, 0, 0)
```
#         设置区域容器布局四边边距均为 0

```python
        self._sections_layout.setSpacing(0)
```
#         设置区域容器内子部件间距为 0

```python

```
#         空行

```python
        self._scroll.setWidget(self._sections_container)
```
#         将区域容器部件设置为滚动区域的可滚动内容部件

```python
        layout.addWidget(self._scroll)
```
#         将滚动区域添加到主垂直布局中

```python
        self.setMinimumWidth(240)
```
#         设置面板容器的最小宽度为 240 像素

```python

```
#     空行

```python
    def add_section(self, title: str, widget: QWidget, expanded: bool = True) -> CollapsibleSection:
```
#     定义添加区域方法（接收自身引用、区域标题字符串、内容部件、展开状态默认为已展开），返回创建的可折叠区域实例

```python
        section = CollapsibleSection(title, expanded=expanded)
```
#         创建可折叠区域实例 `section`，传入标题和展开状态

```python
        section.set_content(widget)
```
#         调用区域的内容设置方法，将传入的部件放入折叠区域

```python
        section.toggled.connect(self._on_section_toggled)
```
#         将区域的 `toggled` 信号连接到容器的区域切换回调方法

```python
        self._sections.append(section)
```
#         将新创建的区域追加到区域列表中

```python
        self._sections_layout.addWidget(section)
```
#         将新区域添加到区域容器布局中

```python
        return section
```
#         返回新创建的可折叠区域实例

```python

```
#     空行

```python
    def _on_section_toggled(self, expanded: bool):
```
#     定义区域切换回调方法（接收自身引用和展开状态布尔值），当某个区域折叠/展开时触发

```python
        self._sections_layout.update()
```
#         更新区域容器布局，重新计算并刷新显示
