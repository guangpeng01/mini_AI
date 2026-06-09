# canvas.py 逐行中文注解翻译

---

```python
"""
```
# 模块文档字符串开始

```python
画布组件 (Python 3.10+) —— 主绘图区域
```
# 画布组件（要求 Python 3.10 及以上版本）—— 主要绘图区域

```python

```
# 空行

```python
负责渲染所有图形项和处理鼠标/键盘交互
```
# 负责渲染所有图形元素并处理鼠标与键盘交互

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
# - 使用 `__slots__` 来减少内存占用

```python
- 使用 X | None 替代 Optional[X]
```
# - 使用 `X | None` 语法替代 `Optional[X]` 类型注解

```python
- 使用 match-case 进行类型分发
```
# - 使用 `match-case` 语句进行类型分发

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
# 从 `__future__` 模块导入注解特性（允许使用前向引用的类型注解）

```python

```
# 空行

```python
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal
```
# 从 PyQt5 核心模块导入 Qt 命名空间、二维浮点坐标类、矩形浮点类和 PyQt 信号类

```python
from PyQt5.QtGui import (
```
# 从 PyQt5 图形界面模块导入以下类：

```python
    QPainter, QPen, QBrush, QColor, QFont, QPainterPath,
```
#     绘制器类、画笔类、画刷类、颜色类、字体类、绘制路径类、

```python
    QCursor, QPixmap, QWheelEvent, QMouseEvent,
```
#     光标类、像素图类、滚轮事件类、鼠标事件类、

```python
    QKeyEvent, QPaintEvent,
```
#     键盘事件类、绘制事件类

```python
)
```
# 结束从 PyQt5 图形界面模块的导入

```python
from PyQt5.QtWidgets import QWidget
```
# 从 PyQt5 控件模块导入部件基类

```python

```
# 空行

```python
from ..core.graphics import (
```
# 从上级目录核心模块的图形子模块导入以下类：

```python
    GraphicItem, PathItem, RectangleItem, EllipseItem,
```
#     图形项基类、路径项类、矩形项类、椭圆项类、

```python
    TextFrame, GroupItem, GraphicStyle, TextType,
```
#     文本框类、编组项类、图形样式类、文本类型枚举、

```python
    StrokeCap, StrokeJoin, Gradient, GradientType, AnchorPoint,
```
#     笔触端点枚举、笔触连接枚举、渐变类、渐变类型枚举、锚点类、

```python
    Justification, MoveItemsCommand,
```
#     对齐方式枚举、移动图形项命令类

```python
)
```
# 结束从核心图形模块的导入

```python
from ..core.document import Document, Layer
```
# 从上级目录核心模块的文档子模块导入文档类和图层类

```python
from ..core.tools import (
```
# 从上级目录核心模块的工具子模块导入以下类：

```python
    BaseTool, ToolType, SelectionTool, DirectSelectTool,
```
#     工具基类、工具类型枚举、选择工具类、直接选择工具类、

```python
    RectangleTool, EllipseTool, PenTool, TextTool, HandTool,
```
#     矩形工具类、椭圆工具类、钢笔工具类、文字工具类、抓手工具类、

```python
    AddAnchorPointTool, DeleteAnchorPointTool, ConvertAnchorPointTool,
```
#     添加锚点工具类、删除锚点工具类、转换锚点工具类

```python
)
```
# 结束从核心工具模块的导入

```python

```
# 空行

```python

```
# 空行

```python
class CanvasWidget(QWidget):
```
# 定义画布部件类（继承自 Qt 部件基类）

```python
    """画布控件
```
#     """画布控件

```python
    注意: PyQt5 QWidget 子类不能使用 __slots__。
```
#     注意：PyQt5 的 QWidget 子类不能使用 `__slots__`。

```python
    """
```
#     """

```python

```
# 空行

```python
    # 信号
```
#     # 信号定义区域

```python
    item_selected = pyqtSignal(list)
```
#     定义"图形项被选中"信号，参数为列表类型

```python
    item_modified = pyqtSignal()
```
#     定义"图形项被修改"信号，无参数

```python
    tool_changed = pyqtSignal(ToolType)
```
#     定义"工具被切换"信号，参数为工具类型

```python
    mouse_position_changed = pyqtSignal(float, float)
```
#     定义"鼠标位置变化"信号，参数为两个浮点数（x 和 y 坐标）

```python

```
# 空行

```python
    def __init__(self, parent=None):
```
#     定义构造方法（接收自身引用、父部件参数，默认为无）

```python
        super().__init__(parent)
```
#         调用父类 QWidget 的构造方法，传入父部件

```python
        self._document: Document | None = None
```
#         初始化私有属性"文档"为空（类型为文档类或空）

```python
        self._current_tool: BaseTool = SelectionTool()
```
#         初始化私有属性"当前工具"为选择工具的实例

```python
        self._tools: dict[ToolType, BaseTool] = {}
```
#         初始化私有属性"工具字典"为空字典（键为工具类型，值为工具基类实例）

```python
        self._init_tools()
```
#         调用私有方法"初始化工具"

```python

```
#         空行

```python
        # 视图变换
```
#         # 视图变换相关属性

```python
        self._zoom: float = 1.0
```
#         初始化私有属性"缩放比例"为 1.0（即 100%）

```python
        self._pan_offset = QPointF(0, 0)
```
#         初始化私有属性"平移偏移量"为原点坐标

```python
        self._is_panning: bool = False
```
#         初始化私有属性"是否正在平移"为假

```python
        self._pan_start = QPointF(0, 0)
```
#         初始化私有属性"平移起始点"为原点坐标

```python

```
#         空行

```python
        # 交互设置
```
#         # 交互设置区域

```python
        self.setMouseTracking(True)
```
#         启用鼠标追踪（即使未按下鼠标按键也能接收鼠标移动事件）

```python
        self.setFocusPolicy(Qt.StrongFocus)
```
#         设置焦点策略为强焦点（可通过点击和 Tab 键获取焦点）

```python
        self.setMinimumSize(400, 300)
```
#         设置部件最小尺寸为 400 像素宽、300 像素高

```python
        self._update_cursor()  # 初始光标根据默认工具（选择工具=箭头）设置
```
#         调用私有方法"更新光标"（初始光标根据默认工具——选择工具对应的箭头光标来设置）

```python

```
#         空行

```python
        # 背景
```
#         # 背景设置区域

```python
        self.setAutoFillBackground(True)
```
#         启用自动填充背景

```python
        pal = self.palette()
```
#         获取当前调色板对象

```python
        pal.setColor(self.backgroundRole(), QColor(55, 55, 55))
```
#         将调色板的背景角色颜色设置为深灰色（RGB 值为 55, 55, 55）

```python
        self.setPalette(pal)
```
#         将修改后的调色板应用到当前部件

```python

```
#         空行

```python
        # 编辑状态
```
#         # 编辑状态区域

```python
        self._editing_text: TextFrame | None = None
```
#         初始化私有属性"正在编辑的文本"为空（类型为文本框类或空）

```python

```
# 空行

```python
    def _init_tools(self):
```
#     定义私有方法"初始化工具"

```python
        """初始化所有工具"""
```
#         """初始化所有工具"""

```python
        self._tools = {
```
#         初始化工具字典，映射各工具类型到对应的工具实例：

```python
            ToolType.SELECTION: SelectionTool(),
```
#             选择工具类型 → 选择工具实例

```python
            ToolType.DIRECT_SELECT: DirectSelectTool(),
```
#             直接选择工具类型 → 直接选择工具实例

```python
            ToolType.RECTANGLE: RectangleTool(),
```
#             矩形工具类型 → 矩形工具实例

```python
            ToolType.ELLIPSE: EllipseTool(),
```
#             椭圆工具类型 → 椭圆工具实例

```python
            ToolType.PEN: PenTool(),
```
#             钢笔工具类型 → 钢笔工具实例

```python
            ToolType.ADD_ANCHOR: AddAnchorPointTool(),
```
#             添加锚点工具类型 → 添加锚点工具实例

```python
            ToolType.DELETE_ANCHOR: DeleteAnchorPointTool(),
```
#             删除锚点工具类型 → 删除锚点工具实例

```python
            ToolType.CONVERT_ANCHOR: ConvertAnchorPointTool(),
```
#             转换锚点工具类型 → 转换锚点工具实例

```python
            ToolType.TEXT: TextTool(),
```
#             文字工具类型 → 文字工具实例

```python
            ToolType.HAND: HandTool(),
```
#             抓手工具类型 → 抓手工具实例

```python
        }
```
#         结束工具字典定义

```python

```
# 空行

```python
    # ── 属性 ──
```
#     # ── 属性访问器 ──

```python

```
# 空行

```python
    @property
```
#     使用属性装饰器定义只读属性

```python
    def document(self) -> Document | None:
```
#     定义"文档"属性的获取方法，返回值为文档类或空

```python
        return self._document
```
#         返回私有属性"文档"

```python

```
# 空行

```python
    @document.setter
```
#     使用属性设置装饰器定义"文档"属性的设置方法

```python
    def document(self, doc: Document):
```
#     定义"文档"属性的设置方法，接收文档类参数

```python
        self._document = doc
```
#         将传入的文档赋值给私有属性"文档"

```python
        for tool in self._tools.values():
```
#         遍历所有工具字典中的工具实例

```python
            tool.set_document(doc)
```
#             为每个工具设置文档引用

```python
        self.update()
```
#         触发部件重绘更新

```python

```
# 空行

```python
    @property
```
#     使用属性装饰器定义只读属性

```python
    def current_tool_type(self) -> ToolType:
```
#     定义"当前工具类型"属性的获取方法，返回工具类型枚举

```python
        return self._current_tool.tool_type
```
#         返回当前工具的工具类型属性

```python

```
# 空行

```python
    @property
```
#     使用属性装饰器定义只读属性

```python
    def zoom(self) -> float:
```
#     定义"缩放比例"属性的获取方法，返回浮点数

```python
        return self._zoom
```
#         返回私有属性"缩放比例"

```python

```
# 空行

```python
    # ── 工具切换 ──
```
#     # ── 工具切换方法 ──

```python

```
# 空行

```python
    def set_tool(self, tool_type: ToolType):
```
#     定义"设置工具"方法（接收工具类型参数）

```python
        """切换工具"""
```
#         """切换工具"""

```python
        if tool_type in self._tools:
```
#         如果请求的工具类型在工具字典中存在

```python
            self._current_tool.cancel()
```
#             取消当前工具的操作

```python
            self._current_tool = self._tools[tool_type]
```
#             将当前工具切换为指定类型的工具实例

```python
            self._current_tool.set_document(self._document)
```
#             为新工具设置文档引用

```python
            self.tool_changed.emit(tool_type)
```
#             发射"工具已切换"信号，携带工具类型参数

```python
            self._update_cursor()
```
#             更新光标样式以匹配新工具

```python
            self.update()
```
#             触发部件重绘更新

```python

```
# 空行

```python
    def _update_cursor(self):
```
#     定义私有方法"更新光标"

```python
        """根据当前工具更新光标"""
```
#         """根据当前工具更新光标样式"""

```python
        # 钢笔工具：根据悬停状态动态切换光标
```
#         # 钢笔工具：根据悬停状态动态切换光标

```python
        if self._current_tool.tool_type == ToolType.PEN:
```
#         如果当前工具是钢笔工具

```python
            hover = getattr(self._current_tool, '_hover_state', 0)
```
#             获取当前工具的悬停状态属性（默认值为 0）

```python
            from ..core.tools import PenTool
```
#             从核心工具模块导入钢笔工具类

```python
            pen_cursors = {
```
#             定义钢笔工具各悬停状态对应的光标映射字典：

```python
                PenTool.PEN_DEFAULT: Qt.CrossCursor,
```
#                 钢笔默认状态 → 十字光标

```python
                PenTool.PEN_PLUS: Qt.CrossCursor,       # Pen+
```
#                 钢笔添加锚点状态 → 十字光标（标注：Pen+）

```python
                PenTool.PEN_MINUS: Qt.CrossCursor,       # Pen-
```
#                 钢笔删除锚点状态 → 十字光标（标注：Pen-）

```python
                PenTool.PEN_CLOSE: Qt.CrossCursor,       # Pen○
```
#                 钢笔闭合路径状态 → 十字光标（标注：Pen○）

```python
                PenTool.PEN_CONTINUE: Qt.CrossCursor,    # Pen/
```
#                 钢笔续画路径状态 → 十字光标（标注：Pen/）

```python
            }
```
#             结束光标映射字典定义

```python
            self.setCursor(QCursor(pen_cursors.get(hover, Qt.CrossCursor)))
```
#             根据悬停状态设置对应光标（找不到则使用默认十字光标）

```python
            return
```
#             提前返回，不执行后续通用光标逻辑

```python

```
# 空行

```python
        cursor = {
```
#         定义通用工具光标映射字典：

```python
            ToolType.SELECTION: Qt.ArrowCursor,
```
#             选择工具 → 箭头光标

```python
            ToolType.DIRECT_SELECT: Qt.ArrowCursor,
```
#             直接选择工具 → 箭头光标

```python
            ToolType.RECTANGLE: Qt.CrossCursor,
```
#             矩形工具 → 十字光标

```python
            ToolType.ELLIPSE: Qt.CrossCursor,
```
#             椭圆工具 → 十字光标

```python
            ToolType.ADD_ANCHOR: Qt.CrossCursor,
```
#             添加锚点工具 → 十字光标

```python
            ToolType.DELETE_ANCHOR: Qt.CrossCursor,
```
#             删除锚点工具 → 十字光标

```python
            ToolType.CONVERT_ANCHOR: Qt.CrossCursor,
```
#             转换锚点工具 → 十字光标

```python
            ToolType.TEXT: Qt.IBeamCursor,
```
#             文字工具 → 工字光标（文本输入光标）

```python
            ToolType.HAND: Qt.OpenHandCursor,
```
#             抓手工具 → 张开手掌光标

```python
            ToolType.ZOOM: Qt.CrossCursor,
```
#             缩放工具 → 十字光标

```python
        }.get(self._current_tool.tool_type, Qt.ArrowCursor)
```
#         根据当前工具类型查找光标（找不到则使用默认箭头光标）

```python
        self.setCursor(QCursor(cursor))
```
#         设置光标样式

```python

```
# 空行

```python
    # ── 坐标转换 ──
```
#     # ── 坐标转换方法 ──

```python

```
# 空行

```python
    def _to_doc_coords(self, pos: QPointF) -> QPointF:
```
#     定义私有方法"转换为文档坐标"（将屏幕坐标转换为文档坐标，接收二维浮点坐标，返回二维浮点坐标）

```python
        center = QPointF(self.width() / 2, self.height() / 2)
```
#         计算部件中心点坐标（宽度的一半、高度的一半）

```python
        return (pos - center - self._pan_offset) / self._zoom
```
#         将屏幕坐标减去中心点和平移偏移量，再除以缩放比例，得到文档坐标

```python

```
# 空行

```python
    def _to_screen_coords(self, pos: QPointF) -> QPointF:
```
#     定义私有方法"转换为屏幕坐标"（将文档坐标转换为屏幕坐标，接收二维浮点坐标，返回二维浮点坐标）

```python
        center = QPointF(self.width() / 2, self.height() / 2)
```
#         计算部件中心点坐标（宽度的一半、高度的一半）

```python
        return pos * self._zoom + center + self._pan_offset
```
#         将文档坐标乘以缩放比例，再加上中心点和平移偏移量，得到屏幕坐标

```python

```
# 空行

```python
    # ── 鼠标事件 ──
```
#     # ── 鼠标事件处理方法 ──

```python

```
# 空行

```python
    def mousePressEvent(self, event: QMouseEvent):
```
#     定义"鼠标按下事件"处理方法（接收鼠标事件参数）

```python
        try:
```
#         开始异常捕获块

```python
            doc_pos = self._to_doc_coords(QPointF(event.pos()))
```
#             将鼠标事件的屏幕坐标转换为文档坐标

```python

```
#             空行

```python
            # 中键平移或抓手工具
```
#             # 中键平移或抓手工具处理

```python
            if event.button() == Qt.MiddleButton or self._current_tool.tool_type == ToolType.HAND:
```
#             如果按下的是鼠标中键，或者当前工具是抓手工具

```python
                self._is_panning = True
```
#                 将"正在平移"标志设为真

```python
                self._pan_start = QPointF(event.pos())
```
#                 记录平移起始位置

```python
                self.setCursor(Qt.ClosedHandCursor)
```
#                 将光标切换为闭合手掌光标（表示正在拖拽）

```python
                return
```
#                 提前返回，不执行后续工具逻辑

```python

```
#             空行

```python
            self._current_tool.mouse_press(doc_pos, event.modifiers())
```
#             将鼠标按下事件和修饰键传递给当前工具处理

```python
            self.update()
```
#             触发部件重绘更新

```python
        except Exception as e:
```
#         捕获异常，赋值给变量 `e`

```python
            import traceback
```
#             导入回溯模块

```python
            traceback.print_exc()
```
#             打印完整的异常堆栈信息

```python
            print(f"[mousePressEvent ERROR] {e}")
```
#             打印鼠标按下事件的错误信息

```python

```
# 空行

```python
    def mouseMoveEvent(self, event: QMouseEvent):
```
#     定义"鼠标移动事件"处理方法（接收鼠标事件参数）

```python
        try:
```
#         开始异常捕获块

```python
            doc_pos = self._to_doc_coords(QPointF(event.pos()))
```
#             将鼠标事件的屏幕坐标转换为文档坐标

```python
            self.mouse_position_changed.emit(doc_pos.x(), doc_pos.y())
```
#             发射"鼠标位置变化"信号，携带文档坐标的 x 和 y 值

```python

```
#             空行

```python
            if self._is_panning:
```
#             如果正在平移画布

```python
                delta = QPointF(event.pos()) - self._pan_start
```
#                 计算鼠标位移量（当前位置减去起始位置）

```python
                self._pan_offset += delta
```
#                 将位移量累加到平移偏移量上

```python
                self._pan_start = QPointF(event.pos())
```
#                 更新平移起始位置为当前鼠标位置

```python
                self.update()
```
#                 触发部件重绘更新

```python
                return
```
#                 提前返回，不执行后续工具逻辑

```python

```
#             空行

```python
            self._current_tool.mouse_move(doc_pos, event.modifiers())
```
#             将鼠标移动事件和修饰键传递给当前工具处理

```python
            
```
#             空行（含缩进空格）

```python
            # 钢笔工具：动态更新光标以反映悬停状态
```
#             # 钢笔工具：动态更新光标以反映悬停状态变化

```python
            if self._current_tool.tool_type == ToolType.PEN:
```
#             如果当前工具是钢笔工具

```python
                self._update_cursor()
```
#                 更新光标样式

```python
            
```
#             空行（含缩进空格）

```python
            self.update()
```
#             触发部件重绘更新

```python
        except Exception as e:
```
#         捕获异常，赋值给变量 `e`

```python
            import traceback
```
#             导入回溯模块

```python
            traceback.print_exc()
```
#             打印完整的异常堆栈信息

```python
            print(f"[mouseMoveEvent ERROR] {e}")
```
#             打印鼠标移动事件的错误信息

```python

```
# 空行

```python
    def mouseReleaseEvent(self, event: QMouseEvent):
```
#     定义"鼠标释放事件"处理方法（接收鼠标事件参数）

```python
        try:
```
#         开始异常捕获块

```python
            if event.button() == Qt.MiddleButton or self._is_panning:
```
#             如果释放的是鼠标中键，或者当前正在平移画布

```python
                self._is_panning = False
```
#                 将"正在平移"标志设为假

```python
                self._update_cursor()
```
#                 恢复光标样式

```python
                return
```
#                 提前返回，不执行后续工具逻辑

```python

```
#             空行

```python
            doc_pos = self._to_doc_coords(QPointF(event.pos()))
```
#             将鼠标事件的屏幕坐标转换为文档坐标

```python
            self._current_tool.mouse_release(doc_pos, event.modifiers())
```
#             将鼠标释放事件和修饰键传递给当前工具处理

```python

```
#             空行

```python
            if self._document:
```
#             如果文档存在

```python
                sel = self._document.get_selection()
```
#                 获取当前选中的图形项列表

```python
                self.item_selected.emit(sel)
```
#                 发射"图形项被选中"信号，携带选中列表

```python

```
#             空行

```python
            self.update()
```
#             触发部件重绘更新

```python
        except Exception as e:
```
#         捕获异常，赋值给变量 `e`

```python
            import traceback
```
#             导入回溯模块

```python
            traceback.print_exc()
```
#             打印完整的异常堆栈信息

```python
            print(f"[mouseReleaseEvent ERROR] {e}")
```
#             打印鼠标释放事件的错误信息

```python

```
# 空行

```python
    def mouseDoubleClickEvent(self, event: QMouseEvent):
```
#     定义"鼠标双击事件"处理方法（接收鼠标事件参数）

```python
        doc_pos = self._to_doc_coords(QPointF(event.pos()))
```
#         将鼠标事件的屏幕坐标转换为文档坐标

```python
        self._current_tool.mouse_double_click(doc_pos, event.modifiers())
```
#         将鼠标双击事件和修饰键传递给当前工具处理

```python

```
#         空行

```python
        # 双击文字进入编辑
```
#         # 双击文字进入编辑模式

```python
        if self._current_tool.tool_type == ToolType.SELECTION and self._document:
```
#         如果当前工具是选择工具且文档存在

```python
            item = self._document.get_item_at(doc_pos.x(), doc_pos.y())
```
#             获取双击位置处的图形项

```python
            if isinstance(item, TextFrame):
```
#             如果该图形项是文本框实例

```python
                self._start_text_edit(item)
```
#                 启动该文本框的文字编辑模式

```python

```
#         空行

```python
        self.update()
```
#         触发部件重绘更新

```python

```
# 空行

```python
    def wheelEvent(self, event: QWheelEvent):
```
#     定义"滚轮事件"处理方法（接收滚轮事件参数）

```python
        """滚轮缩放"""
```
#         """滚轮缩放处理"""

```python
        zoom_factor = 1.1
```
#         定义缩放因子为 1.1（即每次缩放 10%）

```python
        if event.angleDelta().y() > 0:
```
#         如果滚轮向上滚动（y 方向角度增量大于 0）

```python
            self._zoom *= zoom_factor
```
#             将缩放比例乘以缩放因子（放大）

```python
        else:
```
#         否则（滚轮向下滚动）

```python
            self._zoom /= zoom_factor
```
#             将缩放比例除以缩放因子（缩小）

```python
        self._zoom = max(0.05, min(20.0, self._zoom))
```
#         将缩放比例限制在 5% 到 2000% 之间

```python
        self.update()
```
#         触发部件重绘更新

```python

```
# 空行

```python
    # ── 键盘事件 ──
```
#     # ── 键盘事件处理方法 ──

```python

```
# 空行

```python
    def keyPressEvent(self, event: QKeyEvent):
```
#     定义"键盘按下事件"处理方法（接收键盘事件参数）

```python
        try:
```
#         开始异常捕获块

```python
            key = event.key()
```
#             获取按下的键值

```python
            mods = event.modifiers()
```
#             获取当前修饰键状态

```python

```
#             空行

```python
            # 工具快捷键
```
#             # 工具快捷键映射

```python
            shortcuts = {
```
#             定义快捷键与工具类型的映射字典：

```python
                Qt.Key_V: ToolType.SELECTION,
```
#                 V 键 → 选择工具

```python
                Qt.Key_A: ToolType.DIRECT_SELECT,
```
#                 A 键 → 直接选择工具

```python
                Qt.Key_M: ToolType.RECTANGLE,
```
#                 M 键 → 矩形工具

```python
                Qt.Key_L: ToolType.ELLIPSE,
```
#                 L 键 → 椭圆工具

```python
                Qt.Key_P: ToolType.PEN,
```
#                 P 键 → 钢笔工具

```python
                Qt.Key_T: ToolType.TEXT,
```
#                 T 键 → 文字工具

```python
                Qt.Key_H: ToolType.HAND,
```
#                 H 键 → 抓手工具

```python
            }
```
#             结束快捷键映射字典定义

```python

```
#             空行

```python
            # Shift+C → 转换锚点工具
```
#             # Shift+C 组合键 → 转换锚点工具

```python
            if key == Qt.Key_C and (mods & Qt.ShiftModifier):
```
#             如果按下 C 键且同时按住了 Shift 修饰键

```python
                self.set_tool(ToolType.CONVERT_ANCHOR)
```
#                 切换到转换锚点工具

```python
                return
```
#                 提前返回

```python

```
#             空行

```python
            if key in shortcuts:
```
#             如果按下的键在快捷键字典中

```python
                self.set_tool(shortcuts[key])
```
#                 切换到对应的工具

```python
                return
```
#                 提前返回

```python

```
#             空行

```python
            # 方向键微调选中元素（选择工具/直接选择工具模式下）
```
#             # 方向键微调选中元素（仅在选择工具或直接选择工具模式下生效）

```python
            if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
```
#             如果按下的是方向键（左、右、上、下）

```python
                if self._document and self._current_tool.tool_type in (
```
#                 如果文档存在且当前工具是选择工具或直接选择工具

```python
                    ToolType.SELECTION, ToolType.DIRECT_SELECT,
```
#                     （选择工具类型、直接选择工具类型）

```python
                ):
```
#                 结束条件判断

```python
                    sel = self._document.get_selection()
```
#                     获取当前选中的图形项列表

```python
                    if sel:
```
#                     如果有选中的图形项

```python
                        # Shift 加速：每次移动 10px，否则 1px
```
#                         # Shift 加速：每次移动 10 像素，否则移动 1 像素

```python
                        step = 10.0 if (mods & Qt.ShiftModifier) else 1.0
```
#                         根据是否按住 Shift 键确定移动步长

```python
                        dx = dy = 0.0
```
#                         初始化水平方向和垂直方向位移量为 0.0

```python
                        if key == Qt.Key_Left:
```
#                         如果按下左方向键

```python
                            dx = -step
```
#                             水平方向左移一个步长

```python
                        elif key == Qt.Key_Right:
```
#                         否则如果按下右方向键

```python
                            dx = step
```
#                             水平方向右移一个步长

```python
                        elif key == Qt.Key_Up:
```
#                         否则如果按下上方向键

```python
                            dy = -step
```
#                             垂直方向上移一个步长

```python
                        elif key == Qt.Key_Down:
```
#                         否则如果按下下方向键

```python
                            dy = step
```
#                             垂直方向下移一个步长

```python

```
#                         空行

```python
                        for item in sel:
```
#                         遍历所有选中的图形项

```python
                            item.move_by(dx, dy)
```
#                             将每个图形项按计算出的位移量移动

```python

```
#                         空行

```python
                        # 记录移动命令用于撤销（通过 execute_command 统一入口）
```
#                         # 记录移动命令用于撤销（通过 execute_command 统一入口）

```python
                        cmd = MoveItemsCommand(
```
#                         创建移动图形项命令：

```python
                            self._document, list(sel), dx, dy,
```
#                             传入文档对象、选中项列表、水平位移量、垂直位移量

```python
                        )
```
#                         结束命令创建

```python
                        self._document.execute_command(cmd)
```
#                         通过文档的统一命令执行入口执行移动命令（支持撤销）

```python

```
#                         空行

```python
                        self.item_selected.emit(sel)
```
#                         发射"图形项被选中"信号

```python
                        self.item_modified.emit()
```
#                         发射"图形项被修改"信号

```python
                        self.update()
```
#                         触发部件重绘更新

```python
                return
```
#                 提前返回

```python

```
#             空行

```python
            # Delete 删除选中项 或 删除锚点（直接选择工具/钢笔工具）
```
#             # Delete 键：删除选中项，或在直接选择工具/钢笔工具下删除锚点

```python
            if key in (Qt.Key_Delete, Qt.Key_Backspace):
```
#             如果按下的是删除键或退格键

```python
                if self._document:
```
#                 如果文档存在

```python
                    # 直接选择工具/钢笔工具下：删除锚点
```
#                     # 在直接选择工具或钢笔工具下：删除锚点

```python
                    if self._current_tool.tool_type in (ToolType.DIRECT_SELECT, ToolType.PEN):
```
#                     如果当前工具是直接选择工具或钢笔工具

```python
                        self._current_tool.key_press(key, mods)
```
#                         将按键事件传递给当前工具处理（删除锚点）

```python
                        self.item_modified.emit()
```
#                         发射"图形项被修改"信号

```python
                        self.update()
```
#                         触发部件重绘更新

```python
                        return
```
#                         提前返回

```python
                    for item in list(self._document.get_selection()):
```
#                     遍历当前选中的所有图形项（转为列表避免迭代中修改）

```python
                        self._document.remove_item(item)
```
#                         从文档中移除该图形项

```python
                    self.item_selected.emit([])
```
#                     发射"图形项被选中"信号，传入空列表（清空选择）

```python
                    self.update()
```
#                     触发部件重绘更新

```python
                return
```
#                 提前返回

```python

```
#             空行

```python
            # Ctrl+G 编组
```
#             # Ctrl+G 组合键：将选中项编组

```python
            if key == Qt.Key_G and (mods & Qt.ControlModifier):
```
#             如果按下 G 键且同时按住了 Ctrl 修饰键

```python
                if self._document:
```
#                 如果文档存在

```python
                    group = self._document.group_selection()
```
#                     将当前选中项编组，返回编组对象

```python
                    if group:
```
#                     如果编组成功

```python
                        self.item_selected.emit([group])
```
#                         发射"图形项被选中"信号，携带编组对象

```python
                        self.update()
```
#                         触发部件重绘更新

```python
                return
```
#                 提前返回

```python

```
#             空行

```python
            # Ctrl+Shift+G 取消编组
```
#             # Ctrl+Shift+G 组合键：取消编组

```python
            if key == Qt.Key_G and (mods & Qt.ControlModifier) and (mods & Qt.ShiftModifier):
```
#             如果按下 G 键且同时按住了 Ctrl 和 Shift 修饰键

```python
                if self._document:
```
#                 如果文档存在

```python
                    for item in list(self._document.get_selection()):
```
#                     遍历当前选中的所有图形项

```python
                        self._document.ungroup(item)
```
#                         对每个图形项执行取消编组操作

```python
                    self.item_selected.emit([])
```
#                     发射"图形项被选中"信号，传入空列表（清空选择）

```python
                    self.update()
```
#                     触发部件重绘更新

```python
                return
```
#                 提前返回

```python

```
#             空行

```python
            # Ctrl+A 全选
```
#             # Ctrl+A 组合键：全选

```python
            if key == Qt.Key_A and (mods & Qt.ControlModifier):
```
#             如果按下 A 键且同时按住了 Ctrl 修饰键

```python
                if self._document:
```
#                 如果文档存在

```python
                    self._document.select_all()
```
#                     执行全选操作

```python
                    self.item_selected.emit(self._document.get_selection())
```
#                     发射"图形项被选中"信号，携带所有选中项

```python
                    self.update()
```
#                     触发部件重绘更新

```python
                return
```
#                 提前返回

```python

```
#             空行

```python
            # +/- 添加锚点（直接选择工具）
```
#             # +/- 键：添加锚点（在直接选择工具下）

```python
            if key in (Qt.Key_Plus, Qt.Key_Equal, Qt.Key_Minus):
```
#             如果按下的是加号键、等号键或减号键

```python
                if self._current_tool.tool_type == ToolType.DIRECT_SELECT:
```
#                 如果当前工具是直接选择工具

```python
                    self._current_tool.key_press(key, mods)
```
#                     将按键事件传递给当前工具处理（添加/删除锚点）

```python
                    self.item_modified.emit()
```
#                     发射"图形项被修改"信号

```python
                    self.update()
```
#                     触发部件重绘更新

```python
                    return
```
#                     提前返回

```python

```
#             空行

```python
            # 传递给当前工具
```
#             # 将未处理的按键事件传递给当前工具

```python
            self._current_tool.key_press(key, mods)
```
#             将按键事件和修饰键状态传递给当前工具处理

```python
            self.update()
```
#             触发部件重绘更新

```python
        except Exception as e:
```
#         捕获异常，赋值给变量 `e`

```python
            import traceback
```
#             导入回溯模块

```python
            traceback.print_exc()
```
#             打印完整的异常堆栈信息

```python
            print(f"[keyPressEvent ERROR] {e}")
```
#             打印键盘按下事件的错误信息

```python

```
# 空行

```python
    def keyReleaseEvent(self, event: QKeyEvent):
```
#     定义"键盘释放事件"处理方法（接收键盘事件参数）

```python
        """键盘释放事件 —— 处理修饰键释放时的光标更新"""
```
#         """键盘释放事件 —— 处理修饰键释放时的光标更新"""

```python
        try:
```
#         开始异常捕获块

```python
            key = event.key()
```
#             获取释放的键值

```python
            # Alt/Ctrl/Shift 释放时更新光标（钢笔工具悬停状态可能改变）
```
#             # Alt/Ctrl/Shift 释放时更新光标（钢笔工具的悬停状态可能改变）

```python
            if key in (Qt.Key_Alt, Qt.Key_Control, Qt.Key_Shift, Qt.Key_Space):
```
#             如果释放的是 Alt、Ctrl、Shift 或空格键

```python
                if self._current_tool.tool_type == ToolType.PEN:
```
#                 如果当前工具是钢笔工具

```python
                    self._update_cursor()
```
#                     更新光标样式

```python
        except Exception as e:
```
#         捕获异常，赋值给变量 `e`

```python
            import traceback
```
#             导入回溯模块

```python
            traceback.print_exc()
```
#             打印完整的异常堆栈信息

```python
            print(f"[keyReleaseEvent ERROR] {e}")
```
#             打印键盘释放事件的错误信息

```python

```
# 空行

```python
    # ── 文字编辑 ──
```
#     # ── 文字编辑相关方法 ──

```python

```
# 空行

```python
    def _start_text_edit(self, text_frame: TextFrame):
```
#     定义私有方法"开始文字编辑"（接收文本框参数）

```python
        self._editing_text = text_frame
```
#         将正在编辑的文本框设置为传入的文本框

```python
        self.item_modified.emit()
```
#         发射"图形项被修改"信号

```python

```
# 空行

```python
    def edit_selected_text(self, new_text: str):
```
#     定义"编辑选中文本"方法（接收新文本字符串参数）

```python
        if self._editing_text:
```
#         如果当前有正在编辑的文本框

```python
            self._editing_text.contents = new_text
```
#             将文本框的内容更新为新文本

```python
            if self._document:
```
#             如果文档存在

```python
                self._document.modified = True
```
#                 将文档的修改标记设为真

```python
            self.item_modified.emit()
```
#             发射"图形项被修改"信号

```python
            self.update()
```
#             触发部件重绘更新

```python

```
# 空行

```python
    def finish_text_edit(self):
```
#     定义"完成文字编辑"方法

```python
        self._editing_text = None
```
#         将正在编辑的文本框设为空（结束编辑状态）

```python

```
# 空行

```python
    # ── 视图操作 ──
```
#     # ── 视图操作方法 ──

```python

```
# 空行

```python
    def zoom_in(self):
```
#     定义"放大"方法

```python
        self._zoom = min(20.0, self._zoom * 1.25)
```
#         将缩放比例乘以 1.25（放大 25%），最大不超过 20.0（2000%）

```python
        self.update()
```
#         触发部件重绘更新

```python

```
# 空行

```python
    def zoom_out(self):
```
#     定义"缩小"方法

```python
        self._zoom = max(0.05, self._zoom / 1.25)
```
#         将缩放比例除以 1.25（缩小），最小不低于 0.05（5%）

```python
        self.update()
```
#         触发部件重绘更新

```python

```
# 空行

```python
    def zoom_to_fit(self):
```
#     定义"缩放至适合"方法

```python
        if self._document:
```
#         如果文档存在

```python
            self._zoom = min(
```
#             计算适合画布的缩放比例，取宽度和高度中较小的比例

```python
                self.width() / self._document.width,
```
#                 部件宽度除以文档宽度

```python
                self.height() / self._document.height,
```
#                 部件高度除以文档高度

```python
            ) * 0.9
```
#             乘以 0.9（留出 10% 的边距）

```python
            self._pan_offset = QPointF(0, 0)
```
#             将平移偏移量重置为原点

```python
            self.update()
```
#             触发部件重绘更新

```python

```
# 空行

```python
    def zoom_100(self):
```
#     定义"缩放到 100%"方法

```python
        self._zoom = 1.0
```
#         将缩放比例重置为 1.0（即 100%）

```python
        self._pan_offset = QPointF(0, 0)
```
#         将平移偏移量重置为原点

```python
        self.update()
```
#         触发部件重绘更新

```python

```
# 空行

```python
    # ── 绘制 ──
```
#     # ── 绘制相关方法 ──

```python

```
# 空行

```python
    def paintEvent(self, event: QPaintEvent):
```
#     定义"绘制事件"处理方法（接收绘制事件参数）

```python
        try:
```
#         开始异常捕获块

```python
            painter = QPainter(self)
```
#             创建绘制器实例，绑定到当前部件

```python
            painter.setRenderHint(QPainter.Antialiasing)
```
#             启用抗锯齿渲染

```python
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
```
#             启用平滑像素图变换

```python

```
#             空行

```python
            painter.fillRect(self.rect(), QColor(55, 55, 55))
```
#             用深灰色（RGB 55,55,55）填充整个部件矩形区域作为背景

```python

```
#             空行

```python
            if not self._document:
```
#             如果文档不存在

```python
                painter.end()
```
#                 结束绘制

```python
                return
```
#                 提前返回

```python

```
#             空行

```python
            painter.save()
```
#             保存当前绘制器状态

```python
            center = QPointF(self.width() / 2, self.height() / 2)
```
#             计算部件中心点坐标

```python
            painter.translate(center + self._pan_offset)
```
#             将绘制原点平移到中心点加上平移偏移量的位置

```python
            painter.scale(self._zoom, self._zoom)
```
#             按缩放比例对绘制进行缩放

```python

```
#             空行

```python
            # 画板
```
#             # 绘制画板

```python
            self._draw_artboard(painter)
```
#             调用私有方法"绘制画板"

```python

```
#             空行

```python
            # 所有图层
```
#             # 绘制所有图层

```python
            for layer in self._document.layers:
```
#             遍历文档中的所有图层

```python
                if layer.visible:
```
#                 如果该图层可见

```python
                    painter.save()
```
#                     保存当前绘制器状态

```python
                    painter.setOpacity(layer.opacity)
```
#                     设置图层的不透明度

```python
                    
```
#                     空行（含缩进空格）

```python
                    # 第二十二章 - 预览模式：Outline 轮廓模式
```
#                     # 第二十二章 - 预览模式：Outline 轮廓模式

```python
                    if layer.preview_mode == "outline":
```
#                     如果图层的预览模式为"轮廓"

```python
                        painter.setPen(QPen(Qt.gray, 0.5))
```
#                         设置画笔为灰色、宽度 0.5 的轮廓线

```python
                        painter.setBrush(Qt.NoBrush)
```
#                         设置画刷为无填充

```python
                    
```
#                     空行（含缩进空格）

```python
                    # 第二十五章 - 图层级效果（透明度已在上面设置）
```
#                     # 第二十五章 - 图层级效果（透明度已在上方设置）

```python
                    # 第十九章 - 模板图层额外降低透明度
```
#                     # 第十九章 - 模板图层额外降低透明度

```python
                    if layer.is_template:
```
#                     如果该图层是模板图层

```python
                        painter.setOpacity(layer.opacity * 0.5)
```
#                         将不透明度降低为原来的一半

```python
                    
```
#                     空行（含缩进空格）

```python
                    for item in list(layer.items):  # 复制列表避免迭代中修改
```
#                     遍历图层中的所有图形项（复制列表以避免迭代过程中修改集合）

```python
                        if item.visible:
```
#                         如果该图形项可见

```python
                            self._draw_item(painter, item)
```
#                             调用私有方法绘制该图形项

```python
                    
```
#                     空行（含缩进空格）

```python
                    # 也绘制子图层中的对象
```
#                     # 同时绘制子图层中的对象

```python
                    for sub in layer.sublayers:
```
#                     遍历该图层的所有子图层

```python
                        if sub.visible:
```
#                         如果子图层可见

```python
                            for item in list(sub.items):
```
#                             遍历子图层中的所有图形项

```python
                                if item.visible:
```
#                                 如果该图形项可见

```python
                                    self._draw_item(painter, item)
```
#                                     调用私有方法绘制该图形项

```python
                    
```
#                     空行（含缩进空格）

```python
                    painter.restore()
```
#                     恢复绘制器状态

```python

```
#             空行

```python
            # 工具预览（在文档坐标系下绘制，与图形项保持一致）
```
#             # 绘制工具预览（在文档坐标系下绘制，与图形项保持一致）

```python
            self._current_tool.draw_preview(painter)
```
#             调用当前工具的"绘制预览"方法

```python
            painter.restore()  # 恢复到屏幕坐标系（用于 overlay 等）
```
#             恢复绘制器状态到屏幕坐标系（用于叠加层等界面元素）

```python
            painter.end()
```
#             结束绘制

```python
        except Exception as e:
```
#         捕获异常，赋值给变量 `e`

```python
            import traceback
```
#             导入回溯模块

```python
            traceback.print_exc()
```
#             打印完整的异常堆栈信息

```python
            print(f"[paintEvent ERROR] {e}")
```
#             打印绘制事件的错误信息

```python

```
# 空行

```python
    def _draw_artboard(self, painter: QPainter):
```
#     定义私有方法"绘制画板"（接收绘制器参数）

```python
        doc = self._document
```
#         将文档引用赋值给局部变量

```python
        # 画板阴影
```
#         # 绘制画板阴影

```python
        shadow_rect = QRectF(-2, -2, doc.width + 4, doc.height + 4)
```
#         创建比画板大 4 像素的阴影矩形区域

```python
        painter.fillRect(shadow_rect, QColor(0, 0, 0, 60))
```
#         用半透明黑色（alpha 值 60）填充阴影矩形

```python

```
#         空行

```python
        # 画板背景
```
#         # 绘制画板背景

```python
        artboard_rect = QRectF(0, 0, doc.width, doc.height)
```
#         创建画板矩形区域（从原点开始，宽高为文档尺寸）

```python
        painter.fillRect(artboard_rect, Qt.white)
```
#         用白色填充画板矩形

```python

```
#         空行

```python
        # 画板边框
```
#         # 绘制画板边框

```python
        pen = QPen(QColor(180, 180, 180), 1)
```
#         创建浅灰色、宽度为 1 的画笔

```python
        painter.setPen(pen)
```
#         设置画笔为浅灰色边框

```python
        painter.setBrush(Qt.NoBrush)
```
#         设置画刷为无填充

```python
        painter.drawRect(artboard_rect)
```
#         绘制画板矩形边框

```python

```
# 空行

```python
    def _draw_item(self, painter: QPainter, item: GraphicItem):
```
#     定义私有方法"绘制图形项"（接收绘制器参数和图形项参数）

```python
        """使用 match-case (Python 3.10+) 进行类型分发"""
```
#         """使用 match-case（Python 3.10+ 特性）进行类型分发绘制"""

```python
        painter.save()
```
#         保存当前绘制器状态

```python
        painter.setTransform(item._transform, True)
```
#         设置图形项的变换矩阵（与当前变换合并）

```python
        painter.setOpacity(item.opacity)
```
#         设置图形项的不透明度

```python

```
#         空行

```python
        match item:
```
#         使用 match-case 语句对图形项类型进行分发：

```python
            case GroupItem():
```
#             如果是编组项

```python
                for sub in item.items:
```
#                 遍历编组中的所有子项

```python
                    if sub.visible:
```
#                     如果子项可见

```python
                        self._draw_item(painter, sub)
```
#                         递归绘制该子项

```python
            case TextFrame():
```
#             如果是文本框

```python
                self._draw_text(painter, item)
```
#                 调用私有方法"绘制文字"

```python
            case PathItem():
```
#             如果是路径项

```python
                self._draw_shape(painter, item.style, item.painter_path())
```
#                 调用私有方法"绘制形状"，传入样式和绘制路径

```python
            case RectangleItem():
```
#             如果是矩形项

```python
                self._draw_shape(painter, item.style, item.painter_path())
```
#                 调用私有方法"绘制形状"，传入样式和绘制路径

```python
            case EllipseItem():
```
#             如果是椭圆项

```python
                self._draw_shape(painter, item.style, item.painter_path())
```
#                 调用私有方法"绘制形状"，传入样式和绘制路径

```python
            case _:
```
#             如果是其他未知类型

```python
                path = item.painter_path()
```
#                 获取该图形项的绘制路径

```python
                self._draw_shape(painter, item.style, path)
```
#                 调用私有方法"绘制形状"，传入样式和绘制路径

```python

```
#         空行

```python
        if item.selected:
```
#         如果该图形项被选中

```python
            self._draw_selection_handle(painter, item)
```
#             调用私有方法"绘制选中手柄"

```python

```
#         空行

```python
        painter.restore()
```
#         恢复绘制器状态

```python

```
# 空行

```python
    def _draw_shape(self, painter: QPainter, style: GraphicStyle, path: QPainterPath):
```
#     定义私有方法"绘制形状"（接收绘制器参数、图形样式参数、绘制路径参数）

```python
        """绘制通用形状（支持纯色和渐变填充）"""
```
#         """绘制通用形状（支持纯色填充和渐变填充）"""

```python
        if style.has_fill():
```
#         如果样式设置了填充

```python
            if style.fill_gradient:
```
#             如果填充使用了渐变

```python
                rect = path.boundingRect()
```
#                 获取路径的边界矩形

```python
                gradient = style.fill_gradient.to_qgradient(rect)
```
#                 将渐变对象转换为 Qt 渐变对象

```python
                brush = QBrush(gradient)
```
#                 用渐变创建画刷

```python
            else:
```
#             否则（纯色填充）

```python
                brush = style.to_qbrush()
```
#                 将样式转换为 Qt 画刷

```python
            painter.fillPath(path, brush)
```
#             用画刷填充路径

```python

```
#         空行

```python
        if style.stroke_color and style.stroke_width > 0:
```
#         如果样式设置了笔触颜色且笔触宽度大于 0

```python
            pen = style.to_qpen()
```
#             将样式转换为 Qt 画笔

```python
            painter.setPen(pen)
```
#             设置画笔

```python
            painter.setBrush(Qt.NoBrush)
```
#             设置画刷为无填充

```python
            painter.drawPath(path)
```
#             绘制路径边框

```python

```
# 空行

```python
    def _draw_text(self, painter: QPainter, item: TextFrame):
```
#     定义私有方法"绘制文字"（接收绘制器参数和文本框参数）

```python
        """绘制文字"""
```
#         """绘制文字"""

```python
        rect = item.rect
```
#         获取文本框的矩形区域

```python
        font = item.char_attrs.to_qfont()
```
#         将文本框的字符属性转换为 Qt 字体对象

```python
        color = item.char_attrs.fill_color or QColor(0, 0, 0)
```
#         获取文字填充颜色（如果未设置则使用黑色）

```python

```
#         空行

```python
        painter.setFont(font)
```
#         设置绘制器的字体

```python
        painter.setPen(QPen(color))
```
#         设置绘制器的画笔颜色为文字颜色

```python

```
#         空行

```python
        # 对齐 (使用 match-case)
```
#         # 对齐方式处理（使用 match-case 语句）

```python
        align = Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap
```
#         默认对齐方式为左对齐、垂直居中、自动换行

```python
        match item.para_attrs.justification:
```
#         使用 match-case 根据段落属性的对齐方式进行分发：

```python
            case Justification.CENTER:
```
#             如果是居中对齐

```python
                align = Qt.AlignCenter | Qt.AlignVCenter | Qt.TextWordWrap
```
#                 设置为水平居中、垂直居中、自动换行

```python
            case Justification.RIGHT:
```
#             如果是右对齐

```python
                align = Qt.AlignRight | Qt.AlignVCenter | Qt.TextWordWrap
```
#                 设置为右对齐、垂直居中、自动换行

```python
            case _:
```
#             其他情况（包括左对齐）

```python
                pass  # LEFT 默认
```
#                 不做处理（保持默认的左对齐）

```python

```
#         空行

```python
        painter.drawText(rect, align, item.contents)
```
#         在文本框矩形区域内按照对齐方式绘制文本内容

```python

```
#         空行

```python
        if item == self._editing_text:
```
#         如果该文本框正在编辑中

```python
            pen = QPen(QColor(0, 120, 215), 1, Qt.DashLine)
```
#             创建蓝色、宽度 1、虚线样式的画笔

```python
            painter.setPen(pen)
```
#             设置画笔为蓝色虚线

```python
            painter.setBrush(Qt.NoBrush)
```
#             设置画刷为无填充

```python
            painter.drawRect(rect)
```
#             绘制文本框矩形边框（表示编辑状态）

```python

```
# 空行

```python
    def _draw_selection_handle(self, painter: QPainter, item: GraphicItem):
```
#     定义私有方法"绘制选中手柄"（接收绘制器参数和图形项参数）

```python
        """绘制选中边框（缩放手柄由 SelectionTool.draw_preview 负责）"""
```
#         """绘制选中边框（缩放手柄由选择工具的绘制预览方法负责）"""

```python
        rect = item.bounding_rect()
```
#         获取图形项的边界矩形

```python
        scale = max(painter.transform().m11(), 0.001)
```
#         获取当前变换矩阵的水平缩放系数（最小值 0.001 防止除零）

```python
        pen = QPen(QColor(0, 120, 215), 1.5 / scale)
```
#         创建蓝色、宽度随缩放比例反比调整的画笔（保持视觉一致）

```python
        painter.setPen(pen)
```
#         设置画笔

```python
        painter.setBrush(Qt.NoBrush)
```
#         设置画刷为无填充

```python
        painter.drawRect(rect)
```
#         绘制图形项的选中边框矩形
