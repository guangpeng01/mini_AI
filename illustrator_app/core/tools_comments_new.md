# tools.py 中文注解翻译

---

```python
"""
```
# 模块多行文档字符串开始

---

```python
工具系统 (Python 3.10+) —— 选择、矩形、椭圆、钢笔、文字工具
```
# 文档内容：工具系统 (Python 3.10+) —— 选择、矩形、椭圆、钢笔、文字工具

---

```python

```
# 文档字符串空行

---

```python
架构优化:
```
# 文档内容：架构优化:

---

```python
- 使用 __slots__ 减少内存占用
```
# 文档内容：- 使用 __slots__ 减少内存占用

---

```python
- 使用 X | None 替代 Optional[X]
```
# 文档内容：- 使用 X | None 替代 Optional[X]

---

```python
- 使用 match-case 替代 if-elif 链
```
# 文档内容：- 使用 match-case 替代 if-elif 链

---

```python
- 使用 @override 风格注释 (PEP 698 ready)
```
# 文档内容：- 使用 @override 风格注释 (PEP 698 ready)

---

```python
"""
```
# 文档字符串结束标记


---

```python
from __future__ import annotations
```
# 从future特性中导入：annotations


---

```python
import math
```
# 导入math模块

---

```python
from abc import ABC, abstractmethod
```
# 从抽象基类模块中导入：ABC, abstractmethod

---

```python
from enum import Enum, auto
```
# 从枚举类型模块中导入：Enum, auto


---

```python
from PyQt5.QtCore import QPointF, QRectF, Qt
```
# 从PyQt5核心模块中导入：QPointF, QRectF, Qt

---

```python
from PyQt5.QtGui import QColor, QPainter, QPen
```
# 从PyQt5图形界面模块中导入：QColor, QPainter, QPen


---

```python
from .graphics import (
```
# 从本地graphics图形模块中多行导入以下符号：

---

```python
    GraphicItem, RectangleItem, EllipseItem, TextFrame,
```
# 导入符号：GraphicItem, RectangleItem, EllipseItem, TextFrame

---

```python
    PathItem, GraphicStyle, AnchorPoint, AnchorPointType,
```
# 导入符号：PathItem, GraphicStyle, AnchorPoint, AnchorPointType

---

```python
    Command, MoveItemsCommand, ModifyAnchorCommand, ResizeItemCommand,
```
# 导入符号：Command, MoveItemsCommand, ModifyAnchorCommand, ResizeItemCommand

---

```python
)
```
# 多行导入结束括号

---

```python
from .document import Document, Layer
```
# 从本地document文档模块中导入：Document, Layer



---

```python
class ToolType(Enum):
```
# 定义工具类型枚举类，为所有可用工具提供唯一类型标识符，继承自(Enum)

---

```python
    """工具类型"""
```
    # 单行文档字符串：工具类型

---

```python
    SELECTION = auto()              # 选择工具 (V)
```
    # 枚举值：选择工具（快捷键：V）

---

```python
    DIRECT_SELECT = auto()          # 直接选择工具 (A)
```
    # 枚举值：直接选择工具（快捷键：A）

---

```python
    RECTANGLE = auto()              # 矩形工具 (M)
```
    # 枚举值：矩形工具（快捷键：M）

---

```python
    ELLIPSE = auto()                # 椭圆工具 (L)
```
    # 枚举值：椭圆工具（快捷键：L）

---

```python
    PEN = auto()                    # 钢笔工具 (P)
```
    # 枚举值：钢笔工具（快捷键：P）

---

```python
    ADD_ANCHOR = auto()             # 添加锚点工具 (+)
```
    # 枚举值：添加锚点工具（快捷键：+）

---

```python
    DELETE_ANCHOR = auto()          # 删除锚点工具 (-)
```
    # 枚举值：删除锚点工具（快捷键：-）

---

```python
    CONVERT_ANCHOR = auto()         # 转换锚点工具 (Shift+C)
```
    # 枚举值：转换锚点工具（快捷键：Shift+C）

---

```python
    TEXT = auto()                   # 文字工具 (T)
```
    # 枚举值：文字工具（快捷键：T）

---

```python
    HAND = auto()                   # 抓手工具 (H)
```
    # 枚举值：抓手工具（快捷键：H）

---

```python
    ZOOM = auto()                   # 缩放工具 (Z)
```
    # 枚举值：缩放工具（快捷键：Z）



---

```python
class BaseTool(ABC):
```
# 定义工具基类（抽象），所有工具的共同父类，继承自(ABC)

---

```python
    """工具基类（抽象）"""
```
    # 单行文档字符串：工具基类（抽象）

---

```python
    __slots__ = ('tool_type', '_document', '_is_drawing')
```
    # 声明实例属性槽位：('tool_type', '_document', '_is_drawing')，用于节省内存并提升访问速度


---

```python
    def __init__(self, tool_type: ToolType):
```
    # 构造函数，接收自身引用、工具类型标识：工具类型枚举，无返回值

---

```python
        self.tool_type = tool_type
```
        # 实例属性：工具类型标识

---

```python
        self._document: Document | None = None
```
        # 私有实例属性：关联的文档对象引用

---

```python
        self._is_drawing: bool = False
```
        # 私有实例属性：是否正在绘制中


---

```python
    def set_document(self, doc: Document):
```
    # 设置关联文档，接收自身引用、文档对象：文档对象，无返回值

---

```python
        # 将传入的文档赋值给实例的私有文档引用
```
        # 注释：将传入的文档赋值给实例的私有文档引用

---

```python
        self._document = doc
```
        # 私有实例属性：关联的文档对象引用


---

```python
    @property
```
    # 属性装饰器，将方法转为只读属性

---

```python
    def document(self) -> Document | None:
```
    # 定义document方法，接收自身引用，返回可选的文档对象

---

```python
        return self._document
```
        # 返回self._document


---

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
    # 鼠标按下事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        pass
```
        # 空操作占位符，无实际逻辑


---

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
    # 鼠标移动事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        pass
```
        # 空操作占位符，无实际逻辑


---

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
    # 鼠标释放事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        pass
```
        # 空操作占位符，无实际逻辑


---

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
```
    # 鼠标双击事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        pass
```
        # 空操作占位符，无实际逻辑


---

```python
    def key_press(self, key: int, modifiers: int):
```
    # 键盘按键事件处理，接收自身引用、按键码：整数、修饰键标志位：整数，无返回值

---

```python
        pass
```
        # 空操作占位符，无实际逻辑


---

```python
    def draw_preview(self, painter: QPainter):
```
    # 绘制预览，接收自身引用、绘图引擎：绘图引擎，无返回值

---

```python
        pass
```
        # 空操作占位符，无实际逻辑


---

```python
    def cancel(self):
```
    # 取消当前操作，接收自身引用，无返回值

---

```python
        self._is_drawing = False
```
        # 私有实例属性：是否正在绘制中



---

```python
# ── 缩放手柄类型 ───────────────────────────────────────────
```
# 注释：── 缩放手柄类型 ───────────────────────────────────────────


---

```python
class ResizeHandleType(Enum):
```
# 定义缩放手柄位置类型枚举，标识八个方向的缩放手柄，继承自(Enum)

---

```python
    """缩放手柄位置类型"""
```
    # 单行文档字符串：缩放手柄位置类型

---

```python
    TOP_LEFT = auto()
```
    # 将auto()赋值给TOP_LEFT

---

```python
    TOP_CENTER = auto()
```
    # 将auto()赋值给TOP_CENTER

---

```python
    TOP_RIGHT = auto()
```
    # 将auto()赋值给TOP_RIGHT

---

```python
    MIDDLE_LEFT = auto()
```
    # 将auto()赋值给MIDDLE_LEFT

---

```python
    MIDDLE_RIGHT = auto()
```
    # 将auto()赋值给MIDDLE_RIGHT

---

```python
    BOTTOM_LEFT = auto()
```
    # 将auto()赋值给BOTTOM_LEFT

---

```python
    BOTTOM_CENTER = auto()
```
    # 将auto()赋值给BOTTOM_CENTER

---

```python
    BOTTOM_RIGHT = auto()
```
    # 将auto()赋值给BOTTOM_RIGHT



---

```python
# ── 选择工具 ──────────────────────────────────────────────
```
# 注释：── 选择工具 ──────────────────────────────────────────────


---

```python
class SelectionTool(BaseTool):
```
# 定义选择工具类，支持点击选择、框选、多选拖拽和缩放手柄操作，继承自(BaseTool)

---

```python
    """选择工具 —— 点击选择 / 框选 / 多选拖拽 / 缩放手柄"""
```
    # 单行文档字符串：选择工具 —— 点击选择 / 框选 / 多选拖拽 / 缩放手柄

---

```python
    __slots__ = ('_drag_start', '_drag_current', '_dragging_item',
```
    # 声明实例属性槽位：('_drag_start', '_drag_current', '_dragging_item',，用于节省内存并提升访问速度

---

```python
                 '_drag_offset', '_is_marquee',
```
                 # '_drag_offset', '_is_marquee'

---

```python
                 '_dragging_items', '_drag_offsets',
```
                 # '_dragging_items', '_drag_offsets'

---

```python
                 '_total_dx', '_total_dy',
```
                 # 函数参数续行：'_total_dx', '_total_dy'

---

```python
                 '_is_scaling', '_scale_handle',
```
                 # '_is_scaling', '_scale_handle'

---

```python
                 '_scale_orig_rect', '_scale_orig_br',
```
                 # '_scale_orig_rect', '_scale_orig_br'

---

```python
                 '_scale_pivot', '_scale_keep_ratio')
```
                 # '_scale_pivot', '_scale_keep_ratio')


---

```python
    def __init__(self):
```
    # 构造函数，接收自身引用，无返回值

---

```python
        super().__init__(ToolType.SELECTION)
```
        # 调用父类构造函数，传入ToolType.SELECTION

---

```python
        self._drag_start: QPointF | None = None
```
        # 拖拽起始位置

---

```python
        self._drag_current: QPointF | None = None
```
        # 当前拖拽位置

---

```python
        self._dragging_item: GraphicItem | None = None
```
        # 正在拖拽的图形项

---

```python
        self._drag_offset = QPointF(0, 0)
```
        # 拖拽偏移量

---

```python
        self._is_marquee: bool = False
```
        # 是否为框选模式

---

```python
        # 多选拖拽支持
```
        # 注释：多选拖拽支持

---

```python
        self._dragging_items: list[GraphicItem] = []
```
        # 多选拖拽的图形项列表

---

```python
        self._drag_offsets: list[QPointF] = []
```
        # 多选拖拽的偏移量列表

---

```python
        self._total_dx: float = 0.0
```
        # 累计X方向移动总量

---

```python
        self._total_dy: float = 0.0
```
        # 累计Y方向移动总量

---

```python
        # 缩放支持
```
        # 注释：缩放支持

---

```python
        self._is_scaling: bool = False
```
        # 是否为缩放模式

---

```python
        self._scale_handle: ResizeHandleType | None = None
```
        # 当前激活的缩放手柄类型

---

```python
        self._scale_orig_rect = QRectF()
```
        # 缩放前的原始矩形

---

```python
        self._scale_orig_br = QRectF()  # 缩放前 bounding_rect
```
        # 缩放前的边界矩形

---

```python
        self._scale_pivot = QPointF()   # 缩放锚点（对角的那个固定点）
```
        # 缩放固定锚点（对角的那个固定点）

---

```python
        self._scale_keep_ratio: bool = False
```
        # 是否保持宽高比缩放


---

```python
    # ── 手柄检测 ──
```
    # 注释：── 手柄检测 ──


---

```python
    @staticmethod
```
    # 静态方法装饰器，该方法不依赖实例状态

---

```python
    def _get_handle_at(item: GraphicItem, pos: QPointF, tolerance: float = 8) -> ResizeHandleType | None:
```
    # 检测鼠标是否在缩放手柄上（静态方法），接收图形项：图形项、鼠标位置坐标：二维浮点坐标、命中容差：float = 8，返回可选的缩放手柄类型枚举

---

```python
        """检测鼠标是否在缩放手柄上（pos 为世界坐标）"""
```
        # 单行文档字符串：检测鼠标是否在缩放手柄上（pos 为世界坐标）

---

```python
        local_rect = item.bounding_rect()
```
        # 将item.bounding_rect()赋值给local_rect

---

```python
        # 通过图形项的变换矩阵将本地矩形映射到世界坐标矩形
```
        # 注释：通过图形项的变换矩阵将本地矩形映射到世界坐标矩形

---

```python
        rect = item._transform.mapRect(local_rect)
```
        # 将item._transform.mapRect(local_rect)赋值给rect

---

```python
        hs = tolerance  # 手柄命中容差
```
        # 将tolerance  # 手柄命中容差赋值给hs

---

```python
        corners = {
```
        # 将{赋值给corners

---

```python
            ResizeHandleType.TOP_LEFT: rect.topLeft(),
```
            # 将rect.topLeft(),赋值给ResizeHandleType.TOP_LEFT

---

```python
            ResizeHandleType.TOP_RIGHT: rect.topRight(),
```
            # 将rect.topRight(),赋值给ResizeHandleType.TOP_RIGHT

---

```python
            ResizeHandleType.BOTTOM_LEFT: rect.bottomLeft(),
```
            # 将rect.bottomLeft(),赋值给ResizeHandleType.BOTTOM_LEFT

---

```python
            ResizeHandleType.BOTTOM_RIGHT: rect.bottomRight(),
```
            # 将rect.bottomRight(),赋值给ResizeHandleType.BOTTOM_RIGHT

---

```python
        }
```
        # }

---

```python
        edges = {
```
        # 将{赋值给edges

---

```python
            ResizeHandleType.TOP_CENTER: QPointF(rect.center().x(), rect.top()),
```
            # 将QPointF(rect.center().x(), rect.top()),赋值给ResizeHandleType.TOP_CENTER

---

```python
            ResizeHandleType.BOTTOM_CENTER: QPointF(rect.center().x(), rect.bottom()),
```
            # 将QPointF(rect.center().x(), rect.bottom()),赋值给ResizeHandleType.BOTTOM_CENTER

---

```python
            ResizeHandleType.MIDDLE_LEFT: QPointF(rect.left(), rect.center().y()),
```
            # 将QPointF(rect.left(), rect.center().y()),赋值给ResizeHandleType.MIDDLE_LEFT

---

```python
            ResizeHandleType.MIDDLE_RIGHT: QPointF(rect.right(), rect.center().y()),
```
            # 将QPointF(rect.right(), rect.center().y()),赋值给ResizeHandleType.MIDDLE_RIGHT

---

```python
        }
```
        # }


---

```python
        for htype, pt in corners.items():
```
        # 遍历corners.items()，每次迭代将当前元素赋给htype, pt

---

```python
            if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:
```
            # 如果abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs（满足条件时执行）

---

```python
                return htype
```
                # 返回htype

---

```python
        for htype, pt in edges.items():
```
        # 遍历edges.items()，每次迭代将当前元素赋给htype, pt

---

```python
            if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:
```
            # 如果abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs（满足条件时执行）

---

```python
                return htype
```
                # 返回htype

---

```python
        return None
```
        # 返回None


---

```python
    # ── 鼠标事件 ──
```
    # 注释：── 鼠标事件 ──


---

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
    # 鼠标按下事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        self._drag_start = QPointF(pos)
```
        # 拖拽起始位置

---

```python
        self._drag_current = QPointF(pos)
```
        # 当前拖拽位置

---

```python
        self._total_dx = 0.0
```
        # 累计X方向移动总量

---

```python
        self._total_dy = 0.0
```
        # 累计Y方向移动总量

---

```python
        self._is_scaling = False
```
        # 是否为缩放模式

---

```python
        self._scale_handle = None
```
        # 当前激活的缩放手柄类型

---

```python
        self._scale_keep_ratio = bool(modifiers & Qt.ShiftModifier)
```
        # 是否保持宽高比缩放


---

```python
        # 检查是否点击了已选中项的缩放手柄；检查是否点击了已选中图形项的缩放手柄
```
        # 注释：检查是否点击了已选中项的缩放手柄；检查是否点击了已选中图形项的缩放手柄

---

```python
        sel = self._document.get_selection()
```
        # 将self._document.get_selection()赋值给sel

---

```python
        if len(sel) == 1:
```
        # 如果len(sel) == 1（满足条件时执行）

---

```python
            handle = self._get_handle_at(sel[0], pos)
```
            # 将self._get_handle_at(sel[0], pos)赋值给handle

---

```python
            if handle is not None:
```
            # 如果handle is not None（满足条件时执行）

---

```python
                self._dragging_item = sel[0]
```
                # 正在拖拽的图形项

---

```python
                self._is_scaling = True
```
                # 是否为缩放模式

---

```python
                self._scale_handle = handle
```
                # 当前激活的缩放手柄类型

---

```python
                # 使用世界坐标系的 bounding_rect（含 item 变换）
```
                # 注释：使用世界坐标系的 bounding_rect（含 item 变换）

---

```python
                world_rect = sel[0]._transform.mapRect(sel[0].bounding_rect())
```
                # 将sel[0]._transform.mapRect(sel[0].bounding_rect())赋值给world_rect

---

```python
                self._scale_orig_rect = QRectF(world_rect)
```
                # 缩放前的原始矩形

---

```python
                self._scale_orig_br = QRectF(world_rect)
```
                # 缩放前的边界矩形

---

```python
                # 缩放的固定锚点是对角；缩放的固定锚点为对角位置
```
                # 注释：缩放的固定锚点是对角；缩放的固定锚点为对角位置

---

```python
                self._scale_pivot = self._get_opposite_corner(handle, self._scale_orig_rect)
```
                # 缩放固定锚点（对角的那个固定点）

---

```python
                return
```
                # 空返回，结束函数执行

---

```python
    
```
    # 

---

```python
        item = self._document.get_item_at(pos.x(), pos.y())
```
        # 将self._document.get_item_at(pos.x(), pos.y())赋值给item

---

```python
        if item:
```
        # 如果item（满足条件时执行）

---

```python
            self._is_marquee = False  # 点击了物体，不是框选
```
            # 是否为框选模式

---

```python
            # 如果点击的项未被选中，先清除选择并选中它
```
            # 注释：如果点击的项未被选中，先清除选择并选中它

---

```python
            if not item.selected:
```
            # 如果not item.selected（满足条件时执行）

---

```python
                if not (modifiers & Qt.ShiftModifier):
```
                # 如果not (modifiers & Qt.ShiftModifier)（满足条件时执行）

---

```python
                    self._document.clear_selection()
```
                    # 调用self._document的清除所有选中状态方法

---

```python
                item.selected = True
```
                # 将True赋值给item.selected

---

```python
            
```
            # 

---

```python
            # 准备拖拽
```
            # 注释：准备拖拽

---

```python
            sel = self._document.get_selection()
```
            # 将self._document.get_selection()赋值给sel

---

```python
            if len(sel) > 1:
```
            # 如果len(sel) > 1（满足条件时执行）

---

```python
                # 多选状态 → 多选拖拽模式
```
                # 注释：多选状态 → 多选拖拽模式

---

```python
                self._dragging_items = list(sel)
```
                # 多选拖拽的图形项列表

---

```python
                self._drag_offsets = [pos - it._transform.mapRect(it.bounding_rect()).topLeft() for it in sel]
```
                # 多选拖拽的偏移量列表

---

```python
                self._dragging_item = None
```
                # 正在拖拽的图形项

---

```python
            else:
```
            # 否则（不满足上述条件时执行）

---

```python
                # 单选或仅选中了一项 → 单项拖拽（不要清除再重新选中）
```
                # 注释：单选或仅选中了一项 → 单项拖拽（不要清除再重新选中）

---

```python
                self._dragging_item = item
```
                # 正在拖拽的图形项

---

```python
                self._drag_offset = pos - item._transform.mapRect(item.bounding_rect()).topLeft()
```
                # 拖拽偏移量

---

```python
                self._dragging_items = []
```
                # 多选拖拽的图形项列表

---

```python
        else:
```
        # 否则（不满足上述条件时执行）

---

```python
            if not (modifiers & Qt.ShiftModifier):
```
            # 如果not (modifiers & Qt.ShiftModifier)（满足条件时执行）

---

```python
                self._document.clear_selection()
```
                # 调用self._document的清除所有选中状态方法

---

```python
            self._dragging_item = None
```
            # 正在拖拽的图形项

---

```python
            self._dragging_items = []
```
            # 多选拖拽的图形项列表

---

```python
            self._is_marquee = True
```
            # 是否为框选模式


---

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
    # 鼠标移动事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        # 定义鼠标移动事件处理方法
```
        # 注释：定义鼠标移动事件处理方法

---

```python
        if self._drag_start is None:
```
        # 如果拖拽起始位置为空（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        self._drag_current = QPointF(pos)
```
        # 当前拖拽位置


---

```python
        # 缩放模式
```
        # 注释：缩放模式

---

```python
        if self._is_scaling and self._dragging_item:
```
        # 如果在缩放模式且存在拖拽项（满足条件时执行）

---

```python
            self._apply_resize(pos, bool(modifiers & Qt.ShiftModifier))
```
            # 调用self的_apply_resize方法

---

```python
            if self._document:
```
            # 如果self._document（满足条件时执行）

---

```python
                self._document.modified = True
```
                # 将True赋值给self._document.modified

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        dx = pos.x() - self._drag_start.x()
```
        # 将pos.x() - self._drag_start.x()赋值给dx

---

```python
        dy = pos.y() - self._drag_start.y()
```
        # 将pos.y() - self._drag_start.y()赋值给dy

---

```python
        # Shift 约束水平/垂直移动
```
        # 注释：Shift 约束水平/垂直移动

---

```python
        if modifiers & Qt.ShiftModifier:
```
        # 如果modifiers & Qt.ShiftModifier（满足条件时执行）

---

```python
            dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)
```
            # 函数参数续行：dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)


---

```python
        if self._dragging_items:
```
        # 如果存在多选拖拽项（满足条件时执行）

---

```python
            for item in self._dragging_items:
```
            # 遍历所有多选拖拽项，每次迭代将当前元素赋给item

---

```python
                item.move_by(dx, dy)
```
                # 调用item的移动方法

---

```python
            self._total_dx += dx
```
            # 将累计X方向移动总量加等于dx

---

```python
            self._total_dy += dy
```
            # 将累计Y方向移动总量加等于dy

---

```python
            self._drag_start = QPointF(pos)
```
            # 拖拽起始位置

---

```python
            if self._document:
```
            # 如果self._document（满足条件时执行）

---

```python
                self._document.modified = True
```
                # 将True赋值给self._document.modified

---

```python
        elif self._dragging_item and not self._is_scaling:
```
        # 如果拖拽单个项且非缩放模式（满足条件时执行）

---

```python
            self._dragging_item.move_by(dx, dy)
```
            # 调用self._dragging_item的移动方法

---

```python
            self._total_dx += dx
```
            # 将累计X方向移动总量加等于dx

---

```python
            self._total_dy += dy
```
            # 将累计Y方向移动总量加等于dy

---

```python
            self._drag_start = QPointF(pos)
```
            # 拖拽起始位置

---

```python
            if self._document:
```
            # 如果self._document（满足条件时执行）

---

```python
                self._document.modified = True
```
                # 将True赋值给self._document.modified


---

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
    # 鼠标释放事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        # 缩放完成：记录命令（通过 execute_command 统一入口）
```
        # 注释：缩放完成：记录命令（通过 execute_command 统一入口）

---

```python
        if self._is_scaling and self._dragging_item and self._document:
```
        # 如果self._is_scaling and self._dragging_item and self._document（满足条件时执行）

---

```python
            new_world_rect = self._dragging_item._transform.mapRect(self._dragging_item.bounding_rect())
```
            # 将self._dragging_item._transform.mapRect(self._dragging_item.bounding_rect())赋值给new_world_rect

---

```python
            if new_world_rect != self._scale_orig_br:
```
            # 如果new_world_rect != self._scale_orig_br（满足条件时执行）

---

```python
                # 通过尺寸变化记录（使用世界坐标矩形）
```
                # 注释：通过尺寸变化记录（使用世界坐标矩形）

---

```python
                cmd = ResizeItemCommand(
```
                # 将ResizeItemCommand(赋值给cmd

---

```python
                    self._document, self._dragging_item,
```
                    # 函数参数续行：self._document, self._dragging_item

---

```python
                    self._scale_orig_br, new_world_rect,
```
                    # 函数参数续行：self._scale_orig_br, new_world_rect

---

```python
                )
```
                # )

---

```python
                self._document.execute_command(cmd)
```
                # 调用self._document的执行命令（支持撤销）方法

---

```python
            self._is_scaling = False
```
            # 是否为缩放模式

---

```python
            self._scale_handle = None
```
            # 当前激活的缩放手柄类型

---

```python
            self._dragging_item = None
```
            # 正在拖拽的图形项

---

```python
            self._drag_start = None
```
            # 拖拽起始位置

---

```python
            self._drag_current = None
```
            # 当前拖拽位置

---

```python
            self._total_dx = 0.0
```
            # 累计X方向移动总量

---

```python
            self._total_dy = 0.0
```
            # 累计Y方向移动总量

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # 多选拖拽完成后记录移动命令（用于撤销，通过 execute_command 统一入口）
```
        # 注释：多选拖拽完成后记录移动命令（用于撤销，通过 execute_command 统一入口）

---

```python
        moved_items = self._dragging_items if self._dragging_items else (
```
        # 条件赋值：如果self._dragging_items则将moved_items设为self._dragging_items，否则设为(

---

```python
            [self._dragging_item] if self._dragging_item else []
```
            # 函数参数续行：[self._dragging_item] if self._dragging_item else []

---

```python
        )
```
        # )

---

```python
        if moved_items and self._document and (self._total_dx != 0 or self._total_dy != 0):
```
        # 如果moved_items and self._document and (self._total_dx != 0 or self._total_dy != 0)（满足条件时执行）

---

```python
            cmd = MoveItemsCommand(
```
            # 将MoveItemsCommand(赋值给cmd

---

```python
                self._document, moved_items,
```
                # 函数参数续行：self._document, moved_items

---

```python
                self._total_dx, self._total_dy,
```
                # 函数参数续行：self._total_dx, self._total_dy

---

```python
            )
```
            # )

---

```python
            self._document.execute_command(cmd)
```
            # 调用self._document的执行命令（支持撤销）方法


---

```python
        if self._is_marquee and self._drag_start and self._document:
```
        # 如果self._is_marquee and self._drag_start and self._document（满足条件时执行）

---

```python
            rect = QRectF(self._drag_start, pos).normalized()
```
            # 将QRectF(self._drag_start, pos).normalized()赋值给rect

---

```python
            if rect.width() > 2 and rect.height() > 2:
```
            # 如果rect.width() > 2 and rect.height() > 2（满足条件时执行）

---

```python
                for layer in self._document.layers:
```
                # 遍历文档的所有图层，每次迭代将当前元素赋给layer

---

```python
                    items = layer.get_items_in_rect(
```
                    # 将layer.get_items_in_rect(赋值给items

---

```python
                        rect.x(), rect.y(), rect.width(), rect.height(),
```
                        # rect.x(), rect.y(), rect.width(), rect.height()

---

```python
                    )
```
                    # )

---

```python
                    for item in items:
```
                    # 遍历items，每次迭代将当前元素赋给item

---

```python
                        item.selected = True
```
                        # 将True赋值给item.selected


---

```python
        self._drag_start = None
```
        # 拖拽起始位置

---

```python
        self._drag_current = None
```
        # 当前拖拽位置

---

```python
        self._dragging_item = None
```
        # 正在拖拽的图形项

---

```python
        self._dragging_items = []
```
        # 多选拖拽的图形项列表

---

```python
        self._is_marquee = False
```
        # 是否为框选模式

---

```python
        self._is_scaling = False
```
        # 是否为缩放模式

---

```python
        self._scale_handle = None
```
        # 当前激活的缩放手柄类型

---

```python
        self._total_dx = 0.0
```
        # 累计X方向移动总量

---

```python
        self._total_dy = 0.0
```
        # 累计Y方向移动总量


---

```python
    # ── 缩放核心 ──
```
    # 注释：── 缩放核心 ──


---

```python
    @staticmethod
```
    # 静态方法装饰器，该方法不依赖实例状态

---

```python
    def _get_opposite_corner(handle: ResizeHandleType, rect: QRectF) -> QPointF:
```
    # 获取缩放手柄对面的固定锚点（静态方法），接收手柄类型：缩放手柄类型枚举、矩形区域：浮点矩形，返回二维浮点坐标

---

```python
        """获取缩放手柄对面的固定锚点"""
```
        # 单行文档字符串：获取缩放手柄对面的固定锚点

---

```python
        match handle:
```
        # 模式匹配：根据handle的值分派不同处理逻辑

---

```python
            case ResizeHandleType.TOP_LEFT:
```
            # 匹配左上角手柄

---

```python
                return rect.bottomRight()
```
                # 返回rect.bottomRight()

---

```python
            case ResizeHandleType.TOP_CENTER:
```
            # 匹配上边中点手柄

---

```python
                return QPointF(rect.center().x(), rect.bottom())
```
                # 返回QPointF(rect.center().x(), rect.bottom())

---

```python
            case ResizeHandleType.TOP_RIGHT:
```
            # 匹配右上角手柄

---

```python
                return rect.bottomLeft()
```
                # 返回rect.bottomLeft()

---

```python
            case ResizeHandleType.MIDDLE_LEFT:
```
            # 匹配左边中点手柄

---

```python
                return QPointF(rect.right(), rect.center().y())
```
                # 返回QPointF(rect.right(), rect.center().y())

---

```python
            case ResizeHandleType.MIDDLE_RIGHT:
```
            # 匹配右边中点手柄

---

```python
                return QPointF(rect.left(), rect.center().y())
```
                # 返回QPointF(rect.left(), rect.center().y())

---

```python
            case ResizeHandleType.BOTTOM_LEFT:
```
            # 匹配左下角手柄

---

```python
                return rect.topRight()
```
                # 返回rect.topRight()

---

```python
            case ResizeHandleType.BOTTOM_CENTER:
```
            # 匹配下边中点手柄

---

```python
                return QPointF(rect.center().x(), rect.top())
```
                # 返回QPointF(rect.center().x(), rect.top())

---

```python
            case ResizeHandleType.BOTTOM_RIGHT:
```
            # 匹配右下角手柄

---

```python
                return rect.topLeft()
```
                # 返回rect.topLeft()


---

```python
    def _apply_resize(self, mouse_pos: QPointF, keep_ratio: bool):
```
    # 根据手柄类型和鼠标位置调整图形大小，接收自身引用、鼠标位置坐标：二维浮点坐标、是否保持宽高比：布尔值，无返回值

---

```python
        """根据手柄类型和鼠标位置调整图形大小"""
```
        # 单行文档字符串：根据手柄类型和鼠标位置调整图形大小

---

```python
        if not self._dragging_item:
```
        # 如果没有正在拖拽的图形项（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        pivot = self._scale_pivot
```
        # 将self._scale_pivot赋值给pivot

---

```python
        orig = self._scale_orig_rect
```
        # 将self._scale_orig_rect赋值给orig

---

```python
        mx, my = mouse_pos.x(), mouse_pos.y()
```
        # mx, my = mouse_pos.x(), mouse_pos.y()

---

```python
        px, py = pivot.x(), pivot.y()
```
        # px, py = pivot.x(), pivot.y()


---

```python
        # 根据手柄确定新宽高
```
        # 注释：根据手柄确定新宽高

---

```python
        match self._scale_handle:
```
        # 模式匹配：根据self._scale_handle的值分派不同处理逻辑

---

```python
            case ResizeHandleType.TOP_LEFT:
```
            # 匹配左上角手柄

---

```python
                new_w, new_h = px - mx, py - my
```
                # new_w, new_h = px - mx, py - my

---

```python
            case ResizeHandleType.TOP_CENTER:
```
            # 匹配上边中点手柄

---

```python
                new_w = orig.width()
```
                # 将orig.width()赋值给new_w

---

```python
                new_h = py - my
```
                # 将py - my赋值给new_h

---

```python
            case ResizeHandleType.TOP_RIGHT:
```
            # 匹配右上角手柄

---

```python
                new_w = mx - px
```
                # 将mx - px赋值给new_w

---

```python
                new_h = py - my
```
                # 将py - my赋值给new_h

---

```python
            case ResizeHandleType.MIDDLE_LEFT:
```
            # 匹配左边中点手柄

---

```python
                new_w = px - mx
```
                # 将px - mx赋值给new_w

---

```python
                new_h = orig.height()
```
                # 将orig.height()赋值给new_h

---

```python
            case ResizeHandleType.MIDDLE_RIGHT:
```
            # 匹配右边中点手柄

---

```python
                new_w = mx - px
```
                # 将mx - px赋值给new_w

---

```python
                new_h = orig.height()
```
                # 将orig.height()赋值给new_h

---

```python
            case ResizeHandleType.BOTTOM_LEFT:
```
            # 匹配左下角手柄

---

```python
                new_w = px - mx
```
                # 将px - mx赋值给new_w

---

```python
                new_h = my - py
```
                # 将my - py赋值给new_h

---

```python
            case ResizeHandleType.BOTTOM_CENTER:
```
            # 匹配下边中点手柄

---

```python
                new_w = orig.width()
```
                # 将orig.width()赋值给new_w

---

```python
                new_h = my - py
```
                # 将my - py赋值给new_h

---

```python
            case ResizeHandleType.BOTTOM_RIGHT:
```
            # 匹配右下角手柄

---

```python
                new_w = mx - px
```
                # 将mx - px赋值给new_w

---

```python
                new_h = my - py
```
                # 将my - py赋值给new_h

---

```python
            case _:
```
            # 匹配其他未列出的情况（兜底）

---

```python
                return
```
                # 空返回，结束函数执行


---

```python
        # 最小尺寸限制
```
        # 注释：最小尺寸限制

---

```python
        new_w = max(new_w, 10)
```
        # 将max(new_w, 10)赋值给new_w

---

```python
        new_h = max(new_h, 10)
```
        # 将max(new_h, 10)赋值给new_h


---

```python
        # 等比约束
```
        # 注释：等比约束

---

```python
        if keep_ratio:
```
        # 如果keep_ratio（满足条件时执行）

---

```python
            orig_aspect = orig.width() / max(orig.height(), 1)
```
            # 将orig.width() / max(orig.height(), 1)赋值给orig_aspect

---

```python
            if self._scale_handle in (
```
            # 函数参数续行：if self._scale_handle in (

---

```python
                ResizeHandleType.TOP_CENTER, ResizeHandleType.BOTTOM_CENTER,
```
                # ResizeHandleType.TOP_CENTER, ResizeHandleType.BOTTOM_CENTER

---

```python
            ):
```
            # ):

---

```python
                new_w = new_h * orig_aspect
```
                # 将new_h * orig_aspect赋值给new_w

---

```python
            elif self._scale_handle in (
```
            # 函数参数续行：elif self._scale_handle in (

---

```python
                ResizeHandleType.MIDDLE_LEFT, ResizeHandleType.MIDDLE_RIGHT,
```
                # ResizeHandleType.MIDDLE_LEFT, ResizeHandleType.MIDDLE_RIGHT

---

```python
            ):
```
            # ):

---

```python
                new_h = new_w / max(orig_aspect, 0.001)
```
                # 将new_w / max(orig_aspect, 0.001)赋值给new_h

---

```python
            else:
```
            # 否则（不满足上述条件时执行）

---

```python
                # 角手柄：选择较大的维度保持比例
```
                # 注释：角手柄：选择较大的维度保持比例

---

```python
                aspect_w = new_h * orig_aspect
```
                # 将new_h * orig_aspect赋值给aspect_w

---

```python
                aspect_h = new_w / max(orig_aspect, 0.001)
```
                # 将new_w / max(orig_aspect, 0.001)赋值给aspect_h

---

```python
                if abs(new_w - aspect_w) < abs(new_h - aspect_h):
```
                # 如果abs(new_w - aspect_w) < abs(new_h - aspect_h)（满足条件时执行）

---

```python
                    new_h = new_w / max(orig_aspect, 0.001)
```
                    # 将new_w / max(orig_aspect, 0.001)赋值给new_h

---

```python
                else:
```
                # 否则（不满足上述条件时执行）

---

```python
                    new_w = new_h * orig_aspect
```
                    # 将new_h * orig_aspect赋值给new_w


---

```python
        # 应用缩放
```
        # 注释：应用缩放

---

```python
        self._resize_item(self._dragging_item, pivot, orig, new_w, new_h)
```
        # 调用self的_resize_item方法


---

```python
    def _resize_item(self, item: GraphicItem, pivot: QPointF,
```
    # def _resize_item(self, item: GraphicItem, pivot: QPointF

---

```python
                     orig_rect: QRectF, new_w: float, new_h: float):
```
                     # 将QRectF, new_w: float, new_h: float):赋值给orig_rect

---

```python
        """对不同类型的图形应用尺寸变化"""
```
        # 单行文档字符串：对不同类型的图形应用尺寸变化

---

```python
        scale_x = new_w / max(orig_rect.width(), 0.001)
```
        # 将new_w / max(orig_rect.width(), 0.001)赋值给scale_x

---

```python
        scale_y = new_h / max(orig_rect.height(), 0.001)
```
        # 将new_h / max(orig_rect.height(), 0.001)赋值给scale_y


---

```python
        if isinstance(item, RectangleItem):
```
        # 如果isinstance(item, RectangleItem)（满足条件时执行）

---

```python
            # 矩形：直接修改 rect
```
            # 注释：矩形：直接修改 rect

---

```python
            new_x = pivot.x() if pivot.x() < orig_rect.center().x() else pivot.x() - new_w
```
            # 条件赋值：如果pivot.x() < orig_rect.center().x()则将new_x设为pivot.x()，否则设为pivot.x() - new_w

---

```python
            new_y = pivot.y() if pivot.y() < orig_rect.center().y() else pivot.y() - new_h
```
            # 条件赋值：如果pivot.y() < orig_rect.center().y()则将new_y设为pivot.y()，否则设为pivot.y() - new_h

---

```python
            item.rect = QRectF(new_x, new_y, new_w, new_h)
```
            # 将QRectF(new_x, new_y, new_w, new_h)赋值给item.rect

---

```python
        elif isinstance(item, EllipseItem):
```
        # 如果isinstance(item, EllipseItem)（满足条件时执行）

---

```python
            # 椭圆：直接修改 rect
```
            # 注释：椭圆：直接修改 rect

---

```python
            new_x = pivot.x() if pivot.x() < orig_rect.center().x() else pivot.x() - new_w
```
            # 条件赋值：如果pivot.x() < orig_rect.center().x()则将new_x设为pivot.x()，否则设为pivot.x() - new_w

---

```python
            new_y = pivot.y() if pivot.y() < orig_rect.center().y() else pivot.y() - new_h
```
            # 条件赋值：如果pivot.y() < orig_rect.center().y()则将new_y设为pivot.y()，否则设为pivot.y() - new_h

---

```python
            item.rect = QRectF(new_x, new_y, new_w, new_h)
```
            # 将QRectF(new_x, new_y, new_w, new_h)赋值给item.rect

---

```python
        elif isinstance(item, PathItem):
```
        # 如果isinstance(item, PathItem)（满足条件时执行）

---

```python
            # 路径：缩放所有锚点
```
            # 注释：路径：缩放所有锚点

---

```python
            ref_x = pivot.x() if scale_x > 0 else orig_rect.right()
```
            # 条件赋值：如果scale_x > 0则将ref_x设为pivot.x()，否则设为orig_rect.right()

---

```python
            ref_y = pivot.y() if scale_y > 0 else orig_rect.bottom()
```
            # 条件赋值：如果scale_y > 0则将ref_y设为pivot.y()，否则设为orig_rect.bottom()

---

```python
            for anchor in item.anchors:
```
            # 遍历item.anchors，每次迭代将当前元素赋给anchor

---

```python
                anchor.x = ref_x + (anchor.x - ref_x) * scale_x
```
                # 将ref_x + (anchor.x - ref_x) * scale_x赋值给anchor.x

---

```python
                anchor.y = ref_y + (anchor.y - ref_y) * scale_y
```
                # 将ref_y + (anchor.y - ref_y) * scale_y赋值给anchor.y

---

```python
                if anchor.handle_in:
```
                # 如果anchor.handle_in（满足条件时执行）

---

```python
                    anchor.handle_in = QPointF(
```
                    # 将QPointF(赋值给anchor.handle_in

---

```python
                        anchor.handle_in.x() * scale_x,
```
                        # 函数参数续行：anchor.handle_in.x() * scale_x

---

```python
                        anchor.handle_in.y() * scale_y,
```
                        # 函数参数续行：anchor.handle_in.y() * scale_y

---

```python
                    )
```
                    # )

---

```python
                if anchor.handle_out:
```
                # 如果anchor.handle_out（满足条件时执行）

---

```python
                    anchor.handle_out = QPointF(
```
                    # 将QPointF(赋值给anchor.handle_out

---

```python
                        anchor.handle_out.x() * scale_x,
```
                        # 函数参数续行：anchor.handle_out.x() * scale_x

---

```python
                        anchor.handle_out.y() * scale_y,
```
                        # 函数参数续行：anchor.handle_out.y() * scale_y

---

```python
                    )
```
                    # )

---

```python
            item._rebuild_from_anchors()
```
            # 调用item的从锚点数据重建路径方法

---

```python
        elif isinstance(item, TextFrame):
```
        # 如果isinstance(item, TextFrame)（满足条件时执行）

---

```python
            new_x = pivot.x() if pivot.x() < orig_rect.center().x() else pivot.x() - new_w
```
            # 条件赋值：如果pivot.x() < orig_rect.center().x()则将new_x设为pivot.x()，否则设为pivot.x() - new_w

---

```python
            new_y = pivot.y() if pivot.y() < orig_rect.center().y() else pivot.y() - new_h
```
            # 条件赋值：如果pivot.y() < orig_rect.center().y()则将new_y设为pivot.y()，否则设为pivot.y() - new_h

---

```python
            item.rect = QRectF(new_x, new_y, new_w, new_h)
```
            # 将QRectF(new_x, new_y, new_w, new_h)赋值给item.rect

---

```python
        else:
```
        # 否则（不满足上述条件时执行）

---

```python
            # 通用缩放
```
            # 注释：通用缩放

---

```python
            item.scale(scale_x, scale_y, pivot)
```
            # 调用item的缩放方法


---

```python
    # ── 绘制 ──
```
    # 注释：── 绘制 ──


---

```python
    def draw_preview(self, painter: QPainter):
```
    # 绘制预览，接收自身引用、绘图引擎：绘图引擎，无返回值

---

```python
        # 绘制缩放手柄
```
        # 注释：绘制缩放手柄

---

```python
        if self._document:
```
        # 如果self._document（满足条件时执行）

---

```python
            for layer in self._document.layers:
```
            # 遍历文档的所有图层，每次迭代将当前元素赋给layer

---

```python
                if not layer.visible:
```
                # 如果not layer.visible（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                for item in layer.items:
```
                # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                    if item.selected and item.visible:
```
                    # 如果item.selected and item.visible（满足条件时执行）

---

```python
                        self._draw_resize_handles(painter, item)
```
                        # 调用self的_draw_resize_handles方法


---

```python
        if self._is_marquee and self._drag_start and self._drag_current:
```
        # 如果self._is_marquee and self._drag_start and self._drag_current（满足条件时执行）

---

```python
            scale = max(painter.transform().m11(), 0.001)
```
            # 将max(painter.transform().m11(), 0.001)赋值给scale

---

```python
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
```
            # 将QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)赋值给pen

---

```python
            painter.setPen(pen)
```
            # 调用painter的setPen方法

---

```python
            painter.setBrush(QColor(0, 120, 215, 30))
```
            # 调用painter的setBrush方法

---

```python
            painter.drawRect(QRectF(self._drag_start, self._drag_current))
```
            # 调用painter的drawRect方法


---

```python
    def _draw_resize_handles(self, painter: QPainter, item: GraphicItem):
```
    # 绘制8个缩放手柄，接收自身引用、绘图引擎：绘图引擎、图形项：图形项，无返回值

---

```python
        """绘制 8 个缩放手柄（世界坐标系）"""
```
        # 单行文档字符串：绘制 8 个缩放手柄（世界坐标系）

---

```python
        # 将本地 bounding_rect 通过 item 的变换映射到世界坐标
```
        # 注释：将本地 bounding_rect 通过 item 的变换映射到世界坐标

---

```python
        local_rect = item.bounding_rect()
```
        # 将item.bounding_rect()赋值给local_rect

---

```python
        rect = item._transform.mapRect(local_rect)
```
        # 将item._transform.mapRect(local_rect)赋值给rect

---

```python
        scale = max(painter.transform().m11(), 0.001)
```
        # 将max(painter.transform().m11(), 0.001)赋值给scale

---

```python
        handle_size = 7 / scale
```
        # 将7 / scale赋值给handle_size

---

```python
        half_hs = handle_size / 2
```
        # 将handle_size / 2赋值给half_hs


---

```python
        pen = QPen(QColor(0, 120, 215), 1.0 / scale)
```
        # 将QPen(QColor(0, 120, 215), 1.0 / scale)赋值给pen

---

```python
        painter.setPen(pen)
```
        # 调用painter的setPen方法

---

```python
        painter.setBrush(QColor(255, 255, 255))
```
        # 调用painter的setBrush方法


---

```python
        # 四个角
```
        # 注释：四个角

---

```python
        corners = [
```
        # 将[赋值给corners

---

```python
            rect.topLeft(), rect.topRight(),
```
            # rect.topLeft(), rect.topRight()

---

```python
            rect.bottomLeft(), rect.bottomRight(),
```
            # rect.bottomLeft(), rect.bottomRight()

---

```python
        ]
```
        # 函数参数：]

---

```python
        # 四条边的中点
```
        # 注释：四条边的中点

---

```python
        edges = [
```
        # 将[赋值给edges

---

```python
            QPointF(rect.center().x(), rect.top()),
```
            # QPointF(rect.center().x(), rect.top())

---

```python
            QPointF(rect.center().x(), rect.bottom()),
```
            # QPointF(rect.center().x(), rect.bottom())

---

```python
            QPointF(rect.left(), rect.center().y()),
```
            # QPointF(rect.left(), rect.center().y())

---

```python
            QPointF(rect.right(), rect.center().y()),
```
            # QPointF(rect.right(), rect.center().y())

---

```python
        ]
```
        # 函数参数：]


---

```python
        for pt in corners + edges:
```
        # 遍历corners + edges，每次迭代将当前元素赋给pt

---

```python
            painter.drawRect(QRectF(
```
            # painter.drawRect(QRectF(

---

```python
                pt.x() - half_hs, pt.y() - half_hs,
```
                # pt.x() - half_hs, pt.y() - half_hs

---

```python
                handle_size, handle_size,
```
                # handle_size, handle_size

---

```python
            ))
```
            # ))



---

```python
# ── 直接选择工具 ──────────────────────────────────────────
```
# 注释：── 直接选择工具 ──────────────────────────────────────────


---

```python
class DirectSelectTool(BaseTool):
```
# 定义直接选择工具类（白箭头），对照Adobe Illustrator行为复原，支持锚点/手柄选择和编辑，继承自(BaseTool)

---

```python
    """直接选择工具（A）—— 对照 Adobe Illustrator 1:1 复原
```
    # """直接选择工具（A）—— 对照 Adobe Illustrator 1:1 复原

---

```python
    
```
    # 文档字符串空行

---

```python
    AI 中的 Direct Selection Tool (白箭头) 行为：
```
    # 文档内容：AI 中的 Direct Selection Tool (白箭头) 行为：

---

```python
    1. 点击已选中路径的锚点/手柄 → 选中并进入拖拽
```
    # 文档内容：1. 点击已选中路径的锚点/手柄 → 选中并进入拖拽

---

```python
    2. 点击已选中路径的线段 → 选中该路径（显示所有锚点），不添加锚点
```
    # 文档内容：2. 点击已选中路径的线段 → 选中该路径（显示所有锚点），不添加锚点

---

```python
    3. 按住 Alt/Option 拖拽手柄 → 断开手柄对称约束（转为角点）
```
    # 文档内容：3. 按住 Alt/Option 拖拽手柄 → 断开手柄对称约束（转为角点）

---

```python
    4. 拖拽平滑点的手柄 → 自动对称约束
```
    # 文档内容：4. 拖拽平滑点的手柄 → 自动对称约束

---

```python
    5. 未选中路径 → 点击选中（显示锚点），可拖拽整项
```
    # 文档内容：5. 未选中路径 → 点击选中（显示锚点），可拖拽整项

---

```python
    6. 按住 Shift → 多选
```
    # 文档内容：6. 按住 Shift → 多选

---

```python
    7. 框选 → 选中范围内的图形项
```
    # 文档内容：7. 框选 → 选中范围内的图形项

---

```python
    """
```
    # 文档字符串结束标记

---

```python
    __slots__ = (
```
    # 声明实例属性槽位：(，用于节省内存并提升访问速度

---

```python
        '_drag_start', '_drag_current',
```
        # '_drag_start', '_drag_current'

---

```python
        '_dragging_anchor_idx', '_dragging_handle_idx',
```
        # 函数参数续行：'_dragging_anchor_idx', '_dragging_handle_idx'

---

```python
        '_dragging_handle_type', '_dragging_item',
```
        # '_dragging_handle_type', '_dragging_item'

---

```python
        '_drag_offset', '_selected_anchor_idx',
```
        # 函数参数续行：'_drag_offset', '_selected_anchor_idx'

---

```python
        '_is_marquee', '_old_anchors',
```
        # 函数参数续行：'_is_marquee', '_old_anchors'

---

```python
        '_has_moved',
```
        # '_has_moved'

---

```python
        '_press_alt',           # 按下时 Alt 是否已激活（用于断手柄）
```
        # '_press_alt',           # 按下时 Alt 是否已激活（用于断手柄）

---

```python
        '_original_anchor_type', # 记录拖拽前锚点类型
```
        # 函数参数续行：'_original_anchor_type', # 记录拖拽前锚点类型

---

```python
    )
```
    # )


---

```python
    # 基础容差（100%缩放下的像素值，与 AI 一致）
```
    # 注释：基础容差（100%缩放下的像素值，与 AI 一致）

---

```python
    ANCHOR_TOLERANCE = 5.0       # 锚点点击容差
```
    # 类属性：锚点点击容差（100%缩放下的像素值）

---

```python
    HANDLE_TOLERANCE = 4.0       # 手柄点击容差  
```
    # 类属性：手柄点击容差（100%缩放下的像素值）

---

```python
    SEGMENT_TOLERANCE = 4.0      # 路径段点击容差
```
    # 类属性：路径段点击容差（100%缩放下的像素值）

---

```python
    DRAG_THRESHOLD = 3.0         # 最小拖拽阈值（像素）
```
    # 类属性：最小拖拽阈值（像素）


---

```python
    def __init__(self):
```
    # 构造函数，接收自身引用，无返回值

---

```python
        super().__init__(ToolType.DIRECT_SELECT)
```
        # 调用父类构造函数，传入ToolType.DIRECT_SELECT

---

```python
        self._drag_start: QPointF | None = None
```
        # 拖拽起始位置

---

```python
        self._drag_current: QPointF | None = None
```
        # 当前拖拽位置

---

```python
        self._dragging_anchor_idx: int = -1
```
        # 正在拖拽的锚点索引

---

```python
        self._dragging_handle_idx: int = -1
```
        # 正在拖拽的手柄索引

---

```python
        self._dragging_handle_type: str = ''
```
        # 正在拖拽的手柄类型

---

```python
        self._dragging_item: GraphicItem | None = None
```
        # 正在拖拽的图形项

---

```python
        self._drag_offset = QPointF(0, 0)
```
        # 拖拽偏移量

---

```python
        self._selected_anchor_idx: int = -1
```
        # 当前选中的锚点索引

---

```python
        self._is_marquee: bool = False
```
        # 是否为框选模式

---

```python
        self._old_anchors: list[AnchorPoint] = []
```
        # 操作前的锚点状态快照（用于撤销）

---

```python
        self._has_moved: bool = False
```
        # 是否已发生移动

---

```python
        self._press_alt: bool = False
```
        # 按下时Alt键是否已激活

---

```python
        self._original_anchor_type: AnchorPointType | None = None
```
        # 拖拽前的原始锚点类型


---

```python
    # ── 辅助方法 ──
```
    # 注释：── 辅助方法 ──


---

```python
    @staticmethod
```
    # 静态方法装饰器，该方法不依赖实例状态

---

```python
    def _safe_inverted(transform):
```
    # 安全获取逆变换矩阵（静态方法），接收变换矩阵，无返回值

---

```python
        """安全获取逆变换矩阵，返回 (inverted_transform, success)"""
```
        # 单行文档字符串：安全获取逆变换矩阵，返回 (inverted_transform, success)

---

```python
        try:
```
        # 开始异常处理块（尝试执行可能出错的代码）

---

```python
            inv, ok = transform.inverted()
```
            # inv, ok = transform.inverted()

---

```python
            return (inv, ok)
```
            # 返回(inv, ok)

---

```python
        except Exception:
```
        # 捕获所有异常

---

```python
            return (transform, False)
```
            # 返回(transform, False)


---

```python
    def _find_path_at(self, pos: QPointF, must_be_selected: bool = False) -> tuple[PathItem | None, QPointF | None]:
```
    # 从文档中查找点击位置的路径项，接收自身引用、鼠标位置坐标：二维浮点坐标、是否只搜索已选中路径：bool = False，返回tuple[PathItem | None, QPointF | None]

---

```python
        """从文档中查找点击位置的 PathItem，返回 (item, local_pos)"""
```
        # 单行文档字符串：从文档中查找点击位置的 PathItem，返回 (item, local_pos)

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return (None, None)
```
            # 返回(None, None)

---

```python
        for layer in reversed(self._document.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in layer.items:
```
            # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or not item.anchors:
```
                # 如果not isinstance(item, PathItem) or not item.anchors（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                if must_be_selected and not item.selected:
```
                # 如果must_be_selected and not item.selected（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                inv, ok = self._safe_inverted(item._transform)
```
                # 函数参数续行：inv, ok = self._safe_inverted(item._transform)

---

```python
                if not ok:
```
                # 如果not ok（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                local_pos = inv.map(pos)
```
                # 将inv.map(pos)赋值给local_pos

---

```python
                # 用 bounding_rect 快速判断（放宽一点）
```
                # 注释：用 bounding_rect 快速判断（放宽一点）

---

```python
                br = item.bounding_rect()
```
                # 将item.bounding_rect()赋值给br

---

```python
                if not br.contains(local_pos):
```
                # 如果not br.contains(local_pos)（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                return (item, local_pos)
```
                # 返回(item, local_pos)

---

```python
        return (None, None)
```
        # 返回(None, None)


---

```python
    # ── 鼠标事件 ──
```
    # 注释：── 鼠标事件 ──


---

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
    # 鼠标按下事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        self._drag_start = QPointF(pos)
```
        # 拖拽起始位置

---

```python
        self._drag_current = QPointF(pos)
```
        # 当前拖拽位置

---

```python
        self._has_moved = False
```
        # 是否已发生移动

---

```python
        self._press_alt = bool(modifiers & Qt.AltModifier)
```
        # 按下时Alt键是否已激活

---

```python
        self._original_anchor_type = None
```
        # 拖拽前的原始锚点类型


---

```python
        shift = bool(modifiers & Qt.ShiftModifier)
```
        # 将bool(modifiers & Qt.ShiftModifier)赋值给shift


---

```python
        # ── 1. 优先检测已选中路径的手柄 ──
```
        # 注释：── 1. 优先检测已选中路径的手柄 ──

---

```python
        for layer in reversed(self._document.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in layer.items:
```
            # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
                # 如果not isinstance(item, PathItem) or not item.selected or not item.anchors（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                inv, ok = self._safe_inverted(item._transform)
```
                # 函数参数续行：inv, ok = self._safe_inverted(item._transform)

---

```python
                if not ok:
```
                # 如果not ok（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                local_pos = inv.map(pos)
```
                # 将inv.map(pos)赋值给local_pos

---

```python
                idx, htype = item.get_handle_at(
```
                # 函数参数续行：idx, htype = item.get_handle_at(

---

```python
                    local_pos.x(), local_pos.y(),
```
                    # 函数参数续行：local_pos.x(), local_pos.y()

---

```python
                    tolerance=self.HANDLE_TOLERANCE,
```
                    # 将self.HANDLE_TOLERANCE,赋值给tolerance

---

```python
                )
```
                # )

---

```python
                if idx >= 0:
```
                # 如果idx >= 0（满足条件时执行）

---

```python
                    self._dragging_item = item
```
                    # 正在拖拽的图形项

---

```python
                    self._dragging_handle_idx = idx
```
                    # 正在拖拽的手柄索引

---

```python
                    self._dragging_handle_type = htype
```
                    # 正在拖拽的手柄类型

---

```python
                    self._selected_anchor_idx = idx
```
                    # 当前选中的锚点索引

---

```python
                    self._old_anchors = [a.copy() for a in item.anchors]
```
                    # 操作前的锚点状态快照（用于撤销）

---

```python
                    # 记录原始锚点类型（Alt 拖拽时断开约束）
```
                    # 注释：记录原始锚点类型（Alt 拖拽时断开约束）

---

```python
                    self._original_anchor_type = item.anchors[idx].anchor_type
```
                    # 拖拽前的原始锚点类型

---

```python
                    # 如果按 Alt，将锚点转为角点（断开对称约束）
```
                    # 注释：如果按 Alt，将锚点转为角点（断开对称约束）

---

```python
                    if self._press_alt:
```
                    # 如果self._press_alt（满足条件时执行）

---

```python
                        item.anchors[idx].convert_to_corner()
```
                        # 函数参数续行：item.anchors[idx].convert_to_corner()

---

```python
                    return
```
                    # 空返回，结束函数执行


---

```python
        # ── 2. 检测已选中路径的锚点 ──
```
        # 注释：── 2. 检测已选中路径的锚点 ──

---

```python
        for layer in reversed(self._document.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in layer.items:
```
            # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
                # 如果not isinstance(item, PathItem) or not item.selected or not item.anchors（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                inv, ok = self._safe_inverted(item._transform)
```
                # 函数参数续行：inv, ok = self._safe_inverted(item._transform)

---

```python
                if not ok:
```
                # 如果not ok（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                local_pos = inv.map(pos)
```
                # 将inv.map(pos)赋值给local_pos

---

```python
                idx = item.get_anchor_at(
```
                # 将item.get_anchor_at(赋值给idx

---

```python
                    local_pos.x(), local_pos.y(),
```
                    # 函数参数续行：local_pos.x(), local_pos.y()

---

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
                    # 将self.ANCHOR_TOLERANCE,赋值给tolerance

---

```python
                )
```
                # )

---

```python
                if idx >= 0:
```
                # 如果idx >= 0（满足条件时执行）

---

```python
                    self._dragging_item = item
```
                    # 正在拖拽的图形项

---

```python
                    self._dragging_anchor_idx = idx
```
                    # 正在拖拽的锚点索引

---

```python
                    self._selected_anchor_idx = idx
```
                    # 当前选中的锚点索引

---

```python
                    self._old_anchors = [a.copy() for a in item.anchors]
```
                    # 操作前的锚点状态快照（用于撤销）

---

```python
                    self._original_anchor_type = item.anchors[idx].anchor_type
```
                    # 拖拽前的原始锚点类型

---

```python
                    return
```
                    # 空返回，结束函数执行


---

```python
        # ── 3. 检测已选中路径的线段（AI：点击线段选中路径但不添加锚点）──
```
        # 注释：── 3. 检测已选中路径的线段（AI：点击线段选中路径但不添加锚点）──

---

```python
        for layer in reversed(self._document.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in layer.items:
```
            # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
                # 如果not isinstance(item, PathItem) or not item.selected or not item.anchors（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                inv, ok = self._safe_inverted(item._transform)
```
                # 函数参数续行：inv, ok = self._safe_inverted(item._transform)

---

```python
                if not ok:
```
                # 如果not ok（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                local_pos = inv.map(pos)
```
                # 将inv.map(pos)赋值给local_pos

---

```python
                seg = item.get_segment_at(
```
                # 将item.get_segment_at(赋值给seg

---

```python
                    local_pos.x(), local_pos.y(),
```
                    # 函数参数续行：local_pos.x(), local_pos.y()

---

```python
                    tolerance=self.SEGMENT_TOLERANCE,
```
                    # 将self.SEGMENT_TOLERANCE,赋值给tolerance

---

```python
                )
```
                # )

---

```python
                if seg >= 0:
```
                # 如果seg >= 0（满足条件时执行）

---

```python
                    # AI 行为：点击已选中路径的线段，选中该路径用于整体拖拽
```
                    # 注释：AI 行为：点击已选中路径的线段，选中该路径用于整体拖拽

---

```python
                    self._dragging_item = item
```
                    # 正在拖拽的图形项

---

```python
                    self._selected_anchor_idx = -1  # 不选中特定锚点
```
                    # 当前选中的锚点索引

---

```python
                    return
```
                    # 空返回，结束函数执行


---

```python
        # ── 4. 检测未选中路径 → 选中它并准备整体拖拽 ──
```
        # 注释：── 4. 检测未选中路径 → 选中它并准备整体拖拽 ──

---

```python
        # AI 行为：用 Direct Select 工具点击未选中路径的任意位置 → 选中路径显示锚点
```
        # 注释：AI 行为：用 Direct Select 工具点击未选中路径的任意位置 → 选中路径显示锚点

---

```python
        for layer in reversed(self._document.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in layer.items:
```
            # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or item.selected or not item.anchors:
```
                # 如果not isinstance(item, PathItem) or item.selected or not item.anchors（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                inv, ok = self._safe_inverted(item._transform)
```
                # 函数参数续行：inv, ok = self._safe_inverted(item._transform)

---

```python
                if not ok:
```
                # 如果not ok（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                local_pos = inv.map(pos)
```
                # 将inv.map(pos)赋值给local_pos

---

```python
                
```
                # 

---

```python
                # 先检查是否在路径段附近
```
                # 注释：先检查是否在路径段附近

---

```python
                seg = item.get_segment_at(
```
                # 将item.get_segment_at(赋值给seg

---

```python
                    local_pos.x(), local_pos.y(),
```
                    # 函数参数续行：local_pos.x(), local_pos.y()

---

```python
                    tolerance=self.SEGMENT_TOLERANCE,
```
                    # 将self.SEGMENT_TOLERANCE,赋值给tolerance

---

```python
                )
```
                # )

---

```python
                if seg >= 0:
```
                # 如果seg >= 0（满足条件时执行）

---

```python
                    if not shift:
```
                    # 如果not shift（满足条件时执行）

---

```python
                        self._document.clear_selection()
```
                        # 调用self._document的清除所有选中状态方法

---

```python
                    item.selected = True
```
                    # 将True赋值给item.selected

---

```python
                    self._dragging_item = item
```
                    # 正在拖拽的图形项

---

```python
                    self._selected_anchor_idx = -1
```
                    # 当前选中的锚点索引

---

```python
                    return
```
                    # 空返回，结束函数执行

---

```python
                
```
                # 

---

```python
                # 再检查是否在锚点附近
```
                # 注释：再检查是否在锚点附近

---

```python
                idx = item.get_anchor_at(
```
                # 将item.get_anchor_at(赋值给idx

---

```python
                    local_pos.x(), local_pos.y(),
```
                    # 函数参数续行：local_pos.x(), local_pos.y()

---

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
                    # 将self.ANCHOR_TOLERANCE,赋值给tolerance

---

```python
                )
```
                # )

---

```python
                if idx >= 0:
```
                # 如果idx >= 0（满足条件时执行）

---

```python
                    if not shift:
```
                    # 如果not shift（满足条件时执行）

---

```python
                        self._document.clear_selection()
```
                        # 调用self._document的清除所有选中状态方法

---

```python
                    item.selected = True
```
                    # 将True赋值给item.selected

---

```python
                    self._dragging_item = item
```
                    # 正在拖拽的图形项

---

```python
                    self._dragging_anchor_idx = idx
```
                    # 正在拖拽的锚点索引

---

```python
                    self._selected_anchor_idx = idx
```
                    # 当前选中的锚点索引

---

```python
                    self._old_anchors = [a.copy() for a in item.anchors]
```
                    # 操作前的锚点状态快照（用于撤销）

---

```python
                    self._original_anchor_type = item.anchors[idx].anchor_type
```
                    # 拖拽前的原始锚点类型

---

```python
                    return
```
                    # 空返回，结束函数执行

---

```python
                
```
                # 

---

```python
                # 最后检查填充区域
```
                # 注释：最后检查填充区域

---

```python
                if item.contains_point(local_pos):
```
                # 如果item.contains_point(local_pos)（满足条件时执行）

---

```python
                    if not shift:
```
                    # 如果not shift（满足条件时执行）

---

```python
                        self._document.clear_selection()
```
                        # 调用self._document的清除所有选中状态方法

---

```python
                    item.selected = True
```
                    # 将True赋值给item.selected

---

```python
                    self._dragging_item = item
```
                    # 正在拖拽的图形项

---

```python
                    self._selected_anchor_idx = -1
```
                    # 当前选中的锚点索引

---

```python
                    return
```
                    # 空返回，结束函数执行


---

```python
        # ── 5. 检测普通图形项 ──
```
        # 注释：── 5. 检测普通图形项 ──

---

```python
        item = self._document.get_item_at(pos.x(), pos.y())
```
        # 将self._document.get_item_at(pos.x(), pos.y())赋值给item

---

```python
        if item:
```
        # 如果item（满足条件时执行）

---

```python
            if not shift:
```
            # 如果not shift（满足条件时执行）

---

```python
                self._document.clear_selection()
```
                # 调用self._document的清除所有选中状态方法

---

```python
            item.selected = True
```
            # 将True赋值给item.selected

---

```python
            self._dragging_item = item
```
            # 正在拖拽的图形项

---

```python
            self._selected_anchor_idx = -1
```
            # 当前选中的锚点索引

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # ── 6. 框选 ──
```
        # 注释：── 6. 框选 ──

---

```python
        if not shift:
```
        # 如果not shift（满足条件时执行）

---

```python
            self._document.clear_selection()
```
            # 调用self._document的清除所有选中状态方法

---

```python
        self._is_marquee = True
```
        # 是否为框选模式


---

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
    # 鼠标移动事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if self._drag_start is None:
```
        # 如果拖拽起始位置为空（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        self._drag_current = QPointF(pos)
```
        # 当前拖拽位置


---

```python
        dx_total = pos.x() - self._drag_start.x()
```
        # 将pos.x() - self._drag_start.x()赋值给dx_total

---

```python
        dy_total = pos.y() - self._drag_start.y()
```
        # 将pos.y() - self._drag_start.y()赋值给dy_total

---

```python
        dist = math.sqrt(dx_total * dx_total + dy_total * dy_total)
```
        # 将math.sqrt(dx_total * dx_total + dy_total * dy_total)赋值给dist

---

```python
        alt_held = bool(modifiers & Qt.AltModifier)
```
        # 将bool(modifiers & Qt.AltModifier)赋值给alt_held


---

```python
        # ── 手柄拖拽 ──
```
        # 注释：── 手柄拖拽 ──

---

```python
        if self._dragging_handle_idx >= 0 and self._dragging_item:
```
        # 如果self._dragging_handle_idx >= 0 and self._dragging_item（满足条件时执行）

---

```python
            if isinstance(self._dragging_item, PathItem):
```
            # 如果isinstance(self._dragging_item, PathItem)（满足条件时执行）

---

```python
                inv, ok = self._safe_inverted(self._dragging_item._transform)
```
                # 函数参数续行：inv, ok = self._safe_inverted(self._dragging_item._transform)

---

```python
                if not ok:
```
                # 如果not ok（满足条件时执行）

---

```python
                    return
```
                    # 空返回，结束函数执行

---

```python
                local_pos = inv.map(pos)
```
                # 将inv.map(pos)赋值给local_pos

---

```python
                anchor = self._dragging_item.anchors[self._dragging_handle_idx]
```
                # 将self._dragging_item.anchors[self._dragging_handle_idx]赋值给anchor

---

```python
                rel_x = local_pos.x() - anchor.x
```
                # 将local_pos.x() - anchor.x赋值给rel_x

---

```python
                rel_y = local_pos.y() - anchor.y
```
                # 将local_pos.y() - anchor.y赋值给rel_y


---

```python
                # 平滑点约束：不按 Alt 时自动对称
```
                # 注释：平滑点约束：不按 Alt 时自动对称

---

```python
                constrain = (anchor.anchor_type == AnchorPointType.SMOOTH and not alt_held)
```
                # 将(anchor.anchor_type == AnchorPointType.SMOOTH and not alt_held)赋值给constrain


---

```python
                if self._dragging_handle_type == 'in':
```
                # 如果self._dragging_handle_type == 'in'（满足条件时执行）

---

```python
                    self._dragging_item.set_handle_in(
```
                    # 调用self._dragging_item的set_handle_in方法（续行参数）

---

```python
                        self._dragging_handle_idx, rel_x, rel_y,
```
                        # 函数参数续行：self._dragging_handle_idx, rel_x, rel_y

---

```python
                        constrain_smooth=constrain,
```
                        # 将constrain,赋值给constrain_smooth

---

```python
                    )
```
                    # )

---

```python
                else:
```
                # 否则（不满足上述条件时执行）

---

```python
                    self._dragging_item.set_handle_out(
```
                    # 调用self._dragging_item的set_handle_out方法（续行参数）

---

```python
                        self._dragging_handle_idx, rel_x, rel_y,
```
                        # 函数参数续行：self._dragging_handle_idx, rel_x, rel_y

---

```python
                        constrain_smooth=constrain,
```
                        # 将constrain,赋值给constrain_smooth

---

```python
                    )
```
                    # )

---

```python
                if self._document:
```
                # 如果self._document（满足条件时执行）

---

```python
                    self._document.modified = True
```
                    # 将True赋值给self._document.modified


---

```python
        # ── 锚点拖拽（超过阈值后移动）──
```
        # 注释：── 锚点拖拽（超过阈值后移动）──

---

```python
        elif self._dragging_anchor_idx >= 0 and self._dragging_item:
```
        # 如果self._dragging_anchor_idx >= 0 and self._dragging_item（满足条件时执行）

---

```python
            if not self._has_moved:
```
            # 如果not self._has_moved（满足条件时执行）

---

```python
                if dist < self.DRAG_THRESHOLD:
```
                # 如果dist < self.DRAG_THRESHOLD（满足条件时执行）

---

```python
                    return
```
                    # 空返回，结束函数执行

---

```python
                self._has_moved = True
```
                # 是否已发生移动


---

```python
            if isinstance(self._dragging_item, PathItem):
```
            # 如果isinstance(self._dragging_item, PathItem)（满足条件时执行）

---

```python
                inv, ok = self._safe_inverted(self._dragging_item._transform)
```
                # 函数参数续行：inv, ok = self._safe_inverted(self._dragging_item._transform)

---

```python
                if not ok:
```
                # 如果not ok（满足条件时执行）

---

```python
                    return
```
                    # 空返回，结束函数执行

---

```python
                local_pos = inv.map(pos)
```
                # 将inv.map(pos)赋值给local_pos

---

```python
                self._dragging_item.move_anchor(
```
                # 调用self._dragging_item的move_anchor方法（续行参数）

---

```python
                    self._dragging_anchor_idx, local_pos.x(), local_pos.y(),
```
                    # 函数参数续行：self._dragging_anchor_idx, local_pos.x(), local_pos.y()

---

```python
                )
```
                # )

---

```python
                if self._document:
```
                # 如果self._document（满足条件时执行）

---

```python
                    self._document.modified = True
```
                    # 将True赋值给self._document.modified


---

```python
        # ── 整项拖拽（非锚点/手柄拖拽模式）──
```
        # 注释：── 整项拖拽（非锚点/手柄拖拽模式）──

---

```python
        elif self._dragging_item and not self._is_marquee:
```
        # 如果self._dragging_item and not self._is_marquee（满足条件时执行）

---

```python
            if not self._has_moved:
```
            # 如果not self._has_moved（满足条件时执行）

---

```python
                if dist < self.DRAG_THRESHOLD:
```
                # 如果dist < self.DRAG_THRESHOLD（满足条件时执行）

---

```python
                    return
```
                    # 空返回，结束函数执行

---

```python
                self._has_moved = True
```
                # 是否已发生移动


---

```python
            dx = pos.x() - self._drag_start.x()
```
            # 将pos.x() - self._drag_start.x()赋值给dx

---

```python
            dy = pos.y() - self._drag_start.y()
```
            # 将pos.y() - self._drag_start.y()赋值给dy

---

```python
            if modifiers & Qt.ShiftModifier:
```
            # 如果modifiers & Qt.ShiftModifier（满足条件时执行）

---

```python
                dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)
```
                # 函数参数续行：dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)

---

```python
            self._dragging_item.move_by(dx, dy)
```
            # 调用self._dragging_item的移动方法

---

```python
            self._drag_start = QPointF(pos)
```
            # 拖拽起始位置

---

```python
            if self._document:
```
            # 如果self._document（满足条件时执行）

---

```python
                self._document.modified = True
```
                # 将True赋值给self._document.modified


---

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
    # 鼠标释放事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        # ── 如果拖拽了手柄且按了 Alt，需要恢复锚点类型为角点 ──
```
        # 注释：── 如果拖拽了手柄且按了 Alt，需要恢复锚点类型为角点 ──

---

```python
        if self._dragging_handle_idx >= 0 and self._dragging_item:
```
        # 如果self._dragging_handle_idx >= 0 and self._dragging_item（满足条件时执行）

---

```python
            if isinstance(self._dragging_item, PathItem):
```
            # 如果isinstance(self._dragging_item, PathItem)（满足条件时执行）

---

```python
                if self._press_alt or self._has_moved:
```
                # 如果self._press_alt or self._has_moved（满足条件时执行）

---

```python
                    # Alt+拖拽：断开对称约束，转为角点
```
                    # 注释：Alt+拖拽：断开对称约束，转为角点

---

```python
                    anchor = self._dragging_item.anchors[self._dragging_handle_idx]
```
                    # 将self._dragging_item.anchors[self._dragging_handle_idx]赋值给anchor

---

```python
                    if self._press_alt:
```
                    # 如果self._press_alt（满足条件时执行）

---

```python
                        anchor.anchor_type = AnchorPointType.CORNER
```
                        # 将AnchorPointType.CORNER赋值给anchor.anchor_type

---

```python
                    self._dragging_item._build_path()
```
                    # 调用self._dragging_item的重建贝塞尔路径方法


---

```python
        # ── 记录撤销命令（通过 execute_command 统一入口）──
```
        # 注释：── 记录撤销命令（通过 execute_command 统一入口）──

---

```python
        if self._old_anchors and self._dragging_item and self._document:
```
        # 如果self._old_anchors and self._dragging_item and self._document（满足条件时执行）

---

```python
            if isinstance(self._dragging_item, PathItem):
```
            # 如果isinstance(self._dragging_item, PathItem)（满足条件时执行）

---

```python
                new_anchors = [a.copy() for a in self._dragging_item.anchors]
```
                # 将[a.copy() for a in self._dragging_item.anchors]赋值给new_anchors

---

```python
                if self._has_moved and len(self._old_anchors) == len(new_anchors):
```
                # 如果self._has_moved and len(self._old_anchors) == len(new_anchors)（满足条件时执行）

---

```python
                    # 检查是否真的有变化
```
                    # 注释：检查是否真的有变化

---

```python
                    changed = False
```
                    # 将False赋值给changed

---

```python
                    for old, new in zip(self._old_anchors, new_anchors):
```
                    # 遍历zip(self._old_anchors, new_anchors)，每次迭代将当前元素赋给old, new

---

```python
                        if (old.x != new.x or old.y != new.y or
```
                        # if (old.x != new.x or old.y != new.y or

---

```python
                            old.handle_in != new.handle_in or
```
                            # old.handle_in != new.handle_in or

---

```python
                            old.handle_out != new.handle_out or
```
                            # old.handle_out != new.handle_out or

---

```python
                            old.anchor_type != new.anchor_type):
```
                            # 函数参数续行：old.anchor_type != new.anchor_type):

---

```python
                            changed = True
```
                            # 将True赋值给changed

---

```python
                            break
```
                            # 跳出当前循环

---

```python
                    if changed:
```
                    # 如果changed（满足条件时执行）

---

```python
                        cmd = ModifyAnchorCommand(
```
                        # 将ModifyAnchorCommand(赋值给cmd

---

```python
                            self._document, self._dragging_item,
```
                            # 函数参数续行：self._document, self._dragging_item

---

```python
                            self._old_anchors, new_anchors,
```
                            # 函数参数续行：self._old_anchors, new_anchors

---

```python
                        )
```
                        # )

---

```python
                        self._document.execute_command(cmd)
```
                        # 调用self._document的执行命令（支持撤销）方法


---

```python
        # ── 框选 ──
```
        # 注释：── 框选 ──

---

```python
        if self._is_marquee and self._drag_start and self._document:
```
        # 如果self._is_marquee and self._drag_start and self._document（满足条件时执行）

---

```python
            rect = QRectF(self._drag_start, pos).normalized()
```
            # 将QRectF(self._drag_start, pos).normalized()赋值给rect

---

```python
            if rect.width() > 2 and rect.height() > 2:
```
            # 如果rect.width() > 2 and rect.height() > 2（满足条件时执行）

---

```python
                for layer in self._document.layers:
```
                # 遍历文档的所有图层，每次迭代将当前元素赋给layer

---

```python
                    items = layer.get_items_in_rect(
```
                    # 将layer.get_items_in_rect(赋值给items

---

```python
                        rect.x(), rect.y(), rect.width(), rect.height(),
```
                        # rect.x(), rect.y(), rect.width(), rect.height()

---

```python
                    )
```
                    # )

---

```python
                    for item in items:
```
                    # 遍历items，每次迭代将当前元素赋给item

---

```python
                        item.selected = True
```
                        # 将True赋值给item.selected


---

```python
        # ── 重置状态 ──
```
        # 注释：── 重置状态 ──

---

```python
        self._drag_start = None
```
        # 拖拽起始位置

---

```python
        self._drag_current = None
```
        # 当前拖拽位置

---

```python
        self._dragging_anchor_idx = -1
```
        # 正在拖拽的锚点索引

---

```python
        self._dragging_handle_idx = -1
```
        # 正在拖拽的手柄索引

---

```python
        self._dragging_handle_type = ''
```
        # 正在拖拽的手柄类型

---

```python
        self._dragging_item = None
```
        # 正在拖拽的图形项

---

```python
        self._is_marquee = False
```
        # 是否为框选模式

---

```python
        self._old_anchors = []
```
        # 操作前的锚点状态快照（用于撤销）

---

```python
        self._has_moved = False
```
        # 是否已发生移动

---

```python
        self._press_alt = False
```
        # 按下时Alt键是否已激活

---

```python
        self._original_anchor_type = None
```
        # 拖拽前的原始锚点类型


---

```python
    # ── 键盘 ──
```
    # 注释：── 键盘 ──


---

```python
    def key_press(self, key: int, modifiers: int):
```
    # 键盘按键事件处理，接收自身引用、按键码：整数、修饰键标志位：整数，无返回值

---

```python
        """键盘操作对照 AI 行为"""
```
        # 单行文档字符串：键盘操作对照 AI 行为

---

```python
        # Delete/Backspace 删除选中的锚点（AI：Delete Anchor Point）
```
        # 注释：Delete/Backspace 删除选中的锚点（AI：Delete Anchor Point）

---

```python
        if key in (Qt.Key_Delete, Qt.Key_Backspace):
```
        # 如果key in (Qt.Key_Delete, Qt.Key_Backspace)（满足条件时执行）

---

```python
            if self._selected_anchor_idx >= 0 and self._dragging_item:
```
            # 如果self._selected_anchor_idx >= 0 and self._dragging_item（满足条件时执行）

---

```python
                if isinstance(self._dragging_item, PathItem):
```
                # 如果isinstance(self._dragging_item, PathItem)（满足条件时执行）

---

```python
                    if self._dragging_item.anchor_count > 2:
```
                    # 如果self._dragging_item.anchor_count > 2（满足条件时执行）

---

```python
                        old_anchors = [a.copy() for a in self._dragging_item.anchors]
```
                        # 将[a.copy() for a in self._dragging_item.anchors]赋值给old_anchors

---

```python
                        self._dragging_item.remove_anchor(self._selected_anchor_idx)
```
                        # 调用self._dragging_item的移除锚点方法

---

```python
                        if self._document:
```
                        # 如果self._document（满足条件时执行）

---

```python
                            new_anchors = [a.copy() for a in self._dragging_item.anchors]
```
                            # 将[a.copy() for a in self._dragging_item.anchors]赋值给new_anchors

---

```python
                            cmd = ModifyAnchorCommand(
```
                            # 将ModifyAnchorCommand(赋值给cmd

---

```python
                                self._document, self._dragging_item,
```
                                # 函数参数续行：self._document, self._dragging_item

---

```python
                                old_anchors, new_anchors,
```
                                # 函数参数续行：old_anchors, new_anchors

---

```python
                            )
```
                            # )

---

```python
                            self._document.execute_command(cmd)
```
                            # 调用self._document的执行命令（支持撤销）方法

---

```python
                        self._selected_anchor_idx = max(0, min(
```
                        # 当前选中的锚点索引

---

```python
                            self._selected_anchor_idx,
```
                            # 函数参数：self._selected_anchor_idx

---

```python
                            self._dragging_item.anchor_count - 1,
```
                            # 函数参数续行：self._dragging_item.anchor_count - 1

---

```python
                        ))
```
                        # ))

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # Plus/Equal 在选中锚点后添加新锚点（段中点）
```
        # 注释：Plus/Equal 在选中锚点后添加新锚点（段中点）

---

```python
        if key in (Qt.Key_Plus, Qt.Key_Equal):
```
        # 如果key in (Qt.Key_Plus, Qt.Key_Equal)（满足条件时执行）

---

```python
            if self._selected_anchor_idx >= 0 and self._dragging_item:
```
            # 如果self._selected_anchor_idx >= 0 and self._dragging_item（满足条件时执行）

---

```python
                if isinstance(self._dragging_item, PathItem):
```
                # 如果isinstance(self._dragging_item, PathItem)（满足条件时执行）

---

```python
                    self._add_anchor_after_selected(self._dragging_item)
```
                    # 调用self的_add_anchor_after_selected方法

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
    def _add_anchor_after_selected(self, item: PathItem):
```
    # 在选中锚点之后的段中点添加新锚点，接收自身引用、图形项：贝塞尔路径项，无返回值

---

```python
        """在选中锚点之后的段中点添加新锚点"""
```
        # 单行文档字符串：在选中锚点之后的段中点添加新锚点

---

```python
        anchors = item.anchors
```
        # 将item.anchors赋值给anchors

---

```python
        i = self._selected_anchor_idx
```
        # 将self._selected_anchor_idx赋值给i

---

```python
        if i < 0 or len(anchors) < 2:
```
        # 如果i < 0 or len(anchors) < 2（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        n = len(anchors)
```
        # 将len(anchors)赋值给n

---

```python
        j = (i + 1) % n
```
        # 将(i + 1) % n赋值给j

---

```python
        if not item.closed and i == n - 1:
```
        # 如果not item.closed and i == n - 1（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        
```
        # 

---

```python
        # 在贝塞尔曲线段的中点添加锚点
```
        # 注释：在贝塞尔曲线段的中点添加锚点

---

```python
        prev, curr = anchors[i], anchors[j]
```
        # 函数参数续行：prev, curr = anchors[i], anchors[j]

---

```python
        
```
        # 

---

```python
        # 使用贝塞尔采样获取真正的中点
```
        # 注释：使用贝塞尔采样获取真正的中点

---

```python
        samples = PathItem._sample_bezier_segment(prev, curr, num_samples=4)
```
        # 将PathItem._sample_bezier_segment(prev, curr, num_samples=4)赋值给samples

---

```python
        if len(samples) >= 2:
```
        # 如果len(samples) >= 2（满足条件时执行）

---

```python
            # 取中点
```
            # 注释：取中点

---

```python
            mid_idx = len(samples) // 2
```
            # 将len(samples) // 2赋值给mid_idx

---

```python
            mx, my = samples[mid_idx]
```
            # 函数参数续行：mx, my = samples[mid_idx]

---

```python
        else:
```
        # 否则（不满足上述条件时执行）

---

```python
            mx = (prev.x + curr.x) / 2
```
            # 将(prev.x + curr.x) / 2赋值给mx

---

```python
            my = (prev.y + curr.y) / 2
```
            # 将(prev.y + curr.y) / 2赋值给my

---

```python
        
```
        # 

---

```python
        old_anchors = [a.copy() for a in anchors]
```
        # 将[a.copy() for a in anchors]赋值给old_anchors

---

```python
        new_anchor = AnchorPoint(mx, my)
```
        # 将AnchorPoint(mx, my)赋值给new_anchor

---

```python
        item.insert_anchor(i + 1, new_anchor)
```
        # 调用item的插入锚点方法

---

```python
        self._selected_anchor_idx = i + 1
```
        # 当前选中的锚点索引

---

```python
        self._dragging_item = item
```
        # 正在拖拽的图形项

---

```python
        
```
        # 

---

```python
        if self._document:
```
        # 如果self._document（满足条件时执行）

---

```python
            new_anchors = [a.copy() for a in item.anchors]
```
            # 将[a.copy() for a in item.anchors]赋值给new_anchors

---

```python
            cmd = ModifyAnchorCommand(
```
            # 将ModifyAnchorCommand(赋值给cmd

---

```python
                self._document, item, old_anchors, new_anchors,
```
                # 函数参数续行：self._document, item, old_anchors, new_anchors

---

```python
            )
```
            # )

---

```python
            self._document.execute_command(cmd)
```
            # 调用self._document的执行命令（支持撤销）方法


---

```python
    # ── 绘制预览 ──
```
    # 注释：── 绘制预览 ──


---

```python
    def draw_preview(self, painter: QPainter):
```
    # 绘制预览，接收自身引用、绘图引擎：绘图引擎，无返回值

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        for layer in self._document.layers:
```
        # 遍历文档的所有图层，每次迭代将当前元素赋给layer

---

```python
            if not layer.visible:
```
            # 如果not layer.visible（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in layer.items:
```
            # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                if isinstance(item, PathItem) and item.selected:
```
                # 如果isinstance(item, PathItem) and item.selected（满足条件时执行）

---

```python
                    self._draw_anchor_handles(painter, item)
```
                    # 调用self的_draw_anchor_handles方法


---

```python
        if self._is_marquee and self._drag_start and self._drag_current:
```
        # 如果self._is_marquee and self._drag_start and self._drag_current（满足条件时执行）

---

```python
            scale = max(painter.transform().m11(), 0.001)
```
            # 将max(painter.transform().m11(), 0.001)赋值给scale

---

```python
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
```
            # 将QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)赋值给pen

---

```python
            painter.setPen(pen)
```
            # 调用painter的setPen方法

---

```python
            painter.setBrush(QColor(0, 120, 215, 30))
```
            # 调用painter的setBrush方法

---

```python
            painter.drawRect(QRectF(self._drag_start, self._drag_current))
```
            # 调用painter的drawRect方法


---

```python
    def _draw_anchor_handles(self, painter: QPainter, item: PathItem):
```
    # 绘制锚点和贝塞尔手柄，接收自身引用、绘图引擎：绘图引擎、图形项：贝塞尔路径项，无返回值

---

```python
        """绘制锚点和贝塞尔手柄，对照 AI 的视觉风格
```
        # """绘制锚点和贝塞尔手柄，对照 AI 的视觉风格

---

```python
        
```
        # 文档字符串空行

---

```python
        AI 锚点渲染规则：
```
        # 文档内容：AI 锚点渲染规则：

---

```python
        - 未选中锚点：白色填充方形，蓝色边框
```
        # 文档内容：- 未选中锚点：白色填充方形，蓝色边框

---

```python
        - 选中锚点：蓝色填充方形，深蓝边框
```
        # 文档内容：- 选中锚点：蓝色填充方形，深蓝边框

---

```python
        - 手柄线：灰色虚线（handle_in）/ 实线（handle_out）
```
        # 文档内容：- 手柄线：灰色虚线（handle_in）/ 实线（handle_out）

---

```python
        - 手柄端点：白色填充圆形，灰色边框
```
        # 文档内容：- 手柄端点：白色填充圆形，灰色边框

---

```python
        - 平滑点 vs 角点使用相同视觉表示
```
        # 文档内容：- 平滑点 vs 角点使用相同视觉表示

---

```python
        """
```
        # 文档字符串结束标记

---

```python
        if not item.anchors:
```
        # 如果not item.anchors（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        scale = max(painter.transform().m11(), 0.001)
```
        # 将max(painter.transform().m11(), 0.001)赋值给scale

---

```python
        handle_r = 3.5 / scale        # 手柄端点半径
```
        # 将3.5 / scale        # 手柄端点半径赋值给handle_r

---

```python
        anchor_half = 3.5 / scale     # 锚点半边长
```
        # 将3.5 / scale     # 锚点半边长赋值给anchor_half

---

```python
        highlight_half = 4.5 / scale  # 选中锚点半边长
```
        # 将4.5 / scale  # 选中锚点半边长赋值给highlight_half


---

```python
        transform = item._transform
```
        # 将item._transform赋值给transform

---

```python
        anchor_color = QColor(0, 120, 215)       # AI 蓝
```
        # 将QColor(0, 120, 215)       # AI 蓝赋值给anchor_color

---

```python
        anchor_border = QColor(0, 80, 180)
```
        # 将QColor(0, 80, 180)赋值给anchor_border

---

```python
        handle_color = QColor(120, 120, 120)     # 手柄线颜色
```
        # 将QColor(120, 120, 120)     # 手柄线颜色赋值给handle_color


---

```python
        for i, anchor in enumerate(item.anchors):
```
        # 遍历enumerate(item.anchors)，每次迭代将当前元素赋给i, anchor

---

```python
            ax_local, ay_local = anchor.x, anchor.y
```
            # 函数参数续行：ax_local, ay_local = anchor.x, anchor.y

---

```python
            ax = transform.map(QPointF(ax_local, ay_local)).x()
```
            # 将transform.map(QPointF(ax_local, ay_local)).x()赋值给ax

---

```python
            ay = transform.map(QPointF(ax_local, ay_local)).y()
```
            # 将transform.map(QPointF(ax_local, ay_local)).y()赋值给ay


---

```python
            # ── 绘制 handle_in 线和端点 ──
```
            # 注释：── 绘制 handle_in 线和端点 ──

---

```python
            if anchor.handle_in:
```
            # 如果anchor.handle_in（满足条件时执行）

---

```python
                hx_local = ax_local + anchor.handle_in.x()
```
                # 将ax_local + anchor.handle_in.x()赋值给hx_local

---

```python
                hy_local = ay_local + anchor.handle_in.y()
```
                # 将ay_local + anchor.handle_in.y()赋值给hy_local

---

```python
                hx_pt = transform.map(QPointF(hx_local, hy_local))
```
                # 将transform.map(QPointF(hx_local, hy_local))赋值给hx_pt

---

```python
                hx, hy = hx_pt.x(), hx_pt.y()
```
                # hx, hy = hx_pt.x(), hx_pt.y()

---

```python
                
```
                # 

---

```python
                # 手柄线
```
                # 注释：手柄线

---

```python
                handle_pen = QPen(handle_color, 1.0 / scale, Qt.DashLine)
```
                # 将QPen(handle_color, 1.0 / scale, Qt.DashLine)赋值给handle_pen

---

```python
                painter.setPen(handle_pen)
```
                # 调用painter的setPen方法

---

```python
                painter.setBrush(Qt.NoBrush)
```
                # 调用painter的setBrush方法

---

```python
                painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))
```
                # 调用painter的drawLine方法

---

```python
                
```
                # 

---

```python
                # 手柄端点（圆形）
```
                # 注释：手柄端点（圆形）

---

```python
                painter.setBrush(QColor(255, 255, 255))
```
                # 调用painter的setBrush方法

---

```python
                painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))
```
                # 调用painter的setPen方法

---

```python
                painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)
```
                # 调用painter的drawEllipse方法


---

```python
            # ── 绘制 handle_out 线和端点 ──
```
            # 注释：── 绘制 handle_out 线和端点 ──

---

```python
            if anchor.handle_out:
```
            # 如果anchor.handle_out（满足条件时执行）

---

```python
                hx_local = ax_local + anchor.handle_out.x()
```
                # 将ax_local + anchor.handle_out.x()赋值给hx_local

---

```python
                hy_local = ay_local + anchor.handle_out.y()
```
                # 将ay_local + anchor.handle_out.y()赋值给hy_local

---

```python
                hx_pt = transform.map(QPointF(hx_local, hy_local))
```
                # 将transform.map(QPointF(hx_local, hy_local))赋值给hx_pt

---

```python
                hx, hy = hx_pt.x(), hx_pt.y()
```
                # hx, hy = hx_pt.x(), hx_pt.y()

---

```python
                
```
                # 

---

```python
                # 手柄线
```
                # 注释：手柄线

---

```python
                handle_pen = QPen(handle_color, 1.0 / scale, Qt.SolidLine)
```
                # 将QPen(handle_color, 1.0 / scale, Qt.SolidLine)赋值给handle_pen

---

```python
                painter.setPen(handle_pen)
```
                # 调用painter的setPen方法

---

```python
                painter.setBrush(Qt.NoBrush)
```
                # 调用painter的setBrush方法

---

```python
                painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))
```
                # 调用painter的drawLine方法

---

```python
                
```
                # 

---

```python
                # 手柄端点（圆形）
```
                # 注释：手柄端点（圆形）

---

```python
                painter.setBrush(QColor(255, 255, 255))
```
                # 调用painter的setBrush方法

---

```python
                painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))
```
                # 调用painter的setPen方法

---

```python
                painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)
```
                # 调用painter的drawEllipse方法


---

```python
            # ── 绘制锚点（方形）──
```
            # 注释：── 绘制锚点（方形）──

---

```python
            is_highlighted = (i == self._selected_anchor_idx)
```
            # 将(i == self._selected_anchor_idx)赋值给is_highlighted

---

```python
            
```
            # 

---

```python
            if is_highlighted:
```
            # 如果is_highlighted（满足条件时执行）

---

```python
                # 选中锚点：蓝色填充
```
                # 注释：选中锚点：蓝色填充

---

```python
                painter.setBrush(anchor_color)
```
                # 调用painter的setBrush方法

---

```python
                painter.setPen(QPen(anchor_border, 1.5 / scale))
```
                # 调用painter的setPen方法

---

```python
                painter.drawRect(QRectF(
```
                # painter.drawRect(QRectF(

---

```python
                    ax - highlight_half, ay - highlight_half,
```
                    # ax - highlight_half, ay - highlight_half

---

```python
                    highlight_half * 2, highlight_half * 2,
```
                    # highlight_half * 2, highlight_half * 2

---

```python
                ))
```
                # ))

---

```python
            else:
```
            # 否则（不满足上述条件时执行）

---

```python
                # 未选中锚点：白色填充
```
                # 注释：未选中锚点：白色填充

---

```python
                painter.setBrush(QColor(255, 255, 255))
```
                # 调用painter的setBrush方法

---

```python
                painter.setPen(QPen(anchor_color, 1.5 / scale))
```
                # 调用painter的setPen方法

---

```python
                painter.drawRect(QRectF(
```
                # painter.drawRect(QRectF(

---

```python
                    ax - anchor_half, ay - anchor_half,
```
                    # 函数参数续行：ax - anchor_half, ay - anchor_half

---

```python
                    anchor_half * 2, anchor_half * 2,
```
                    # 函数参数续行：anchor_half * 2, anchor_half * 2

---

```python
                ))
```
                # ))


---

```python
    def cancel(self):
```
    # 取消当前操作，接收自身引用，无返回值

---

```python
        self._selected_anchor_idx = -1
```
        # 当前选中的锚点索引

---

```python
        self._dragging_anchor_idx = -1
```
        # 正在拖拽的锚点索引

---

```python
        self._dragging_handle_idx = -1
```
        # 正在拖拽的手柄索引

---

```python
        self._dragging_item = None
```
        # 正在拖拽的图形项

---

```python
        super().cancel()
```
        # super().cancel()


---

```python
    @staticmethod
```
    # 静态方法装饰器，该方法不依赖实例状态

---

```python
    def _draw_single_anchor(painter: QPainter, item: PathItem, 
```
    # 函数参数续行：def _draw_single_anchor(painter: QPainter, item: PathItem

---

```python
                             anchor_idx: int, highlighted: bool = True):
```
                             # 将int, highlighted: bool = True):赋值给anchor_idx

---

```python
        """绘制单个锚点（供其他锚点工具使用）"""
```
        # 单行文档字符串：绘制单个锚点（供其他锚点工具使用）

---

```python
        if anchor_idx < 0 or anchor_idx >= len(item.anchors):
```
        # 如果anchor_idx < 0 or anchor_idx >= len(item.anchors)（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        scale = max(painter.transform().m11(), 0.001)
```
        # 将max(painter.transform().m11(), 0.001)赋值给scale

---

```python
        anchor_half = 4.5 / scale if highlighted else 3.5 / scale
```
        # 条件赋值：如果highlighted则将anchor_half设为4.5 / scale，否则设为3.5 / scale

---

```python
        transform = item._transform
```
        # 将item._transform赋值给transform

---

```python
        anchor = item.anchors[anchor_idx]
```
        # 将item.anchors[anchor_idx]赋值给anchor

---

```python
        ax = transform.map(QPointF(anchor.x, anchor.y)).x()
```
        # 将transform.map(QPointF(anchor.x, anchor.y)).x()赋值给ax

---

```python
        ay = transform.map(QPointF(anchor.x, anchor.y)).y()
```
        # 将transform.map(QPointF(anchor.x, anchor.y)).y()赋值给ay

---

```python
        
```
        # 

---

```python
        if highlighted:
```
        # 如果highlighted（满足条件时执行）

---

```python
            painter.setBrush(QColor(0, 120, 215))
```
            # 调用painter的setBrush方法

---

```python
            painter.setPen(QPen(QColor(0, 80, 180), 1.5 / scale))
```
            # 调用painter的setPen方法

---

```python
        else:
```
        # 否则（不满足上述条件时执行）

---

```python
            painter.setBrush(QColor(255, 255, 255))
```
            # 调用painter的setBrush方法

---

```python
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
```
            # 调用painter的setPen方法

---

```python
        
```
        # 

---

```python
        painter.drawRect(QRectF(
```
        # painter.drawRect(QRectF(

---

```python
            ax - anchor_half, ay - anchor_half,
```
            # 函数参数续行：ax - anchor_half, ay - anchor_half

---

```python
            anchor_half * 2, anchor_half * 2,
```
            # 函数参数续行：anchor_half * 2, anchor_half * 2

---

```python
        ))
```
        # ))



---

```python
# ── 形状工具 ──────────────────────────────────────────────
```
# 注释：── 形状工具 ──────────────────────────────────────────────


---

```python
class ShapeTool(BaseTool, ABC):
```
# 定义形状工具基类（抽象），为矩形/椭圆等形状工具提供共同逻辑，继承自(BaseTool, ABC)

---

```python
    """形状工具基类（矩形/椭圆）"""
```
    # 单行文档字符串：形状工具基类（矩形/椭圆）

---

```python
    __slots__ = ('_drag_start', '_drag_current', '_preview_item')
```
    # 声明实例属性槽位：('_drag_start', '_drag_current', '_preview_item')，用于节省内存并提升访问速度


---

```python
    def __init__(self, tool_type: ToolType):
```
    # 构造函数，接收自身引用、工具类型标识：工具类型枚举，无返回值

---

```python
        super().__init__(tool_type)
```
        # 调用父类构造函数，传入tool_type

---

```python
        self._drag_start: QPointF | None = None
```
        # 拖拽起始位置

---

```python
        self._drag_current: QPointF | None = None
```
        # 当前拖拽位置

---

```python
        self._preview_item: GraphicItem | None = None
```
        # 预览图形项


---

```python
    @abstractmethod
```
    # 抽象方法装饰器，子类必须实现此方法

---

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
    # 工厂方法：创建具体图形项，接收自身引用、矩形区域：浮点矩形，返回图形项

---

```python
        ...
```
        # 省略号：占位符，表示抽象方法体由子类实现


---

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
    # 鼠标按下事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        self._drag_start = QPointF(pos)
```
        # 拖拽起始位置

---

```python
        self._drag_current = QPointF(pos)
```
        # 当前拖拽位置

---

```python
        self._is_drawing = True
```
        # 私有实例属性：是否正在绘制中

---

```python
        if self._document:
```
        # 如果self._document（满足条件时执行）

---

```python
            self._document.clear_selection()
```
            # 调用self._document的清除所有选中状态方法


---

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
    # 鼠标移动事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if self._is_drawing:
```
        # 如果在绘制状态（满足条件时执行）

---

```python
            self._drag_current = QPointF(pos)
```
            # 当前拖拽位置


---

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
    # 鼠标释放事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._is_drawing or not self._document or not self._drag_start:
```
        # 如果not self._is_drawing or not self._document or not self._drag_start（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        self._drag_current = QPointF(pos)
```
        # 当前拖拽位置

---

```python
        rect = QRectF(self._drag_start, self._drag_current).normalized()
```
        # 将QRectF(self._drag_start, self._drag_current).normalized()赋值给rect


---

```python
        # Shift 约束等比（正方形/正圆）
```
        # 注释：Shift 约束等比（正方形/正圆）

---

```python
        if modifiers & Qt.ShiftModifier:
```
        # 如果modifiers & Qt.ShiftModifier（满足条件时执行）

---

```python
            size = max(rect.width(), rect.height())
```
            # 将max(rect.width(), rect.height())赋值给size

---

```python
            if rect.width() < rect.height():
```
            # 如果rect.width() < rect.height()（满足条件时执行）

---

```python
                rect.setWidth(size)
```
                # 调用rect的设置宽度方法

---

```python
            else:
```
            # 否则（不满足上述条件时执行）

---

```python
                rect.setHeight(size)
```
                # 调用rect的设置高度方法


---

```python
        if rect.width() > 2 and rect.height() > 2:
```
        # 如果rect.width() > 2 and rect.height() > 2（满足条件时执行）

---

```python
            item = self._create_item(rect)
```
            # 将self._create_item(rect)赋值给item

---

```python
            item.selected = True
```
            # 将True赋值给item.selected

---

```python
            self._document.add_item(item)
```
            # 调用self._document的添加图形项方法


---

```python
        self._drag_start = None
```
        # 拖拽起始位置

---

```python
        self._drag_current = None
```
        # 当前拖拽位置

---

```python
        self._is_drawing = False
```
        # 私有实例属性：是否正在绘制中


---

```python
    def draw_preview(self, painter: QPainter):
```
    # 绘制预览，接收自身引用、绘图引擎：绘图引擎，无返回值

---

```python
        if self._is_drawing and self._drag_start and self._drag_current:
```
        # 如果self._is_drawing and self._drag_start and self._drag_current（满足条件时执行）

---

```python
            rect = QRectF(self._drag_start, self._drag_current).normalized()
```
            # 将QRectF(self._drag_start, self._drag_current).normalized()赋值给rect

---

```python
            scale = max(painter.transform().m11(), 0.001)
```
            # 将max(painter.transform().m11(), 0.001)赋值给scale

---

```python
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
```
            # 将QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)赋值给pen

---

```python
            painter.setPen(pen)
```
            # 调用painter的setPen方法

---

```python
            painter.setBrush(QColor(0, 120, 215, 20))
```
            # 调用painter的setBrush方法

---

```python
            painter.drawRect(rect)
```
            # 调用painter的drawRect方法



---

```python
class RectangleTool(ShapeTool):
```
# 定义矩形工具类，用于绘制矩形图形，继承自(ShapeTool)

---

```python
    """矩形工具"""
```
    # 单行文档字符串：矩形工具

---

```python
    __slots__ = ()
```
    # 声明实例属性槽位：()，用于节省内存并提升访问速度


---

```python
    def __init__(self):
```
    # 构造函数，接收自身引用，无返回值

---

```python
        super().__init__(ToolType.RECTANGLE)
```
        # 调用父类构造函数，传入ToolType.RECTANGLE


---

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
    # 工厂方法：创建具体图形项，接收自身引用、矩形区域：浮点矩形，返回图形项

---

```python
        item = RectangleItem(rect.x(), rect.y(), rect.width(), rect.height())
```
        # 将RectangleItem(rect.x(), rect.y(), rect.width(), rect.height())赋值给item

---

```python
        item.style.fill_color = QColor(200, 200, 200)
```
        # 将QColor(200, 200, 200)赋值给item.style.fill_color

---

```python
        item.style.stroke_color = QColor(50, 50, 50)
```
        # 将QColor(50, 50, 50)赋值给item.style.stroke_color

---

```python
        item.style.stroke_width = 2.0
```
        # 将2.0赋值给item.style.stroke_width

---

```python
        return item
```
        # 返回item



---

```python
class EllipseTool(ShapeTool):
```
# 定义椭圆工具类，用于绘制椭圆图形，继承自(ShapeTool)

---

```python
    """椭圆工具"""
```
    # 单行文档字符串：椭圆工具

---

```python
    __slots__ = ()
```
    # 声明实例属性槽位：()，用于节省内存并提升访问速度


---

```python
    def __init__(self):
```
    # 构造函数，接收自身引用，无返回值

---

```python
        super().__init__(ToolType.ELLIPSE)
```
        # 调用父类构造函数，传入ToolType.ELLIPSE


---

```python
    def _create_item(self, rect: QRectF) -> GraphicItem:
```
    # 工厂方法：创建具体图形项，接收自身引用、矩形区域：浮点矩形，返回图形项

---

```python
        item = EllipseItem(rect.x(), rect.y(), rect.width(), rect.height())
```
        # 将EllipseItem(rect.x(), rect.y(), rect.width(), rect.height())赋值给item

---

```python
        item.style.fill_color = QColor(200, 200, 200)
```
        # 将QColor(200, 200, 200)赋值给item.style.fill_color

---

```python
        item.style.stroke_color = QColor(50, 50, 50)
```
        # 将QColor(50, 50, 50)赋值给item.style.stroke_color

---

```python
        item.style.stroke_width = 2.0
```
        # 将2.0赋值给item.style.stroke_width

---

```python
        return item
```
        # 返回item



---

```python
# ── 添加锚点工具 (Add Anchor Point Tool, +) ──────────────────
```
# 注释：── 添加锚点工具 (Add Anchor Point Tool, +) ──────────────────


---

```python
class AddAnchorPointTool(BaseTool):
```
# 定义添加锚点工具类，在路径段上点击添加新锚点，继承自(BaseTool)

---

```python
    """添加锚点工具 —— 在路径段上点击添加新锚点
```
    # """添加锚点工具 —— 在路径段上点击添加新锚点

---

```python
    
```
    # 文档字符串空行

---

```python
    对照 AI 行为：
```
    # 文档内容：对照 AI 行为：

---

```python
    - 点击路径段 → 在最近位置添加新锚点（不进入拖拽）
```
    # 文档内容：- 点击路径段 → 在最近位置添加新锚点（不进入拖拽）

---

```python
    - 只对已选中的路径有效
```
    # 文档内容：- 只对已选中的路径有效

---

```python
    """
```
    # 文档字符串结束标记

---

```python
    __slots__ = ('_selected_anchor_idx', '_dragging_item')
```
    # 声明实例属性槽位：('_selected_anchor_idx', '_dragging_item')，用于节省内存并提升访问速度


---

```python
    SEGMENT_TOLERANCE = 4.0
```
    # 类属性：路径段点击容差（100%缩放下的像素值）


---

```python
    def __init__(self):
```
    # 构造函数，接收自身引用，无返回值

---

```python
        super().__init__(ToolType.ADD_ANCHOR)
```
        # 调用父类构造函数，传入ToolType.ADD_ANCHOR

---

```python
        self._selected_anchor_idx: int = -1
```
        # 当前选中的锚点索引

---

```python
        self._dragging_item: GraphicItem | None = None
```
        # 正在拖拽的图形项


---

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
    # 鼠标按下事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        
```
        # 

---

```python
        for layer in reversed(self._document.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in layer.items:
```
            # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
                # 如果not isinstance(item, PathItem) or not item.selected or not item.anchors（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
```
                # inv, ok = DirectSelectTool._safe_inverted(item._transform)

---

```python
                if not ok:
```
                # 如果not ok（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                local_pos = inv.map(pos)
```
                # 将inv.map(pos)赋值给local_pos

---

```python
                seg = item.get_segment_at(
```
                # 将item.get_segment_at(赋值给seg

---

```python
                    local_pos.x(), local_pos.y(),
```
                    # 函数参数续行：local_pos.x(), local_pos.y()

---

```python
                    tolerance=self.SEGMENT_TOLERANCE,
```
                    # 将self.SEGMENT_TOLERANCE,赋值给tolerance

---

```python
                )
```
                # )

---

```python
                if seg >= 0:
```
                # 如果seg >= 0（满足条件时执行）

---

```python
                    # 找到最近点
```
                    # 注释：找到最近点

---

```python
                    closest = item.get_closest_point_on_segment(seg, local_pos.x(), local_pos.y())
```
                    # 将item.get_closest_point_on_segment(seg, local_pos.x(), local_pos.y())赋值给closest

---

```python
                    
```
                    # 

---

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
                    # 将[a.copy() for a in item.anchors]赋值给old_anchors

---

```python
                    new_anchor = AnchorPoint(closest[0], closest[1])
```
                    # 将AnchorPoint(closest[0], closest[1])赋值给new_anchor

---

```python
                    insert_idx = seg + 1
```
                    # 将seg + 1赋值给insert_idx

---

```python
                    item.insert_anchor(insert_idx, new_anchor)
```
                    # 调用item的插入锚点方法

---

```python
                    
```
                    # 

---

```python
                    self._selected_anchor_idx = insert_idx
```
                    # 当前选中的锚点索引

---

```python
                    self._dragging_item = item
```
                    # 正在拖拽的图形项

---

```python
                    
```
                    # 

---

```python
                    if self._document:
```
                    # 如果self._document（满足条件时执行）

---

```python
                        new_anchors = [a.copy() for a in item.anchors]
```
                        # 将[a.copy() for a in item.anchors]赋值给new_anchors

---

```python
                        cmd = ModifyAnchorCommand(
```
                        # 将ModifyAnchorCommand(赋值给cmd

---

```python
                            self._document, item, old_anchors, new_anchors,
```
                            # 函数参数续行：self._document, item, old_anchors, new_anchors

---

```python
                        )
```
                        # )

---

```python
                        self._document.execute_command(cmd)
```
                        # 调用self._document的执行命令（支持撤销）方法

---

```python
                    return
```
                    # 空返回，结束函数执行


---

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
    # 鼠标移动事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        pass  # 不拖拽
```
        # 空操作占位符：不拖拽


---

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
    # 鼠标释放事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        pass
```
        # 空操作占位符，无实际逻辑


---

```python
    def draw_preview(self, painter: QPainter):
```
    # 绘制预览，接收自身引用、绘图引擎：绘图引擎，无返回值

---

```python
        """高亮显示新添加的锚点"""
```
        # 单行文档字符串：高亮显示新添加的锚点

---

```python
        if self._selected_anchor_idx >= 0 and self._dragging_item:
```
        # 如果self._selected_anchor_idx >= 0 and self._dragging_item（满足条件时执行）

---

```python
            if isinstance(self._dragging_item, PathItem):
```
            # 如果isinstance(self._dragging_item, PathItem)（满足条件时执行）

---

```python
                DirectSelectTool._draw_single_anchor(
```
                # 调用DirectSelectTool的_draw_single_anchor方法（续行参数）

---

```python
                    painter, self._dragging_item, self._selected_anchor_idx, True
```
                    # 函数参数续行：painter, self._dragging_item, self._selected_anchor_idx, True

---

```python
                )
```
                # )


---

```python
    def cancel(self):
```
    # 取消当前操作，接收自身引用，无返回值

---

```python
        self._selected_anchor_idx = -1
```
        # 当前选中的锚点索引

---

```python
        self._dragging_item = None
```
        # 正在拖拽的图形项

---

```python
        super().cancel()
```
        # super().cancel()



---

```python
# ── 删除锚点工具 (Delete Anchor Point Tool, -) ────────────────
```
# 注释：── 删除锚点工具 (Delete Anchor Point Tool, -) ────────────────


---

```python
class DeleteAnchorPointTool(BaseTool):
```
# 定义删除锚点工具类，点击锚点直接删除，继承自(BaseTool)

---

```python
    """删除锚点工具 —— 点击锚点直接删除
```
    # """删除锚点工具 —— 点击锚点直接删除

---

```python
    
```
    # 文档字符串空行

---

```python
    对照 AI 行为：
```
    # 文档内容：对照 AI 行为：

---

```python
    - 点击锚点 → 删除该锚点（保留路径连续性）
```
    # 文档内容：- 点击锚点 → 删除该锚点（保留路径连续性）

---

```python
    - 至少保留 2 个锚点
```
    # 文档内容：- 至少保留 2 个锚点

---

```python
    - 只对已选中的路径有效
```
    # 文档内容：- 只对已选中的路径有效

---

```python
    """
```
    # 文档字符串结束标记

---

```python
    __slots__ = ('_selected_anchor_idx', '_dragging_item')
```
    # 声明实例属性槽位：('_selected_anchor_idx', '_dragging_item')，用于节省内存并提升访问速度


---

```python
    ANCHOR_TOLERANCE = 5.0
```
    # 类属性：锚点点击容差（100%缩放下的像素值）


---

```python
    def __init__(self):
```
    # 构造函数，接收自身引用，无返回值

---

```python
        super().__init__(ToolType.DELETE_ANCHOR)
```
        # 调用父类构造函数，传入ToolType.DELETE_ANCHOR

---

```python
        self._selected_anchor_idx: int = -1
```
        # 当前选中的锚点索引

---

```python
        self._dragging_item: GraphicItem | None = None
```
        # 正在拖拽的图形项


---

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
    # 鼠标按下事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        
```
        # 

---

```python
        for layer in reversed(self._document.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in layer.items:
```
            # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
                # 如果not isinstance(item, PathItem) or not item.selected or not item.anchors（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                if item.anchor_count <= 2:
```
                # 如果item.anchor_count <= 2（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
```
                # inv, ok = DirectSelectTool._safe_inverted(item._transform)

---

```python
                if not ok:
```
                # 如果not ok（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                local_pos = inv.map(pos)
```
                # 将inv.map(pos)赋值给local_pos

---

```python
                idx = item.get_anchor_at(
```
                # 将item.get_anchor_at(赋值给idx

---

```python
                    local_pos.x(), local_pos.y(),
```
                    # 函数参数续行：local_pos.x(), local_pos.y()

---

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
                    # 将self.ANCHOR_TOLERANCE,赋值给tolerance

---

```python
                )
```
                # )

---

```python
                if idx >= 0:
```
                # 如果idx >= 0（满足条件时执行）

---

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
                    # 将[a.copy() for a in item.anchors]赋值给old_anchors

---

```python
                    item.remove_anchor(idx)
```
                    # 调用item的移除锚点方法

---

```python
                    
```
                    # 

---

```python
                    self._dragging_item = item
```
                    # 正在拖拽的图形项

---

```python
                    self._selected_anchor_idx = -1
```
                    # 当前选中的锚点索引

---

```python
                    
```
                    # 

---

```python
                    if self._document:
```
                    # 如果self._document（满足条件时执行）

---

```python
                        new_anchors = [a.copy() for a in item.anchors]
```
                        # 将[a.copy() for a in item.anchors]赋值给new_anchors

---

```python
                        cmd = ModifyAnchorCommand(
```
                        # 将ModifyAnchorCommand(赋值给cmd

---

```python
                            self._document, item, old_anchors, new_anchors,
```
                            # 函数参数续行：self._document, item, old_anchors, new_anchors

---

```python
                        )
```
                        # )

---

```python
                        self._document.execute_command(cmd)
```
                        # 调用self._document的执行命令（支持撤销）方法

---

```python
                    return
```
                    # 空返回，结束函数执行


---

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
    # 鼠标移动事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        pass
```
        # 空操作占位符，无实际逻辑


---

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
    # 鼠标释放事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        pass
```
        # 空操作占位符，无实际逻辑


---

```python
    def draw_preview(self, painter: QPainter):
```
    # 绘制预览，接收自身引用、绘图引擎：绘图引擎，无返回值

---

```python
        pass  # AI 的删除锚点工具在悬停时显示 - 图标，这里简化处理
```
        # 空操作占位符：AI 的删除锚点工具在悬停时显示 - 图标，这里简化处理


---

```python
    def cancel(self):
```
    # 取消当前操作，接收自身引用，无返回值

---

```python
        self._selected_anchor_idx = -1
```
        # 当前选中的锚点索引

---

```python
        self._dragging_item = None
```
        # 正在拖拽的图形项

---

```python
        super().cancel()
```
        # super().cancel()



---

```python
# ── 转换锚点工具 (Convert Anchor Point Tool, Shift+C) ─────────
```
# 注释：── 转换锚点工具 (Convert Anchor Point Tool, Shift+C) ─────────


---

```python
class ConvertAnchorPointTool(BaseTool):
```
# 定义转换锚点工具类，切换锚点类型或拖拽拉出手柄，继承自(BaseTool)

---

```python
    """转换锚点工具 —— 切换锚点类型 / 拖拽拉出手柄
```
    # """转换锚点工具 —— 切换锚点类型 / 拖拽拉出手柄

---

```python
    
```
    # 文档字符串空行

---

```python
    对照 AI 行为：
```
    # 文档内容：对照 AI 行为：

---

```python
    - 点击平滑点 → 转为角点（移除手柄）
```
    # 文档内容：- 点击平滑点 → 转为角点（移除手柄）

---

```python
    - 点击角点并拖拽 → 拉出手柄转为平滑点
```
    # 文档内容：- 点击角点并拖拽 → 拉出手柄转为平滑点

---

```python
    - 拖拽手柄 → 断开对称约束
```
    # 文档内容：- 拖拽手柄 → 断开对称约束

---

```python
    """
```
    # 文档字符串结束标记

---

```python
    __slots__ = (
```
    # 声明实例属性槽位：(，用于节省内存并提升访问速度

---

```python
        '_drag_start', '_dragging_item', '_dragging_anchor_idx',
```
        # 函数参数续行：'_drag_start', '_dragging_item', '_dragging_anchor_idx'

---

```python
        '_is_dragging', '_old_anchors',
```
        # 函数参数续行：'_is_dragging', '_old_anchors'

---

```python
    )
```
    # )


---

```python
    ANCHOR_TOLERANCE = 5.0
```
    # 类属性：锚点点击容差（100%缩放下的像素值）

---

```python
    DRAG_THRESHOLD = 3.0
```
    # 类属性：最小拖拽阈值（像素）


---

```python
    def __init__(self):
```
    # 构造函数，接收自身引用，无返回值

---

```python
        super().__init__(ToolType.CONVERT_ANCHOR)
```
        # 调用父类构造函数，传入ToolType.CONVERT_ANCHOR

---

```python
        self._drag_start: QPointF | None = None
```
        # 拖拽起始位置

---

```python
        self._dragging_item: GraphicItem | None = None
```
        # 正在拖拽的图形项

---

```python
        self._dragging_anchor_idx: int = -1
```
        # 正在拖拽的锚点索引

---

```python
        self._is_dragging: bool = False
```
        # 将bool = False赋值给self._is_dragging

---

```python
        self._old_anchors: list[AnchorPoint] = []
```
        # 操作前的锚点状态快照（用于撤销）


---

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
    # 鼠标按下事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        self._drag_start = QPointF(pos)
```
        # 拖拽起始位置

---

```python
        self._is_dragging = False
```
        # 将False赋值给self._is_dragging

---

```python
        
```
        # 

---

```python
        for layer in reversed(self._document.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in layer.items:
```
            # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
```
                # 如果not isinstance(item, PathItem) or not item.selected or not item.anchors（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
```
                # inv, ok = DirectSelectTool._safe_inverted(item._transform)

---

```python
                if not ok:
```
                # 如果not ok（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                local_pos = inv.map(pos)
```
                # 将inv.map(pos)赋值给local_pos

---

```python
                idx = item.get_anchor_at(
```
                # 将item.get_anchor_at(赋值给idx

---

```python
                    local_pos.x(), local_pos.y(),
```
                    # 函数参数续行：local_pos.x(), local_pos.y()

---

```python
                    tolerance=self.ANCHOR_TOLERANCE,
```
                    # 将self.ANCHOR_TOLERANCE,赋值给tolerance

---

```python
                )
```
                # )

---

```python
                if idx >= 0:
```
                # 如果idx >= 0（满足条件时执行）

---

```python
                    self._dragging_item = item
```
                    # 正在拖拽的图形项

---

```python
                    self._dragging_anchor_idx = idx
```
                    # 正在拖拽的锚点索引

---

```python
                    self._old_anchors = [a.copy() for a in item.anchors]
```
                    # 操作前的锚点状态快照（用于撤销）

---

```python
                    return
```
                    # 空返回，结束函数执行


---

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
    # 鼠标移动事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._dragging_item or self._dragging_anchor_idx < 0:
```
        # 如果not self._dragging_item or self._dragging_anchor_idx < 0（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        if self._drag_start is None:
```
        # 如果拖拽起始位置为空（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        
```
        # 

---

```python
        dx = pos.x() - self._drag_start.x()
```
        # 将pos.x() - self._drag_start.x()赋值给dx

---

```python
        dy = pos.y() - self._drag_start.y()
```
        # 将pos.y() - self._drag_start.y()赋值给dy

---

```python
        dist = math.sqrt(dx*dx + dy*dy)
```
        # 将math.sqrt(dx*dx + dy*dy)赋值给dist

---

```python
        
```
        # 

---

```python
        if not self._is_dragging:
```
        # 如果not self._is_dragging（满足条件时执行）

---

```python
            if dist < self.DRAG_THRESHOLD:
```
            # 如果dist < self.DRAG_THRESHOLD（满足条件时执行）

---

```python
                return
```
                # 空返回，结束函数执行

---

```python
            self._is_dragging = True
```
            # 将True赋值给self._is_dragging

---

```python
        
```
        # 

---

```python
        # 拖拽：从锚点拉出手柄
```
        # 注释：拖拽：从锚点拉出手柄

---

```python
        if isinstance(self._dragging_item, PathItem):
```
        # 如果isinstance(self._dragging_item, PathItem)（满足条件时执行）

---

```python
            inv, ok = DirectSelectTool._safe_inverted(self._dragging_item._transform)
```
            # 函数参数续行：inv, ok = DirectSelectTool._safe_inverted(self._dragging_item._transform)

---

```python
            if not ok:
```
            # 如果not ok（满足条件时执行）

---

```python
                return
```
                # 空返回，结束函数执行

---

```python
            local_pos = inv.map(pos)
```
            # 将inv.map(pos)赋值给local_pos

---

```python
            anchor = self._dragging_item.anchors[self._dragging_anchor_idx]
```
            # 将self._dragging_item.anchors[self._dragging_anchor_idx]赋值给anchor

---

```python
            
```
            # 

---

```python
            rel_x = local_pos.x() - anchor.x
```
            # 将local_pos.x() - anchor.x赋值给rel_x

---

```python
            rel_y = local_pos.y() - anchor.y
```
            # 将local_pos.y() - anchor.y赋值给rel_y

---

```python
            
```
            # 

---

```python
            # 拉出双向对称手柄（平滑点）
```
            # 注释：拉出双向对称手柄（平滑点）

---

```python
            anchor.handle_out = QPointF(rel_x, rel_y)
```
            # 将QPointF(rel_x, rel_y)赋值给anchor.handle_out

---

```python
            anchor.handle_in = QPointF(-rel_x, -rel_y)
```
            # 将QPointF(-rel_x, -rel_y)赋值给anchor.handle_in

---

```python
            anchor.anchor_type = AnchorPointType.SMOOTH
```
            # 将AnchorPointType.SMOOTH赋值给anchor.anchor_type

---

```python
            
```
            # 

---

```python
            self._dragging_item._build_path()
```
            # 调用self._dragging_item的重建贝塞尔路径方法

---

```python
            if self._document:
```
            # 如果self._document（满足条件时执行）

---

```python
                self._document.modified = True
```
                # 将True赋值给self._document.modified


---

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
    # 鼠标释放事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._dragging_item or self._dragging_anchor_idx < 0:
```
        # 如果not self._dragging_item or self._dragging_anchor_idx < 0（满足条件时执行）

---

```python
            self._drag_start = None
```
            # 拖拽起始位置

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        
```
        # 

---

```python
        if isinstance(self._dragging_item, PathItem):
```
        # 如果isinstance(self._dragging_item, PathItem)（满足条件时执行）

---

```python
            anchor = self._dragging_item.anchors[self._dragging_anchor_idx]
```
            # 将self._dragging_item.anchors[self._dragging_anchor_idx]赋值给anchor

---

```python
            
```
            # 

---

```python
            if not self._is_dragging:
```
            # 如果not self._is_dragging（满足条件时执行）

---

```python
                # 点击（未拖拽）：切换锚点类型
```
                # 注释：点击（未拖拽）：切换锚点类型

---

```python
                if anchor.has_handles:
```
                # 如果anchor.has_handles（满足条件时执行）

---

```python
                    # 有手柄 → 转为角点（移除手柄）
```
                    # 注释：有手柄 → 转为角点（移除手柄）

---

```python
                    anchor.remove_handles()
```
                    # 调用anchor的移除手柄方法

---

```python
                # 无手柄的角点 → 点击不产生变化（AI 行为）
```
                # 注释：无手柄的角点 → 点击不产生变化（AI 行为）

---

```python
                self._dragging_item._build_path()
```
                # 调用self._dragging_item的重建贝塞尔路径方法

---

```python
            
```
            # 

---

```python
            # 记录撤销命令（通过 execute_command 统一入口）
```
            # 注释：记录撤销命令（通过 execute_command 统一入口）

---

```python
            if self._document and self._old_anchors:
```
            # 如果self._document and self._old_anchors（满足条件时执行）

---

```python
                new_anchors = [a.copy() for a in self._dragging_item.anchors]
```
                # 将[a.copy() for a in self._dragging_item.anchors]赋值给new_anchors

---

```python
                cmd = ModifyAnchorCommand(
```
                # 将ModifyAnchorCommand(赋值给cmd

---

```python
                    self._document, self._dragging_item,
```
                    # 函数参数续行：self._document, self._dragging_item

---

```python
                    self._old_anchors, new_anchors,
```
                    # 函数参数续行：self._old_anchors, new_anchors

---

```python
                )
```
                # )

---

```python
                self._document.execute_command(cmd)
```
                # 调用self._document的执行命令（支持撤销）方法

---

```python
        
```
        # 

---

```python
        self._drag_start = None
```
        # 拖拽起始位置

---

```python
        self._dragging_item = None
```
        # 正在拖拽的图形项

---

```python
        self._dragging_anchor_idx = -1
```
        # 正在拖拽的锚点索引

---

```python
        self._is_dragging = False
```
        # 将False赋值给self._is_dragging

---

```python
        self._old_anchors = []
```
        # 操作前的锚点状态快照（用于撤销）


---

```python
    def draw_preview(self, painter: QPainter):
```
    # 绘制预览，接收自身引用、绘图引擎：绘图引擎，无返回值

---

```python
        """拖拽时显示预览手柄线"""
```
        # 单行文档字符串：拖拽时显示预览手柄线

---

```python
        if self._is_dragging and self._dragging_item and self._dragging_anchor_idx >= 0:
```
        # 如果self._is_dragging and self._dragging_item and self._dragging_anchor_idx >= 0（满足条件时执行）

---

```python
            if isinstance(self._dragging_item, PathItem):
```
            # 如果isinstance(self._dragging_item, PathItem)（满足条件时执行）

---

```python
                DirectSelectTool._draw_single_anchor(
```
                # 调用DirectSelectTool的_draw_single_anchor方法（续行参数）

---

```python
                    painter, self._dragging_item, self._dragging_anchor_idx, True
```
                    # 函数参数续行：painter, self._dragging_item, self._dragging_anchor_idx, True

---

```python
                )
```
                # )


---

```python
    def cancel(self):
```
    # 取消当前操作，接收自身引用，无返回值

---

```python
        self._dragging_item = None
```
        # 正在拖拽的图形项

---

```python
        self._dragging_anchor_idx = -1
```
        # 正在拖拽的锚点索引

---

```python
        self._is_dragging = False
```
        # 将False赋值给self._is_dragging

---

```python
        super().cancel()
```
        # super().cancel()



---

```python
# ── 钢笔工具 ──────────────────────────────────────────────
```
# 注释：── 钢笔工具 ──────────────────────────────────────────────


---

```python
class PenTool(BaseTool):
```
# 定义钢笔工具类，对照Adobe Illustrator行为复原，支持创建角点/平滑点/闭合路径，继承自(BaseTool)

---

```python
    """钢笔工具 —— Adobe Illustrator 1:1 复原
```
    # """钢笔工具 —— Adobe Illustrator 1:1 复原

---

```python
    
```
    # 文档字符串空行

---

```python
    功能对照：
```
    # 文档内容：功能对照：

---

```python
    - 单击 = 创建角点（Corner Point），无手柄
```
    # 文档内容：- 单击 = 创建角点（Corner Point），无手柄

---

```python
    - 单击并拖动 = 创建平滑点（Smooth Point），拉出对称手柄
```
    # 文档内容：- 单击并拖动 = 创建平滑点（Smooth Point），拉出对称手柄

---

```python
    - 点击起始锚点 = 闭合路径（光标出现圆圈 ○）
```
    # 文档内容：- 点击起始锚点 = 闭合路径（光标出现圆圈 ○）

---

```python
    - Enter/Return = 结束路径
```
    # 文档内容：- Enter/Return = 结束路径

---

```python
    - Escape = 取消路径
```
    # 文档内容：- Escape = 取消路径

---

```python
    
```
    # 文档字符串空行

---

```python
    隐藏功能：
```
    # 文档内容：隐藏功能：

---

```python
    - Alt/Option 拖拽 = 调整单侧方向线（断开对称）
```
    # 文档内容：- Alt/Option 拖拽 = 调整单侧方向线（断开对称）

---

```python
    - Ctrl/Cmd = 临时切换直接选择工具调整锚点
```
    # 文档内容：- Ctrl/Cmd = 临时切换直接选择工具调整锚点

---

```python
    - Space = 在拖动过程中临时移动当前锚点位置
```
    # 文档内容：- Space = 在拖动过程中临时移动当前锚点位置

---

```python
    - Shift = 约束角度（45度增量）
```
    # 文档内容：- Shift = 约束角度（45度增量）

---

```python
    
```
    # 文档字符串空行

---

```python
    光标状态：
```
    # 文档内容：光标状态：

---

```python
    - 默认 = Pen（十字光标）
```
    # 文档内容：- 默认 = Pen（十字光标）

---

```python
    - 悬停已有锚点 = Pen-（删除锚点）
```
    # 文档内容：- 悬停已有锚点 = Pen-（删除锚点）

---

```python
    - 悬停已有路径段 = Pen+（添加锚点）
```
    # 文档内容：- 悬停已有路径段 = Pen+（添加锚点）

---

```python
    - 悬停起始锚点 = Pen○（闭合路径）
```
    # 文档内容：- 悬停起始锚点 = Pen○（闭合路径）

---

```python
    - 悬停端点 = Pen/（继续路径）
```
    # 文档内容：- 悬停端点 = Pen/（继续路径）

---

```python
    """
```
    # 文档字符串结束标记

---

```python
    
```
    # 

---

```python
    DRAG_THRESHOLD = 3  # 拖拽阈值（像素），小于此值视为单击
```
    # 类属性：最小拖拽阈值（像素）

---

```python
    CLOSE_TOLERANCE = 8  # 闭合路径检测容差
```
    # 类属性：闭合路径检测容差

---

```python
    HANDLE_TOLERANCE = 5  # 手柄命中容差
```
    # 类属性：手柄点击容差（100%缩放下的像素值）

---

```python
    ANCHOR_TOLERANCE = 6  # 锚点命中容差
```
    # 类属性：锚点点击容差（100%缩放下的像素值）

---

```python
    SEGMENT_TOLERANCE = 5  # 路径段命中容差
```
    # 类属性：路径段点击容差（100%缩放下的像素值）

---

```python
    SHIFT_ANGLE_STEP = 45  # Shift约束角度步长（度）
```
    # 类属性：Shift约束角度步长（度）


---

```python
    __slots__ = (
```
    # 声明实例属性槽位：(，用于节省内存并提升访问速度

---

```python
        '_current_path', '_drawing', '_hover_state',
```
        # '_current_path', '_drawing', '_hover_state'

---

```python
        '_drag_start_pos', '_is_dragging_handle',
```
        # '_drag_start_pos', '_is_dragging_handle'

---

```python
        '_dragged_anchor_idx', '_dragged_handle_side',
```
        # 函数参数续行：'_dragged_anchor_idx', '_dragged_handle_side'

---

```python
        '_alt_adjusting', '_space_moving', '_space_start_pos',
```
        # '_alt_adjusting', '_space_moving', '_space_start_pos'

---

```python
        '_ctrl_temp_select', '_ctrl_drag_start',
```
        # '_ctrl_temp_select', '_ctrl_drag_start'

---

```python
    )
```
    # )


---

```python
    # ── 钢笔光标状态枚举 ──
```
    # 注释：── 钢笔光标状态枚举 ──

---

```python
    PEN_DEFAULT = 0        # 默认钢笔
```
    # 类属性：默认钢笔光标状态常量（值为0）

---

```python
    PEN_PLUS = 1           # Pen+  添加锚点
```
    # 类属性：Pen+添加锚点光标状态常量（值为1）

---

```python
    PEN_MINUS = 2          # Pen-  删除锚点
```
    # 类属性：Pen-删除锚点光标状态常量（值为2）

---

```python
    PEN_CLOSE = 3          # Pen○  闭合路径
```
    # 类属性：Pen○闭合路径光标状态常量（值为3）

---

```python
    PEN_CONTINUE = 4       # Pen/  继续路径
```
    # 类属性：Pen/继续路径光标状态常量（值为4）


---

```python
    def __init__(self):
```
    # 构造函数，接收自身引用，无返回值

---

```python
        super().__init__(ToolType.PEN)
```
        # 调用父类构造函数，传入ToolType.PEN

---

```python
        self._current_path: PathItem | None = None
```
        # 当前正在绘制的路径项

---

```python
        self._drawing: bool = False          # 正在拖拽中（创建平滑点）
```
        # 是否正在拖拽中

---

```python
        self._hover_state: int = PenTool.PEN_DEFAULT
```
        # 悬停光标状态

---

```python
        
```
        # 

---

```python
        # 拖拽状态
```
        # 注释：拖拽状态

---

```python
        self._drag_start_pos: QPointF | None = None
```
        # 拖拽起始位置

---

```python
        self._is_dragging_handle: bool = False
```
        # 是否正在拖拽手柄

---

```python
        self._dragged_anchor_idx: int = -1
```
        # 被拖拽的锚点索引

---

```python
        self._dragged_handle_side: str = ''
```
        # 被拖拽的手柄侧

---

```python
        
```
        # 

---

```python
        # 隐藏功能状态
```
        # 注释：隐藏功能状态

---

```python
        self._alt_adjusting: bool = False     # Alt 调整单侧方向线
```
        # Alt键调整单侧方向线标志

---

```python
        self._space_moving: bool = False       # Space 移动当前锚点
```
        # Space键移动当前锚点标志

---

```python
        self._space_start_pos: QPointF | None = None
```
        # Space移动起始位置

---

```python
        self._ctrl_temp_select: bool = False   # Ctrl 临时直接选择
```
        # Ctrl临时切换直接选择工具标志

---

```python
        self._ctrl_drag_start: QPointF | None = None
```
        # Ctrl拖拽起始位置


---

```python
    # ── 辅助方法 ──
```
    # 注释：── 辅助方法 ──


---

```python
    def _snap_angle(self, dx: float, dy: float) -> tuple[float, float]:
```
    # Shift约束角度到最近的45度增量，接收自身引用、X方向偏移量：浮点数、Y方向偏移量：浮点数，返回tuple[float, float]

---

```python
        """Shift约束角度到最近的45度增量"""
```
        # 单行文档字符串：Shift约束角度到最近的45度增量

---

```python
        angle = math.atan2(dy, dx)
```
        # 将math.atan2(dy, dx)赋值给angle

---

```python
        step_rad = math.radians(PenTool.SHIFT_ANGLE_STEP)
```
        # 将math.radians(PenTool.SHIFT_ANGLE_STEP)赋值给step_rad

---

```python
        snapped = round(angle / step_rad) * step_rad
```
        # 将round(angle / step_rad) * step_rad赋值给snapped

---

```python
        length = math.sqrt(dx*dx + dy*dy)
```
        # 将math.sqrt(dx*dx + dy*dy)赋值给length

---

```python
        return (math.cos(snapped) * length, math.sin(snapped) * length)
```
        # 返回(math.cos(snapped) * length, math.sin(snapped) * length)


---

```python
    def _detect_hover_state(self, pos: QPointF, doc) -> int:
```
    # 检测悬停位置并返回钢笔光标状态，接收自身引用、鼠标位置坐标：二维浮点坐标、文档对象，返回整数

---

```python
        """检测悬停位置，返回钢笔光标状态"""
```
        # 单行文档字符串：检测悬停位置，返回钢笔光标状态

---

```python
        # 遍历所有可见图层的路径项
```
        # 注释：遍历所有可见图层的路径项

---

```python
        for layer in reversed(doc.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in layer.items:
```
            # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or not item.visible or item.locked:
```
                # 如果not isinstance(item, PathItem) or not item.visible or item.locked（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                
```
                # 

---

```python
                # 1) 检测锚点 → Pen-
```
                # 注释：1) 检测锚点 → Pen-

---

```python
                anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
```
                # 将item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)赋值给anchor_idx

---

```python
                if anchor_idx >= 0:
```
                # 如果anchor_idx >= 0（满足条件时执行）

---

```python
                    # 如果是当前正在绘制的路径的锚点，继续判断
```
                    # 注释：如果是当前正在绘制的路径的锚点，继续判断

---

```python
                    if item is self._current_path:
```
                    # 如果item is self._current_path（满足条件时执行）

---

```python
                        # 起始锚点 → Pen○ 闭合
```
                        # 注释：起始锚点 → Pen○ 闭合

---

```python
                        if anchor_idx == 0 and len(item.anchors) >= 2:
```
                        # 如果anchor_idx == 0 and len(item.anchors) >= 2（满足条件时执行）

---

```python
                            return PenTool.PEN_CLOSE
```
                            # 返回PenTool.PEN_CLOSE

---

```python
                        # 端点 → Pen/ 继续
```
                        # 注释：端点 → Pen/ 继续

---

```python
                        if anchor_idx == len(item.anchors) - 1:
```
                        # 如果anchor_idx == len(item.anchors) - 1（满足条件时执行）

---

```python
                            return PenTool.PEN_CONTINUE
```
                            # 返回PenTool.PEN_CONTINUE

---

```python
                    return PenTool.PEN_MINUS
```
                    # 返回PenTool.PEN_MINUS

---

```python
                
```
                # 

---

```python
                # 2) 检测路径段 → Pen+
```
                # 注释：2) 检测路径段 → Pen+

---

```python
                seg_idx = item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)
```
                # 将item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)赋值给seg_idx

---

```python
                if seg_idx >= 0:
```
                # 如果seg_idx >= 0（满足条件时执行）

---

```python
                    return PenTool.PEN_PLUS
```
                    # 返回PenTool.PEN_PLUS

---

```python
        
```
        # 

---

```python
        # 3) 如果当前有路径且接近起始点 → Pen○
```
        # 注释：3) 如果当前有路径且接近起始点 → Pen○

---

```python
        if self._current_path and len(self._current_path.anchors) >= 2:
```
        # 如果self._current_path and len(self._current_path.anchors) >= 2（满足条件时执行）

---

```python
            first = self._current_path.anchors[0]
```
            # 将self._current_path.anchors[0]赋值给first

---

```python
            dist = math.sqrt((pos.x() - first.x)**2 + (pos.y() - first.y)**2)
```
            # 将math.sqrt((pos.x() - first.x)**2 + (pos.y() - first.y)**2)赋值给dist

---

```python
            if dist < PenTool.CLOSE_TOLERANCE:
```
            # 如果dist < PenTool.CLOSE_TOLERANCE（满足条件时执行）

---

```python
                return PenTool.PEN_CLOSE
```
                # 返回PenTool.PEN_CLOSE

---

```python
        
```
        # 

---

```python
        return PenTool.PEN_DEFAULT
```
        # 返回PenTool.PEN_DEFAULT


---

```python
    # ── 鼠标事件 ──
```
    # 注释：── 鼠标事件 ──


---

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
    # 鼠标按下事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        doc = self._document
```
        # 将self._document赋值给doc

---

```python
        is_alt = bool(modifiers & Qt.AltModifier)
```
        # 将bool(modifiers & Qt.AltModifier)赋值给is_alt

---

```python
        is_ctrl = bool(modifiers & Qt.ControlModifier)
```
        # 将bool(modifiers & Qt.ControlModifier)赋值给is_ctrl

---

```python
        is_shift = bool(modifiers & Qt.ShiftModifier)
```
        # 将bool(modifiers & Qt.ShiftModifier)赋值给is_shift


---

```python
        # ── Ctrl/Cmd 临时切换直接选择工具 ──
```
        # 注释：── Ctrl/Cmd 临时切换直接选择工具 ──

---

```python
        if is_ctrl:
```
        # 如果is_ctrl（满足条件时执行）

---

```python
            self._ctrl_temp_select = True
```
            # Ctrl临时切换直接选择工具标志

---

```python
            self._ctrl_drag_start = QPointF(pos)
```
            # Ctrl拖拽起始位置

---

```python
            # 查找点击位置的路径项和锚点
```
            # 注释：查找点击位置的路径项和锚点

---

```python
            for layer in reversed(doc.layers):
```
            # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
                if not layer.visible or layer.locked:
```
                # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                for item in layer.items:
```
                # 遍历图层中的所有图形项，每次迭代将当前元素赋给item

---

```python
                    if not isinstance(item, PathItem) or not item.visible or item.locked:
```
                    # 如果not isinstance(item, PathItem) or not item.visible or item.locked（满足条件时执行）

---

```python
                        continue
```
                        # 跳过当前迭代，继续下一次循环

---

```python
                    anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
```
                    # 将item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)赋值给anchor_idx

---

```python
                    if anchor_idx >= 0:
```
                    # 如果anchor_idx >= 0（满足条件时执行）

---

```python
                        self._dragged_anchor_idx = anchor_idx
```
                        # 被拖拽的锚点索引

---

```python
                        # 临时将该路径设为当前编辑路径
```
                        # 注释：临时将该路径设为当前编辑路径

---

```python
                        self._current_path = item
```
                        # 当前正在绘制的路径项

---

```python
                        return
```
                        # 空返回，结束函数执行

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # ── 检测悬停状态决定行为 ──
```
        # 注释：── 检测悬停状态决定行为 ──

---

```python
        hover = self._detect_hover_state(pos, doc)
```
        # 将self._detect_hover_state(pos, doc)赋值给hover


---

```python
        # 悬停已有路径的锚点（非当前路径） → 删除锚点（Pen-）
```
        # 注释：悬停已有路径的锚点（非当前路径） → 删除锚点（Pen-）

---

```python
        if hover == PenTool.PEN_MINUS:
```
        # 如果hover == PenTool.PEN_MINUS（满足条件时执行）

---

```python
            self._try_delete_anchor(pos, doc)
```
            # 调用self的_try_delete_anchor方法

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # 悬停已有路径段 → 添加锚点（Pen+）
```
        # 注释：悬停已有路径段 → 添加锚点（Pen+）

---

```python
        if hover == PenTool.PEN_PLUS:
```
        # 如果hover == PenTool.PEN_PLUS（满足条件时执行）

---

```python
            self._try_add_anchor(pos, doc)
```
            # 调用self的_try_add_anchor方法

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # 悬停当前路径起始锚点 → 闭合路径（Pen○）
```
        # 注释：悬停当前路径起始锚点 → 闭合路径（Pen○）

---

```python
        if hover == PenTool.PEN_CLOSE and self._current_path:
```
        # 如果hover == PenTool.PEN_CLOSE and self._current_path（满足条件时执行）

---

```python
            self._close_path()
```
            # 调用self的_close_path方法

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # ── 正常绘制模式 ──
```
        # 注释：── 正常绘制模式 ──

---

```python
        # 如果没有当前路径，创建新路径
```
        # 注释：如果没有当前路径，创建新路径

---

```python
        if self._current_path is None:
```
        # 如果self._current_path is None（满足条件时执行）

---

```python
            self._current_path = PathItem()
```
            # 当前正在绘制的路径项

---

```python
            self._current_path.style.fill_color = QColor(200, 200, 200, 100)
```
            # 将QColor(200, 200, 200, 100)赋值给self._current_path.style.fill_color

---

```python
            self._current_path.style.stroke_color = QColor(50, 50, 50)
```
            # 将QColor(50, 50, 50)赋值给self._current_path.style.stroke_color

---

```python
            self._current_path.style.stroke_width = 2.0
```
            # 将2.0赋值给self._current_path.style.stroke_width

---

```python
            doc.add_item(self._current_path)
```
            # 调用doc的添加图形项方法


---

```python
        # 记录拖拽起始位置
```
        # 注释：记录拖拽起始位置

---

```python
        self._drag_start_pos = QPointF(pos)
```
        # 拖拽起始位置

---

```python
        self._drawing = True
```
        # 是否正在拖拽中


---

```python
    def mouse_move(self, pos: QPointF, modifiers: int):
```
    # 鼠标移动事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        is_alt = bool(modifiers & Qt.AltModifier)
```
        # 将bool(modifiers & Qt.AltModifier)赋值给is_alt

---

```python
        is_ctrl = bool(modifiers & Qt.ControlModifier)
```
        # 将bool(modifiers & Qt.ControlModifier)赋值给is_ctrl

---

```python
        is_shift = bool(modifiers & Qt.ShiftModifier)
```
        # 将bool(modifiers & Qt.ShiftModifier)赋值给is_shift

---

```python
        is_space = bool(modifiers & Qt.Key_Space if hasattr(Qt, 'Key_Space') else False)
```
        # 条件赋值：如果hasattr(Qt, 'Key_Space')则将is_space设为bool(modifiers & Qt.Key_Space，否则设为False)


---

```python
        # ── Ctrl 临时直接选择：移动锚点 ──
```
        # 注释：── Ctrl 临时直接选择：移动锚点 ──

---

```python
        if self._ctrl_temp_select and self._current_path and self._ctrl_drag_start:
```
        # 如果self._ctrl_temp_select and self._current_path and self._ctrl_drag_start（满足条件时执行）

---

```python
            dx = pos.x() - self._ctrl_drag_start.x()
```
            # 将pos.x() - self._ctrl_drag_start.x()赋值给dx

---

```python
            dy = pos.y() - self._ctrl_drag_start.y()
```
            # 将pos.y() - self._ctrl_drag_start.y()赋值给dy

---

```python
            if self._dragged_anchor_idx >= 0 and self._dragged_anchor_idx < self._current_path.anchor_count:
```
            # 如果self._dragged_anchor_idx >= 0 and self._dragged_anchor_idx < self._current_path.anchor_count（满足条件时执行）

---

```python
                self._current_path.move_anchor(
```
                # 调用self._current_path的move_anchor方法（续行参数）

---

```python
                    self._dragged_anchor_idx,
```
                    # 函数参数：self._dragged_anchor_idx

---

```python
                    self._current_path.anchors[self._dragged_anchor_idx].x + dx,
```
                    # 函数参数续行：self._current_path.anchors[self._dragged_anchor_idx].x + dx

---

```python
                    self._current_path.anchors[self._dragged_anchor_idx].y + dy,
```
                    # 函数参数续行：self._current_path.anchors[self._dragged_anchor_idx].y + dy

---

```python
                )
```
                # )

---

```python
            self._ctrl_drag_start = QPointF(pos)
```
            # Ctrl拖拽起始位置

---

```python
            self._document.modified = True
```
            # 将True赋值给self._document.modified

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # ── Space 移动当前锚点（仅在拖拽中） ──
```
        # 注释：── Space 移动当前锚点（仅在拖拽中） ──

---

```python
        if self._space_moving and self._current_path and self._space_start_pos:
```
        # 如果self._space_moving and self._current_path and self._space_start_pos（满足条件时执行）

---

```python
            dx = pos.x() - self._space_start_pos.x()
```
            # 将pos.x() - self._space_start_pos.x()赋值给dx

---

```python
            dy = pos.y() - self._space_start_pos.y()
```
            # 将pos.y() - self._space_start_pos.y()赋值给dy

---

```python
            last_idx = self._current_path.anchor_count - 1
```
            # 将self._current_path.anchor_count - 1赋值给last_idx

---

```python
            if last_idx >= 0:
```
            # 如果last_idx >= 0（满足条件时执行）

---

```python
                anchor = self._current_path.anchors[last_idx]
```
                # 将self._current_path.anchors[last_idx]赋值给anchor

---

```python
                self._current_path.move_anchor(last_idx, anchor.x + dx, anchor.y + dy)
```
                # 调用self._current_path的移动锚点方法

---

```python
            self._space_start_pos = QPointF(pos)
```
            # Space移动起始位置

---

```python
            self._document.modified = True
```
            # 将True赋值给self._document.modified

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # ── 更新悬停光标状态 ──
```
        # 注释：── 更新悬停光标状态 ──

---

```python
        if not self._drawing:
```
        # 如果not self._drawing（满足条件时执行）

---

```python
            self._hover_state = self._detect_hover_state(pos, self._document)
```
            # 悬停光标状态

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # ── 拖拽中：实时更新最后一个锚点的手柄 ──
```
        # 注释：── 拖拽中：实时更新最后一个锚点的手柄 ──

---

```python
        if self._drawing and self._drag_start_pos and self._current_path:
```
        # 如果self._drawing and self._drag_start_pos and self._current_path（满足条件时执行）

---

```python
            last_idx = self._current_path.anchor_count - 1
```
            # 将self._current_path.anchor_count - 1赋值给last_idx

---

```python
            if last_idx >= 0:
```
            # 如果last_idx >= 0（满足条件时执行）

---

```python
                dx = pos.x() - self._drag_start_pos.x()
```
                # 将pos.x() - self._drag_start_pos.x()赋值给dx

---

```python
                dy = pos.y() - self._drag_start_pos.y()
```
                # 将pos.y() - self._drag_start_pos.y()赋值给dy

---

```python
                
```
                # 

---

```python
                # Shift 约束角度
```
                # 注释：Shift 约束角度

---

```python
                if is_shift and (dx != 0 or dy != 0):
```
                # 如果is_shift and (dx != 0 or dy != 0)（满足条件时执行）

---

```python
                    dx, dy = self._snap_angle(dx, dy)
```
                    # 函数参数续行：dx, dy = self._snap_angle(dx, dy)

---

```python
                
```
                # 

---

```python
                # 拖拽距离小于阈值：视为角点（无手柄）
```
                # 注释：拖拽距离小于阈值：视为角点（无手柄）

---

```python
                dist = math.sqrt(dx*dx + dy*dy)
```
                # 将math.sqrt(dx*dx + dy*dy)赋值给dist

---

```python
                if dist < PenTool.DRAG_THRESHOLD:
```
                # 如果dist < PenTool.DRAG_THRESHOLD（满足条件时执行）

---

```python
                    self._current_path.remove_handles(last_idx)
```
                    # 调用self._current_path的移除手柄方法

---

```python
                else:
```
                # 否则（不满足上述条件时执行）

---

```python
                    # 创建/更新手柄（平滑点）
```
                    # 注释：创建/更新手柄（平滑点）

---

```python
                    if is_alt:
```
                    # 如果is_alt（满足条件时执行）

---

```python
                        # Alt 键：仅设置 handle_out（单侧控制），handle_in 置空
```
                        # 注释：Alt 键：仅设置 handle_out（单侧控制），handle_in 置空

---

```python
                        anchor = self._current_path.anchors[last_idx]
```
                        # 将self._current_path.anchors[last_idx]赋值给anchor

---

```python
                        anchor.handle_out = QPointF(dx, dy)
```
                        # 将QPointF(dx, dy)赋值给anchor.handle_out

---

```python
                        anchor.handle_in = None
```
                        # 将None赋值给anchor.handle_in

---

```python
                        anchor.anchor_type = AnchorPointType.CORNER
```
                        # 将AnchorPointType.CORNER赋值给anchor.anchor_type

---

```python
                        self._current_path._build_path()
```
                        # 调用self._current_path的重建贝塞尔路径方法

---

```python
                    else:
```
                    # 否则（不满足上述条件时执行）

---

```python
                        # 正常拖拽：创建对称平滑点
```
                        # 注释：正常拖拽：创建对称平滑点

---

```python
                        self._current_path.set_handle_out(
```
                        # 调用self._current_path的set_handle_out方法（续行参数）

---

```python
                            last_idx, dx, dy, constrain_smooth=True
```
                            # 函数参数续行：last_idx, dx, dy, constrain_smooth=True

---

```python
                        )
```
                        # )

---

```python
                
```
                # 

---

```python
                self._document.modified = True
```
                # 将True赋值给self._document.modified


---

```python
    def mouse_release(self, pos: QPointF, modifiers: int):
```
    # 鼠标释放事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # ── Ctrl 临时直接选择：释放 ──
```
        # 注释：── Ctrl 临时直接选择：释放 ──

---

```python
        if self._ctrl_temp_select:
```
        # 如果self._ctrl_temp_select（满足条件时执行）

---

```python
            self._ctrl_temp_select = False
```
            # Ctrl临时切换直接选择工具标志

---

```python
            self._ctrl_drag_start = None
```
            # Ctrl拖拽起始位置

---

```python
            self._dragged_anchor_idx = -1
```
            # 被拖拽的锚点索引

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        # ── Space 移动锚点：释放 ──
```
        # 注释：── Space 移动锚点：释放 ──

---

```python
        if self._space_moving:
```
        # 如果self._space_moving（满足条件时执行）

---

```python
            self._space_moving = False
```
            # Space键移动当前锚点标志

---

```python
            self._space_start_pos = None
```
            # Space移动起始位置

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        if not self._drawing or self._drag_start_pos is None:
```
        # 如果not self._drawing or self._drag_start_pos is None（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        is_alt = bool(modifiers & Qt.AltModifier)
```
        # 将bool(modifiers & Qt.AltModifier)赋值给is_alt

---

```python
        is_shift = bool(modifiers & Qt.ShiftModifier)
```
        # 将bool(modifiers & Qt.ShiftModifier)赋值给is_shift


---

```python
        dx = pos.x() - self._drag_start_pos.x()
```
        # 将pos.x() - self._drag_start_pos.x()赋值给dx

---

```python
        dy = pos.y() - self._drag_start_pos.y()
```
        # 将pos.y() - self._drag_start_pos.y()赋值给dy

---

```python
        
```
        # 

---

```python
        # Shift 约束角度
```
        # 注释：Shift 约束角度

---

```python
        if is_shift and (dx != 0 or dy != 0):
```
        # 如果is_shift and (dx != 0 or dy != 0)（满足条件时执行）

---

```python
            dx, dy = self._snap_angle(dx, dy)
```
            # 函数参数续行：dx, dy = self._snap_angle(dx, dy)

---

```python
        
```
        # 

---

```python
        dist = math.sqrt(dx*dx + dy*dy)
```
        # 将math.sqrt(dx*dx + dy*dy)赋值给dist


---

```python
        if self._current_path is None:
```
        # 如果self._current_path is None（满足条件时执行）

---

```python
            # 不应该到这里
```
            # 注释：不应该到这里

---

```python
            self._drawing = False
```
            # 是否正在拖拽中

---

```python
            self._drag_start_pos = None
```
            # 拖拽起始位置

---

```python
            return
```
            # 空返回，结束函数执行


---

```python
        if dist < PenTool.DRAG_THRESHOLD:
```
        # 如果dist < PenTool.DRAG_THRESHOLD（满足条件时执行）

---

```python
            # ── 短拖拽/单击：创建角点（无手柄） ──
```
            # 注释：── 短拖拽/单击：创建角点（无手柄） ──

---

```python
            anchor = AnchorPoint(pos.x(), pos.y(), anchor_type=AnchorPointType.CORNER)
```
            # 将AnchorPoint(pos.x(), pos.y(), anchor_type=AnchorPointType.CORNER)赋值给anchor

---

```python
            self._current_path.add_anchor(anchor)
```
            # 调用self._current_path的添加锚点方法

---

```python
        else:
```
        # 否则（不满足上述条件时执行）

---

```python
            if is_alt:
```
            # 如果is_alt（满足条件时执行）

---

```python
                # ── Alt+拖拽：创建不对称点（只有 handle_out） ──
```
                # 注释：── Alt+拖拽：创建不对称点（只有 handle_out） ──

---

```python
                anchor = AnchorPoint(
```
                # 将AnchorPoint(赋值给anchor

---

```python
                    self._drag_start_pos.x(), self._drag_start_pos.y(),
```
                    # 函数参数续行：self._drag_start_pos.x(), self._drag_start_pos.y()

---

```python
                    handle_out=QPointF(dx, dy),
```
                    # 将QPointF(dx, dy),赋值给handle_out

---

```python
                    anchor_type=AnchorPointType.CORNER,
```
                    # 将AnchorPointType.CORNER,赋值给anchor_type

---

```python
                )
```
                # )

---

```python
            else:
```
            # 否则（不满足上述条件时执行）

---

```python
                # ── 正常拖拽：创建平滑点（对称手柄） ──
```
                # 注释：── 正常拖拽：创建平滑点（对称手柄） ──

---

```python
                anchor = AnchorPoint(
```
                # 将AnchorPoint(赋值给anchor

---

```python
                    self._drag_start_pos.x(), self._drag_start_pos.y(),
```
                    # 函数参数续行：self._drag_start_pos.x(), self._drag_start_pos.y()

---

```python
                    handle_out=QPointF(dx, dy),
```
                    # 将QPointF(dx, dy),赋值给handle_out

---

```python
                    handle_in=QPointF(-dx, -dy),
```
                    # 将QPointF(-dx, -dy),赋值给handle_in

---

```python
                    anchor_type=AnchorPointType.SMOOTH,
```
                    # 将AnchorPointType.SMOOTH,赋值给anchor_type

---

```python
                )
```
                # )

---

```python
            self._current_path.add_anchor(anchor)
```
            # 调用self._current_path的添加锚点方法

---

```python
        
```
        # 

---

```python
        self._document.modified = True
```
        # 将True赋值给self._document.modified

---

```python
        self._drawing = False
```
        # 是否正在拖拽中

---

```python
        self._drag_start_pos = None
```
        # 拖拽起始位置


---

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
```
    # 鼠标双击事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        """双击结束路径（不闭合）"""
```
        # 单行文档字符串：双击结束路径（不闭合）

---

```python
        if self._current_path:
```
        # 如果self._current_path（满足条件时执行）

---

```python
            self._current_path.closed = False
```
            # 将False赋值给self._current_path.closed

---

```python
            self._current_path._build_path()
```
            # 调用self._current_path的重建贝塞尔路径方法

---

```python
            self._current_path = None
```
            # 当前正在绘制的路径项

---

```python
            self._drawing = False
```
            # 是否正在拖拽中

---

```python
            self._drag_start_pos = None
```
            # 拖拽起始位置


---

```python
    # ── 键盘事件 ──
```
    # 注释：── 键盘事件 ──


---

```python
    def key_press(self, key: int, modifiers: int):
```
    # 键盘按键事件处理，接收自身引用、按键码：整数、修饰键标志位：整数，无返回值

---

```python
        if key == Qt.Key_Escape:
```
        # 如果key == Qt.Key_Escape（满足条件时执行）

---

```python
            # Escape：取消当前路径
```
            # 注释：Escape：取消当前路径

---

```python
            if self._current_path and self._document:
```
            # 如果self._current_path and self._document（满足条件时执行）

---

```python
                self._document.remove_item(self._current_path)
```
                # 调用self._document的移除图形项方法

---

```python
            self._current_path = None
```
            # 当前正在绘制的路径项

---

```python
            self._drawing = False
```
            # 是否正在拖拽中

---

```python
            self._drag_start_pos = None
```
            # 拖拽起始位置

---

```python
            self._hover_state = PenTool.PEN_DEFAULT
```
            # 悬停光标状态

---

```python
        elif key in (Qt.Key_Return, Qt.Key_Enter):
```
        # 如果key in (Qt.Key_Return, Qt.Key_Enter)（满足条件时执行）

---

```python
            # Enter/Return：结束路径（不闭合）
```
            # 注释：Enter/Return：结束路径（不闭合）

---

```python
            if self._current_path:
```
            # 如果self._current_path（满足条件时执行）

---

```python
                self._current_path.closed = False
```
                # 将False赋值给self._current_path.closed

---

```python
                self._current_path._build_path()
```
                # 调用self._current_path的重建贝塞尔路径方法

---

```python
                self._current_path = None
```
                # 当前正在绘制的路径项

---

```python
                self._drawing = False
```
                # 是否正在拖拽中

---

```python
                self._drag_start_pos = None
```
                # 拖拽起始位置

---

```python
                self._hover_state = PenTool.PEN_DEFAULT
```
                # 悬停光标状态


---

```python
    # ── 辅助操作 ──
```
    # 注释：── 辅助操作 ──


---

```python
    def _close_path(self):
```
    # 闭合当前路径，接收自身引用，无返回值

---

```python
        """闭合当前路径"""
```
        # 单行文档字符串：闭合当前路径

---

```python
        if self._current_path and len(self._current_path.anchors) >= 2:
```
        # 如果self._current_path and len(self._current_path.anchors) >= 2（满足条件时执行）

---

```python
            self._current_path.closed = True
```
            # 将True赋值给self._current_path.closed

---

```python
            self._current_path._build_path()
```
            # 调用self._current_path的重建贝塞尔路径方法

---

```python
        self._current_path = None
```
        # 当前正在绘制的路径项

---

```python
        self._drawing = False
```
        # 是否正在拖拽中

---

```python
        self._drag_start_pos = None
```
        # 拖拽起始位置


---

```python
    def _try_delete_anchor(self, pos: QPointF, doc):
```
    # 尝试删除悬停位置的锚点，接收自身引用、鼠标位置坐标：二维浮点坐标、文档对象，无返回值

---

```python
        """尝试删除悬停的锚点（Pen-行为）"""
```
        # 单行文档字符串：尝试删除悬停的锚点（Pen-行为）

---

```python
        for layer in reversed(doc.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in list(layer.items):
```
            # 遍历图层中的所有图形项（复制列表避免遍历中修改），每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or not item.visible or item.locked:
```
                # 如果not isinstance(item, PathItem) or not item.visible or item.locked（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
```
                # 将item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)赋值给anchor_idx

---

```python
                if anchor_idx >= 0 and item.anchor_count > 2:
```
                # 如果anchor_idx >= 0 and item.anchor_count > 2（满足条件时执行）

---

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
                    # 将[a.copy() for a in item.anchors]赋值给old_anchors

---

```python
                    item.remove_anchor(anchor_idx)
```
                    # 调用item的移除锚点方法

---

```python
                    new_anchors = [a.copy() for a in item.anchors]
```
                    # 将[a.copy() for a in item.anchors]赋值给new_anchors

---

```python
                    cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)
```
                    # 将ModifyAnchorCommand(doc, item, old_anchors, new_anchors)赋值给cmd

---

```python
                    doc.execute_command(cmd)
```
                    # 调用doc的执行命令（支持撤销）方法

---

```python
                    return
```
                    # 空返回，结束函数执行


---

```python
    def _try_add_anchor(self, pos: QPointF, doc):
```
    # 尝试在路径段上添加新锚点，接收自身引用、鼠标位置坐标：二维浮点坐标、文档对象，无返回值

---

```python
        """尝试在路径段上添加锚点（Pen+行为）"""
```
        # 单行文档字符串：尝试在路径段上添加锚点（Pen+行为）

---

```python
        for layer in reversed(doc.layers):
```
        # 遍历文档的所有图层（逆序遍历），每次迭代将当前元素赋给layer

---

```python
            if not layer.visible or layer.locked:
```
            # 如果not layer.visible or layer.locked（满足条件时执行）

---

```python
                continue
```
                # 跳过当前迭代，继续下一次循环

---

```python
            for item in list(layer.items):
```
            # 遍历图层中的所有图形项（复制列表避免遍历中修改），每次迭代将当前元素赋给item

---

```python
                if not isinstance(item, PathItem) or not item.visible or item.locked:
```
                # 如果not isinstance(item, PathItem) or not item.visible or item.locked（满足条件时执行）

---

```python
                    continue
```
                    # 跳过当前迭代，继续下一次循环

---

```python
                seg_idx = item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)
```
                # 将item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)赋值给seg_idx

---

```python
                if seg_idx >= 0:
```
                # 如果seg_idx >= 0（满足条件时执行）

---

```python
                    # 找到段上的精确插入位置
```
                    # 注释：找到段上的精确插入位置

---

```python
                    cx, cy = item.get_closest_point_on_segment(seg_idx, pos.x(), pos.y())
```
                    # 函数参数续行：cx, cy = item.get_closest_point_on_segment(seg_idx, pos.x(), pos.y())

---

```python
                    # 在段后插入新锚点
```
                    # 注释：在段后插入新锚点

---

```python
                    old_anchors = [a.copy() for a in item.anchors]
```
                    # 将[a.copy() for a in item.anchors]赋值给old_anchors

---

```python
                    new_anchor = AnchorPoint(cx, cy, anchor_type=AnchorPointType.CORNER)
```
                    # 将AnchorPoint(cx, cy, anchor_type=AnchorPointType.CORNER)赋值给new_anchor

---

```python
                    item.insert_anchor(seg_idx + 1, new_anchor)
```
                    # 调用item的插入锚点方法

---

```python
                    new_anchors = [a.copy() for a in item.anchors]
```
                    # 将[a.copy() for a in item.anchors]赋值给new_anchors

---

```python
                    cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)
```
                    # 将ModifyAnchorCommand(doc, item, old_anchors, new_anchors)赋值给cmd

---

```python
                    doc.execute_command(cmd)
```
                    # 调用doc的执行命令（支持撤销）方法

---

```python
                    return
```
                    # 空返回，结束函数执行


---

```python
    # ── 绘制预览 ──
```
    # 注释：── 绘制预览 ──


---

```python
    def draw_preview(self, painter: QPainter):
```
    # 绘制预览，接收自身引用、绘图引擎：绘图引擎，无返回值

---

```python
        """绘制钢笔工具预览：
```
        # """绘制钢笔工具预览：

---

```python
        - 已放置的锚点
```
        # 文档内容：- 已放置的锚点

---

```python
        - 路径线段
```
        # 文档内容：- 路径线段

---

```python
        - 拖拽中的手柄预览
```
        # 文档内容：- 拖拽中的手柄预览

---

```python
        - 悬停光标指示
```
        # 文档内容：- 悬停光标指示

---

```python
        """
```
        # 文档字符串结束标记

---

```python
        if not self._current_path:
```
        # 如果当前没有路径（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        
```
        # 

---

```python
        anchors = self._current_path.anchors
```
        # 将self._current_path.anchors赋值给anchors

---

```python
        if not anchors:
```
        # 如果not anchors（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        
```
        # 

---

```python
        scale = max(painter.transform().m11(), 0.001)
```
        # 将max(painter.transform().m11(), 0.001)赋值给scale

---

```python
        
```
        # 

---

```python
        # ── 绘制已放置的锚点 ──
```
        # 注释：── 绘制已放置的锚点 ──

---

```python
        for i, anchor in enumerate(anchors):
```
        # 遍历enumerate(anchors)，每次迭代将当前元素赋给i, anchor

---

```python
            pt = QPointF(anchor.x, anchor.y)
```
            # 将QPointF(anchor.x, anchor.y)赋值给pt

---

```python
            
```
            # 

---

```python
            # 锚点圆圈
```
            # 注释：锚点圆圈

---

```python
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
```
            # 调用painter的setPen方法

---

```python
            painter.setBrush(QColor(255, 255, 255))
```
            # 调用painter的setBrush方法

---

```python
            painter.drawEllipse(pt, 3 / scale, 3 / scale)
```
            # 调用painter的drawEllipse方法

---

```python
            
```
            # 

---

```python
            # 手柄线（handle_in）
```
            # 注释：手柄线（handle_in）

---

```python
            if anchor.handle_in:
```
            # 如果anchor.handle_in（满足条件时执行）

---

```python
                hin = QPointF(anchor.x + anchor.handle_in.x(), 
```
                # 将QPointF(anchor.x + anchor.handle_in.x(),赋值给hin

---

```python
                             anchor.y + anchor.handle_in.y())
```
                             # 函数参数续行：anchor.y + anchor.handle_in.y())

---

```python
                pen = QPen(QColor(0, 120, 215), 0.8 / scale)
```
                # 将QPen(QColor(0, 120, 215), 0.8 / scale)赋值给pen

---

```python
                pen.setStyle(Qt.DashLine)
```
                # 调用pen的setStyle方法

---

```python
                painter.setPen(pen)
```
                # 调用painter的setPen方法

---

```python
                painter.drawLine(pt, hin)
```
                # 调用painter的drawLine方法

---

```python
                # 手柄端点
```
                # 注释：手柄端点

---

```python
                painter.setBrush(QColor(255, 255, 255))
```
                # 调用painter的setBrush方法

---

```python
                painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))
```
                # 调用painter的setPen方法

---

```python
                painter.drawEllipse(hin, 2.5 / scale, 2.5 / scale)
```
                # 调用painter的drawEllipse方法

---

```python
            
```
            # 

---

```python
            # 手柄线（handle_out）
```
            # 注释：手柄线（handle_out）

---

```python
            if anchor.handle_out:
```
            # 如果anchor.handle_out（满足条件时执行）

---

```python
                hout = QPointF(anchor.x + anchor.handle_out.x(), 
```
                # 将QPointF(anchor.x + anchor.handle_out.x(),赋值给hout

---

```python
                              anchor.y + anchor.handle_out.y())
```
                              # 函数参数续行：anchor.y + anchor.handle_out.y())

---

```python
                painter.setPen(QPen(QColor(0, 120, 215), 0.8 / scale))
```
                # 调用painter的setPen方法

---

```python
                painter.drawLine(pt, hout)
```
                # 调用painter的drawLine方法

---

```python
                # 手柄端点
```
                # 注释：手柄端点

---

```python
                painter.setBrush(QColor(255, 255, 255))
```
                # 调用painter的setBrush方法

---

```python
                painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))
```
                # 调用painter的setPen方法

---

```python
                painter.drawEllipse(hout, 2.5 / scale, 2.5 / scale)
```
                # 调用painter的drawEllipse方法

---

```python
        
```
        # 

---

```python
        # ── 绘制路径线段 ──
```
        # 注释：── 绘制路径线段 ──

---

```python
        if len(anchors) >= 2:
```
        # 如果len(anchors) >= 2（满足条件时执行）

---

```python
            pen = QPen(QColor(0, 120, 215), 1.5 / scale)
```
            # 将QPen(QColor(0, 120, 215), 1.5 / scale)赋值给pen

---

```python
            painter.setPen(pen)
```
            # 调用painter的setPen方法

---

```python
            painter.setBrush(Qt.NoBrush)
```
            # 调用painter的setBrush方法

---

```python
            
```
            # 

---

```python
            for i in range(len(anchors) - 1):
```
            # 遍历range(len(anchors) - 1)，每次迭代将当前元素赋给i

---

```python
                prev, curr = anchors[i], anchors[i + 1]
```
                # 函数参数续行：prev, curr = anchors[i], anchors[i + 1]

---

```python
                samples = PathItem._sample_bezier_segment(prev, curr, num_samples=30)
```
                # 将PathItem._sample_bezier_segment(prev, curr, num_samples=30)赋值给samples

---

```python
                for k in range(len(samples) - 1):
```
                # 遍历range(len(samples) - 1)，每次迭代将当前元素赋给k

---

```python
                    p1 = QPointF(samples[k][0], samples[k][1])
```
                    # 将QPointF(samples[k][0], samples[k][1])赋值给p1

---

```python
                    p2 = QPointF(samples[k+1][0], samples[k+1][1])
```
                    # 将QPointF(samples[k+1][0], samples[k+1][1])赋值给p2

---

```python
                    painter.drawLine(p1, p2)
```
                    # 调用painter的drawLine方法

---

```python
        
```
        # 

---

```python
        # ── 拖拽中：绘制从最后一个锚点出发的预览手柄 ──
```
        # 注释：── 拖拽中：绘制从最后一个锚点出发的预览手柄 ──

---

```python
        if self._drawing and self._drag_start_pos:
```
        # 如果self._drawing and self._drag_start_pos（满足条件时执行）

---

```python
            last_anchor = anchors[-1]
```
            # 将anchors[-1]赋值给last_anchor

---

```python
            last_pt = QPointF(last_anchor.x, last_anchor.y)
```
            # 将QPointF(last_anchor.x, last_anchor.y)赋值给last_pt

---

```python
            
```
            # 

---

```python
            # 手柄线预览
```
            # 注释：手柄线预览

---

```python
            painter.setPen(QPen(QColor(0, 120, 215, 150), 0.8 / scale, Qt.DashLine))
```
            # 调用painter的setPen方法

---

```python
            painter.drawLine(last_pt, self._drag_start_pos)
```
            # 调用painter的drawLine方法

---

```python
            
```
            # 

---

```python
            # 预览锚点
```
            # 注释：预览锚点

---

```python
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
```
            # 调用painter的setPen方法

---

```python
            painter.setBrush(QColor(0, 120, 215, 100))
```
            # 调用painter的setBrush方法

---

```python
            painter.drawEllipse(self._drag_start_pos, 3 / scale, 3 / scale)
```
            # 调用painter的drawEllipse方法

---

```python
        
```
        # 

---

```python
        # ── 悬停光标指示（在第一个锚点上绘制闭合图标） ──
```
        # 注释：── 悬停光标指示（在第一个锚点上绘制闭合图标） ──

---

```python
        if self._hover_state == PenTool.PEN_CLOSE and len(anchors) >= 2:
```
        # 如果self._hover_state == PenTool.PEN_CLOSE and len(anchors) >= 2（满足条件时执行）

---

```python
            first_pt = QPointF(anchors[0].x, anchors[0].y)
```
            # 将QPointF(anchors[0].x, anchors[0].y)赋值给first_pt

---

```python
            painter.setPen(QPen(QColor(0, 120, 215), 2 / scale))
```
            # 调用painter的setPen方法

---

```python
            painter.setBrush(Qt.NoBrush)
```
            # 调用painter的setBrush方法

---

```python
            r = 6 / scale
```
            # 将6 / scale赋值给r

---

```python
            painter.drawEllipse(first_pt, r, r)
```
            # 调用painter的drawEllipse方法


---

```python
    def cancel(self):
```
    # 取消当前操作，接收自身引用，无返回值

---

```python
        if self._current_path and self._document:
```
        # 如果self._current_path and self._document（满足条件时执行）

---

```python
            self._document.remove_item(self._current_path)
```
            # 调用self._document的移除图形项方法

---

```python
        self._current_path = None
```
        # 当前正在绘制的路径项

---

```python
        self._drawing = False
```
        # 是否正在拖拽中

---

```python
        self._drag_start_pos = None
```
        # 拖拽起始位置

---

```python
        self._hover_state = PenTool.PEN_DEFAULT
```
        # 悬停光标状态

---

```python
        self._ctrl_temp_select = False
```
        # Ctrl临时切换直接选择工具标志

---

```python
        self._space_moving = False
```
        # Space键移动当前锚点标志

---

```python
        super().cancel()
```
        # super().cancel()



---

```python
# ── 文字工具 ──────────────────────────────────────────────
```
# 注释：── 文字工具 ──────────────────────────────────────────────


---

```python
class TextTool(BaseTool):
```
# 定义文字工具类，点击创建文字，继承自(BaseTool)

---

```python
    """文字工具 —— 点击创建文字"""
```
    # 单行文档字符串：文字工具 —— 点击创建文字

---

```python
    __slots__ = ()
```
    # 声明实例属性槽位：()，用于节省内存并提升访问速度


---

```python
    def __init__(self):
```
    # 构造函数，接收自身引用，无返回值

---

```python
        super().__init__(ToolType.TEXT)
```
        # 调用父类构造函数，传入ToolType.TEXT


---

```python
    def mouse_press(self, pos: QPointF, modifiers: int):
```
    # 鼠标按下事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        if not self._document:
```
        # 如果文档对象不存在（满足条件时执行）

---

```python
            return
```
            # 空返回，结束函数执行

---

```python
        text_frame = TextFrame(pos.x(), pos.y())
```
        # 将TextFrame(pos.x(), pos.y())赋值给text_frame

---

```python
        text_frame.contents = "文字"
```
        # 将"文字"赋值给text_frame.contents

---

```python
        text_frame.char_attrs.font_size = 24
```
        # 将24赋值给text_frame.char_attrs.font_size

---

```python
        text_frame.char_attrs.fill_color = QColor(50, 50, 50)
```
        # 将QColor(50, 50, 50)赋值给text_frame.char_attrs.fill_color

---

```python
        text_frame.style.fill_color = None
```
        # 将None赋值给text_frame.style.fill_color

---

```python
        text_frame.selected = True
```
        # 将True赋值给text_frame.selected

---

```python
        self._document.clear_selection()
```
        # 调用self._document的清除所有选中状态方法

---

```python
        self._document.add_item(text_frame)
```
        # 调用self._document的添加图形项方法

---

```python
        self._document.modified = True
```
        # 将True赋值给self._document.modified


---

```python
    def mouse_double_click(self, pos: QPointF, modifiers: int):
```
    # 鼠标双击事件处理，接收自身引用、鼠标位置坐标：二维浮点坐标、修饰键标志位：整数，无返回值

---

```python
        pass  # 由 UI 层处理
```
        # 空操作占位符：由 UI 层处理



---

```python
# ── 抓手工具 ──────────────────────────────────────────────
```
# 注释：── 抓手工具 ──────────────────────────────────────────────


---

```python
class HandTool(BaseTool):
```
# 定义抓手工具类，拖拽平移画布，继承自(BaseTool)

---

```python
    """抓手工具 —— 拖拽平移画布"""
```
    # 单行文档字符串：抓手工具 —— 拖拽平移画布

---

```python
    __slots__ = ()
```
    # 声明实例属性槽位：()，用于节省内存并提升访问速度


---

```python
    def __init__(self):
```
    # 构造函数，接收自身引用，无返回值

---

```python
        super().__init__(ToolType.HAND)
```
        # 调用父类构造函数，传入ToolType.HAND

