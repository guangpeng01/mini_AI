# tools.py 逐行中文注释翻译

> 源文件路径：`tools.py`（共 1934 行）
> 本文件对工具系统源代码进行逐行中文注释翻译。
> 涵盖：`ToolType`/`ResizeHandleType` 枚举、`BaseTool` 抽象基类、
> `SelectionTool`、`DirectSelectTool`、`ShapeTool`/`RectangleTool`/`EllipseTool`、
> `AddAnchorPointTool`、`DeleteAnchorPointTool`、`ConvertAnchorPointTool`、
> `PenTool`、`TextTool`、`HandTool`。

---

```python
"""
```
# 三引号字符串结束 —— 模块文档字符串至此闭合

```python
工具系统 (Python 3.10+) —— 选择、矩形、椭圆、钢笔、文字工具
```
# 模块标题：描述本模块为工具系统，要求 Python 3.10+，支持选择、矩形、椭圆、钢笔、文字等多种工具

```python

```
# 空行，分隔文档内容

```python
架构优化:
```
# 架构优化策略小节标题

```python
- 使用 __slots__ 减少内存占用
```
# 优化策略一：通过 `__slots__` 限定实例属性，禁止动态 `__dict__` 字典，减少每个实例的内存占用

```python
- 使用 X | None 替代 Optional[X]
```
# 优化策略二：采用 Python 3.10+ 联合类型语法 `X | None` 替代 `typing.Optional[X]`，写法更简洁

```python
- 使用 match-case 替代 if-elif 链
```
# 优化策略三：使用 Python 3.10+ 结构化模式匹配 `match-case` 语句替代传统 `if-elif` 条件链，提升多分支代码清晰度

```python
- 使用 @override 风格注释 (PEP 698 ready)
```
# 优化策略四：为未来的 PEP 698 `@override` 装饰器覆写检查做准备，使代码风格提前对齐

```python
"""
```
# 三引号字符串结束 —— 模块文档字符串至此闭合

```python

```
# 空行（代码结构分隔）

```python
from __future__ import annotations
```
# 导入 `annotations` 特性：使类型注解在运行时惰性求值，支持前向引用和避免循环导入

```python

```
# 空行（代码结构分隔）

```python
import math
```
# 导入标准数学库 `math`：提供三角函数（atan2/sin/cos）和 sqrt 开方运算

```python
from abc import ABC, abstractmethod
```
# 从 `abc` 模块导入：`ABC` 抽象基类、`@abstractmethod` 抽象方法装饰器

```python
from enum import Enum, auto
```
# 从 `enum` 模块导入：`Enum` 枚举基类、`auto()` 自动编号函数

```python

```
# 空行（代码结构分隔）

```python
from PyQt5.QtCore import QPointF, QRectF, Qt
```
# 导入 PyQt5 核心类：`QPointF` 二维浮点坐标、`QRectF` 浮点矩形、`Qt` 全局常量（修饰键/按键码）

```python
from PyQt5.QtGui import QColor, QPainter, QPen
```
# 导入 PyQt5 图形类：`QColor` 颜色、`QPainter` 绘图引擎、`QPen` 画笔

```python

```
# 空行（代码结构分隔）

```python
from .graphics import (
```
# 从当前包 `graphics` 子模块导入图形相关类

```python
    GraphicItem, RectangleItem, EllipseItem, TextFrame,
```
#   导入四种图形项：`GraphicItem` 基类、`RectangleItem` 矩形、`EllipseItem` 椭圆、`TextFrame` 文字框

```python
    PathItem, GraphicStyle, AnchorPoint, AnchorPointType,
```
#   导入路径相关：`PathItem` 贝塞尔路径、`GraphicStyle` 样式、`AnchorPoint` 锚点、`AnchorPointType` 锚点类型

```python
    Command, MoveItemsCommand, ModifyAnchorCommand, ResizeItemCommand,
```
#   导入命令模式四件套：`Command` 基类、`MoveItemsCommand` 移动命令、`ModifyAnchorCommand` 修改锚点命令、`ResizeItemCommand` 缩放命令（用于撤销/重做）

```python
)
```
# 从 graphics 子模块导入结束

```python
from .document import Document, Layer
```
# 从当前包 `document` 子模块导入：`Document` 文档类、`Layer` 图层类

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
class ToolType(Enum):
```
# 定义 `ToolType` 枚举类：为所有可用工具提供唯一类型标识符，使用 `auto()` 自动分配值

```python
    """工具类型"""
```
# 类/方法文档字符串：工具类型

```python
    SELECTION = auto()              # 选择工具 (V)
```
#     枚举成员：选择工具，对应快捷键 V

```python
    DIRECT_SELECT = auto()          # 直接选择工具 (A)
```
#     枚举成员：直接选择工具，对应快捷键 A

```python
    RECTANGLE = auto()              # 矩形工具 (M)
```
#     枚举成员：矩形工具，对应快捷键 M

```python
    ELLIPSE = auto()                # 椭圆工具 (L)
```
#     枚举成员：椭圆工具，对应快捷键 L

```python
    PEN = auto()                    # 钢笔工具 (P)
```
#     枚举成员：钢笔工具，对应快捷键 P

```python
    ADD_ANCHOR = auto()             # 添加锚点工具 (+)
```
#     枚举成员：添加锚点工具，对应快捷键 +

```python
    DELETE_ANCHOR = auto()          # 删除锚点工具 (-)
```
#     枚举成员：删除锚点工具，对应快捷键 -

```python
    CONVERT_ANCHOR = auto()         # 转换锚点工具 (Shift+C)
```
#     枚举成员：转换锚点工具，对应快捷键 Shift+C

```python
    TEXT = auto()                   # 文字工具 (T)
```
#     枚举成员：文字工具，对应快捷键 T

```python
    HAND = auto()                   # 抓手工具 (H)
```
#     枚举成员：抓手工具，对应快捷键 H

```python
    ZOOM = auto()                   # 缩放工具 (Z)
```
#     枚举成员：缩放工具，对应快捷键 Z

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
class BaseTool(ABC):
```
# 定义工具抽象基类 `BaseTool`，继承 `ABC`：为所有具体工具提供统一的鼠标/键盘/绘制事件接口

```python
    """工具基类（抽象）"""
```
# 类/方法文档字符串：工具基类（抽象）

```python
    __slots__ = ('tool_type', '_document', '_is_drawing')
```
#     声明实例属性槽位：限定只能拥有 tool_type、_document、_is_drawing 三个属性，禁止动态添加

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self, tool_type: ToolType):
```
# 初始化方法（构造函数），接收自身引用、工具类型标识：工具类型，无返回值

```python
        self.tool_type = tool_type
```
#         保存传入的工具类型标识符到实例属性

```python
        self._document: Document | None = None
```
#         初始化私有文档引用为空，后续通过 set_document() 注入

```python
        self._is_drawing: bool = False
```
#         初始化绘制状态标志为 False，标记当前未在绘制中

```python

```
# 空行（代码结构分隔）

```python
    def set_document(self, doc: Document):
```
# 设置关联的文档对象，接收自身引用、文档对象：文档对象，无返回值

```python
        self._document = doc
```
#         将传入的文档实例保存为私有属性

```python

```
# 空行（代码结构分隔）

```python
    @property
```
#     只读属性装饰器：将方法转为属性访问

```python
    def document(self) -> Document | None:
```
# 文档属性（只读），接收自身引用，返回可选的文档对象

```python
        return self._document
```
#         返回当前关联的文档实例（可能为 None）

```python

```
# 空行（代码结构分隔）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# 鼠标按下事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        pass
```
#         空实现（占位），由具体工具子类覆写

```python

```
# 空行（代码结构分隔）

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# 鼠标移动事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        pass
```
#         空实现（占位），由具体工具子类覆写

```python

```
# 空行（代码结构分隔）

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# 鼠标释放事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        pass
```
#         空实现（占位），由具体工具子类覆写

```python

```
# 空行（代码结构分隔）

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
```
# 鼠标双击事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        pass
```
#         空实现（占位），由具体工具子类覆写

```python

```
# 空行（代码结构分隔）

```python
    def key_press(self, key: int, modifiers: int):
```
# 键盘按键事件处理方法，接收自身引用、按键码：整数、修饰键标志位：整数，无返回值

```python
        pass
```
#         空实现（占位），由具体工具子类覆写

```python

```
# 空行（代码结构分隔）

```python
    def draw_preview(self, painter: QPainter):
```
# 绘制预览方法，接收自身引用、绘图引擎：绘图引擎，无返回值

```python
        pass
```
#         空实现（占位），由具体工具子类覆写

```python

```
# 空行（代码结构分隔）

```python
    def cancel(self):
```
# 取消当前操作并重置状态，接收自身引用，无返回值

```python
        self._is_drawing = False
```
#         将绘制状态标志重置为 False，标记取消绘制

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
# ── 缩放手柄类型 ───────────────────────────────────────────
```
# 分隔注释：缩放手柄类型枚举定义区域

```python

```
# 空行（代码结构分隔）

```python
class ResizeHandleType(Enum):
```
# 定义 `ResizeHandleType` 枚举：标识选择工具缩放手柄的 8 个位置（四角 + 四边中点）

```python
    """缩放手柄位置类型"""
```
# 类/方法文档字符串：缩放手柄位置类型

```python
    TOP_LEFT = auto()
```
# `TOP_LEFT` 左上角缩放手柄

```python
    TOP_CENTER = auto()
```
# `TOP_CENTER` 上边中点缩放手柄

```python
    TOP_RIGHT = auto()
```
# `TOP_RIGHT` 右上角缩放手柄

```python
    MIDDLE_LEFT = auto()
```
# `MIDDLE_LEFT` 左边中点缩放手柄

```python
    MIDDLE_RIGHT = auto()
```
# `MIDDLE_RIGHT` 右边中点缩放手柄

```python
    BOTTOM_LEFT = auto()
```
# `BOTTOM_LEFT` 左下角缩放手柄

```python
    BOTTOM_CENTER = auto()
```
# `BOTTOM_CENTER` 下边中点缩放手柄

```python
    BOTTOM_RIGHT = auto()
```
# `BOTTOM_RIGHT` 右下角缩放手柄

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
# ── 选择工具 ──────────────────────────────────────────────
```
# 分隔注释：选择工具类定义区域

```python

```
# 空行（代码结构分隔）

```python
class SelectionTool(BaseTool):
```
# 定义 `SelectionTool` 选择工具类：继承 `BaseTool`，实现点击选择、框选、多选拖拽、缩放手柄

```python
    """选择工具 —— 点击选择 / 框选 / 多选拖拽 / 缩放手柄"""
```
# 类/方法文档字符串：选择工具 —— 点击选择 / 框选 / 多选拖拽 / 缩放手柄

```python
    __slots__ = ('_drag_start', '_drag_current', '_dragging_item',
```
# 声明实例属性槽位：限定该类只能拥有元组中列出的属性，禁止动态添加新属性

```python
                 '_drag_offset', '_is_marquee',
```
# __slots__ 续行：'_drag_offset' 单项拖拽时鼠标与图形项左上角的坐标差值、'_is_marquee' 框选模式标志（空白区域拖拽时为 True）

```python
                 '_dragging_items', '_drag_offsets',
```
# __slots__ 续行：'_dragging_items' 多选拖拽时保存的所有选中图形项列表、'_drag_offsets' 多选拖拽时每个图形项对应的鼠标偏移量列表

```python
                 '_total_dx', '_total_dy',
```
# __slots__ 续行：'_total_dx' 多选拖拽累计水平总距离（用于撤销命令）、'_total_dy' 多选拖拽累计垂直总距离（用于撤销命令）

```python
                 '_is_scaling', '_scale_handle',
```
# __slots__ 续行：'_is_scaling' 是否处于缩放操作模式（拖拽手柄时为 True）、'_scale_handle' 当前拖拽的缩放手柄类型（TOP_LEFT/MIDDLE_RIGHT 等枚举值）

```python
                 '_scale_orig_rect', '_scale_orig_br',
```
# __slots__ 续行：'_scale_orig_rect' 缩放前的原始矩形快照（用于计算新宽高）、'_scale_orig_br' 缩放前的包围矩形快照（用于撤销对比新旧矩形）

```python
                 '_scale_pivot', '_scale_keep_ratio')
```
# __slots__ 续行：'_scale_pivot' 缩放时对角的固定锚点坐标（缩放以此为不动点）、'_scale_keep_ratio' 是否等比缩放约束（Shift 键控制）

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self):
```
# 初始化方法（构造函数），接收自身引用，无返回值

```python
        super().__init__(ToolType.SELECTION)
```
#         调用父类 BaseTool 构造函数，传入选择工具类型标识符

```python
        self._drag_start: QPointF | None = None
```
#         初始化拖拽起始坐标为 None

```python
        self._drag_current: QPointF | None = None
```
#         初始化拖拽当前坐标为 None

```python
        self._dragging_item: GraphicItem | None = None
```
# 初始化单选拖拽目标图形项为 None，表示当前无活跃的拖拽目标

```python
        self._drag_offset = QPointF(0, 0)
```
# 初始化拖拽偏移量为原点 (0,0)，记录鼠标按下位置与图形项左上角的坐标差值

```python
        self._is_marquee: bool = False
```
#         初始化框选模式标志为 False

```python
        # 多选拖拽支持
```
# 注释说明：多选拖拽支持

```python
        self._dragging_items: list[GraphicItem] = []
```
#         初始化多选拖拽图形项列表为空

```python
        self._drag_offsets: list[QPointF] = []
```
#         初始化多选拖拽偏移量列表为空

```python
        self._total_dx: float = 0.0
```
#         初始化累计水平拖拽距离为 0

```python
        self._total_dy: float = 0.0
```
#         初始化累计垂直拖拽距离为 0

```python
        # 缩放支持
```
# 注释说明：缩放支持

```python
        self._is_scaling: bool = False
```
#         初始化缩放操作标志为 False

```python
        self._scale_handle: ResizeHandleType | None = None
```
#         初始化当前拖拽的缩放手柄类型为 None

```python
        self._scale_orig_rect = QRectF()
```
#         创建空矩形保存缩放前的原始矩形

```python
        self._scale_orig_br = QRectF()  # 缩放前 bounding_rect
```
#         创建空矩形保存缩放前的包围矩形快照

```python
        self._scale_pivot = QPointF()   # 缩放锚点（对角的那个固定点）
```
#         创建空坐标点保存缩放固定锚点（对角位置）

```python
        self._scale_keep_ratio: bool = False
```
#         初始化等比缩放约束标志为 False

```python

```
# 空行（代码结构分隔）

```python
    # ── 手柄检测 ──
```
# 分隔注释：手柄检测辅助方法区域

```python

```
# 空行（代码结构分隔）

```python
    @staticmethod
```
# staticmethod 装饰器

```python
    def _get_handle_at(item: GraphicItem, pos: QPointF, tolerance: float = 8) -> ResizeHandleType | None:
```
# 定义 `_get_handle_at` 静态方法：检测鼠标 `pos`（世界坐标）是否在 `item` 的缩放手柄上，容差 `tolerance` 默认 8px，返回手柄类型或 None

```python
        """检测鼠标是否在缩放手柄上（pos 为世界坐标）"""
```
# 类/方法文档字符串：检测鼠标是否在缩放手柄上（pos 为世界坐标）

```python
        local_rect = item.bounding_rect()
```
#         获取图形项在本地坐标系下的包围矩形

```python
        rect = item._transform.mapRect(local_rect)
```
#         通过图形项的变换矩阵将本地矩形映射到世界坐标系

```python
        hs = tolerance  # 手柄命中容差
```
#         将容差值赋给手柄命中检测半径变量

```python
        corners = {
```
#         构建四角手柄位置字典：键为手柄类型，值为世界坐标

```python
            ResizeHandleType.TOP_LEFT: rect.topLeft(),
```
#   左上角手柄 → 矩形左上角坐标 `rect.topLeft()`

```python
            ResizeHandleType.TOP_RIGHT: rect.topRight(),
```
#   右上角手柄 → 矩形右上角坐标 `rect.topRight()`

```python
            ResizeHandleType.BOTTOM_LEFT: rect.bottomLeft(),
```
#   左下角手柄 → 矩形左下角坐标 `rect.bottomLeft()`

```python
            ResizeHandleType.BOTTOM_RIGHT: rect.bottomRight(),
```
#   右下角手柄 → 矩形右下角坐标 `rect.bottomRight()`

```python
        }
```
#         手柄位置字典定义结束

```python
        edges = {
```
#         构建四边中点手柄位置字典：键为手柄类型，值为世界坐标

```python
            ResizeHandleType.TOP_CENTER: QPointF(rect.center().x(), rect.top()),
```
#   上边中点手柄：x = 矩形中心x，y = 矩形顶部y

```python
            ResizeHandleType.BOTTOM_CENTER: QPointF(rect.center().x(), rect.bottom()),
```
#   下边中点手柄：x = 矩形中心x，y = 矩形底部y

```python
            ResizeHandleType.MIDDLE_LEFT: QPointF(rect.left(), rect.center().y()),
```
#   左边中点手柄：x = 矩形左边x，y = 矩形中心y

```python
            ResizeHandleType.MIDDLE_RIGHT: QPointF(rect.right(), rect.center().y()),
```
#   右边中点手柄：x = 矩形右边x，y = 矩形中心y

```python
        }
```
#         手柄位置字典定义结束

```python

```
# 空行（代码结构分隔）

```python
        for htype, pt in corners.items():
```
# 遍历四角手柄字典：`htype` 手柄类型、`pt` 对应角点坐标

```python
            if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:
```
#             判断鼠标坐标与手柄坐标在 x/y 方向距离是否都小于容差

```python
                return htype
```
#                 命中则返回对应的手柄类型

```python
        for htype, pt in edges.items():
```
# 遍历四边中点手柄字典：角手柄未命中时继续检测边手柄

```python
            if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:
```
#             判断鼠标坐标与手柄坐标在 x/y 方向距离是否都小于容差

```python
                return htype
```
#                 命中则返回对应的手柄类型

```python
        return None
```
# 所有 8 个手柄都未命中，返回 None

```python

```
# 空行（代码结构分隔）

```python
    # ── 鼠标事件 ──
```
# 分隔注释：鼠标事件处理方法区域

```python

```
# 空行（代码结构分隔）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# 鼠标按下事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        self._drag_start = QPointF(pos)
```
#         记录拖拽起始坐标

```python
        self._drag_current = QPointF(pos)
```
#         记录拖拽当前坐标（初始与起始相同）

```python
        self._total_dx = 0.0
```
#         重置累计水平拖拽距离

```python
        self._total_dy = 0.0
```
#         重置累计垂直拖拽距离

```python
        self._is_scaling = False
```
# 重置缩放操作标志为 False，退出缩放模式

```python
        self._scale_handle = None
```
# 清空当前拖拽的缩放手柄类型引用，表示无活跃缩放操作

```python
        self._scale_keep_ratio = bool(modifiers & Qt.ShiftModifier)
```
#         检测 Shift 键是否按下，决定是否等比缩放

```python

```
# 空行（代码结构分隔）

```python
        # 检查是否点击了已选中项的缩放手柄
```
# 注释说明：检查是否点击了已选中项的缩放手柄

```python
        sel = self._document.get_selection()
```
#         获取文档中当前选中的图形项列表

```python
        if len(sel) == 1:
```
#         如果只选中了一个图形项，检查是否点击了缩放手柄

```python
            handle = self._get_handle_at(sel[0], pos)
```
#             检测鼠标位置是否在该选中项的缩放手柄上

```python
            if handle is not None:
```
#             如果命中了缩放手柄

```python
                self._dragging_item = sel[0]
```
#                 将选中的图形项设为当前拖拽目标

```python
                self._is_scaling = True
```
#                 进入缩放模式

```python
                self._scale_handle = handle
```
#                 记录命中的手柄类型

```python
                # 使用世界坐标系的 bounding_rect（含 item 变换）
```
# 注释说明：使用世界坐标系的 bounding_rect（含 item 变换）

```python
                world_rect = sel[0]._transform.mapRect(sel[0].bounding_rect())
```
#                 获取图形项在世界坐标系中的包围矩形

```python
                self._scale_orig_rect = QRectF(world_rect)
```
#                 保存缩放前的原始矩形

```python
                self._scale_orig_br = QRectF(world_rect)
```
#                 保存缩放前的包围矩形快照（用于撤销对比）

```python
                # 缩放的固定锚点是对角
```
# 注释说明：缩放的固定锚点是对角

```python
                self._scale_pivot = self._get_opposite_corner(handle, self._scale_orig_rect)
```
# 获取当前缩放手柄对角的固定锚点坐标，作为缩放的固定参照点

```python
                return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        item = self._document.get_item_at(pos.x(), pos.y())
```
# 通过文档查找鼠标位置下的最顶层图形项

```python
        if item:
```
#         如果鼠标下方有图形项

```python
            self._is_marquee = False  # 点击了物体，不是框选
```
#             标记为非框选模式（点击了具体物体）

```python
            # 如果点击的项未被选中，先清除选择并选中它
```
# 注释说明：如果点击的项未被选中，先清除选择并选中它

```python
            if not item.selected:
```
#             如果点击的图形项当前未被选中

```python
                if not (modifiers & Qt.ShiftModifier):
```
#                 如果未按住 Shift 键（不追加选择）

```python
                    self._document.clear_selection()
```
#                     清除文档中所有图形项的选中状态

```python
                item.selected = True
```
# 将当前图形项设为选中状态

```python

```
# 空行（代码结构分隔）

```python
            # 准备拖拽
```
# 注释说明：准备拖拽

```python
            sel = self._document.get_selection()
```
#         获取文档中当前选中的图形项列表

```python
            if len(sel) > 1:
```
#             如果选中了多个图形项，启用多选拖拽模式

```python
                # 多选状态 → 多选拖拽模式
```
# 注释说明：多选状态 → 多选拖拽模式

```python
                self._dragging_items = list(sel)
```
#                 将所有选中项保存到多选拖拽列表

```python
                self._drag_offsets = [pos - it._transform.mapRect(it.bounding_rect()).topLeft() for it in sel]
```
# 为每个选中项计算拖拽偏移量：鼠标位置减去该项的世界坐标左上角

```python
                self._dragging_item = None
```
#         清空拖拽目标

```python
            else:
```
# 否则（以上条件均不满足时执行）

```python
                # 单选或仅选中了一项 → 单项拖拽（不要清除再重新选中）
```
# 注释说明：单选或仅选中了一项 → 单项拖拽（不要清除再重新选中）

```python
                self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python
                self._drag_offset = pos - item._transform.mapRect(item.bounding_rect()).topLeft()
```
#                 计算拖拽偏移量（鼠标位置减去图形项左上角）

```python
                self._dragging_items = []
```
# 清空多选拖拽的图形项列表

```python
        else:
```
# 否则（以上条件均不满足时执行）

```python
            if not (modifiers & Qt.ShiftModifier):
```
#                 如果未按住 Shift 键（不追加选择）

```python
                self._document.clear_selection()
```
#                     清除文档中所有图形项的选中状态

```python
            self._dragging_item = None
```
#         清空拖拽目标

```python
            self._dragging_items = []
```
# 清空多选拖拽的图形项列表

```python
            self._is_marquee = True
```
#             进入框选模式

```python

```
# 空行（代码结构分隔）

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# 鼠标移动事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if self._drag_start is None:
```
#         如果没有拖拽起始点，不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        self._drag_current = QPointF(pos)
```
#         记录拖拽当前坐标（初始与起始相同）

```python

```
# 空行（代码结构分隔）

```python
        # 缩放模式
```
# 注释说明：缩放模式

```python
        if self._is_scaling and self._dragging_item:
```
#         如果处于缩放模式且有拖拽目标

```python
            self._apply_resize(pos, bool(modifiers & Qt.ShiftModifier))
```
# 执行缩放变换计算：根据缩放手柄类型和鼠标位置更新图形项的变换矩阵

```python
            if self._document:
```
# 如果工具关联了文档

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        dx = pos.x() - self._drag_start.x()
```
#         计算水平方向增量

```python
        dy = pos.y() - self._drag_start.y()
```
#         计算垂直方向增量

```python
        # Shift 约束水平/垂直移动
```
# 注释说明：Shift 约束水平/垂直移动

```python
        if modifiers & Qt.ShiftModifier:
```
#         如果按住 Shift，约束为纯水平或垂直移动

```python
            dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)
```
# 三元表达式：若水平偏移大于垂直偏移则约束为纯水平移动，否则约束为纯垂直移动（Shift约束）

```python

```
# 空行（代码结构分隔）

```python
        if self._dragging_items:
```
#         如果处于多选拖拽模式

```python
            for item in self._dragging_items:
```
# 遍历多选拖拽列表中的每个图形项，逐一处理移动操作

```python
                item.move_by(dx, dy)
```
# 将图形项按增量 (dx, dy) 平移，同时更新其在世界坐标系中的位置

```python
            self._total_dx += dx
```
# 累计水平拖拽总距离（+= 累加，用于撤销命令记录实际移动量）

```python
            self._total_dy += dy
```
# 累计垂直拖拽总距离（+= 累加，用于撤销命令记录实际移动量）

```python
            self._drag_start = QPointF(pos)
```
#         记录拖拽起始坐标

```python
            if self._document:
```
# 如果工具关联了文档

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python
        elif self._dragging_item and not self._is_scaling:
```
# 否则如果是单项拖拽模式（有拖拽目标且非缩放状态）：移动单个图形项

```python
            self._dragging_item.move_by(dx, dy)
```
# 将拖拽目标图形项按增量 (dx, dy) 平移移动

```python
            self._total_dx += dx
```
# 累计水平拖拽总距离（+= 累加，用于撤销命令记录实际移动量）

```python
            self._total_dy += dy
```
# 累计垂直拖拽总距离（+= 累加，用于撤销命令记录实际移动量）

```python
            self._drag_start = QPointF(pos)
```
#         记录拖拽起始坐标

```python
            if self._document:
```
# 如果工具关联了文档

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行（代码结构分隔）

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# 鼠标释放事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        # 缩放完成：记录命令（通过 execute_command 统一入口）
```
# 注释说明：缩放完成：记录命令（通过 execute_command 统一入口）

```python
        if self._is_scaling and self._dragging_item and self._document:
```
# 条件检查：`self._is_scaling` 当前处于缩放操作中，`self._dragging_item` 有有效的拖拽目标图形项，`self._document` 工具已关联文档——三个条件同时满足时才记录缩放撤销命令

```python
            new_world_rect = self._dragging_item._transform.mapRect(self._dragging_item.bounding_rect())
```
# 获取缩放后图形项在世界坐标系中的包围矩形：将图形项的本地矩形通过其变换矩阵映射到世界坐标

```python
            if new_world_rect != self._scale_orig_br:
```
# 如果存在选中的图形项

```python
                # 通过尺寸变化记录（使用世界坐标矩形）
```
# 注释说明：通过尺寸变化记录（使用世界坐标矩形）

```python
                cmd = ResizeItemCommand(
```
# 创建缩放命令对象，记录缩放前后的矩形状态，用于撤销/重做操作

```python
                    self._document, self._dragging_item,
```
# ResizeItemCommand 参数续行：self._document 文档对象（命令执行上下文）、self._dragging_item 被缩放的图形项（记录操作目标）

```python
                    self._scale_orig_br, new_world_rect,
```
# ResizeItemCommand 参数续行：self._scale_orig_br 缩放前的包围矩形快照（旧值）、new_world_rect 缩放后的包围矩形（新值）

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                self._document.execute_command(cmd)
```
# 通过文档统一入口执行命令对象（自动推入撤销栈，支持 Ctrl+Z 撤销）

```python
            self._is_scaling = False
```
# 重置缩放操作标志为 False，退出缩放模式

```python
            self._scale_handle = None
```
# 清空当前拖拽的缩放手柄类型引用，表示无活跃缩放操作

```python
            self._dragging_item = None
```
#         清空拖拽目标

```python
            self._drag_start = None
```
# 清空拖拽起始点

```python
            self._drag_current = None
```
#         清空拖拽当前坐标

```python
            self._total_dx = 0.0
```
#         重置累计水平拖拽距离

```python
            self._total_dy = 0.0
```
#         重置累计垂直拖拽距离

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # 多选拖拽完成后记录移动命令（用于撤销，通过 execute_command 统一入口）
```
# 注释说明：多选拖拽完成后记录移动命令（用于撤销，通过 execute_command 统一入口）

```python
        moved_items = self._dragging_items if self._dragging_items else (
```
# 构建实际需要记录移动的图形项列表：多选拖拽时直接用 `_dragging_items` 列表，单项拖拽时包装为单元素列表 `[self._dragging_item]`，无拖拽目标则为空列表

```python
            [self._dragging_item] if self._dragging_item else []
```
# 三元表达式：有单项拖拽目标则包装为列表，否则为空列表

```python
        )
```
# 闭合三元表达式括号，完成 moved_items 赋值

```python
        if moved_items and self._document and (self._total_dx != 0 or self._total_dy != 0):
```
# 条件检查：`moved_items` 有被移动的图形项列表（非空），`self._document` 工具已关联文档，`self._total_dx != 0 or self._total_dy != 0` 累计移动距离不为零——三个条件同时满足才记录移动撤销命令

```python
            cmd = MoveItemsCommand(
```
# 将 MoveItemsCommand(...) 构造的撤销命令对象保存到 cmd，记录本次多选/单项拖拽的移动信息

```python
                self._document, moved_items,
```
# MoveItemsCommand 参数续行：self._document 文档对象（命令执行上下文）、moved_items 本次拖拽移动的所有图形项列表

```python
                self._total_dx, self._total_dy,
```
# MoveItemsCommand 参数续行：self._total_dx 累计水平移动总量、self._total_dy 累计垂直移动总量
```
# 闭合括号：结束函数调用的参数列表

```python
            self._document.execute_command(cmd)
```
# 通过文档统一入口执行命令对象（自动推入撤销栈，支持 Ctrl+Z 撤销）

```python

```
# 空行（代码结构分隔）

```python
        if self._is_marquee and self._drag_start and self._document:
```
# 如果处于框选模式

```python
            rect = QRectF(self._drag_start, pos).normalized()
```
#             构建规范化框选矩形

```python
            if rect.width() > 2 and rect.height() > 2:
```
# 如果矩形尺寸足够大（过滤意外点击）

```python
                for layer in self._document.layers:
```
# 遍历文档的所有图层，每次迭代将当前图层元素赋给 layer

```python
                    items = layer.get_items_in_rect(
```
# 调用图层的 `get_items_in_rect` 方法，查询框选矩形范围内的所有图形项

```python
                        rect.x(), rect.y(), rect.width(), rect.height(),
```
# 获取矩形左上角的 x 坐标（世界坐标系中的水平位置）

```python
                    )
```
# 闭合括号：结束函数调用的参数列表

```python
                    for item in items:
```
# 遍历框选命中的图形项列表，将每个项标记为选中状态

```python
                        item.selected = True
```
# 将当前图形项设为选中状态

```python

```
# 空行（代码结构分隔）

```python
        self._drag_start = None
```
# 清空拖拽起始点

```python
        self._drag_current = None
```
#         清空拖拽当前坐标

```python
        self._dragging_item = None
```
#         清空拖拽目标

```python
        self._dragging_items = []
```
# 清空多选拖拽的图形项列表

```python
        self._is_marquee = False
```
#         退出框选模式

```python
        self._is_scaling = False
```
# 重置缩放操作标志为 False，退出缩放模式

```python
        self._scale_handle = None
```
# 清空当前拖拽的缩放手柄类型引用，表示无活跃缩放操作

```python
        self._total_dx = 0.0
```
#         重置累计水平拖拽距离

```python
        self._total_dy = 0.0
```
#         重置累计垂直拖拽距离

```python

```
# 空行（代码结构分隔）

```python
    # ── 缩放核心 ──
```
# 分隔注释：缩放核心算法区域

```python

```
# 空行（代码结构分隔）

```python
    @staticmethod
```
# staticmethod 装饰器

```python
    def _get_opposite_corner(handle: ResizeHandleType, rect: QRectF) -> QPointF:
```
# 定义 `_get_opposite_corner` 静态方法：根据手柄类型 `handle` 和矩形 `rect`，返回对角的固定锚点坐标

```python
        """获取缩放手柄对面的固定锚点"""
```
# 类/方法文档字符串：获取缩放手柄对面的固定锚点

```python
        match handle:
```
# `match-case` 模式匹配（Python 3.10+）：根据手柄类型枚举分支处理

```python
            case ResizeHandleType.TOP_LEFT:
```
#   左上角手柄的对角固定锚点 → 右下角 `rect.bottomRight()`

```python
                return rect.bottomRight()
```
#   返回矩形右下角坐标

```python
            case ResizeHandleType.TOP_CENTER:
```
#   上边中点手柄的对角固定锚点 → 底边中点

```python
                return QPointF(rect.center().x(), rect.bottom())
```
#   返回底边中点坐标：x = 矩形中心x，y = 矩形底部y

```python
            case ResizeHandleType.TOP_RIGHT:
```
#   右上角手柄的对角固定锚点 → 左下角 `rect.bottomLeft()`

```python
                return rect.bottomLeft()
```
#   返回矩形左下角坐标

```python
            case ResizeHandleType.MIDDLE_LEFT:
```
#   左边中点手柄的对角固定锚点 → 右边中点

```python
                return QPointF(rect.right(), rect.center().y())
```
#   返回右边中点坐标：x = 矩形右边x，y = 矩形中心y

```python
            case ResizeHandleType.MIDDLE_RIGHT:
```
#   右边中点手柄的对角固定锚点 → 左边中点

```python
                return QPointF(rect.left(), rect.center().y())
```
#   返回左边中点坐标：x = 矩形左边x，y = 矩形中心y

```python
            case ResizeHandleType.BOTTOM_LEFT:
```
#   左下角手柄的对角固定锚点 → 右上角 `rect.topRight()`

```python
                return rect.topRight()
```
#   返回矩形右上角坐标

```python
            case ResizeHandleType.BOTTOM_CENTER:
```
#   下边中点手柄的对角固定锚点 → 顶边中点

```python
                return QPointF(rect.center().x(), rect.top())
```
#   返回顶边中点坐标：x = 矩形中心x，y = 矩形顶部y

```python
            case ResizeHandleType.BOTTOM_RIGHT:
```
#   右下角手柄的对角固定锚点 → 左上角 `rect.topLeft()`

```python
                return rect.topLeft()
```
#   返回矩形左上角坐标

```python

```
# 空行（代码结构分隔）

```python
    def _apply_resize(self, mouse_pos: QPointF, keep_ratio: bool):
```
# 定义 `_apply_resize` 方法：根据手柄类型和鼠标位置实时调整图形大小

```python
        """根据手柄类型和鼠标位置调整图形大小"""
```
# 类/方法文档字符串：根据手柄类型和鼠标位置调整图形大小

```python
        if not self._dragging_item:
```
# 前置检查：如果当前没有拖拽目标图形项（`_dragging_item` 为 None），说明没有可缩放的对象，提前退出避免空指针错误

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        pivot = self._scale_pivot
```
# 将缩放固定锚点坐标 `self._scale_pivot` 赋值给局部变量 `pivot`，方便后续计算中使用

```python
        orig = self._scale_orig_rect
```
# 将缩放前的原始矩形 `self._scale_orig_rect` 赋值给局部变量 `orig`，用于后续计算原始宽高

```python
        mx, my = mouse_pos.x(), mouse_pos.y()
```
将鼠标位置的世界坐标分量提取到局部变量：`mx` 鼠标 x 坐标（缩放手柄位置）、`my` 鼠标 y 坐标（缩放手柄位置），供后续缩放尺寸计算使用

```python
        px, py = pivot.x(), pivot.y()
```
将缩放固定锚点的世界坐标分量提取到局部变量：`px` 固定锚点 x 坐标（缩放的不动点水平位置）、`py` 固定锚点 y 坐标（缩放的不动点垂直位置），供后续新宽高计算使用

```python

```
# 空行（代码结构分隔）

```python
        # 根据手柄确定新宽高
```
# 注释说明：根据手柄确定新宽高

```python
        match self._scale_handle:
```
# Python 3.10+ 结构化模式匹配：根据当前拖拽的缩放手柄类型（`self._scale_handle`）计算新矩形的宽高；不同手柄位置决定哪些维度会随鼠标移动而改变

```python
            case ResizeHandleType.TOP_LEFT:
```
#   左上角手柄的对角固定锚点 → 右下角 `rect.bottomRight()`

```python
                new_w, new_h = px - mx, py - my
```
# 计算左上角手柄的新宽高：`new_w = px - mx` 固定锚点 x - 鼠标 x（从鼠标向右到固定点），`new_h = py - my` 固定锚点 y - 鼠标 y

```python
            case ResizeHandleType.TOP_CENTER:
```
#   上边中点手柄的对角固定锚点 → 底边中点

```python
                new_w = orig.width()
```
# 获取缩放前矩形的原始宽度 `orig.width()`，作为上/下边中点手柄缩放时保持不变的宽度值

```python
                new_h = py - my
```
# 上边中点手柄：宽度保持不变（`new_w = orig.width()`），高度随鼠标移动变化 `new_h = py - my`

```python
            case ResizeHandleType.TOP_RIGHT:
```
#   右上角手柄的对角固定锚点 → 左下角 `rect.bottomLeft()`

```python
                new_w = mx - px
```
# 右上角手柄：宽度 `new_w = mx - px` 鼠标 x - 固定锚点 x（从固定点向右到鼠标），高度 `new_h = py - my` 从固定锚点向上到鼠标

```python
            case ResizeHandleType.MIDDLE_LEFT:
```
#   左边中点手柄的对角固定锚点 → 右边中点

```python
                new_w = px - mx
```
# 左边中点手柄：宽度 `new_w = px - mx`，高度保持原始值不变
```
# 获取缩放前矩形的原始高度 `orig.height()`，作为左/右边中点手柄缩放时保持不变的高度值

```python
            case ResizeHandleType.MIDDLE_RIGHT:
```
#   右边中点手柄的对角固定锚点 → 左边中点

```python
                new_w = mx - px
```
# 右边中点手柄：宽度 `new_w = mx - px` 鼠标到固定锚点的水平距离，高度保持不变
```
# 获取缩放前矩形的原始高度 `orig.height()`，作为左边中点手柄缩放时保持不变的高度值

```python
            case ResizeHandleType.BOTTOM_LEFT:
```
#   左下角手柄的对角固定锚点 → 右上角 `rect.topRight()`

```python
                new_w = px - mx
```
# 左下角手柄：宽度 `new_w = px - mx`，高度 `new_h = my - py` 从固定锚点向下到鼠标
```
# 下边中点手柄部分：高度 `new_h = my - py` 从固定锚点向下到鼠标
```
#   下边中点手柄的对角固定锚点 → 顶边中点

```python
                new_w = orig.width()
```
# 获取缩放前矩形的原始宽度 `orig.width()`，左/右边中点手柄缩放时保持宽度不变

```python
                new_h = my - py
```
# 下边中点手柄：高度 `new_h = my - py` 从固定锚点（顶边中点）向下到鼠标位置

```python
            case ResizeHandleType.BOTTOM_RIGHT:
```
#   右下角手柄的对角固定锚点 → 左上角 `rect.topLeft()`

```python
                new_w = mx - px
```
# 右下角手柄：宽度 `new_w = mx - px`（鼠标到固定锚点的水平距离），高度 `new_h = my - py`（鼠标到固定锚点的垂直距离）

```python
            case _:
```
# `case _` 是通配符分支：如果 `self._scale_handle` 的值不匹配以上任何已知手柄类型，说明手柄类型无效，提前退出缩放操作

```python
                return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # 最小尺寸限制
```
# 注释说明：最小尺寸限制

```python
        new_w = max(new_w, 10)
```
# 强制限制新宽度最小值为 10px，防止用户将图形缩放到不可见的大小

```python
        new_h = max(new_h, 10)
```
# 强制限制新高度最小值为 10px，防止图形被缩放到不可见的大小

```python

```
# 空行（代码结构分隔）

```python
        # 等比约束
```
# 注释说明：等比约束

```python
        if keep_ratio:
```
# 如果需要保持宽高比

```python
            orig_aspect = orig.width() / max(orig.height(), 1)
```
# 计算原始宽高比（宽÷高，分母用 max 防止除零），用于后续等比缩放约束

```python
            if self._scale_handle in (
```
# 如果存在选中的图形项

```python
                ResizeHandleType.TOP_CENTER, ResizeHandleType.BOTTOM_CENTER,
```
# 元组包含两种边中点手柄类型：上边中点（TOP_CENTER）和底边中点（BOTTOM_CENTER）——用于判断当前是否为上下方向的手柄

```python
            ):
```
# 闭合手柄类型元组，结束条件判断

```python
                new_w = new_h * orig_aspect
```
# 上下边中点手柄等比约束：宽度 = 高度 × 原始宽高比，保持等比例缩放
```
# elif 分支：当前缩放手柄为顶边中点（TOP_CENTER）或底边中点（BOTTOM_CENTER），属于上下方向的边中点手柄

```python
                ResizeHandleType.MIDDLE_LEFT, ResizeHandleType.MIDDLE_RIGHT,
```
# elif 分支：当前缩放手柄为左边中点（MIDDLE_LEFT）或右边中点（MIDDLE_RIGHT），属于左右方向的边中点手柄；拖拽时只改变宽度，高度保持原始值

```python
            ):
```
# 闭合左右边中点手柄类型元组，结束条件判断

```python
                new_h = new_w / max(orig_aspect, 0.001)
```
# 按宽度等比计算对应的高度值

```python
            else:
```
# 否则（以上条件均不满足时执行）

```python
                # 角手柄：选择较大的维度保持比例
```
# 注释说明：角手柄：选择较大的维度保持比例

```python
                aspect_w = new_h * orig_aspect
```
# 按高度等比计算对应的宽度值

```python
                aspect_h = new_w / max(orig_aspect, 0.001)
```
# 按宽度等比计算对应的高度值

```python
                if abs(new_w - aspect_w) < abs(new_h - aspect_h):
```
# 如果满足条件：abs(new_w - aspect_w) < abs(new_h - aspect_h)（满足时执行以下逻辑）

```python
                    new_h = new_w / max(orig_aspect, 0.001)
```
# 按宽度等比计算对应的高度值

```python
                else:
```
# 否则（以上条件均不满足时执行）

```python
                    new_w = new_h * orig_aspect
```
# 角手柄等比约束：以高度为主轴时，按原始宽高比计算等比宽度 `new_w = new_h × orig_aspect`

```python

```
# 空行（代码结构分隔）

```python
        # 应用缩放
```
# 注释说明：应用缩放

```python
        self._resize_item(self._dragging_item, pivot, orig, new_w, new_h)
```
# 对单个图形项执行缩放操作，根据手柄类型和鼠标位置计算新尺寸

```python

```
# 空行（代码结构分隔）

```python
    def _resize_item(self, item: GraphicItem, pivot: QPointF,
```
# 定义 `_resize_item` 方法：根据图形项类型（矩形/椭圆/路径/文字/通用）应用不同的缩放逻辑

```python
                     orig_rect: QRectF, new_w: float, new_h: float):
```
# 参数：`item` 图形项、`pivot` 固定锚点、`orig_rect` 原始矩形、`new_w` 新宽度、`new_h` 新高度

```python
        """对不同类型的图形应用尺寸变化"""
```
# 类/方法文档字符串：对不同类型的图形应用尺寸变化

```python
        scale_x = new_w / max(orig_rect.width(), 0.001)
```
计算水平缩放因子 `scale_x`：新宽度除以原始宽度（分母用 max 防止除零），大于 1 表示放大、小于 1 表示缩小，后续用于路径锚点和手柄的等比缩放变换

```python
        scale_y = new_h / max(orig_rect.height(), 0.001)
```
计算垂直缩放因子 `scale_y`：新高度除以原始高度（分母用 max 防止除零），大于 1 表示放大、小于 1 表示缩小，后续用于路径锚点和手柄的等比缩放变换

```python

```
# 空行（代码结构分隔）

```python
        if isinstance(item, RectangleItem):
```
# 如果图形项是矩形类型

```python
            # 矩形：直接修改 rect
```
# 注释说明：矩形：直接修改 rect

```python
            new_x = pivot.x() if pivot.x() < orig_rect.center().x() else pivot.x() - new_w
```
# 计算新矩形的 x 坐标：如果固定锚点在矩形中心左侧，x = pivot.x；否则 x = pivot.x - new_w（固定锚点在右边）

```python
            new_y = pivot.y() if pivot.y() < orig_rect.center().y() else pivot.y() - new_h
```
# 计算新矩形的 y 坐标：如果固定锚点在矩形中心上方，y = pivot.y；否则 y = pivot.y - new_h（固定锚点在下方）

```python
            item.rect = QRectF(new_x, new_y, new_w, new_h)
```
# 设置椭圆的 `rect` 属性

```python
        elif isinstance(item, EllipseItem):
```
# elif 分支：当前图形项为椭圆类型（EllipseItem），采用与矩形相同的定位逻辑——根据固定锚点位置计算新矩形的 x/y 坐标

```python
            # 椭圆：直接修改 rect
```
# 注释说明：椭圆：直接修改 rect

```python
            new_x = pivot.x() if pivot.x() < orig_rect.center().x() else pivot.x() - new_w
```
# 计算新矩形的 x 坐标：如果固定锚点在矩形中心左侧，x = pivot.x；否则 x = pivot.x - new_w（固定锚点在右边）

```python
            new_y = pivot.y() if pivot.y() < orig_rect.center().y() else pivot.y() - new_h
```
# 计算新矩形的 y 坐标：如果固定锚点在矩形中心上方，y = pivot.y；否则 y = pivot.y - new_h（固定锚点在下方）

```python
            item.rect = QRectF(new_x, new_y, new_w, new_h)
```
# 设置椭圆的 `rect` 属性

```python
        elif isinstance(item, PathItem):
```
# elif 分支：当前图形项为贝塞尔路径类型（PathItem），缩放路径需要按比例缩放所有锚点坐标及控制手柄位置，而非直接修改 rect

```python
            # 路径：缩放所有锚点
```
# 注释说明：路径：缩放所有锚点

```python
            ref_x = pivot.x() if scale_x > 0 else orig_rect.right()
```
# 确定路径缩放的参考点 x 坐标：正常缩放时用固定锚点的 x，反转时用矩形右边界
```
# 确定路径缩放的参考点 y 坐标：正常缩放时用固定锚点的 y，反转时用矩形底边界

```python
            for anchor in item.anchors:
```
# 遍历路径的所有锚点，检查每个锚点是否被点击命中

```python
                anchor.x = ref_x + (anchor.x - ref_x) * scale_x
```
以缩放参考点 `ref_x` 为基点对锚点 x 坐标进行等比缩放：`anchor.x - ref_x` 计算锚点相对于参考点的水平距离，乘以 `scale_x` 后加回参考点偏移，得到缩放后的新 x 坐标

```python
                anchor.y = ref_y + (anchor.y - ref_y) * scale_y
```
以缩放参考点 `ref_y` 为基点对锚点 y 坐标进行等比缩放：`anchor.y - ref_y` 计算锚点相对于参考点的垂直距离，乘以 `scale_y` 后加回参考点偏移，得到缩放后的新 y 坐标

```python
                if anchor.handle_in:
```
# 如果锚点有入方向手柄

```python
                    anchor.handle_in = QPointF(
```
根据水平缩放因子 `scale_x` 重新计算入方向手柄坐标：原手柄 x 偏移量乘以缩放比，使手柄随锚点同步缩放
```
# 获取入方向手柄的 x 坐标（贝塞尔曲线进入控制点水平位置）

```python
                        anchor.handle_in.y() * scale_y,
```
# 获取入方向手柄的 y 坐标（贝塞尔曲线进入控制点垂直位置）

```python
                    )
```
# 闭合括号：结束函数调用的参数列表

```python
                if anchor.handle_out:
```
# 如果锚点有出方向手柄

```python
                    anchor.handle_out = QPointF(
```
根据缩放比例创建新的入方向手柄 QPointF 对象：手柄 x/y 偏移量分别乘以水平/垂直缩放因子

```python
                        anchor.handle_out.x() * scale_x,
```
# 获取出方向手柄的 x 坐标（贝塞尔曲线离开控制点水平位置）

```python
                        anchor.handle_out.y() * scale_y,
```
# 获取出方向手柄的 y 坐标（贝塞尔曲线离开控制点垂直位置）

```python
                    )
```
# 闭合括号：结束函数调用的参数列表

```python
            item._rebuild_from_anchors()
```
# 根据锚点数据重新生成路径几何形状（锚点位置变化后调用）

```python
        elif isinstance(item, TextFrame):
```
# elif 分支：当前图形项为文字框类型（TextFrame），与矩形/椭圆相同采用直接修改 rect 的方式调整文字框大小

```python
            new_x = pivot.x() if pivot.x() < orig_rect.center().x() else pivot.x() - new_w
```
# 计算新矩形的 x 坐标：如果固定锚点在矩形中心左侧，x = pivot.x；否则 x = pivot.x - new_w（固定锚点在右边）

```python
            new_y = pivot.y() if pivot.y() < orig_rect.center().y() else pivot.y() - new_h
```
# 计算新矩形的 y 坐标：如果固定锚点在矩形中心上方，y = pivot.y；否则 y = pivot.y - new_h（固定锚点在下方）

```python
            item.rect = QRectF(new_x, new_y, new_w, new_h)
```
# 设置椭圆的 `rect` 属性

```python
        else:
```
# 否则（以上条件均不满足时执行）

```python
            # 通用缩放
```
# 注释说明：通用缩放

```python
            item.scale(scale_x, scale_y, pivot)
```
# 对图形项进行缩放变换，参数为缩放因子和固定参照点

```python

```
# 空行（代码结构分隔）

```python
    # ── 绘制 ──
```
# 分隔注释：绘制预览方法区域

```python

```
# 空行（代码结构分隔）

```python
    def draw_preview(self, painter: QPainter):
```
# 绘制预览方法，接收自身引用、绘图引擎：绘图引擎，无返回值

```python
        # 绘制缩放手柄
```
# 注释说明：绘制缩放手柄

```python
        if self._document:
```
# 如果工具关联了文档

```python
            for layer in self._document.layers:
```
# 遍历文档的所有图层，每次迭代将当前图层元素赋给 layer

```python
                if not layer.visible:
```
# 如果图层不可见（visible 为 False），则跳过该图层

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                    if item.selected and item.visible:
```
# 如果图形项已选中且可见

```python
                        self._draw_resize_handles(painter, item)
```
# 绘制选中图形项的8个缩放手柄（四角+四边中点），显示可缩放区域

```python

```
# 空行（代码结构分隔）

```python
        if self._is_marquee and self._drag_start and self._drag_current:
```
# 如果处于框选模式

```python
            scale = max(painter.transform().m11(), 0.001)
```
#         获取画布缩放比例

```python
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
```
# 创建画笔对象：颜色为蓝色 (0,120,215)，线宽随缩放反比（1/scale），线型为虚线（Qt.DashLine），用于绘制框选矩形

```python
            painter.setPen(pen)
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
            painter.setBrush(QColor(0, 120, 215, 30))
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
            painter.drawRect(QRectF(self._drag_start, self._drag_current))
```
# 在指定矩形区域绘制矩形（使用当前画笔描边+画刷填充）

```python

```
# 空行（代码结构分隔）

```python
    def _draw_resize_handles(self, painter: QPainter, item: GraphicItem):
```
# 定义 `_draw_resize_handles` 方法：为指定图形项绘制 8 个缩放手柄（四角 + 四边中点）

```python
        """绘制 8 个缩放手柄（世界坐标系）"""
```
# 类/方法文档字符串：绘制 8 个缩放手柄（世界坐标系）

```python
        # 将本地 bounding_rect 通过 item 的变换映射到世界坐标
```
# 注释说明：将本地 bounding_rect 通过 item 的变换映射到世界坐标

```python
        local_rect = item.bounding_rect()
```
#         获取图形项在本地坐标系下的包围矩形

```python
        rect = item._transform.mapRect(local_rect)
```
#         通过图形项的变换矩阵将本地矩形映射到世界坐标系

```python
        scale = max(painter.transform().m11(), 0.001)
```
#         获取画布缩放比例

```python
        handle_size = 7 / scale
```
# 计算手柄的显示尺寸：基础 7px 除以画布缩放比例，保证不同缩放级别下手柄视觉大小一致
```
# 计算手柄半尺寸（用于居中绘制），将手柄总尺寸除以 2

```python

```
# 空行（代码结构分隔）

```python
        pen = QPen(QColor(0, 120, 215), 1.0 / scale)
```
# 创建蓝色实线画笔：颜色 (0,120,215)，线宽 1/scale——用于绘制缩放手柄边框
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python

```
# 空行（代码结构分隔）

```python
        # 四个角
```
# 注释说明：四个角

```python
        corners = [
```
# 构建 8 个控制点中的四角手柄坐标列表 [TL, TR, BL, BR]

```python
            rect.topLeft(), rect.topRight(),
```
# 获取矩形左上角坐标点 QPointF(x, y)

```python
            rect.bottomLeft(), rect.bottomRight(),
```
# 获取矩形左下角坐标点 QPointF(x, y)

```python
        ]
```
# 列表结束

```python
        # 四条边的中点
```
# 注释说明：四条边的中点

```python
        edges = [
```
# 构建 8 个控制点中的四边中点手柄坐标列表 [TC, BC, ML, MR]

```python
            QPointF(rect.center().x(), rect.top()),
```
# 下边中点坐标：x = 矩形中心x，y = 矩形底部y

```python
            QPointF(rect.center().x(), rect.bottom()),
```
# 左边中点坐标：x = 矩形左边x，y = 矩形中心y

```python
            QPointF(rect.left(), rect.center().y()),
```
# 右边中点坐标：x = 矩形右边x，y = 矩形中心y

```python
            QPointF(rect.right(), rect.center().y()),
```
# 构造浮点精度坐标点 QPointF(x, y)，用于精确定位

```python
        ]
```
# 列表结束

```python

```
# 空行（代码结构分隔）

```python
        for pt in corners + edges:
```
# 遍历缩放矩形的8个控制点（四角+四边中点），检测鼠标悬停位置

```python
            painter.drawRect(QRectF(
```
# 绘制缩放手柄控制点方框：以控制点坐标为中心、手柄大小为边长绘制小正方形

```python
                pt.x() - half_hs, pt.y() - half_hs,
```
# QRectF 左上角 x 坐标：控制点 x - 半手柄尺寸；左上角 y 坐标：控制点 y - 半手柄尺寸

```python
                handle_size, handle_size,
```
# QRectF 宽度和高度：均为手柄尺寸（正方形手柄）

```python
            ))
```
# 多重括号闭合

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
# ── 直接选择工具 ──────────────────────────────────────────
```
# 分隔注释：直接选择工具 —— 用于视觉分组

```python

```
# 空行（代码结构分隔）

```python
class DirectSelectTool(BaseTool):
```
# 定义 `DirectSelectTool` 直接选择工具类（白箭头）：继承 `BaseTool`，实现路径锚点/手柄编辑、线段点击选中、整项拖拽

```python
    """直接选择工具（A）—— 对照 Adobe Illustrator 1:1 复原
```
#     类文档字符串：直接选择工具，对照 Adobe Illustrator 1:1 复原

```python

```
# 空行（代码结构分隔）

```python
    AI 中的 Direct Selection Tool (白箭头) 行为：
```
# 对照 Adobe Illustrator 直接选择工具的行为规范：锚点选择与拖拽交互逻辑

```python
    1. 点击已选中路径的锚点/手柄 → 选中并进入拖拽
```
# 直接选择工具行为规范第 1 条：点击已选中路径的锚点/手柄，选中该锚点并进入拖拽编辑模式

```python
    2. 点击已选中路径的线段 → 选中该路径（显示所有锚点），不添加锚点
```
# 行为规范第 2 条：点击已选中路径的线段（非锚点/手柄位置），选中整个路径显示所有锚点，不添加新锚点

```python
    3. 按住 Alt/Option 拖拽手柄 → 断开手柄对称约束（转为角点）
```
# 行为规范第 3 条：按住 Alt/Option 键拖拽锚点手柄时，断开双向手柄的对称约束，使该锚点转为独立角点

```python
    4. 拖拽平滑点的手柄 → 自动对称约束
```
# 行为规范第 4 条：拖拽平滑点的手柄时，入方向和出方向手柄自动保持对称约束（长度相等、方向相反）

```python
    5. 未选中路径 → 点击选中（显示锚点），可拖拽整项
```
# 行为规范第 5 条：点击未选中路径的任意位置，选中该路径并显示所有锚点，可拖拽整项移动

```python
    6. 按住 Shift → 多选
```
# 行为规范第 6 条：按住 Shift 键点击可追加选中多个路径或锚点（切换选中/取消选中）

```python
    7. 框选 → 选中范围内的图形项
```
# 行为规范第 7 条：在空白区域拖拽绘制框选矩形，选中矩形范围内的所有图形项

```python
    """
```
# 三引号字符串结束 —— 模块文档字符串至此闭合

```python
    __slots__ = (
```
# 声明实例属性槽位：限定该类只能拥有元组中列出的属性，禁止动态添加新属性

```python
        '_drag_start', '_drag_current',
```
# __slots__ 续行：'_drag_start' 拖拽起始坐标（鼠标按下时记录）、'_drag_current' 拖拽当前坐标（实时跟踪鼠标位置）

```python
        '_dragging_anchor_idx', '_dragging_handle_idx',
```
# __slots__ 续行：'_dragging_anchor_idx' 正在拖拽的锚点索引（≥0 表示有活跃拖拽）、'_dragging_handle_idx' 正在拖拽的贝塞尔手柄索引

```python
        '_dragging_handle_type', '_dragging_item',
```
# __slots__ 续行：'_dragging_handle_type' 拖拽手柄方向类型（'in' 入方向 / 'out' 出方向）、'_dragging_item' 当前拖拽的目标图形项

```python
        '_drag_offset', '_selected_anchor_idx',
```
# __slots__ 续行：'_drag_offset' 鼠标按下位置与图形项左上角的坐标差值、'_selected_anchor_idx' 当前选中（高亮）的锚点索引（-1 表示无选中）

```python
        '_is_marquee', '_old_anchors',
```
# __slots__ 续行：'_is_marquee' 是否处于框选模式（空白区域拖拽时为 True）、'_old_anchors' 操作前的锚点快照列表（用于撤销对比）

```python
        '_has_moved',
```
# __slots__ 续行：'_has_moved' 鼠标按下后是否已发生有效拖拽移动（距离超过阈值 DRAG_THRESHOLD）

```python
        '_press_alt',           # 按下时 Alt 是否已激活（用于断手柄）
```
# __slots__ 续行：'_press_alt' 记录鼠标按下瞬间 Alt 键是否已激活（用于判断是否断开手柄对称约束）

```python
        '_original_anchor_type', # 记录拖拽前锚点类型
```
# __slots__ 续行：'_original_anchor_type' 记录拖拽操作前锚点的原始类型（角点/平滑点），用于 Alt+拖拽后类型恢复

```python
    )
```
# 闭合括号：结束函数调用的参数列表

```python

```
# 空行（代码结构分隔）

```python
    # 基础容差（100%缩放下的像素值，与 AI 一致）
```
# 注释说明：基础容差（100%缩放下的像素值，与 AI 一致）

```python
    ANCHOR_TOLERANCE = 5.0       # 锚点点击容差
```
# 定义锚点点击命中容差为 5px，鼠标与锚点距离在此范围内即视为命中

```python
    HANDLE_TOLERANCE = 4.0       # 手柄点击容差  
```
# 定义贝塞尔手柄点击命中容差为 4px（手柄较小，容差比锚点更紧凑）

```python
    SEGMENT_TOLERANCE = 4.0      # 路径段点击容差
```
# 定义路径段点击命中容差为 4px，鼠标与路径曲线距离在此范围内即视为命中该段

```python
    DRAG_THRESHOLD = 3.0         # 最小拖拽阈值（像素）
```
# 定义最小拖拽阈值为 3px，鼠标移动距离小于此值视为点击而非拖拽

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self):
```
# 初始化方法（构造函数），接收自身引用，无返回值

```python
        super().__init__(ToolType.DIRECT_SELECT)
```
#         调用父类构造函数，传入直接选择工具类型

```python
        self._drag_start: QPointF | None = None
```
#         初始化拖拽起始坐标为 None

```python
        self._drag_current: QPointF | None = None
```
#         初始化拖拽当前坐标为 None

```python
        self._dragging_anchor_idx: int = -1
```
# 初始化拖拽锚点索引为 -1（无效值），表示当前未选中任何锚点进行拖拽

```python
        self._dragging_handle_idx: int = -1
```
# 初始化拖拽手柄索引为 -1（无效值），表示当前未选中任何手柄进行拖拽

```python
        self._dragging_handle_type: str = ''
```
# 初始化拖拽手柄类型为空字符串，`'in'` 表示入方向手柄、`'out'` 表示出方向手柄

```python
        self._dragging_item: GraphicItem | None = None
```
# 初始化单选拖拽目标图形项为 None，表示当前无活跃的拖拽目标

```python
        self._drag_offset = QPointF(0, 0)
```
# 初始化拖拽偏移量为原点 (0,0)，记录鼠标按下位置与图形项左上角的坐标差值

```python
        self._selected_anchor_idx: int = -1
```
# 初始化选中锚点索引为 -1（无效值），表示当前没有选中的锚点

```python
        self._is_marquee: bool = False
```
#         初始化框选模式标志为 False

```python
        self._old_anchors: list[AnchorPoint] = []
```
# 初始化旧锚点快照列表为空，用于拖拽开始时保存锚点原始状态（生成撤销命令时使用）

```python
        self._has_moved: bool = False
```
# 初始化移动标志为 False，标记鼠标按下后尚未发生有效拖拽移动

```python
        self._press_alt: bool = False
```
# 初始化 Alt 键标志为 False，记录鼠标按下时是否按住 Alt（用于断开手柄对称约束）

```python
        self._original_anchor_type: AnchorPointType | None = None
```
# 初始化原始锚点类型为 None，用于记录拖拽前锚点是平滑点还是角点（Alt 拖拽后恢复用）

```python

```
# 空行（代码结构分隔）

```python
    # ── 辅助方法 ──
```
# 分隔注释：辅助方法区域

```python

```
# 空行（代码结构分隔）

```python
    @staticmethod
```
# staticmethod 装饰器

```python
    def _safe_inverted(transform):
```
# 定义 `_safe_inverted` 静态方法：安全获取变换矩阵的逆矩阵，返回 (逆矩阵, 是否成功) 元组

```python
        """安全获取逆变换矩阵，返回 (inverted_transform, success)"""
```
# 类/方法文档字符串：安全获取逆变换矩阵，返回 (inverted_transform, success)

```python
        try:
```
# 尝试执行（异常处理）

```python
            inv, ok = transform.inverted()
```
# 尝试调用变换矩阵的 `inverted()` 方法获取逆矩阵：`inv` 逆矩阵、`ok` 是否成功

```python
            return (inv, ok)
```
# 返回 (inv, ok)

```python
        except Exception:
```
# 捕获异常：Exception

```python
            return (transform, False)
```
# 返回 (transform, False)

```python

```
# 空行（代码结构分隔）

```python
    def _find_path_at(self, pos: QPointF, must_be_selected: bool = False) -> tuple[PathItem | None, QPointF | None]:
```
# 定义 `_find_path_at` 方法：在文档中查找鼠标位置下的 PathItem，参数 `must_be_selected` 限制只搜索已选中路径

```python
        """从文档中查找点击位置的 PathItem，返回 (item, local_pos)"""
```
# 类/方法文档字符串：从文档中查找点击位置的 PathItem，返回 (item, local_pos)

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return (None, None)
```
# 返回 (None, None)

```python
        for layer in reversed(self._document.layers):
```
# 倒序遍历文档的所有图层（从顶层到底层，模拟 AI 的 hit-test 顺序）

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                if not isinstance(item, PathItem) or not item.anchors:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                if must_be_selected and not item.selected:
```
#                 如果要求必须已选中，跳过未选中项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                inv, ok = self._safe_inverted(item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵（用于世界坐标→局部坐标转换）

```python
                if not ok:
```
# 如果逆矩阵获取失败（`ok` 为 False），说明图形项的变换矩阵不可逆（例如缩放为 0），跳过该图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                # 用 bounding_rect 快速判断（放宽一点）
```
# 注释说明：用 bounding_rect 快速判断（放宽一点）

```python
                br = item.bounding_rect()
```
#                 获取路径的包围矩形

```python
                if not br.contains(local_pos):
```
#                 如果本地坐标不在包围矩形内，跳过

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                return (item, local_pos)
```
# 返回 (item, local_pos)

```python
        return (None, None)
```
# 返回 (None, None)

```python

```
# 空行（代码结构分隔）

```python
    # ── 鼠标事件 ──
```
# 分隔注释：鼠标事件处理方法区域

```python

```
# 空行（代码结构分隔）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# 鼠标按下事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        self._drag_start = QPointF(pos)
```
#         记录拖拽起始坐标

```python
        self._drag_current = QPointF(pos)
```
#         记录拖拽当前坐标（初始与起始相同）

```python
        self._has_moved = False
```
# 重置移动标志

```python
        self._press_alt = bool(modifiers & Qt.AltModifier)
```
#         记录鼠标按下时 Alt 键是否被按住

```python
        self._original_anchor_type = None
```
# 重置原始锚点类型

```python

```
# 空行（代码结构分隔）

```python
        shift = bool(modifiers & Qt.ShiftModifier)
```
#         检测 Shift 键是否被按住

```python

```
# 空行（代码结构分隔）

```python
        # ── 1. 优先检测已选中路径的手柄 ──
```
#         第一步：优先检测已选中路径的贝塞尔手柄

```python
        for layer in reversed(self._document.layers):
```
# 倒序遍历文档的所有图层（从顶层到底层，模拟 AI 的 hit-test 顺序）

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                inv, ok = self._safe_inverted(item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵（用于世界坐标→局部坐标转换）

```python
                if not ok:
```
# 如果逆矩阵获取失败（ok 为 False），说明变换矩阵不可逆（如缩放为 0），跳过该图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                idx, htype = item.get_handle_at(
```
# 调用路径项的 `get_handle_at` 方法，检测鼠标局部坐标是否命中某个锚点/手柄，返回 (锚点索引, 手柄类型) 元组

```python
                    local_pos.x(), local_pos.y(),
```
# 获取本地坐标系中的 x 坐标分量

```python
                    tolerance=self.HANDLE_TOLERANCE,
```
# 使用手柄容差 4.0px 进行命中检测

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                if idx >= 0:
```
# 如果命中了锚点/手柄

```python
                    self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python
                    self._dragging_handle_idx = idx
```
#                     记录拖拽的手柄索引

```python
                    self._dragging_handle_type = htype
```
#                     记录手柄类型（入/出方向）

```python
                    self._selected_anchor_idx = idx
```
# 记录当前选中的锚点索引

```python
                    self._old_anchors = [a.copy() for a in item.anchors]
```
# 深拷贝当前所有锚点保存为旧状态（用于生成 ModifyAnchorCommand 撤销命令）

```python
                    # 记录原始锚点类型（Alt 拖拽时断开约束）
```
# 注释说明：记录原始锚点类型（Alt 拖拽时断开约束）

```python
                    self._original_anchor_type = item.anchors[idx].anchor_type
```
# 记录拖拽前该锚点的类型（SMOOTH 或 CORNER）

```python
                    # 如果按 Alt，将锚点转为角点（断开对称约束）
```
# 注释说明：如果按 Alt，将锚点转为角点（断开对称约束）

```python
                    if self._press_alt:
```
#                     如果按下 Alt 键

```python
                        item.anchors[idx].convert_to_corner()
```
# 将指定索引的锚点转换为角点类型（移除贝塞尔手柄，形成折线转角）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── 2. 检测已选中路径的锚点 ──
```
#         第二步：检测已选中路径的锚点

```python
        for layer in reversed(self._document.layers):
```
# 倒序遍历文档的所有图层（从顶层到底层，模拟 AI 的 hit-test 顺序）

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                inv, ok = self._safe_inverted(item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵（用于世界坐标→局部坐标转换）

```python
                if not ok:
```
# 如果逆矩阵获取失败（ok 为 False），说明变换矩阵不可逆（如缩放为 0），跳过该图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                idx = item.get_anchor_at(
```
#                     检测本地坐标处是否有锚点

```python
                    local_pos.x(), local_pos.y(),
```
# 获取本地坐标系中的 x 坐标分量

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
# 使用锚点容差 5.0px 进行命中检测

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                if idx >= 0:
```
# 如果命中了锚点/手柄

```python
                    self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python
                    self._dragging_anchor_idx = idx
```
# 记录被拖拽的锚点索引

```python
                    self._selected_anchor_idx = idx
```
# 记录当前选中的锚点索引

```python
                    self._old_anchors = [a.copy() for a in item.anchors]
```
# 深拷贝当前所有锚点保存为旧状态（用于生成 ModifyAnchorCommand 撤销命令）

```python
                    self._original_anchor_type = item.anchors[idx].anchor_type
```
# 记录拖拽前该锚点的类型（SMOOTH 或 CORNER）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── 3. 检测已选中路径的线段（AI：点击线段选中路径但不添加锚点）──
```
#         第三步：检测已选中路径的线段

```python
        for layer in reversed(self._document.layers):
```
# 倒序遍历文档的所有图层（从顶层到底层，模拟 AI 的 hit-test 顺序）

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                inv, ok = self._safe_inverted(item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵（用于世界坐标→局部坐标转换）

```python
                if not ok:
```
# 如果逆矩阵获取失败（ok 为 False），说明变换矩阵不可逆（如缩放为 0），跳过该图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                seg = item.get_segment_at(
```
#                     检测本地坐标处是否有路径段

```python
                    local_pos.x(), local_pos.y(),
```
# 获取本地坐标系中的 x 坐标分量

```python
                    tolerance=self.SEGMENT_TOLERANCE,
```
# 使用路径段容差 4.0px 进行命中检测

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                if seg >= 0:
```
# 如果命中了路径段

```python
                    # AI 行为：点击已选中路径的线段，选中该路径用于整体拖拽
```
# 注释说明：AI 行为：点击已选中路径的线段，选中该路径用于整体拖拽

```python
                    self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python
                    self._selected_anchor_idx = -1  # 不选中特定锚点
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── 4. 检测未选中路径 → 选中它并准备整体拖拽 ──
```
#         第四步：检测未选中的路径并选中

```python
        # AI 行为：用 Direct Select 工具点击未选中路径的任意位置 → 选中路径显示锚点
```
# 注释说明：AI 行为：用 Direct Select 工具点击未选中路径的任意位置 → 选中路径显示锚点

```python
        for layer in reversed(self._document.layers):
```
# 倒序遍历文档的所有图层（从顶层到底层，模拟 AI 的 hit-test 顺序）

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                if not isinstance(item, PathItem) or item.selected or not item.anchors:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                inv, ok = self._safe_inverted(item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵（用于世界坐标→局部坐标转换）

```python
                if not ok:
```
# 如果逆矩阵获取失败（ok 为 False），说明变换矩阵不可逆（如缩放为 0），跳过该图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python

```
# 空行（代码结构分隔）

```python
                # 先检查是否在路径段附近
```
# 注释说明：先检查是否在路径段附近

```python
                seg = item.get_segment_at(
```
#                     检测本地坐标处是否有路径段

```python
                    local_pos.x(), local_pos.y(),
```
# 获取本地坐标系中的 x 坐标分量

```python
                    tolerance=self.SEGMENT_TOLERANCE,
```
# 使用路径段容差 4.0px 进行命中检测

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                if seg >= 0:
```
# 如果命中了路径段

```python
                    if not shift:
```
#                     如果未按 Shift（不追加选择）

```python
                        self._document.clear_selection()
```
#                     清除文档中所有图形项的选中状态

```python
                    item.selected = True
```
# 将当前图形项设为选中状态

```python
                    self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python
                    self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
                # 再检查是否在锚点附近
```
# 注释说明：再检查是否在锚点附近

```python
                idx = item.get_anchor_at(
```
#                     检测本地坐标处是否有锚点

```python
                    local_pos.x(), local_pos.y(),
```
# 获取本地坐标系中的 x 坐标分量

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
# 使用锚点容差 5.0px 进行命中检测

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                if idx >= 0:
```
# 如果命中了锚点/手柄

```python
                    if not shift:
```
#                     如果未按 Shift（不追加选择）

```python
                        self._document.clear_selection()
```
#                     清除文档中所有图形项的选中状态

```python
                    item.selected = True
```
# 将当前图形项设为选中状态

```python
                    self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python
                    self._dragging_anchor_idx = idx
```
# 记录被拖拽的锚点索引

```python
                    self._selected_anchor_idx = idx
```
# 记录当前选中的锚点索引

```python
                    self._old_anchors = [a.copy() for a in item.anchors]
```
# 深拷贝当前所有锚点保存为旧状态（用于生成 ModifyAnchorCommand 撤销命令）

```python
                    self._original_anchor_type = item.anchors[idx].anchor_type
```
# 记录拖拽前该锚点的类型（SMOOTH 或 CORNER）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
                # 最后检查填充区域
```
# 注释说明：最后检查填充区域

```python
                if item.contains_point(local_pos):
```
#                     检测本地坐标是否在路径填充区域

```python
                    if not shift:
```
#                     如果未按 Shift（不追加选择）

```python
                        self._document.clear_selection()
```
#                     清除文档中所有图形项的选中状态

```python
                    item.selected = True
```
# 将当前图形项设为选中状态

```python
                    self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python
                    self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── 5. 检测普通图形项 ──
```
#         第五步：检测非路径类型的普通图形项

```python
        item = self._document.get_item_at(pos.x(), pos.y())
```
# 通过文档查找鼠标位置下的最顶层图形项

```python
        if item:
```
#         如果鼠标下方有图形项

```python
            if not shift:
```
#                     如果未按 Shift（不追加选择）

```python
                self._document.clear_selection()
```
#                     清除文档中所有图形项的选中状态

```python
            item.selected = True
```
# 将当前图形项设为选中状态

```python
            self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python
            self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── 6. 框选 ──
```
#         第六步：以上都未命中，进入框选模式

```python
        if not shift:
```
#                     如果未按 Shift（不追加选择）

```python
            self._document.clear_selection()
```
#                     清除文档中所有图形项的选中状态

```python
        self._is_marquee = True
```
#             进入框选模式

```python

```
# 空行（代码结构分隔）

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# 鼠标移动事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if self._drag_start is None:
```
#         如果没有拖拽起始点，不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        self._drag_current = QPointF(pos)
```
#         记录拖拽当前坐标（初始与起始相同）

```python

```
# 空行（代码结构分隔）

```python
        dx_total = pos.x() - self._drag_start.x()
```
#         计算从起始点到当前点的总水平偏移

```python
        dy_total = pos.y() - self._drag_start.y()
```
#         计算从起始点到当前点的总垂直偏移

```python
        dist = math.sqrt(dx_total * dx_total + dy_total * dy_total)
```
#         计算欧几里得距离（拖拽总距离）

```python
        alt_held = bool(modifiers & Qt.AltModifier)
```
#         检测 Alt 键是否持续按住

```python

```
# 空行（代码结构分隔）

```python
        # ── 手柄拖拽 ──
```
#         以下为贝塞尔手柄拖拽处理分支

```python
        if self._dragging_handle_idx >= 0 and self._dragging_item:
```
#         如果正在拖拽手柄且有目标图形项

```python
            if isinstance(self._dragging_item, PathItem):
```
# 类型检查：确认拖拽目标 `self._dragging_item` 是 PathItem（贝塞尔路径）类型，只有路径才能进行锚点移动操作

```python
                inv, ok = self._safe_inverted(self._dragging_item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵（用于世界坐标→局部坐标转换）

```python
                if not ok:
```
# 如果逆矩阵获取失败（`ok` 为 False），说明图形项的变换矩阵不可逆，无法继续处理锚点拖拽

```python
                    return
```
#         提前返回，不执行后续逻辑

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                anchor = self._dragging_item.anchors[self._dragging_handle_idx]
```
#                 获取被拖拽手柄所属的锚点

```python
                rel_x = local_pos.x() - anchor.x
```
#                 计算手柄相对锚点的水平偏移

```python
                rel_y = local_pos.y() - anchor.y
```
#                 计算手柄相对锚点的垂直偏移

```python

```
# 空行（代码结构分隔）

```python
                # 平滑点约束：不按 Alt 时自动对称
```
# 注释说明：平滑点约束：不按 Alt 时自动对称

```python
                constrain = (anchor.anchor_type == AnchorPointType.SMOOTH and not alt_held)
```
# 判断是否需要施加对称约束：锚点类型为平滑点（SMOOTH）且未按住 Alt 键时 constrain=True，否则 False

```python

```
# 空行（代码结构分隔）

```python
                if self._dragging_handle_type == 'in':
```
# 如果存在选中的图形项

```python
                    self._dragging_item.set_handle_in(
```
# 设置锚点的入方向手柄位置（贝塞尔曲线的进入控制点）

```python
                        self._dragging_handle_idx, rel_x, rel_y,
```
# set_handle_in 参数续行：self._dragging_handle_idx 手柄所属锚点索引、rel_x/rel_y 手柄相对于锚点的偏移坐标

```python
                        constrain_smooth=constrain,
```
# 传入 constrain 参数：是否对平滑点施加对称约束（True 时入/出手柄自动保持方向相反、长度相等）

```python
                    )
```
# 闭合括号：结束函数调用的参数列表

```python
                else:
```
# 否则（以上条件均不满足时执行）

```python
                    self._dragging_item.set_handle_out(
```
# 设置锚点的出方向手柄位置（贝塞尔曲线的离开控制点）

```python
                        self._dragging_handle_idx, rel_x, rel_y,
```
# set_handle_out 参数续行：self._dragging_handle_idx 手柄所属锚点索引、rel_x/rel_y 手柄相对于锚点的偏移坐标

```python
                        constrain_smooth=constrain,
```
# 传入 constrain 参数：是否对平滑点施加对称约束（True 时入/出手柄自动保持方向相反、长度相等）

```python
                    )
```
# 闭合括号：结束 set_handle_out 函数调用
```
# 如果工具关联了文档

```python
                    self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行（代码结构分隔）

```python
        # ── 锚点拖拽（超过阈值后移动）──
```
#         以下为锚点拖拽处理分支

```python
        elif self._dragging_anchor_idx >= 0 and self._dragging_item:
```
# elif 分支：`self._dragging_anchor_idx >= 0` 表示当前正在拖拽某个锚点（索引≥0），`self._dragging_item` 确认存在有效的拖拽目标图形项；此分支处理锚点拖拽移动逻辑
# 是平滑锚点 并且 没有按住Alt键

```python
            if not self._has_moved:
```
#             如果尚未确认开始有效拖拽

```python
                if dist < self.DRAG_THRESHOLD:
```
#                 如果距离未超过阈值

```python
                    return
```
#         提前返回，不执行后续逻辑

```python
                self._has_moved = True
```
# 标记已发生实际移动

```python

```
# 空行（代码结构分隔）

```python
            if isinstance(self._dragging_item, PathItem):
```
# 类型检查确认：拖拽目标是 PathItem，继续执行手柄调整逻辑

```python
                inv, ok = self._safe_inverted(self._dragging_item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵（用于世界坐标→局部坐标转换）

```python
                if not ok:
```
# 如果逆矩阵获取失败（ok 为 False），说明变换矩阵不可逆（如缩放为 0），跳过该图形项

```python
                    return
```
#         提前返回，不执行后续逻辑

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                self._dragging_item.move_anchor(
```
# 将指定索引的锚点移动到新位置 (x, y)，同时更新路径形状

```python
                    self._dragging_anchor_idx, local_pos.x(), local_pos.y(),
```
# 将锚点移动到新位置：(当前锚点x+增量, 当前锚点y+增量)，增量来自鼠标位移

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                if self._document:
```
# 如果工具关联了文档

```python
                    self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行（代码结构分隔）

```python
        # ── 整项拖拽（非锚点/手柄拖拽模式）──
```
#         以下为整项拖拽处理分支

```python
        elif self._dragging_item and not self._is_marquee:
```
# elif 分支：`self._dragging_item` 表示存在拖拽目标图形项，`not self._is_marquee` 表示当前不是框选模式；此分支处理整项拖拽（点击路径内部后拖动整个图形项）

```python
            if not self._has_moved:
```
#             如果尚未确认开始有效拖拽

```python
                if dist < self.DRAG_THRESHOLD:
```
#                 如果距离未超过阈值

```python
                    return
```
#         提前返回，不执行后续逻辑

```python
                self._has_moved = True
```
# 标记已发生实际移动

```python

```
# 空行（代码结构分隔）

```python
            dx = pos.x() - self._drag_start.x()
```
#         计算水平方向增量

```python
            dy = pos.y() - self._drag_start.y()
```
#         计算垂直方向增量

```python
            if modifiers & Qt.ShiftModifier:
```
#         如果按住 Shift，约束为纯水平或垂直移动

```python
                dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)
```
# 三元表达式：若水平偏移大于垂直偏移则约束为纯水平移动，否则约束为纯垂直移动（Shift约束）

```python
            self._dragging_item.move_by(dx, dy)
```
# 将拖拽目标图形项按增量 (dx, dy) 平移移动

```python
            self._drag_start = QPointF(pos)
```
#         记录拖拽起始坐标

```python
            if self._document:
```
# 如果工具关联了文档

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行（代码结构分隔）

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# 鼠标释放事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        # ── 如果拖拽了手柄且按了 Alt，需要恢复锚点类型为角点 ──
```
#         以下处理 Alt+手柄拖拽后的锚点类型恢复

```python
        if self._dragging_handle_idx >= 0 and self._dragging_item:
```
#         如果正在拖拽手柄且有目标图形项

```python
            if isinstance(self._dragging_item, PathItem):
```
# 类型检查：确认拖拽目标是 PathItem，只有路径项才有锚点类型恢复逻辑

```python
                if self._press_alt or self._has_moved:
```
# 如果已发生有效拖拽移动

```python
                    # Alt+拖拽：断开对称约束，转为角点
```
# 注释说明：Alt+拖拽：断开对称约束，转为角点

```python
                    anchor = self._dragging_item.anchors[self._dragging_handle_idx]
```
#                 获取被拖拽手柄所属的锚点

```python
                    if self._press_alt:
```
#                     如果按下 Alt 键

```python
                        anchor.anchor_type = AnchorPointType.CORNER
```
#                     将锚点类型强制设为角点

```python
                    self._dragging_item._build_path()
```
# 根据当前锚点数据重新构建 QPainterPath 绘制路径

```python

```
# 空行（代码结构分隔）

```python
        # ── 记录撤销命令（通过 execute_command 统一入口）──
```
#         以下为撤销命令记录逻辑

```python
        if self._old_anchors and self._dragging_item and self._document:
```
# 如果有锚点快照、拖拽目标和文档

```python
            if isinstance(self._dragging_item, PathItem):
```
# 类型检查：确认拖拽目标是 PathItem，只有路径项才需要对比锚点变化生成 ModifyAnchorCommand

```python
                new_anchors = [a.copy() for a in self._dragging_item.anchors]
```
#             创建当前所有锚点的副本

```python
                if self._has_moved and len(self._old_anchors) == len(new_anchors):
```
#             如果确实发生了移动且锚点数量一致

```python
                    # 检查是否真的有变化
```
# 注释说明：检查是否真的有变化

```python
                    changed = False
```
# 初始化局部变量 changed 为 False

```python
                    for old, new in zip(self._old_anchors, new_anchors):
```
# 并行遍历旧锚点列表和新锚点列表，逐一对比创建修改命令

```python
                        if (old.x != new.x or old.y != new.y or
```
# 逐项对比新旧锚点属性是否发生变化：`old.x != new.x` x 坐标不同，`old.y != new.y` y 坐标不同——任一成立说明锚点位置有变化

```python
                            old.handle_in != new.handle_in or
```
# 继续对比：`old.handle_in != new.handle_in` 入方向控制手柄位置是否发生变化

```python
                            old.handle_out != new.handle_out or
```
# 继续对比：`old.handle_out != new.handle_out` 出方向控制手柄位置是否发生变化

```python
                            old.anchor_type != new.anchor_type):
```
# 继续对比：`old.anchor_type != new.anchor_type` 锚点类型（角点/平滑点）是否发生变化

```python
                            changed = True
```
# 初始化局部变量 changed 为 True

```python
                            break
```
# 跳出当前循环

```python
                    if changed:
```
#                 如果确实存在变化

```python
                        cmd = ModifyAnchorCommand(
```
#                     创建修改锚点撤销命令，记录操作前后的锚点状态快照

```python
                            self._document, self._dragging_item,
```
# ModifyAnchorCommand 参数：self._document 文档对象（命令上下文）、self._dragging_item 被修改锚点的图形项

```python
                            self._old_anchors, new_anchors,
```
# ModifyAnchorCommand 参数：self._old_anchors 操作前的锚点快照列表（旧值）、new_anchors 操作后的锚点副本列表（新值）

```python
                        )
```
# 闭合括号：结束 ModifyAnchorCommand 构造函数调用

```python
                        self._document.execute_command(cmd)
```
# 通过文档统一入口执行命令对象（自动推入撤销栈，支持 Ctrl+Z 撤销）

```python

```
# 空行（代码结构分隔）

```python
        # ── 框选 ──
```
#         框选完成处理

```python
        if self._is_marquee and self._drag_start and self._document:
```
# 如果处于框选模式

```python
            rect = QRectF(self._drag_start, pos).normalized()
```
#             构建规范化框选矩形

```python
            if rect.width() > 2 and rect.height() > 2:
```
# 如果矩形尺寸足够大（过滤意外点击）

```python
                for layer in self._document.layers:
```
# 遍历文档的所有图层，每次迭代将当前图层元素赋给 layer

```python
                    items = layer.get_items_in_rect(
```
# 调用图层的 get_items_in_rect 方法，查询框选矩形范围内的所有图形项，保存到 items

```python
                        rect.x(), rect.y(), rect.width(), rect.height(),
```
# 获取矩形左上角的 x 坐标（世界坐标系中的水平位置）

```python
                    )
```
# 闭合括号：结束函数调用的参数列表

```python
                    for item in items:
```
# 遍历框选命中的图形项列表，将每个项标记为选中状态

```python
                        item.selected = True
```
# 将当前图形项设为选中状态

```python

```
# 空行（代码结构分隔）

```python
        # ── 重置状态 ──
```
#         重置直接选择工具的所有交互状态

```python
        self._drag_start = None
```
# 清空拖拽起始点

```python
        self._drag_current = None
```
#         清空拖拽当前坐标

```python
        self._dragging_anchor_idx = -1
```
# 重置拖拽锚点索引

```python
        self._dragging_handle_idx = -1
```
# 重置拖拽手柄索引

```python
        self._dragging_handle_type = ''
```
# 重置拖拽手柄类型为空字符串

```python
        self._dragging_item = None
```
#         清空拖拽目标

```python
        self._is_marquee = False
```
#         退出框选模式

```python
        self._old_anchors = []
```
# 清空旧锚点列表

```python
        self._has_moved = False
```
# 重置移动标志

```python
        self._press_alt = False
```
# 重置 Alt 键标志

```python
        self._original_anchor_type = None
```
# 重置原始锚点类型

```python

```
# 空行（代码结构分隔）

```python
    # ── 键盘 ──
```
# 分隔注释：键盘事件处理区域

```python

```
# 空行（代码结构分隔）

```python
    def key_press(self, key: int, modifiers: int):
```
# 键盘按键事件处理方法，接收自身引用、按键码：整数、修饰键标志位：整数，无返回值

```python
        """键盘操作对照 AI 行为"""
```
# 类/方法文档字符串：键盘操作对照 AI 行为

```python
        # Delete/Backspace 删除选中的锚点（AI：Delete Anchor Point）
```
# 注释说明：Delete/Backspace 删除选中的锚点（AI：Delete Anchor Point）

```python
        if key in (Qt.Key_Delete, Qt.Key_Backspace):
```
#         如果按下 Delete 或 Backspace

```python
            if self._selected_anchor_idx >= 0 and self._dragging_item:
```
#             如果有选中锚点和目标图形项

```python
                if isinstance(self._dragging_item, PathItem):
```
# 类型检查：确认拖拽目标是 PathItem，只有路径才有锚点可删除

```python
                    if self._dragging_item.anchor_count > 2:
```
#                 如果路径至少有 3 个锚点（最少保留 2 个）

```python
                        old_anchors = [a.copy() for a in self._dragging_item.anchors]
```
#                     保存删除前锚点快照

```python
                        self._dragging_item.remove_anchor(self._selected_anchor_idx)
```
# 删除指定索引的锚点，路径自动连接前后相邻锚点保持连续

```python
                        if self._document:
```
# 如果工具关联了文档

```python
                            new_anchors = [a.copy() for a in self._dragging_item.anchors]
```
#             创建当前所有锚点的副本

```python
                            cmd = ModifyAnchorCommand(
```
#                     创建修改锚点撤销命令，记录删除前后的锚点状态

```python
                                self._document, self._dragging_item,
```
# ModifyAnchorCommand 参数：self._document 文档对象（命令上下文）、self._dragging_item 被修改锚点的图形项

```python
                                old_anchors, new_anchors,
```
# ModifyAnchorCommand 参数：old_anchors 删除前的锚点快照列表（旧值）、new_anchors 删除后的锚点列表（新值）

```python
                            )
```
# 闭合括号：结束函数调用的参数列表

```python
                            self._document.execute_command(cmd)
```
# 通过文档统一入口执行命令对象（自动推入撤销栈，支持 Ctrl+Z 撤销）

```python
                        self._selected_anchor_idx = max(0, min(
```
# 将选中锚点索引限制在有效范围 [0, anchor_count-1]：`min()` 不超过最大索引，`max()` 不小于 0

```python
                            self._selected_anchor_idx,
```
# min() 参数：self._selected_anchor_idx 删除后需调整的选中锚点索引（不直接删除后的新索引）、

```python
                            self._dragging_item.anchor_count - 1,
```
# min() 参数：self._dragging_item.anchor_count - 1 删除一个锚点后的最大有效索引（锚点总数减 1）

```python
                        ))
```
# 多重括号闭合

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # Plus/Equal 在选中锚点后添加新锚点（段中点）
```
# 注释说明：Plus/Equal 在选中锚点后添加新锚点（段中点）

```python
        if key in (Qt.Key_Plus, Qt.Key_Equal):
```
# 如果按下了 + 或 = 键（Qt.Key_Plus / Qt.Key_Equal），触发在选中锚点之后添加新锚点的操作

```python
            if self._selected_anchor_idx >= 0 and self._dragging_item:
```
#             如果有选中锚点和目标图形项

```python
                if isinstance(self._dragging_item, PathItem):
```
# 类型检查：确认拖拽目标是 PathItem，只有路径才能在锚点之间插入新锚点

```python
                    self._add_anchor_after_selected(self._dragging_item)
```
# 在选中锚点之后插入新锚点（用于钢笔工具继续绘制路径）

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
    def _add_anchor_after_selected(self, item: PathItem):
```
# 在选中锚点之后的段中点添加新锚点，接收自身引用、图形项：贝塞尔路径项，无返回值

```python
        """在选中锚点之后的段中点添加新锚点"""
```
# 类/方法文档字符串：在选中锚点之后的段中点添加新锚点

```python
        anchors = item.anchors
```
#         获取路径的所有锚点

```python
        i = self._selected_anchor_idx
```
#         获取选中锚点索引

```python
        if i < 0 or len(anchors) < 2:
```
# 前置检查：`i < 0` 没有选中锚点（索引无效），`len(anchors) < 2` 锚点不足 2 个无法构成路径段——任一成立则无法在段中点添加锚点

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        n = len(anchors)
```
#         获取锚点总数

```python
        j = (i + 1) % n
```
# 取下一个锚点的索引：`(i + 1) % n` 对锚点总数取模，实现循环路径的首尾连接

```python
        if not item.closed and i == n - 1:
```
#         如果路径未闭合且当前是最后锚点，不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # 在贝塞尔曲线段的中点添加锚点
```
# 注释说明：在贝塞尔曲线段的中点添加锚点

```python
        prev, curr = anchors[i], anchors[j]
```
# 提取当前锚点 `prev`（索引 i）和下一个锚点 `curr`（索引 j = (i+1) % n），构成要插入新锚点的路径段

```python

```
# 空行（代码结构分隔）

```python
        # 使用贝塞尔采样获取真正的中点
```
# 注释说明：使用贝塞尔采样获取真正的中点

```python
        samples = PathItem._sample_bezier_segment(prev, curr, num_samples=4)
```
#                 对该段进行 4 次贝塞尔采样

```python
        if len(samples) >= 2:
```
# 如果贝塞尔采样成功获得至少 2 个采样点，则可以从中取中点坐标

```python
            # 取中点
```
# 注释说明：取中点

```python
            mid_idx = len(samples) // 2
```
# 取采样点的中间索引（总采样数÷2 向下取整），获取贝塞尔曲线段的几何中点坐标
```
# 从贝塞尔采样点列表中取出中间点的坐标 (mx, my) 作为新锚点的位置
```
# 否则（以上条件均不满足时执行）

```python
            mx = (prev.x + curr.x) / 2
```
# 计算前后两个锚点的 x 坐标平均值，作为新锚点的 x 坐标（中点位置）

```python
            my = (prev.y + curr.y) / 2
```
# 计算前后两个锚点的 y 坐标平均值，作为新锚点的 y 坐标（中点位置）

```python

```
# 空行（代码结构分隔）

```python
        old_anchors = [a.copy() for a in anchors]
```
# 列表推导式：对路径中的每个锚点执行 `a.copy()` 深拷贝，生成拖拽前的锚点状态快照，保存到 `old_anchors`

```python
        new_anchor = AnchorPoint(mx, my)
```
#             创建新锚点（默认角点）

```python
        item.insert_anchor(i + 1, new_anchor)
```
# 在路径的指定位置插入新锚点（用于钢笔工具和添加锚点工具）

```python
        self._selected_anchor_idx = i + 1
```
# 将新插入锚点的索引 `i + 1` 设为当前选中锚点索引，并将该路径设为拖拽目标
```
#                 设置当前图形项为单项拖拽目标

```python

```
# 空行（代码结构分隔）

```python
        if self._document:
```
# 如果工具关联了文档

```python
            new_anchors = [a.copy() for a in item.anchors]
```
# 对每个锚点执行深拷贝，生成锚点列表的副本（避免直接修改原始数据）

```python
            cmd = ModifyAnchorCommand(
```
#                     创建修改锚点撤销命令

```python
                self._document, item, old_anchors, new_anchors,
```
# ModifyAnchorCommand 参数（单行写法）：self._document 文档对象、item 目标路径项、old_anchors 插入前的锚点快照、new_anchors 插入后的锚点列表

```python
            )
```
# 闭合括号：结束 ModifyAnchorCommand 构造函数调用

```python
            self._document.execute_command(cmd)
```
# 通过文档统一入口执行命令对象（自动推入撤销栈，支持 Ctrl+Z 撤销）

```python

```
# 空行（代码结构分隔）

```python
    # ── 绘制预览 ──
```
# 分隔注释：绘制预览方法区域

```python

```
# 空行（代码结构分隔）

```python
    def draw_preview(self, painter: QPainter):
```
# 绘制预览方法，接收自身引用、绘图引擎：绘图引擎，无返回值

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        for layer in self._document.layers:
```
# 遍历文档的所有图层，每次迭代将当前图层元素赋给 layer

```python
            if not layer.visible:
```
# 如果图层不可见（visible 为 False），则跳过该图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                if isinstance(item, PathItem) and item.selected:
```
# 条件检查：`isinstance(item, PathItem)` 当前项是贝塞尔路径，`item.selected` 该路径已被选中——两者同时满足才需要绘制锚点手柄

```python
                    self._draw_anchor_handles(painter, item)
```
# 绘制路径上所有锚点和贝塞尔手柄的视觉表示（方块+控制线+圆形手柄）

```python

```
# 空行（代码结构分隔）

```python
        if self._is_marquee and self._drag_start and self._drag_current:
```
# 如果处于框选模式

```python
            scale = max(painter.transform().m11(), 0.001)
```
#         获取画布缩放比例

```python
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
```
# 创建蓝色虚线画笔：颜色 (0,120,215)，线宽 1/scale（反比缩放），虚线样式——用于绘制框选矩形边框
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
            painter.drawRect(QRectF(self._drag_start, self._drag_current))
```
# 在指定矩形区域绘制矩形（使用当前画笔描边+画刷填充）

```python

```
# 空行（代码结构分隔）

```python
    def _draw_anchor_handles(self, painter: QPainter, item: PathItem):
```
# 绘制锚点和贝塞尔手柄，接收自身引用、绘图引擎：绘图引擎、图形项：贝塞尔路径项，无返回值

```python
        """绘制锚点和贝塞尔手柄，对照 AI 的视觉风格
```
# 方法文档字符串开始：描述绘制锚点和手柄的视觉规范

```python

```
# 空行（代码结构分隔）

```python
        AI 锚点渲染规则：
```
# 文档字符串中的渲染规则说明：

```python
        - 未选中锚点：白色填充方形，蓝色边框
```
# 未选中锚点样式：白色填充的方形锚点，蓝色边框线条

```python
        - 选中锚点：蓝色填充方形，深蓝边框
```
# 选中锚点样式：蓝色填充的方形锚点，深蓝色边框线条（与未选中区分）

```python
        - 手柄线：灰色虚线（handle_in）/ 实线（handle_out）
```
# 手柄连线样式：handle_in（入方向）为灰色虚线，handle_out（出方向）为灰色实线

```python
        - 手柄端点：白色填充圆形，灰色边框
```
# 手柄端点样式：白色填充的圆形控制点，灰色边框

```python
        - 平滑点 vs 角点使用相同视觉表示
```
# 视觉规则：平滑点和角点使用相同的视觉表示（不通过外观区分类型，只通过手柄有无区分）

```python
        """
```
# 三引号字符串结束 —— 模块文档字符串至此闭合

```python
        if not item.anchors:
```
# 前置检查：如果路径没有任何锚点（`not item.anchors`），则无需绘制锚点手柄，提前返回

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        scale = max(painter.transform().m11(), 0.001)
```
#         获取画布缩放比例

```python
        handle_r = 3.5 / scale        # 手柄端点半径
```
# 计算手柄端点的显示半径：3.5px 除以缩放比例，保证视觉大小一致

```python
        anchor_half = 3.5 / scale     # 锚点半边长
```
# 计算未选中锚点的半边长（绘制尺寸）：3.5px 除以缩放比例

```python
        highlight_half = 4.5 / scale  # 选中锚点半边长
```
# 计算选中（高亮）锚点的半边长（比未选中稍大 4.5px）：除以缩放比例

```python

```
# 空行（代码结构分隔）

```python
        transform = item._transform
```
#         获取图形项变换矩阵

```python
        anchor_color = QColor(0, 120, 215)       # AI 蓝
```
# 创建 AI 标准蓝色 (0,120,215) 作为锚点填充色

```python
        anchor_border = QColor(0, 80, 180)
```
# 创建深蓝色 (0,80,180) 作为锚点边框色

```python
        handle_color = QColor(120, 120, 120)     # 手柄线颜色
```
# 创建灰色 (120,120,120) 作为手柄线颜色

```python

```
# 空行（代码结构分隔）

```python
        for i, anchor in enumerate(item.anchors):
```
# 带索引遍历路径的所有锚点，用于定位当前处理的锚点序号和对象

```python
            ax_local, ay_local = anchor.x, anchor.y
```
# 提取当前锚点的局部坐标 (x, y)，保存到局部变量供坐标变换使用

```python
            ax = transform.map(QPointF(ax_local, ay_local)).x()
```
# 将锚点局部坐标 (ax_local, ay_local) 通过图形项的变换矩阵映射到世界坐标系，分别提取 x/y 分量

```python
            ay = transform.map(QPointF(ax_local, ay_local)).y()
```
# 提取世界坐标系中的 y 坐标分量

```python

```
# 空行（代码结构分隔）

```python
            # ── 绘制 handle_in 线和端点 ──
```
# 分隔注释：绘制 handle_in 线和端点 —— 用于视觉分组

```python
            if anchor.handle_in:
```
# 如果锚点有入方向手柄

```python
                hx_local = ax_local + anchor.handle_in.x()
```
将锚点的局部 x 坐标 `ax_local` 加上入方向手柄相对于锚点的 x 偏移量 `anchor.handle_in.x()`，得到手柄入点在局部坐标系中的绝对 x 坐标 `hx_local`

```python
                hy_local = ay_local + anchor.handle_in.y()
```
将锚点的局部 y 坐标 `ay_local` 加上入方向手柄相对于锚点的 y 偏移量 `anchor.handle_in.y()`，得到手柄入点在局部坐标系中的绝对 y 坐标 `hy_local`

```python
                hx_pt = transform.map(QPointF(hx_local, hy_local))
```
# 将手柄端点的局部坐标通过变换矩阵映射到世界坐标系，得到手柄在世界空间中的位置
```
# 将入方向手柄世界坐标 `hx_pt` 的 x/y 分量分别提取到 `hx`（入方向手柄世界 x）和 `hy`（入方向手柄世界 y），用于绘制手柄连线和端点

```python

```
# 空行（代码结构分隔）

```python
                # 手柄线
```
# 注释说明：手柄线

```python
                handle_pen = QPen(handle_color, 1.0 / scale, Qt.DashLine)
```
# 创建灰色实线画笔：颜色 (120,120,120)，线宽 1/scale——用于绘制 handle_out 出方向手柄连线

```python
                painter.setPen(handle_pen)
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
                painter.setBrush(Qt.NoBrush)
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
                painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))
```
# 绘制从起点到终点的线段（使用当前画笔样式）

```python

```
# 空行（代码结构分隔）

```python
                # 手柄端点（圆形）
```
# 注释说明：手柄端点（圆形）

```python
                painter.setBrush(QColor(255, 255, 255))
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
                painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
                painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)
```
# 在指定矩形内绘制内切椭圆（用于锚点和手柄端点的圆形表示）

```python

```
# 空行（代码结构分隔）

```python
            # ── 绘制 handle_out 线和端点 ──
```
# 分隔注释：绘制 handle_out 线和端点 —— 用于视觉分组

```python
            if anchor.handle_out:
```
# 如果锚点有出方向手柄

```python
                hx_local = ax_local + anchor.handle_out.x()
```
# 将锚点的局部 x 坐标 `ax_local` 加上出方向手柄相对于锚点的 x 偏移量 `anchor.handle_out.x()`，得到手柄出点在局部坐标系中的绝对 x 坐标 `hx_local`

```python
                hy_local = ay_local + anchor.handle_out.y()
```
# 将锚点的局部 y 坐标 `ay_local` 加上出方向手柄相对于锚点的 y 偏移量 `anchor.handle_out.y()`，得到手柄出点在局部坐标系中的绝对 y 坐标 `hy_local`

```python
                hx_pt = transform.map(QPointF(hx_local, hy_local))
```
# 将手柄端点的局部坐标通过图形项变换矩阵映射到世界坐标系

```python
                hx, hy = hx_pt.x(), hx_pt.y()
```
# 将出方向手柄世界坐标 `hx_pt` 的 x/y 分量分别提取到 `hx`（出方向手柄世界 x）和 `hy`（出方向手柄世界 y），用于绘制手柄连线和端点

```python

```
# 空行（代码结构分隔）

```python
                # 手柄线
```
# 注释说明：手柄线

```python
                handle_pen = QPen(handle_color, 1.0 / scale, Qt.SolidLine)
```
# 创建灰色实线画笔：颜色 (120,120,120)，线宽 1/scale——用于绘制 handle_out 出方向手柄连线

```python
                painter.setPen(handle_pen)
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
                painter.setBrush(Qt.NoBrush)
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
                painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))
```
# 绘制从起点到终点的线段（使用当前画笔样式）

```python

```
# 空行（代码结构分隔）

```python
                # 手柄端点（圆形）
```
# 注释说明：手柄端点（圆形）

```python
                painter.setBrush(QColor(255, 255, 255))
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
                painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
                painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)
```
# 在指定矩形内绘制内切椭圆（用于锚点和手柄端点的圆形表示）

```python

```
# 空行（代码结构分隔）

```python
            # ── 绘制锚点（方形）──
```
# 分隔注释：绘制锚点（方形） —— 用于视觉分组

```python
            is_highlighted = (i == self._selected_anchor_idx)
```
# 判断当前遍历到的锚点是否为高亮选中状态：当前索引 i 等于 self._selected_anchor_idx 时为 True

```python

```
# 空行（代码结构分隔）

```python
            if is_highlighted:
```
# 如果当前锚点是高亮选中状态（`is_highlighted` 为 True，即 `i == self._selected_anchor_idx`），使用蓝色填充绘制

```python
                # 选中锚点：蓝色填充
```
# 注释说明：选中锚点：蓝色填充

```python
                painter.setBrush(anchor_color)
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
                painter.setPen(QPen(anchor_border, 1.5 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
                painter.drawRect(QRectF(
```
# 绘制高亮选中锚点方框（蓝色填充）：以锚点世界坐标为中心绘制正方形

```python
                    ax - highlight_half, ay - highlight_half,
```
# QRectF 左上角 x/y：锚点世界坐标减去半尺寸；矩形宽高均为 highlight_half*2（选中时更大的锚点方块）

```python
                    highlight_half * 2, highlight_half * 2,
```
# QRectF 宽度和高度：均为 highlight_half 的两倍（选中锚点方块的边长）

```python
                ))
```
# 多重括号闭合

```python
            else:
```
# 否则（以上条件均不满足时执行）

```python
                # 未选中锚点：白色填充
```
# 注释说明：未选中锚点：白色填充

```python
                painter.setBrush(QColor(255, 255, 255))
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
                painter.setPen(QPen(anchor_color, 1.5 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
                painter.drawRect(QRectF(
```
# 绘制未选中锚点方框（白色填充）：以锚点世界坐标为中心绘制较小的正方形

```python
                    ax - anchor_half, ay - anchor_half,
```
# QRectF 左上角 x/y：锚点世界坐标减去半尺寸；矩形宽高均为 anchor_half*2（未选中时较小的锚点方块）

```python
                    anchor_half * 2, anchor_half * 2,
```
# QRectF 宽高：锚点方块的边长（anchor_half 的两倍）

```python
                ))
```
# 多重括号闭合：QRectF 右括号 + drawRect 右括号

```python

```
# 空行（代码结构分隔）

```python
    def cancel(self):
```
# 取消当前操作并重置状态，接收自身引用，无返回值

```python
        self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
        self._dragging_anchor_idx = -1
```
# 重置拖拽锚点索引

```python
        self._dragging_handle_idx = -1
```
# 重置拖拽手柄索引

```python
        self._dragging_item = None
```
#         清空拖拽目标

```python
        super().cancel()
```
#         调用父类 cancel() 重置基类状态

```python

```
# 空行（代码结构分隔）

```python
    @staticmethod
```
# staticmethod 装饰器

```python
    def _draw_single_anchor(painter: QPainter, item: PathItem, 
```
# 定义绘制单个锚点的静态方法，接收绘图引擎、贝塞尔路径项、锚点索引、是否高亮显示（默认True），无返回值

```python
                             anchor_idx: int, highlighted: bool = True):
```
# 参数续行：anchor_idx 要绘制的锚点索引（整数）、highlighted 是否高亮显示（布尔值，True 时使用蓝色填充加大尺寸，False 时使用白色填充较小尺寸）

```python
        """绘制单个锚点（供其他锚点工具使用）"""
```
# 类/方法文档字符串：绘制单个锚点（供其他锚点工具使用）

```python
        if anchor_idx < 0 or anchor_idx >= len(item.anchors):
```
# 边界检查：`anchor_idx < 0` 表示无选中锚点，`anchor_idx >= len(item.anchors)` 表示索引越界——两者任一成立则索引无效，提前返回

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        scale = max(painter.transform().m11(), 0.001)
```
#         获取画布缩放比例

```python
        anchor_half = 4.5 / scale if highlighted else 3.5 / scale
```
# 根据是否高亮选择锚点尺寸：选中时稍大 4.5px（更醒目），未选中时 3.5px（更紧凑）

```python
        transform = item._transform
```
#         获取图形项变换矩阵

```python
        anchor = item.anchors[anchor_idx]
```
#         获取指定索引的锚点

```python
        ax = transform.map(QPointF(anchor.x, anchor.y)).x()
```
#         将锚点 x 坐标映射到世界坐标

```python
        ay = transform.map(QPointF(anchor.x, anchor.y)).y()
```
#         将锚点 y 坐标映射到世界坐标

```python

```
# 空行（代码结构分隔）

```python
        if highlighted:
```
# 如果当前锚点为高亮状态（`highlighted` 为 True），使用蓝色填充 + 深蓝边框绘制选中锚点

```python
            painter.setBrush(QColor(0, 120, 215))
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
            painter.setPen(QPen(QColor(0, 80, 180), 1.5 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
        else:
```
# 否则（以上条件均不满足时执行）

```python
            painter.setBrush(QColor(255, 255, 255))
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python

```
# 空行（代码结构分隔）

```python
        painter.drawRect(QRectF(
```
# 绘制锚点方块：以锚点世界坐标 (ax, ay) 为中心绘制正方形标记

```python
            ax - anchor_half, ay - anchor_half,
```
# QRectF 左上角坐标：ax 减去半尺寸得到左上角 x、ay 减去半尺寸得到左上角 y

```python
            anchor_half * 2, anchor_half * 2,
```
# QRectF 宽度和高度：均为 anchor_half 的两倍（锚点方块的边长）

```python
        ))
```
# 多重括号闭合

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
# ── 形状工具 ──────────────────────────────────────────────
```
# 分隔注释：形状工具 —— 用于视觉分组

```python

```
# 空行（代码结构分隔）

```python
class ShapeTool(BaseTool, ABC):
```
# 定义 ShapeTool 形状工具抽象基类：继承 BaseTool 和 ABC，为矩形/椭圆工具提供统一的拖拽绘制框架

```python
    """形状工具基类（矩形/椭圆）"""
```
# 类/方法文档字符串：形状工具基类（矩形/椭圆）

```python
    __slots__ = ('_drag_start', '_drag_current', '_preview_item')
```
#     声明形状工具实例属性槽位

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self, tool_type: ToolType):
```
# 初始化方法（构造函数），接收自身引用、工具类型标识：工具类型，无返回值

```python
        super().__init__(tool_type)
```
#         调用父类构造函数

```python
        self._drag_start: QPointF | None = None
```
#         初始化拖拽起始坐标为 None

```python
        self._drag_current: QPointF | None = None
```
#         初始化拖拽当前坐标为 None

```python
        self._preview_item: GraphicItem | None = None
```
# 初始化形状预览图形项为 None（拖拽绘制过程中暂存预览对象，释放鼠标后转为正式图形项）

```python

```
# 空行（代码结构分隔）

```python
    @abstractmethod
```
# abstractmethod 装饰器

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
# 工厂方法：创建具体图形项，接收自身引用、矩形区域：浮点矩形，返回图形项

```python
        ...
```
# 省略号（抽象方法占位，由子类实现）

```python

```
# 空行（代码结构分隔）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# 鼠标按下事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        self._drag_start = QPointF(pos)
```
#         记录拖拽起始坐标

```python
        self._drag_current = QPointF(pos)
```
#         记录拖拽当前坐标（初始与起始相同）

```python
        self._is_drawing = True
```
# 将绘制状态标志初始化为 True

```python
        if self._document:
```
# 如果工具关联了文档

```python
            self._document.clear_selection()
```
#                     清除文档中所有图形项的选中状态

```python

```
# 空行（代码结构分隔）

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# 鼠标移动事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if self._is_drawing:
```
# 如果正在绘制中

```python
            self._drag_current = QPointF(pos)
```
#         记录拖拽当前坐标（初始与起始相同）

```python

```
# 空行（代码结构分隔）

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# 鼠标释放事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._is_drawing or not self._document or not self._drag_start:
```
# 如果工具未关联文档

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        self._drag_current = QPointF(pos)
```
#         记录拖拽当前坐标（初始与起始相同）

```python
        rect = QRectF(self._drag_start, self._drag_current).normalized()
```
# 创建矩形区域对象 `rect`：以鼠标按下位置和释放位置为对角构建矩形，`normalized()` 确保宽高为正值（处理反向拖拽）

```python

```
# 空行（代码结构分隔）

```python
        # Shift 约束等比（正方形/正圆）
```
# 注释说明：Shift 约束等比（正方形/正圆）

```python
        if modifiers & Qt.ShiftModifier:
```
#         如果按住 Shift，约束为纯水平或垂直移动

```python
            size = max(rect.width(), rect.height())
```
# 取矩形宽高中较大的值作为等比约束的统一尺寸
```
# 如果矩形高度大于宽度（纵向拖拽为主），则将宽度拉伸到与高度相等，形成正方形/正圆

```python
                rect.setWidth(size)
```
# 设置矩形的宽度（通过调整右边界实现）

```python
            else:
```
# 否则（以上条件均不满足时执行）

```python
                rect.setHeight(size)
```
# 设置矩形的高度（通过调整下边界实现）

```python

```
# 空行（代码结构分隔）

```python
        if rect.width() > 2 and rect.height() > 2:
```
# 如果矩形尺寸足够大（过滤意外点击）

```python
            item = self._create_item(rect)
```
# 调用子类工厂方法（RectangleTool/EllipseTool）创建具体图形项实例

```python
            item.selected = True
```
# 将当前图形项设为选中状态

```python
            self._document.add_item(item)
```
# 将新创建的图形项添加到文档的当前活动图层中

```python

```
# 空行（代码结构分隔）

```python
        self._drag_start = None
```
# 清空拖拽起始点

```python
        self._drag_current = None
```
#         清空拖拽当前坐标

```python
        self._is_drawing = False
```
#         将绘制状态标志重置为 False，标记取消绘制

```python

```
# 空行（代码结构分隔）

```python
    def draw_preview(self, painter: QPainter):
```
# 绘制预览方法，接收自身引用、绘图引擎：绘图引擎，无返回值

```python
        if self._is_drawing and self._drag_start and self._drag_current:
```
# 如果正在绘制中

```python
            rect = QRectF(self._drag_start, self._drag_current).normalized()
```
# 创建拖拽预览矩形区域对象 `rect`：以起始和当前位置为对角构建矩形并规范化

```python
            scale = max(painter.transform().m11(), 0.001)
```
#         获取画布缩放比例

```python
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
```
# 创建蓝色虚线画笔 + 半透明蓝色填充——用于绘制形状工具拖拽预览矩形
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
            painter.drawRect(rect)
```
# 在指定矩形区域绘制矩形（使用当前画笔描边+画刷填充）

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
class RectangleTool(ShapeTool):
```
# 定义 RectangleTool 矩形工具类：继承 ShapeTool，实现矩形的拖拽绘制

```python
    """矩形工具"""
```
# 类/方法文档字符串：矩形工具

```python
    __slots__ = ()
```
#     空槽位（无额外属性）

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self):
```
# 初始化方法（构造函数），接收自身引用，无返回值

```python
        super().__init__(ToolType.RECTANGLE)
```
#         调用父类构造函数，传入矩形工具类型

```python

```
# 空行（代码结构分隔）

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
# 工厂方法：创建具体图形项，接收自身引用、矩形区域：浮点矩形，返回图形项

```python
        item = RectangleItem(rect.x(), rect.y(), rect.width(), rect.height())
```
#         创建矩形图形项实例

```python
        item.style.fill_color = QColor(200, 200, 200)
```
#         设置默认填充色为浅灰色

```python
        item.style.stroke_color = QColor(50, 50, 50)
```
#         设置默认描边色为深灰色

```python
        item.style.stroke_width = 2.0
```
#         设置默认描边宽度 2 像素

```python
        return item
```
# 返回 item

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
class EllipseTool(ShapeTool):
```
# 定义 EllipseTool 椭圆工具类：继承 ShapeTool，实现椭圆的拖拽绘制

```python
    """椭圆工具"""
```
# 类/方法文档字符串：椭圆工具

```python
    __slots__ = ()
```
#     空槽位（无额外属性）

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self):
```
# 初始化方法（构造函数），接收自身引用，无返回值

```python
        super().__init__(ToolType.ELLIPSE)
```
# 调用父类构造函数进行初始化

```python

```
# 空行（代码结构分隔）

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
# 工厂方法：创建具体图形项，接收自身引用、矩形区域：浮点矩形，返回图形项

```python
        item = EllipseItem(rect.x(), rect.y(), rect.width(), rect.height())
```
# 创建椭圆图形项实例：传入矩形区域的坐标和尺寸

```python
        item.style.fill_color = QColor(200, 200, 200)
```
#         设置默认填充色为浅灰色

```python
        item.style.stroke_color = QColor(50, 50, 50)
```
#         设置默认描边色为深灰色

```python
        item.style.stroke_width = 2.0
```
#         设置默认描边宽度 2 像素

```python
        return item
```
# 返回 item

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
# ── 添加锚点工具 (Add Anchor Point Tool, +) ──────────────────
```
# 分隔注释：添加锚点工具 (Add Anchor Point Tool, +) —— 用于视觉分组

```python

```
# 空行（代码结构分隔）

```python
class AddAnchorPointTool(BaseTool):
```
# 定义 AddAnchorPointTool 添加锚点工具类：继承 BaseTool，在路径段上点击添加新锚点（对照 AI 的 + 工具）

```python
    """添加锚点工具 —— 在路径段上点击添加新锚点
```
# 类文档字符串续行：描述工具功能 —— 在路径段上点击添加新锚点

```python

```
# 空行（代码结构分隔）

```python
    对照 AI 行为：
```
# 工具行为规范：对照 Adobe Illustrator 的添加/删除/转换锚点工具行为

```python
    - 点击路径段 → 在最近位置添加新锚点（不进入拖拽）
```
# 行为规则：点击路径段 → 在最近位置添加新锚点（不进入拖拽）

```python
    - 只对已选中的路径有效
```
# 行为规则：只对已选中的路径有效

```python
    """
```
# 三引号字符串结束 —— 模块文档字符串至此闭合

```python
    __slots__ = ('_selected_anchor_idx', '_dragging_item')
```
# 声明实例属性槽位

```python

```
# 空行（代码结构分隔）

```python
    SEGMENT_TOLERANCE = 4.0
```
#     路径段命中容差：4 像素

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self):
```
# 初始化方法（构造函数），接收自身引用，无返回值

```python
        super().__init__(ToolType.ADD_ANCHOR)
```
#         调用父类构造函数，传入添加锚点工具类型

```python
        self._selected_anchor_idx: int = -1
```
# 初始化选中锚点索引为 -1（无效值），表示当前没有选中锚点

```python
        self._dragging_item: GraphicItem | None = None
```
# 初始化单选拖拽目标图形项为 None，表示当前无活跃的拖拽目标

```python

```
# 空行（代码结构分隔）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# 鼠标按下事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        for layer in reversed(self._document.layers):
```
# 倒序遍历文档的所有图层（从顶层到底层，模拟 AI 的 hit-test 顺序）

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵：`inv` 逆矩阵（用于世界坐标→局部坐标转换）、`ok` 是否成功；调用 DirectSelectTool 的静态方法实现

```python
                if not ok:
```
# 如果逆矩阵获取失败（ok 为 False），说明变换矩阵不可逆（如缩放为 0），跳过该图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                seg = item.get_segment_at(

```python
                    local_pos.x(), local_pos.y(),
```
# 获取本地坐标系中的 x 坐标分量

```python
                    tolerance=self.SEGMENT_TOLERANCE,
```
# 使用路径段容差 4.0px 进行命中检测

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                if seg >= 0:
```
# 如果命中了路径段

```python
                    # 找到最近点
```
# 注释说明：找到最近点

```python
                    closest = item.get_closest_point_on_segment(seg, local_pos.x(), local_pos.y())
```
#                     获取段上最近坐标

```python

```
# 空行（代码结构分隔）

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
# 列表推导式：对路径中每个锚点执行深拷贝，生成操作前的锚点状态快照

```python
                    new_anchor = AnchorPoint(closest[0], closest[1])
```
# 使用计算出的坐标 (mx, my) 创建新的角点锚点对象（默认类型为角点，无方向手柄）

```python
                    insert_idx = seg + 1
```
# 计算新锚点的插入位置索引：在检测到的路径段之后插入（`seg + 1`）

```python
                    item.insert_anchor(insert_idx, new_anchor)
```
# 在路径的指定位置插入新锚点（用于钢笔工具和添加锚点工具）

```python

```
# 空行（代码结构分隔）

```python
                    self._selected_anchor_idx = insert_idx
```
# 将新锚点的插入索引设为当前选中锚点索引

```python
                    self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python

```
# 空行（代码结构分隔）

```python
                    if self._document:
```
# 如果工具关联了文档

```python
                        new_anchors = [a.copy() for a in item.anchors]
```
# 对每个锚点执行深拷贝，生成锚点列表的副本（避免直接修改原始数据）

```python
                        cmd = ModifyAnchorCommand(
```
#                     创建修改锚点撤销命令

```python
                            self._document, item, old_anchors, new_anchors,
```
# ModifyAnchorCommand 参数：self._document 文档对象、item 目标路径项、old_anchors 操作前锚点快照、new_anchors 操作后锚点列表

```python
                        )
```
# 闭合括号：结束函数调用的参数列表

```python
                        self._document.execute_command(cmd)
```
# 通过文档统一入口执行命令对象（自动推入撤销栈，支持 Ctrl+Z 撤销）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# 鼠标移动事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        pass  # 不拖拽
```
# 空实现：添加锚点工具不支持拖拽，鼠标释放时不做任何操作

```python

```
# 空行（代码结构分隔）

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# 鼠标释放事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        pass
```
#         空实现（占位），由具体工具子类覆写

```python

```
# 空行（代码结构分隔）

```python
    def draw_preview(self, painter: QPainter):
```
# 绘制预览方法，接收自身引用、绘图引擎：绘图引擎，无返回值

```python
        """高亮显示新添加的锚点"""
```
# 类/方法文档字符串：高亮显示新添加的锚点

```python
        if self._selected_anchor_idx >= 0 and self._dragging_item:
```
#             如果有选中锚点和目标图形项

```python
            if isinstance(self._dragging_item, PathItem):
```
# 类型检查确认：拖拽目标是 PathItem，继续执行手柄调整逻辑

```python
                DirectSelectTool._draw_single_anchor(
```
# 调用 DirectSelectTool 的静态方法绘制单个锚点及其手柄的预览

```python
                    painter, self._dragging_item, self._selected_anchor_idx, True
```
# 参数：绘图引擎 painter、目标路径 self._dragging_item、选中锚点索引、高亮=True

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python

```
# 空行（代码结构分隔）

```python
    def cancel(self):
```
# 取消当前操作并重置状态，接收自身引用，无返回值

```python
        self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
        self._dragging_item = None
```
#         清空拖拽目标

```python
        super().cancel()
```
#         调用父类 cancel() 重置基类状态

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
# ── 删除锚点工具 (Delete Anchor Point Tool, -) ────────────────
```
# 分隔注释：删除锚点工具 (Delete Anchor Point Tool, -) —— 用于视觉分组

```python

```
# 空行（代码结构分隔）

```python
class DeleteAnchorPointTool(BaseTool):
```
# 定义 DeleteAnchorPointTool 删除锚点工具类：继承 BaseTool，点击锚点直接删除（对照 AI 的 - 工具）

```python
    """删除锚点工具 —— 点击锚点直接删除
```
# 类文档字符串续行：描述工具功能 —— 点击锚点直接删除

```python

```
# 空行（代码结构分隔）

```python
    对照 AI 行为：
```
# 工具行为规范：对照 Adobe Illustrator 的添加/删除/转换锚点工具行为

```python
    - 点击锚点 → 删除该锚点（保留路径连续性）
```
# 行为规则：点击锚点 → 删除该锚点，相邻锚点自动连接保持路径连续

```python
    - 至少保留 2 个锚点
```
# 行为规则：路径至少保留 2 个锚点（删除后不足 2 个则禁止操作）

```python
    - 只对已选中的路径有效
```
# 行为规则：只对已选中的路径有效

```python
    """
```
# 三引号字符串结束 —— 模块文档字符串至此闭合

```python
    __slots__ = ('_selected_anchor_idx', '_dragging_item')
```
# 声明实例属性槽位

```python

```
# 空行（代码结构分隔）

```python
    ANCHOR_TOLERANCE = 5.0
```
# 定义锚点命中检测容差为 5px（鼠标与锚点距离在此范围内视为命中）

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self):
```
# 初始化方法（构造函数），接收自身引用，无返回值

```python
        super().__init__(ToolType.DELETE_ANCHOR)
```
#         调用父类构造函数，传入删除锚点工具类型

```python
        self._selected_anchor_idx: int = -1
```
# 初始化选中锚点索引为 -1（无效值），表示当前没有选中锚点

```python
        self._dragging_item: GraphicItem | None = None
```
# 初始化单选拖拽目标图形项为 None，表示当前无活跃的拖拽目标

```python

```
# 空行（代码结构分隔）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# 鼠标按下事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        for layer in reversed(self._document.layers):
```
# 倒序遍历文档的所有图层（从顶层到底层，模拟 AI 的 hit-test 顺序）

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                if item.anchor_count <= 2:
```
#                 如果锚点不超过 2 个，跳过（最少保留 2 个）

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵：`inv` 逆矩阵（用于世界坐标→局部坐标转换）、`ok` 是否成功；调用 DirectSelectTool 的静态方法实现

```python
                if not ok:
```
# 如果逆矩阵获取失败（ok 为 False），说明变换矩阵不可逆（如缩放为 0），跳过该图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                idx = item.get_anchor_at(
```
#                     检测本地坐标处是否有锚点

```python
                    local_pos.x(), local_pos.y(),
```
# 获取本地坐标系中的 x 坐标分量

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
# 使用锚点容差 5.0px 进行命中检测

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                if idx >= 0:
```
# 如果命中了锚点/手柄

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
# 列表推导式：对路径中每个锚点执行深拷贝，生成操作前的锚点状态快照

```python
                    item.remove_anchor(idx)
```
# 删除路径的指定锚点，相邻锚点自动连接保持路径连续性

```python

```
# 空行（代码结构分隔）

```python
                    self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python
                    self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python

```
# 空行（代码结构分隔）

```python
                    if self._document:
```
# 如果工具关联了文档

```python
                        new_anchors = [a.copy() for a in item.anchors]
```
# 对每个锚点执行深拷贝，生成锚点列表的副本（避免直接修改原始数据）

```python
                        cmd = ModifyAnchorCommand(
```
#                     创建修改锚点撤销命令

```python
                            self._document, item, old_anchors, new_anchors,
```
# ModifyAnchorCommand 参数：self._document 文档对象、item 目标路径项、old_anchors 操作前锚点快照、new_anchors 操作后锚点列表

```python
                        )
```
# 闭合括号：结束函数调用的参数列表

```python
                        self._document.execute_command(cmd)
```
# 通过文档统一入口执行命令对象（自动推入撤销栈，支持 Ctrl+Z 撤销）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# 鼠标移动事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        pass
```
#         空实现（占位），由具体工具子类覆写

```python

```
# 空行（代码结构分隔）

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# 鼠标释放事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        pass
```
#         空实现（占位），由具体工具子类覆写

```python

```
# 空行（代码结构分隔）

```python
    def draw_preview(self, painter: QPainter):
```
# 绘制预览方法，接收自身引用、绘图引擎：绘图引擎，无返回值

```python
        pass  # AI 的删除锚点工具在悬停时显示 - 图标，这里简化处理
```
# 空实现：删除锚点工具的 mouse_move 采用简化处理（AI 原版会显示 - 光标提示）

```python

```
# 空行（代码结构分隔）

```python
    def cancel(self):
```
# 取消当前操作并重置状态，接收自身引用，无返回值

```python
        self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
        self._dragging_item = None
```
#         清空拖拽目标

```python
        super().cancel()
```
#         调用父类 cancel() 重置基类状态

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
# ── 转换锚点工具 (Convert Anchor Point Tool, Shift+C) ─────────
```
# 分隔注释：转换锚点工具 (Convert Anchor Point Tool, Shift+C) ─ —— 用于视觉分组

```python

```
# 空行（代码结构分隔）

```python
class ConvertAnchorPointTool(BaseTool):
```
# 定义 ConvertAnchorPointTool 转换锚点工具类：继承 BaseTool，切换锚点类型或拖拽拉出手柄（对照 AI 的 Shift+C 工具）

```python
    """转换锚点工具 —— 切换锚点类型 / 拖拽拉出手柄
```
# 类文档字符串续行：描述工具功能 —— 切换锚点类型 / 拖拽拉出手柄

```python

```
# 空行（代码结构分隔）

```python
    对照 AI 行为：
```
# 工具行为规范：对照 Adobe Illustrator 的添加/删除/转换锚点工具行为

```python
    - 点击平滑点 → 转为角点（移除手柄）
```
# 行为规则：点击平滑点 → 转为角点（移除双向手柄）

```python
    - 点击角点并拖拽 → 拉出手柄转为平滑点
```
# 行为规则续行：点击角点并拖拽 → 拉出手柄将角点转为平滑点

```python
    - 拖拽手柄 → 断开对称约束
```
# 行为规则续行：拖拽已有手柄 → 断开双向手柄的对称约束

```python
    """
```
# 三引号字符串结束 —— 模块文档字符串至此闭合

```python
    __slots__ = (
```
# 声明实例属性槽位：限定该类只能拥有元组中列出的属性，禁止动态添加新属性

```python
        '_drag_start', '_dragging_item', '_dragging_anchor_idx',
```
# __slots__ 续行：'_drag_start' 拖拽起始坐标、'_dragging_item' 当前拖拽目标图形项、'_dragging_anchor_idx' 正在拖拽的锚点索引

```python
        '_is_dragging', '_old_anchors',
```
# __slots__ 续行：'_is_dragging' 是否已确认开始有效拖拽（超过阈值）、'_old_anchors' 操作前锚点快照（用于撤销）

```python
    )
```
# 闭合括号：结束函数调用的参数列表

```python

```
# 空行（代码结构分隔）

```python
    ANCHOR_TOLERANCE = 5.0
```
# 定义锚点命中检测容差为 5px（鼠标与锚点距离在此范围内视为命中）

```python
    DRAG_THRESHOLD = 3.0
```
# 定义最小拖拽阈值为 3px（鼠标移动距离小于此值视为点击而非拖拽）

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self):
```
# 初始化方法（构造函数），接收自身引用，无返回值

```python
        super().__init__(ToolType.CONVERT_ANCHOR)
```
#         调用父类构造函数，传入转换锚点工具类型

```python
        self._drag_start: QPointF | None = None
```
#         初始化拖拽起始坐标为 None

```python
        self._dragging_item: GraphicItem | None = None
```
# 初始化单选拖拽目标图形项为 None，表示当前无活跃的拖拽目标

```python
        self._dragging_anchor_idx: int = -1
```
# 初始化拖拽锚点索引为 -1（无效值），表示当前未选中任何锚点

```python
        self._is_dragging: bool = False
```
# 初始化拖拽标志为 False，标记当前未在进行锚点手柄拖拽

```python
        self._old_anchors: list[AnchorPoint] = []
```
# 初始化旧锚点快照列表为空，用于操作前保存锚点原始状态（生成撤销命令时使用）

```python

```
# 空行（代码结构分隔）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# 鼠标按下事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        self._drag_start = QPointF(pos)
```
#         记录拖拽起始坐标

```python
        self._is_dragging = False
```
# 将拖拽进行中标志初始化为 False

```python

```
# 空行（代码结构分隔）

```python
        for layer in reversed(self._document.layers):
```
# 倒序遍历文档的所有图层（从顶层到底层，模拟 AI 的 hit-test 顺序）

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵：`inv` 逆矩阵（用于世界坐标→局部坐标转换）、`ok` 是否成功；调用 DirectSelectTool 的静态方法实现

```python
                if not ok:
```
# 如果逆矩阵获取失败（ok 为 False），说明变换矩阵不可逆（如缩放为 0），跳过该图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                idx = item.get_anchor_at(
```
#                     检测本地坐标处是否有锚点

```python
                    local_pos.x(), local_pos.y(),
```
# 获取本地坐标系中的 x 坐标分量

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
# 使用锚点容差 5.0px 进行命中检测

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                if idx >= 0:
```
# 如果命中了锚点/手柄

```python
                    self._dragging_item = item
```
#                 设置当前图形项为单项拖拽目标

```python
                    self._dragging_anchor_idx = idx
```
# 记录被拖拽的锚点索引

```python
                    self._old_anchors = [a.copy() for a in item.anchors]
```
# 深拷贝当前所有锚点保存为旧状态（用于生成 ModifyAnchorCommand 撤销命令）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# 鼠标移动事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._dragging_item or self._dragging_anchor_idx < 0:
```
# 类型检查确认：拖拽目标是 PathItem，继续执行手柄调整逻辑

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        if self._drag_start is None:
```
#         如果没有拖拽起始点，不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        dx = pos.x() - self._drag_start.x()
```
#         计算水平方向增量

```python
        dy = pos.y() - self._drag_start.y()
```
#         计算垂直方向增量

```python
        dist = math.sqrt(dx*dx + dy*dy)
```
# 计算鼠标当前位置与起始锚点之间的欧几里得距离，用于判断是否满足闭合路径的容差条件

```python

```
# 空行（代码结构分隔）

```python
        if not self._is_dragging:
```
# 条件分支：鼠标按下后移动距离超过阈值，确认进入拖拽模式

```python
            if dist < self.DRAG_THRESHOLD:
```
#                 如果距离未超过阈值

```python
                return
```
#         提前返回，不执行后续逻辑

```python
            self._is_dragging = True
```
# 将拖拽进行中标志初始化为 True

```python

```
# 空行（代码结构分隔）

```python
        # 拖拽：从锚点拉出手柄
```
# 注释说明：拖拽：从锚点拉出手柄

```python
        if isinstance(self._dragging_item, PathItem):
```
# 类型检查确认：拖拽目标是 PathItem，继续执行手柄调整逻辑

```python
            inv, ok = DirectSelectTool._safe_inverted(self._dragging_item._transform)
```
# 安全获取当前拖拽目标图形项变换矩阵的逆矩阵：`inv` 逆矩阵（用于世界坐标→局部坐标转换）、`ok` 是否成功

```python
            if not ok:
```
# 如果逆矩阵获取失败（ok 为 False），说明变换矩阵不可逆（如缩放为 0），跳过该图形项

```python
                return
```
#         提前返回，不执行后续逻辑

```python
            local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
            anchor = self._dragging_item.anchors[self._dragging_anchor_idx]
```
# 获取当前拖拽的锚点对象 `anchors[self._dragging_anchor_idx]`，保存到局部变量 `anchor`

```python

```
# 空行（代码结构分隔）

```python
            rel_x = local_pos.x() - anchor.x
```
#                 计算手柄相对锚点的水平偏移

```python
            rel_y = local_pos.y() - anchor.y
```
#                 计算手柄相对锚点的垂直偏移

```python

```
# 空行（代码结构分隔）

```python
            # 拉出双向对称手柄（平滑点）
```
# 注释说明：拉出双向对称手柄（平滑点）

```python
            anchor.handle_out = QPointF(rel_x, rel_y)
```
# 设置出方向手柄坐标为 QPointF(rel_x, rel_y)，即鼠标相对于锚点的偏移方向

```python
            anchor.handle_in = QPointF(-rel_x, -rel_y)
```
# 设置入方向手柄坐标为 QPointF(-rel_x, -rel_y)，与出方向手柄方向相反（对称约束）

```python
            anchor.anchor_type = AnchorPointType.SMOOTH
```
# 将锚点类型设为 SMOOTH（平滑点），表示拥有对称双向手柄

```python

```
# 空行（代码结构分隔）

```python
            self._dragging_item._build_path()
```
# 根据当前锚点数据重新构建 QPainterPath 绘制路径

```python
            if self._document:
```
# 如果工具关联了文档

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行（代码结构分隔）

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# 鼠标释放事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._dragging_item or self._dragging_anchor_idx < 0:
```
# 类型检查确认：拖拽目标是 PathItem，继续执行手柄调整逻辑

```python
            self._drag_start = None
```
# 清空拖拽起始点

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        if isinstance(self._dragging_item, PathItem):
```
# 类型检查：确认拖拽目标是 PathItem，只有路径才有锚点类型可转换（角点↔平滑点）

```python
            anchor = self._dragging_item.anchors[self._dragging_anchor_idx]
```
# 获取被拖拽手柄所属的锚点对象，保存到局部变量 anchor

```python

```
# 空行（代码结构分隔）

```python
            if not self._is_dragging:
```
# 条件分支：鼠标按下后移动距离超过阈值，确认进入拖拽模式

```python
                # 点击（未拖拽）：切换锚点类型
```
# 注释说明：点击（未拖拽）：切换锚点类型

```python
                if anchor.has_handles:
```
# 如果锚点有手柄（平滑点）

```python
                    # 有手柄 → 转为角点（移除手柄）
```
# 注释说明：有手柄 → 转为角点（移除手柄）

```python
                    anchor.remove_handles()
```
# 移除锚点的贝塞尔控制手柄（将平滑点转为角点）

```python
                # 无手柄的角点 → 点击不产生变化（AI 行为）
```
# 注释说明：无手柄的角点 → 点击不产生变化（AI 行为）

```python
                self._dragging_item._build_path()
```
# 根据当前锚点数据重新构建 QPainterPath 绘制路径

```python

```
# 空行（代码结构分隔）

```python
            # 记录撤销命令（通过 execute_command 统一入口）
```
# 注释说明：记录撤销命令（通过 execute_command 统一入口）

```python
            if self._document and self._old_anchors:
```
# 如果存在旧锚点快照（用于撤销）

```python
                new_anchors = [a.copy() for a in self._dragging_item.anchors]
```
#             创建当前所有锚点的副本

```python
                cmd = ModifyAnchorCommand(
```
#                     创建修改锚点撤销命令

```python
                    self._document, self._dragging_item,
```
# ModifyAnchorCommand 参数：self._document 文档对象（命令上下文）、self._dragging_item 被操作的路径项

```python
                    self._old_anchors, new_anchors,
```
# ModifyAnchorCommand 参数：self._old_anchors 操作前锚点快照（旧值）、new_anchors 操作后锚点列表（新值）

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
                self._document.execute_command(cmd)
```
# 通过文档统一入口执行命令对象（自动推入撤销栈，支持 Ctrl+Z 撤销）

```python

```
# 空行（代码结构分隔）

```python
        self._drag_start = None
```
# 清空拖拽起始点

```python
        self._dragging_item = None
```
#         清空拖拽目标

```python
        self._dragging_anchor_idx = -1
```
# 重置拖拽锚点索引

```python
        self._is_dragging = False
```
# 将拖拽进行中标志初始化为 False

```python
        self._old_anchors = []
```
# 清空旧锚点列表

```python

```
# 空行（代码结构分隔）

```python
    def draw_preview(self, painter: QPainter):
```
# 绘制预览方法，接收自身引用、绘图引擎：绘图引擎，无返回值

```python
        """拖拽时显示预览手柄线"""
```
# 类/方法文档字符串：拖拽时显示预览手柄线

```python
        if self._is_dragging and self._dragging_item and self._dragging_anchor_idx >= 0:
```
# 条件检查：`self._is_dragging` 正在拖拽中，`self._dragging_item` 有拖拽目标图形项，`self._dragging_anchor_idx >= 0` 有有效的锚点索引——三个条件同时满足时才执行手柄调整逻辑

```python
            if isinstance(self._dragging_item, PathItem):
```
# 类型检查：确认拖拽目标是 PathItem，只有路径才有锚点手柄可修改

```python
                DirectSelectTool._draw_single_anchor(
```
# 调用 DirectSelectTool 的静态方法绘制单个锚点及其手柄的预览

```python
                    painter, self._dragging_item, self._dragging_anchor_idx, True
```
# 参数：painter 绘图引擎、self._dragging_item 目标路径项、self._dragging_anchor_idx 锚点索引、True 表示高亮显示

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python

```
# 空行（代码结构分隔）

```python
    def cancel(self):
```
# 取消当前操作并重置状态，接收自身引用，无返回值

```python
        self._dragging_item = None
```
#         清空拖拽目标

```python
        self._dragging_anchor_idx = -1
```
# 重置拖拽锚点索引

```python
        self._is_dragging = False
```
# 将拖拽进行中标志初始化为 False

```python
        super().cancel()
```
#         调用父类 cancel() 重置基类状态

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
# ── 钢笔工具 ──────────────────────────────────────────────
```
# 分隔注释：钢笔工具 —— 用于视觉分组

```python

```
# 空行（代码结构分隔）

```python
class PenTool(BaseTool):
```
# 定义 PenTool 钢笔工具类：继承 BaseTool，1:1 对照 Adobe Illustrator 钢笔工具——单击创建角点、拖拽创建平滑点、闭合路径、添加/删除锚点

```python
    """钢笔工具 —— Adobe Illustrator 1:1 复原
```
# 类文档字符串续行：描述工具功能 —— 1:1 复原 Adobe Illustrator 钢笔工具

```python

```
# 空行（代码结构分隔）

```python
    功能对照：
```
# 功能对照表标题续行（列出钢笔工具的核心交互行为）

```python
    - 单击 = 创建角点（Corner Point），无手柄
```
# - 单击：创建角点（Corner Point），无方向手柄

```python
    - 单击并拖动 = 创建平滑点（Smooth Point），拉出对称手柄
```
# - 单击并拖动：创建平滑点（Smooth Point），拖拽拉出对称方向手柄

```python
    - 点击起始锚点 = 闭合路径（光标出现圆圈 ○）
```
# - 点击起始锚点：闭合路径（光标出现圆圈 ○ 提示）

```python
    - Enter/Return = 结束路径
```
# - Enter/Return：结束开放路径（不闭合首尾）

```python
    - Escape = 取消路径
```
# - Escape：取消当前绘制中的路径，丢弃所有锚点

```python

```
# 空行（代码结构分隔）

```python
    隐藏功能：
```
# 隐藏功能列表标题续行（高级用户快捷操作）

```python
    - Alt/Option 拖拽 = 调整单侧方向线（断开对称）
```
# - Alt/Option 拖拽：调整单侧方向线（断开对称约束，转为角点）

```python
    - Ctrl/Cmd = 临时切换直接选择工具调整锚点
```
# - Ctrl/Cmd：临时切换为直接选择工具，可调整已放置的锚点位置

```python
    - Space = 在拖动过程中临时移动当前锚点位置
```
# - Space（空格）：在拖动过程中临时移动当前锚点位置（不改变手柄方向）

```python
    - Shift = 约束角度（45度增量）
```
# - Shift：约束手柄角度为 45° 增量

```python

```
# 空行（代码结构分隔）

```python
    光标状态：
```
# 光标状态列表标题续行（不同悬停位置显示不同光标形状）

```python
    - 默认 = Pen（十字光标）
```
# - 默认：Pen（十字光标），表示标准钢笔工具

```python
    - 悬停已有锚点 = Pen-（删除锚点）
```
# - 悬停已有锚点：Pen-（删除锚点光标）

```python
    - 悬停已有路径段 = Pen+（添加锚点）
```
# - 悬停已有路径段：Pen+（添加锚点光标）

```python
    - 悬停起始锚点 = Pen○（闭合路径）
```
# - 悬停起始锚点：Pen○（闭合路径光标）

```python
    - 悬停端点 = Pen/（继续路径）
```
# - 悬停端点：Pen/（继续路径光标），表示点击可从端点继续绘制路径

```python
    """
```
# 三引号字符串结束 —— 模块文档字符串至此闭合

```python

```
# 空行（代码结构分隔）

```python
    DRAG_THRESHOLD = 3  # 拖拽阈值（像素），小于此值视为单击
```
# 定义拖拽阈值为 3px：鼠标移动距离小于此值视为单击（创建角点），大于等于此值视为拖拽（创建平滑点并拉出手柄）

```python
    CLOSE_TOLERANCE = 8  # 闭合路径检测容差
```
# 定义闭合路径检测容差为 8px：鼠标与起始锚点距离小于此值时自动闭合路径

```python
    HANDLE_TOLERANCE = 5  # 手柄命中容差
```
# 定义手柄命中检测容差为 5px

```python
    ANCHOR_TOLERANCE = 6  # 锚点命中容差
```
# 定义锚点命中检测容差为 6px

```python
    SEGMENT_TOLERANCE = 5  # 路径段命中容差
```
# 定义路径段命中检测容差为 5px

```python
    SHIFT_ANGLE_STEP = 45  # Shift约束角度步长（度）
```
# 定义 Shift 约束的角度步长为 45°，拖拽手柄时角度自动吸附到 0°/45°/90°/135° 等固定方向

```python

```
# 空行（代码结构分隔）

```python
    __slots__ = (
```
# 声明实例属性槽位：限定该类只能拥有元组中列出的属性，禁止动态添加新属性

```python
        '_current_path', '_drawing', '_hover_state',
```
# __slots__ 续行：'_current_path' 当前正在绘制的路径项、'_drawing' 是否处于绘制状态、'_hover_state' 钢笔光标悬停状态枚举

```python
        '_drag_start_pos', '_is_dragging_handle',
```
# __slots__ 续行：'_drag_start_pos' 拖拽起始坐标、'_is_dragging_handle' 是否正在拖拽方向手柄

```python
        '_dragged_anchor_idx', '_dragged_handle_side',
```
# __slots__ 续行：'_dragged_anchor_idx' 被拖拽手柄所属锚点索引、'_dragged_handle_side' 手柄方向（'in'/'out'）

```python
        '_alt_adjusting', '_space_moving', '_space_start_pos',
```
# __slots__ 续行：'_alt_adjusting' Alt 键调整中、'_space_moving' Space 键移动中、'_space_start_pos' Space 按下时的锚点位置

```python
        '_ctrl_temp_select', '_ctrl_drag_start',
```
# __slots__ 续行：'_ctrl_temp_select' Ctrl 临时切换为直接选择、'_ctrl_drag_start' Ctrl 切换时拖拽起始位置

```python
    )
```
# 闭合括号：结束函数调用的参数列表

```python

```
# 空行（代码结构分隔）

```python
    # ── 钢笔光标状态枚举 ──
```
# 分隔注释：钢笔光标状态枚举 —— 用于视觉分组

```python
    PEN_DEFAULT = 0        # 默认钢笔
```
# 光标状态常量 `PEN_DEFAULT = 0`：默认十字光标，鼠标不在任何特殊目标上时显示

```python
    PEN_PLUS = 1           # Pen+  添加锚点
```
# 光标状态常量 `PEN_PLUS = 1`：Pen+ 光标，鼠标悬停在路径段上可添加新锚点时显示

```python
    PEN_MINUS = 2          # Pen-  删除锚点
```
# 光标状态常量 `PEN_MINUS = 2`：Pen- 光标，鼠标悬停在已有锚点上可删除时显示

```python
    PEN_CLOSE = 3          # Pen○  闭合路径
```
# 光标状态常量 `PEN_CLOSE = 3`：Pen○ 闭合光标，鼠标悬停在起始锚点上可闭合路径时显示

```python
    PEN_CONTINUE = 4       # Pen/  继续路径
```
# 光标状态常量 `PEN_CONTINUE = 4`：Pen/ 继续光标，鼠标悬停在路径端点上可继续绘制时显示

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self):
```
# 初始化方法（构造函数），接收自身引用，无返回值

```python
        super().__init__(ToolType.PEN)
```
#         调用父类构造函数，传入钢笔工具类型

```python
        self._current_path: PathItem | None = None
```
# 初始化当前绘制路径为 None，钢笔工具开始绘制时创建路径对象

```python
        self._drawing: bool = False          # 正在拖拽中（创建平滑点）
```
# 初始化绘制状态 `_drawing` 为 False，表示当前没有正在绘制新路径

```python
        self._hover_state: int = PenTool.PEN_DEFAULT
```
# 初始化钢笔光标悬停状态为默认值 `PEN_DEFAULT`（标准十字光标）

```python

```
# 空行（代码结构分隔）

```python
        # 拖拽状态
```
# 注释说明：拖拽状态

```python
        self._drag_start_pos: QPointF | None = None
```
# 初始化拖拽起始位置为 None，记录鼠标按下时的位置（用于创建平滑点手柄）

```python
        self._is_dragging_handle: bool = False
```
# 初始化手柄拖拽标志为 False，标记当前未在拖拽锚点的方向手柄

```python
        self._dragged_anchor_idx: int = -1
```
# 初始化被拖拽手柄所属的锚点索引为 -1（无效值）

```python
        self._dragged_handle_side: str = ''
```
# 初始化拖拽的手柄方向为空字符串，`'in'` 入方向手柄、`'out'` 出方向手柄

```python

```
# 空行（代码结构分隔）

```python
        # 隐藏功能状态
```
# 注释说明：隐藏功能状态

```python
        self._alt_adjusting: bool = False     # Alt 调整单侧方向线
```
# 初始化 Alt 键调整标志为 False：标记是否正在使用 Alt 键断开手柄对称约束

```python
        self._space_moving: bool = False       # Space 移动当前锚点
```
# 初始化 Space 移动标志为 False：标记是否正在按住空格键临时移动锚点位置

```python
        self._space_start_pos: QPointF | None = None
```
# 初始化 Space 键按下时的锚点起始位置为 None（Space 键临时移动锚点功能）

```python
        self._ctrl_temp_select: bool = False   # Ctrl 临时直接选择
```
# 初始化 Ctrl 临时直接选择标志为 False：标记是否正在按住 Ctrl 键临时切换为直接选择工具

```python
        self._ctrl_drag_start: QPointF | None = None
```
# 初始化 Ctrl 键按下时的拖拽起始位置为 None（Ctrl 键临时切换为直接选择工具功能）

```python

```
# 空行（代码结构分隔）

```python
    # ── 辅助方法 ──
```
# 分隔注释：辅助方法区域

```python

```
# 空行（代码结构分隔）

```python
    def _snap_angle(self, dx: float, dy: float) -> tuple[float, float]:
```
# 将偏移量约束到最近的45度增量，接收自身引用、X方向偏移量：浮点数、Y方向偏移量：浮点数，返回坐标元组(浮点X, 浮点Y)

```python
        """Shift约束角度到最近的45度增量"""
```
# 类/方法文档字符串：Shift约束角度到最近的45度增量

```python
        angle = math.atan2(dy, dx)
```
# 使用 atan2 计算鼠标拖拽方向的角度（弧度），再转换为 Shift 约束角度步长的弧度值（45° = π/4）
第一行：把配置的角度步长转成计算机能用的弧度
第二行：把当前角度吸附对齐到最近的步长角度
```python
        snapped = round(angle / step_rad) * step_rad
```
# 将 `angle` 除以 45° 的弧度值后四舍五入，再乘回弧度值，得到约束到最近 45° 增量的角度 `snapped`

```python
        length = math.sqrt(dx*dx + dy*dy)
```
# 计算鼠标拖拽的直线距离 `length`（用于创建手柄时的长度参考）
根据角度和长度，计算出平面直角坐标系上的点 (x, y)
```python
        return (math.cos(snapped) * length, math.sin(snapped) * length)
```
# 返回 (math.cos(snapped) * length, math.sin(snapped) * length)

```python

```
# 空行（代码结构分隔）

```python
    def _detect_hover_state(self, pos: QPointF, doc) -> int:
```
# 检测悬停位置并返回钢笔光标状态，接收自身引用、鼠标位置坐标：二维浮点坐标、文档对象，返回整数

```python
        """检测悬停位置，返回钢笔光标状态"""
```
# 类/方法文档字符串：检测悬停位置，返回钢笔光标状态

```python
        # 遍历所有可见图层的路径项
```
# 注释说明：遍历所有可见图层的路径项

```python
        for layer in reversed(doc.layers):
```
# 逆序遍历文档的图层（从上到下），优先处理顶层可见元素

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                if not isinstance(item, PathItem) or not item.visible or item.locked:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python

```
# 空行（代码结构分隔）

```python
                # 1) 检测锚点 → Pen-
```
# 注释说明：1) 检测锚点 → Pen-

```python
                anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
```
# 对当前路径的所有锚点调用 `get_anchor_at` 检测鼠标局部坐标是否命中某个锚点，`anchor_idx` 为命中锚点的索引（≥0 命中，-1 未命中）
```
# 注释说明：如果是当前正在绘制的路径的锚点，继续判断

```python
                    if item is self._current_path:
```
# 条件检查：当前命中的路径项 `item` 就是正在绘制的路径 `self._current_path`，需要进一步判断鼠标是在起始锚点还是端点上

```python
                        # 起始锚点 → Pen○ 闭合
```
# 注释说明：起始锚点 → Pen○ 闭合

```python
                        if anchor_idx == 0 and len(item.anchors) >= 2:
```
# 条件检查：`anchor_idx == 0` 鼠标在起始锚点上，`len(item.anchors) >= 2` 路径至少有 2 个锚点可以闭合——同时满足时显示 Pen○ 闭合光标

```python
                            return PenTool.PEN_CLOSE
```
# 返回 PenTool.PEN_CLOSE

```python
                        # 端点 → Pen/ 继续
```
# 注释说明：端点 → Pen/ 继续

```python
                        if anchor_idx == len(item.anchors) - 1:
```
# 条件检查：`anchor_idx == len(item.anchors) - 1` 鼠标在路径的最后一个端点锚点上，可以继续追加绘制

```python
                            return PenTool.PEN_CONTINUE
```
# 返回 PenTool.PEN_CONTINUE

```python
                    return PenTool.PEN_MINUS
```
# 返回 PenTool.PEN_MINUS

```python

```
# 空行（代码结构分隔）

```python
                # 2) 检测路径段 → Pen+
```
# 注释说明：2) 检测路径段 → Pen+

```python
                seg_idx = item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)
```
# 对当前路径的所有线段调用 `get_segment_at` 检测鼠标局部坐标是否命中某条路径段，`seg_idx` 为命中段的索引

```python
                if seg_idx >= 0:
```
# 如果命中了锚点/手柄

```python
                    return PenTool.PEN_PLUS
```
# 返回 PenTool.PEN_PLUS

```python

```
# 空行（代码结构分隔）

```python
        # 3) 如果当前有路径且接近起始点 → Pen○
```
# 注释说明：3) 如果当前有路径且接近起始点 → Pen○

```python
        if self._current_path and len(self._current_path.anchors) >= 2:
```
# 如果存在当前正在绘制的路径

```python
            first = self._current_path.anchors[0]
```
# 获取当前绘制路径的第一个锚点（起始锚点），用于判断是否满足闭合条件

```python
            dist = math.sqrt((pos.x() - first.x)**2 + (pos.y() - first.y)**2)
```
# 计算鼠标与起始锚点之间的欧几里得距离，用于判断是否满足闭合容差条件

```python
            if dist < PenTool.CLOSE_TOLERANCE:
```
# 如果满足条件：dist < PenTool.CLOSE_TOLERANCE（满足时执行以下逻辑）

```python
                return PenTool.PEN_CLOSE
```
# 返回 PenTool.PEN_CLOSE

```python

```
# 空行（代码结构分隔）

```python
        return PenTool.PEN_DEFAULT
```
# 返回 PenTool.PEN_DEFAULT

```python

```
# 空行（代码结构分隔）

```python
    # ── 鼠标事件 ──
```
# 分隔注释：鼠标事件处理方法区域

```python

```
# 空行（代码结构分隔）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# 鼠标按下事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        doc = self._document
```
# 将工具关联的文档引用 `self._document` 赋值给局部变量 `doc`，便于后续方法调用中频繁使用

```python
        is_alt = bool(modifiers & Qt.AltModifier)
```
# 检测修饰键状态：`is_alt` Alt/Option 键是否按下（用于断开手柄对称约束）

```python

```
# 空行（代码结构分隔）

```python
        # ── Ctrl/Cmd 临时切换直接选择工具 ──
```
# 分隔注释：Ctrl/Cmd 临时切换直接选择工具 —— 用于视觉分组

```python
        if is_ctrl:
```
# 如果按住 Ctrl 键

```python
            self._ctrl_temp_select = True
```
# 将Ctrl 临时选择标志初始化为 True

```python
            self._ctrl_drag_start = QPointF(pos)
```
# 记录拖拽起始位置到 _ctrl_drag_start

```python
            # 查找点击位置的路径项和锚点
```
# 注释说明：查找点击位置的路径项和锚点

```python
            for layer in reversed(doc.layers):
```
# 逆序遍历文档的图层（从上到下），优先处理顶层可见元素

```python
                if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                for item in layer.items:
```
# 遍历当前图层的所有图形项

```python
                    if not isinstance(item, PathItem) or not item.visible or item.locked:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                        continue
```
# 跳过当前循环迭代，继续下一个

```python
                    anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
```
# 调用 `get_anchor_at` 检测鼠标局部坐标是否命中某个锚点，`anchor_idx` 为命中锚点的索引（≥0 命中，-1 未命中）

```python
                    if anchor_idx >= 0:
```
# 如果命中了锚点

```python
                        self._dragged_anchor_idx = anchor_idx
```
# 记录被拖拽手柄所属的锚点索引到 _dragged_anchor_idx

```python
                        # 临时将该路径设为当前编辑路径
```
# 注释说明：临时将该路径设为当前编辑路径

```python
                        self._current_path = item
```
# 将当前路径项保存为钢笔工具的绘制路径（_current_path），后续锚点添加操作都作用于此路径

```python
                        return
```
#         提前返回，不执行后续逻辑

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── 检测悬停状态决定行为 ──
```
# 分隔注释：检测悬停状态决定行为 —— 用于视觉分组

```python
        hover = self._detect_hover_state(pos, doc)
```
# 调用 `_detect_hover_state` 检测鼠标当前位置下应显示的钢笔光标状态（Pen-/Pen+/Pen○/Pen/ 或默认）

```python

```
# 空行（代码结构分隔）

```python
        # 悬停已有路径的锚点（非当前路径） → 删除锚点（Pen-）
```
# 注释说明：悬停已有路径的锚点（非当前路径） → 删除锚点（Pen-）

```python
        if hover == PenTool.PEN_MINUS:
```
# 如果满足条件：hover == PenTool.PEN_MINUS（满足时执行以下逻辑）

```python
            self._try_delete_anchor(pos, doc)
```
# 尝试删除路径上点击位置的锚点（钢笔工具模式下 Alt+点击锚点删除）

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # 悬停已有路径段 → 添加锚点（Pen+）
```
# 注释说明：悬停已有路径段 → 添加锚点（Pen+）

```python
        if hover == PenTool.PEN_PLUS:
```
# 如果满足条件：hover == PenTool.PEN_PLUS（满足时执行以下逻辑）

```python
            self._try_add_anchor(pos, doc)
```
# 尝试在路径线段上添加新锚点（钢笔工具模式下点击路径段添加锚点）

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # 悬停当前路径起始锚点 → 闭合路径（Pen○）
```
# 注释说明：悬停当前路径起始锚点 → 闭合路径（Pen○）

```python
        if hover == PenTool.PEN_CLOSE and self._current_path:
```
# 如果存在当前正在绘制的路径

```python
            self._close_path()
```
# 闭合当前钢笔路径：连接首尾锚点形成封闭形状

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── 正常绘制模式 ──
```
# 分隔注释：正常绘制模式 —— 用于视觉分组

```python
        # 如果没有当前路径，创建新路径
```
# 注释说明：如果没有当前路径，创建新路径

```python
        if self._current_path is None:
```
# 如果存在当前正在绘制的路径

```python
            self._current_path = PathItem()
```
# 创建新的空白 PathItem 路径对象作为钢笔工具的当前绘制路径，后续锚点添加操作都作用于此路径

```python
            self._current_path.style.fill_color = QColor(200, 200, 200, 100)
```
# 设置路径默认填充色为浅灰色 (200,200,200)

```python
            self._current_path.style.stroke_color = QColor(50, 50, 50)
```
# 设置路径默认描边色为深灰色 (50,50,50)

```python
            self._current_path.style.stroke_width = 2.0
```
# 设置路径描边线宽为 2.0（默认粗细）

```python
            doc.add_item(self._current_path)
```
# 将图形项添加到文档的活动图层中

```python

```
# 空行（代码结构分隔）

```python
        # 记录拖拽起始位置
```
# 注释说明：记录拖拽起始位置

```python
        self._drag_start_pos = QPointF(pos)
```
# 记录拖拽起始位置到 _drag_start_pos

```python
        self._drawing = True
```
# 将拖拽绘制状态初始化为 True

```python

```
# 空行（代码结构分隔）

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# 鼠标移动事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        is_alt = bool(modifiers & Qt.AltModifier)
```
# 检测 Alt/Option 键是否按下：将 Qt 修饰键位掩码与 AltModifier 做按位与运算，转换为布尔值，用于断开手柄对称约束

```python
        is_ctrl = bool(modifiers & Qt.ControlModifier)
```
# 检测 Ctrl/Cmd 键是否按下：将 Qt 修饰键位掩码与 ControlModifier 做按位与运算，用于临时切换为直接选择工具

```python
        is_shift = bool(modifiers & Qt.ShiftModifier)
```
# 检测 Shift 键是否按下：将 Qt 修饰键位掩码与 ShiftModifier 做按位与运算，用于约束手柄角度为 45° 增量

```python
        is_space = bool(modifiers & Qt.Key_Space if hasattr(Qt, 'Key_Space') else False)
```
# 检测空格键是否按下：用于在拖拽过程中临时移动当前锚点位置（不改变手柄方向）

```python

```
# 空行（代码结构分隔）

```python
        # ── Ctrl 临时直接选择：移动锚点 ──
```
# 分隔注释：Ctrl 临时直接选择：移动锚点 —— 用于视觉分组

```python
        if self._ctrl_temp_select and self._current_path and self._ctrl_drag_start:
```
# 如果处于 Ctrl 临时选择模式

```python
            dx = pos.x() - self._ctrl_drag_start.x()
```
# 计算鼠标相对于拖拽起始位置的水平偏移量 dx

```python
            dy = pos.y() - self._ctrl_drag_start.y()
```
# 计算鼠标相对于拖拽起始位置的垂直偏移量 dy

```python
            if self._dragged_anchor_idx >= 0 and self._dragged_anchor_idx < self._current_path.anchor_count:
```
# 如果存在当前正在绘制的路径

```python
                self._current_path.move_anchor(
```
# 将钢笔工具正在绘制的路径上指定锚点移动到新位置

```python
                    self._dragged_anchor_idx,
```
# move_anchor 参数：self._dragged_anchor_idx 要移动的锚点索引

```python
                    self._current_path.anchors[self._dragged_anchor_idx].x + dx,
```
# move_anchor 参数：锚点原始 x 坐标 + 水平偏移 dx，得到新的 x 坐标

```python
                    self._current_path.anchors[self._dragged_anchor_idx].y + dy,
```
# move_anchor 参数：锚点原始 y 坐标 + 垂直偏移 dy，得到新的 y 坐标

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
            self._ctrl_drag_start = QPointF(pos)
```
# 记录拖拽起始位置到 _ctrl_drag_start

```python
            self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── Space 移动当前锚点（仅在拖拽中） ──
```
# 分隔注释：Space 移动当前锚点（仅在拖拽中） —— 用于视觉分组

```python
        if self._space_moving and self._current_path and self._space_start_pos:
```
# 如果处于 Space 移动模式

```python
            dx = pos.x() - self._space_start_pos.x()
```
# 计算鼠标相对于拖拽起始位置的水平偏移量 dx

```python
            dy = pos.y() - self._space_start_pos.y()
```
# 计算鼠标相对于拖拽起始位置的垂直偏移量 dy

```python
            last_idx = self._current_path.anchor_count - 1
```
# 计算当前路径最后一个锚点的索引（锚点总数 - 1），用于闭合检测和端点锚点操作

```python
            if last_idx >= 0:
```
# 如果命中了锚点/手柄

```python
                anchor = self._current_path.anchors[last_idx]
```
# 获取当前绘制路径的最后一个锚点（端点锚点），用于后续的手柄拖拽或闭合检测

```python
                self._current_path.move_anchor(last_idx, anchor.x + dx, anchor.y + dy)
```
# 将钢笔工具正在绘制的路径上指定锚点移动到新位置

```python
            self._space_start_pos = QPointF(pos)
```
# 记录拖拽起始位置到 _space_start_pos

```python
            self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── 更新悬停光标状态 ──
```
# 分隔注释：更新悬停光标状态 —— 用于视觉分组

```python
        if not self._drawing:
```
# 如果正在绘制中

```python
            self._hover_state = self._detect_hover_state(pos, self._document)
```
# 获取当前缩放手柄对角的固定锚点坐标，作为缩放的固定参照点

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── 拖拽中：实时更新最后一个锚点的手柄 ──
```
# 分隔注释：拖拽中：实时更新最后一个锚点的手柄 —— 用于视觉分组

```python
        if self._drawing and self._drag_start_pos and self._current_path:
```
# 如果正在绘制中

```python
            last_idx = self._current_path.anchor_count - 1
```
# 计算当前路径最后一个锚点的索引（锚点总数 - 1），用于闭合检测和端点锚点操作

```python
            if last_idx >= 0:
```
# 如果命中了锚点/手柄

```python
                dx = pos.x() - self._drag_start_pos.x()
```
# 计算鼠标相对于拖拽起始位置的水平偏移量 dx

```python
                dy = pos.y() - self._drag_start_pos.y()
```
# 计算鼠标相对于拖拽起始位置的垂直偏移量 dy

```python

```
# 空行（代码结构分隔）

```python
                # Shift 约束角度
```
# 注释说明：Shift 约束角度

```python
                if is_shift and (dx != 0 or dy != 0):
```
# 如果按住 Shift 键

```python
                    dx, dy = self._snap_angle(dx, dy)
```
# 将手柄偏移量 `(dx, dy)` 通过 `_snap_angle` 约束到最近的 45° 增量方向（Shift 约束），更新 dx/dy 为约束后的值
```
# 注释说明：拖拽距离小于阈值：视为角点（无手柄）

```python
                dist = math.sqrt(dx*dx + dy*dy)
```
# 计算鼠标与起始锚点之间的欧几里得距离，用于判断是否满足闭合容差条件

```python
                if dist < PenTool.DRAG_THRESHOLD:
```
# 如果满足条件：dist < PenTool.DRAG_THRESHOLD（满足时执行以下逻辑）

```python
                    self._current_path.remove_handles(last_idx)
```
# 移除钢笔工具路径上指定锚点的贝塞尔控制手柄（平滑点→角点）

```python
                else:
```
# 否则（以上条件均不满足时执行）

```python
                    # 创建/更新手柄（平滑点）
```
# 注释说明：创建/更新手柄（平滑点）

```python
                    if is_alt:
```
# 如果按住 Alt 键

```python
                        # Alt 键：仅设置 handle_out（单侧控制），handle_in 置空
```
# 注释说明：Alt 键：仅设置 handle_out（单侧控制），handle_in 置空

```python
                        anchor = self._current_path.anchors[last_idx]
```
# 获取当前路径的最后一个锚点（端点），保存到局部变量 anchor 用于修改手柄方向

```python
                        anchor.handle_out = QPointF(dx, dy)
```
# 设置出方向手柄坐标为 QPointF(rel_x, rel_y)，即鼠标相对于锚点的偏移方向

```python
                        anchor.handle_in = None
```
# 将入方向手柄设为 None：Alt+拖拽时只保留出方向手柄，移除入方向手柄形成不对称控制

```python
                        anchor.anchor_type = AnchorPointType.CORNER
```
#                     将锚点类型强制设为角点

```python
                        self._current_path._build_path()
```
# 根据钢笔工具路径的锚点数据重新构建 QPainterPath 几何路径

```python
                    else:
```
# 否则（以上条件均不满足时执行）

```python
                        # 正常拖拽：创建对称平滑点
```
# 注释说明：正常拖拽：创建对称平滑点

```python
                        self._current_path.set_handle_out(
```
# 设置钢笔工具路径锚点的出方向贝塞尔控制手柄位置

```python
                            last_idx, dx, dy, constrain_smooth=True
```
# 初始化局部变量 last_idx, dx, dy, constrain_smooth 为 True

```python
                        )
```
# 闭合括号：结束函数调用的参数列表

```python

```
# 空行（代码结构分隔）

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行（代码结构分隔）

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# 鼠标释放事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── Ctrl 临时直接选择：释放 ──
```
# 分隔注释：Ctrl 临时直接选择：释放 —— 用于视觉分组

```python
        if self._ctrl_temp_select:
```
# 如果处于 Ctrl 临时选择模式

```python
            self._ctrl_temp_select = False
```
# 重置 Ctrl 临时选择标志

```python
            self._ctrl_drag_start = None
```
# 将Ctrl 临时拖拽起始位置初始化为空值

```python
            self._dragged_anchor_idx = -1
```
# 将拖拽锚点索引初始化为 -1（无效索引）

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        # ── Space 移动锚点：释放 ──
```
# 分隔注释：Space 移动锚点：释放 —— 用于视觉分组

```python
        if self._space_moving:
```
# 如果处于 Space 移动模式

```python
            self._space_moving = False
```
# 重置 Space 移动标志

```python
            self._space_start_pos = None
```
# 将Space 移动起始位置初始化为空值

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        if not self._drawing or self._drag_start_pos is None:
```
# 如果正在绘制中

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        is_alt = bool(modifiers & Qt.AltModifier)
```
# 检测 Alt/Option 键是否按下：用于判断创建不对称锚点（只有 handle_out 的角点）

```python

```
# 空行（代码结构分隔）

```python
        dx = pos.x() - self._drag_start_pos.x()
```
# 计算鼠标相对于拖拽起始位置的水平偏移量 dx

```python
        dy = pos.y() - self._drag_start_pos.y()
```
# 计算鼠标相对于拖拽起始位置的垂直偏移量 dy

```python

```
# 空行（代码结构分隔）

```python
        # Shift 约束角度
```
# 注释说明：Shift 约束角度

```python
        if is_shift and (dx != 0 or dy != 0):
```
# 如果按住 Shift 键

```python
            dx, dy = self._snap_angle(dx, dy)
```
# 将手柄偏移量 `(dx, dy)` 通过 `_snap_angle` 约束到最近的 45° 增量方向（Shift 约束），更新 dx/dy 为约束后的值

```python

```
# 空行（代码结构分隔）

```python
        dist = math.sqrt(dx*dx + dy*dy)
```
# 计算鼠标与起始锚点之间的欧几里得距离，用于判断是否满足闭合容差条件

```python

```
# 空行（代码结构分隔）

```python
        if self._current_path is None:
```
# 如果存在当前正在绘制的路径

```python
            # 不应该到这里
```
# 注释说明：不应该到这里

```python
            self._drawing = False
```
# 将拖拽绘制状态初始化为 False

```python
            self._drag_start_pos = None
```
# 将拖拽起始位置初始化为空值

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        if dist < PenTool.DRAG_THRESHOLD:
```
# 如果满足条件：dist < PenTool.DRAG_THRESHOLD（满足时执行以下逻辑）

```python
            # ── 短拖拽/单击：创建角点（无手柄） ──
```
# 分隔注释：短拖拽/单击：创建角点（无手柄） —— 用于视觉分组

```python
            anchor = AnchorPoint(pos.x(), pos.y(), anchor_type=AnchorPointType.CORNER)
```
# 在鼠标点击位置 `pos` 创建新的角点锚点（CORNER 类型，无方向手柄），保存到局部变量 `anchor`

```python
            self._current_path.add_anchor(anchor)
```
# 向钢笔工具正在绘制的路径末尾追加新锚点

```python
        else:
```
# 否则（以上条件均不满足时执行）

```python
            if is_alt:
```
# 如果按住 Alt 键

```python
                # ── Alt+拖拽：创建不对称点（只有 handle_out） ──
```
# 分隔注释：Alt+拖拽：创建不对称点（只有 handle_out） —— 用于视觉分组

```python
                anchor = AnchorPoint(
```
# 创建新锚点对象 AnchorPoint(mx, my)，保存到局部变量 anchor

```python
                    self._drag_start_pos.x(), self._drag_start_pos.y(),
```
# 获取拖拽起始位置的 x 坐标分量

```python
                    handle_out=QPointF(dx, dy),
```
# 创建出方向手柄坐标 QPointF(rel_x, rel_y)

```python
                    anchor_type=AnchorPointType.CORNER,
```
# 设置锚点类型变量 anchor_type 为 CORNER（角点，无方向手柄）

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
            else:
```
# 否则（以上条件均不满足时执行）

```python
                # ── 正常拖拽：创建平滑点（对称手柄） ──
```
# 分隔注释：正常拖拽：创建平滑点（对称手柄） —— 用于视觉分组

```python
                anchor = AnchorPoint(
```
# 创建新锚点对象 AnchorPoint(mx, my)，保存到局部变量 anchor

```python
                    self._drag_start_pos.x(), self._drag_start_pos.y(),
```
# 获取拖拽起始位置的 x 坐标分量

```python
                    handle_out=QPointF(dx, dy),
```
# 创建出方向手柄坐标 QPointF(rel_x, rel_y)

```python
                    handle_in=QPointF(-dx, -dy),
```
# 创建入方向手柄坐标 QPointF(-rel_x, -rel_y)，方向与 handle_out 相反

```python
                    anchor_type=AnchorPointType.SMOOTH,
```
# 设置锚点类型变量 anchor_type 为 SMOOTH（平滑点，有对称双向手柄）

```python
                )
```
# 闭合括号：结束函数调用的参数列表

```python
            self._current_path.add_anchor(anchor)
```
# 向钢笔工具正在绘制的路径末尾追加新锚点

```python

```
# 空行（代码结构分隔）

```python
        self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python
        self._drawing = False
```
# 将拖拽绘制状态初始化为 False

```python
        self._drag_start_pos = None
```
# 将拖拽起始位置初始化为空值

```python

```
# 空行（代码结构分隔）

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
```
# 鼠标双击事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        """双击结束路径（不闭合）"""
```
# 类/方法文档字符串：双击结束路径（不闭合）

```python
        if self._current_path:
```
# 如果存在当前正在绘制的路径

```python
            self._current_path.closed = False
```
# 将路径的 `closed` 属性设为 False，标记路径为开放式（不闭合）

```python
            self._current_path._build_path()
```
# 根据钢笔工具路径的锚点数据重新构建 QPainterPath 几何路径

```python
            self._current_path = None
```
# 将当前绘制路径初始化为空值

```python
            self._drawing = False
```
# 将拖拽绘制状态初始化为 False

```python
            self._drag_start_pos = None
```
# 将拖拽起始位置初始化为空值

```python

```
# 空行（代码结构分隔）

```python
    # ── 键盘事件 ──
```
# 分隔注释：键盘事件 —— 用于视觉分组

```python

```
# 空行（代码结构分隔）

```python
    def key_press(self, key: int, modifiers: int):
```
# 键盘按键事件处理方法，接收自身引用、按键码：整数、修饰键标志位：整数，无返回值

```python
        if key == Qt.Key_Escape:
```
# 如果满足条件：key == Qt.Key_Escape（满足时执行以下逻辑）

```python
            # Escape：取消当前路径
```
# 注释说明：Escape：取消当前路径

```python
            if self._current_path and self._document:
```
# 如果存在当前正在绘制的路径

```python
                self._document.remove_item(self._current_path)
```
# 从文档中移除指定图形项（同时从图层中删除）

```python
            self._current_path = None
```
# 将当前绘制路径初始化为空值

```python
            self._drawing = False
```
# 将拖拽绘制状态初始化为 False

```python
            self._drag_start_pos = None
```
# 将拖拽起始位置初始化为空值

```python
            self._hover_state = PenTool.PEN_DEFAULT
```
# 重置悬停状态为默认钢笔光标（`PEN_DEFAULT`），表示鼠标不在任何特殊目标上

```python
        elif key in (Qt.Key_Return, Qt.Key_Enter):
```
# elif 分支：按下了 Enter 或 Return 键（Qt.Key_Return / Qt.Key_Enter），用于结束当前正在绘制的路径但不闭合

```python
            # Enter/Return：结束路径（不闭合）
```
# 注释说明：Enter/Return：结束路径（不闭合）

```python
            if self._current_path:
```
# 如果存在当前正在绘制的路径

```python
                self._current_path.closed = False
```
# 将_current_path.closed初始化为 False

```python
                self._current_path._build_path()
```
# 根据钢笔工具路径的锚点数据重新构建 QPainterPath 几何路径

```python
                self._current_path = None
```
# 将当前绘制路径初始化为空值

```python
                self._drawing = False
```
# 将拖拽绘制状态初始化为 False

```python
                self._drag_start_pos = None
```
# 将拖拽起始位置初始化为空值

```python
                self._hover_state = PenTool.PEN_DEFAULT
```
# 重置钢笔光标悬停状态为默认值（标准十字光标）

```python

```
# 空行（代码结构分隔）

```python
    # ── 辅助操作 ──
```
# 分隔注释：辅助操作 —— 用于视觉分组

```python

```
# 空行（代码结构分隔）

```python
    def _close_path(self):
```
# 闭合当前正在绘制的路径，接收自身引用，无返回值

```python
        """闭合当前路径"""
```
# 类/方法文档字符串：闭合当前路径

```python
        if self._current_path and len(self._current_path.anchors) >= 2:
```
# 如果存在当前正在绘制的路径

```python
            self._current_path.closed = True
```
# 将路径的 `closed` 属性设为 True，标记路径为闭合式（首尾锚点相连）

```python
            self._current_path._build_path()
```
# 根据钢笔工具路径的锚点数据重新构建 QPainterPath 几何路径

```python
        self._current_path = None
```
# 将当前绘制路径初始化为空值

```python
        self._drawing = False
```
# 将拖拽绘制状态初始化为 False

```python
        self._drag_start_pos = None
```
# 将拖拽起始位置初始化为空值

```python

```
# 空行（代码结构分隔）

```python
    def _try_delete_anchor(self, pos: QPointF, doc):
```
# 尝试删除悬停位置的锚点，接收自身引用、鼠标位置坐标：二维浮点坐标、文档对象，无返回值

```python
        """尝试删除悬停的锚点（Pen-行为）"""
```
# 类/方法文档字符串：尝试删除悬停的锚点（Pen-行为）

```python
        for layer in reversed(doc.layers):
```
# 逆序遍历文档的图层（从上到下），优先处理顶层可见元素

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in list(layer.items):
```
# 遍历图层中所有图形项的副本列表（避免遍历时修改集合引发错误）

```python
                if not isinstance(item, PathItem) or not item.visible or item.locked:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
```
# 调用 `get_anchor_at` 检测鼠标局部坐标是否命中某个锚点，`anchor_idx` 为命中锚点的索引（≥0 命中，-1 未命中）

```python
                if anchor_idx >= 0 and item.anchor_count > 2:
```
# 条件检查：`anchor_idx >= 0` 鼠标位置命中了某个锚点，`item.anchor_count > 2` 路径至少有 3 个锚点（删除后至少保留 2 个）——同时满足才允许删除

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
# 列表推导式：对路径中每个锚点执行深拷贝，生成操作前的锚点状态快照

```python
                    item.remove_anchor(anchor_idx)
```
# 删除路径的指定锚点，相邻锚点自动连接保持路径连续性

```python
                    new_anchors = [a.copy() for a in item.anchors]
```
# 对每个锚点执行深拷贝，生成锚点列表的副本（避免直接修改原始数据）

```python
                    cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)
```
# 创建 `ModifyAnchorCommand` 撤销命令对象，记录锚点修改前后的状态快照，用于支持 Ctrl+Z 撤销

```python
                    doc.execute_command(cmd)
```
# 通过文档执行命令对象（推入撤销栈，支持 Ctrl+Z）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
    def _try_add_anchor(self, pos: QPointF, doc):
```
# 尝试在路径段上添加新锚点，接收自身引用、鼠标位置坐标：二维浮点坐标、文档对象，无返回值

```python
        """尝试在路径段上添加锚点（Pen+行为）"""
```
# 类/方法文档字符串：尝试在路径段上添加锚点（Pen+行为）

```python
        for layer in reversed(doc.layers):
```
# 逆序遍历文档的图层（从上到下），优先处理顶层可见元素

```python
            if not layer.visible or layer.locked:
```
# 跳过不可见或已锁定的图层

```python
                continue
```
# 跳过当前循环迭代，继续下一个

```python
            for item in list(layer.items):
```
# 遍历图层中所有图形项的副本列表（避免遍历时修改集合引发错误）

```python
                if not isinstance(item, PathItem) or not item.visible or item.locked:
```
# 类型检查：只处理 PathItem 贝塞尔路径类型的图形项

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                seg_idx = item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)
```
# 对当前路径的所有线段调用 `get_segment_at` 检测鼠标局部坐标是否命中某条路径段，`seg_idx` 为命中段的索引（≥0 命中）

```python
                if seg_idx >= 0:
```
# 如果命中了锚点/手柄

```python
                    # 找到段上的精确插入位置
```
# 注释说明：找到段上的精确插入位置

```python
                    cx, cy = item.get_closest_point_on_segment(seg_idx, pos.x(), pos.y())
```
# 在路径段 `seg_idx` 上查找距离鼠标点击位置最近的点，将结果坐标 `(cx, cy)` 作为新锚点的插入位置（精确定位到曲线上的最近点）

```python
                    # 在段后插入新锚点
```
# 注释说明：在段后插入新锚点

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
# 列表推导式：对路径中每个锚点执行深拷贝，生成操作前的锚点状态快照

```python
                    new_anchor = AnchorPoint(cx, cy, anchor_type=AnchorPointType.CORNER)
```
# 使用计算出的坐标 (mx, my) 创建新的角点锚点对象（默认类型为角点，无方向手柄）

```python
                    item.insert_anchor(seg_idx + 1, new_anchor)
```
# 在路径的指定位置插入新锚点（用于钢笔工具和添加锚点工具）

```python
                    new_anchors = [a.copy() for a in item.anchors]
```
# 对每个锚点执行深拷贝，生成锚点列表的副本（避免直接修改原始数据）

```python
                    cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)
```
# 创建 `ModifyAnchorCommand` 撤销命令对象，记录锚点修改前后的状态快照

```python
                    doc.execute_command(cmd)
```
# 通过文档执行命令对象（推入撤销栈，支持 Ctrl+Z）

```python
                    return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
    # ── 绘制预览 ──
```
# 分隔注释：绘制预览方法区域

```python

```
# 空行（代码结构分隔）

```python
    def draw_preview(self, painter: QPainter):
```
# 绘制预览方法，接收自身引用、绘图引擎：绘图引擎，无返回值

```python
        """绘制钢笔工具预览：
```
# 方法文档字符串续行：描述钢笔工具的绘制预览功能

```python
        - 已放置的锚点
```
# 预览内容续行：绘制已放置的所有锚点标记（角点方块/平滑点圆点）

```python
        - 路径线段
```
# 预览内容续行：绘制已完成段之间的贝塞尔路径曲线

```python
        - 拖拽中的手柄预览
```
# 预览内容续行：绘制当前正在拖拽的贝塞尔方向手柄线

```python
        - 悬停光标指示
```
# 预览内容续行：绘制鼠标悬停目标（锚点/路径段）的高亮指示

```python
        """
```
# 三引号字符串结束 —— 模块文档字符串至此闭合

```python
        if not self._current_path:
```
# 如果存在当前正在绘制的路径

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        anchors = self._current_path.anchors
```
# 获取当前绘制路径的所有锚点列表，用于检查路径是否满足闭合条件（至少 2 个锚点）

```python
        if not anchors:
```
# 如果路径没有任何锚点（`not anchors` 为 True），则无法执行删除操作，提前返回

```python
            return
```
#         提前返回，不执行后续逻辑

```python

```
# 空行（代码结构分隔）

```python
        scale = max(painter.transform().m11(), 0.001)
```
#         获取画布缩放比例

```python

```
# 空行（代码结构分隔）

```python
        # ── 绘制已放置的锚点 ──
```
# 分隔注释：绘制已放置的锚点 —— 用于视觉分组

```python
        for i, anchor in enumerate(anchors):
```
# 带索引遍历锚点列表，i为当前锚点序号，anchor为锚点对象

```python
            pt = QPointF(anchor.x, anchor.y)
```
# 将锚点的局部坐标 `(anchor.x, anchor.y)` 封装为 QPointF 坐标点 `pt`，作为绘制锚点圆圈和手柄线的基准位置

```python

```
# 空行（代码结构分隔）

```python
            # 锚点圆圈
```
# 注释说明：锚点圆圈

```python
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
            painter.setBrush(QColor(255, 255, 255))
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
            painter.drawEllipse(pt, 3 / scale, 3 / scale)
```
# 在指定矩形内绘制内切椭圆（用于锚点和手柄端点的圆形表示）

```python

```
# 空行（代码结构分隔）

```python
            # 手柄线（handle_in）
```
# 注释说明：手柄线（handle_in）

```python
            if anchor.handle_in:
```
# 如果锚点有入方向手柄

```python
                hin = QPointF(anchor.x + anchor.handle_in.x(), 
```
# 创建入方向手柄坐标点 QPointF(-rel_x, -rel_y)

```python
                             anchor.y + anchor.handle_in.y())
```
# 计算入方向手柄端点的 y 坐标：锚点 y + 手柄相对偏移 y

```python
                pen = QPen(QColor(0, 120, 215), 0.8 / scale)
```
# 创建蓝色画笔对象 `pen`：颜色 AI 蓝 (0,120,215)，线宽 0.8/scale，用于绘制入方向手柄连线

```python
                pen.setStyle(Qt.DashLine)
```
# 设置画笔的线条样式（实线/虚线/点线等），用于贝塞尔手柄线的虚线表示

```python
                painter.setPen(pen)
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
                painter.drawLine(pt, hin)
```
# 绘制从起点到终点的线段（使用当前画笔样式）

```python
                # 手柄端点
```
# 注释说明：手柄端点

```python
                painter.setBrush(QColor(255, 255, 255))
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
                painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
                painter.drawEllipse(hin, 2.5 / scale, 2.5 / scale)
```
# 在指定矩形内绘制内切椭圆（用于锚点和手柄端点的圆形表示）

```python

```
# 空行（代码结构分隔）

```python
            # 手柄线（handle_out）
```
# 注释说明：手柄线（handle_out）

```python
            if anchor.handle_out:
```
# 如果锚点有出方向手柄

```python
                hout = QPointF(anchor.x + anchor.handle_out.x(), 
```
# 创建出方向手柄坐标点 QPointF(rel_x, rel_y)

```python
                              anchor.y + anchor.handle_out.y())
```
# 计算出方向手柄端点的 y 坐标：锚点 y + 手柄相对偏移 y

```python
                painter.setPen(QPen(QColor(0, 120, 215), 0.8 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
                painter.drawLine(pt, hout)
```
# 绘制从起点到终点的线段（使用当前画笔样式）

```python
                # 手柄端点
```
# 注释说明：手柄端点

```python
                painter.setBrush(QColor(255, 255, 255))
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
                painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
                painter.drawEllipse(hout, 2.5 / scale, 2.5 / scale)
```
# 在指定矩形内绘制内切椭圆（用于锚点和手柄端点的圆形表示）

```python

```
# 空行（代码结构分隔）

```python
        # ── 绘制路径线段 ──
```
# 分隔注释：绘制路径线段 —— 用于视觉分组

```python
        if len(anchors) >= 2:
```
# 如果满足条件：len(anchors) >= 2（满足时执行以下逻辑）

```python
            pen = QPen(QColor(0, 120, 215), 1.5 / scale)
```
# 创建画笔对象用于绘制文本框预览边框（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
            painter.setBrush(Qt.NoBrush)
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python

```
# 空行（代码结构分隔）

```python
            for i in range(len(anchors) - 1):
```
# 按索引遍历锚点间的线段，范围0到倒数第二个锚点，用于绘制路径线段

```python
                prev, curr = anchors[i], anchors[i + 1]
```
# 提取相邻的两个锚点 `prev`（索引 i）和 `curr`（索引 i+1），构成要检测/操作的贝塞尔曲线段

```python
                samples = PathItem._sample_bezier_segment(prev, curr, num_samples=30)
```
# 对相邻锚点 `prev→curr` 构成的贝塞尔曲线段进行 30 次均匀采样，生成 `samples` 坐标列表，用于逐段绘制平滑的路径曲线预览

```python
                for k in range(len(samples) - 1):
```
# 按索引遍历采样点间的线段，用于绘制平滑的路径预览

```python
                    p1 = QPointF(samples[k][0], samples[k][1])
```
# 将贝塞尔采样点列表中第 k 个采样坐标封装为 QPointF 坐标点 `p1`，作为路径线段的起点

```python
                    p2 = QPointF(samples[k+1][0], samples[k+1][1])
```
# 将贝塞尔采样点列表中第 k+1 个采样坐标封装为 QPointF 坐标点 `p2`，作为路径线段的终点

```python
                    painter.drawLine(p1, p2)
```
# 绘制从起点到终点的线段（使用当前画笔样式）

```python

```
# 空行（代码结构分隔）

```python
        # ── 拖拽中：绘制从最后一个锚点出发的预览手柄 ──
```
# 分隔注释：拖拽中：绘制从最后一个锚点出发的预览手柄 —— 用于视觉分组

```python
        if self._drawing and self._drag_start_pos:
```
# 如果正在绘制中

```python
            last_anchor = anchors[-1]
```
# 获取路径锚点列表的最后一个锚点（即当前绘制路径的端点）

```python
            last_pt = QPointF(last_anchor.x, last_anchor.y)
```
# 将最后一个锚点的世界坐标保存到 last_pt（用于闭合路径计算）

```python

```
# 空行（代码结构分隔）

```python
            # 手柄线预览
```
# 注释说明：手柄线预览

```python
            painter.setPen(QPen(QColor(0, 120, 215, 150), 0.8 / scale, Qt.DashLine))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
            painter.drawLine(last_pt, self._drag_start_pos)
```
# 绘制从起点到终点的线段（使用当前画笔样式）

```python

```
# 空行（代码结构分隔）

```python
            # 预览锚点
```
# 注释说明：预览锚点

```python
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
            painter.setBrush(QColor(0, 120, 215, 100))
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
            painter.drawEllipse(self._drag_start_pos, 3 / scale, 3 / scale)
```
# 在指定矩形内绘制内切椭圆（用于锚点和手柄端点的圆形表示）

```python

```
# 空行（代码结构分隔）

```python
        # ── 悬停光标指示（在第一个锚点上绘制闭合图标） ──
```
# 分隔注释：悬停光标指示（在第一个锚点上绘制闭合图标） —— 用于视觉分组

```python
        if self._hover_state == PenTool.PEN_CLOSE and len(anchors) >= 2:
```
# 如果悬停状态为闭合路径

```python
            first_pt = QPointF(anchors[0].x, anchors[0].y)
```
# 将第一个锚点的世界坐标保存到 first_pt（用于闭合路径计算）

```python
            painter.setPen(QPen(QColor(0, 120, 215), 2 / scale))
```
# 设置画笔样式（颜色、线宽、虚实线类型），用于后续的描边绘制

```python
            painter.setBrush(Qt.NoBrush)
```
# 设置画刷样式（填充颜色、填充图案），用于后续的填充绘制

```python
            r = 6 / scale
```
# 计算手柄端点的显示半径：基础 6px 除以缩放比例，保证不同缩放级别下视觉大小一致

```python
            painter.drawEllipse(first_pt, r, r)
```
# 在指定矩形内绘制内切椭圆（用于锚点和手柄端点的圆形表示）

```python

```
# 空行（代码结构分隔）

```python
    def cancel(self):
```
# 取消当前操作并重置状态，接收自身引用，无返回值

```python
        if self._current_path and self._document:
```
# 如果存在当前正在绘制的路径

```python
            self._document.remove_item(self._current_path)
```
# 从文档中移除指定图形项（同时从图层中删除）

```python
        self._current_path = None
```
# 将当前绘制路径初始化为空值

```python
        self._drawing = False
```
# 将拖拽绘制状态初始化为 False

```python
        self._drag_start_pos = None
```
# 将拖拽起始位置初始化为空值

```python
        self._hover_state = PenTool.PEN_DEFAULT
```
# 重置钢笔光标悬停状态为默认值（标准十字光标）

```python
        self._ctrl_temp_select = False
```
# 重置 Ctrl 临时选择标志

```python
        self._space_moving = False
```
# 重置 Space 移动标志

```python
        super().cancel()
```
#         调用父类 cancel() 重置基类状态

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
# ── 文字工具 ──────────────────────────────────────────────
```
# 分隔注释：文字工具 —— 用于视觉分组

```python

```
# 空行（代码结构分隔）

```python
class TextTool(BaseTool):
```
# 定义 `TextTool` 文字工具类：继承 `BaseTool`，点击画布创建文字框

```python
    """文字工具 —— 点击创建文字"""
```
# 类/方法文档字符串：文字工具 —— 点击创建文字

```python
    __slots__ = ()
```
#     空槽位（无额外属性）

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self):
```
# 初始化方法（构造函数），接收自身引用，无返回值

```python
        super().__init__(ToolType.TEXT)
```
#         调用父类构造函数，传入文字工具类型

```python

```
# 空行（代码结构分隔）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# 鼠标按下事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        if not self._document:
```
#         如果工具未关联文档，则不处理

```python
            return
```
#         提前返回，不执行后续逻辑

```python
        text_frame = TextFrame(pos.x(), pos.y())
```
# 创建 TextFrame 文字框实例，传入矩形区域的坐标和尺寸

```python
        text_frame.contents = "文字"
```
# 设置文字框的内容为 "文字"（创建文字工具时的默认占位文本）

```python
        text_frame.char_attrs.font_size = 24
```
# 设置文字框的默认字号为 24pt

```python
        text_frame.char_attrs.fill_color = QColor(50, 50, 50)
```
# 设置文字框的默认文字填充颜色

```python
        text_frame.style.fill_color = None
```
# 将文字框的填充颜色设为 None（透明），文字框默认不绘制背景填充

```python
        text_frame.selected = True
```
# 将文字框设为选中状态（创建后自动选中，方便用户立即编辑内容）

```python
        self._document.clear_selection()
```
#                     清除文档中所有图形项的选中状态

```python
        self._document.add_item(text_frame)
```
# 将新创建的图形项添加到文档的当前活动图层中

```python
        self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行（代码结构分隔）

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
```
# 鼠标双击事件处理方法，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

```python
        pass  # 由 UI 层处理
```
# pass 空实现：文字内容的编辑操作由 UI 层（文字编辑器组件）处理，工具层不干预

```python

```
# 空行（代码结构分隔）

```python

```
# 空行（代码结构分隔）

```python
# ── 抓手工具 ──────────────────────────────────────────────
```
# 分隔注释：抓手工具 —— 用于视觉分组

```python

```
# 空行（代码结构分隔）

```python
class HandTool(BaseTool):
```
# 定义 `HandTool` 抓手工具类：继承 `BaseTool`，拖拽平移画布视图

```python
    """抓手工具 —— 拖拽平移画布"""
```
# 类/方法文档字符串：抓手工具 —— 拖拽平移画布

```python
    __slots__ = ()
```
#     空槽位（无额外属性）

```python

```
# 空行（代码结构分隔）

```python
    def __init__(self):
```
# 初始化方法（构造函数），接收自身引用，无返回值

```python
        super().__init__(ToolType.HAND)
```
#         调用父类构造函数，传入抓手工具类型

