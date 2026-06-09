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
# 三引号字符串开始 —— 模块文档字符串

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
# 三引号字符串开始 —— 模块文档字符串

```python

```
# 空行

```python
from __future__ import annotations
```
# 导入 `annotations` 特性：使类型注解在运行时惰性求值，支持前向引用和避免循环导入

```python

```
# 空行

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
# 空行

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
# 空行

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
# 空行

```python

```
# 空行

```python
class ToolType(Enum):
```
# 定义 `ToolType` 枚举类：为所有可用工具提供唯一类型标识符，使用 `auto()` 自动分配值

```python
    """工具类型"""
```
# """工具类型"""

```python
    SELECTION = auto()              # 选择工具 (V)
```
# SELECTION = auto()              # 选择工具 (V)

```python
    DIRECT_SELECT = auto()          # 直接选择工具 (A)
```
# DIRECT_SELECT = auto()          # 直接选择工具 (A)

```python
    RECTANGLE = auto()              # 矩形工具 (M)
```
# RECTANGLE = auto()              # 矩形工具 (M)

```python
    ELLIPSE = auto()                # 椭圆工具 (L)
```
# ELLIPSE = auto()                # 椭圆工具 (L)

```python
    PEN = auto()                    # 钢笔工具 (P)
```
# PEN = auto()                    # 钢笔工具 (P)

```python
    ADD_ANCHOR = auto()             # 添加锚点工具 (+)
```
# ADD_ANCHOR = auto()             # 添加锚点工具 (+)

```python
    DELETE_ANCHOR = auto()          # 删除锚点工具 (-)
```
# DELETE_ANCHOR = auto()          # 删除锚点工具 (-)

```python
    CONVERT_ANCHOR = auto()         # 转换锚点工具 (Shift+C)
```
# CONVERT_ANCHOR = auto()         # 转换锚点工具 (Shift+C)

```python
    TEXT = auto()                   # 文字工具 (T)
```
# TEXT = auto()                   # 文字工具 (T)

```python
    HAND = auto()                   # 抓手工具 (H)
```
# HAND = auto()                   # 抓手工具 (H)

```python
    ZOOM = auto()                   # 缩放工具 (Z)
```
# ZOOM = auto()                   # 缩放工具 (Z)

```python

```
# 空行

```python

```
# 空行

```python
class BaseTool(ABC):
```
# 定义工具抽象基类 `BaseTool`，继承 `ABC`：为所有具体工具提供统一的鼠标/键盘/绘制事件接口

```python
    """工具基类（抽象）"""
```
# """工具基类（抽象）"""

```python
    __slots__ = ('tool_type', '_document', '_is_drawing')
```
# __slots__ = ('tool_type', '_document', '_is_drawing')

```python

```
# 空行

```python
    def __init__(self, tool_type: ToolType):
```
# def __init__(self, tool_type: ToolType):

```python
        self.tool_type = tool_type
```
# self.tool_type = tool_type

```python
        self._document: Document | None = None
```
# self._document: Document | None = None

```python
        self._is_drawing: bool = False
```
# self._is_drawing: bool = False

```python

```
# 空行

```python
    def set_document(self, doc: Document):
```
# def set_document(self, doc: Document):

```python
        self._document = doc
```
# self._document = doc

```python

```
# 空行

```python
    @property
```
# @property

```python
    def document(self) -> Document | None:
```
# def document(self) -> Document | None:

```python
        return self._document
```
# return self._document

```python

```
# 空行

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# def mouse_press(self, pos: QPointF, modifiers: int):

```python
        pass
```
# pass

```python

```
# 空行

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# def mouse_move(self, pos: QPointF, modifiers: int):

```python
        pass
```
# pass

```python

```
# 空行

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# def mouse_release(self, pos: QPointF, modifiers: int):

```python
        pass
```
# pass

```python

```
# 空行

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
```
# def mouse_double_click(self, pos: QPointF, modifiers: int):

```python
        pass
```
# pass

```python

```
# 空行

```python
    def key_press(self, key: int, modifiers: int):
```
# def key_press(self, key: int, modifiers: int):

```python
        pass
```
# pass

```python

```
# 空行

```python
    def draw_preview(self, painter: QPainter):
```
# def draw_preview(self, painter: QPainter):

```python
        pass
```
# pass

```python

```
# 空行

```python
    def cancel(self):
```
# def cancel(self):

```python
        self._is_drawing = False
```
# self._is_drawing = False

```python

```
# 空行

```python

```
# 空行

```python
# ── 缩放手柄类型 ───────────────────────────────────────────
```
# 分隔注释：缩放手柄类型 ─ —— 用于视觉分组

```python

```
# 空行

```python
class ResizeHandleType(Enum):
```
# 定义 `ResizeHandleType` 枚举：标识选择工具缩放手柄的 8 个位置（四角 + 四边中点）

```python
    """缩放手柄位置类型"""
```
# """缩放手柄位置类型"""

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
# 空行

```python

```
# 空行

```python
# ── 选择工具 ──────────────────────────────────────────────
```
# 分隔注释：选择工具 —— 用于视觉分组

```python

```
# 空行

```python
class SelectionTool(BaseTool):
```
# 定义 `SelectionTool` 选择工具类：继承 `BaseTool`，实现点击选择、框选、多选拖拽、缩放手柄

```python
    """选择工具 —— 点击选择 / 框选 / 多选拖拽 / 缩放手柄"""
```
# """选择工具 —— 点击选择 / 框选 / 多选拖拽 / 缩放手柄"""

```python
    __slots__ = ('_drag_start', '_drag_current', '_dragging_item',
```
# __slots__ = ('_drag_start', '_drag_current', '_dragging_item',

```python
                 '_drag_offset', '_is_marquee',
```
# '_drag_offset', '_is_marquee',

```python
                 '_dragging_items', '_drag_offsets',
```
# '_dragging_items', '_drag_offsets',

```python
                 '_total_dx', '_total_dy',
```
# '_total_dx', '_total_dy',

```python
                 '_is_scaling', '_scale_handle',
```
# '_is_scaling', '_scale_handle',

```python
                 '_scale_orig_rect', '_scale_orig_br',
```
# '_scale_orig_rect', '_scale_orig_br',

```python
                 '_scale_pivot', '_scale_keep_ratio')
```
# '_scale_pivot', '_scale_keep_ratio')

```python

```
# 空行

```python
    def __init__(self):
```
# def __init__(self):

```python
        super().__init__(ToolType.SELECTION)
```
# super().__init__(ToolType.SELECTION)

```python
        self._drag_start: QPointF | None = None
```
# self._drag_start: QPointF | None = None

```python
        self._drag_current: QPointF | None = None
```
# self._drag_current: QPointF | None = None

```python
        self._dragging_item: GraphicItem | None = None
```
# self._dragging_item: GraphicItem | None = None

```python
        self._drag_offset = QPointF(0, 0)
```
# self._drag_offset = QPointF(0, 0)

```python
        self._is_marquee: bool = False
```
# self._is_marquee: bool = False

```python
        # 多选拖拽支持
```
# 源代码注释：多选拖拽支持

```python
        self._dragging_items: list[GraphicItem] = []
```
# self._dragging_items: list[GraphicItem] = []

```python
        self._drag_offsets: list[QPointF] = []
```
# self._drag_offsets: list[QPointF] = []

```python
        self._total_dx: float = 0.0
```
# self._total_dx: float = 0.0

```python
        self._total_dy: float = 0.0
```
# self._total_dy: float = 0.0

```python
        # 缩放支持
```
# 源代码注释：缩放支持

```python
        self._is_scaling: bool = False
```
# self._is_scaling: bool = False

```python
        self._scale_handle: ResizeHandleType | None = None
```
# self._scale_handle: ResizeHandleType | None = None

```python
        self._scale_orig_rect = QRectF()
```
# self._scale_orig_rect = QRectF()

```python
        self._scale_orig_br = QRectF()  # 缩放前 bounding_rect
```
# self._scale_orig_br = QRectF()  # 缩放前 bounding_rect

```python
        self._scale_pivot = QPointF()   # 缩放锚点（对角的那个固定点）
```
# self._scale_pivot = QPointF()   # 缩放锚点（对角的那个固定点）

```python
        self._scale_keep_ratio: bool = False
```
# self._scale_keep_ratio: bool = False

```python

```
# 空行

```python
    # ── 手柄检测 ──
```
# 分隔注释：手柄检测 —— 用于视觉分组

```python

```
# 空行

```python
    @staticmethod
```
# @staticmethod

```python
    def _get_handle_at(item: GraphicItem, pos: QPointF, tolerance: float = 8) -> ResizeHandleType | None:
```
# 定义 `_get_handle_at` 静态方法：检测鼠标 `pos`（世界坐标）是否在 `item` 的缩放手柄上，容差 `tolerance` 默认 8px，返回手柄类型或 None

```python
        """检测鼠标是否在缩放手柄上（pos 为世界坐标）"""
```
# 文档字符串：说明 pos 为世界坐标（非局部坐标）

```python
        local_rect = item.bounding_rect()
```
# local_rect = item.bounding_rect()

```python
        rect = item._transform.mapRect(local_rect)
```
# rect = item._transform.mapRect(local_rect)

```python
        hs = tolerance  # 手柄命中容差
```
# hs = tolerance  # 手柄命中容差

```python
        corners = {
```
# corners = {

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
# }

```python
        edges = {
```
# edges = {

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
# }

```python

```
# 空行

```python
        for htype, pt in corners.items():
```
# 遍历四角手柄字典：`htype` 手柄类型、`pt` 对应角点坐标

```python
            if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:
```
# if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:

```python
                return htype
```
# return htype

```python
        for htype, pt in edges.items():
```
# 遍历四边中点手柄字典：角手柄未命中时继续检测边手柄

```python
            if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:
```
# if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:

```python
                return htype
```
# return htype

```python
        return None
```
# 所有 8 个手柄都未命中，返回 None

```python

```
# 空行

```python
    # ── 鼠标事件 ──
```
# 分隔注释：鼠标事件 —— 用于视觉分组

```python

```
# 空行

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# def mouse_press(self, pos: QPointF, modifiers: int):

```python
        if not self._document:
```
# if not self._document:

```python
            return
```
# 提前返回，不再继续后续检测

```python
        self._drag_start = QPointF(pos)
```
# 更新拖拽起始点为当前位置

```python
        self._drag_current = QPointF(pos)
```
# self._drag_current = QPointF(pos)

```python
        self._total_dx = 0.0
```
# self._total_dx = 0.0

```python
        self._total_dy = 0.0
```
# self._total_dy = 0.0

```python
        self._is_scaling = False
```
# self._is_scaling = False

```python
        self._scale_handle = None
```
# self._scale_handle = None

```python
        self._scale_keep_ratio = bool(modifiers & Qt.ShiftModifier)
```
# self._scale_keep_ratio = bool(modifiers & Qt.ShiftModifier)

```python

```
# 空行

```python
        # 检查是否点击了已选中项的缩放手柄
```
# 源代码注释：检查是否点击了已选中项的缩放手柄

```python
        sel = self._document.get_selection()
```
# sel = self._document.get_selection()

```python
        if len(sel) == 1:
```
# if len(sel) == 1:

```python
            handle = self._get_handle_at(sel[0], pos)
```
# handle = self._get_handle_at(sel[0], pos)

```python
            if handle is not None:
```
# if handle is not None:

```python
                self._dragging_item = sel[0]
```
# self._dragging_item = sel[0]

```python
                self._is_scaling = True
```
# self._is_scaling = True

```python
                self._scale_handle = handle
```
# self._scale_handle = handle

```python
                # 使用世界坐标系的 bounding_rect（含 item 变换）
```
# 源代码注释：使用世界坐标系的 bounding_rect（含 item 变换）

```python
                world_rect = sel[0]._transform.mapRect(sel[0].bounding_rect())
```
# world_rect = sel[0]._transform.mapRect(sel[0].bounding_rect())

```python
                self._scale_orig_rect = QRectF(world_rect)
```
# self._scale_orig_rect = QRectF(world_rect)

```python
                self._scale_orig_br = QRectF(world_rect)
```
# self._scale_orig_br = QRectF(world_rect)

```python
                # 缩放的固定锚点是对角
```
# 源代码注释：缩放的固定锚点是对角

```python
                self._scale_pivot = self._get_opposite_corner(handle, self._scale_orig_rect)
```
# self._scale_pivot = self._get_opposite_corner(handle, self._scale_orig_rect)

```python
                return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        item = self._document.get_item_at(pos.x(), pos.y())
```
# 通过文档查找鼠标位置下的最顶层图形项

```python
        if item:
```
# if item:

```python
            self._is_marquee = False  # 点击了物体，不是框选
```
# 设置框选标志为 False

```python
            # 如果点击的项未被选中，先清除选择并选中它
```
# 源代码注释：如果点击的项未被选中，先清除选择并选中它

```python
            if not item.selected:
```
# 检查图形项是否已被选中

```python
                if not (modifiers & Qt.ShiftModifier):
```
# if not (modifiers & Qt.ShiftModifier):

```python
                    self._document.clear_selection()
```
# 调用文档方法清除所有图形项的选中状态

```python
                item.selected = True
```
# 将当前图形项设为选中状态

```python

```
# 空行

```python
            # 准备拖拽
```
# 源代码注释：准备拖拽

```python
            sel = self._document.get_selection()
```
# sel = self._document.get_selection()

```python
            if len(sel) > 1:
```
# if len(sel) > 1:

```python
                # 多选状态 → 多选拖拽模式
```
# 源代码注释：多选状态 → 多选拖拽模式

```python
                self._dragging_items = list(sel)
```
# self._dragging_items = list(sel)

```python
                self._drag_offsets = [pos - it._transform.mapRect(it.bounding_rect()).topLeft() for it in sel]
```
# self._drag_offsets = [pos - it._transform.mapRect(it.bounding_rect()).topLeft() for it in sel]

```python
                self._dragging_item = None
```
# 清空被拖拽图形项

```python
            else:
```
# else:

```python
                # 单选或仅选中了一项 → 单项拖拽（不要清除再重新选中）
```
# 源代码注释：单选或仅选中了一项 → 单项拖拽（不要清除再重新选中）

```python
                self._dragging_item = item
```
# 设置当前图形项为被拖拽项

```python
                self._drag_offset = pos - item._transform.mapRect(item.bounding_rect()).topLeft()
```
# self._drag_offset = pos - item._transform.mapRect(item.bounding_rect()).topLeft()

```python
                self._dragging_items = []
```
# 清空多选拖拽列表

```python
        else:
```
# else:

```python
            if not (modifiers & Qt.ShiftModifier):
```
# if not (modifiers & Qt.ShiftModifier):

```python
                self._document.clear_selection()
```
# 调用文档方法清除所有图形项的选中状态

```python
            self._dragging_item = None
```
# 清空被拖拽图形项

```python
            self._dragging_items = []
```
# 清空多选拖拽列表

```python
            self._is_marquee = True
```
# 设置框选标志为 True

```python

```
# 空行

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# def mouse_move(self, pos: QPointF, modifiers: int):

```python
        if self._drag_start is None:
```
# if self._drag_start is None:

```python
            return
```
# 提前返回，不再继续后续检测

```python
        self._drag_current = QPointF(pos)
```
# self._drag_current = QPointF(pos)

```python

```
# 空行

```python
        # 缩放模式
```
# 源代码注释：缩放模式

```python
        if self._is_scaling and self._dragging_item:
```
# if self._is_scaling and self._dragging_item:

```python
            self._apply_resize(pos, bool(modifiers & Qt.ShiftModifier))
```
# self._apply_resize(pos, bool(modifiers & Qt.ShiftModifier))

```python
            if self._document:
```
# if self._document:

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        dx = pos.x() - self._drag_start.x()
```
# dx = pos.x() - self._drag_start.x()

```python
        dy = pos.y() - self._drag_start.y()
```
# dy = pos.y() - self._drag_start.y()

```python
        # Shift 约束水平/垂直移动
```
# 源代码注释：Shift 约束水平/垂直移动

```python
        if modifiers & Qt.ShiftModifier:
```
# if modifiers & Qt.ShiftModifier:

```python
            dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)
```
# dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)

```python

```
# 空行

```python
        if self._dragging_items:
```
# if self._dragging_items:

```python
            for item in self._dragging_items:
```
# for item in self._dragging_items:

```python
                item.move_by(dx, dy)
```
# item.move_by(dx, dy)

```python
            self._total_dx += dx
```
# self._total_dx += dx

```python
            self._total_dy += dy
```
# self._total_dy += dy

```python
            self._drag_start = QPointF(pos)
```
# 更新拖拽起始点为当前位置

```python
            if self._document:
```
# if self._document:

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python
        elif self._dragging_item and not self._is_scaling:
```
# elif self._dragging_item and not self._is_scaling:

```python
            self._dragging_item.move_by(dx, dy)
```
# self._dragging_item.move_by(dx, dy)

```python
            self._total_dx += dx
```
# self._total_dx += dx

```python
            self._total_dy += dy
```
# self._total_dy += dy

```python
            self._drag_start = QPointF(pos)
```
# 更新拖拽起始点为当前位置

```python
            if self._document:
```
# if self._document:

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# def mouse_release(self, pos: QPointF, modifiers: int):

```python
        # 缩放完成：记录命令（通过 execute_command 统一入口）
```
# 源代码注释：缩放完成：记录命令（通过 execute_command 统一入口）

```python
        if self._is_scaling and self._dragging_item and self._document:
```
# if self._is_scaling and self._dragging_item and self._document:

```python
            new_world_rect = self._dragging_item._transform.mapRect(self._dragging_item.bounding_rect())
```
# new_world_rect = self._dragging_item._transform.mapRect(self._dragging_item.bounding_rect())

```python
            if new_world_rect != self._scale_orig_br:
```
# if new_world_rect != self._scale_orig_br:

```python
                # 通过尺寸变化记录（使用世界坐标矩形）
```
# 源代码注释：通过尺寸变化记录（使用世界坐标矩形）

```python
                cmd = ResizeItemCommand(
```
# cmd = ResizeItemCommand(

```python
                    self._document, self._dragging_item,
```
# self._document, self._dragging_item,

```python
                    self._scale_orig_br, new_world_rect,
```
# self._scale_orig_br, new_world_rect,

```python
                )
```
# 导入结束括号

```python
                self._document.execute_command(cmd)
```
# self._document.execute_command(cmd)

```python
            self._is_scaling = False
```
# self._is_scaling = False

```python
            self._scale_handle = None
```
# self._scale_handle = None

```python
            self._dragging_item = None
```
# 清空被拖拽图形项

```python
            self._drag_start = None
```
# 清空拖拽起始点

```python
            self._drag_current = None
```
# self._drag_current = None

```python
            self._total_dx = 0.0
```
# self._total_dx = 0.0

```python
            self._total_dy = 0.0
```
# self._total_dy = 0.0

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # 多选拖拽完成后记录移动命令（用于撤销，通过 execute_command 统一入口）
```
# 源代码注释：多选拖拽完成后记录移动命令（用于撤销，通过 execute_command 统一入口）

```python
        moved_items = self._dragging_items if self._dragging_items else (
```
# moved_items = self._dragging_items if self._dragging_items else (

```python
            [self._dragging_item] if self._dragging_item else []
```
# [self._dragging_item] if self._dragging_item else []

```python
        )
```
# 导入结束括号

```python
        if moved_items and self._document and (self._total_dx != 0 or self._total_dy != 0):
```
# if moved_items and self._document and (self._total_dx != 0 or self._total_dy != 0):

```python
            cmd = MoveItemsCommand(
```
# cmd = MoveItemsCommand(

```python
                self._document, moved_items,
```
# self._document, moved_items,

```python
                self._total_dx, self._total_dy,
```
# self._total_dx, self._total_dy,

```python
            )
```
# 导入结束括号

```python
            self._document.execute_command(cmd)
```
# self._document.execute_command(cmd)

```python

```
# 空行

```python
        if self._is_marquee and self._drag_start and self._document:
```
# if self._is_marquee and self._drag_start and self._document:

```python
            rect = QRectF(self._drag_start, pos).normalized()
```
# rect = QRectF(self._drag_start, pos).normalized()

```python
            if rect.width() > 2 and rect.height() > 2:
```
# if rect.width() > 2 and rect.height() > 2:

```python
                for layer in self._document.layers:
```
# for layer in self._document.layers:

```python
                    items = layer.get_items_in_rect(
```
# items = layer.get_items_in_rect(

```python
                        rect.x(), rect.y(), rect.width(), rect.height(),
```
# rect.x(), rect.y(), rect.width(), rect.height(),

```python
                    )
```
# 导入结束括号

```python
                    for item in items:
```
# for item in items:

```python
                        item.selected = True
```
# 将当前图形项设为选中状态

```python

```
# 空行

```python
        self._drag_start = None
```
# 清空拖拽起始点

```python
        self._drag_current = None
```
# self._drag_current = None

```python
        self._dragging_item = None
```
# 清空被拖拽图形项

```python
        self._dragging_items = []
```
# 清空多选拖拽列表

```python
        self._is_marquee = False
```
# 设置框选标志为 False

```python
        self._is_scaling = False
```
# self._is_scaling = False

```python
        self._scale_handle = None
```
# self._scale_handle = None

```python
        self._total_dx = 0.0
```
# self._total_dx = 0.0

```python
        self._total_dy = 0.0
```
# self._total_dy = 0.0

```python

```
# 空行

```python
    # ── 缩放核心 ──
```
# 分隔注释：缩放核心 —— 用于视觉分组

```python

```
# 空行

```python
    @staticmethod
```
# @staticmethod

```python
    def _get_opposite_corner(handle: ResizeHandleType, rect: QRectF) -> QPointF:
```
# 定义 `_get_opposite_corner` 静态方法：根据手柄类型 `handle` 和矩形 `rect`，返回对角的固定锚点坐标

```python
        """获取缩放手柄对面的固定锚点"""
```
# 文档字符串：获取缩放手柄对面（对角）的固定锚点位置

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
# 空行

```python
    def _apply_resize(self, mouse_pos: QPointF, keep_ratio: bool):
```
# 定义 `_apply_resize` 方法：根据手柄类型和鼠标位置实时调整图形大小

```python
        """根据手柄类型和鼠标位置调整图形大小"""
```
# 文档字符串：说明此方法根据手柄类型和鼠标位置实时调整图形项大小

```python
        if not self._dragging_item:
```
# if not self._dragging_item:

```python
            return
```
# 提前返回，不再继续后续检测

```python
        pivot = self._scale_pivot
```
# pivot = self._scale_pivot

```python
        orig = self._scale_orig_rect
```
# orig = self._scale_orig_rect

```python
        mx, my = mouse_pos.x(), mouse_pos.y()
```
# mx, my = mouse_pos.x(), mouse_pos.y()

```python
        px, py = pivot.x(), pivot.y()
```
# px, py = pivot.x(), pivot.y()

```python

```
# 空行

```python
        # 根据手柄确定新宽高
```
# 源代码注释：根据手柄确定新宽高

```python
        match self._scale_handle:
```
# match self._scale_handle:

```python
            case ResizeHandleType.TOP_LEFT:
```
#   左上角手柄的对角固定锚点 → 右下角 `rect.bottomRight()`

```python
                new_w, new_h = px - mx, py - my
```
# new_w, new_h = px - mx, py - my

```python
            case ResizeHandleType.TOP_CENTER:
```
#   上边中点手柄的对角固定锚点 → 底边中点

```python
                new_w = orig.width()
```
# new_w = orig.width()

```python
                new_h = py - my
```
# new_h = py - my

```python
            case ResizeHandleType.TOP_RIGHT:
```
#   右上角手柄的对角固定锚点 → 左下角 `rect.bottomLeft()`

```python
                new_w = mx - px
```
# new_w = mx - px

```python
                new_h = py - my
```
# new_h = py - my

```python
            case ResizeHandleType.MIDDLE_LEFT:
```
#   左边中点手柄的对角固定锚点 → 右边中点

```python
                new_w = px - mx
```
# new_w = px - mx

```python
                new_h = orig.height()
```
# new_h = orig.height()

```python
            case ResizeHandleType.MIDDLE_RIGHT:
```
#   右边中点手柄的对角固定锚点 → 左边中点

```python
                new_w = mx - px
```
# new_w = mx - px

```python
                new_h = orig.height()
```
# new_h = orig.height()

```python
            case ResizeHandleType.BOTTOM_LEFT:
```
#   左下角手柄的对角固定锚点 → 右上角 `rect.topRight()`

```python
                new_w = px - mx
```
# new_w = px - mx

```python
                new_h = my - py
```
# new_h = my - py

```python
            case ResizeHandleType.BOTTOM_CENTER:
```
#   下边中点手柄的对角固定锚点 → 顶边中点

```python
                new_w = orig.width()
```
# new_w = orig.width()

```python
                new_h = my - py
```
# new_h = my - py

```python
            case ResizeHandleType.BOTTOM_RIGHT:
```
#   右下角手柄的对角固定锚点 → 左上角 `rect.topLeft()`

```python
                new_w = mx - px
```
# new_w = mx - px

```python
                new_h = my - py
```
# new_h = my - py

```python
            case _:
```
# case _:

```python
                return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # 最小尺寸限制
```
# 源代码注释：最小尺寸限制

```python
        new_w = max(new_w, 10)
```
# new_w = max(new_w, 10)

```python
        new_h = max(new_h, 10)
```
# new_h = max(new_h, 10)

```python

```
# 空行

```python
        # 等比约束
```
# 源代码注释：等比约束

```python
        if keep_ratio:
```
# if keep_ratio:

```python
            orig_aspect = orig.width() / max(orig.height(), 1)
```
# orig_aspect = orig.width() / max(orig.height(), 1)

```python
            if self._scale_handle in (
```
# if self._scale_handle in (

```python
                ResizeHandleType.TOP_CENTER, ResizeHandleType.BOTTOM_CENTER,
```
# ResizeHandleType.TOP_CENTER, ResizeHandleType.BOTTOM_CENTER,

```python
            ):
```
# ):

```python
                new_w = new_h * orig_aspect
```
# new_w = new_h * orig_aspect

```python
            elif self._scale_handle in (
```
# elif self._scale_handle in (

```python
                ResizeHandleType.MIDDLE_LEFT, ResizeHandleType.MIDDLE_RIGHT,
```
# ResizeHandleType.MIDDLE_LEFT, ResizeHandleType.MIDDLE_RIGHT,

```python
            ):
```
# ):

```python
                new_h = new_w / max(orig_aspect, 0.001)
```
# new_h = new_w / max(orig_aspect, 0.001)

```python
            else:
```
# else:

```python
                # 角手柄：选择较大的维度保持比例
```
# 源代码注释：角手柄：选择较大的维度保持比例

```python
                aspect_w = new_h * orig_aspect
```
# aspect_w = new_h * orig_aspect

```python
                aspect_h = new_w / max(orig_aspect, 0.001)
```
# aspect_h = new_w / max(orig_aspect, 0.001)

```python
                if abs(new_w - aspect_w) < abs(new_h - aspect_h):
```
# if abs(new_w - aspect_w) < abs(new_h - aspect_h):

```python
                    new_h = new_w / max(orig_aspect, 0.001)
```
# new_h = new_w / max(orig_aspect, 0.001)

```python
                else:
```
# else:

```python
                    new_w = new_h * orig_aspect
```
# new_w = new_h * orig_aspect

```python

```
# 空行

```python
        # 应用缩放
```
# 源代码注释：应用缩放

```python
        self._resize_item(self._dragging_item, pivot, orig, new_w, new_h)
```
# self._resize_item(self._dragging_item, pivot, orig, new_w, new_h)

```python

```
# 空行

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
# 文档字符串：说明根据图形类型选择不同的缩放策略

```python
        scale_x = new_w / max(orig_rect.width(), 0.001)
```
# scale_x = new_w / max(orig_rect.width(), 0.001)

```python
        scale_y = new_h / max(orig_rect.height(), 0.001)
```
# scale_y = new_h / max(orig_rect.height(), 0.001)

```python

```
# 空行

```python
        if isinstance(item, RectangleItem):
```
# if isinstance(item, RectangleItem):

```python
            # 矩形：直接修改 rect
```
# 源代码注释：矩形：直接修改 rect

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
# elif isinstance(item, EllipseItem):

```python
            # 椭圆：直接修改 rect
```
# 源代码注释：椭圆：直接修改 rect

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
# elif isinstance(item, PathItem):

```python
            # 路径：缩放所有锚点
```
# 源代码注释：路径：缩放所有锚点

```python
            ref_x = pivot.x() if scale_x > 0 else orig_rect.right()
```
# ref_x = pivot.x() if scale_x > 0 else orig_rect.right()

```python
            ref_y = pivot.y() if scale_y > 0 else orig_rect.bottom()
```
# ref_y = pivot.y() if scale_y > 0 else orig_rect.bottom()

```python
            for anchor in item.anchors:
```
# for anchor in item.anchors:

```python
                anchor.x = ref_x + (anchor.x - ref_x) * scale_x
```
# anchor.x = ref_x + (anchor.x - ref_x) * scale_x

```python
                anchor.y = ref_y + (anchor.y - ref_y) * scale_y
```
# anchor.y = ref_y + (anchor.y - ref_y) * scale_y

```python
                if anchor.handle_in:
```
# if anchor.handle_in:

```python
                    anchor.handle_in = QPointF(
```
# anchor.handle_in = QPointF(

```python
                        anchor.handle_in.x() * scale_x,
```
# anchor.handle_in.x() * scale_x,

```python
                        anchor.handle_in.y() * scale_y,
```
# anchor.handle_in.y() * scale_y,

```python
                    )
```
# 导入结束括号

```python
                if anchor.handle_out:
```
# if anchor.handle_out:

```python
                    anchor.handle_out = QPointF(
```
# anchor.handle_out = QPointF(

```python
                        anchor.handle_out.x() * scale_x,
```
# anchor.handle_out.x() * scale_x,

```python
                        anchor.handle_out.y() * scale_y,
```
# anchor.handle_out.y() * scale_y,

```python
                    )
```
# 导入结束括号

```python
            item._rebuild_from_anchors()
```
# item._rebuild_from_anchors()

```python
        elif isinstance(item, TextFrame):
```
# elif isinstance(item, TextFrame):

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
# else:

```python
            # 通用缩放
```
# 源代码注释：通用缩放

```python
            item.scale(scale_x, scale_y, pivot)
```
# item.scale(scale_x, scale_y, pivot)

```python

```
# 空行

```python
    # ── 绘制 ──
```
# 分隔注释：绘制 —— 用于视觉分组

```python

```
# 空行

```python
    def draw_preview(self, painter: QPainter):
```
# def draw_preview(self, painter: QPainter):

```python
        # 绘制缩放手柄
```
# 源代码注释：绘制缩放手柄

```python
        if self._document:
```
# if self._document:

```python
            for layer in self._document.layers:
```
# for layer in self._document.layers:

```python
                if not layer.visible:
```
# if not layer.visible:

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
# if item.selected and item.visible:

```python
                        self._draw_resize_handles(painter, item)
```
# self._draw_resize_handles(painter, item)

```python

```
# 空行

```python
        if self._is_marquee and self._drag_start and self._drag_current:
```
# if self._is_marquee and self._drag_start and self._drag_current:

```python
            scale = max(painter.transform().m11(), 0.001)
```
# scale = max(painter.transform().m11(), 0.001)

```python
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
```
# pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)

```python
            painter.setPen(pen)
```
# painter.setPen(pen)

```python
            painter.setBrush(QColor(0, 120, 215, 30))
```
# painter.setBrush(QColor(0, 120, 215, 30))

```python
            painter.drawRect(QRectF(self._drag_start, self._drag_current))
```
# painter.drawRect(QRectF(self._drag_start, self._drag_current))

```python

```
# 空行

```python
    def _draw_resize_handles(self, painter: QPainter, item: GraphicItem):
```
# 定义 `_draw_resize_handles` 方法：为指定图形项绘制 8 个缩放手柄（四角 + 四边中点）

```python
        """绘制 8 个缩放手柄（世界坐标系）"""
```
# 文档字符串：绘制 8 个缩放手柄，使用世界坐标系

```python
        # 将本地 bounding_rect 通过 item 的变换映射到世界坐标
```
# 源代码注释：将本地 bounding_rect 通过 item 的变换映射到世界坐标

```python
        local_rect = item.bounding_rect()
```
# local_rect = item.bounding_rect()

```python
        rect = item._transform.mapRect(local_rect)
```
# rect = item._transform.mapRect(local_rect)

```python
        scale = max(painter.transform().m11(), 0.001)
```
# scale = max(painter.transform().m11(), 0.001)

```python
        handle_size = 7 / scale
```
# handle_size = 7 / scale

```python
        half_hs = handle_size / 2
```
# half_hs = handle_size / 2

```python

```
# 空行

```python
        pen = QPen(QColor(0, 120, 215), 1.0 / scale)
```
# pen = QPen(QColor(0, 120, 215), 1.0 / scale)

```python
        painter.setPen(pen)
```
# painter.setPen(pen)

```python
        painter.setBrush(QColor(255, 255, 255))
```
# painter.setBrush(QColor(255, 255, 255))

```python

```
# 空行

```python
        # 四个角
```
# 源代码注释：四个角

```python
        corners = [
```
# corners = [

```python
            rect.topLeft(), rect.topRight(),
```
# rect.topLeft(), rect.topRight(),

```python
            rect.bottomLeft(), rect.bottomRight(),
```
# rect.bottomLeft(), rect.bottomRight(),

```python
        ]
```
# ]

```python
        # 四条边的中点
```
# 源代码注释：四条边的中点

```python
        edges = [
```
# edges = [

```python
            QPointF(rect.center().x(), rect.top()),
```
# QPointF(rect.center().x(), rect.top()),

```python
            QPointF(rect.center().x(), rect.bottom()),
```
# QPointF(rect.center().x(), rect.bottom()),

```python
            QPointF(rect.left(), rect.center().y()),
```
# QPointF(rect.left(), rect.center().y()),

```python
            QPointF(rect.right(), rect.center().y()),
```
# QPointF(rect.right(), rect.center().y()),

```python
        ]
```
# ]

```python

```
# 空行

```python
        for pt in corners + edges:
```
# for pt in corners + edges:

```python
            painter.drawRect(QRectF(
```
# painter.drawRect(QRectF(

```python
                pt.x() - half_hs, pt.y() - half_hs,
```
# pt.x() - half_hs, pt.y() - half_hs,

```python
                handle_size, handle_size,
```
# handle_size, handle_size,

```python
            ))
```
# ))

```python

```
# 空行

```python

```
# 空行

```python
# ── 直接选择工具 ──────────────────────────────────────────
```
# 分隔注释：直接选择工具 —— 用于视觉分组

```python

```
# 空行

```python
class DirectSelectTool(BaseTool):
```
# 定义 `DirectSelectTool` 直接选择工具类（白箭头）：继承 `BaseTool`，实现路径锚点/手柄编辑、线段点击选中、整项拖拽

```python
    """直接选择工具（A）—— 对照 Adobe Illustrator 1:1 复原
```
# """直接选择工具（A）—— 对照 Adobe Illustrator 1:1 复原

```python

```
# 空行

```python
    AI 中的 Direct Selection Tool (白箭头) 行为：
```
# AI 中的 Direct Selection Tool (白箭头) 行为：

```python
    1. 点击已选中路径的锚点/手柄 → 选中并进入拖拽
```
# 1. 点击已选中路径的锚点/手柄 → 选中并进入拖拽

```python
    2. 点击已选中路径的线段 → 选中该路径（显示所有锚点），不添加锚点
```
# 2. 点击已选中路径的线段 → 选中该路径（显示所有锚点），不添加锚点

```python
    3. 按住 Alt/Option 拖拽手柄 → 断开手柄对称约束（转为角点）
```
# 3. 按住 Alt/Option 拖拽手柄 → 断开手柄对称约束（转为角点）

```python
    4. 拖拽平滑点的手柄 → 自动对称约束
```
# 4. 拖拽平滑点的手柄 → 自动对称约束

```python
    5. 未选中路径 → 点击选中（显示锚点），可拖拽整项
```
# 5. 未选中路径 → 点击选中（显示锚点），可拖拽整项

```python
    6. 按住 Shift → 多选
```
# 6. 按住 Shift → 多选

```python
    7. 框选 → 选中范围内的图形项
```
# 7. 框选 → 选中范围内的图形项

```python
    """
```
# 三引号字符串开始 —— 模块文档字符串

```python
    __slots__ = (
```
# __slots__ = (

```python
        '_drag_start', '_drag_current',
```
# '_drag_start', '_drag_current',

```python
        '_dragging_anchor_idx', '_dragging_handle_idx',
```
# '_dragging_anchor_idx', '_dragging_handle_idx',

```python
        '_dragging_handle_type', '_dragging_item',
```
# '_dragging_handle_type', '_dragging_item',

```python
        '_drag_offset', '_selected_anchor_idx',
```
# '_drag_offset', '_selected_anchor_idx',

```python
        '_is_marquee', '_old_anchors',
```
# '_is_marquee', '_old_anchors',

```python
        '_has_moved',
```
# '_has_moved',

```python
        '_press_alt',           # 按下时 Alt 是否已激活（用于断手柄）
```
# '_press_alt',           # 按下时 Alt 是否已激活（用于断手柄）

```python
        '_original_anchor_type', # 记录拖拽前锚点类型
```
# '_original_anchor_type', # 记录拖拽前锚点类型

```python
    )
```
# 导入结束括号

```python

```
# 空行

```python
    # 基础容差（100%缩放下的像素值，与 AI 一致）
```
# 源代码注释：基础容差（100%缩放下的像素值，与 AI 一致）

```python
    ANCHOR_TOLERANCE = 5.0       # 锚点点击容差
```
# ANCHOR_TOLERANCE = 5.0       # 锚点点击容差

```python
    HANDLE_TOLERANCE = 4.0       # 手柄点击容差  
```
# HANDLE_TOLERANCE = 4.0       # 手柄点击容差

```python
    SEGMENT_TOLERANCE = 4.0      # 路径段点击容差
```
# SEGMENT_TOLERANCE = 4.0      # 路径段点击容差

```python
    DRAG_THRESHOLD = 3.0         # 最小拖拽阈值（像素）
```
# DRAG_THRESHOLD = 3.0         # 最小拖拽阈值（像素）

```python

```
# 空行

```python
    def __init__(self):
```
# def __init__(self):

```python
        super().__init__(ToolType.DIRECT_SELECT)
```
# super().__init__(ToolType.DIRECT_SELECT)

```python
        self._drag_start: QPointF | None = None
```
# self._drag_start: QPointF | None = None

```python
        self._drag_current: QPointF | None = None
```
# self._drag_current: QPointF | None = None

```python
        self._dragging_anchor_idx: int = -1
```
# self._dragging_anchor_idx: int = -1

```python
        self._dragging_handle_idx: int = -1
```
# self._dragging_handle_idx: int = -1

```python
        self._dragging_handle_type: str = ''
```
# self._dragging_handle_type: str = ''

```python
        self._dragging_item: GraphicItem | None = None
```
# self._dragging_item: GraphicItem | None = None

```python
        self._drag_offset = QPointF(0, 0)
```
# self._drag_offset = QPointF(0, 0)

```python
        self._selected_anchor_idx: int = -1
```
# self._selected_anchor_idx: int = -1

```python
        self._is_marquee: bool = False
```
# self._is_marquee: bool = False

```python
        self._old_anchors: list[AnchorPoint] = []
```
# self._old_anchors: list[AnchorPoint] = []

```python
        self._has_moved: bool = False
```
# self._has_moved: bool = False

```python
        self._press_alt: bool = False
```
# self._press_alt: bool = False

```python
        self._original_anchor_type: AnchorPointType | None = None
```
# self._original_anchor_type: AnchorPointType | None = None

```python

```
# 空行

```python
    # ── 辅助方法 ──
```
# 分隔注释：辅助方法 —— 用于视觉分组

```python

```
# 空行

```python
    @staticmethod
```
# @staticmethod

```python
    def _safe_inverted(transform):
```
# 定义 `_safe_inverted` 静态方法：安全获取变换矩阵的逆矩阵，返回 (逆矩阵, 是否成功) 元组

```python
        """安全获取逆变换矩阵，返回 (inverted_transform, success)"""
```
# 文档字符串：说明返回值格式

```python
        try:
```
# try:

```python
            inv, ok = transform.inverted()
```
# 尝试调用变换矩阵的 `inverted()` 方法获取逆矩阵：`inv` 逆矩阵、`ok` 是否成功

```python
            return (inv, ok)
```
# return (inv, ok)

```python
        except Exception:
```
# except Exception:

```python
            return (transform, False)
```
# return (transform, False)

```python

```
# 空行

```python
    def _find_path_at(self, pos: QPointF, must_be_selected: bool = False) -> tuple[PathItem | None, QPointF | None]:
```
# 定义 `_find_path_at` 方法：在文档中查找鼠标位置下的 PathItem，参数 `must_be_selected` 限制只搜索已选中路径

```python
        """从文档中查找点击位置的 PathItem，返回 (item, local_pos)"""
```
# 文档字符串：返回 (找到的 PathItem, 局部坐标) 元组

```python
        if not self._document:
```
# if not self._document:

```python
            return (None, None)
```
# return (None, None)

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
# 检查图形项是否已被选中

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
# if not ok:

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
# 源代码注释：用 bounding_rect 快速判断（放宽一点）

```python
                br = item.bounding_rect()
```
# br = item.bounding_rect()

```python
                if not br.contains(local_pos):
```
# if not br.contains(local_pos):

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                return (item, local_pos)
```
# return (item, local_pos)

```python
        return (None, None)
```
# return (None, None)

```python

```
# 空行

```python
    # ── 鼠标事件 ──
```
# 分隔注释：鼠标事件 —— 用于视觉分组

```python

```
# 空行

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# def mouse_press(self, pos: QPointF, modifiers: int):

```python
        if not self._document:
```
# if not self._document:

```python
            return
```
# 提前返回，不再继续后续检测

```python
        self._drag_start = QPointF(pos)
```
# 更新拖拽起始点为当前位置

```python
        self._drag_current = QPointF(pos)
```
# self._drag_current = QPointF(pos)

```python
        self._has_moved = False
```
# 重置移动标志

```python
        self._press_alt = bool(modifiers & Qt.AltModifier)
```
# self._press_alt = bool(modifiers & Qt.AltModifier)

```python
        self._original_anchor_type = None
```
# 重置原始锚点类型

```python

```
# 空行

```python
        shift = bool(modifiers & Qt.ShiftModifier)
```
# shift = bool(modifiers & Qt.ShiftModifier)

```python

```
# 空行

```python
        # ── 1. 优先检测已选中路径的手柄 ──
```
# 分隔注释：1. 优先检测已选中路径的手柄 —— 用于视觉分组

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
# if not ok:

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
# 调用 PathItem 的 `get_handle_at` 方法检测鼠标是否在手柄上

```python
                    local_pos.x(), local_pos.y(),
```
# local_pos.x(), local_pos.y(),

```python
                    tolerance=self.HANDLE_TOLERANCE,
```
# 使用手柄容差 4.0px 进行命中检测

```python
                )
```
# 导入结束括号

```python
                if idx >= 0:
```
# if idx >= 0:

```python
                    self._dragging_item = item
```
# 设置当前图形项为被拖拽项

```python
                    self._dragging_handle_idx = idx
```
# self._dragging_handle_idx = idx

```python
                    self._dragging_handle_type = htype
```
# self._dragging_handle_type = htype

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
# 源代码注释：记录原始锚点类型（Alt 拖拽时断开约束）

```python
                    self._original_anchor_type = item.anchors[idx].anchor_type
```
# 记录拖拽前该锚点的类型（SMOOTH 或 CORNER）

```python
                    # 如果按 Alt，将锚点转为角点（断开对称约束）
```
# 源代码注释：如果按 Alt，将锚点转为角点（断开对称约束）

```python
                    if self._press_alt:
```
# if self._press_alt:

```python
                        item.anchors[idx].convert_to_corner()
```
# item.anchors[idx].convert_to_corner()

```python
                    return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── 2. 检测已选中路径的锚点 ──
```
# 分隔注释：2. 检测已选中路径的锚点 —— 用于视觉分组

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
# if not ok:

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
# 调用 PathItem 的 `get_anchor_at` 方法检测鼠标是否命中某个锚点

```python
                    local_pos.x(), local_pos.y(),
```
# local_pos.x(), local_pos.y(),

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
# 使用锚点容差 5.0px 进行命中检测

```python
                )
```
# 导入结束括号

```python
                if idx >= 0:
```
# if idx >= 0:

```python
                    self._dragging_item = item
```
# 设置当前图形项为被拖拽项

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
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── 3. 检测已选中路径的线段（AI：点击线段选中路径但不添加锚点）──
```
# 分隔注释：3. 检测已选中路径的线段（AI：点击线段选中路径但不添加锚点） —— 用于视觉分组

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
# if not ok:

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
# 调用 PathItem 的 `get_segment_at` 方法检测鼠标是否在路径段附近

```python
                    local_pos.x(), local_pos.y(),
```
# local_pos.x(), local_pos.y(),

```python
                    tolerance=self.SEGMENT_TOLERANCE,
```
# 使用路径段容差 4.0px 进行命中检测

```python
                )
```
# 导入结束括号

```python
                if seg >= 0:
```
# if seg >= 0:

```python
                    # AI 行为：点击已选中路径的线段，选中该路径用于整体拖拽
```
# 源代码注释：AI 行为：点击已选中路径的线段，选中该路径用于整体拖拽

```python
                    self._dragging_item = item
```
# 设置当前图形项为被拖拽项

```python
                    self._selected_anchor_idx = -1  # 不选中特定锚点
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
                    return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── 4. 检测未选中路径 → 选中它并准备整体拖拽 ──
```
# 分隔注释：4. 检测未选中路径 → 选中它并准备整体拖拽 —— 用于视觉分组

```python
        # AI 行为：用 Direct Select 工具点击未选中路径的任意位置 → 选中路径显示锚点
```
# 源代码注释：AI 行为：用 Direct Select 工具点击未选中路径的任意位置 → 选中路径显示锚点

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
# if not ok:

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
# 空行

```python
                # 先检查是否在路径段附近
```
# 源代码注释：先检查是否在路径段附近

```python
                seg = item.get_segment_at(
```
# 调用 PathItem 的 `get_segment_at` 方法检测鼠标是否在路径段附近

```python
                    local_pos.x(), local_pos.y(),
```
# local_pos.x(), local_pos.y(),

```python
                    tolerance=self.SEGMENT_TOLERANCE,
```
# 使用路径段容差 4.0px 进行命中检测

```python
                )
```
# 导入结束括号

```python
                if seg >= 0:
```
# if seg >= 0:

```python
                    if not shift:
```
# if not shift:

```python
                        self._document.clear_selection()
```
# 调用文档方法清除所有图形项的选中状态

```python
                    item.selected = True
```
# 将当前图形项设为选中状态

```python
                    self._dragging_item = item
```
# 设置当前图形项为被拖拽项

```python
                    self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
                    return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
                # 再检查是否在锚点附近
```
# 源代码注释：再检查是否在锚点附近

```python
                idx = item.get_anchor_at(
```
# 调用 PathItem 的 `get_anchor_at` 方法检测鼠标是否命中某个锚点

```python
                    local_pos.x(), local_pos.y(),
```
# local_pos.x(), local_pos.y(),

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
# 使用锚点容差 5.0px 进行命中检测

```python
                )
```
# 导入结束括号

```python
                if idx >= 0:
```
# if idx >= 0:

```python
                    if not shift:
```
# if not shift:

```python
                        self._document.clear_selection()
```
# 调用文档方法清除所有图形项的选中状态

```python
                    item.selected = True
```
# 将当前图形项设为选中状态

```python
                    self._dragging_item = item
```
# 设置当前图形项为被拖拽项

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
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
                # 最后检查填充区域
```
# 源代码注释：最后检查填充区域

```python
                if item.contains_point(local_pos):
```
# if item.contains_point(local_pos):

```python
                    if not shift:
```
# if not shift:

```python
                        self._document.clear_selection()
```
# 调用文档方法清除所有图形项的选中状态

```python
                    item.selected = True
```
# 将当前图形项设为选中状态

```python
                    self._dragging_item = item
```
# 设置当前图形项为被拖拽项

```python
                    self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
                    return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── 5. 检测普通图形项 ──
```
# 分隔注释：5. 检测普通图形项 —— 用于视觉分组

```python
        item = self._document.get_item_at(pos.x(), pos.y())
```
# 通过文档查找鼠标位置下的最顶层图形项

```python
        if item:
```
# if item:

```python
            if not shift:
```
# if not shift:

```python
                self._document.clear_selection()
```
# 调用文档方法清除所有图形项的选中状态

```python
            item.selected = True
```
# 将当前图形项设为选中状态

```python
            self._dragging_item = item
```
# 设置当前图形项为被拖拽项

```python
            self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── 6. 框选 ──
```
# 分隔注释：6. 框选 —— 用于视觉分组

```python
        if not shift:
```
# if not shift:

```python
            self._document.clear_selection()
```
# 调用文档方法清除所有图形项的选中状态

```python
        self._is_marquee = True
```
# 设置框选标志为 True

```python

```
# 空行

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# def mouse_move(self, pos: QPointF, modifiers: int):

```python
        if self._drag_start is None:
```
# if self._drag_start is None:

```python
            return
```
# 提前返回，不再继续后续检测

```python
        self._drag_current = QPointF(pos)
```
# self._drag_current = QPointF(pos)

```python

```
# 空行

```python
        dx_total = pos.x() - self._drag_start.x()
```
# dx_total = pos.x() - self._drag_start.x()

```python
        dy_total = pos.y() - self._drag_start.y()
```
# dy_total = pos.y() - self._drag_start.y()

```python
        dist = math.sqrt(dx_total * dx_total + dy_total * dy_total)
```
# dist = math.sqrt(dx_total * dx_total + dy_total * dy_total)

```python
        alt_held = bool(modifiers & Qt.AltModifier)
```
# alt_held = bool(modifiers & Qt.AltModifier)

```python

```
# 空行

```python
        # ── 手柄拖拽 ──
```
# 分隔注释：手柄拖拽 —— 用于视觉分组

```python
        if self._dragging_handle_idx >= 0 and self._dragging_item:
```
# if self._dragging_handle_idx >= 0 and self._dragging_item:

```python
            if isinstance(self._dragging_item, PathItem):
```
# if isinstance(self._dragging_item, PathItem):

```python
                inv, ok = self._safe_inverted(self._dragging_item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵（用于世界坐标→局部坐标转换）

```python
                if not ok:
```
# if not ok:

```python
                    return
```
# 提前返回，不再继续后续检测

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                anchor = self._dragging_item.anchors[self._dragging_handle_idx]
```
# anchor = self._dragging_item.anchors[self._dragging_handle_idx]

```python
                rel_x = local_pos.x() - anchor.x
```
# rel_x = local_pos.x() - anchor.x

```python
                rel_y = local_pos.y() - anchor.y
```
# rel_y = local_pos.y() - anchor.y

```python

```
# 空行

```python
                # 平滑点约束：不按 Alt 时自动对称
```
# 源代码注释：平滑点约束：不按 Alt 时自动对称

```python
                constrain = (anchor.anchor_type == AnchorPointType.SMOOTH and not alt_held)
```
# constrain = (anchor.anchor_type == AnchorPointType.SMOOTH and not alt_held)

```python

```
# 空行

```python
                if self._dragging_handle_type == 'in':
```
# if self._dragging_handle_type == 'in':

```python
                    self._dragging_item.set_handle_in(
```
# self._dragging_item.set_handle_in(

```python
                        self._dragging_handle_idx, rel_x, rel_y,
```
# self._dragging_handle_idx, rel_x, rel_y,

```python
                        constrain_smooth=constrain,
```
# constrain_smooth=constrain,

```python
                    )
```
# 导入结束括号

```python
                else:
```
# else:

```python
                    self._dragging_item.set_handle_out(
```
# self._dragging_item.set_handle_out(

```python
                        self._dragging_handle_idx, rel_x, rel_y,
```
# self._dragging_handle_idx, rel_x, rel_y,

```python
                        constrain_smooth=constrain,
```
# constrain_smooth=constrain,

```python
                    )
```
# 导入结束括号

```python
                if self._document:
```
# if self._document:

```python
                    self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行

```python
        # ── 锚点拖拽（超过阈值后移动）──
```
# 分隔注释：锚点拖拽（超过阈值后移动） —— 用于视觉分组

```python
        elif self._dragging_anchor_idx >= 0 and self._dragging_item:
```
# elif self._dragging_anchor_idx >= 0 and self._dragging_item:

```python
            if not self._has_moved:
```
# if not self._has_moved:

```python
                if dist < self.DRAG_THRESHOLD:
```
# if dist < self.DRAG_THRESHOLD:

```python
                    return
```
# 提前返回，不再继续后续检测

```python
                self._has_moved = True
```
# 标记已发生实际移动

```python

```
# 空行

```python
            if isinstance(self._dragging_item, PathItem):
```
# if isinstance(self._dragging_item, PathItem):

```python
                inv, ok = self._safe_inverted(self._dragging_item._transform)
```
# 安全获取图形项变换矩阵的逆矩阵（用于世界坐标→局部坐标转换）

```python
                if not ok:
```
# if not ok:

```python
                    return
```
# 提前返回，不再继续后续检测

```python
                local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
                self._dragging_item.move_anchor(
```
# self._dragging_item.move_anchor(

```python
                    self._dragging_anchor_idx, local_pos.x(), local_pos.y(),
```
# self._dragging_anchor_idx, local_pos.x(), local_pos.y(),

```python
                )
```
# 导入结束括号

```python
                if self._document:
```
# if self._document:

```python
                    self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行

```python
        # ── 整项拖拽（非锚点/手柄拖拽模式）──
```
# 分隔注释：整项拖拽（非锚点/手柄拖拽模式） —— 用于视觉分组

```python
        elif self._dragging_item and not self._is_marquee:
```
# elif self._dragging_item and not self._is_marquee:

```python
            if not self._has_moved:
```
# if not self._has_moved:

```python
                if dist < self.DRAG_THRESHOLD:
```
# if dist < self.DRAG_THRESHOLD:

```python
                    return
```
# 提前返回，不再继续后续检测

```python
                self._has_moved = True
```
# 标记已发生实际移动

```python

```
# 空行

```python
            dx = pos.x() - self._drag_start.x()
```
# dx = pos.x() - self._drag_start.x()

```python
            dy = pos.y() - self._drag_start.y()
```
# dy = pos.y() - self._drag_start.y()

```python
            if modifiers & Qt.ShiftModifier:
```
# if modifiers & Qt.ShiftModifier:

```python
                dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)
```
# dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)

```python
            self._dragging_item.move_by(dx, dy)
```
# self._dragging_item.move_by(dx, dy)

```python
            self._drag_start = QPointF(pos)
```
# 更新拖拽起始点为当前位置

```python
            if self._document:
```
# if self._document:

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# def mouse_release(self, pos: QPointF, modifiers: int):

```python
        # ── 如果拖拽了手柄且按了 Alt，需要恢复锚点类型为角点 ──
```
# 分隔注释：如果拖拽了手柄且按了 Alt，需要恢复锚点类型为角点 —— 用于视觉分组

```python
        if self._dragging_handle_idx >= 0 and self._dragging_item:
```
# if self._dragging_handle_idx >= 0 and self._dragging_item:

```python
            if isinstance(self._dragging_item, PathItem):
```
# if isinstance(self._dragging_item, PathItem):

```python
                if self._press_alt or self._has_moved:
```
# if self._press_alt or self._has_moved:

```python
                    # Alt+拖拽：断开对称约束，转为角点
```
# 源代码注释：Alt+拖拽：断开对称约束，转为角点

```python
                    anchor = self._dragging_item.anchors[self._dragging_handle_idx]
```
# anchor = self._dragging_item.anchors[self._dragging_handle_idx]

```python
                    if self._press_alt:
```
# if self._press_alt:

```python
                        anchor.anchor_type = AnchorPointType.CORNER
```
# anchor.anchor_type = AnchorPointType.CORNER

```python
                    self._dragging_item._build_path()
```
# self._dragging_item._build_path()

```python

```
# 空行

```python
        # ── 记录撤销命令（通过 execute_command 统一入口）──
```
# 分隔注释：记录撤销命令（通过 execute_command 统一入口） —— 用于视觉分组

```python
        if self._old_anchors and self._dragging_item and self._document:
```
# if self._old_anchors and self._dragging_item and self._document:

```python
            if isinstance(self._dragging_item, PathItem):
```
# if isinstance(self._dragging_item, PathItem):

```python
                new_anchors = [a.copy() for a in self._dragging_item.anchors]
```
# new_anchors = [a.copy() for a in self._dragging_item.anchors]

```python
                if self._has_moved and len(self._old_anchors) == len(new_anchors):
```
# if self._has_moved and len(self._old_anchors) == len(new_anchors):

```python
                    # 检查是否真的有变化
```
# 源代码注释：检查是否真的有变化

```python
                    changed = False
```
# changed = False

```python
                    for old, new in zip(self._old_anchors, new_anchors):
```
# for old, new in zip(self._old_anchors, new_anchors):

```python
                        if (old.x != new.x or old.y != new.y or
```
# if (old.x != new.x or old.y != new.y or

```python
                            old.handle_in != new.handle_in or
```
# old.handle_in != new.handle_in or

```python
                            old.handle_out != new.handle_out or
```
# old.handle_out != new.handle_out or

```python
                            old.anchor_type != new.anchor_type):
```
# old.anchor_type != new.anchor_type):

```python
                            changed = True
```
# changed = True

```python
                            break
```
# break

```python
                    if changed:
```
# if changed:

```python
                        cmd = ModifyAnchorCommand(
```
# cmd = ModifyAnchorCommand(

```python
                            self._document, self._dragging_item,
```
# self._document, self._dragging_item,

```python
                            self._old_anchors, new_anchors,
```
# self._old_anchors, new_anchors,

```python
                        )
```
# 导入结束括号

```python
                        self._document.execute_command(cmd)
```
# self._document.execute_command(cmd)

```python

```
# 空行

```python
        # ── 框选 ──
```
# 分隔注释：框选 —— 用于视觉分组

```python
        if self._is_marquee and self._drag_start and self._document:
```
# if self._is_marquee and self._drag_start and self._document:

```python
            rect = QRectF(self._drag_start, pos).normalized()
```
# rect = QRectF(self._drag_start, pos).normalized()

```python
            if rect.width() > 2 and rect.height() > 2:
```
# if rect.width() > 2 and rect.height() > 2:

```python
                for layer in self._document.layers:
```
# for layer in self._document.layers:

```python
                    items = layer.get_items_in_rect(
```
# items = layer.get_items_in_rect(

```python
                        rect.x(), rect.y(), rect.width(), rect.height(),
```
# rect.x(), rect.y(), rect.width(), rect.height(),

```python
                    )
```
# 导入结束括号

```python
                    for item in items:
```
# for item in items:

```python
                        item.selected = True
```
# 将当前图形项设为选中状态

```python

```
# 空行

```python
        # ── 重置状态 ──
```
# 分隔注释：重置状态 —— 用于视觉分组

```python
        self._drag_start = None
```
# 清空拖拽起始点

```python
        self._drag_current = None
```
# self._drag_current = None

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
# 清空被拖拽图形项

```python
        self._is_marquee = False
```
# 设置框选标志为 False

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
# 空行

```python
    # ── 键盘 ──
```
# 分隔注释：键盘 —— 用于视觉分组

```python

```
# 空行

```python
    def key_press(self, key: int, modifiers: int):
```
# def key_press(self, key: int, modifiers: int):

```python
        """键盘操作对照 AI 行为"""
```
# """键盘操作对照 AI 行为"""

```python
        # Delete/Backspace 删除选中的锚点（AI：Delete Anchor Point）
```
# 源代码注释：Delete/Backspace 删除选中的锚点（AI：Delete Anchor Point）

```python
        if key in (Qt.Key_Delete, Qt.Key_Backspace):
```
# if key in (Qt.Key_Delete, Qt.Key_Backspace):

```python
            if self._selected_anchor_idx >= 0 and self._dragging_item:
```
# if self._selected_anchor_idx >= 0 and self._dragging_item:

```python
                if isinstance(self._dragging_item, PathItem):
```
# if isinstance(self._dragging_item, PathItem):

```python
                    if self._dragging_item.anchor_count > 2:
```
# if self._dragging_item.anchor_count > 2:

```python
                        old_anchors = [a.copy() for a in self._dragging_item.anchors]
```
# old_anchors = [a.copy() for a in self._dragging_item.anchors]

```python
                        self._dragging_item.remove_anchor(self._selected_anchor_idx)
```
# self._dragging_item.remove_anchor(self._selected_anchor_idx)

```python
                        if self._document:
```
# if self._document:

```python
                            new_anchors = [a.copy() for a in self._dragging_item.anchors]
```
# new_anchors = [a.copy() for a in self._dragging_item.anchors]

```python
                            cmd = ModifyAnchorCommand(
```
# cmd = ModifyAnchorCommand(

```python
                                self._document, self._dragging_item,
```
# self._document, self._dragging_item,

```python
                                old_anchors, new_anchors,
```
# old_anchors, new_anchors,

```python
                            )
```
# 导入结束括号

```python
                            self._document.execute_command(cmd)
```
# self._document.execute_command(cmd)

```python
                        self._selected_anchor_idx = max(0, min(
```
# self._selected_anchor_idx = max(0, min(

```python
                            self._selected_anchor_idx,
```
# self._selected_anchor_idx,

```python
                            self._dragging_item.anchor_count - 1,
```
# self._dragging_item.anchor_count - 1,

```python
                        ))
```
# ))

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # Plus/Equal 在选中锚点后添加新锚点（段中点）
```
# 源代码注释：Plus/Equal 在选中锚点后添加新锚点（段中点）

```python
        if key in (Qt.Key_Plus, Qt.Key_Equal):
```
# if key in (Qt.Key_Plus, Qt.Key_Equal):

```python
            if self._selected_anchor_idx >= 0 and self._dragging_item:
```
# if self._selected_anchor_idx >= 0 and self._dragging_item:

```python
                if isinstance(self._dragging_item, PathItem):
```
# if isinstance(self._dragging_item, PathItem):

```python
                    self._add_anchor_after_selected(self._dragging_item)
```
# self._add_anchor_after_selected(self._dragging_item)

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
    def _add_anchor_after_selected(self, item: PathItem):
```
# def _add_anchor_after_selected(self, item: PathItem):

```python
        """在选中锚点之后的段中点添加新锚点"""
```
# """在选中锚点之后的段中点添加新锚点"""

```python
        anchors = item.anchors
```
# anchors = item.anchors

```python
        i = self._selected_anchor_idx
```
# i = self._selected_anchor_idx

```python
        if i < 0 or len(anchors) < 2:
```
# if i < 0 or len(anchors) < 2:

```python
            return
```
# 提前返回，不再继续后续检测

```python
        n = len(anchors)
```
# n = len(anchors)

```python
        j = (i + 1) % n
```
# j = (i + 1) % n

```python
        if not item.closed and i == n - 1:
```
# if not item.closed and i == n - 1:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # 在贝塞尔曲线段的中点添加锚点
```
# 源代码注释：在贝塞尔曲线段的中点添加锚点

```python
        prev, curr = anchors[i], anchors[j]
```
# prev, curr = anchors[i], anchors[j]

```python

```
# 空行

```python
        # 使用贝塞尔采样获取真正的中点
```
# 源代码注释：使用贝塞尔采样获取真正的中点

```python
        samples = PathItem._sample_bezier_segment(prev, curr, num_samples=4)
```
# samples = PathItem._sample_bezier_segment(prev, curr, num_samples=4)

```python
        if len(samples) >= 2:
```
# if len(samples) >= 2:

```python
            # 取中点
```
# 源代码注释：取中点

```python
            mid_idx = len(samples) // 2
```
# mid_idx = len(samples) // 2

```python
            mx, my = samples[mid_idx]
```
# mx, my = samples[mid_idx]

```python
        else:
```
# else:

```python
            mx = (prev.x + curr.x) / 2
```
# mx = (prev.x + curr.x) / 2

```python
            my = (prev.y + curr.y) / 2
```
# my = (prev.y + curr.y) / 2

```python

```
# 空行

```python
        old_anchors = [a.copy() for a in anchors]
```
# old_anchors = [a.copy() for a in anchors]

```python
        new_anchor = AnchorPoint(mx, my)
```
# new_anchor = AnchorPoint(mx, my)

```python
        item.insert_anchor(i + 1, new_anchor)
```
# item.insert_anchor(i + 1, new_anchor)

```python
        self._selected_anchor_idx = i + 1
```
# self._selected_anchor_idx = i + 1

```python
        self._dragging_item = item
```
# 设置当前图形项为被拖拽项

```python

```
# 空行

```python
        if self._document:
```
# if self._document:

```python
            new_anchors = [a.copy() for a in item.anchors]
```
# new_anchors = [a.copy() for a in item.anchors]

```python
            cmd = ModifyAnchorCommand(
```
# cmd = ModifyAnchorCommand(

```python
                self._document, item, old_anchors, new_anchors,
```
# self._document, item, old_anchors, new_anchors,

```python
            )
```
# 导入结束括号

```python
            self._document.execute_command(cmd)
```
# self._document.execute_command(cmd)

```python

```
# 空行

```python
    # ── 绘制预览 ──
```
# 分隔注释：绘制预览 —— 用于视觉分组

```python

```
# 空行

```python
    def draw_preview(self, painter: QPainter):
```
# def draw_preview(self, painter: QPainter):

```python
        if not self._document:
```
# if not self._document:

```python
            return
```
# 提前返回，不再继续后续检测

```python
        for layer in self._document.layers:
```
# for layer in self._document.layers:

```python
            if not layer.visible:
```
# if not layer.visible:

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
# if isinstance(item, PathItem) and item.selected:

```python
                    self._draw_anchor_handles(painter, item)
```
# self._draw_anchor_handles(painter, item)

```python

```
# 空行

```python
        if self._is_marquee and self._drag_start and self._drag_current:
```
# if self._is_marquee and self._drag_start and self._drag_current:

```python
            scale = max(painter.transform().m11(), 0.001)
```
# scale = max(painter.transform().m11(), 0.001)

```python
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
```
# pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)

```python
            painter.setPen(pen)
```
# painter.setPen(pen)

```python
            painter.setBrush(QColor(0, 120, 215, 30))
```
# painter.setBrush(QColor(0, 120, 215, 30))

```python
            painter.drawRect(QRectF(self._drag_start, self._drag_current))
```
# painter.drawRect(QRectF(self._drag_start, self._drag_current))

```python

```
# 空行

```python
    def _draw_anchor_handles(self, painter: QPainter, item: PathItem):
```
# def _draw_anchor_handles(self, painter: QPainter, item: PathItem):

```python
        """绘制锚点和贝塞尔手柄，对照 AI 的视觉风格
```
# """绘制锚点和贝塞尔手柄，对照 AI 的视觉风格

```python

```
# 空行

```python
        AI 锚点渲染规则：
```
# AI 锚点渲染规则：

```python
        - 未选中锚点：白色填充方形，蓝色边框
```
# - 未选中锚点：白色填充方形，蓝色边框

```python
        - 选中锚点：蓝色填充方形，深蓝边框
```
# - 选中锚点：蓝色填充方形，深蓝边框

```python
        - 手柄线：灰色虚线（handle_in）/ 实线（handle_out）
```
# - 手柄线：灰色虚线（handle_in）/ 实线（handle_out）

```python
        - 手柄端点：白色填充圆形，灰色边框
```
# - 手柄端点：白色填充圆形，灰色边框

```python
        - 平滑点 vs 角点使用相同视觉表示
```
# - 平滑点 vs 角点使用相同视觉表示

```python
        """
```
# 三引号字符串开始 —— 模块文档字符串

```python
        if not item.anchors:
```
# if not item.anchors:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        scale = max(painter.transform().m11(), 0.001)
```
# scale = max(painter.transform().m11(), 0.001)

```python
        handle_r = 3.5 / scale        # 手柄端点半径
```
# handle_r = 3.5 / scale        # 手柄端点半径

```python
        anchor_half = 3.5 / scale     # 锚点半边长
```
# anchor_half = 3.5 / scale     # 锚点半边长

```python
        highlight_half = 4.5 / scale  # 选中锚点半边长
```
# highlight_half = 4.5 / scale  # 选中锚点半边长

```python

```
# 空行

```python
        transform = item._transform
```
# transform = item._transform

```python
        anchor_color = QColor(0, 120, 215)       # AI 蓝
```
# anchor_color = QColor(0, 120, 215)       # AI 蓝

```python
        anchor_border = QColor(0, 80, 180)
```
# anchor_border = QColor(0, 80, 180)

```python
        handle_color = QColor(120, 120, 120)     # 手柄线颜色
```
# handle_color = QColor(120, 120, 120)     # 手柄线颜色

```python

```
# 空行

```python
        for i, anchor in enumerate(item.anchors):
```
# for i, anchor in enumerate(item.anchors):

```python
            ax_local, ay_local = anchor.x, anchor.y
```
# ax_local, ay_local = anchor.x, anchor.y

```python
            ax = transform.map(QPointF(ax_local, ay_local)).x()
```
# ax = transform.map(QPointF(ax_local, ay_local)).x()

```python
            ay = transform.map(QPointF(ax_local, ay_local)).y()
```
# ay = transform.map(QPointF(ax_local, ay_local)).y()

```python

```
# 空行

```python
            # ── 绘制 handle_in 线和端点 ──
```
# 分隔注释：绘制 handle_in 线和端点 —— 用于视觉分组

```python
            if anchor.handle_in:
```
# if anchor.handle_in:

```python
                hx_local = ax_local + anchor.handle_in.x()
```
# hx_local = ax_local + anchor.handle_in.x()

```python
                hy_local = ay_local + anchor.handle_in.y()
```
# hy_local = ay_local + anchor.handle_in.y()

```python
                hx_pt = transform.map(QPointF(hx_local, hy_local))
```
# hx_pt = transform.map(QPointF(hx_local, hy_local))

```python
                hx, hy = hx_pt.x(), hx_pt.y()
```
# hx, hy = hx_pt.x(), hx_pt.y()

```python

```
# 空行

```python
                # 手柄线
```
# 源代码注释：手柄线

```python
                handle_pen = QPen(handle_color, 1.0 / scale, Qt.DashLine)
```
# handle_pen = QPen(handle_color, 1.0 / scale, Qt.DashLine)

```python
                painter.setPen(handle_pen)
```
# painter.setPen(handle_pen)

```python
                painter.setBrush(Qt.NoBrush)
```
# painter.setBrush(Qt.NoBrush)

```python
                painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))
```
# painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))

```python

```
# 空行

```python
                # 手柄端点（圆形）
```
# 源代码注释：手柄端点（圆形）

```python
                painter.setBrush(QColor(255, 255, 255))
```
# painter.setBrush(QColor(255, 255, 255))

```python
                painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))
```
# painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))

```python
                painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)
```
# painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)

```python

```
# 空行

```python
            # ── 绘制 handle_out 线和端点 ──
```
# 分隔注释：绘制 handle_out 线和端点 —— 用于视觉分组

```python
            if anchor.handle_out:
```
# if anchor.handle_out:

```python
                hx_local = ax_local + anchor.handle_out.x()
```
# hx_local = ax_local + anchor.handle_out.x()

```python
                hy_local = ay_local + anchor.handle_out.y()
```
# hy_local = ay_local + anchor.handle_out.y()

```python
                hx_pt = transform.map(QPointF(hx_local, hy_local))
```
# hx_pt = transform.map(QPointF(hx_local, hy_local))

```python
                hx, hy = hx_pt.x(), hx_pt.y()
```
# hx, hy = hx_pt.x(), hx_pt.y()

```python

```
# 空行

```python
                # 手柄线
```
# 源代码注释：手柄线

```python
                handle_pen = QPen(handle_color, 1.0 / scale, Qt.SolidLine)
```
# handle_pen = QPen(handle_color, 1.0 / scale, Qt.SolidLine)

```python
                painter.setPen(handle_pen)
```
# painter.setPen(handle_pen)

```python
                painter.setBrush(Qt.NoBrush)
```
# painter.setBrush(Qt.NoBrush)

```python
                painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))
```
# painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))

```python

```
# 空行

```python
                # 手柄端点（圆形）
```
# 源代码注释：手柄端点（圆形）

```python
                painter.setBrush(QColor(255, 255, 255))
```
# painter.setBrush(QColor(255, 255, 255))

```python
                painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))
```
# painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))

```python
                painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)
```
# painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)

```python

```
# 空行

```python
            # ── 绘制锚点（方形）──
```
# 分隔注释：绘制锚点（方形） —— 用于视觉分组

```python
            is_highlighted = (i == self._selected_anchor_idx)
```
# is_highlighted = (i == self._selected_anchor_idx)

```python

```
# 空行

```python
            if is_highlighted:
```
# if is_highlighted:

```python
                # 选中锚点：蓝色填充
```
# 源代码注释：选中锚点：蓝色填充

```python
                painter.setBrush(anchor_color)
```
# painter.setBrush(anchor_color)

```python
                painter.setPen(QPen(anchor_border, 1.5 / scale))
```
# painter.setPen(QPen(anchor_border, 1.5 / scale))

```python
                painter.drawRect(QRectF(
```
# painter.drawRect(QRectF(

```python
                    ax - highlight_half, ay - highlight_half,
```
# ax - highlight_half, ay - highlight_half,

```python
                    highlight_half * 2, highlight_half * 2,
```
# highlight_half * 2, highlight_half * 2,

```python
                ))
```
# ))

```python
            else:
```
# else:

```python
                # 未选中锚点：白色填充
```
# 源代码注释：未选中锚点：白色填充

```python
                painter.setBrush(QColor(255, 255, 255))
```
# painter.setBrush(QColor(255, 255, 255))

```python
                painter.setPen(QPen(anchor_color, 1.5 / scale))
```
# painter.setPen(QPen(anchor_color, 1.5 / scale))

```python
                painter.drawRect(QRectF(
```
# painter.drawRect(QRectF(

```python
                    ax - anchor_half, ay - anchor_half,
```
# ax - anchor_half, ay - anchor_half,

```python
                    anchor_half * 2, anchor_half * 2,
```
# anchor_half * 2, anchor_half * 2,

```python
                ))
```
# ))

```python

```
# 空行

```python
    def cancel(self):
```
# def cancel(self):

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
# 清空被拖拽图形项

```python
        super().cancel()
```
# super().cancel()

```python

```
# 空行

```python
    @staticmethod
```
# @staticmethod

```python
    def _draw_single_anchor(painter: QPainter, item: PathItem, 
```
# def _draw_single_anchor(painter: QPainter, item: PathItem,

```python
                             anchor_idx: int, highlighted: bool = True):
```
# anchor_idx: int, highlighted: bool = True):

```python
        """绘制单个锚点（供其他锚点工具使用）"""
```
# """绘制单个锚点（供其他锚点工具使用）"""

```python
        if anchor_idx < 0 or anchor_idx >= len(item.anchors):
```
# if anchor_idx < 0 or anchor_idx >= len(item.anchors):

```python
            return
```
# 提前返回，不再继续后续检测

```python
        scale = max(painter.transform().m11(), 0.001)
```
# scale = max(painter.transform().m11(), 0.001)

```python
        anchor_half = 4.5 / scale if highlighted else 3.5 / scale
```
# anchor_half = 4.5 / scale if highlighted else 3.5 / scale

```python
        transform = item._transform
```
# transform = item._transform

```python
        anchor = item.anchors[anchor_idx]
```
# anchor = item.anchors[anchor_idx]

```python
        ax = transform.map(QPointF(anchor.x, anchor.y)).x()
```
# ax = transform.map(QPointF(anchor.x, anchor.y)).x()

```python
        ay = transform.map(QPointF(anchor.x, anchor.y)).y()
```
# ay = transform.map(QPointF(anchor.x, anchor.y)).y()

```python

```
# 空行

```python
        if highlighted:
```
# if highlighted:

```python
            painter.setBrush(QColor(0, 120, 215))
```
# painter.setBrush(QColor(0, 120, 215))

```python
            painter.setPen(QPen(QColor(0, 80, 180), 1.5 / scale))
```
# painter.setPen(QPen(QColor(0, 80, 180), 1.5 / scale))

```python
        else:
```
# else:

```python
            painter.setBrush(QColor(255, 255, 255))
```
# painter.setBrush(QColor(255, 255, 255))

```python
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
```
# painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))

```python

```
# 空行

```python
        painter.drawRect(QRectF(
```
# painter.drawRect(QRectF(

```python
            ax - anchor_half, ay - anchor_half,
```
# ax - anchor_half, ay - anchor_half,

```python
            anchor_half * 2, anchor_half * 2,
```
# anchor_half * 2, anchor_half * 2,

```python
        ))
```
# ))

```python

```
# 空行

```python

```
# 空行

```python
# ── 形状工具 ──────────────────────────────────────────────
```
# 分隔注释：形状工具 —— 用于视觉分组

```python

```
# 空行

```python
class ShapeTool(BaseTool, ABC):
```
# 定义 ShapeTool 形状工具抽象基类：继承 BaseTool 和 ABC，为矩形/椭圆工具提供统一的拖拽绘制框架

```python
    """形状工具基类（矩形/椭圆）"""
```
# """形状工具基类（矩形/椭圆）"""

```python
    __slots__ = ('_drag_start', '_drag_current', '_preview_item')
```
# __slots__ = ('_drag_start', '_drag_current', '_preview_item')

```python

```
# 空行

```python
    def __init__(self, tool_type: ToolType):
```
# def __init__(self, tool_type: ToolType):

```python
        super().__init__(tool_type)
```
# super().__init__(tool_type)

```python
        self._drag_start: QPointF | None = None
```
# self._drag_start: QPointF | None = None

```python
        self._drag_current: QPointF | None = None
```
# self._drag_current: QPointF | None = None

```python
        self._preview_item: GraphicItem | None = None
```
# self._preview_item: GraphicItem | None = None

```python

```
# 空行

```python
    @abstractmethod
```
# @abstractmethod

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
# def _create_item(self, rect: QRectF) -> GraphicItem:

```python
        ...
```
# ...

```python

```
# 空行

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# def mouse_press(self, pos: QPointF, modifiers: int):

```python
        self._drag_start = QPointF(pos)
```
# 更新拖拽起始点为当前位置

```python
        self._drag_current = QPointF(pos)
```
# self._drag_current = QPointF(pos)

```python
        self._is_drawing = True
```
# self._is_drawing = True

```python
        if self._document:
```
# if self._document:

```python
            self._document.clear_selection()
```
# 调用文档方法清除所有图形项的选中状态

```python

```
# 空行

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# def mouse_move(self, pos: QPointF, modifiers: int):

```python
        if self._is_drawing:
```
# if self._is_drawing:

```python
            self._drag_current = QPointF(pos)
```
# self._drag_current = QPointF(pos)

```python

```
# 空行

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# def mouse_release(self, pos: QPointF, modifiers: int):

```python
        if not self._is_drawing or not self._document or not self._drag_start:
```
# if not self._is_drawing or not self._document or not self._drag_start:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        self._drag_current = QPointF(pos)
```
# self._drag_current = QPointF(pos)

```python
        rect = QRectF(self._drag_start, self._drag_current).normalized()
```
# rect = QRectF(self._drag_start, self._drag_current).normalized()

```python

```
# 空行

```python
        # Shift 约束等比（正方形/正圆）
```
# 源代码注释：Shift 约束等比（正方形/正圆）

```python
        if modifiers & Qt.ShiftModifier:
```
# if modifiers & Qt.ShiftModifier:

```python
            size = max(rect.width(), rect.height())
```
# size = max(rect.width(), rect.height())

```python
            if rect.width() < rect.height():
```
# if rect.width() < rect.height():

```python
                rect.setWidth(size)
```
# rect.setWidth(size)

```python
            else:
```
# else:

```python
                rect.setHeight(size)
```
# rect.setHeight(size)

```python

```
# 空行

```python
        if rect.width() > 2 and rect.height() > 2:
```
# if rect.width() > 2 and rect.height() > 2:

```python
            item = self._create_item(rect)
```
# item = self._create_item(rect)

```python
            item.selected = True
```
# 将当前图形项设为选中状态

```python
            self._document.add_item(item)
```
# self._document.add_item(item)

```python

```
# 空行

```python
        self._drag_start = None
```
# 清空拖拽起始点

```python
        self._drag_current = None
```
# self._drag_current = None

```python
        self._is_drawing = False
```
# self._is_drawing = False

```python

```
# 空行

```python
    def draw_preview(self, painter: QPainter):
```
# def draw_preview(self, painter: QPainter):

```python
        if self._is_drawing and self._drag_start and self._drag_current:
```
# if self._is_drawing and self._drag_start and self._drag_current:

```python
            rect = QRectF(self._drag_start, self._drag_current).normalized()
```
# rect = QRectF(self._drag_start, self._drag_current).normalized()

```python
            scale = max(painter.transform().m11(), 0.001)
```
# scale = max(painter.transform().m11(), 0.001)

```python
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
```
# pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)

```python
            painter.setPen(pen)
```
# painter.setPen(pen)

```python
            painter.setBrush(QColor(0, 120, 215, 20))
```
# painter.setBrush(QColor(0, 120, 215, 20))

```python
            painter.drawRect(rect)
```
# painter.drawRect(rect)

```python

```
# 空行

```python

```
# 空行

```python
class RectangleTool(ShapeTool):
```
# 定义 RectangleTool 矩形工具类：继承 ShapeTool，实现矩形的拖拽绘制

```python
    """矩形工具"""
```
# """矩形工具"""

```python
    __slots__ = ()
```
# __slots__ = ()

```python

```
# 空行

```python
    def __init__(self):
```
# def __init__(self):

```python
        super().__init__(ToolType.RECTANGLE)
```
# super().__init__(ToolType.RECTANGLE)

```python

```
# 空行

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
# def _create_item(self, rect: QRectF) -> GraphicItem:

```python
        item = RectangleItem(rect.x(), rect.y(), rect.width(), rect.height())
```
# item = RectangleItem(rect.x(), rect.y(), rect.width(), rect.height())

```python
        item.style.fill_color = QColor(200, 200, 200)
```
# item.style.fill_color = QColor(200, 200, 200)

```python
        item.style.stroke_color = QColor(50, 50, 50)
```
# item.style.stroke_color = QColor(50, 50, 50)

```python
        item.style.stroke_width = 2.0
```
# item.style.stroke_width = 2.0

```python
        return item
```
# return item

```python

```
# 空行

```python

```
# 空行

```python
class EllipseTool(ShapeTool):
```
# 定义 EllipseTool 椭圆工具类：继承 ShapeTool，实现椭圆的拖拽绘制

```python
    """椭圆工具"""
```
# """椭圆工具"""

```python
    __slots__ = ()
```
# __slots__ = ()

```python

```
# 空行

```python
    def __init__(self):
```
# def __init__(self):

```python
        super().__init__(ToolType.ELLIPSE)
```
# super().__init__(ToolType.ELLIPSE)

```python

```
# 空行

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
# def _create_item(self, rect: QRectF) -> GraphicItem:

```python
        item = EllipseItem(rect.x(), rect.y(), rect.width(), rect.height())
```
# item = EllipseItem(rect.x(), rect.y(), rect.width(), rect.height())

```python
        item.style.fill_color = QColor(200, 200, 200)
```
# item.style.fill_color = QColor(200, 200, 200)

```python
        item.style.stroke_color = QColor(50, 50, 50)
```
# item.style.stroke_color = QColor(50, 50, 50)

```python
        item.style.stroke_width = 2.0
```
# item.style.stroke_width = 2.0

```python
        return item
```
# return item

```python

```
# 空行

```python

```
# 空行

```python
# ── 添加锚点工具 (Add Anchor Point Tool, +) ──────────────────
```
# 分隔注释：添加锚点工具 (Add Anchor Point Tool, +) —— 用于视觉分组

```python

```
# 空行

```python
class AddAnchorPointTool(BaseTool):
```
# 定义 AddAnchorPointTool 添加锚点工具类：继承 BaseTool，在路径段上点击添加新锚点（对照 AI 的 + 工具）

```python
    """添加锚点工具 —— 在路径段上点击添加新锚点
```
# """添加锚点工具 —— 在路径段上点击添加新锚点

```python

```
# 空行

```python
    对照 AI 行为：
```
# 对照 AI 行为：

```python
    - 点击路径段 → 在最近位置添加新锚点（不进入拖拽）
```
# - 点击路径段 → 在最近位置添加新锚点（不进入拖拽）

```python
    - 只对已选中的路径有效
```
# - 只对已选中的路径有效

```python
    """
```
# 三引号字符串开始 —— 模块文档字符串

```python
    __slots__ = ('_selected_anchor_idx', '_dragging_item')
```
# __slots__ = ('_selected_anchor_idx', '_dragging_item')

```python

```
# 空行

```python
    SEGMENT_TOLERANCE = 4.0
```
# SEGMENT_TOLERANCE = 4.0

```python

```
# 空行

```python
    def __init__(self):
```
# def __init__(self):

```python
        super().__init__(ToolType.ADD_ANCHOR)
```
# super().__init__(ToolType.ADD_ANCHOR)

```python
        self._selected_anchor_idx: int = -1
```
# self._selected_anchor_idx: int = -1

```python
        self._dragging_item: GraphicItem | None = None
```
# self._dragging_item: GraphicItem | None = None

```python

```
# 空行

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# def mouse_press(self, pos: QPointF, modifiers: int):

```python
        if not self._document:
```
# if not self._document:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

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
# inv, ok = DirectSelectTool._safe_inverted(item._transform)

```python
                if not ok:
```
# if not ok:

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
# 调用 PathItem 的 `get_segment_at` 方法检测鼠标是否在路径段附近

```python
                    local_pos.x(), local_pos.y(),
```
# local_pos.x(), local_pos.y(),

```python
                    tolerance=self.SEGMENT_TOLERANCE,
```
# 使用路径段容差 4.0px 进行命中检测

```python
                )
```
# 导入结束括号

```python
                if seg >= 0:
```
# if seg >= 0:

```python
                    # 找到最近点
```
# 源代码注释：找到最近点

```python
                    closest = item.get_closest_point_on_segment(seg, local_pos.x(), local_pos.y())
```
# closest = item.get_closest_point_on_segment(seg, local_pos.x(), local_pos.y())

```python

```
# 空行

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
# old_anchors = [a.copy() for a in item.anchors]

```python
                    new_anchor = AnchorPoint(closest[0], closest[1])
```
# new_anchor = AnchorPoint(closest[0], closest[1])

```python
                    insert_idx = seg + 1
```
# insert_idx = seg + 1

```python
                    item.insert_anchor(insert_idx, new_anchor)
```
# item.insert_anchor(insert_idx, new_anchor)

```python

```
# 空行

```python
                    self._selected_anchor_idx = insert_idx
```
# self._selected_anchor_idx = insert_idx

```python
                    self._dragging_item = item
```
# 设置当前图形项为被拖拽项

```python

```
# 空行

```python
                    if self._document:
```
# if self._document:

```python
                        new_anchors = [a.copy() for a in item.anchors]
```
# new_anchors = [a.copy() for a in item.anchors]

```python
                        cmd = ModifyAnchorCommand(
```
# cmd = ModifyAnchorCommand(

```python
                            self._document, item, old_anchors, new_anchors,
```
# self._document, item, old_anchors, new_anchors,

```python
                        )
```
# 导入结束括号

```python
                        self._document.execute_command(cmd)
```
# self._document.execute_command(cmd)

```python
                    return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# def mouse_move(self, pos: QPointF, modifiers: int):

```python
        pass  # 不拖拽
```
# pass  # 不拖拽

```python

```
# 空行

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# def mouse_release(self, pos: QPointF, modifiers: int):

```python
        pass
```
# pass

```python

```
# 空行

```python
    def draw_preview(self, painter: QPainter):
```
# def draw_preview(self, painter: QPainter):

```python
        """高亮显示新添加的锚点"""
```
# """高亮显示新添加的锚点"""

```python
        if self._selected_anchor_idx >= 0 and self._dragging_item:
```
# if self._selected_anchor_idx >= 0 and self._dragging_item:

```python
            if isinstance(self._dragging_item, PathItem):
```
# if isinstance(self._dragging_item, PathItem):

```python
                DirectSelectTool._draw_single_anchor(
```
# DirectSelectTool._draw_single_anchor(

```python
                    painter, self._dragging_item, self._selected_anchor_idx, True
```
# painter, self._dragging_item, self._selected_anchor_idx, True

```python
                )
```
# 导入结束括号

```python

```
# 空行

```python
    def cancel(self):
```
# def cancel(self):

```python
        self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
        self._dragging_item = None
```
# 清空被拖拽图形项

```python
        super().cancel()
```
# super().cancel()

```python

```
# 空行

```python

```
# 空行

```python
# ── 删除锚点工具 (Delete Anchor Point Tool, -) ────────────────
```
# 分隔注释：删除锚点工具 (Delete Anchor Point Tool, -) —— 用于视觉分组

```python

```
# 空行

```python
class DeleteAnchorPointTool(BaseTool):
```
# 定义 DeleteAnchorPointTool 删除锚点工具类：继承 BaseTool，点击锚点直接删除（对照 AI 的 - 工具）

```python
    """删除锚点工具 —— 点击锚点直接删除
```
# """删除锚点工具 —— 点击锚点直接删除

```python

```
# 空行

```python
    对照 AI 行为：
```
# 对照 AI 行为：

```python
    - 点击锚点 → 删除该锚点（保留路径连续性）
```
# - 点击锚点 → 删除该锚点（保留路径连续性）

```python
    - 至少保留 2 个锚点
```
# - 至少保留 2 个锚点

```python
    - 只对已选中的路径有效
```
# - 只对已选中的路径有效

```python
    """
```
# 三引号字符串开始 —— 模块文档字符串

```python
    __slots__ = ('_selected_anchor_idx', '_dragging_item')
```
# __slots__ = ('_selected_anchor_idx', '_dragging_item')

```python

```
# 空行

```python
    ANCHOR_TOLERANCE = 5.0
```
# ANCHOR_TOLERANCE = 5.0

```python

```
# 空行

```python
    def __init__(self):
```
# def __init__(self):

```python
        super().__init__(ToolType.DELETE_ANCHOR)
```
# super().__init__(ToolType.DELETE_ANCHOR)

```python
        self._selected_anchor_idx: int = -1
```
# self._selected_anchor_idx: int = -1

```python
        self._dragging_item: GraphicItem | None = None
```
# self._dragging_item: GraphicItem | None = None

```python

```
# 空行

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# def mouse_press(self, pos: QPointF, modifiers: int):

```python
        if not self._document:
```
# if not self._document:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

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
# if item.anchor_count <= 2:

```python
                    continue
```
# 跳过当前循环迭代，继续下一个

```python
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
```
# inv, ok = DirectSelectTool._safe_inverted(item._transform)

```python
                if not ok:
```
# if not ok:

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
# 调用 PathItem 的 `get_anchor_at` 方法检测鼠标是否命中某个锚点

```python
                    local_pos.x(), local_pos.y(),
```
# local_pos.x(), local_pos.y(),

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
# 使用锚点容差 5.0px 进行命中检测

```python
                )
```
# 导入结束括号

```python
                if idx >= 0:
```
# if idx >= 0:

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
# old_anchors = [a.copy() for a in item.anchors]

```python
                    item.remove_anchor(idx)
```
# item.remove_anchor(idx)

```python

```
# 空行

```python
                    self._dragging_item = item
```
# 设置当前图形项为被拖拽项

```python
                    self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python

```
# 空行

```python
                    if self._document:
```
# if self._document:

```python
                        new_anchors = [a.copy() for a in item.anchors]
```
# new_anchors = [a.copy() for a in item.anchors]

```python
                        cmd = ModifyAnchorCommand(
```
# cmd = ModifyAnchorCommand(

```python
                            self._document, item, old_anchors, new_anchors,
```
# self._document, item, old_anchors, new_anchors,

```python
                        )
```
# 导入结束括号

```python
                        self._document.execute_command(cmd)
```
# self._document.execute_command(cmd)

```python
                    return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# def mouse_move(self, pos: QPointF, modifiers: int):

```python
        pass
```
# pass

```python

```
# 空行

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# def mouse_release(self, pos: QPointF, modifiers: int):

```python
        pass
```
# pass

```python

```
# 空行

```python
    def draw_preview(self, painter: QPainter):
```
# def draw_preview(self, painter: QPainter):

```python
        pass  # AI 的删除锚点工具在悬停时显示 - 图标，这里简化处理
```
# pass  # AI 的删除锚点工具在悬停时显示 - 图标，这里简化处理

```python

```
# 空行

```python
    def cancel(self):
```
# def cancel(self):

```python
        self._selected_anchor_idx = -1
```
# 重置选中锚点索引为 -1（表示无选中锚点）

```python
        self._dragging_item = None
```
# 清空被拖拽图形项

```python
        super().cancel()
```
# super().cancel()

```python

```
# 空行

```python

```
# 空行

```python
# ── 转换锚点工具 (Convert Anchor Point Tool, Shift+C) ─────────
```
# 分隔注释：转换锚点工具 (Convert Anchor Point Tool, Shift+C) ─ —— 用于视觉分组

```python

```
# 空行

```python
class ConvertAnchorPointTool(BaseTool):
```
# 定义 ConvertAnchorPointTool 转换锚点工具类：继承 BaseTool，切换锚点类型或拖拽拉出手柄（对照 AI 的 Shift+C 工具）

```python
    """转换锚点工具 —— 切换锚点类型 / 拖拽拉出手柄
```
# """转换锚点工具 —— 切换锚点类型 / 拖拽拉出手柄

```python

```
# 空行

```python
    对照 AI 行为：
```
# 对照 AI 行为：

```python
    - 点击平滑点 → 转为角点（移除手柄）
```
# - 点击平滑点 → 转为角点（移除手柄）

```python
    - 点击角点并拖拽 → 拉出手柄转为平滑点
```
# - 点击角点并拖拽 → 拉出手柄转为平滑点

```python
    - 拖拽手柄 → 断开对称约束
```
# - 拖拽手柄 → 断开对称约束

```python
    """
```
# 三引号字符串开始 —— 模块文档字符串

```python
    __slots__ = (
```
# __slots__ = (

```python
        '_drag_start', '_dragging_item', '_dragging_anchor_idx',
```
# '_drag_start', '_dragging_item', '_dragging_anchor_idx',

```python
        '_is_dragging', '_old_anchors',
```
# '_is_dragging', '_old_anchors',

```python
    )
```
# 导入结束括号

```python

```
# 空行

```python
    ANCHOR_TOLERANCE = 5.0
```
# ANCHOR_TOLERANCE = 5.0

```python
    DRAG_THRESHOLD = 3.0
```
# DRAG_THRESHOLD = 3.0

```python

```
# 空行

```python
    def __init__(self):
```
# def __init__(self):

```python
        super().__init__(ToolType.CONVERT_ANCHOR)
```
# super().__init__(ToolType.CONVERT_ANCHOR)

```python
        self._drag_start: QPointF | None = None
```
# self._drag_start: QPointF | None = None

```python
        self._dragging_item: GraphicItem | None = None
```
# self._dragging_item: GraphicItem | None = None

```python
        self._dragging_anchor_idx: int = -1
```
# self._dragging_anchor_idx: int = -1

```python
        self._is_dragging: bool = False
```
# self._is_dragging: bool = False

```python
        self._old_anchors: list[AnchorPoint] = []
```
# self._old_anchors: list[AnchorPoint] = []

```python

```
# 空行

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# def mouse_press(self, pos: QPointF, modifiers: int):

```python
        if not self._document:
```
# if not self._document:

```python
            return
```
# 提前返回，不再继续后续检测

```python
        self._drag_start = QPointF(pos)
```
# 更新拖拽起始点为当前位置

```python
        self._is_dragging = False
```
# self._is_dragging = False

```python

```
# 空行

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
# inv, ok = DirectSelectTool._safe_inverted(item._transform)

```python
                if not ok:
```
# if not ok:

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
# 调用 PathItem 的 `get_anchor_at` 方法检测鼠标是否命中某个锚点

```python
                    local_pos.x(), local_pos.y(),
```
# local_pos.x(), local_pos.y(),

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
# 使用锚点容差 5.0px 进行命中检测

```python
                )
```
# 导入结束括号

```python
                if idx >= 0:
```
# if idx >= 0:

```python
                    self._dragging_item = item
```
# 设置当前图形项为被拖拽项

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
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# def mouse_move(self, pos: QPointF, modifiers: int):

```python
        if not self._dragging_item or self._dragging_anchor_idx < 0:
```
# if not self._dragging_item or self._dragging_anchor_idx < 0:

```python
            return
```
# 提前返回，不再继续后续检测

```python
        if self._drag_start is None:
```
# if self._drag_start is None:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        dx = pos.x() - self._drag_start.x()
```
# dx = pos.x() - self._drag_start.x()

```python
        dy = pos.y() - self._drag_start.y()
```
# dy = pos.y() - self._drag_start.y()

```python
        dist = math.sqrt(dx*dx + dy*dy)
```
# dist = math.sqrt(dx*dx + dy*dy)

```python

```
# 空行

```python
        if not self._is_dragging:
```
# if not self._is_dragging:

```python
            if dist < self.DRAG_THRESHOLD:
```
# if dist < self.DRAG_THRESHOLD:

```python
                return
```
# 提前返回，不再继续后续检测

```python
            self._is_dragging = True
```
# self._is_dragging = True

```python

```
# 空行

```python
        # 拖拽：从锚点拉出手柄
```
# 源代码注释：拖拽：从锚点拉出手柄

```python
        if isinstance(self._dragging_item, PathItem):
```
# if isinstance(self._dragging_item, PathItem):

```python
            inv, ok = DirectSelectTool._safe_inverted(self._dragging_item._transform)
```
# inv, ok = DirectSelectTool._safe_inverted(self._dragging_item._transform)

```python
            if not ok:
```
# if not ok:

```python
                return
```
# 提前返回，不再继续后续检测

```python
            local_pos = inv.map(pos)
```
# 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标

```python
            anchor = self._dragging_item.anchors[self._dragging_anchor_idx]
```
# anchor = self._dragging_item.anchors[self._dragging_anchor_idx]

```python

```
# 空行

```python
            rel_x = local_pos.x() - anchor.x
```
# rel_x = local_pos.x() - anchor.x

```python
            rel_y = local_pos.y() - anchor.y
```
# rel_y = local_pos.y() - anchor.y

```python

```
# 空行

```python
            # 拉出双向对称手柄（平滑点）
```
# 源代码注释：拉出双向对称手柄（平滑点）

```python
            anchor.handle_out = QPointF(rel_x, rel_y)
```
# anchor.handle_out = QPointF(rel_x, rel_y)

```python
            anchor.handle_in = QPointF(-rel_x, -rel_y)
```
# anchor.handle_in = QPointF(-rel_x, -rel_y)

```python
            anchor.anchor_type = AnchorPointType.SMOOTH
```
# anchor.anchor_type = AnchorPointType.SMOOTH

```python

```
# 空行

```python
            self._dragging_item._build_path()
```
# self._dragging_item._build_path()

```python
            if self._document:
```
# if self._document:

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# def mouse_release(self, pos: QPointF, modifiers: int):

```python
        if not self._dragging_item or self._dragging_anchor_idx < 0:
```
# if not self._dragging_item or self._dragging_anchor_idx < 0:

```python
            self._drag_start = None
```
# 清空拖拽起始点

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        if isinstance(self._dragging_item, PathItem):
```
# if isinstance(self._dragging_item, PathItem):

```python
            anchor = self._dragging_item.anchors[self._dragging_anchor_idx]
```
# anchor = self._dragging_item.anchors[self._dragging_anchor_idx]

```python

```
# 空行

```python
            if not self._is_dragging:
```
# if not self._is_dragging:

```python
                # 点击（未拖拽）：切换锚点类型
```
# 源代码注释：点击（未拖拽）：切换锚点类型

```python
                if anchor.has_handles:
```
# if anchor.has_handles:

```python
                    # 有手柄 → 转为角点（移除手柄）
```
# 源代码注释：有手柄 → 转为角点（移除手柄）

```python
                    anchor.remove_handles()
```
# anchor.remove_handles()

```python
                # 无手柄的角点 → 点击不产生变化（AI 行为）
```
# 源代码注释：无手柄的角点 → 点击不产生变化（AI 行为）

```python
                self._dragging_item._build_path()
```
# self._dragging_item._build_path()

```python

```
# 空行

```python
            # 记录撤销命令（通过 execute_command 统一入口）
```
# 源代码注释：记录撤销命令（通过 execute_command 统一入口）

```python
            if self._document and self._old_anchors:
```
# if self._document and self._old_anchors:

```python
                new_anchors = [a.copy() for a in self._dragging_item.anchors]
```
# new_anchors = [a.copy() for a in self._dragging_item.anchors]

```python
                cmd = ModifyAnchorCommand(
```
# cmd = ModifyAnchorCommand(

```python
                    self._document, self._dragging_item,
```
# self._document, self._dragging_item,

```python
                    self._old_anchors, new_anchors,
```
# self._old_anchors, new_anchors,

```python
                )
```
# 导入结束括号

```python
                self._document.execute_command(cmd)
```
# self._document.execute_command(cmd)

```python

```
# 空行

```python
        self._drag_start = None
```
# 清空拖拽起始点

```python
        self._dragging_item = None
```
# 清空被拖拽图形项

```python
        self._dragging_anchor_idx = -1
```
# 重置拖拽锚点索引

```python
        self._is_dragging = False
```
# self._is_dragging = False

```python
        self._old_anchors = []
```
# 清空旧锚点列表

```python

```
# 空行

```python
    def draw_preview(self, painter: QPainter):
```
# def draw_preview(self, painter: QPainter):

```python
        """拖拽时显示预览手柄线"""
```
# """拖拽时显示预览手柄线"""

```python
        if self._is_dragging and self._dragging_item and self._dragging_anchor_idx >= 0:
```
# if self._is_dragging and self._dragging_item and self._dragging_anchor_idx >= 0:

```python
            if isinstance(self._dragging_item, PathItem):
```
# if isinstance(self._dragging_item, PathItem):

```python
                DirectSelectTool._draw_single_anchor(
```
# DirectSelectTool._draw_single_anchor(

```python
                    painter, self._dragging_item, self._dragging_anchor_idx, True
```
# painter, self._dragging_item, self._dragging_anchor_idx, True

```python
                )
```
# 导入结束括号

```python

```
# 空行

```python
    def cancel(self):
```
# def cancel(self):

```python
        self._dragging_item = None
```
# 清空被拖拽图形项

```python
        self._dragging_anchor_idx = -1
```
# 重置拖拽锚点索引

```python
        self._is_dragging = False
```
# self._is_dragging = False

```python
        super().cancel()
```
# super().cancel()

```python

```
# 空行

```python

```
# 空行

```python
# ── 钢笔工具 ──────────────────────────────────────────────
```
# 分隔注释：钢笔工具 —— 用于视觉分组

```python

```
# 空行

```python
class PenTool(BaseTool):
```
# 定义 PenTool 钢笔工具类：继承 BaseTool，1:1 对照 Adobe Illustrator 钢笔工具——单击创建角点、拖拽创建平滑点、闭合路径、添加/删除锚点

```python
    """钢笔工具 —— Adobe Illustrator 1:1 复原
```
# """钢笔工具 —— Adobe Illustrator 1:1 复原

```python

```
# 空行

```python
    功能对照：
```
# 功能对照：

```python
    - 单击 = 创建角点（Corner Point），无手柄
```
# - 单击 = 创建角点（Corner Point），无手柄

```python
    - 单击并拖动 = 创建平滑点（Smooth Point），拉出对称手柄
```
# - 单击并拖动 = 创建平滑点（Smooth Point），拉出对称手柄

```python
    - 点击起始锚点 = 闭合路径（光标出现圆圈 ○）
```
# - 点击起始锚点 = 闭合路径（光标出现圆圈 ○）

```python
    - Enter/Return = 结束路径
```
# - Enter/Return = 结束路径

```python
    - Escape = 取消路径
```
# - Escape = 取消路径

```python

```
# 空行

```python
    隐藏功能：
```
# 隐藏功能：

```python
    - Alt/Option 拖拽 = 调整单侧方向线（断开对称）
```
# - Alt/Option 拖拽 = 调整单侧方向线（断开对称）

```python
    - Ctrl/Cmd = 临时切换直接选择工具调整锚点
```
# - Ctrl/Cmd = 临时切换直接选择工具调整锚点

```python
    - Space = 在拖动过程中临时移动当前锚点位置
```
# - Space = 在拖动过程中临时移动当前锚点位置

```python
    - Shift = 约束角度（45度增量）
```
# - Shift = 约束角度（45度增量）

```python

```
# 空行

```python
    光标状态：
```
# 光标状态：

```python
    - 默认 = Pen（十字光标）
```
# - 默认 = Pen（十字光标）

```python
    - 悬停已有锚点 = Pen-（删除锚点）
```
# - 悬停已有锚点 = Pen-（删除锚点）

```python
    - 悬停已有路径段 = Pen+（添加锚点）
```
# - 悬停已有路径段 = Pen+（添加锚点）

```python
    - 悬停起始锚点 = Pen○（闭合路径）
```
# - 悬停起始锚点 = Pen○（闭合路径）

```python
    - 悬停端点 = Pen/（继续路径）
```
# - 悬停端点 = Pen/（继续路径）

```python
    """
```
# 三引号字符串开始 —— 模块文档字符串

```python

```
# 空行

```python
    DRAG_THRESHOLD = 3  # 拖拽阈值（像素），小于此值视为单击
```
# DRAG_THRESHOLD = 3  # 拖拽阈值（像素），小于此值视为单击

```python
    CLOSE_TOLERANCE = 8  # 闭合路径检测容差
```
# CLOSE_TOLERANCE = 8  # 闭合路径检测容差

```python
    HANDLE_TOLERANCE = 5  # 手柄命中容差
```
# HANDLE_TOLERANCE = 5  # 手柄命中容差

```python
    ANCHOR_TOLERANCE = 6  # 锚点命中容差
```
# ANCHOR_TOLERANCE = 6  # 锚点命中容差

```python
    SEGMENT_TOLERANCE = 5  # 路径段命中容差
```
# SEGMENT_TOLERANCE = 5  # 路径段命中容差

```python
    SHIFT_ANGLE_STEP = 45  # Shift约束角度步长（度）
```
# SHIFT_ANGLE_STEP = 45  # Shift约束角度步长（度）

```python

```
# 空行

```python
    __slots__ = (
```
# __slots__ = (

```python
        '_current_path', '_drawing', '_hover_state',
```
# '_current_path', '_drawing', '_hover_state',

```python
        '_drag_start_pos', '_is_dragging_handle',
```
# '_drag_start_pos', '_is_dragging_handle',

```python
        '_dragged_anchor_idx', '_dragged_handle_side',
```
# '_dragged_anchor_idx', '_dragged_handle_side',

```python
        '_alt_adjusting', '_space_moving', '_space_start_pos',
```
# '_alt_adjusting', '_space_moving', '_space_start_pos',

```python
        '_ctrl_temp_select', '_ctrl_drag_start',
```
# '_ctrl_temp_select', '_ctrl_drag_start',

```python
    )
```
# 导入结束括号

```python

```
# 空行

```python
    # ── 钢笔光标状态枚举 ──
```
# 分隔注释：钢笔光标状态枚举 —— 用于视觉分组

```python
    PEN_DEFAULT = 0        # 默认钢笔
```
# PEN_DEFAULT = 0        # 默认钢笔

```python
    PEN_PLUS = 1           # Pen+  添加锚点
```
# PEN_PLUS = 1           # Pen+  添加锚点

```python
    PEN_MINUS = 2          # Pen-  删除锚点
```
# PEN_MINUS = 2          # Pen-  删除锚点

```python
    PEN_CLOSE = 3          # Pen○  闭合路径
```
# PEN_CLOSE = 3          # Pen○  闭合路径

```python
    PEN_CONTINUE = 4       # Pen/  继续路径
```
# PEN_CONTINUE = 4       # Pen/  继续路径

```python

```
# 空行

```python
    def __init__(self):
```
# def __init__(self):

```python
        super().__init__(ToolType.PEN)
```
# super().__init__(ToolType.PEN)

```python
        self._current_path: PathItem | None = None
```
# self._current_path: PathItem | None = None

```python
        self._drawing: bool = False          # 正在拖拽中（创建平滑点）
```
# self._drawing: bool = False          # 正在拖拽中（创建平滑点）

```python
        self._hover_state: int = PenTool.PEN_DEFAULT
```
# self._hover_state: int = PenTool.PEN_DEFAULT

```python

```
# 空行

```python
        # 拖拽状态
```
# 源代码注释：拖拽状态

```python
        self._drag_start_pos: QPointF | None = None
```
# self._drag_start_pos: QPointF | None = None

```python
        self._is_dragging_handle: bool = False
```
# self._is_dragging_handle: bool = False

```python
        self._dragged_anchor_idx: int = -1
```
# self._dragged_anchor_idx: int = -1

```python
        self._dragged_handle_side: str = ''
```
# self._dragged_handle_side: str = ''

```python

```
# 空行

```python
        # 隐藏功能状态
```
# 源代码注释：隐藏功能状态

```python
        self._alt_adjusting: bool = False     # Alt 调整单侧方向线
```
# self._alt_adjusting: bool = False     # Alt 调整单侧方向线

```python
        self._space_moving: bool = False       # Space 移动当前锚点
```
# self._space_moving: bool = False       # Space 移动当前锚点

```python
        self._space_start_pos: QPointF | None = None
```
# self._space_start_pos: QPointF | None = None

```python
        self._ctrl_temp_select: bool = False   # Ctrl 临时直接选择
```
# self._ctrl_temp_select: bool = False   # Ctrl 临时直接选择

```python
        self._ctrl_drag_start: QPointF | None = None
```
# self._ctrl_drag_start: QPointF | None = None

```python

```
# 空行

```python
    # ── 辅助方法 ──
```
# 分隔注释：辅助方法 —— 用于视觉分组

```python

```
# 空行

```python
    def _snap_angle(self, dx: float, dy: float) -> tuple[float, float]:
```
# def _snap_angle(self, dx: float, dy: float) -> tuple[float, float]:

```python
        """Shift约束角度到最近的45度增量"""
```
# """Shift约束角度到最近的45度增量"""

```python
        angle = math.atan2(dy, dx)
```
# angle = math.atan2(dy, dx)

```python
        step_rad = math.radians(PenTool.SHIFT_ANGLE_STEP)
```
# step_rad = math.radians(PenTool.SHIFT_ANGLE_STEP)

```python
        snapped = round(angle / step_rad) * step_rad
```
# snapped = round(angle / step_rad) * step_rad

```python
        length = math.sqrt(dx*dx + dy*dy)
```
# length = math.sqrt(dx*dx + dy*dy)

```python
        return (math.cos(snapped) * length, math.sin(snapped) * length)
```
# return (math.cos(snapped) * length, math.sin(snapped) * length)

```python

```
# 空行

```python
    def _detect_hover_state(self, pos: QPointF, doc) -> int:
```
# def _detect_hover_state(self, pos: QPointF, doc) -> int:

```python
        """检测悬停位置，返回钢笔光标状态"""
```
# """检测悬停位置，返回钢笔光标状态"""

```python
        # 遍历所有可见图层的路径项
```
# 源代码注释：遍历所有可见图层的路径项

```python
        for layer in reversed(doc.layers):
```
# for layer in reversed(doc.layers):

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
# 空行

```python
                # 1) 检测锚点 → Pen-
```
# 源代码注释：1) 检测锚点 → Pen-

```python
                anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
```
# 调用 PathItem 的 `get_anchor_at` 方法检测鼠标是否命中某个锚点

```python
                if anchor_idx >= 0:
```
# if anchor_idx >= 0:

```python
                    # 如果是当前正在绘制的路径的锚点，继续判断
```
# 源代码注释：如果是当前正在绘制的路径的锚点，继续判断

```python
                    if item is self._current_path:
```
# if item is self._current_path:

```python
                        # 起始锚点 → Pen○ 闭合
```
# 源代码注释：起始锚点 → Pen○ 闭合

```python
                        if anchor_idx == 0 and len(item.anchors) >= 2:
```
# if anchor_idx == 0 and len(item.anchors) >= 2:

```python
                            return PenTool.PEN_CLOSE
```
# return PenTool.PEN_CLOSE

```python
                        # 端点 → Pen/ 继续
```
# 源代码注释：端点 → Pen/ 继续

```python
                        if anchor_idx == len(item.anchors) - 1:
```
# if anchor_idx == len(item.anchors) - 1:

```python
                            return PenTool.PEN_CONTINUE
```
# return PenTool.PEN_CONTINUE

```python
                    return PenTool.PEN_MINUS
```
# return PenTool.PEN_MINUS

```python

```
# 空行

```python
                # 2) 检测路径段 → Pen+
```
# 源代码注释：2) 检测路径段 → Pen+

```python
                seg_idx = item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)
```
# 调用 PathItem 的 `get_segment_at` 方法检测鼠标是否在路径段附近

```python
                if seg_idx >= 0:
```
# if seg_idx >= 0:

```python
                    return PenTool.PEN_PLUS
```
# return PenTool.PEN_PLUS

```python

```
# 空行

```python
        # 3) 如果当前有路径且接近起始点 → Pen○
```
# 源代码注释：3) 如果当前有路径且接近起始点 → Pen○

```python
        if self._current_path and len(self._current_path.anchors) >= 2:
```
# if self._current_path and len(self._current_path.anchors) >= 2:

```python
            first = self._current_path.anchors[0]
```
# first = self._current_path.anchors[0]

```python
            dist = math.sqrt((pos.x() - first.x)**2 + (pos.y() - first.y)**2)
```
# dist = math.sqrt((pos.x() - first.x)**2 + (pos.y() - first.y)**2)

```python
            if dist < PenTool.CLOSE_TOLERANCE:
```
# if dist < PenTool.CLOSE_TOLERANCE:

```python
                return PenTool.PEN_CLOSE
```
# return PenTool.PEN_CLOSE

```python

```
# 空行

```python
        return PenTool.PEN_DEFAULT
```
# return PenTool.PEN_DEFAULT

```python

```
# 空行

```python
    # ── 鼠标事件 ──
```
# 分隔注释：鼠标事件 —— 用于视觉分组

```python

```
# 空行

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# def mouse_press(self, pos: QPointF, modifiers: int):

```python
        if not self._document:
```
# if not self._document:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        doc = self._document
```
# doc = self._document

```python
        is_alt = bool(modifiers & Qt.AltModifier)
```
# is_alt = bool(modifiers & Qt.AltModifier)

```python
        is_ctrl = bool(modifiers & Qt.ControlModifier)
```
# is_ctrl = bool(modifiers & Qt.ControlModifier)

```python
        is_shift = bool(modifiers & Qt.ShiftModifier)
```
# is_shift = bool(modifiers & Qt.ShiftModifier)

```python

```
# 空行

```python
        # ── Ctrl/Cmd 临时切换直接选择工具 ──
```
# 分隔注释：Ctrl/Cmd 临时切换直接选择工具 —— 用于视觉分组

```python
        if is_ctrl:
```
# if is_ctrl:

```python
            self._ctrl_temp_select = True
```
# self._ctrl_temp_select = True

```python
            self._ctrl_drag_start = QPointF(pos)
```
# self._ctrl_drag_start = QPointF(pos)

```python
            # 查找点击位置的路径项和锚点
```
# 源代码注释：查找点击位置的路径项和锚点

```python
            for layer in reversed(doc.layers):
```
# for layer in reversed(doc.layers):

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
# 调用 PathItem 的 `get_anchor_at` 方法检测鼠标是否命中某个锚点

```python
                    if anchor_idx >= 0:
```
# if anchor_idx >= 0:

```python
                        self._dragged_anchor_idx = anchor_idx
```
# self._dragged_anchor_idx = anchor_idx

```python
                        # 临时将该路径设为当前编辑路径
```
# 源代码注释：临时将该路径设为当前编辑路径

```python
                        self._current_path = item
```
# self._current_path = item

```python
                        return
```
# 提前返回，不再继续后续检测

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── 检测悬停状态决定行为 ──
```
# 分隔注释：检测悬停状态决定行为 —— 用于视觉分组

```python
        hover = self._detect_hover_state(pos, doc)
```
# hover = self._detect_hover_state(pos, doc)

```python

```
# 空行

```python
        # 悬停已有路径的锚点（非当前路径） → 删除锚点（Pen-）
```
# 源代码注释：悬停已有路径的锚点（非当前路径） → 删除锚点（Pen-）

```python
        if hover == PenTool.PEN_MINUS:
```
# if hover == PenTool.PEN_MINUS:

```python
            self._try_delete_anchor(pos, doc)
```
# self._try_delete_anchor(pos, doc)

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # 悬停已有路径段 → 添加锚点（Pen+）
```
# 源代码注释：悬停已有路径段 → 添加锚点（Pen+）

```python
        if hover == PenTool.PEN_PLUS:
```
# if hover == PenTool.PEN_PLUS:

```python
            self._try_add_anchor(pos, doc)
```
# self._try_add_anchor(pos, doc)

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # 悬停当前路径起始锚点 → 闭合路径（Pen○）
```
# 源代码注释：悬停当前路径起始锚点 → 闭合路径（Pen○）

```python
        if hover == PenTool.PEN_CLOSE and self._current_path:
```
# if hover == PenTool.PEN_CLOSE and self._current_path:

```python
            self._close_path()
```
# self._close_path()

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── 正常绘制模式 ──
```
# 分隔注释：正常绘制模式 —— 用于视觉分组

```python
        # 如果没有当前路径，创建新路径
```
# 源代码注释：如果没有当前路径，创建新路径

```python
        if self._current_path is None:
```
# if self._current_path is None:

```python
            self._current_path = PathItem()
```
# self._current_path = PathItem()

```python
            self._current_path.style.fill_color = QColor(200, 200, 200, 100)
```
# self._current_path.style.fill_color = QColor(200, 200, 200, 100)

```python
            self._current_path.style.stroke_color = QColor(50, 50, 50)
```
# self._current_path.style.stroke_color = QColor(50, 50, 50)

```python
            self._current_path.style.stroke_width = 2.0
```
# self._current_path.style.stroke_width = 2.0

```python
            doc.add_item(self._current_path)
```
# doc.add_item(self._current_path)

```python

```
# 空行

```python
        # 记录拖拽起始位置
```
# 源代码注释：记录拖拽起始位置

```python
        self._drag_start_pos = QPointF(pos)
```
# self._drag_start_pos = QPointF(pos)

```python
        self._drawing = True
```
# self._drawing = True

```python

```
# 空行

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
# def mouse_move(self, pos: QPointF, modifiers: int):

```python
        if not self._document:
```
# if not self._document:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        is_alt = bool(modifiers & Qt.AltModifier)
```
# is_alt = bool(modifiers & Qt.AltModifier)

```python
        is_ctrl = bool(modifiers & Qt.ControlModifier)
```
# is_ctrl = bool(modifiers & Qt.ControlModifier)

```python
        is_shift = bool(modifiers & Qt.ShiftModifier)
```
# is_shift = bool(modifiers & Qt.ShiftModifier)

```python
        is_space = bool(modifiers & Qt.Key_Space if hasattr(Qt, 'Key_Space') else False)
```
# is_space = bool(modifiers & Qt.Key_Space if hasattr(Qt, 'Key_Space') else False)

```python

```
# 空行

```python
        # ── Ctrl 临时直接选择：移动锚点 ──
```
# 分隔注释：Ctrl 临时直接选择：移动锚点 —— 用于视觉分组

```python
        if self._ctrl_temp_select and self._current_path and self._ctrl_drag_start:
```
# if self._ctrl_temp_select and self._current_path and self._ctrl_drag_start:

```python
            dx = pos.x() - self._ctrl_drag_start.x()
```
# dx = pos.x() - self._ctrl_drag_start.x()

```python
            dy = pos.y() - self._ctrl_drag_start.y()
```
# dy = pos.y() - self._ctrl_drag_start.y()

```python
            if self._dragged_anchor_idx >= 0 and self._dragged_anchor_idx < self._current_path.anchor_count:
```
# if self._dragged_anchor_idx >= 0 and self._dragged_anchor_idx < self._current_path.anchor_count:

```python
                self._current_path.move_anchor(
```
# self._current_path.move_anchor(

```python
                    self._dragged_anchor_idx,
```
# self._dragged_anchor_idx,

```python
                    self._current_path.anchors[self._dragged_anchor_idx].x + dx,
```
# self._current_path.anchors[self._dragged_anchor_idx].x + dx,

```python
                    self._current_path.anchors[self._dragged_anchor_idx].y + dy,
```
# self._current_path.anchors[self._dragged_anchor_idx].y + dy,

```python
                )
```
# 导入结束括号

```python
            self._ctrl_drag_start = QPointF(pos)
```
# self._ctrl_drag_start = QPointF(pos)

```python
            self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── Space 移动当前锚点（仅在拖拽中） ──
```
# 分隔注释：Space 移动当前锚点（仅在拖拽中） —— 用于视觉分组

```python
        if self._space_moving and self._current_path and self._space_start_pos:
```
# if self._space_moving and self._current_path and self._space_start_pos:

```python
            dx = pos.x() - self._space_start_pos.x()
```
# dx = pos.x() - self._space_start_pos.x()

```python
            dy = pos.y() - self._space_start_pos.y()
```
# dy = pos.y() - self._space_start_pos.y()

```python
            last_idx = self._current_path.anchor_count - 1
```
# last_idx = self._current_path.anchor_count - 1

```python
            if last_idx >= 0:
```
# if last_idx >= 0:

```python
                anchor = self._current_path.anchors[last_idx]
```
# anchor = self._current_path.anchors[last_idx]

```python
                self._current_path.move_anchor(last_idx, anchor.x + dx, anchor.y + dy)
```
# self._current_path.move_anchor(last_idx, anchor.x + dx, anchor.y + dy)

```python
            self._space_start_pos = QPointF(pos)
```
# self._space_start_pos = QPointF(pos)

```python
            self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── 更新悬停光标状态 ──
```
# 分隔注释：更新悬停光标状态 —— 用于视觉分组

```python
        if not self._drawing:
```
# if not self._drawing:

```python
            self._hover_state = self._detect_hover_state(pos, self._document)
```
# self._hover_state = self._detect_hover_state(pos, self._document)

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── 拖拽中：实时更新最后一个锚点的手柄 ──
```
# 分隔注释：拖拽中：实时更新最后一个锚点的手柄 —— 用于视觉分组

```python
        if self._drawing and self._drag_start_pos and self._current_path:
```
# if self._drawing and self._drag_start_pos and self._current_path:

```python
            last_idx = self._current_path.anchor_count - 1
```
# last_idx = self._current_path.anchor_count - 1

```python
            if last_idx >= 0:
```
# if last_idx >= 0:

```python
                dx = pos.x() - self._drag_start_pos.x()
```
# dx = pos.x() - self._drag_start_pos.x()

```python
                dy = pos.y() - self._drag_start_pos.y()
```
# dy = pos.y() - self._drag_start_pos.y()

```python

```
# 空行

```python
                # Shift 约束角度
```
# 源代码注释：Shift 约束角度

```python
                if is_shift and (dx != 0 or dy != 0):
```
# if is_shift and (dx != 0 or dy != 0):

```python
                    dx, dy = self._snap_angle(dx, dy)
```
# dx, dy = self._snap_angle(dx, dy)

```python

```
# 空行

```python
                # 拖拽距离小于阈值：视为角点（无手柄）
```
# 源代码注释：拖拽距离小于阈值：视为角点（无手柄）

```python
                dist = math.sqrt(dx*dx + dy*dy)
```
# dist = math.sqrt(dx*dx + dy*dy)

```python
                if dist < PenTool.DRAG_THRESHOLD:
```
# if dist < PenTool.DRAG_THRESHOLD:

```python
                    self._current_path.remove_handles(last_idx)
```
# self._current_path.remove_handles(last_idx)

```python
                else:
```
# else:

```python
                    # 创建/更新手柄（平滑点）
```
# 源代码注释：创建/更新手柄（平滑点）

```python
                    if is_alt:
```
# if is_alt:

```python
                        # Alt 键：仅设置 handle_out（单侧控制），handle_in 置空
```
# 源代码注释：Alt 键：仅设置 handle_out（单侧控制），handle_in 置空

```python
                        anchor = self._current_path.anchors[last_idx]
```
# anchor = self._current_path.anchors[last_idx]

```python
                        anchor.handle_out = QPointF(dx, dy)
```
# anchor.handle_out = QPointF(dx, dy)

```python
                        anchor.handle_in = None
```
# anchor.handle_in = None

```python
                        anchor.anchor_type = AnchorPointType.CORNER
```
# anchor.anchor_type = AnchorPointType.CORNER

```python
                        self._current_path._build_path()
```
# self._current_path._build_path()

```python
                    else:
```
# else:

```python
                        # 正常拖拽：创建对称平滑点
```
# 源代码注释：正常拖拽：创建对称平滑点

```python
                        self._current_path.set_handle_out(
```
# self._current_path.set_handle_out(

```python
                            last_idx, dx, dy, constrain_smooth=True
```
# last_idx, dx, dy, constrain_smooth=True

```python
                        )
```
# 导入结束括号

```python

```
# 空行

```python
                self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
# def mouse_release(self, pos: QPointF, modifiers: int):

```python
        if not self._document:
```
# if not self._document:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── Ctrl 临时直接选择：释放 ──
```
# 分隔注释：Ctrl 临时直接选择：释放 —— 用于视觉分组

```python
        if self._ctrl_temp_select:
```
# if self._ctrl_temp_select:

```python
            self._ctrl_temp_select = False
```
# 重置 Ctrl 临时选择标志

```python
            self._ctrl_drag_start = None
```
# self._ctrl_drag_start = None

```python
            self._dragged_anchor_idx = -1
```
# self._dragged_anchor_idx = -1

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        # ── Space 移动锚点：释放 ──
```
# 分隔注释：Space 移动锚点：释放 —— 用于视觉分组

```python
        if self._space_moving:
```
# if self._space_moving:

```python
            self._space_moving = False
```
# 重置 Space 移动标志

```python
            self._space_start_pos = None
```
# self._space_start_pos = None

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        if not self._drawing or self._drag_start_pos is None:
```
# if not self._drawing or self._drag_start_pos is None:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        is_alt = bool(modifiers & Qt.AltModifier)
```
# is_alt = bool(modifiers & Qt.AltModifier)

```python
        is_shift = bool(modifiers & Qt.ShiftModifier)
```
# is_shift = bool(modifiers & Qt.ShiftModifier)

```python

```
# 空行

```python
        dx = pos.x() - self._drag_start_pos.x()
```
# dx = pos.x() - self._drag_start_pos.x()

```python
        dy = pos.y() - self._drag_start_pos.y()
```
# dy = pos.y() - self._drag_start_pos.y()

```python

```
# 空行

```python
        # Shift 约束角度
```
# 源代码注释：Shift 约束角度

```python
        if is_shift and (dx != 0 or dy != 0):
```
# if is_shift and (dx != 0 or dy != 0):

```python
            dx, dy = self._snap_angle(dx, dy)
```
# dx, dy = self._snap_angle(dx, dy)

```python

```
# 空行

```python
        dist = math.sqrt(dx*dx + dy*dy)
```
# dist = math.sqrt(dx*dx + dy*dy)

```python

```
# 空行

```python
        if self._current_path is None:
```
# if self._current_path is None:

```python
            # 不应该到这里
```
# 源代码注释：不应该到这里

```python
            self._drawing = False
```
# self._drawing = False

```python
            self._drag_start_pos = None
```
# self._drag_start_pos = None

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        if dist < PenTool.DRAG_THRESHOLD:
```
# if dist < PenTool.DRAG_THRESHOLD:

```python
            # ── 短拖拽/单击：创建角点（无手柄） ──
```
# 分隔注释：短拖拽/单击：创建角点（无手柄） —— 用于视觉分组

```python
            anchor = AnchorPoint(pos.x(), pos.y(), anchor_type=AnchorPointType.CORNER)
```
# anchor = AnchorPoint(pos.x(), pos.y(), anchor_type=AnchorPointType.CORNER)

```python
            self._current_path.add_anchor(anchor)
```
# self._current_path.add_anchor(anchor)

```python
        else:
```
# else:

```python
            if is_alt:
```
# if is_alt:

```python
                # ── Alt+拖拽：创建不对称点（只有 handle_out） ──
```
# 分隔注释：Alt+拖拽：创建不对称点（只有 handle_out） —— 用于视觉分组

```python
                anchor = AnchorPoint(
```
# anchor = AnchorPoint(

```python
                    self._drag_start_pos.x(), self._drag_start_pos.y(),
```
# self._drag_start_pos.x(), self._drag_start_pos.y(),

```python
                    handle_out=QPointF(dx, dy),
```
# handle_out=QPointF(dx, dy),

```python
                    anchor_type=AnchorPointType.CORNER,
```
# anchor_type=AnchorPointType.CORNER,

```python
                )
```
# 导入结束括号

```python
            else:
```
# else:

```python
                # ── 正常拖拽：创建平滑点（对称手柄） ──
```
# 分隔注释：正常拖拽：创建平滑点（对称手柄） —— 用于视觉分组

```python
                anchor = AnchorPoint(
```
# anchor = AnchorPoint(

```python
                    self._drag_start_pos.x(), self._drag_start_pos.y(),
```
# self._drag_start_pos.x(), self._drag_start_pos.y(),

```python
                    handle_out=QPointF(dx, dy),
```
# handle_out=QPointF(dx, dy),

```python
                    handle_in=QPointF(-dx, -dy),
```
# handle_in=QPointF(-dx, -dy),

```python
                    anchor_type=AnchorPointType.SMOOTH,
```
# anchor_type=AnchorPointType.SMOOTH,

```python
                )
```
# 导入结束括号

```python
            self._current_path.add_anchor(anchor)
```
# self._current_path.add_anchor(anchor)

```python

```
# 空行

```python
        self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python
        self._drawing = False
```
# self._drawing = False

```python
        self._drag_start_pos = None
```
# self._drag_start_pos = None

```python

```
# 空行

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
```
# def mouse_double_click(self, pos: QPointF, modifiers: int):

```python
        """双击结束路径（不闭合）"""
```
# """双击结束路径（不闭合）"""

```python
        if self._current_path:
```
# if self._current_path:

```python
            self._current_path.closed = False
```
# self._current_path.closed = False

```python
            self._current_path._build_path()
```
# self._current_path._build_path()

```python
            self._current_path = None
```
# self._current_path = None

```python
            self._drawing = False
```
# self._drawing = False

```python
            self._drag_start_pos = None
```
# self._drag_start_pos = None

```python

```
# 空行

```python
    # ── 键盘事件 ──
```
# 分隔注释：键盘事件 —— 用于视觉分组

```python

```
# 空行

```python
    def key_press(self, key: int, modifiers: int):
```
# def key_press(self, key: int, modifiers: int):

```python
        if key == Qt.Key_Escape:
```
# if key == Qt.Key_Escape:

```python
            # Escape：取消当前路径
```
# 源代码注释：Escape：取消当前路径

```python
            if self._current_path and self._document:
```
# if self._current_path and self._document:

```python
                self._document.remove_item(self._current_path)
```
# self._document.remove_item(self._current_path)

```python
            self._current_path = None
```
# self._current_path = None

```python
            self._drawing = False
```
# self._drawing = False

```python
            self._drag_start_pos = None
```
# self._drag_start_pos = None

```python
            self._hover_state = PenTool.PEN_DEFAULT
```
# self._hover_state = PenTool.PEN_DEFAULT

```python
        elif key in (Qt.Key_Return, Qt.Key_Enter):
```
# elif key in (Qt.Key_Return, Qt.Key_Enter):

```python
            # Enter/Return：结束路径（不闭合）
```
# 源代码注释：Enter/Return：结束路径（不闭合）

```python
            if self._current_path:
```
# if self._current_path:

```python
                self._current_path.closed = False
```
# self._current_path.closed = False

```python
                self._current_path._build_path()
```
# self._current_path._build_path()

```python
                self._current_path = None
```
# self._current_path = None

```python
                self._drawing = False
```
# self._drawing = False

```python
                self._drag_start_pos = None
```
# self._drag_start_pos = None

```python
                self._hover_state = PenTool.PEN_DEFAULT
```
# self._hover_state = PenTool.PEN_DEFAULT

```python

```
# 空行

```python
    # ── 辅助操作 ──
```
# 分隔注释：辅助操作 —— 用于视觉分组

```python

```
# 空行

```python
    def _close_path(self):
```
# def _close_path(self):

```python
        """闭合当前路径"""
```
# """闭合当前路径"""

```python
        if self._current_path and len(self._current_path.anchors) >= 2:
```
# if self._current_path and len(self._current_path.anchors) >= 2:

```python
            self._current_path.closed = True
```
# self._current_path.closed = True

```python
            self._current_path._build_path()
```
# self._current_path._build_path()

```python
        self._current_path = None
```
# self._current_path = None

```python
        self._drawing = False
```
# self._drawing = False

```python
        self._drag_start_pos = None
```
# self._drag_start_pos = None

```python

```
# 空行

```python
    def _try_delete_anchor(self, pos: QPointF, doc):
```
# def _try_delete_anchor(self, pos: QPointF, doc):

```python
        """尝试删除悬停的锚点（Pen-行为）"""
```
# """尝试删除悬停的锚点（Pen-行为）"""

```python
        for layer in reversed(doc.layers):
```
# for layer in reversed(doc.layers):

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
# for item in list(layer.items):

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
# 调用 PathItem 的 `get_anchor_at` 方法检测鼠标是否命中某个锚点

```python
                if anchor_idx >= 0 and item.anchor_count > 2:
```
# if anchor_idx >= 0 and item.anchor_count > 2:

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
# old_anchors = [a.copy() for a in item.anchors]

```python
                    item.remove_anchor(anchor_idx)
```
# item.remove_anchor(anchor_idx)

```python
                    new_anchors = [a.copy() for a in item.anchors]
```
# new_anchors = [a.copy() for a in item.anchors]

```python
                    cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)
```
# cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)

```python
                    doc.execute_command(cmd)
```
# doc.execute_command(cmd)

```python
                    return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
    def _try_add_anchor(self, pos: QPointF, doc):
```
# def _try_add_anchor(self, pos: QPointF, doc):

```python
        """尝试在路径段上添加锚点（Pen+行为）"""
```
# """尝试在路径段上添加锚点（Pen+行为）"""

```python
        for layer in reversed(doc.layers):
```
# for layer in reversed(doc.layers):

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
# for item in list(layer.items):

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
# 调用 PathItem 的 `get_segment_at` 方法检测鼠标是否在路径段附近

```python
                if seg_idx >= 0:
```
# if seg_idx >= 0:

```python
                    # 找到段上的精确插入位置
```
# 源代码注释：找到段上的精确插入位置

```python
                    cx, cy = item.get_closest_point_on_segment(seg_idx, pos.x(), pos.y())
```
# cx, cy = item.get_closest_point_on_segment(seg_idx, pos.x(), pos.y())

```python
                    # 在段后插入新锚点
```
# 源代码注释：在段后插入新锚点

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
# old_anchors = [a.copy() for a in item.anchors]

```python
                    new_anchor = AnchorPoint(cx, cy, anchor_type=AnchorPointType.CORNER)
```
# new_anchor = AnchorPoint(cx, cy, anchor_type=AnchorPointType.CORNER)

```python
                    item.insert_anchor(seg_idx + 1, new_anchor)
```
# item.insert_anchor(seg_idx + 1, new_anchor)

```python
                    new_anchors = [a.copy() for a in item.anchors]
```
# new_anchors = [a.copy() for a in item.anchors]

```python
                    cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)
```
# cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)

```python
                    doc.execute_command(cmd)
```
# doc.execute_command(cmd)

```python
                    return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
    # ── 绘制预览 ──
```
# 分隔注释：绘制预览 —— 用于视觉分组

```python

```
# 空行

```python
    def draw_preview(self, painter: QPainter):
```
# def draw_preview(self, painter: QPainter):

```python
        """绘制钢笔工具预览：
```
# """绘制钢笔工具预览：

```python
        - 已放置的锚点
```
# - 已放置的锚点

```python
        - 路径线段
```
# - 路径线段

```python
        - 拖拽中的手柄预览
```
# - 拖拽中的手柄预览

```python
        - 悬停光标指示
```
# - 悬停光标指示

```python
        """
```
# 三引号字符串开始 —— 模块文档字符串

```python
        if not self._current_path:
```
# if not self._current_path:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        anchors = self._current_path.anchors
```
# anchors = self._current_path.anchors

```python
        if not anchors:
```
# if not anchors:

```python
            return
```
# 提前返回，不再继续后续检测

```python

```
# 空行

```python
        scale = max(painter.transform().m11(), 0.001)
```
# scale = max(painter.transform().m11(), 0.001)

```python

```
# 空行

```python
        # ── 绘制已放置的锚点 ──
```
# 分隔注释：绘制已放置的锚点 —— 用于视觉分组

```python
        for i, anchor in enumerate(anchors):
```
# for i, anchor in enumerate(anchors):

```python
            pt = QPointF(anchor.x, anchor.y)
```
# pt = QPointF(anchor.x, anchor.y)

```python

```
# 空行

```python
            # 锚点圆圈
```
# 源代码注释：锚点圆圈

```python
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
```
# painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))

```python
            painter.setBrush(QColor(255, 255, 255))
```
# painter.setBrush(QColor(255, 255, 255))

```python
            painter.drawEllipse(pt, 3 / scale, 3 / scale)
```
# painter.drawEllipse(pt, 3 / scale, 3 / scale)

```python

```
# 空行

```python
            # 手柄线（handle_in）
```
# 源代码注释：手柄线（handle_in）

```python
            if anchor.handle_in:
```
# if anchor.handle_in:

```python
                hin = QPointF(anchor.x + anchor.handle_in.x(), 
```
# hin = QPointF(anchor.x + anchor.handle_in.x(),

```python
                             anchor.y + anchor.handle_in.y())
```
# anchor.y + anchor.handle_in.y())

```python
                pen = QPen(QColor(0, 120, 215), 0.8 / scale)
```
# pen = QPen(QColor(0, 120, 215), 0.8 / scale)

```python
                pen.setStyle(Qt.DashLine)
```
# pen.setStyle(Qt.DashLine)

```python
                painter.setPen(pen)
```
# painter.setPen(pen)

```python
                painter.drawLine(pt, hin)
```
# painter.drawLine(pt, hin)

```python
                # 手柄端点
```
# 源代码注释：手柄端点

```python
                painter.setBrush(QColor(255, 255, 255))
```
# painter.setBrush(QColor(255, 255, 255))

```python
                painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))
```
# painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))

```python
                painter.drawEllipse(hin, 2.5 / scale, 2.5 / scale)
```
# painter.drawEllipse(hin, 2.5 / scale, 2.5 / scale)

```python

```
# 空行

```python
            # 手柄线（handle_out）
```
# 源代码注释：手柄线（handle_out）

```python
            if anchor.handle_out:
```
# if anchor.handle_out:

```python
                hout = QPointF(anchor.x + anchor.handle_out.x(), 
```
# hout = QPointF(anchor.x + anchor.handle_out.x(),

```python
                              anchor.y + anchor.handle_out.y())
```
# anchor.y + anchor.handle_out.y())

```python
                painter.setPen(QPen(QColor(0, 120, 215), 0.8 / scale))
```
# painter.setPen(QPen(QColor(0, 120, 215), 0.8 / scale))

```python
                painter.drawLine(pt, hout)
```
# painter.drawLine(pt, hout)

```python
                # 手柄端点
```
# 源代码注释：手柄端点

```python
                painter.setBrush(QColor(255, 255, 255))
```
# painter.setBrush(QColor(255, 255, 255))

```python
                painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))
```
# painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))

```python
                painter.drawEllipse(hout, 2.5 / scale, 2.5 / scale)
```
# painter.drawEllipse(hout, 2.5 / scale, 2.5 / scale)

```python

```
# 空行

```python
        # ── 绘制路径线段 ──
```
# 分隔注释：绘制路径线段 —— 用于视觉分组

```python
        if len(anchors) >= 2:
```
# if len(anchors) >= 2:

```python
            pen = QPen(QColor(0, 120, 215), 1.5 / scale)
```
# pen = QPen(QColor(0, 120, 215), 1.5 / scale)

```python
            painter.setPen(pen)
```
# painter.setPen(pen)

```python
            painter.setBrush(Qt.NoBrush)
```
# painter.setBrush(Qt.NoBrush)

```python

```
# 空行

```python
            for i in range(len(anchors) - 1):
```
# for i in range(len(anchors) - 1):

```python
                prev, curr = anchors[i], anchors[i + 1]
```
# prev, curr = anchors[i], anchors[i + 1]

```python
                samples = PathItem._sample_bezier_segment(prev, curr, num_samples=30)
```
# samples = PathItem._sample_bezier_segment(prev, curr, num_samples=30)

```python
                for k in range(len(samples) - 1):
```
# for k in range(len(samples) - 1):

```python
                    p1 = QPointF(samples[k][0], samples[k][1])
```
# p1 = QPointF(samples[k][0], samples[k][1])

```python
                    p2 = QPointF(samples[k+1][0], samples[k+1][1])
```
# p2 = QPointF(samples[k+1][0], samples[k+1][1])

```python
                    painter.drawLine(p1, p2)
```
# painter.drawLine(p1, p2)

```python

```
# 空行

```python
        # ── 拖拽中：绘制从最后一个锚点出发的预览手柄 ──
```
# 分隔注释：拖拽中：绘制从最后一个锚点出发的预览手柄 —— 用于视觉分组

```python
        if self._drawing and self._drag_start_pos:
```
# if self._drawing and self._drag_start_pos:

```python
            last_anchor = anchors[-1]
```
# last_anchor = anchors[-1]

```python
            last_pt = QPointF(last_anchor.x, last_anchor.y)
```
# last_pt = QPointF(last_anchor.x, last_anchor.y)

```python

```
# 空行

```python
            # 手柄线预览
```
# 源代码注释：手柄线预览

```python
            painter.setPen(QPen(QColor(0, 120, 215, 150), 0.8 / scale, Qt.DashLine))
```
# painter.setPen(QPen(QColor(0, 120, 215, 150), 0.8 / scale, Qt.DashLine))

```python
            painter.drawLine(last_pt, self._drag_start_pos)
```
# painter.drawLine(last_pt, self._drag_start_pos)

```python

```
# 空行

```python
            # 预览锚点
```
# 源代码注释：预览锚点

```python
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
```
# painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))

```python
            painter.setBrush(QColor(0, 120, 215, 100))
```
# painter.setBrush(QColor(0, 120, 215, 100))

```python
            painter.drawEllipse(self._drag_start_pos, 3 / scale, 3 / scale)
```
# painter.drawEllipse(self._drag_start_pos, 3 / scale, 3 / scale)

```python

```
# 空行

```python
        # ── 悬停光标指示（在第一个锚点上绘制闭合图标） ──
```
# 分隔注释：悬停光标指示（在第一个锚点上绘制闭合图标） —— 用于视觉分组

```python
        if self._hover_state == PenTool.PEN_CLOSE and len(anchors) >= 2:
```
# if self._hover_state == PenTool.PEN_CLOSE and len(anchors) >= 2:

```python
            first_pt = QPointF(anchors[0].x, anchors[0].y)
```
# first_pt = QPointF(anchors[0].x, anchors[0].y)

```python
            painter.setPen(QPen(QColor(0, 120, 215), 2 / scale))
```
# painter.setPen(QPen(QColor(0, 120, 215), 2 / scale))

```python
            painter.setBrush(Qt.NoBrush)
```
# painter.setBrush(Qt.NoBrush)

```python
            r = 6 / scale
```
# r = 6 / scale

```python
            painter.drawEllipse(first_pt, r, r)
```
# painter.drawEllipse(first_pt, r, r)

```python

```
# 空行

```python
    def cancel(self):
```
# def cancel(self):

```python
        if self._current_path and self._document:
```
# if self._current_path and self._document:

```python
            self._document.remove_item(self._current_path)
```
# self._document.remove_item(self._current_path)

```python
        self._current_path = None
```
# self._current_path = None

```python
        self._drawing = False
```
# self._drawing = False

```python
        self._drag_start_pos = None
```
# self._drag_start_pos = None

```python
        self._hover_state = PenTool.PEN_DEFAULT
```
# self._hover_state = PenTool.PEN_DEFAULT

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
# super().cancel()

```python

```
# 空行

```python

```
# 空行

```python
# ── 文字工具 ──────────────────────────────────────────────
```
# 分隔注释：文字工具 —— 用于视觉分组

```python

```
# 空行

```python
class TextTool(BaseTool):
```
# 定义 `TextTool` 文字工具类：继承 `BaseTool`，点击画布创建文字框

```python
    """文字工具 —— 点击创建文字"""
```
# """文字工具 —— 点击创建文字"""

```python
    __slots__ = ()
```
# __slots__ = ()

```python

```
# 空行

```python
    def __init__(self):
```
# def __init__(self):

```python
        super().__init__(ToolType.TEXT)
```
# super().__init__(ToolType.TEXT)

```python

```
# 空行

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
# def mouse_press(self, pos: QPointF, modifiers: int):

```python
        if not self._document:
```
# if not self._document:

```python
            return
```
# 提前返回，不再继续后续检测

```python
        text_frame = TextFrame(pos.x(), pos.y())
```
# text_frame = TextFrame(pos.x(), pos.y())

```python
        text_frame.contents = "文字"
```
# text_frame.contents = "文字"

```python
        text_frame.char_attrs.font_size = 24
```
# text_frame.char_attrs.font_size = 24

```python
        text_frame.char_attrs.fill_color = QColor(50, 50, 50)
```
# text_frame.char_attrs.fill_color = QColor(50, 50, 50)

```python
        text_frame.style.fill_color = None
```
# text_frame.style.fill_color = None

```python
        text_frame.selected = True
```
# text_frame.selected = True

```python
        self._document.clear_selection()
```
# 调用文档方法清除所有图形项的选中状态

```python
        self._document.add_item(text_frame)
```
# self._document.add_item(text_frame)

```python
        self._document.modified = True
```
# 标记文档已被修改（触发重绘和保存提示）

```python

```
# 空行

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
```
# def mouse_double_click(self, pos: QPointF, modifiers: int):

```python
        pass  # 由 UI 层处理
```
# pass  # 由 UI 层处理

```python

```
# 空行

```python

```
# 空行

```python
# ── 抓手工具 ──────────────────────────────────────────────
```
# 分隔注释：抓手工具 —— 用于视觉分组

```python

```
# 空行

```python
class HandTool(BaseTool):
```
# 定义 `HandTool` 抓手工具类：继承 `BaseTool`，拖拽平移画布视图

```python
    """抓手工具 —— 拖拽平移画布"""
```
# """抓手工具 —— 拖拽平移画布"""

```python
    __slots__ = ()
```
# __slots__ = ()

```python

```
# 空行

```python
    def __init__(self):
```
# def __init__(self):

```python
        super().__init__(ToolType.HAND)
```
# super().__init__(ToolType.HAND)

