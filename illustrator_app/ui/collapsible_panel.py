"""
可折叠面板组件 (Python 3.10+) —— 手风琴式折叠展开面板

架构优化:
- 使用 __slots__ 减少内存占用
- 使用 X | None 替代 Optional[X]
- 使用 match-case 替代 if-elif
"""

from __future__ import annotations

from PyQt5.QtCore import Qt, pyqtSignal, QPointF
from PyQt5.QtGui import QColor, QFont, QPainter, QPolygonF
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame,
)


class ArrowIcon(QWidget):
    # 定义箭头图标类，用于绘制折叠/展开指示箭头
    """折叠/展开 三角箭头
    注意: PyQt5 QWidget 子类不能使用 __slots__。
    """

    def __init__(self, expanded: bool = True, parent=None):
        # 接收自身引用，展开状态标志，默认为已展开，父部件参数，默认为空
        super().__init__(parent)
        self._expanded = expanded
        self.setFixedSize(12, 12)

    def set_expanded(self, expanded: bool):
        # 定义设置展开状态方法
        self._expanded = expanded
        self.update()

    def paintEvent(self, event):
        # 绘制事件处理方法，用于自定义箭头图标渲染
        painter = QPainter(self)
        # 创建绘图工具实例，以当前部件为绘图设备
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#bbb"))

        points = [(2, 4), (6, 8), (10, 4)] if self._expanded else [(4, 2), (4, 10), (8, 6)]
        painter.drawPolygon(QPolygonF([QPointF(x, y) for x, y in points]))
        # 使用坐标点列表构建浮点多边形，并绘制填充三角形箭头


class CollapsibleSection(QWidget):
    """单个可折叠区域
    注意: PyQt5 QWidget 子类不能使用 __slots__。
    """
    # 定义名为toggled的信号，用于通知折叠状态变化
    toggled = pyqtSignal(bool)

    def __init__(self, title: str, parent=None, expanded: bool = True):
        super().__init__(parent)
        self._title = title
        # 私有属性（展开状态）
        self._expanded = expanded
        # （内容部件）
        self._content_widget: QWidget | None = None
        self._init_ui()
    # 调用内部界面初始化方法
    def _init_ui(self):
        # 创建垂直布局实例
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题栏 - 使用 eventFilter 替代直接赋值 mousePressEvent
        # 
        self._header = QFrame()
        self._header.setFixedHeight(32)
        self._header.setCursor(Qt.PointingHandCursor)
        self._header.installEventFilter(self)
        # 为标题栏安装事件过滤器，由当前可折叠区域实例处理事件

        header_layout = QHBoxLayout(self._header)
        header_layout.setContentsMargins(8, 0, 8, 0)
        header_layout.setSpacing(4)

        self._arrow = ArrowIcon(expanded=self._expanded)
        header_layout.addWidget(self._arrow)

        title_label = QLabel(self._title)
        title_label.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        title_label.setStyleSheet("color: #ccc;")
        header_layout.addWidget(title_label, 1)

        self._header.setStyleSheet("""
            QFrame { background-color: #3a3a3a; border-bottom: 1px solid #4a4a4a; }
            QFrame:hover { background-color: #444; }
        """)
        layout.addWidget(self._header)

        # 内容容器；创建框架容器
        self._content_frame = QFrame()
        self._content_frame.setStyleSheet("background-color: #2d2d2d;")
        self._content_layout = QVBoxLayout(self._content_frame)
        # 创建垂直布局实例
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)

        if not self._expanded:
            self._content_frame.setVisible(False)
            self._content_frame.setMaximumHeight(0)

        layout.addWidget(self._content_frame)

    def set_content(self, widget: QWidget):
        # 定义设置内容方法，用于替换或设置折叠区域中的内容
        if self._content_widget:
            self._content_layout.removeWidget(self._content_widget)
            self._content_widget.deleteLater()
        self._content_widget = widget
        self._content_layout.addWidget(widget)

    def eventFilter(self, obj, event):
        """事件过滤器 —— 处理标题栏点击"""
        # 定义事件过滤方法，处理标题栏点击
        from PyQt5.QtCore import QEvent
        if obj is self._header and event.type() == QEvent.MouseButtonPress:
            self.toggle()
            return True
        return super().eventFilter(obj, event)

    def toggle(self):
        self.set_expanded(not self._expanded)

    def set_expanded(self, expanded: bool):
        if self._expanded == expanded:
            return
        # 更新私有属性，为目标展开状态
        self._expanded = expanded
        # 同步更新箭头图标的展开方向
        self._arrow.set_expanded(expanded)

        if expanded:
            self._content_frame.setVisible(True)
            self._content_frame.setMaximumHeight(16777215)
            if self._content_widget:
                # 如果存在内容部件，显示内容部件
                self._content_widget.setVisible(True)
        else:
            # 将内容框架最大高度设为0（折叠）
            self._content_frame.setMaximumHeight(0)
            # 隐藏内容架构
            self._content_frame.setVisible(False)
            if self._content_widget:
                self._content_widget.setVisible(False)

        self.toggled.emit(expanded)
        # 发射信号，传递当前展开状态布尔值

    @property
    # 属性装饰器，将方法转为只读属性访问
    def expanded(self) -> bool:
        return self._expanded


class PanelContainer(QWidget):
    """右侧折叠面板容器
    注意: PyQt5 QWidget 子类不能使用 __slots__。
    """

    def __init__(self, parent=None):
        # 定义构造方法
        super().__init__(parent)
        self._sections: list[CollapsibleSection] = []
        self._init_ui()

    def _init_ui(self):
        # 创建垂直布局实例，以当前部件为父容器
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        # 启用滚动区域内容自动调整大小
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 设置水平滚动条策略为始终关闭
        self._scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: #2d2d2d; }
            QScrollBar:vertical { background: #2d2d2d; width: 6px; margin: 0; }
            QScrollBar::handle:vertical { background: #555; border-radius: 3px; min-height: 30px; }
            QScrollBar::handle:vertical:hover { background: #777; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        self._sections_container = QWidget()
        self._sections_layout = QVBoxLayout(self._sections_container)
        self._sections_layout.setContentsMargins(0, 0, 0, 0)
        self._sections_layout.setSpacing(0)

        self._scroll.setWidget(self._sections_container)
        # 将区域容器部件设置为滚动区域的可滚动内容部件
        layout.addWidget(self._scroll)
        self.setMinimumWidth(240)

    def add_section(self, title: str, widget: QWidget, expanded: bool = True) -> CollapsibleSection:
        section = CollapsibleSection(title, expanded=expanded)
        # 创建可折叠区域实例，传入标题和展开状态
        section.set_content(widget)
        section.toggled.connect(self._on_section_toggled)
        # 将区域的信号连接到容器的区域切换回调方法
        self._sections.append(section)
        self._sections_layout.addWidget(section)
        # 将新区域添加到区域容器布局中
        return section

    def _on_section_toggled(self, expanded: bool):
        # 定义区域切换回调方法，接收自身引用和展开状态布尔值，当某个区域折叠/展开时触发
        self._sections_layout.update()
        # 更新区域容器布局，重新计算并刷新显示
