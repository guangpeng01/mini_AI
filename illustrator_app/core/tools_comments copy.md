@# tools.py 中文注解翻译

```python
"""
```
# 三引号字符串开始——模块文档字符串

```python
工具系统 (Python 3.10+) —— 选择、矩形、椭圆、钢笔、文字工具
```
# 工具系统（Python 3.10+版本）——包含选择工具、矩形工具、椭圆工具、钢笔工具、文字工具

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
# - 使用 __slots__ 机制减少实例内存占用

```python
- 使用 X | None 替代 Optional[X]
```
# - 使用 X | None 语法替代 Optional[X] 类型注解（Python 3.10+特性）

```python
- 使用 match-case 替代 if-elif 链
```
# - 使用 match-case 模式匹配替代 if-elif 条件链（Python 3.10+特性）

```python
- 使用 @override 风格注释 (PEP 698 ready)
```
# - 使用 @override 风格注释（为 PEP 698 做准备）

```python
"""
```
# 三引号字符串结束——模块文档字符串

```python
```
# 空行

```python
from __future__ import annotations
```
# 从 __future__ 模块导入 annotations 注解特性（允许延迟评估类型注解）

```python
```
# 空行

```python
import math
```
# 导入 math 数学运算标准库

```python
from abc import ABC, abstractmethod
```
# 从 abc（抽象基类）模块导入 ABC 抽象基类和 abstractmethod 抽象方法装饰器

```python
from enum import Enum, auto
```
# 从 enum 模块导入 Enum 枚举类和 auto 自动枚举值分配函数

```python
```
# 空行

```python
from PyQt5.QtCore import QPointF, QRectF, Qt
```
# 从 PyQt5.QtCore 模块导入 QPointF 二维浮点坐标点、QRectF 浮点矩形和 Qt 命名空间常量

```python
from PyQt5.QtGui import QColor, QPainter, QPen
```
# 从 PyQt5.QtGui 模块导入 QColor 颜色类、QPainter 绘图器和 QPen 画笔类

```python
```
# 空行

```python
from .graphics import (
```
# 从同级 graphics 子模块导入以下组件：

```python
    GraphicItem, RectangleItem, EllipseItem, TextFrame,
```
#     图形项基类、矩形项、椭圆项、文字框架

```python
    PathItem, GraphicStyle, AnchorPoint, AnchorPointType,
```
#     路径项、图形样式、锚点、锚点类型

```python
    Command, MoveItemsCommand, ModifyAnchorCommand, ResizeItemCommand,
```
#     命令基类、移动多项命令、修改锚点命令、调整尺寸命令

```python
)
```
#     导入语句结束

```python
from .document import Document, Layer
```
# 从同级 document 子模块导入 Document 文档类和 Layer 图层类

---

## ToolType 枚举类（第28-40行）

```python
class ToolType(Enum):
```
# 定义工具类型枚举类

```python
    """工具类型"""
```
#     工具类型文档字符串——定义所有可用工具的枚举

```python
    SELECTION = auto()              # 选择工具 (V)
```
#     选择工具 = 自动分配枚举值              # 快捷键 V

```python
    DIRECT_SELECT = auto()          # 直接选择工具 (A)
```
#     直接选择工具 = 自动分配枚举值          # 快捷键 A

```python
    RECTANGLE = auto()              # 矩形工具 (M)
```
#     矩形工具 = 自动分配枚举值              # 快捷键 M

```python
    ELLIPSE = auto()                # 椭圆工具 (L)
```
#     椭圆工具 = 自动分配枚举值              # 快捷键 L

```python
    PEN = auto()                    # 钢笔工具 (P)
```
#     钢笔工具 = 自动分配枚举值              # 快捷键 P

```python
    ADD_ANCHOR = auto()             # 添加锚点工具 (+)
```
#     添加锚点工具 = 自动分配枚举值           # 快捷键 +

```python
    DELETE_ANCHOR = auto()          # 删除锚点工具 (-)
```
#     删除锚点工具 = 自动分配枚举值           # 快捷键 -

```python
    CONVERT_ANCHOR = auto()         # 转换锚点工具 (Shift+C)
```
#     转换锚点工具 = 自动分配枚举值          # 快捷键 Shift+C

```python
    TEXT = auto()                   # 文字工具 (T)
```
#     文字工具 = 自动分配枚举值               # 快捷键 T

```python
    HAND = auto()                   # 抓手工具 (H)
```
#     抓手工具 = 自动分配枚举值               # 快捷键 H

```python
    ZOOM = auto()                   # 缩放工具 (Z)
```
#     缩放工具 = 自动分配枚举值               # 快捷键 Z

---

## BaseTool 工具基类（第43-78行）

```python
class BaseTool(ABC):
```
# 定义工具基类（抽象基类），继承自 ABC

```python
    """工具基类（抽象）"""
```
#     工具基类文档字符串——所有具体工具的抽象父类

```python
    __slots__ = ('tool_type', '_document', '_is_drawing')
```
#     使用 __slots__ 限定实例属性为：tool_type（工具类型）、_document（文档引用）、_is_drawing（是否正在绘制）

```python
```
#     空行

```python
    def __init__(self, tool_type: ToolType):
```
#     定义构造函数，接受参数：tool_type（工具类型）

```python
        self.tool_type = tool_type
```
#         将传入的 工具类型 赋值给实例属性 工具类型

```python
        self._document: Document | None = None
```
#         初始化 文档引用 属性为空值，类型为 Document 或 None

```python
        self._is_drawing: bool = False
```
#         初始化 是否正在绘制 标志为 False

```python
```
#     空行

```python
    def set_document(self, doc: Document):
```
#     定义设置文档方法，接受参数：doc（文档对象）

```python
        self._document = doc
```
#         将传入的 文档 赋值给实例的私有文档引用

```python
```
#     空行

```python
    @property
```
#     属性装饰器——将方法转为只读属性

```python
    def document(self) -> Document | None:
```
#     定义文档属性访问器，返回值为 Document 或 None

```python
        return self._document
```
#         返回私有文档引用

```python
```
#     空行

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
#     定义鼠标按下事件处理方法，接受参数：pos（鼠标位置），modifiers（修饰键状态）

```python
        pass
```
#         占位——子类中重写

```python
```
#     空行

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
#     定义鼠标移动事件处理方法，接受参数：pos（鼠标位置），modifiers（修饰键状态）

```python
        pass
```
#         占位——子类中重写

```python
```
#     空行

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
#     定义鼠标释放事件处理方法，接受参数：pos（鼠标位置），modifiers（修饰键状态）

```python
        pass
```
#         占位——子类中重写

```python
```
#     空行

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
```
#     定义鼠标双击事件处理方法，接受参数：pos（鼠标位置），modifiers（修饰键状态）

```python
        pass
```
#         占位——子类中重写

```python
```
#     空行

```python
    def key_press(self, key: int, modifiers: int):
```
#     定义键盘按下事件处理方法，接受参数：key（按键码），modifiers（修饰键状态）

```python
        pass
```
#         占位——子类中重写

```python
```
#     空行

```python
    def draw_preview(self, painter: QPainter):
```
#     定义绘制预览方法，接受参数：painter（绘图器对象）

```python
        pass
```
#         占位——子类中重写

```python
```
#     空行

```python
    def cancel(self):
```
#     定义取消操作方法

```python
        self._is_drawing = False
```
#         将 是否正在绘制 标志重置为 False

---

## ResizeHandleType 缩放手柄类型枚举（第83-92行）

```python
class ResizeHandleType(Enum):
```
# 定义缩放手柄类型枚举类

```python
    """缩放手柄位置类型"""
```
#     缩放手柄位置类型文档字符串

```python
    TOP_LEFT = auto()
```
#     左上角 = 自动分配枚举值

```python
    TOP_CENTER = auto()
```
#     顶部居中 = 自动分配枚举值

```python
    TOP_RIGHT = auto()
```
#     右上角 = 自动分配枚举值

```python
    MIDDLE_LEFT = auto()
```
#     左侧居中 = 自动分配枚举值

```python
    MIDDLE_RIGHT = auto()
```
#     右侧居中 = 自动分配枚举值

```python
    BOTTOM_LEFT = auto()
```
#     左下角 = 自动分配枚举值

```python
    BOTTOM_CENTER = auto()
```
#     底部居中 = 自动分配枚举值

```python
    BOTTOM_RIGHT = auto()
```
#     右下角 = 自动分配枚举值

---

## SelectionTool 选择工具（第97-475行）

```python
class SelectionTool(BaseTool):
```
# 定义选择工具类，继承自 BaseTool 工具基类

```python
    """选择工具 —— 点击选择 / 框选 / 多选拖拽 / 缩放手柄"""
```
#     选择工具文档字符串——支持点击选择、框选、多选拖拽和缩放手柄操作

```python
    __slots__ = ('_drag_start', '_drag_current', '_dragging_item',
```
#     使用 __slots__ 限定实例属性为以下变量：

```python
                 '_drag_offset', '_is_marquee',
```
#                  拖拽偏移量、是否框选模式

```python
                 '_dragging_items', '_drag_offsets',
```
#                  多选拖拽的图形项列表、多选拖拽的偏移量列表

```python
                 '_total_dx', '_total_dy',
```
#                  累计水平位移、累计垂直位移

```python
                 '_is_scaling', '_scale_handle',
```
#                  是否正在缩放、缩放手柄类型

```python
                 '_scale_orig_rect', '_scale_orig_br',
```
#                  缩放原始矩形、缩放前边界矩形

```python
                 '_scale_pivot', '_scale_keep_ratio')
```
#                  缩放固定锚点、是否保持比例

```python
```
#     空行

```python
    def __init__(self):
```
#     定义选择工具的构造函数

```python
        super().__init__(ToolType.SELECTION)
```
#         调用父类构造函数，传入工具类型为 选择

```python
        self._drag_start: QPointF | None = None
```
#         初始化 拖拽起始位置 为 None

```python
        self._drag_current: QPointF | None = None
```
#         初始化 拖拽当前位置 为 None

```python
        self._dragging_item: GraphicItem | None = None
```
#         初始化 正在拖拽的图形项 为 None

```python
        self._drag_offset = QPointF(0, 0)
```
#         初始化 拖拽偏移量 为原点坐标(0, 0)

```python
        self._is_marquee: bool = False
```
#         初始化 是否框选模式 为 False

```python
        # 多选拖拽支持
```
#         注释：多选拖拽支持相关属性

```python
        self._dragging_items: list[GraphicItem] = []
```
#         初始化 多选拖拽的图形项列表 为空列表

```python
        self._drag_offsets: list[QPointF] = []
```
#         初始化 多选拖拽的偏移量列表 为空列表

```python
        self._total_dx: float = 0.0
```
#         初始化 累计水平位移 为 0.0

```python
        self._total_dy: float = 0.0
```
#         初始化 累计垂直位移 为 0.0

```python
        # 缩放支持
```
#         注释：缩放支持相关属性

```python
        self._is_scaling: bool = False
```
#         初始化 是否正在缩放 为 False

```python
        self._scale_handle: ResizeHandleType | None = None
```
#         初始化 缩放手柄类型 为 None

```python
        self._scale_orig_rect = QRectF()
```
#         初始化 缩放原始矩形 为空矩形

```python
        self._scale_orig_br = QRectF()  # 缩放前 bounding_rect
```
#         初始化 缩放前边界矩形 为空矩形  # 记录缩放前的包围矩形

```python
        self._scale_pivot = QPointF()   # 缩放锚点（对角的那个固定点）
```
#         初始化 缩放固定锚点 为原点坐标   # 缩放的锚点（对角位置的那个固定点）

```python
        self._scale_keep_ratio: bool = False
```
#         初始化 是否保持比例 为 False

```python
```
#     空行

```python
    # ── 手柄检测 ──
```
#     注释：手柄检测方法区域

```python
```
#     空行

```python
    @staticmethod
```
#     静态方法装饰器

```python
    def _get_handle_at(item: GraphicItem, pos: QPointF, tolerance: float = 8) -> ResizeHandleType | None:
```
#     定义检测手柄位置的私有静态方法，接受参数：item（图形项），pos（鼠标位置），tolerance（容差，默认8像素），返回手柄类型或None

```python
        """检测鼠标是否在缩放手柄上（pos 为世界坐标）"""
```
#         文档字符串——检测鼠标是否位于缩放手柄上（pos 参数为世界坐标系坐标）

```python
        local_rect = item.bounding_rect()
```
#         获取图形项的本地坐标系边界矩形

```python
        rect = item._transform.mapRect(local_rect)
```
#         通过图形项的变换矩阵将本地矩形映射到世界坐标矩形

```python
        hs = tolerance  # 手柄命中容差
```
#         将容差赋值给 hs 变量  # 手柄命中的容差范围

```python
        corners = {
```
#         定义四个角手柄的坐标字典：

```python
            ResizeHandleType.TOP_LEFT: rect.topLeft(),
```
#             左上角手柄位置：矩形的左上角

```python
            ResizeHandleType.TOP_RIGHT: rect.topRight(),
```
#             右上角手柄位置：矩形的右上角

```python
            ResizeHandleType.BOTTOM_LEFT: rect.bottomLeft(),
```
#             左下角手柄位置：矩形的左下角

```python
            ResizeHandleType.BOTTOM_RIGHT: rect.bottomRight(),
```
#             右下角手柄位置：矩形的右下角

```python
        }
```
#         字典结束

```python
        edges = {
```
#         定义四条边中点手柄的坐标字典：

```python
            ResizeHandleType.TOP_CENTER: QPointF(rect.center().x(), rect.top()),
```
#             顶部居中手柄位置：矩形顶边的中点

```python
            ResizeHandleType.BOTTOM_CENTER: QPointF(rect.center().x(), rect.bottom()),
```
#             底部居中手柄位置：矩形底边的中点

```python
            ResizeHandleType.MIDDLE_LEFT: QPointF(rect.left(), rect.center().y()),
```
#             左侧居中手柄位置：矩形左边的中点

```python
            ResizeHandleType.MIDDLE_RIGHT: QPointF(rect.right(), rect.center().y()),
```
#             右侧居中手柄位置：矩形右边的中点

```python
        }
```
#         字典结束

```python
```
#         空行

```python
        for htype, pt in corners.items():
```
#         遍历四个角手柄的类型和坐标：

```python
            if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:
```
#             如果鼠标位置与手柄坐标的水平和垂直距离都小于容差：

```python
                return htype
```
#                 返回匹配的手柄类型

```python
        for htype, pt in edges.items():
```
#         遍历四条边中点手柄的类型和坐标：

```python
            if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:
```
#             如果鼠标位置与手柄坐标的水平和垂直距离都小于容差：

```python
                return htype
```
#                 返回匹配的手柄类型

```python
        return None
```
#         未命中任何手柄，返回 None

### 选择工具鼠标事件处理（第158-295行）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
#     定义选择工具的鼠标按下事件处理方法，接受参数：pos（鼠标位置），modifiers（修饰键状态）

```python
        if not self._document:
```
#         如果文档引用不存在：

```python
            return
```
#             直接返回

```python
        self._drag_start = QPointF(pos)
```
#         记录拖拽起始位置为当前鼠标位置

```python
        self._drag_current = QPointF(pos)
```
#         记录拖拽当前位置为当前鼠标位置

```python
        self._total_dx = 0.0
```
#         重置累计水平位移为 0.0

```python
        self._total_dy = 0.0
```
#         重置累计垂直位移为 0.0

```python
        self._is_scaling = False
```
#         重置缩放状态为 False

```python
        self._scale_handle = None
```
#         重置缩放手柄为 None

```python
        self._scale_keep_ratio = bool(modifiers & Qt.ShiftModifier)
```
#         根据是否按住 Shift 键设置是否保持等比缩放

```python
```
#         空行

```python
        # 检查是否点击了已选中项的缩放手柄
```
#         注释：检查是否点击了已选中图形项的缩放手柄

```python
        sel = self._document.get_selection()
```
#         获取文档中当前的选中项列表

```python
        if len(sel) == 1:
```
#         如果只选中了一个图形项：

```python
            handle = self._get_handle_at(sel[0], pos)
```
#             检测该选中项上是否有手柄被点击

```python
            if handle is not None:
```
#             如果命中了缩放手柄：

```python
                self._dragging_item = sel[0]
```
#                 设置正在拖拽的图形项为该选中项

```python
                self._is_scaling = True
```
#                 进入缩放模式

```python
                self._scale_handle = handle
```
#                 记录被拖拽的缩放手柄类型

```python
                # 使用世界坐标系的 bounding_rect（含 item 变换）
```
#                 注释：使用世界坐标系的包围矩形（包含图形项的变换）

```python
                world_rect = sel[0]._transform.mapRect(sel[0].bounding_rect())
```
#                 获取选中项经过变换后的世界坐标矩形

```python
                self._scale_orig_rect = QRectF(world_rect)
```
#                 保存缩放前的原始矩形副本

```python
                self._scale_orig_br = QRectF(world_rect)
```
#                 保存缩放前的边界矩形副本

```python
                # 缩放的固定锚点是对角
```
#                 注释：缩放的固定锚点为对角位置

```python
                self._scale_pivot = self._get_opposite_corner(handle, self._scale_orig_rect)
```
#                 获取手柄对角的固定锚点位置；self._获取对角顶点(句柄, self._原始缩放矩形)

```python
                return
```
#                 返回，不再执行后续逻辑

```python
```
#         空行

```python
        item = self._document.get_item_at(pos.x(), pos.y())
```
#         查找鼠标位置处的图形项

```python
        if item:
```
#         如果找到了图形项：

```python
            # 如果点击的项未被选中，先清除选择并选中它
```
#             注释：如果点击的图形项未被选中，先清除选择并选中它

```python
            if not item.selected:
```
#             如果该图形项未被选中：

```python
                if not (modifiers & Qt.ShiftModifier):
```
#                 如果没有按住 Shift 键：

```python
                    self._document.clear_selection()
```
#                     清除所有已选中项

```python
                item.selected = True
```
#                 将该图形项设为选中状态

```python
            # 如果点击的项已选中（多选状态），进入多选拖拽模式
```
#             注释：如果点击的图形项已选中（多选状态），进入多选拖拽模式

```python
            sel = self._document.get_selection()
```
#             重新获取当前选中项列表

```python
            if len(sel) > 1 and item.selected:
```
#             如果选中了多项且该图形项已被选中：

```python
                self._dragging_items = list(sel)
```
#                 将所有选中项存入多选拖拽列表

```python
                self._drag_offsets = [pos - it._transform.mapRect(it.bounding_rect()).topLeft() for it in sel]
```
#                 计算每个选中项的拖拽偏移量（鼠标位置减去各项世界坐标左上角）

```python
                self._dragging_item = None
```
#                 清除单项拖拽引用

```python
            else:
```
#             否则（单项选中或按住Shift新选中）：

```python
                if not (modifiers & Qt.ShiftModifier):
```
#                 如果没有按住 Shift 键：

```python
                    self._document.clear_selection()
```
#                     清除所有已选中项

```python
                item.selected = True
```
#                 将该图形项设为选中状态

```python
                self._dragging_item = item
```
#                 设置正在拖拽的图形项

```python
                self._drag_offset = pos - item._transform.mapRect(item.bounding_rect()).topLeft()
```
#                 计算单项拖拽偏移量

```python
                self._dragging_items = []
```
#                 清空多选拖拽列表

```python
        else:
```
#         如果没有找到图形项（点击空白区域）：

```python
            if not (modifiers & Qt.ShiftModifier):
```
#             如果没有按住 Shift 键：

```python
                self._document.clear_selection()
```
#                 清除所有已选中项

```python
            self._dragging_item = None
```
#             清除单项拖拽引用

```python
            self._dragging_items = []
```
#             清空多选拖拽列表

```python
            self._is_marquee = True
```
#             进入框选模式

### 选择工具 mouse_move（第212-244行）

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
#     定义选择工具的鼠标移动事件处理方法

```python
        if self._drag_start is None:
```
#         如果没有拖拽起始位置：

```python
            return
```
#             直接返回

```python
        self._drag_current = QPointF(pos)
```
#         更新拖拽当前位置

```python
```
#         空行

```python
        # 缩放模式
```
#         注释：缩放模式处理

```python
        if self._is_scaling and self._dragging_item:
```
#         如果正在缩放且存在拖拽图形项：

```python
            self._apply_resize(pos, bool(modifiers & Qt.ShiftModifier))
```
#             应用缩放变换，传入鼠标位置和是否按住 Shift

```python
            if self._document:
```
#             如果文档引用存在：

```python
                self._document.modified = True
```
#                 标记文档为已修改

```python
            return
```
#             返回，不执行后续拖拽逻辑

```python
```
#         空行

```python
        dx = pos.x() - self._drag_start.x()
```
#         计算水平位移增量

```python
        dy = pos.y() - self._drag_start.y()
```
#         计算垂直位移增量

```python
        # Shift 约束水平/垂直移动
```
#         注释：Shift 键约束为纯水平或纯垂直移动

```python
        if modifiers & Qt.ShiftModifier:
```
#         如果按住 Shift 键：

```python
            dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)
```
#             选择位移较大的方向保留，另一个方向归零

```python
```
#         空行

```python
        if self._dragging_items:
```
#         如果存在多选拖拽列表：

```python
            for item in self._dragging_items:
```
#             遍历所有拖拽中的图形项：

```python
                item.move_by(dx, dy)
```
#                 将每个图形项移动 dx, dy 增量

```python
            self._total_dx += dx
```
#             累加水平位移

```python
            self._total_dy += dy
```
#             累加垂直位移

```python
            self._drag_start = QPointF(pos)
```
#             更新拖拽起始位置为当前位置

```python
            if self._document:
```
#             如果文档引用存在：

```python
                self._document.modified = True
```
#                 标记文档为已修改

```python
        elif self._dragging_item and not self._is_scaling:
```
#         否则如果存在单项拖拽且不在缩放模式：

```python
            self._dragging_item.move_by(dx, dy)
```
#             将图形项移动 dx, dy 增量

```python
            self._total_dx += dx
```
#             累加水平位移

```python
            self._total_dy += dy
```
#             累加垂直位移

```python
            self._drag_start = QPointF(pos)
```
#             更新拖拽起始位置为当前位置

```python
            if self._document:
```
#             如果文档引用存在：

```python
                self._document.modified = True
```
#                 标记文档为已修改

### 选择工具 mouse_release（第246-295行）

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
#     定义选择工具的鼠标释放事件处理方法

```python
        # 缩放完成：记录命令（通过 execute_command 统一入口）
```
#         注释：缩放完成时记录撤销命令（通过 execute_command 统一入口）

```python
        if self._is_scaling and self._dragging_item and self._document:
```
#         如果正在缩放、存在拖拽图形项、且文档存在：

```python
            new_world_rect = self._dragging_item._transform.mapRect(self._dragging_item.bounding_rect())
```
#             获取缩放后的新世界坐标矩形

```python
            if new_world_rect != self._scale_orig_br:
```
#             如果新矩形与缩放前矩形不同（确实发生了尺寸变化）：

```python
                # 通过尺寸变化记录（使用世界坐标矩形）
```
#                 注释：通过尺寸变化记录撤销命令（使用世界坐标矩形）

```python
                cmd = ResizeItemCommand(
```
#                 创建调整尺寸命令：

```python
                    self._document, self._dragging_item,
```
#                     传入文档、目标图形项

```python
                    self._scale_orig_br, new_world_rect,
```
#                     传入原始矩形和新矩形

```python
                )
```
#                 命令创建结束

```python
                self._document.execute_command(cmd)
```
#                 通过文档统一入口执行命令（支持撤销/重做）

```python
            self._is_scaling = False
```
#             重置缩放状态为 False

```python
            self._scale_handle = None
```
#             重置缩放手柄为 None

```python
            self._dragging_item = None
```
#             重置拖拽图形项为 None

```python
            self._drag_start = None
```
#             重置拖拽起始位置

```python
            self._drag_current = None
```
#             重置拖拽当前位置

```python
            self._total_dx = 0.0
```
#             重置累计水平位移

```python
            self._total_dy = 0.0
```
#             重置累计垂直位移

```python
            return
```
#             返回，不执行后续逻辑

```python
```
#         空行

```python
        # 多选拖拽完成后记录移动命令（用于撤销，通过 execute_command 统一入口）
```
#         注释：多选拖拽完成后记录移动命令（用于撤销，通过 execute_command 统一入口）

```python
        moved_items = self._dragging_items if self._dragging_items else (
```
#         确定已移动的图形项列表：优先使用多选拖拽列表，否则使用单项拖拽

```python
            [self._dragging_item] if self._dragging_item else []
```
#             如果存在单项拖拽图形项则包装为列表，否则为空列表

```python
        )
```
#         条件表达式结束

```python
        if moved_items and self._document and (self._total_dx != 0 or self._total_dy != 0):
```
#         如果存在已移动项、文档存在、且累计位移不为零：

```python
            cmd = MoveItemsCommand(
```
#             创建移动多项命令：

```python
                self._document, moved_items,
```
#                 传入文档和已移动图形项列表

```python
                self._total_dx, self._total_dy,
```
#                 传入累计水平和垂直位移

```python
            )
```
#             命令创建结束

```python
            self._document.execute_command(cmd)
```
#             通过文档统一入口执行命令

```python
```
#         空行

```python
        if self._is_marquee and self._drag_start and self._document:
```
#         如果处于框选模式、有起始位置、且文档存在：

```python
            rect = QRectF(self._drag_start, pos).normalized()
```
#             根据起始和结束位置创建规范化矩形

```python
            if rect.width() > 2 and rect.height() > 2:
```
#             如果矩形宽高都大于2像素（排除误触）：

```python
                for layer in self._document.layers:
```
#                 遍历文档的所有图层：

```python
                    items = layer.get_items_in_rect(
```
#                     获取矩形范围内的图形项：

```python
                        rect.x(), rect.y(), rect.width(), rect.height(),
```
#                         传入矩形的 x, y, 宽度, 高度

```python
                    )
```
#                     获取完成

```python
                    for item in items:
```
#                     遍历矩形范围内的图形项：

```python
                        item.selected = True
```
#                         将每个图形项设为选中状态

```python
```
#         空行

```python
        self._drag_start = None
```
#         重置拖拽起始位置

```python
        self._drag_current = None
```
#         重置拖拽当前位置

```python
        self._dragging_item = None
```
#         重置拖拽图形项

```python
        self._dragging_items = []
```
#         清空多选拖拽列表

```python
        self._is_marquee = False
```
#         重置框选模式为 False

```python
        self._is_scaling = False
```
#         重置缩放状态为 False

```python
        self._scale_handle = None
```
#         重置缩放手柄

```python
        self._total_dx = 0.0
```
#         重置累计水平位移

```python
        self._total_dy = 0.0
```
#         重置累计垂直位移

### 选择工具缩放核心方法（第299-424行）

```python
    @staticmethod
```
#     静态方法装饰器

```python
    def _get_opposite_corner(handle: ResizeHandleType, rect: QRectF) -> QPointF:
```
#     定义获取对角固定锚点的私有静态方法，接受参数：handle（手柄类型），rect（矩形），返回对角坐标点

```python
        """获取缩放手柄对面的固定锚点"""
```
#         文档字符串——获取缩放手柄对面的固定锚点坐标

```python
        match handle:
```
#         使用 match-case 模式匹配手柄类型：

```python
            case ResizeHandleType.TOP_LEFT:
```
#             当手柄类型为左上角时：

```python
                return rect.bottomRight()
```
#                 返回右下角坐标（对角固定点）

```python
            case ResizeHandleType.TOP_CENTER:
```
#             当手柄类型为顶部居中时：

```python
                return QPointF(rect.center().x(), rect.bottom())
```
#                 返回底部居中坐标

```python
            case ResizeHandleType.TOP_RIGHT:
```
#             当手柄类型为右上角时：

```python
                return rect.bottomLeft()
```
#                 返回左下角坐标

```python
            case ResizeHandleType.MIDDLE_LEFT:
```
#             当手柄类型为左侧居中时：

```python
                return QPointF(rect.right(), rect.center().y())
```
#                 返回右侧居中坐标

```python
            case ResizeHandleType.MIDDLE_RIGHT:
```
#             当手柄类型为右侧居中时：

```python
                return QPointF(rect.left(), rect.center().y())
```
#                 返回左侧居中坐标

```python
            case ResizeHandleType.BOTTOM_LEFT:
```
#             当手柄类型为左下角时：

```python
                return rect.topRight()
```
#                 返回右上角坐标

```python
            case ResizeHandleType.BOTTOM_CENTER:
```
#             当手柄类型为底部居中时：

```python
                return QPointF(rect.center().x(), rect.top())
```
#                 返回顶部居中坐标

```python
            case ResizeHandleType.BOTTOM_RIGHT:
```
#             当手柄类型为右下角时：

```python
                return rect.topLeft()
```
#                 返回左上角坐标

```python
```
#     空行

```python
    def _apply_resize(self, mouse_pos: QPointF, keep_ratio: bool):
```
#     定义应用缩放的私有方法，接受参数：mouse_pos（鼠标位置），keep_ratio（是否保持比例）

```python
        """根据手柄类型和鼠标位置调整图形大小"""
```
#         文档字符串——根据手柄类型和鼠标位置调整图形的大小

```python
        if not self._dragging_item:
```
#         如果不存在拖拽图形项：

```python
            return
```
#             直接返回

```python
        pivot = self._scale_pivot
```
#         获取缩放固定锚点

```python
        orig = self._scale_orig_rect
```
#         获取缩放前的原始矩形

```python
        mx, my = mouse_pos.x(), mouse_pos.y()
```
#         提取鼠标位置的 x 和 y 坐标

```python
        px, py = pivot.x(), pivot.y()
```
#         提取固定锚点的 x 和 y 坐标

```python
```
#         空行

```python
        # 根据手柄确定新宽高
```
#         注释：根据手柄类型计算新的宽度和高度

```python
        match self._scale_handle:
```
#         使用 match-case 模式匹配缩放手柄类型：

```python
            case ResizeHandleType.TOP_LEFT:
```
#             左上角手柄：

```python
                new_w, new_h = px - mx, py - my
```
#                 新宽度=锚点x - 鼠标x，新高度=锚点y - 鼠标y

```python
            case ResizeHandleType.TOP_CENTER:
```
#             顶部居中手柄：

```python
                new_w = orig.width()
```
#                 宽度保持不变

```python
                new_h = py - my
```
#                 新高度=锚点y - 鼠标y

```python
            case ResizeHandleType.TOP_RIGHT:
```
#             右上角手柄：

```python
                new_w = mx - px
```
#                 新宽度=鼠标x - 锚点x

```python
                new_h = py - my
```
#                 新高度=锚点y - 鼠标y

```python
            case ResizeHandleType.MIDDLE_LEFT:
```
#             左侧居中手柄：

```python
                new_w = px - mx
```
#                 新宽度=锚点x - 鼠标x

```python
                new_h = orig.height()
```
#                 高度保持不变

```python
            case ResizeHandleType.MIDDLE_RIGHT:
```
#             右侧居中手柄：

```python
                new_w = mx - px
```
#                 新宽度=鼠标x - 锚点x

```python
                new_h = orig.height()
```
#                 高度保持不变

```python
            case ResizeHandleType.BOTTOM_LEFT:
```
#             左下角手柄：

```python
                new_w = px - mx
```
#                 新宽度=锚点x - 鼠标x

```python
                new_h = my - py
```
#                 新高度=鼠标y - 锚点y

```python
            case ResizeHandleType.BOTTOM_CENTER:
```
#             底部居中手柄：

```python
                new_w = orig.width()
```
#                 宽度保持不变

```python
                new_h = my - py
```
#                 新高度=鼠标y - 锚点y

```python
            case ResizeHandleType.BOTTOM_RIGHT:
```
#             右下角手柄：

```python
                new_w = mx - px
```
#                 新宽度=鼠标x - 锚点x

```python
                new_h = my - py
```
#                 新高度=鼠标y - 锚点y

```python
            case _:
```
#             其他未知手柄类型：

```python
                return
```
#                 直接返回

```python
```
#         空行

```python
        # 最小尺寸限制
```
#         注释：最小尺寸限制

```python
        new_w = max(new_w, 10)
```
#         新宽度最小为10像素

```python
        new_h = max(new_h, 10)
```
#         新高度最小为10像素

```python
```
#         空行

```python
        # 等比约束
```
#         注释：等比约束处理

```python
        if keep_ratio:
```
#         如果需要保持等比：

```python
            orig_aspect = orig.width() / max(orig.height(), 1)
```
#             计算原始宽高比（避免除以零）

```python
            if self._scale_handle in (
```
#             如果手柄为顶部居中或底部居中（只改变高度）：

```python
                ResizeHandleType.TOP_CENTER, ResizeHandleType.BOTTOM_CENTER,
```
#                 顶部居中、底部居中

```python
            ):
```
#             条件结束：

```python
                new_w = new_h * orig_aspect
```
#                 根据新高度和原始宽高比计算新宽度

```python
            elif self._scale_handle in (
```
#             否则如果手柄为左侧居中或右侧居中（只改变宽度）：

```python
                ResizeHandleType.MIDDLE_LEFT, ResizeHandleType.MIDDLE_RIGHT,
```
#                 左侧居中、右侧居中

```python
            ):
```
#             条件结束：

```python
                new_h = new_w / max(orig_aspect, 0.001)
```
#                 根据新宽度和原始宽高比计算新高度

```python
            else:
```
#             否则（角手柄——宽高都可变）：

```python
                # 角手柄：选择较大的维度保持比例
```
#                 注释：角手柄——选择变化幅度更大的维度来保持比例

```python
                aspect_w = new_h * orig_aspect
```
#                 根据高度按比例计算宽度

```python
                aspect_h = new_w / max(orig_aspect, 0.001)
```
#                 根据宽度按比例计算高度

```python
                if abs(new_w - aspect_w) < abs(new_h - aspect_h):
```
#                 如果宽度方向的偏差更小：

```python
                    new_h = new_w / max(orig_aspect, 0.001)
```
#                     以宽度为准计算高度

```python
                else:
```
#                 否则（高度方向偏差更小）：

```python
                    new_w = new_h * orig_aspect
```
#                     以高度为准计算宽度

```python
```
#         空行

```python
        # 应用缩放
```
#         注释：应用缩放到图形项

```python
        self._resize_item(self._dragging_item, pivot, orig, new_w, new_h)
```
#         调用内部缩放方法，传入图形项、锚点、原始矩形、新宽度、新高度

```python
```
#     空行

```python
    def _resize_item(self, item: GraphicItem, pivot: QPointF,
```
#     定义图形项缩放私有方法，接受参数：item（图形项），pivot（固定锚点），

```python
                     orig_rect: QRectF, new_w: float, new_h: float):
```
#                      orig_rect（原始矩形），new_w（新宽度），new_h（新高度）

```python
        """对不同类型的图形应用尺寸变化"""
```
#         文档字符串——对不同类型的图形项应用尺寸变化

```python
        scale_x = new_w / max(orig_rect.width(), 0.001)
```
#         计算水平缩放比例

```python
        scale_y = new_h / max(orig_rect.height(), 0.001)
```
#         计算垂直缩放比例

```python
```
#         空行

```python
        if isinstance(item, RectangleItem):
```
#         如果图形项是矩形：

```python
            # 矩形：直接修改 rect
```
#             注释：矩形——直接修改矩形属性

```python
            new_x = pivot.x() if pivot.x() < orig_rect.center().x() else pivot.x() - new_w
```
#             根据锚点位置计算新的 x 坐标

```python
            new_y = pivot.y() if pivot.y() < orig_rect.center().y() else pivot.y() - new_h
```
#             根据锚点位置计算新的 y 坐标

```python
            item.rect = QRectF(new_x, new_y, new_w, new_h)
```
#             设置矩形项的新矩形

```python
        elif isinstance(item, EllipseItem):
```
#         否则如果图形项是椭圆：

```python
            # 椭圆：直接修改 rect
```
#             注释：椭圆——直接修改矩形属性

```python
            new_x = pivot.x() if pivot.x() < orig_rect.center().x() else pivot.x() - new_w
```
#             根据锚点位置计算新的 x 坐标

```python
            new_y = pivot.y() if pivot.y() < orig_rect.center().y() else pivot.y() - new_h
```
#             根据锚点位置计算新的 y 坐标

```python
            item.rect = QRectF(new_x, new_y, new_w, new_h)
```
#             设置椭圆项的新矩形

```python
        elif isinstance(item, PathItem):
```
#         否则如果图形项是路径：

```python
            # 路径：缩放所有锚点
```
#             注释：路径——缩放所有锚点坐标

```python
            ref_x = pivot.x() if scale_x > 0 else orig_rect.right()
```
#             确定水平参考点（缩放锚点或右边界）

```python
            ref_y = pivot.y() if scale_y > 0 else orig_rect.bottom()
```
#             确定垂直参考点（缩放锚点或底边界）

```python
            for anchor in item.anchors:
```
#             遍历路径的所有锚点：

```python
                anchor.x = ref_x + (anchor.x - ref_x) * scale_x
```
#                 根据缩放比例计算新的锚点 x 坐标

```python
                anchor.y = ref_y + (anchor.y - ref_y) * scale_y
```
#                 根据缩放比例计算新的锚点 y 坐标

```python
                if anchor.handle_in:
```
#                 如果存在入方向手柄：

```python
                    anchor.handle_in = QPointF(
```
#                     缩放入方向手柄坐标：

```python
                        anchor.handle_in.x() * scale_x,
```
#                         手柄 x 坐标乘以水平缩放比

```python
                        anchor.handle_in.y() * scale_y,
```
#                         手柄 y 坐标乘以垂直缩放比

```python
                    )
```
#                     坐标点创建结束

```python
                if anchor.handle_out:
```
#                 如果存在出方向手柄：

```python
                    anchor.handle_out = QPointF(
```
#                     缩放出方向手柄坐标：

```python
                        anchor.handle_out.x() * scale_x,
```
#                         手柄 x 坐标乘以水平缩放比

```python
                        anchor.handle_out.y() * scale_y,
```
#                         手柄 y 坐标乘以垂直缩放比

```python
                    )
```
#                     坐标点创建结束

```python
            item._rebuild_from_anchors()
```
#             根据更新后的锚点重建路径

```python
        elif isinstance(item, TextFrame):
```
#         否则如果图形项是文字框架：

```python
            new_x = pivot.x() if pivot.x() < orig_rect.center().x() else pivot.x() - new_w
```
#             根据锚点位置计算新的 x 坐标

```python
            new_y = pivot.y() if pivot.y() < orig_rect.center().y() else pivot.y() - new_h
```
#             根据锚点位置计算新的 y 坐标

```python
            item.rect = QRectF(new_x, new_y, new_w, new_h)
```
#             设置文字框架的新矩形

```python
        else:
```
#         否则（其他类型图形项）：

```python
            # 通用缩放
```
#             注释：通用缩放处理

```python
            item.scale(scale_x, scale_y, pivot)
```
#             调用图形项的通用缩放方法

### 选择工具绘制方法（第428-475行）

```python
    def draw_preview(self, painter: QPainter):
```
#     定义选择工具的绘制预览方法，接受参数：painter（绘图器）

```python
        # 绘制缩放手柄
```
#         注释：绘制缩放手柄

```python
        if self._document:
```
#         如果文档存在：

```python
            for layer in self._document.layers:
```
#             遍历文档的所有图层：

```python
                if not layer.visible:
```
#                 如果图层不可见：

```python
                    continue
```
#                     跳过该图层

```python
                for item in layer.items:
```
#                 遍历图层中的所有图形项：

```python
                    if item.selected and item.visible:
```
#                     如果图形项被选中且可见：

```python
                        self._draw_resize_handles(painter, item)
```
#                         绘制该图形项的缩放手柄

```python
```
#         空行

```python
        if self._is_marquee and self._drag_start and self._drag_current:
```
#         如果处于框选模式且有起始和当前位置：

```python
            scale = max(painter.transform().m11(), 0.001)
```
#             获取当前视图缩放比例

```python
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
```
#             创建蓝色虚线画笔（线宽随缩放反比调整）

```python
            painter.setPen(pen)
```
#             设置绘图器的画笔

```python
            painter.setBrush(QColor(0, 120, 215, 30))
```
#             设置半透明蓝色填充

```python
            painter.drawRect(QRectF(self._drag_start, self._drag_current))
```
#             绘制框选矩形

```python
```
#     空行

```python
    def _draw_resize_handles(self, painter: QPainter, item: GraphicItem):
```
#     定义绘制缩放手柄的私有方法，接受参数：painter（绘图器），item（图形项）

```python
        """绘制 8 个缩放手柄（世界坐标系）"""
```
#         文档字符串——绘制8个缩放手柄（在世界坐标系中）

```python
        local_rect = item.bounding_rect()
```
#         获取图形项的本地边界矩形

```python
        rect = item._transform.mapRect(local_rect)
```
#         通过变换矩阵映射到世界坐标矩形

```python
        scale = max(painter.transform().m11(), 0.001)
```
#         获取当前视图缩放比例

```python
        handle_size = 7 / scale
```
#         计算手柄尺寸（随缩放反比调整）

```python
        half_hs = handle_size / 2
```
#         计算手柄半尺寸

```python
        pen = QPen(QColor(0, 120, 215), 1.0 / scale)
```
#         创建蓝色实线画笔

```python
        painter.setPen(pen)
```
#         设置绘图器的画笔

```python
        painter.setBrush(QColor(255, 255, 255))
```
#         设置白色填充

```python
        corners = [
```
#         定义四个角的坐标列表：

```python
            rect.topLeft(), rect.topRight(),
```
#             左上角、右上角

```python
            rect.bottomLeft(), rect.bottomRight(),
```
#             左下角、右下角

```python
        ]
```
#         列表结束

```python
        edges = [
```
#         定义四条边中点的坐标列表：

```python
            QPointF(rect.center().x(), rect.top()),
```
#             顶部居中

```python
            QPointF(rect.center().x(), rect.bottom()),
```
#             底部居中

```python
            QPointF(rect.left(), rect.center().y()),
```
#             左侧居中

```python
            QPointF(rect.right(), rect.center().y()),
```
#             右侧居中

```python
        ]
```
#         列表结束

```python
        for pt in corners + edges:
```
#         遍历所有手柄位置（四个角 + 四条边中点）：

```python
            painter.drawRect(QRectF(
```
#             绘制手柄小方块矩形：

```python
                pt.x() - half_hs, pt.y() - half_hs,
```
#                 以手柄中心为基准，左上角偏移半尺寸

```python
                handle_size, handle_size,
```
#                 手柄的宽度和高度

```python
            ))
```
#             矩形绘制结束

---

## DirectSelectTool 直接选择工具（第480-1038行）

```python
class DirectSelectTool(BaseTool):
```
# 定义直接选择工具类，继承自 BaseTool 工具基类

```python
    """直接选择工具（A）—— 对照 Adobe Illustrator 1:1 复原
```
#     直接选择工具（A）文档字符串——对照 Adobe Illustrator 1:1 复刻

```python
    AI 中的 Direct Selection Tool (白箭头) 行为：
```
#     AI（Adobe Illustrator）中白箭头直接选择工具的行为：

```python
    1. 点击已选中路径的锚点/手柄 → 选中并进入拖拽
```
#     1. 点击已选中路径的锚点/手柄 → 选中并进入拖拽模式

```python
    2. 点击已选中路径的线段 → 选中该路径（显示所有锚点），不添加锚点
```
#     2. 点击已选中路径的线段 → 选中该路径（显示所有锚点），不添加锚点

```python
    3. 按住 Alt/Option 拖拽手柄 → 断开手柄对称约束（转为角点）
```
#     3. 按住 Alt/Option 键拖拽手柄 → 断开手柄对称约束（转为角点）

```python
    4. 拖拽平滑点的手柄 → 自动对称约束
```
#     4. 拖拽平滑点的手柄 → 自动保持对称约束

```python
    5. 未选中路径 → 点击选中（显示锚点），可拖拽整项
```
#     5. 未选中路径 → 点击选中（显示锚点），可拖拽整个图形项

```python
    6. 按住 Shift → 多选
```
#     6. 按住 Shift 键 → 多选模式

```python
    7. 框选 → 选中范围内的图形项
```
#     7. 框选 → 选中框选范围内的图形项

```python
    """
```
#     文档字符串结束

```python
    __slots__ = (
```
#     使用 __slots__ 限定实例属性为以下变量：

```python
        '_drag_start', '_drag_current',
```
#         拖拽起始位置、拖拽当前位置

```python
        '_dragging_anchor_idx', '_dragging_handle_idx',
```
#         正在拖拽的锚点索引、正在拖拽的手柄索引

```python
        '_dragging_handle_type', '_dragging_item',
```
#         正在拖拽的手柄类型、正在拖拽的图形项

```python
        '_drag_offset', '_selected_anchor_idx',
```
#         拖拽偏移量、已选中的锚点索引

```python
        '_is_marquee', '_old_anchors',
```
#         是否框选模式、操作前的锚点备份列表

```python
        '_has_moved',
```
#         是否已经产生实际拖拽移动

```python
        '_press_alt',           # 按下时 Alt 是否已激活（用于断手柄）
```
#         按下时 Alt 键是否已激活（用于断开手柄对称约束）

```python
        '_original_anchor_type', # 记录拖拽前锚点类型
```
#         记录拖拽前的锚点类型

```python
    )
```
#     __slots__ 定义结束

```python
    # 基础容差（100%缩放下的像素值，与 AI 一致）
```
#     注释：基础容差常量（100%缩放下的像素值，与 AI 一致）

```python
    ANCHOR_TOLERANCE = 5.0       # 锚点点击容差
```
#     锚点点击容差 = 5.0 像素

```python
    HANDLE_TOLERANCE = 4.0       # 手柄点击容差  
```
#     手柄点击容差 = 4.0 像素

```python
    SEGMENT_TOLERANCE = 4.0      # 路径段点击容差
```
#     路径段点击容差 = 4.0 像素

```python
    DRAG_THRESHOLD = 3.0         # 最小拖拽阈值（像素）
```
#     最小拖拽阈值 = 3.0 像素（超过此值才视为拖拽）

### 直接选择工具构造函数（第509-523行）

```python
    def __init__(self):
```
#     定义直接选择工具的构造函数

```python
        super().__init__(ToolType.DIRECT_SELECT)
```
#         调用父类构造函数，传入工具类型为 直接选择

```python
        self._drag_start: QPointF | None = None
```
#         初始化 拖拽起始位置 为 None

```python
        self._drag_current: QPointF | None = None
```
#         初始化 拖拽当前位置 为 None

```python
        self._dragging_anchor_idx: int = -1
```
#         初始化 拖拽锚点索引 为 -1（无效值）

```python
        self._dragging_handle_idx: int = -1
```
#         初始化 拖拽手柄索引 为 -1（无效值）

```python
        self._dragging_handle_type: str = ''
```
#         初始化 拖拽手柄类型 为空字符串

```python
        self._dragging_item: GraphicItem | None = None
```
#         初始化 拖拽图形项 为 None

```python
        self._drag_offset = QPointF(0, 0)
```
#         初始化 拖拽偏移量 为原点

```python
        self._selected_anchor_idx: int = -1
```
#         初始化 已选中锚点索引 为 -1（无效值）

```python
        self._is_marquee: bool = False
```
#         初始化 是否框选模式 为 False

```python
        self._old_anchors: list[AnchorPoint] = []
```
#         初始化 操作前锚点备份列表 为空列表

```python
        self._has_moved: bool = False
```
#         初始化 是否已移动 为 False

```python
        self._press_alt: bool = False
```
#         初始化 Alt 键按下状态 为 False

```python
        self._original_anchor_type: AnchorPointType | None = None
```
#         初始化 原始锚点类型 为 None

### 直接选择工具辅助方法（第527-557行）

```python
    @staticmethod
```
#     静态方法装饰器

```python
    def _safe_inverted(transform):
```
#     定义安全获取逆变换矩阵的私有静态方法，接受参数：transform（变换矩阵）

```python
        """安全获取逆变换矩阵，返回 (inverted_transform, success)"""
```
#         文档字符串——安全获取逆变换矩阵，返回 (逆变换矩阵, 是否成功)

```python
        try:
```
#         尝试执行：

```python
            inv, ok = transform.inverted()
```
#             获取逆变换矩阵和成功标志

```python
            return (inv, ok)
```
#             返回逆变换矩阵和成功标志

```python
        except Exception:
```
#         如果发生异常：

```python
            return (transform, False)
```
#             返回原始变换矩阵和失败标志 False

```python
```
#     空行

```python
    def _find_path_at(self, pos: QPointF, must_be_selected: bool = False) -> tuple[PathItem | None, QPointF | None]:
```
#     定义查找点击位置路径项的私有方法，接受参数：pos（位置），must_be_selected（是否要求已选中，默认False），返回元组（路径项或None，本地坐标或None）

```python
        """从文档中查找点击位置的 PathItem，返回 (item, local_pos)"""
```
#         文档字符串——从文档中查找点击位置的路径项，返回 (图形项, 本地坐标)

```python
        if not self._document:
```
#         如果文档不存在：

```python
            return (None, None)
```
#             返回 (None, None)

```python
        for layer in reversed(self._document.layers):
```
#         从顶层到底层反向遍历文档图层：

```python
            if not layer.visible or layer.locked:
```
#             如果图层不可见或已锁定：

```python
                continue
```
#                 跳过该图层

```python
            for item in layer.items:
```
#             遍历图层中的图形项：

```python
                if not isinstance(item, PathItem) or not item.anchors:
```
#                 如果不是路径项或没有锚点：

```python
                    continue
```
#                     跳过该图形项

```python
                if must_be_selected and not item.selected:
```
#                 如果要求已选中但图形项未被选中：

```python
                    continue
```
#                     跳过该图形项

```python
                inv, ok = self._safe_inverted(item._transform)
```
#                 安全获取图形项的逆变换矩阵

```python
                if not ok:
```
#                 如果逆变换失败：

```python
                    continue
```
#                     跳过该图形项

```python
                local_pos = inv.map(pos)
```
#                 将世界坐标映射到图形项的本地坐标

```python
                br = item.bounding_rect()
```
#                 获取图形项的本地边界矩形

```python
                if not br.contains(local_pos):
```
#                 如果本地坐标不在边界矩形内：

```python
                    continue
```
#                     跳过该图形项

```python
                return (item, local_pos)
```
#                 找到匹配的路径项，返回 (图形项, 本地坐标)

```python
        return (None, None)
```
#         未找到匹配项，返回 (None, None)

### 直接选择工具鼠标按下事件（第561-708行）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
#     定义直接选择工具的鼠标按下事件处理方法

```python
        if not self._document:
```
#         如果文档不存在：

```python
            return
```
#             直接返回

```python
        self._drag_start = QPointF(pos)
```
#         记录拖拽起始位置

```python
        self._drag_current = QPointF(pos)
```
#         记录拖拽当前位置

```python
        self._has_moved = False
```
#         重置是否已移动为 False

```python
        self._press_alt = bool(modifiers & Qt.AltModifier)
```
#         记录按下时 Alt 键是否激活

```python
        self._original_anchor_type = None
```
#         重置原始锚点类型为 None

```python
        shift = bool(modifiers & Qt.ShiftModifier)
```
#         判断 Shift 键是否按下

```python
        # ── 1. 优先检测已选中路径的手柄 ──
```
#         注释：第1步——优先检测已选中路径的手柄

```python
        for layer in reversed(self._document.layers):
```
#         从顶层到底层反向遍历文档图层，检测已选中路径的手柄：

```python
            if not layer.visible or layer.locked:
                continue
```
#             跳过不可见或已锁定的图层

```python
            for item in layer.items:
```
#             遍历图层中的图形项：

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
```
#                 跳过非路径项、未选中项或无锚点的项

```python
                inv, ok = self._safe_inverted(item._transform)
```
#                 安全获取逆变换矩阵

```python
                if not ok:
                    continue
```
#                 逆变换失败则跳过

```python
                local_pos = inv.map(pos)
```
#                 将世界坐标映射到本地坐标

```python
                idx, htype = item.get_handle_at(
```
#                 检测本地坐标处是否有手柄：

```python
                    local_pos.x(), local_pos.y(),
                    tolerance=self.HANDLE_TOLERANCE,
                )
```
#                 使用手柄容差进行检测

```python
                if idx >= 0:
```
#                 如果找到手柄（索引 >= 0）：

```python
                    self._dragging_item = item
                    self._dragging_handle_idx = idx
                    self._dragging_handle_type = htype
                    self._selected_anchor_idx = idx
```
#                     设置拖拽图形项、手柄索引、手柄类型和选中锚点索引

```python
                    self._old_anchors = [a.copy() for a in item.anchors]
```
#                     备份所有锚点的副本（用于撤销）

```python
                    self._original_anchor_type = item.anchors[idx].anchor_type
```
#                     记录当前锚点的原始类型

```python
                    if self._press_alt:
                        item.anchors[idx].convert_to_corner()
```
#                     如果按下 Alt 键，将锚点转为角点（断开对称约束）

```python
                    return
```
#                     返回

```python
        # ── 2. 检测已选中路径的锚点 ──
```
#         注释：第2步——检测已选中路径的锚点

```python
        for layer in reversed(self._document.layers):
```
#         反向遍历图层，检测已选中路径的锚点

```python
            if not layer.visible or layer.locked:
                continue
```
#             跳过不可见或已锁定的图层

```python
            for item in layer.items:
```
#             遍历图形项

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
```
#                 跳过不符合条件的项

```python
                inv, ok = self._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
```
#                 获取本地坐标

```python
                idx = item.get_anchor_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.ANCHOR_TOLERANCE,
                )
```
#                 检测本地坐标处是否有锚点

```python
                if idx >= 0:
```
#                 如果找到锚点：

```python
                    self._dragging_item = item
                    self._dragging_anchor_idx = idx
                    self._selected_anchor_idx = idx
                    self._old_anchors = [a.copy() for a in item.anchors]
                    self._original_anchor_type = item.anchors[idx].anchor_type
```
#                     设置拖拽状态并备份锚点

```python
                    return
```
#                     返回

```python
        # ── 3. 检测已选中路径的线段（AI：点击线段选中路径但不添加锚点）──
```
#         注释：第3步——检测已选中路径的线段（AI 行为：点击线段选中路径但不添加锚点）

```python
        for layer in reversed(self._document.layers):
```
#         反向遍历图层，检测已选中路径的线段

```python
            if not layer.visible or layer.locked:
                continue
```
#             跳过不可见或已锁定图层

```python
            for item in layer.items:
```
#             遍历图形项

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
```
#                 跳过不符合条件的项

```python
                inv, ok = self._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
```
#                 获取本地坐标

```python
                seg = item.get_segment_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.SEGMENT_TOLERANCE,
                )
```
#                 检测路径段

```python
                if seg >= 0:
```
#                 如果找到路径段：

```python
                    self._dragging_item = item
                    self._selected_anchor_idx = -1  # 不选中特定锚点
```
#                     AI 行为：选中该路径用于整体拖拽，不选中特定锚点

```python
                    return
```
#                     返回

```python
        # ── 4. 检测未选中路径 → 选中它并准备整体拖拽 ──
```
#         注释：第4步——检测未选中路径 → 选中它并准备整体拖拽

```python
        for layer in reversed(self._document.layers):
```
#         反向遍历图层，检测未选中路径

```python
            if not layer.visible or layer.locked:
                continue
```
#             跳过不可见或锁定图层

```python
            for item in layer.items:
```
#             遍历图形项

```python
                if not isinstance(item, PathItem) or item.selected or not item.anchors:
                    continue
```
#                 跳过非路径项、已选中项或无锚点项

```python
                inv, ok = self._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
```
#                 获取本地坐标

```python
                # 先检查是否在路径段附近
```
#                 注释：先检查是否在路径段附近

```python
                seg = item.get_segment_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.SEGMENT_TOLERANCE,
                )
                if seg >= 0:
                    if not shift:
                        self._document.clear_selection()
                    item.selected = True
                    self._dragging_item = item
                    self._selected_anchor_idx = -1
                    return
```
#                 如果找到路径段：清除选择（非Shift时），选中路径，准备整体拖拽

```python
                # 再检查是否在锚点附近
```
#                 注释：再检查是否在锚点附近

```python
                idx = item.get_anchor_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.ANCHOR_TOLERANCE,
                )
                if idx >= 0:
                    if not shift:
                        self._document.clear_selection()
                    item.selected = True
                    self._dragging_item = item
                    self._dragging_anchor_idx = idx
                    self._selected_anchor_idx = idx
                    self._old_anchors = [a.copy() for a in item.anchors]
                    self._original_anchor_type = item.anchors[idx].anchor_type
                    return
```
#                 如果找到锚点：清除选择，选中路径，准备锚点拖拽

```python
                # 最后检查填充区域
```
#                 注释：最后检查填充区域

```python
                if item.contains_point(local_pos):
                    if not shift:
                        self._document.clear_selection()
                    item.selected = True
                    self._dragging_item = item
                    self._selected_anchor_idx = -1
                    return
```
#                 如果在路径填充区域内：选中路径，准备整体拖拽

```python
        # ── 5. 检测普通图形项 ──
```
#         注释：第5步——检测普通图形项（非路径项）

```python
        item = self._document.get_item_at(pos.x(), pos.y())
```
#         查找鼠标位置处的图形项

```python
        if item:
            if not shift:
                self._document.clear_selection()
            item.selected = True
            self._dragging_item = item
            self._selected_anchor_idx = -1
            return
```
#         如果找到图形项：清除选择（非Shift时），选中并准备拖拽

```python
        # ── 6. 框选 ──
```
#         注释：第6步——框选模式

```python
        if not shift:
            self._document.clear_selection()
        self._is_marquee = True
```
#         清除选择（非Shift时），进入框选模式

### 直接选择工具鼠标移动事件（第710-779行）

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
#     定义直接选择工具的鼠标移动事件处理方法

```python
        if self._drag_start is None:
            return
```
#         如果没有拖拽起始位置，直接返回

```python
        self._drag_current = QPointF(pos)
```
#         更新拖拽当前位置

```python
        dx_total = pos.x() - self._drag_start.x()
        dy_total = pos.y() - self._drag_start.y()
        dist = math.sqrt(dx_total * dx_total + dy_total * dy_total)
        alt_held = bool(modifiers & Qt.AltModifier)
```
#         计算总位移距离和 Alt 键状态

```python
        # ── 手柄拖拽 ──
```
#         注释：手柄拖拽处理

```python
        if self._dragging_handle_idx >= 0 and self._dragging_item:
```
#         如果正在拖拽手柄且存在拖拽图形项：

```python
            if isinstance(self._dragging_item, PathItem):
```
#             如果拖拽的图形项是路径项：

```python
                inv, ok = self._safe_inverted(self._dragging_item._transform)
                if not ok:
                    return
                local_pos = inv.map(pos)
                anchor = self._dragging_item.anchors[self._dragging_handle_idx]
                rel_x = local_pos.x() - anchor.x
                rel_y = local_pos.y() - anchor.y
```
#                 获取本地坐标和相对于锚点的偏移量

```python
                constrain = (anchor.anchor_type == AnchorPointType.SMOOTH and not alt_held)
```
#                 判断是否需要约束对称（平滑点且未按Alt）

```python
                if self._dragging_handle_type == 'in':
                    self._dragging_item.set_handle_in(
                        self._dragging_handle_idx, rel_x, rel_y,
                        constrain_smooth=constrain,
                    )
                else:
                    self._dragging_item.set_handle_out(
                        self._dragging_handle_idx, rel_x, rel_y,
                        constrain_smooth=constrain,
                    )
```
#                 根据手柄类型（入/出）设置手柄位置

```python
                if self._document:
                    self._document.modified = True
```
#                 标记文档为已修改

```python
        # ── 锚点拖拽（超过阈值后移动）──
```
#         注释：锚点拖拽处理（超过阈值后才移动）

```python
        elif self._dragging_anchor_idx >= 0 and self._dragging_item:
```
#         否则如果正在拖拽锚点且存在拖拽图形项：

```python
            if not self._has_moved:
                if dist < self.DRAG_THRESHOLD:
                    return
                self._has_moved = True
```
#             未超过阈值时不移动，超过后标记为已移动

```python
            if isinstance(self._dragging_item, PathItem):
                inv, ok = self._safe_inverted(self._dragging_item._transform)
                if not ok:
                    return
                local_pos = inv.map(pos)
                self._dragging_item.move_anchor(
                    self._dragging_anchor_idx, local_pos.x(), local_pos.y(),
                )
                if self._document:
                    self._document.modified = True
```
#             将锚点移动到新的本地坐标位置

```python
        # ── 整项拖拽（非锚点/手柄拖拽模式）──
```
#         注释：整项拖拽处理（非锚点/手柄拖拽模式）

```python
        elif self._dragging_item and not self._is_marquee:
```
#         否则如果存在拖拽图形项且不在框选模式：

```python
            if not self._has_moved:
                if dist < self.DRAG_THRESHOLD:
                    return
                self._has_moved = True
```
#             未超过阈值时不移动

```python
            dx = pos.x() - self._drag_start.x()
            dy = pos.y() - self._drag_start.y()
            if modifiers & Qt.ShiftModifier:
                dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)
            self._dragging_item.move_by(dx, dy)
            self._drag_start = QPointF(pos)
            if self._document:
                self._document.modified = True
```
#             Shift 约束方向后移动图形项，更新起始位置

### 直接选择工具鼠标释放事件（第781-835行）

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
#     定义直接选择工具的鼠标释放事件处理方法

```python
        # ── 如果拖拽了手柄且按了 Alt，需要恢复锚点类型为角点 ──
```
#         注释：如果拖拽了手柄且按了 Alt 键，需要恢复锚点类型为角点

```python
        if self._dragging_handle_idx >= 0 and self._dragging_item:
            if isinstance(self._dragging_item, PathItem):
                if self._press_alt or self._has_moved:
                    anchor = self._dragging_item.anchors[self._dragging_handle_idx]
                    if self._press_alt:
                        anchor.anchor_type = AnchorPointType.CORNER
                    self._dragging_item._build_path()
```
#         Alt+拖拽时将锚点转为角点并重建路径

```python
        # ── 记录撤销命令（通过 execute_command 统一入口）──
```
#         注释：记录撤销命令（通过 execute_command 统一入口）

```python
        if self._old_anchors and self._dragging_item and self._document:
            if isinstance(self._dragging_item, PathItem):
                new_anchors = [a.copy() for a in self._dragging_item.anchors]
                if self._has_moved and len(self._old_anchors) == len(new_anchors):
                    changed = False
                    for old, new in zip(self._old_anchors, new_anchors):
                        if (old.x != new.x or old.y != new.y or
                            old.handle_in != new.handle_in or
                            old.handle_out != new.handle_out or
                            old.anchor_type != new.anchor_type):
                            changed = True
                            break
                    if changed:
                        cmd = ModifyAnchorCommand(
                            self._document, self._dragging_item,
                            self._old_anchors, new_anchors,
                        )
                        self._document.execute_command(cmd)
```
#         检查锚点是否有变化，如有则创建修改锚点命令并执行

```python
        # ── 框选 ──
```
#         注释：框选处理

```python
        if self._is_marquee and self._drag_start and self._document:
            rect = QRectF(self._drag_start, pos).normalized()
            if rect.width() > 2 and rect.height() > 2:
                for layer in self._document.layers:
                    items = layer.get_items_in_rect(
                        rect.x(), rect.y(), rect.width(), rect.height(),
                    )
                    for item in items:
                        item.selected = True
```
#         框选范围内图形项设为选中状态

```python
        # ── 重置状态 ──
```
#         注释：重置所有状态变量

```python
        self._drag_start = None
        self._drag_current = None
        self._dragging_anchor_idx = -1
        self._dragging_handle_idx = -1
        self._dragging_handle_type = ''
        self._dragging_item = None
        self._is_marquee = False
        self._old_anchors = []
        self._has_moved = False
        self._press_alt = False
        self._original_anchor_type = None
```
#         重置所有拖拽和选择状态

### 直接选择工具键盘事件（第839-903行）

```python
    def key_press(self, key: int, modifiers: int):
```
#     定义直接选择工具的键盘按下事件处理方法

```python
        """键盘操作对照 AI 行为"""
```
#         文档字符串——键盘操作对照 AI 行为

```python
        # Delete/Backspace 删除选中的锚点（AI：Delete Anchor Point）
```
#         注释：Delete/Backspace 键删除选中的锚点（对应 AI 的删除锚点工具）

```python
        if key in (Qt.Key_Delete, Qt.Key_Backspace):
```
#         如果按下 Delete 或 Backspace 键：

```python
            if self._selected_anchor_idx >= 0 and self._dragging_item:
                if isinstance(self._dragging_item, PathItem):
                    if self._dragging_item.anchor_count > 2:
```
#             如果有选中的锚点且路径锚点数量大于2（至少保留2个）：

```python
                        old_anchors = [a.copy() for a in self._dragging_item.anchors]
                        self._dragging_item.remove_anchor(self._selected_anchor_idx)
```
#                         备份锚点并删除选中锚点

```python
                        if self._document:
                            new_anchors = [a.copy() for a in self._dragging_item.anchors]
                            cmd = ModifyAnchorCommand(
                                self._document, self._dragging_item,
                                old_anchors, new_anchors,
                            )
                            self._document.execute_command(cmd)
```
#                         记录撤销命令并执行

```python
                        self._selected_anchor_idx = max(0, min(
                            self._selected_anchor_idx,
                            self._dragging_item.anchor_count - 1,
                        ))
```
#                         调整选中锚点索引到有效范围

```python
            return
```
#             返回

```python
        # Plus/Equal 在选中锚点后添加新锚点（段中点）
```
#         注释：Plus/Equal 键在选中锚点之后添加新锚点（在路径段中点）

```python
        if key in (Qt.Key_Plus, Qt.Key_Equal):
            if self._selected_anchor_idx >= 0 and self._dragging_item:
                if isinstance(self._dragging_item, PathItem):
                    self._add_anchor_after_selected(self._dragging_item)
            return
```
#         按 +/= 键时在选中锚点后的段中点添加新锚点

```python
    def _add_anchor_after_selected(self, item: PathItem):
```
#     定义在选中锚点之后添加新锚点的私有方法

```python
        """在选中锚点之后的段中点添加新锚点"""
```
#         文档字符串——在选中锚点之后的路径段中点添加新锚点

```python
        anchors = item.anchors
        i = self._selected_anchor_idx
        if i < 0 or len(anchors) < 2:
            return
        n = len(anchors)
        j = (i + 1) % n
        if not item.closed and i == n - 1:
            return
```
#         获取锚点和索引，检查有效性，开放路径末尾无法添加

```python
        prev, curr = anchors[i], anchors[j]
        samples = PathItem._sample_bezier_segment(prev, curr, num_samples=4)
        if len(samples) >= 2:
            mid_idx = len(samples) // 2
            mx, my = samples[mid_idx]
        else:
            mx = (prev.x + curr.x) / 2
            my = (prev.y + curr.y) / 2
```
#         使用贝塞尔采样获取真正的曲线中点

```python
        old_anchors = [a.copy() for a in anchors]
        new_anchor = AnchorPoint(mx, my)
        item.insert_anchor(i + 1, new_anchor)
        self._selected_anchor_idx = i + 1
        self._dragging_item = item
```
#         在选中锚点之后插入新锚点

```python
        if self._document:
            new_anchors = [a.copy() for a in item.anchors]
            cmd = ModifyAnchorCommand(
                self._document, item, old_anchors, new_anchors,
            )
            self._document.execute_command(cmd)
```
#         记录撤销命令并执行

### 直接选择工具绘制预览（第907-1038行）

```python
    def draw_preview(self, painter: QPainter):
```
#     定义直接选择工具的绘制预览方法

```python
        if not self._document:
            return
        for layer in self._document.layers:
            if not layer.visible:
                continue
            for item in layer.items:
                if isinstance(item, PathItem) and item.selected:
                    self._draw_anchor_handles(painter, item)
```
#         遍历所有可见图层，为已选中的路径项绘制锚点手柄

```python
        if self._is_marquee and self._drag_start and self._drag_current:
            scale = max(painter.transform().m11(), 0.001)
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(QColor(0, 120, 215, 30))
            painter.drawRect(QRectF(self._drag_start, self._drag_current))
```
#         框选模式时绘制蓝色虚线框选矩形

```python
    def _draw_anchor_handles(self, painter: QPainter, item: PathItem):
```
#     定义绘制锚点和手柄的私有方法

```python
        """绘制锚点和贝塞尔手柄，对照 AI 的视觉风格
        
        AI 锚点渲染规则：
        - 未选中锚点：白色填充方形，蓝色边框
        - 选中锚点：蓝色填充方形，深蓝边框
        - 手柄线：灰色虚线（handle_in）/ 实线（handle_out）
        - 手柄端点：白色填充圆形，灰色边框
        - 平滑点 vs 角点使用相同视觉表示
        """
```
#         文档字符串——AI 锚点渲染规则说明

```python
        if not item.anchors:
            return
```
#         如果没有锚点则返回

```python
        scale = max(painter.transform().m11(), 0.001)
        handle_r = 3.5 / scale        # 手柄端点半径
        anchor_half = 3.5 / scale     # 锚点半边长
        highlight_half = 4.5 / scale  # 选中锚点半边长
        transform = item._transform
        anchor_color = QColor(0, 120, 215)       # AI 蓝
        anchor_border = QColor(0, 80, 180)
        handle_color = QColor(120, 120, 120)     # 手柄线颜色
```
#         初始化绘制参数：缩放比例、尺寸、颜色

```python
        for i, anchor in enumerate(item.anchors):
            ax_local, ay_local = anchor.x, anchor.y
            ax = transform.map(QPointF(ax_local, ay_local)).x()
            ay = transform.map(QPointF(ax_local, ay_local)).y()
```
#         遍历所有锚点，将本地坐标映射到世界坐标

```python
            # ── 绘制 handle_in 线和端点 ──
```
#             注释：绘制入方向手柄线和端点

```python
            if anchor.handle_in:
                hx_local = ax_local + anchor.handle_in.x()
                hy_local = ay_local + anchor.handle_in.y()
                hx_pt = transform.map(QPointF(hx_local, hy_local))
                hx, hy = hx_pt.x(), hx_pt.y()
```
#                 计算入方向手柄的世界坐标

```python
                handle_pen = QPen(handle_color, 1.0 / scale, Qt.DashLine)
                painter.setPen(handle_pen)
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))
```
#                 绘制灰色虚线手柄线

```python
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))
                painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)
```
#                 绘制白色圆形手柄端点

```python
            # ── 绘制 handle_out 线和端点 ──
```
#             注释：绘制出方向手柄线和端点

```python
            if anchor.handle_out:
                hx_local = ax_local + anchor.handle_out.x()
                hy_local = ay_local + anchor.handle_out.y()
                hx_pt = transform.map(QPointF(hx_local, hy_local))
                hx, hy = hx_pt.x(), hx_pt.y()
```
#                 计算出方向手柄的世界坐标

```python
                handle_pen = QPen(handle_color, 1.0 / scale, Qt.SolidLine)
                painter.setPen(handle_pen)
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))
```
#                 绘制灰色实线手柄线

```python
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))
                painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)
```
#                 绘制白色圆形手柄端点

```python
            # ── 绘制锚点（方形）──
```
#             注释：绘制锚点（方形）

```python
            is_highlighted = (i == self._selected_anchor_idx)
```
#             判断当前锚点是否为高亮（选中）状态

```python
            if is_highlighted:
                painter.setBrush(anchor_color)
                painter.setPen(QPen(anchor_border, 1.5 / scale))
                painter.drawRect(QRectF(
                    ax - highlight_half, ay - highlight_half,
                    highlight_half * 2, highlight_half * 2,
                ))
```
#             选中锚点：蓝色填充、深蓝边框的较大方形

```python
            else:
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(anchor_color, 1.5 / scale))
                painter.drawRect(QRectF(
                    ax - anchor_half, ay - anchor_half,
                    anchor_half * 2, anchor_half * 2,
                ))
```
#             未选中锚点：白色填充、蓝色边框的较小方形

### 直接选择工具 cancel 和静态方法（第1008-1038行）

```python
    def cancel(self):
```
#     定义直接选择工具的取消操作方法

```python
        self._selected_anchor_idx = -1
        self._dragging_anchor_idx = -1
        self._dragging_handle_idx = -1
        self._dragging_item = None
        super().cancel()
```
#         重置所有选择和拖拽状态，调用父类取消方法

```python
    @staticmethod
    def _draw_single_anchor(painter: QPainter, item: PathItem, 
                             anchor_idx: int, highlighted: bool = True):
```
#     定义绘制单个锚点的私有静态方法（供其他锚点工具复用）

```python
        """绘制单个锚点（供其他锚点工具使用）"""
```
#         文档字符串——绘制单个锚点（供其他锚点工具使用）

```python
        if anchor_idx < 0 or anchor_idx >= len(item.anchors):
            return
```
#         锚点索引越界则返回

```python
        scale = max(painter.transform().m11(), 0.001)
        anchor_half = 4.5 / scale if highlighted else 3.5 / scale
        transform = item._transform
        anchor = item.anchors[anchor_idx]
        ax = transform.map(QPointF(anchor.x, anchor.y)).x()
        ay = transform.map(QPointF(anchor.x, anchor.y)).y()
```
#         计算世界坐标和尺寸参数

```python
        if highlighted:
            painter.setBrush(QColor(0, 120, 215))
            painter.setPen(QPen(QColor(0, 80, 180), 1.5 / scale))
        else:
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
```
#         根据高亮状态设置颜色

```python
        painter.drawRect(QRectF(
            ax - anchor_half, ay - anchor_half,
            anchor_half * 2, anchor_half * 2,
        ))
```
#         绘制锚点方形

---

## ShapeTool 形状工具基类（第1043-1099行）

```python
class ShapeTool(BaseTool, ABC):
```
# 定义形状工具基类，继承自 BaseTool 和 ABC（抽象基类）

```python
    """形状工具基类（矩形/椭圆）"""
```
#     形状工具基类文档字符串——矩形和椭圆工具的公共父类

```python
    __slots__ = ('_drag_start', '_drag_current', '_preview_item')
```
#     使用 __slots__ 限定实例属性：拖拽起始位置、拖拽当前位置、预览图形项

```python
    def __init__(self, tool_type: ToolType):
```
#     定义形状工具的构造函数，接受参数：tool_type（工具类型）

```python
        super().__init__(tool_type)
        self._drag_start: QPointF | None = None
        self._drag_current: QPointF | None = None
        self._preview_item: GraphicItem | None = None
```
#         初始化拖拽状态和预览图形项

```python
    @abstractmethod
    def _create_item(self, rect: QRectF) -> GraphicItem:
        ...
```
#     定义创建图形项的抽象方法——子类必须实现

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
#     定义形状工具的鼠标按下事件处理方法

```python
        self._drag_start = QPointF(pos)
        self._drag_current = QPointF(pos)
        self._is_drawing = True
        if self._document:
            self._document.clear_selection()
```
#         记录起始位置，标记为正在绘制，清除选择

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
        if self._is_drawing:
            self._drag_current = QPointF(pos)
```
#     鼠标移动时更新当前位置

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
#     定义形状工具的鼠标释放事件处理方法

```python
        if not self._is_drawing or not self._document or not self._drag_start:
            return
```
#         不在绘制状态则返回

```python
        self._drag_current = QPointF(pos)
        rect = QRectF(self._drag_start, self._drag_current).normalized()
```
#         创建规范化矩形

```python
        # Shift 约束等比（正方形/正圆）
```
#         注释：Shift 键约束为等比（正方形/正圆）

```python
        if modifiers & Qt.ShiftModifier:
            size = max(rect.width(), rect.height())
            if rect.width() < rect.height():
                rect.setWidth(size)
            else:
                rect.setHeight(size)
```
#         按住 Shift 键时取较大维度作为统一尺寸

```python
        if rect.width() > 2 and rect.height() > 2:
            item = self._create_item(rect)
            item.selected = True
            self._document.add_item(item)
```
#         矩形足够大时创建图形项并添加到文档

```python
        self._drag_start = None
        self._drag_current = None
        self._is_drawing = False
```
#         重置所有绘制状态

```python
    def draw_preview(self, painter: QPainter):
```
#     定义形状工具的绘制预览方法

```python
        if self._is_drawing and self._drag_start and self._drag_current:
            rect = QRectF(self._drag_start, self._drag_current).normalized()
            scale = max(painter.transform().m11(), 0.001)
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(QColor(0, 120, 215, 20))
            painter.drawRect(rect)
```
#         绘制时显示蓝色虚线预览矩形

---

## RectangleTool 矩形工具（第1102-1114行）

```python
class RectangleTool(ShapeTool):
```
# 定义矩形工具类，继承自 ShapeTool 形状工具基类

```python
    """矩形工具"""
```
#     矩形工具文档字符串

```python
    __slots__ = ()
```
#     不额外定义实例属性

```python
    def __init__(self):
        super().__init(ToolType.RECTANGLE)
```
#     构造函数，传入工具类型为 矩形

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
#     实现创建图形项方法

```python
        item = RectangleItem(rect.x(), rect.y(), rect.width(), rect.height())
```
#         创建矩形项，传入 x, y, 宽度, 高度

```python
        item.style.fill_color = QColor(200, 200, 200)
        item.style.stroke_color = QColor(50, 50, 50)
        item.style.stroke_width = 2.0
```
#         设置填充颜色为浅灰色、描边颜色为深灰色、描边宽度为 2.0

```python
        return item
```
#         返回创建的矩形项

---

## EllipseTool 椭圆工具（第1117-1129行）

```python
class EllipseTool(ShapeTool):
```
# 定义椭圆工具类，继承自 ShapeTool 形状工具基类

```python
    """椭圆工具"""
```
#     椭圆工具文档字符串

```python
    __slots__ = ()
```
#     不额外定义实例属性

```python
    def __init__(self):
        super().__init(ToolType.ELLIPSE)
```
#     构造函数，传入工具类型为 椭圆

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
#     实现创建图形项方法

```python
        item = EllipseItem(rect.x(), rect.y(), rect.width(), rect.height())
```
#         创建椭圆项

```python
        item.style.fill_color = QColor(200, 200, 200)
        item.style.stroke_color = QColor(50, 50, 50)
        item.style.stroke_width = 2.0
```
#         设置默认样式（与矩形相同）

```python
        return item
```
#         返回创建的椭圆项

---

## AddAnchorPointTool 添加锚点工具（第1134-1205行）

```python
class AddAnchorPointTool(BaseTool):
```
# 定义添加锚点工具类，继承自 BaseTool 工具基类

```python
    """添加锚点工具 —— 在路径段上点击添加新锚点
    
    对照 AI 行为：
    - 点击路径段 → 在最近位置添加新锚点（不进入拖拽）
    - 只对已选中的路径有效
    """
```
#     文档字符串——在路径段上点击添加新锚点，只对已选中路径有效

```python
    __slots__ = ('_selected_anchor_idx', '_dragging_item')
```
#     实例属性：选中锚点索引、拖拽图形项

```python
    SEGMENT_TOLERANCE = 4.0
```
#     路径段命中容差 = 4.0 像素

```python
    def __init__(self):
        super().__init(ToolType.ADD_ANCHOR)
        self._selected_anchor_idx: int = -1
        self._dragging_item: GraphicItem | None = None
```
#     构造函数，初始化状态

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
#     鼠标按下事件处理

```python
        if not self._document:
            return
```
#         文档不存在则返回

```python
        for layer in reversed(self._document.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
```
#         反向遍历图层和图形项，只处理已选中的路径项

```python
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
```
#             获取本地坐标

```python
                seg = item.get_segment_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.SEGMENT_TOLERANCE,
                )
```
#             检测路径段

```python
                if seg >= 0:
                    closest = item.get_closest_point_on_segment(seg, local_pos.x(), local_pos.y())
                    old_anchors = [a.copy() for a in item.anchors]
                    new_anchor = AnchorPoint(closest[0], closest[1])
                    insert_idx = seg + 1
                    item.insert_anchor(insert_idx, new_anchor)
                    self._selected_anchor_idx = insert_idx
                    self._dragging_item = item
```
#                 找到最近点，创建新锚点并插入

```python
                    if self._document:
                        new_anchors = [a.copy() for a in item.anchors]
                        cmd = ModifyAnchorCommand(
                            self._document, item, old_anchors, new_anchors,
                        )
                        self._document.execute_command(cmd)
                    return
```
#                 记录撤销命令并执行

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
        pass  # 不拖拽
```
#     鼠标移动——不进入拖拽模式

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
        pass
```
#     鼠标释放——无操作

```python
    def draw_preview(self, painter: QPainter):
        """高亮显示新添加的锚点"""
        if self._selected_anchor_idx >= 0 and self._dragging_item:
            if isinstance(self._dragging_item, PathItem):
                DirectSelectTool._draw_single_anchor(
                    painter, self._dragging_item, self._selected_anchor_idx, True
                )
```
#     高亮显示新添加的锚点（复用直接选择工具的绘制方法）

```python
    def cancel(self):
        self._selected_anchor_idx = -1
        self._dragging_item = None
        super().cancel()
```
#     取消操作——重置状态

---

## DeleteAnchorPointTool 删除锚点工具（第1210-1274行）

```python
class DeleteAnchorPointTool(BaseTool):
```
# 定义删除锚点工具类，继承自 BaseTool 工具基类

```python
    """删除锚点工具 —— 点击锚点直接删除
    
    对照 AI 行为：
    - 点击锚点 → 删除该锚点（保留路径连续性）
    - 至少保留 2 个锚点
    - 只对已选中的路径有效
    """
```
#     文档字符串——点击锚点直接删除，至少保留2个锚点

```python
    __slots__ = ('_selected_anchor_idx', '_dragging_item')
    ANCHOR_TOLERANCE = 5.0
```
#     实例属性和锚点容差常量

```python
    def __init__(self):
        super().__init(ToolType.DELETE_ANCHOR)
        self._selected_anchor_idx: int = -1
        self._dragging_item: GraphicItem | None = None
```
#     构造函数，初始化状态

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
#     鼠标按下事件处理

```python
        if not self._document:
            return
        for layer in reversed(self._document.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
                if item.anchor_count <= 2:
                    continue
```
#         遍历已选中路径项，锚点数不超过2的跳过

```python
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
                idx = item.get_anchor_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.ANCHOR_TOLERANCE,
                )
```
#             检测锚点

```python
                if idx >= 0:
                    old_anchors = [a.copy() for a in item.anchors]
                    item.remove_anchor(idx)
                    self._dragging_item = item
                    self._selected_anchor_idx = -1
                    if self._document:
                        new_anchors = [a.copy() for a in item.anchors]
                        cmd = ModifyAnchorCommand(
                            self._document, item, old_anchors, new_anchors,
                        )
                        self._document.execute_command(cmd)
                    return
```
#             找到锚点后删除并记录撤销命令

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
        pass
```
#     鼠标移动——无操作

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
        pass
```
#     鼠标释放——无操作

```python
    def draw_preview(self, painter: QPainter):
        pass  # AI 的删除锚点工具在悬停时显示 - 图标，这里简化处理
```
#     绘制预览——简化处理（AI 中悬停时显示 - 图标）

```python
    def cancel(self):
        self._selected_anchor_idx = -1
        self._dragging_item = None
        super().cancel()
```
#     取消操作——重置状态

---

## ConvertAnchorPointTool 转换锚点工具（第1279-1407行）

```python
class ConvertAnchorPointTool(BaseTool):
```
# 定义转换锚点工具类，继承自 BaseTool 工具基类

```python
    """转换锚点工具 —— 切换锚点类型 / 拖拽拉出手柄
    
    对照 AI 行为：
    - 点击平滑点 → 转为角点（移除手柄）
    - 点击角点并拖拽 → 拉出手柄转为平滑点
    - 拖拽手柄 → 断开对称约束
    """
```
#     文档字符串——切换锚点类型或拖拽拉出手柄

```python
    __slots__ = (
        '_drag_start', '_dragging_item', '_dragging_anchor_idx',
        '_is_dragging', '_old_anchors',
    )
```
#     实例属性：拖拽起始位置、拖拽图形项、拖拽锚点索引、是否拖拽中、锚点备份

```python
    ANCHOR_TOLERANCE = 5.0
    DRAG_THRESHOLD = 3.0
```
#     锚点容差和拖拽阈值常量

```python
    def __init__(self):
        super().__init(ToolType.CONVERT_ANCHOR)
        self._drag_start: QPointF | None = None
        self._dragging_item: GraphicItem | None = None
        self._dragging_anchor_idx: int = -1
        self._is_dragging: bool = False
        self._old_anchors: list[AnchorPoint] = []
```
#     构造函数，初始化所有状态

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
#     鼠标按下事件处理

```python
        if not self._document:
            return
        self._drag_start = QPointF(pos)
        self._is_dragging = False
```
#         记录起始位置，标记未拖拽

```python
        for layer in reversed(self._document.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
                idx = item.get_anchor_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.ANCHOR_TOLERANCE,
                )
                if idx >= 0:
                    self._dragging_item = item
                    self._dragging_anchor_idx = idx
                    self._old_anchors = [a.copy() for a in item.anchors]
                    return
```
#         遍历已选中路径，找到被点击的锚点并备份

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
#     鼠标移动事件处理

```python
        if not self._dragging_item or self._dragging_anchor_idx < 0:
            return
        if self._drag_start is None:
            return
```
#         无拖拽目标则返回

```python
        dx = pos.x() - self._drag_start.x()
        dy = pos.y() - self._drag_start.y()
        dist = math.sqrt(dx*dx + dy*dy)
```
#         计算位移和距离

```python
        if not self._is_dragging:
            if dist < self.DRAG_THRESHOLD:
                return
            self._is_dragging = True
```
#         未超过阈值则不处理，超过后标记为拖拽中

```python
        # 拖拽：从锚点拉出手柄
```
#         注释：拖拽——从锚点拉出手柄

```python
        if isinstance(self._dragging_item, PathItem):
            inv, ok = DirectSelectTool._safe_inverted(self._dragging_item._transform)
            if not ok:
                return
            local_pos = inv.map(pos)
            anchor = self._dragging_item.anchors[self._dragging_anchor_idx]
```
#             获取本地坐标和目标锚点

```python
            rel_x = local_pos.x() - anchor.x
            rel_y = local_pos.y() - anchor.y
```
#             计算相对于锚点的偏移

```python
            # 拉出双向对称手柄（平滑点）
            anchor.handle_out = QPointF(rel_x, rel_y)
            anchor.handle_in = QPointF(-rel_x, -rel_y)
            anchor.anchor_type = AnchorPointType.SMOOTH
```
#             创建双向对称手柄，设为平滑点

```python
            self._dragging_item._build_path()
            if self._document:
                self._document.modified = True
```
#             重建路径并标记文档已修改

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
#     鼠标释放事件处理

```python
        if not self._dragging_item or self._dragging_anchor_idx < 0:
            self._drag_start = None
            return
```
#         无拖拽目标则重置并返回

```python
        if isinstance(self._dragging_item, PathItem):
            anchor = self._dragging_item.anchors[self._dragging_anchor_idx]
```
#             获取目标锚点

```python
            if not self._is_dragging:
                # 点击（未拖拽）：切换锚点类型
                if anchor.has_handles:
                    # 有手柄 → 转为角点（移除手柄）
                    anchor.remove_handles()
                # 无手柄的角点 → 点击不产生变化（AI 行为）
                self._dragging_item._build_path()
```
#             点击未拖拽时：有手柄则移除转为角点，无手柄则不变

```python
            # 记录撤销命令（通过 execute_command 统一入口）
```
#             注释：记录撤销命令

```python
            if self._document and self._old_anchors:
                new_anchors = [a.copy() for a in self._dragging_item.anchors]
                cmd = ModifyAnchorCommand(
                    self._document, self._dragging_item,
                    self._old_anchors, new_anchors,
                )
                self._document.execute_command(cmd)
```
#             创建并执行修改锚点命令

```python
        self._drag_start = None
        self._dragging_item = None
        self._dragging_anchor_idx = -1
        self._is_dragging = False
        self._old_anchors = []
```
#         重置所有状态

```python
    def draw_preview(self, painter: QPainter):
        """拖拽时显示预览手柄线"""
        if self._is_dragging and self._dragging_item and self._dragging_anchor_idx >= 0:
            if isinstance(self._dragging_item, PathItem):
                DirectSelectTool._draw_single_anchor(
                    painter, self._dragging_item, self._dragging_anchor_idx, True
                )
```
#     拖拽时高亮显示当前锚点

```python
    def cancel(self):
        self._dragging_item = None
        self._dragging_anchor_idx = -1
        self._is_dragging = False
        super().cancel()
```
#     取消操作——重置状态

---

## PenTool 钢笔工具（第1412-1896行）

```python
class PenTool(BaseTool):
```
# 定义钢笔工具类，继承自 BaseTool 工具基类

```python
    """钢笔工具 —— Adobe Illustrator 1:1 复原
    
    功能对照：
    - 单击 = 创建角点（Corner Point），无手柄
    - 单击并拖动 = 创建平滑点（Smooth Point），拉出对称手柄
    - 点击起始锚点 = 闭合路径（光标出现圆圈 ○）
    - Enter/Return = 结束路径
    - Escape = 取消路径
    
    隐藏功能：
    - Alt/Option 拖拽 = 调整单侧方向线（断开对称）
    - Ctrl/Cmd = 临时切换直接选择工具调整锚点
    - Space = 在拖动过程中临时移动当前锚点位置
    - Shift = 约束角度（45度增量）
    
    光标状态：
    - 默认 = Pen（十字光标）
    - 悬停已有锚点 = Pen-（删除锚点）
    - 悬停已有路径段 = Pen+（添加锚点）
    - 悬停起始锚点 = Pen○（闭合路径）
    - 悬停端点 = Pen/（继续路径）
    """
```
#     钢笔工具文档字符串——完整的功能对照说明

```python
    DRAG_THRESHOLD = 3  # 拖拽阈值（像素），小于此值视为单击
    CLOSE_TOLERANCE = 8  # 闭合路径检测容差
    HANDLE_TOLERANCE = 5  # 手柄命中容差
    ANCHOR_TOLERANCE = 6  # 锚点命中容差
    SEGMENT_TOLERANCE = 5  # 路径段命中容差
    SHIFT_ANGLE_STEP = 45  # Shift约束角度步长（度）
```
#     各种容差和阈值常量

```python
    __slots__ = (
        '_current_path', '_drawing', '_hover_state',
        '_drag_start_pos', '_is_dragging_handle',
        '_dragged_anchor_idx', '_dragged_handle_side',
        '_alt_adjusting', '_space_moving', '_space_start_pos',
        '_ctrl_temp_select', '_ctrl_drag_start',
    )
```
#     实例属性：当前路径、绘制状态、悬停状态、拖拽起始位置、手柄拖拽状态、锚点索引、手柄侧、Alt调整、Space移动、Space起始位置、Ctrl临时选择、Ctrl拖拽起始位置

```python
    # ── 钢笔光标状态枚举 ──
```
#     注释：钢笔光标状态枚举

```python
    PEN_DEFAULT = 0        # 默认钢笔
    PEN_PLUS = 1           # Pen+  添加锚点
    PEN_MINUS = 2          # Pen-  删除锚点
    PEN_CLOSE = 3          # Pen○  闭合路径
    PEN_CONTINUE = 4       # Pen/  继续路径
```
#     光标状态常量

### 钢笔工具构造函数（第1458-1475行）

```python
    def __init__(self):
```
#     定义钢笔工具的构造函数

```python
        super().__init(ToolType.PEN)
        self._current_path: PathItem | None = None
        self._drawing: bool = False          # 正在拖拽中（创建平滑点）
        self._hover_state: int = PenTool.PEN_DEFAULT
```
#         初始化当前路径、绘制状态和悬停状态

```python
        # 拖拽状态
```
#         注释：拖拽状态相关属性

```python
        self._drag_start_pos: QPointF | None = None
        self._is_dragging_handle: bool = False
        self._dragged_anchor_idx: int = -1
        self._dragged_handle_side: str = ''
```
#         拖拽起始位置、是否拖拽手柄、锚点索引、手柄侧

```python
        # 隐藏功能状态
```
#         注释：隐藏功能相关属性

```python
        self._alt_adjusting: bool = False     # Alt 调整单侧方向线
        self._space_moving: bool = False       # Space 移动当前锚点
        self._space_start_pos: QPointF | None = None
        self._ctrl_temp_select: bool = False   # Ctrl 临时直接选择
        self._ctrl_drag_start: QPointF | None = None
```
#         Alt调整、Space移动、Ctrl临时选择的各状态变量

### 钢笔工具辅助方法（第1479-1522行）

```python
    def _snap_angle(self, dx: float, dy: float) -> tuple[float, float]:
        """Shift约束角度到最近的45度增量"""
```
#         文档字符串——Shift 约束角度到最近的 45 度增量

```python
        angle = math.atan2(dy, dx)
        step_rad = math.radians(PenTool.SHIFT_ANGLE_STEP)
        snapped = round(angle / step_rad) * step_rad
        length = math.sqrt(dx*dx + dy*dy)
        return (math.cos(snapped) * length, math.sin(snapped) * length)
```
#         计算角度并吸附到最近45度增量，保持长度不变

```python
    def _detect_hover_state(self, pos: QPointF, doc) -> int:
        """检测悬停位置，返回钢笔光标状态"""
```
#         文档字符串——检测悬停位置，返回钢笔光标状态

```python
        for layer in reversed(doc.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                if not isinstance(item, PathItem) or not item.visible or item.locked:
                    continue
```
#         遍历所有可见未锁定的路径项

```python
                # 1) 检测锚点 → Pen-
```
#                 注释：第1步——检测锚点，返回 Pen-

```python
                anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
                if anchor_idx >= 0:
                    if item is self._current_path:
                        if anchor_idx == 0 and len(item.anchors) >= 2:
                            return PenTool.PEN_CLOSE
                        if anchor_idx == len(item.anchors) - 1:
                            return PenTool.PEN_CONTINUE
                    return PenTool.PEN_MINUS
```
#                 当前路径的起始锚点→PEN_CLOSE，端点→PEN_CONTINUE，其他→PEN_MINUS

```python
                # 2) 检测路径段 → Pen+
```
#                 注释：第2步——检测路径段，返回 Pen+

```python
                seg_idx = item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)
                if seg_idx >= 0:
                    return PenTool.PEN_PLUS
```
#                 找到路径段则返回 PEN_PLUS

```python
        # 3) 如果当前有路径且接近起始点 → Pen○
```
#         注释：第3步——如果当前有路径且接近起始点，返回 Pen○

```python
        if self._current_path and len(self._current_path.anchors) >= 2:
            first = self._current_path.anchors[0]
            dist = math.sqrt((pos.x() - first.x)**2 + (pos.y() - first.y)**2)
            if dist < PenTool.CLOSE_TOLERANCE:
                return PenTool.PEN_CLOSE
```
#         当前路径接近起始点时返回 PEN_CLOSE

```python
        return PenTool.PEN_DEFAULT
```
#         默认返回 PEN_DEFAULT

### 钢笔工具鼠标事件（第1526-1719行）

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
#     定义钢笔工具的鼠标按下事件处理方法

```python
        if not self._document:
            return
        doc = self._document
        is_alt = bool(modifiers & Qt.AltModifier)
        is_ctrl = bool(modifiers & Qt.ControlModifier)
        is_shift = bool(modifiers & Qt.ShiftModifier)
```
#         获取文档和修饰键状态

```python
        # ── Ctrl/Cmd 临时切换直接选择工具 ──
```
#         注释：Ctrl/Cmd 临时切换直接选择工具

```python
        if is_ctrl:
            self._ctrl_temp_select = True
            self._ctrl_drag_start = QPointF(pos)
            for layer in reversed(doc.layers):
                if not layer.visible or layer.locked:
                    continue
                for item in layer.items:
                    if not isinstance(item, PathItem) or not item.visible or item.locked:
                        continue
                    anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
                    if anchor_idx >= 0:
                        self._dragged_anchor_idx = anchor_idx
                        self._current_path = item
                        return
            return
```
#         Ctrl 键按下时查找锚点，临时切换为直接选择模式

```python
        # ── 检测悬停状态决定行为 ──
```
#         注释：检测悬停状态决定行为

```python
        hover = self._detect_hover_state(pos, doc)
```
#         检测当前悬停状态

```python
        if hover == PenTool.PEN_MINUS:
            self._try_delete_anchor(pos, doc)
            return
```
#         PEN_MINUS 状态→尝试删除锚点

```python
        if hover == PenTool.PEN_PLUS:
            self._try_add_anchor(pos, doc)
            return
```
#         PEN_PLUS 状态→尝试添加锚点

```python
        if hover == PenTool.PEN_CLOSE and self._current_path:
            self._close_path()
            return
```
#         PEN_CLOSE 状态→闭合当前路径

```python
        # ── 正常绘制模式 ──
```
#         注释：正常绘制模式

```python
        if self._current_path is None:
            self._current_path = PathItem()
            self._current_path.style.fill_color = QColor(200, 200, 200, 100)
            self._current_path.style.stroke_color = QColor(50, 50, 50)
            self._current_path.style.stroke_width = 2.0
            doc.add_item(self._current_path)
```
#         如果没有当前路径则创建新路径并添加到文档

```python
        self._drag_start_pos = QPointF(pos)
        self._drawing = True
```
#         记录拖拽起始位置，进入绘制模式

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
#     定义钢笔工具的鼠标移动事件处理方法

```python
        if not self._document:
            return
        is_alt = bool(modifiers & Qt.AltModifier)
        is_ctrl = bool(modifiers & Qt.ControlModifier)
        is_shift = bool(modifiers & Qt.ShiftModifier)
```
#         获取修饰键状态

```python
        # ── Ctrl 临时直接选择：移动锚点 ──
```
#         注释：Ctrl 临时直接选择——移动锚点

```python
        if self._ctrl_temp_select and self._current_path and self._ctrl_drag_start:
            dx = pos.x() - self._ctrl_drag_start.x()
            dy = pos.y() - self._ctrl_drag_start.y()
            if self._dragged_anchor_idx >= 0 and self._dragged_anchor_idx < self._current_path.anchor_count:
                self._current_path.move_anchor(
                    self._dragged_anchor_idx,
                    self._current_path.anchors[self._dragged_anchor_idx].x + dx,
                    self._current_path.anchors[self._dragged_anchor_idx].y + dy,
                )
            self._ctrl_drag_start = QPointF(pos)
            self._document.modified = True
            return
```
#         Ctrl 模式下移动锚点位置

```python
        # ── Space 移动当前锚点（仅在拖拽中） ──
```
#         注释：Space 移动当前锚点（仅在拖拽中）

```python
        if self._space_moving and self._current_path and self._space_start_pos:
            dx = pos.x() - self._space_start_pos.x()
            dy = pos.y() - self._space_start_pos.y()
            last_idx = self._current_path.anchor_count - 1
            if last_idx >= 0:
                anchor = self._current_path.anchors[last_idx]
                self._current_path.move_anchor(last_idx, anchor.x + dx, anchor.y + dy)
            self._space_start_pos = QPointF(pos)
            self._document.modified = True
            return
```
#         Space 模式下移动当前最后一个锚点

```python
        # ── 更新悬停光标状态 ──
```
#         注释：更新悬停光标状态

```python
        if not self._drawing:
            self._hover_state = self._detect_hover_state(pos, self._document)
            return
```
#         未在绘制时更新光标状态

```python
        # ── 拖拽中：实时更新最后一个锚点的手柄 ──
```
#         注释：拖拽中——实时更新最后一个锚点的手柄

```python
        if self._drawing and self._drag_start_pos and self._current_path:
            last_idx = self._current_path.anchor_count - 1
            if last_idx >= 0:
                dx = pos.x() - self._drag_start_pos.x()
                dy = pos.y() - self._drag_start_pos.y()
```
#             计算从起始位置的位移

```python
                # Shift 约束角度
                if is_shift and (dx != 0 or dy != 0):
                    dx, dy = self._snap_angle(dx, dy)
```
#                 Shift 键约束角度到45度增量

```python
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < PenTool.DRAG_THRESHOLD:
                    self._current_path.remove_handles(last_idx)
                else:
```
#                 位移小于阈值则移除手柄（角点）

```python
                    if is_alt:
                        # Alt 键：仅设置 handle_out（单侧控制），handle_in 置空
                        anchor = self._current_path.anchors[last_idx]
                        anchor.handle_out = QPointF(dx, dy)
                        anchor.handle_in = None
                        anchor.anchor_type = AnchorPointType.CORNER
                        self._current_path._build_path()
                    else:
                        # 正常拖拽：创建对称平滑点
                        self._current_path.set_handle_out(
                            last_idx, dx, dy, constrain_smooth=True
                        )
```
#                 Alt 键只设置单侧手柄（断开对称），否则创建对称平滑点

```python
                self._document.modified = True
```
#             标记文档为已修改

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
#     定义钢笔工具的鼠标释放事件处理方法

```python
        if not self._document:
            return
```
#         文档不存在则返回

```python
        # ── Ctrl 临时直接选择：释放 ──
```
#         注释：Ctrl 临时直接选择——释放

```python
        if self._ctrl_temp_select:
            self._ctrl_temp_select = False
            self._ctrl_drag_start = None
            self._dragged_anchor_idx = -1
            return
```
#         重置 Ctrl 临时选择状态

```python
        # ── Space 移动锚点：释放 ──
```
#         注释：Space 移动锚点——释放

```python
        if self._space_moving:
            self._space_moving = False
            self._space_start_pos = None
            return
```
#         重置 Space 移动状态

```python
        if not self._drawing or self._drag_start_pos is None:
            return
```
#         不在绘制中则返回

```python
        is_alt = bool(modifiers & Qt.AltModifier)
        is_shift = bool(modifiers & Qt.ShiftModifier)
        dx = pos.x() - self._drag_start_pos.x()
        dy = pos.y() - self._drag_start_pos.y()
```
#         获取修饰键和位移

```python
        if is_shift and (dx != 0 or dy != 0):
            dx, dy = self._snap_angle(dx, dy)
```
#         Shift 键约束角度

```python
        dist = math.sqrt(dx*dx + dy*dy)
```
#         计算位移距离

```python
        if self._current_path is None:
            self._drawing = False
            self._drag_start_pos = None
            return
```
#         无当前路径则重置

```python
        if dist < PenTool.DRAG_THRESHOLD:
```
#         如果位移小于阈值（单击）：

```python
            # ── 短拖拽/单击：创建角点（无手柄） ──
            anchor = AnchorPoint(pos.x(), pos.y(), anchor_type=AnchorPointType.CORNER)
            self._current_path.add_anchor(anchor)
```
#             创建角点（无手柄）并添加到路径

```python
        else:
            if is_alt:
                # ── Alt+拖拽：创建不对称点（只有 handle_out） ──
                anchor = AnchorPoint(
                    self._drag_start_pos.x(), self._drag_start_pos.y(),
                    handle_out=QPointF(dx, dy),
                    anchor_type=AnchorPointType.CORNER,
                )
            else:
                # ── 正常拖拽：创建平滑点（对称手柄） ──
                anchor = AnchorPoint(
                    self._drag_start_pos.x(), self._drag_start_pos.y(),
                    handle_out=QPointF(dx, dy),
                    handle_in=QPointF(-dx, -dy),
                    anchor_type=AnchorPointType.SMOOTH,
                )
            self._current_path.add_anchor(anchor)
```
#         拖拽超过阈值：Alt 创建不对称点，正常创建对称平滑点

```python
        self._document.modified = True
        self._drawing = False
        self._drag_start_pos = None
```
#         标记修改，重置绘制状态

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
        """双击结束路径（不闭合）"""
```
#         文档字符串——双击结束路径（不闭合）

```python
        if self._current_path:
            self._current_path.closed = False
            self._current_path._build_path()
            self._current_path = None
            self._drawing = False
            self._drag_start_pos = None
```
#         将路径设为不闭合，重建路径，重置状态

### 钢笔工具键盘事件（第1732-1749行）

```python
    def key_press(self, key: int, modifiers: int):
```
#     定义钢笔工具的键盘按下事件处理方法

```python
        if key == Qt.Key_Escape:
```
#         如果按下 Escape 键：

```python
            # Escape：取消当前路径
            if self._current_path and self._document:
                self._document.remove_item(self._current_path)
```
#             从文档中移除当前路径

```python
            self._current_path = None
            self._drawing = False
            self._drag_start_pos = None
            self._hover_state = PenTool.PEN_DEFAULT
```
#             重置所有状态

```python
        elif key in (Qt.Key_Return, Qt.Key_Enter):
```
#         否则如果按下 Enter/Return 键：

```python
            # Enter/Return：结束路径（不闭合）
            if self._current_path:
                self._current_path.closed = False
                self._current_path._build_path()
                self._current_path = None
                self._drawing = False
                self._drag_start_pos = None
                self._hover_state = PenTool.PEN_DEFAULT
```
#             将路径设为不闭合并重置状态

### 钢笔工具辅助操作（第1753-1798行）

```python
    def _close_path(self):
        """闭合当前路径"""
```
#         文档字符串——闭合当前路径

```python
        if self._current_path and len(self._current_path.anchors) >= 2:
            self._current_path.closed = True
            self._current_path._build_path()
        self._current_path = None
        self._drawing = False
        self._drag_start_pos = None
```
#         将路径设为闭合，重建路径，重置状态

```python
    def _try_delete_anchor(self, pos: QPointF, doc):
        """尝试删除悬停的锚点（Pen-行为）"""
```
#         文档字符串——尝试删除悬停的锚点（Pen- 行为）

```python
        for layer in reversed(doc.layers):
            if not layer.visible or layer.locked:
                continue
            for item in list(layer.items):
                if not isinstance(item, PathItem) or not item.visible or item.locked:
                    continue
                anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
                if anchor_idx >= 0 and item.anchor_count > 2:
                    old_anchors = [a.copy() for a in item.anchors]
                    item.remove_anchor(anchor_idx)
                    new_anchors = [a.copy() for a in item.anchors]
                    cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)
                    doc.execute_command(cmd)
                    return
```
#         遍历所有路径项，找到锚点后删除并记录撤销命令

```python
    def _try_add_anchor(self, pos: QPointF, doc):
        """尝试在路径段上添加锚点（Pen+行为）"""
```
#         文档字符串——尝试在路径段上添加锚点（Pen+ 行为）

```python
        for layer in reversed(doc.layers):
            if not layer.visible or layer.locked:
                continue
            for item in list(layer.items):
                if not isinstance(item, PathItem) or not item.visible or item.locked:
                    continue
                seg_idx = item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)
                if seg_idx >= 0:
                    cx, cy = item.get_closest_point_on_segment(seg_idx, pos.x(), pos.y())
                    old_anchors = [a.copy() for a in item.anchors]
                    new_anchor = AnchorPoint(cx, cy, anchor_type=AnchorPointType.CORNER)
                    item.insert_anchor(seg_idx + 1, new_anchor)
                    new_anchors = [a.copy() for a in item.anchors]
                    cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)
                    doc.execute_command(cmd)
                    return
```
#         遍历所有路径项，在路径段最近点处插入新锚点

### 钢笔工具绘制预览（第1802-1885行）

```python
    def draw_preview(self, painter: QPainter):
        """绘制钢笔工具预览：
        - 已放置的锚点
        - 路径线段
        - 拖拽中的手柄预览
        - 悬停光标指示
        """
```
#         文档字符串——绘制钢笔工具预览（锚点、线段、手柄、光标指示）

```python
        if not self._current_path:
            return
        anchors = self._current_path.anchors
        if not anchors:
            return
```
#         无当前路径或无锚点则返回

```python
        scale = max(painter.transform().m11(), 0.001)
```
#         获取当前视图缩放比例

```python
        # ── 绘制已放置的锚点 ──
```
#         注释：绘制已放置的锚点

```python
        for i, anchor in enumerate(anchors):
            pt = QPointF(anchor.x, anchor.y)
```
#         遍历所有锚点

```python
            # 锚点圆圈
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
            painter.setBrush(QColor(255, 255, 255))
            painter.drawEllipse(pt, 3 / scale, 3 / scale)
```
#             绘制蓝色边框白色填充的锚点圆圈

```python
            # 手柄线（handle_in）
            if anchor.handle_in:
                hin = QPointF(anchor.x + anchor.handle_in.x(), 
                             anchor.y + anchor.handle_in.y())
                pen = QPen(QColor(0, 120, 215), 0.8 / scale)
                pen.setStyle(Qt.DashLine)
                painter.setPen(pen)
                painter.drawLine(pt, hin)
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))
                painter.drawEllipse(hin, 2.5 / scale, 2.5 / scale)
```
#             绘制入方向手柄虚线和端点

```python
            # 手柄线（handle_out）
            if anchor.handle_out:
                hout = QPointF(anchor.x + anchor.handle_out.x(), 
                              anchor.y + anchor.handle_out.y())
                painter.setPen(QPen(QColor(0, 120, 215), 0.8 / scale))
                painter.drawLine(pt, hout)
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))
                painter.drawEllipse(hout, 2.5 / scale, 2.5 / scale)
```
#             绘制出方向手柄实线和端点

```python
        # ── 绘制路径线段 ──
```
#         注释：绘制路径线段

```python
        if len(anchors) >= 2:
            pen = QPen(QColor(0, 120, 215), 1.5 / scale)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            for i in range(len(anchors) - 1):
                prev, curr = anchors[i], anchors[i + 1]
                samples = PathItem._sample_bezier_segment(prev, curr, num_samples=30)
                for k in range(len(samples) - 1):
                    p1 = QPointF(samples[k][0], samples[k][1])
                    p2 = QPointF(samples[k+1][0], samples[k+1][1])
                    painter.drawLine(p1, p2)
```
#         使用贝塞尔采样绘制路径线段（30个采样点）

```python
        # ── 拖拽中：绘制从最后一个锚点出发的预览手柄 ──
```
#         注释：拖拽中——绘制预览手柄

```python
        if self._drawing and self._drag_start_pos:
            last_anchor = anchors[-1]
            last_pt = QPointF(last_anchor.x, last_anchor.y)
            painter.setPen(QPen(QColor(0, 120, 215, 150), 0.8 / scale, Qt.DashLine))
            painter.drawLine(last_pt, self._drag_start_pos)
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
            painter.setBrush(QColor(0, 120, 215, 100))
            painter.drawEllipse(self._drag_start_pos, 3 / scale, 3 / scale)
```
#         绘制从最后一个锚点到拖拽位置的虚线预览

```python
        # ── 悬停光标指示（在第一个锚点上绘制闭合图标） ──
```
#         注释：悬停光标指示——在第一个锚点上绘制闭合图标

```python
        if self._hover_state == PenTool.PEN_CLOSE and len(anchors) >= 2:
            first_pt = QPointF(anchors[0].x, anchors[0].y)
            painter.setPen(QPen(QColor(0, 120, 215), 2 / scale))
            painter.setBrush(Qt.NoBrush)
            r = 6 / scale
            painter.drawEllipse(first_pt, r, r)
```
#         当悬停状态为 PEN_CLOSE 时在起始锚点绘制闭合圆圈指示

### 钢笔工具 cancel 方法（第1887-1896行）

```python
    def cancel(self):
```
#     定义钢笔工具的取消操作方法

```python
        if self._current_path and self._document:
            self._document.remove_item(self._current_path)
```
#         如果有当前路径则从文档中移除

```python
        self._current_path = None
        self._drawing = False
        self._drag_start_pos = None
        self._hover_state = PenTool.PEN_DEFAULT
        self._ctrl_temp_select = False
        self._space_moving = False
        super().cancel()
```
#         重置所有状态，调用父类取消方法

---

## TextTool 文字工具（第1901-1922行）

```python
class TextTool(BaseTool):
```
# 定义文字工具类，继承自 BaseTool 工具基类

```python
    """文字工具 —— 点击创建文字"""
```
#     文字工具文档字符串——点击创建文字

```python
    __slots__ = ()
```
#     不额外定义实例属性

```python
    def __init__(self):
        super().__init(ToolType.TEXT)
```
#     构造函数，传入工具类型为 文字

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
#     定义文字工具的鼠标按下事件处理方法

```python
        if not self._document:
            return
        text_frame = TextFrame(pos.x(), pos.y())
```
#         在鼠标位置创建文字框架

```python
        text_frame.contents = "文字"
```
#         设置默认文字内容为"文字"

```python
        text_frame.char_attrs.font_size = 24
```
#         设置字体大小为 24

```python
        text_frame.char_attrs.fill_color = QColor(50, 50, 50)
```
#         设置字体颜色为深灰色

```python
        text_frame.style.fill_color = None
```
#         设置框架填充颜色为空（透明背景）

```python
        text_frame.selected = True
        self._document.clear_selection()
        self._document.add_item(text_frame)
        self._document.modified = True
```
#         选中文字框架，清除其他选择，添加到文档

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
        pass  # 由 UI 层处理
```
#     双击事件——由 UI 层处理

---

## HandTool 抓手工具（第1927-1933行）

```python
class HandTool(BaseTool):
```
# 定义抓手工具类，继承自 BaseTool 工具基类

```python
    """抓手工具 —— 拖拽平移画布"""
```
#     抓手工具文档字符串——拖拽平移画布

```python
    __slots__ = ()
```
#     不额外定义实例属性

```python
    def __init__(self):
        super().__init(ToolType.HAND)
```
#     构造函数，传入工具类型为 抓手

