# document.py 中文注解翻译

---

```python
"""
```
# 模块文档字符串开始

```python
文档和图层管理 (Python 3.10+)
```
# 文档和图层管理（要求 Python 3.10 及以上版本）

```python

```
# 空行

```python
对应 Ai Document, Layers, Layer
```
# 对应 Adobe Illustrator 中的文档（Document）、图层集合（Layers）、图层（Layer）

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
#     - 使用 __slots__ 机制减少内存占用

```python
- 使用 X | None 替代 Optional[X]
```
#     - 使用 X | None 语法替代 Optional[X] 写法

```python
- 使用 match-case 替代 if-elif
```
#     - 使用 match-case 语句替代 if-elif 条件判断

```python
- 命令模式集成撤销/重做
```
#     - 集成命令模式实现撤销/重做功能

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
# 从 __future__ 模块导入 annotations 注解功能（支持延迟求值的类型注解）

```python

```
# 空行

```python
import json
```
# 导入 json 标准库（用于 JSON 序列化与反序列化）

```python
import uuid
```
# 导入 uuid 标准库（用于生成唯一标识符）

```python
from enum import Enum, auto
```
# 从 enum 模块导入 Enum 枚举类和 auto 自动赋值函数

```python

```
# 空行

```python
from PyQt5.QtCore import QPointF, QRectF
```
# 从 PyQt5.QtCore 模块导入 QPointF（二维点坐标类）和 QRectF（矩形区域类）

```python
from PyQt5.QtGui import QColor
```
# 从 PyQt5.QtGui 模块导入 QColor（颜色类）

```python

```
# 空行

```python
from ..logging_config import get_logger
```
# 从上级目录的 logging_config 模块导入 get_logger 日志获取函数

```python
from .graphics import (
```
# 从同级 graphics 模块导入以下类：

```python
    GraphicItem, PathItem, RectangleItem, EllipseItem,
```
#     图形项基类、路径项、矩形项、椭圆项

```python
    TextFrame, GroupItem, BlendMode, Swatch,
```
#     文本框、编组项、混合模式、色板

```python
    Command, CommandHistory, AddItemCommand, RemoveItemCommand,
```
#     命令基类、命令历史、添加项命令、移除项命令

```python
    MoveItemsCommand, ChangeStyleCommand, ModifyAnchorCommand,
```
#     移动项命令、修改样式命令、修改锚点命令

```python
    ResizeItemCommand,
```
#     调整项尺寸命令

```python
)
```
# 导入语句结束

```python

```
# 空行

```python
logger = get_logger(__name__)
```
# 获取当前模块名称对应的日志记录器实例

```python

```
# 空行

```python
class DocumentColorMode(Enum):
```
# 定义文档颜色模式枚举类

```python
    """文档颜色模式"""
```
#     类文档字符串：文档颜色模式

```python
    CMYK = auto()
```
#     CMYK 颜色模式（自动赋值）

```python
    RGB = auto()
```
#     RGB 颜色模式（自动赋值）

```python

```
# 空行

```python
class Layer:
```
# 定义图层类（对应 Adobe Illustrator 的图层）

```python
    """图层（对应 Ai Layer）—— 1:1 对照 Adobe Illustrator 图层面板
```
#     类文档字符串：图层（对应 Ai 图层）—— 一一对照 Adobe Illustrator 图层面板

```python
    
```
#     空行

```python
    对照 PDF 各章功能：
```
#     对照 PDF 各章节功能：

```python
    第三章 - 新建图层：Name/Color/Template/Print/Preview 选项
```
#     第三章 - 新建图层：名称/颜色/模板/打印/预览选项

```python
    第四章 - 重命名图层
```
#     第四章 - 重命名图层

```python
    第七章 - 显示与隐藏图层（visible）
```
#     第七章 - 显示与隐藏图层（可见性）

```python
    第八章 - 锁定与解锁图层（locked）
```
#     第八章 - 锁定与解锁图层（锁定状态）

```python
    第十章 - 子图层（sublayers）
```
#     第十章 - 子图层

```python
    第十一章 - 展开与折叠（expanded）
```
#     第十一章 - 展开与折叠（展开状态）

```python
    第十九章 - 模板模式（is_template）：自动锁定+降低透明度
```
#     第十九章 - 模板模式：自动锁定并降低透明度

```python
    第二十章 - 图层颜色（color）：选区/路径边框颜色
```
#     第二十章 - 图层颜色：选区/路径边框颜色

```python
    第二十一章 - 打印控制（printable）
```
#     第二十一章 - 打印控制（可打印性）

```python
    第二十二章 - 预览模式（preview_mode）：preview/outline
```
#     第二十二章 - 预览模式：预览/轮廓

```python
    第二十五章 - 图层与外观系统：图层级效果
```
#     第二十五章 - 图层与外观系统：图层级效果

```python
    """
```
#     类文档字符串结束

```python
    __slots__ = (
```
#     定义固定属性槽（优化内存占用）

```python
        '_id', 'name', 'visible', 'locked', '_items', '_opacity',
```
#         内部唯一标识符、名称、可见性、锁定状态、图形项列表、不透明度

```python
        '_color', '_is_template', '_printable', '_preview_mode',
```
#         图层颜色、是否为模板、是否可打印、预览模式

```python
        '_expanded', '_sublayers', '_parent_layer',
```
#         是否展开、子图层列表、父图层引用

```python
        '_layer_effects',  # 第二十五章：图层级效果
```
#         图层级效果（第二十五章：图层级效果）

```python
    )
```
#     固定属性槽定义结束

```python

```
# 空行

```python
    def __init__(self, name: str = "图层 1"):
```
#     定义初始化方法（接收自身引用、名称参数：字符串默认"图层 1"）

```python
        self._id = str(uuid.uuid4())
```
#         设置内部唯一标识符为 UUID4 生成的字符串

```python
        self.name = name
```
#         设置图层名称为传入的名称参数

```python
        self.visible: bool = True
```
#         设置可见性为真（默认可见）

```python
        self.locked: bool = False
```
#         设置锁定状态为假（默认未锁定）

```python
        self._items: list[GraphicItem] = []
```
#         初始化图形项列表为空列表

```python
        self._opacity: float = 1.0
```
#         设置不透明度为 1.0（完全不透明）

```python
        # 新增字段
```
#         以下为新增字段

```python
        self._color: QColor | None = None          # 图层颜色（用于路径边框标识）
```
#         初始化图层颜色为空（用于路径边框标识）

```python
        self._is_template: bool = False             # 模板模式
```
#         初始化模板模式为假

```python
        self._printable: bool = True                # 打印状态
```
#         初始化打印状态为真（可打印）

```python
        self._preview_mode: str = "preview"         # "preview" 或 "outline"
```
#         初始化预览模式为"preview"（"preview" 或 "outline"）

```python
        self._expanded: bool = True                 # 图层面板展开状态
```
#         初始化图层面板展开状态为真（默认展开）

```python
        self._sublayers: list[Layer] = []           # 子图层列表
```
#         初始化子图层列表为空列表

```python
        self._parent_layer: Layer | None = None     # 父图层
```
#         初始化父图层引用为空（无父图层）

```python
        # 第二十五章：图层级效果
```
#         第二十五章：图层级效果

```python
        self._layer_effects: dict = {
```
#         初始化图层级效果字典，包含以下三种效果：

```python
            "drop_shadow": {"enabled": False, "offset_x": 5, "offset_y": 5, "blur": 4, "color": QColor(0, 0, 0, 100)},
```
#             "投影阴影"：启用状态假、X偏移5、Y偏移5、模糊半径4、颜色为黑色半透明

```python
            "blur": {"enabled": False, "radius": 5},
```
#             "模糊"：启用状态假、模糊半径5

```python
            "transform": {"enabled": False, "scale_x": 1.0, "scale_y": 1.0, "rotate": 0.0},
```
#             "变换"：启用状态假、X缩放1.0、Y缩放1.0、旋转角度0.0

```python
        }
```
#         图层级效果字典定义结束

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def id(self) -> str:
```
#     定义唯一标识符只读属性（返回字符串）

```python
        return self._id
```
#         返回内部唯一标识符

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def items(self) -> list[GraphicItem]:
```
#     定义图形项列表只读属性（返回图形项列表）

```python
        return self._items
```
#         返回内部图形项列表

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def opacity(self) -> float:
```
#     定义不透明度只读属性（返回浮点数）

```python
        return self._opacity
```
#         返回内部不透明度值

```python

```
# 空行

```python
    @opacity.setter
```
#     不透明度属性设置器装饰器

```python
    def opacity(self, value: float):
```
#     定义不透明度设置方法（接收浮点数值）

```python
        self._opacity = max(0.0, min(1.0, value))
```
#         将不透明度值限制在 0.0 到 1.0 之间后赋值

```python

```
# 空行

```python
    # ── 新增属性 ──
```
#     以下为新增属性定义

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def color(self) -> QColor | None:
```
#     定义图层颜色只读属性（返回 QColor 对象或空）

```python
        """图层识别颜色"""
```
#         属性文档字符串：图层识别颜色

```python
        return self._color
```
#         返回内部图层颜色

```python

```
# 空行

```python
    @color.setter
```
#     图层颜色属性设置器装饰器

```python
    def color(self, value: QColor | None):
```
#     定义图层颜色设置方法（接收 QColor 对象或空）

```python
        self._color = value
```
#         将传入的颜色值赋给内部图层颜色

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def is_template(self) -> bool:
```
#     定义模板模式只读属性（返回布尔值）

```python
        """模板模式：自动锁定 + 降低透明度"""
```
#         属性文档字符串：模板模式——自动锁定并降低透明度

```python
        return self._is_template
```
#         返回内部模板模式标志

```python

```
# 空行

```python
    @is_template.setter
```
#     模板模式属性设置器装饰器

```python
    def is_template(self, value: bool):
```
#     定义模板模式设置方法（接收布尔值）

```python
        self._is_template = value
```
#         设置内部模板模式标志

```python
        if value:
```
#         如果值为真（即启用模板模式）

```python
            self.locked = True
```
#             自动将图层锁定

```python
            self._opacity = 0.5
```
#             自动将不透明度降低到 0.5

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def printable(self) -> bool:
```
#     定义可打印性只读属性（返回布尔值）

```python
        """是否参与打印"""
```
#         属性文档字符串：是否参与打印

```python
        return self._printable
```
#         返回内部可打印标志

```python

```
# 空行

```python
    @printable.setter
```
#     可打印性属性设置器装饰器

```python
    def printable(self, value: bool):
```
#     定义可打印性设置方法（接收布尔值）

```python
        self._printable = value
```
#         将传入值赋给内部可打印标志

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def preview_mode(self) -> str:
```
#     定义预览模式只读属性（返回字符串）

```python
        """预览模式：'preview' 或 'outline'"""
```
#         属性文档字符串：预览模式——'preview'（预览）或 'outline'（轮廓）

```python
        return self._preview_mode
```
#         返回内部预览模式值

```python

```
# 空行

```python
    @preview_mode.setter
```
#     预览模式属性设置器装饰器

```python
    def preview_mode(self, value: str):
```
#     定义预览模式设置方法（接收字符串）

```python
        if value in ("preview", "outline"):
```
#         如果传入值是"preview"或"outline"之一

```python
            self._preview_mode = value
```
#             将值赋给内部预览模式

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def expanded(self) -> bool:
```
#     定义展开状态只读属性（返回布尔值）

```python
        return self._expanded
```
#         返回内部展开状态

```python

```
# 空行

```python
    @expanded.setter
```
#     展开状态属性设置器装饰器

```python
    def expanded(self, value: bool):
```
#     定义展开状态设置方法（接收布尔值）

```python
        self._expanded = value
```
#         将传入值赋给内部展开状态

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def sublayers(self) -> list[Layer]:
```
#     定义子图层列表只读属性（返回图层列表）

```python
        return self._sublayers
```
#         返回内部子图层列表

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def parent_layer(self) -> Layer | None:
```
#     定义父图层只读属性（返回图层对象或空）

```python
        return self._parent_layer
```
#         返回内部父图层引用

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def is_sublayer(self) -> bool:
```
#     定义是否为子图层的只读属性（返回布尔值）

```python
        return self._parent_layer is not None
```
#         返回父图层是否存在（非空则为子图层）

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def layer_effects(self) -> dict:
```
#     定义图层级效果只读属性（返回字典）

```python
        """图层级效果（第二十五章）
```
#         属性文档字符串：图层级效果（第二十五章）

```python
        
```
#         空行

```python
        可对整个图层应用：
```
#         可对整个图层应用以下效果：

```python
        - Drop Shadow（阴影）
```
#         - 投影阴影

```python
        - Blur（模糊）
```
#         - 模糊

```python
        - Transform（变换）
```
#         - 变换

```python
        """
```
#         属性文档字符串结束

```python
        return self._layer_effects
```
#         返回内部图层级效果字典

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def all_items_recursive(self) -> list[GraphicItem]:
```
#     定义递归获取所有嵌套对象的只读属性（返回图形项列表）

```python
        """获取所有嵌套对象（包括子图层）用于选择整个图层（第十四章）"""
```
#         属性文档字符串：获取所有嵌套对象（包括子图层）用于选择整个图层（第十四章）

```python
        result = list(self._items)
```
#         初始化结果列表为当前图层的图形项副本

```python
        for sub in self._sublayers:
```
#         遍历每个子图层

```python
            result.extend(sub.all_items())
```
#             将子图层的所有图形项追加到结果列表

```python
        return result
```
#         返回包含所有图形项的结果列表

```python

```
# 空行

```python
    # ── 子图层管理 ──
```
#     以下为子图层管理方法

```python

```
# 空行

```python
    def add_sublayer(self, name: str | None = None) -> Layer:
```
#     定义添加子图层方法（接收名称参数：字符串或空，默认空，返回图层对象）

```python
        """添加子图层"""
```
#         方法文档字符串：添加子图层

```python
        if name is None:
```
#         如果未传入名称

```python
            name = f"子图层 {len(self._sublayers) + 1}"
```
#             自动生成名称为"子图层 N"（N为当前子图层数量加1）

```python
        sub = Layer(name)
```
#         创建新图层实例并传入名称

```python
        sub._parent_layer = self
```
#         设置新图层的父图层为当前图层

```python
        self._sublayers.append(sub)
```
#         将新图层追加到子图层列表

```python
        return sub
```
#         返回新创建的子图层

```python

```
# 空行

```python
    def remove_sublayer(self, sublayer: Layer):
```
#     定义移除子图层方法（接收子图层参数）

```python
        """移除子图层"""
```
#         方法文档字符串：移除子图层

```python
        if sublayer in self._sublayers:
```
#         如果传入的子图层存在于子图层列表中

```python
            sublayer._parent_layer = None
```
#             清除该子图层的父图层引用

```python
            self._sublayers.remove(sublayer)
```
#             从子图层列表中移除该子图层

```python

```
# 空行

```python
    def all_items(self) -> list[GraphicItem]:
```
#     定义获取所有图形项方法（返回图形项列表）

```python
        """获取图层及所有子图层的图形项"""
```
#         方法文档字符串：获取图层及所有子图层的图形项

```python
        result = list(self._items)
```
#         初始化结果列表为当前图层的图形项副本

```python
        for sub in self._sublayers:
```
#         遍历每个子图层

```python
            result.extend(sub.all_items())
```
#             将子图层的所有图形项追加到结果列表

```python
        return result
```
#         返回包含所有图形项的结果列表

```python

```
# 空行

```python
    # ── 复制图层 ──
```
#     以下为复制图层方法

```python

```
# 空行

```python
    def duplicate(self) -> Layer:
```
#     定义复制图层方法（返回图层对象）

```python
        """复制图层（包含所有图形项和子图层）"""
```
#         方法文档字符串：复制图层（包含所有图形项和子图层）

```python
        new_layer = Layer(self.name + " 拷贝")
```
#         创建新图层，名称为原图层名称加" 拷贝"

```python
        new_layer.visible = self.visible
```
#         复制可见性属性

```python
        new_layer.locked = self.locked
```
#         复制锁定状态属性

```python
        new_layer._opacity = self._opacity
```
#         复制不透明度值

```python
        new_layer._color = QColor(self._color) if self._color else None
```
#         如果原图层有颜色则深拷贝颜色对象，否则设为空

```python
        new_layer._is_template = self._is_template
```
#         复制模板模式标志

```python
        new_layer._printable = self._printable
```
#         复制可打印标志

```python
        new_layer._preview_mode = self._preview_mode
```
#         复制预览模式

```python
        # 深拷贝图形项
```
#         以下为深拷贝图形项

```python
        for item in self._items:
```
#         遍历原图层的每个图形项

```python
            data = item.to_dict()
```
#             将图形项序列化为字典

```python
            cloned = GraphicItem.from_dict(data)
```
#             从字典反序列化创建新图形项（深拷贝）

```python
            new_layer.add_item(cloned)
```
#             将克隆的图形项添加到新图层

```python
        # 深拷贝子图层
```
#         以下为深拷贝子图层

```python
        for sub in self._sublayers:
```
#         遍历原图层的每个子图层

```python
            cloned_sub = sub.duplicate()
```
#             递归复制子图层

```python
            cloned_sub._parent_layer = new_layer
```
#             设置克隆子图层的父图层为新图层

```python
            new_layer._sublayers.append(cloned_sub)
```
#             将克隆的子图层追加到新图层的子图层列表

```python
        return new_layer
```
#         返回复制后的新图层

```python

```
# 空行

```python
    # ── 合并 ──
```
#     以下为合并方法

```python

```
# 空行

```python
    def merge_from(self, other: Layer):
```
#     定义从其他图层合并方法（接收另一图层参数）

```python
        """将另一个图层的所有图形项合并到当前图层"""
```
#         方法文档字符串：将另一个图层的所有图形项合并到当前图层

```python
        for item in list(other._items):
```
#         遍历另一图层的图形项列表的副本

```python
            other.remove_item(item)
```
#             从另一图层中移除该图形项

```python
            self.add_item(item)
```
#             将该图形项添加到当前图层

```python
        for sub in list(other._sublayers):
```
#         遍历另一图层的子图层列表的副本

```python
            other._sublayers.remove(sub)
```
#             从另一图层的子图层列表中移除

```python
            sub._parent_layer = self
```
#             将子图层的父图层设置为当前图层

```python
            self._sublayers.append(sub)
```
#             将子图层追加到当前图层的子图层列表

```python

```
# 空行

```python
    # ── 图形项管理 ──
```
#     以下为图形项管理方法

```python

```
# 空行

```python
    def add_item(self, item: GraphicItem, index: int = -1):
```
#     定义添加图形项方法（接收图形项参数和索引参数：整数默认-1）

```python
        """添加图形项到图层"""
```
#         方法文档字符串：添加图形项到图层

```python
        item._layer = self
```
#         设置图形项所属图层为当前图层

```python
        if index < 0 or index >= len(self._items):
```
#         如果索引为负值或超出列表范围

```python
            self._items.append(item)
```
#             将图形项追加到列表末尾

```python
        else:
```
#         否则

```python
            self._items.insert(index, item)
```
#             将图形项插入到指定索引位置

```python

```
# 空行

```python
    def remove_item(self, item: GraphicItem):
```
#     定义移除图形项方法（接收图形项参数）

```python
        """从图层中移除图形项"""
```
#         方法文档字符串：从图层中移除图形项

```python
        if item in self._items:
```
#         如果图形项存在于当前图层的图形项列表中

```python
            item._layer = None
```
#             清除图形项的所属图层引用

```python
            self._items.remove(item)
```
#             从图形项列表中移除该图形项

```python

```
# 空行

```python
    # ── 排列操作 ──
```
#     以下为排列操作方法（调整图形项绘制顺序）

```python

```
# 空行

```python
    def bring_to_front(self, item: GraphicItem):
```
#     定义移到最前方法（接收图形项参数）

```python
        if item in self._items:
```
#         如果图形项存在于当前图层的图形项列表中

```python
            self._items.remove(item)
```
#             先从列表中移除该图形项

```python
            self._items.append(item)
```
#             再追加到列表末尾（绘制在最前面）

```python

```
# 空行

```python
    def send_to_back(self, item: GraphicItem):
```
#     定义移到最后方法（接收图形项参数）

```python
        if item in self._items:
```
#         如果图形项存在于当前图层的图形项列表中

```python
            self._items.remove(item)
```
#             先从列表中移除该图形项

```python
            self._items.insert(0, item)
```
#             再插入到列表开头（绘制在最后面）

```python

```
# 空行

```python
    def bring_forward(self, item: GraphicItem):
```
#     定义上移一层方法（接收图形项参数）

```python
        if item in self._items:
```
#         如果图形项存在于当前图层的图形项列表中

```python
            idx = self._items.index(item)
```
#             获取该图形项在列表中的索引

```python
            if idx < len(self._items) - 1:
```
#             如果该图形项不是列表中最后一个元素

```python
                self._items[idx], self._items[idx + 1] = (
```
#                 交换当前图形项与下一个图形项的位置

```python
                    self._items[idx + 1], self._items[idx],
```
#                 （完成位置交换的另一半）

```python
                )
```
#                 交换操作结束

```python

```
# 空行

```python
    def send_backward(self, item: GraphicItem):
```
#     定义下移一层方法（接收图形项参数）

```python
        if item in self._items:
```
#         如果图形项存在于当前图层的图形项列表中

```python
            idx = self._items.index(item)
```
#             获取该图形项在列表中的索引

```python
            if idx > 0:
```
#             如果该图形项不是列表中第一个元素

```python
                self._items[idx], self._items[idx - 1] = (
```
#                 交换当前图形项与前一个图形项的位置

```python
                    self._items[idx - 1], self._items[idx],
```
#                 （完成位置交换的另一半）

```python
                )
```
#                 交换操作结束

```python

```
# 空行

```python
    # ── 碰撞检测 ──
```
#     以下为碰撞检测方法

```python

```
# 空行

```python
    def get_item_at(self, x: float, y: float) -> GraphicItem | None:
```
#     定义获取指定坐标处图形项方法（接收X坐标：浮点数、Y坐标：浮点数，返回图形项或空）

```python
        """获取指定坐标处最上层的图形项"""
```
#         方法文档字符串：获取指定坐标处最上层的图形项

```python
        pt = QPointF(x, y)
```
#         用传入的坐标创建 QPointF 二维点对象

```python
        for item in reversed(self._items):
```
#         从后向前（即从最上层向下）遍历图形项列表

```python
            if item.visible and not item.locked and item.contains_point(pt):
```
#             如果图形项可见且未锁定且包含该坐标点

```python
                return item
```
#                 返回该图形项

```python
        return None
```
#         未找到则返回空

```python

```
# 空行

```python
    def get_items_in_rect(
```
#     定义获取矩形区域内图形项方法

```python
        self, x: float, y: float, w: float, h: float,
```
#     （接收自身引用、X坐标：浮点数、Y坐标：浮点数、宽度：浮点数、高度：浮点数）

```python
    ) -> list[GraphicItem]:
```
#     返回图形项列表

```python
        """获取矩形选区内的所有图形项"""
```
#         方法文档字符串：获取矩形选区内的所有图形项

```python
        rect = QRectF(x, y, w, h).normalized()
```
#         用传入参数创建矩形区域并标准化（确保宽高为正值）

```python
        result = []
```
#         初始化结果列表为空

```python
        for item in self._items:
```
#         遍历每个图形项

```python
            if item.visible and not item.locked:
```
#             如果图形项可见且未锁定

```python
                if rect.intersects(item.bounding_rect()):
```
#                 如果矩形区域与图形项的边界矩形相交

```python
                    result.append(item)
```
#                     将该图形项追加到结果列表

```python
        return result
```
#         返回结果列表

```python

```
# 空行

```python
    # ── 序列化 ──
```
#     以下为序列化方法（将图层数据转为字典格式）

```python

```
# 空行

```python
    def to_dict(self) -> dict:
```
#     定义序列化为字典方法（返回字典）

```python
        # 序列化 layer_effects
```
#         序列化图层级效果

```python
        effects = {}
```
#         初始化效果字典为空

```python
        for name, effect in self._layer_effects.items():
```
#         遍历图层级效果字典的每个键值对

```python
            eff_copy = dict(effect)
```
#             创建效果字典的浅拷贝

```python
            if "color" in eff_copy and isinstance(eff_copy["color"], QColor):
```
#             如果效果拷贝中包含"color"键且值为 QColor 类型

```python
                c = eff_copy["color"]
```
#                 获取颜色对象

```python
                eff_copy["color"] = [c.red(), c.green(), c.blue(), c.alpha()]
```
#                 将 QColor 转换为红、绿、蓝、透明度的列表形式

```python
            effects[name] = eff_copy
```
#             将转换后的效果存入效果字典

```python
        
```
#         空行

```python
        return {
```
#         返回包含以下字段的数据字典：

```python
            "id": self._id,
```
#             唯一标识符

```python
            "name": self.name,
```
#             图层名称

```python
            "visible": self.visible,
```
#             可见性

```python
            "locked": self.locked,
```
#             锁定状态

```python
            "opacity": self._opacity,
```
#             不透明度

```python
            "color": [self._color.red(), self._color.green(), self._color.blue()] if self._color else None,
```
#             图层颜色（RGB列表，无颜色则为空）

```python
            "is_template": self._is_template,
```
#             模板模式标志

```python
            "printable": self._printable,
```
#             可打印标志

```python
            "preview_mode": self._preview_mode,
```
#             预览模式

```python
            "expanded": self._expanded,
```
#             展开状态

```python
            "items": [item.to_dict() for item in self._items],
```
#             图形项列表（每个图形项序列化为字典）

```python
            "sublayers": [sub.to_dict() for sub in self._sublayers],
```
#             子图层列表（每个子图层递归序列化为字典）

```python
            "layer_effects": effects,
```
#             图层级效果

```python
        }
```
#         数据字典定义结束

```python

```
# 空行

```python
    @staticmethod
```
#     静态方法装饰器

```python
    def from_dict(data: dict) -> Layer:
```
#     定义从字典反序列化为图层对象的静态方法（接收数据字典，返回图层对象）

```python
        layer = Layer(data.get("name", "图层"))
```
#         创建图层实例（名称从字典获取，默认为"图层"）

```python
        layer._id = data.get("id", str(uuid.uuid4()))
```
#         设置唯一标识符（从字典获取，默认生成新的UUID）

```python
        layer.visible = data.get("visible", True)
```
#         设置可见性（默认真）

```python
        layer.locked = data.get("locked", False)
```
#         设置锁定状态（默认假）

```python
        layer._opacity = data.get("opacity", 1.0)
```
#         设置不透明度（默认1.0）

```python
        color_data = data.get("color")
```
#         从字典获取颜色数据

```python
        layer._color = QColor(*color_data) if color_data else None
```
#         如果有颜色数据则创建 QColor 对象，否则设为空

```python
        layer._is_template = data.get("is_template", False)
```
#         设置模板模式（默认假）

```python
        layer._printable = data.get("printable", True)
```
#         设置可打印标志（默认真）

```python
        layer._preview_mode = data.get("preview_mode", "preview")
```
#         设置预览模式（默认"preview"）

```python
        layer._expanded = data.get("expanded", True)
```
#         设置展开状态（默认真）

```python
        layer._items = [GraphicItem.from_dict(i) for i in data.get("items", [])]
```
#         从字典中反序列化每个图形项列表（默认空列表）

```python
        for item in layer._items:
```
#         遍历每个图形项

```python
            item._layer = layer
```
#             设置图形项所属图层为当前图层

```python
        # 子图层
```
#         以下处理子图层

```python
        layer._sublayers = [Layer.from_dict(s) for s in data.get("sublayers", [])]
```
#         递归反序列化子图层列表（默认空列表）

```python
        for sub in layer._sublayers:
```
#         遍历每个子图层

```python
            sub._parent_layer = layer
```
#             设置子图层的父图层为当前图层

```python
        # 图层级效果
```
#         以下处理图层级效果

```python
        effects_data = data.get("layer_effects", {})
```
#         从字典获取图层级效果数据（默认空字典）

```python
        if effects_data:
```
#         如果存在效果数据

```python
            for name, eff in effects_data.items():
```
#             遍历每个效果名称和效果数据

```python
                if name in layer._layer_effects:
```
#                 如果效果名称存在于图层的图层级效果中

```python
                    layer._layer_effects[name].update(eff)
```
#                     用字典数据更新该效果的属性

```python
                    if "color" in eff and isinstance(eff["color"], list) and len(eff["color"]) >= 3:
```
#                     如果效果中包含"color"键且值为列表且长度至少为3

```python
                        alpha = eff["color"][3] if len(eff["color"]) > 3 else 255
```
#                         获取透明度值（如果有第4个元素则使用，否则默认255）

```python
                        layer._layer_effects[name]["color"] = QColor(*eff["color"][:3], alpha)
```
#                         用RGB值和透明度重建 QColor 对象

```python
        return layer
```
#         返回反序列化后的图层对象

```python

```
# 空行

```python
class Document:
```
# 定义文档类（对应 Adobe Illustrator 的文档）

```python
    """文档（对应 Ai Document）"""
```
#     类文档字符串：文档（对应 Ai 文档）

```python
    __slots__ = (
```
#     定义固定属性槽（优化内存占用）

```python
        '_id', 'name', 'width', 'height', 'color_mode',
```
#         内部唯一标识符、名称、宽度、高度、颜色模式

```python
        '_layers', '_swatches', '_file_path', '_modified',
```
#         图层列表、色板列表、文件路径、修改标志

```python
        '_history', '_active_layer_index',
```
#         命令历史、活动图层索引

```python
    )
```
#     固定属性槽定义结束

```python

```
# 空行

```python
    def __init__(
```
#     定义初始化方法

```python
        self,
```
#         接收自身引用

```python
        width: float = 800,
```
#         宽度参数：浮点数默认800

```python
        height: float = 600,
```
#         高度参数：浮点数默认600

```python
        color_mode: DocumentColorMode = DocumentColorMode.RGB,
```
#         颜色模式参数：文档颜色模式枚举默认RGB

```python
        name: str = "未命名-1",
```
#         名称参数：字符串默认"未命名-1"

```python
    ):
```
#     初始化方法参数列表结束

```python
        self._id = str(uuid.uuid4())
```
#         设置内部唯一标识符为 UUID4 生成的字符串

```python
        self.name = name
```
#         设置文档名称为传入的名称参数

```python
        self.width = width
```
#         设置文档宽度

```python
        self.height = height
```
#         设置文档高度

```python
        self.color_mode = color_mode
```
#         设置文档颜色模式

```python
        self._layers: list[Layer] = []
```
#         初始化图层列表为空列表

```python
        self._swatches: list[Swatch] = Swatch.default_swatches()
```
#         初始化色板列表为默认色板集合

```python
        self._file_path: str | None = None
```
#         初始化文件路径为空

```python
        self._modified: bool = False
```
#         初始化修改标志为假（未修改）

```python
        self._history = CommandHistory()
```
#         创建命令历史实例

```python
        self._active_layer_index = 0
```
#         设置活动图层索引为 0（第一个图层）

```python

```
# 空行

```python
        # 默认创建一个图层
```
#         默认创建一个图层

```python
        self._layers.append(Layer("图层 1"))
```
#         追加一个名称为"图层 1"的新图层到图层列表

```python
        logger.debug(f"文档已创建: {name} ({width}x{height}, {color_mode.name})")
```
#         记录调试日志：文档已创建（包含名称、尺寸、颜色模式）

```python

```
# 空行

```python
    # ── 属性 ──
```
#     以下为属性定义

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def id(self) -> str:
```
#     定义唯一标识符只读属性（返回字符串）

```python
        return self._id
```
#         返回内部唯一标识符

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def layers(self) -> list[Layer]:
```
#     定义图层列表只读属性（返回图层列表）

```python
        return self._layers
```
#         返回内部图层列表

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def active_layer(self) -> Layer:
```
#     定义活动图层只读属性（返回图层对象）

```python
        return self._layers[self._active_layer_index]
```
#         返回活动图层索引对应的图层

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def active_layer_index(self) -> int:
```
#     定义活动图层索引只读属性（返回整数）

```python
        return self._active_layer_index
```
#         返回内部活动图层索引

```python

```
# 空行

```python
    @active_layer_index.setter
```
#     活动图层索引属性设置器装饰器

```python
    def active_layer_index(self, value: int):
```
#     定义活动图层索引设置方法（接收整数值）

```python
        if 0 <= value < len(self._layers):
```
#         如果值在有效范围内（0到图层总数减1）

```python
            self._active_layer_index = value
```
#             设置内部活动图层索引

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def swatches(self) -> list[Swatch]:
```
#     定义色板列表只读属性（返回色板列表）

```python
        return self._swatches
```
#         返回内部色板列表

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def modified(self) -> bool:
```
#     定义修改状态只读属性（返回布尔值）

```python
        return self._modified
```
#         返回内部修改标志

```python

```
# 空行

```python
    @modified.setter
```
#     修改状态属性设置器装饰器

```python
    def modified(self, value: bool):
```
#     定义修改状态设置方法（接收布尔值）

```python
        self._modified = value
```
#         将传入值赋给内部修改标志

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def file_path(self) -> str | None:
```
#     定义文件路径只读属性（返回字符串或空）

```python
        return self._file_path
```
#         返回内部文件路径

```python

```
# 空行

```python
    @file_path.setter
```
#     文件路径属性设置器装饰器

```python
    def file_path(self, value: str):
```
#     定义文件路径设置方法（接收字符串）

```python
        self._file_path = value
```
#         将传入值赋给内部文件路径

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def history(self) -> CommandHistory:
```
#     定义命令历史只读属性（返回命令历史对象）

```python
        return self._history
```
#         返回内部命令历史对象

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def can_undo(self) -> bool:
```
#     定义是否可撤销只读属性（返回布尔值）

```python
        return self._history.can_undo
```
#         返回命令历史的可撤销状态

```python

```
# 空行

```python
    @property
```
#     属性装饰器

```python
    def can_redo(self) -> bool:
```
#     定义是否可重做只读属性（返回布尔值）

```python
        return self._history.can_redo
```
#         返回命令历史的可重做状态

```python

```
# 空行

```python
    # ── 命令模式 ──
```
#     以下为命令模式相关方法（撤销/重做）

```python

```
# 空行

```python
    def execute_command(self, command: Command):
```
#     定义执行命令方法（接收命令参数）

```python
        """执行命令并记录到历史"""
```
#         方法文档字符串：执行命令并记录到历史

```python
        logger.debug(f"执行命令: {command.description()}")
```
#         记录调试日志：执行命令（包含命令描述）

```python
        self._history.execute(command)
```
#         通过命令历史执行该命令

```python
        self._modified = True
```
#         标记文档已修改

```python

```
# 空行

```python
    def undo(self) -> bool:
```
#     定义撤销方法（返回布尔值表示是否成功撤销）

```python
        cmd = self._history.undo()
```
#         调用命令历史的撤销方法，获取被撤销的命令

```python
        if cmd:
```
#         如果存在被撤销的命令

```python
            self._modified = True
```
#             标记文档已修改

```python
            return True
```
#             返回真（撤销成功）

```python
        return False
```
#         返回假（没有可撤销的操作）

```python

```
# 空行

```python
    def redo(self) -> bool:
```
#     定义重做方法（返回布尔值表示是否成功重做）

```python
        cmd = self._history.redo()
```
#         调用命令历史的重做方法，获取被重做的命令

```python
        if cmd:
```
#         如果存在被重做的命令

```python
            self._modified = True
```
#             标记文档已修改

```python
            return True
```
#             返回真（重做成功）

```python
        return False
```
#         返回假（没有可重做的操作）

```python

```
# 空行

```python
    # ── 图层操作 ──
```
#     以下为图层操作方法

```python

```
# 空行

```python
    def add_layer(self, name: str | None = None) -> Layer:
```
#     定义添加图层方法（接收名称参数：字符串或空默认空，返回图层对象）

```python
        if name is None:
```
#         如果未传入名称

```python
            name = f"图层 {len(self._layers) + 1}"
```
#             自动生成名称为"图层 N"（N为当前图层数量加1）

```python
        layer = Layer(name)
```
#         创建新图层实例

```python
        self._layers.append(layer)
```
#         将新图层追加到图层列表

```python
        self._active_layer_index = len(self._layers) - 1
```
#         将活动图层索引设为最后一个（即新建的图层）

```python
        self._modified = True
```
#         标记文档已修改

```python
        return layer
```
#         返回新创建的图层

```python

```
# 空行

```python
    def remove_layer(self, layer: Layer):
```
#     定义移除图层方法（接收图层参数）

```python
        if layer in self._layers and len(self._layers) > 1:
```
#         如果图层存在于列表中且图层数量大于1（至少保留一个图层）

```python
            self._layers.remove(layer)
```
#             从图层列表中移除该图层

```python
            if self._active_layer_index >= len(self._layers):
```
#             如果活动图层索引超出范围

```python
                self._active_layer_index = len(self._layers) - 1
```
#                 将活动图层索引调整为最后一个有效索引

```python
            self._modified = True
```
#             标记文档已修改

```python

```
# 空行

```python
    def reorder_layer(self, layer: Layer, new_index: int):
```
#     定义重排图层顺序方法（接收图层参数和新索引参数：整数）

```python
        if layer in self._layers:
```
#         如果图层存在于图层列表中

```python
            self._layers.remove(layer)
```
#             先从列表中移除该图层

```python
            new_index = max(0, min(new_index, len(self._layers)))
```
#             将新索引限制在有效范围内（0到列表长度）

```python
            self._layers.insert(new_index, layer)
```
#             将图层插入到新索引位置

```python
            self._active_layer_index = new_index
```
#             将活动图层索引设为新索引

```python
            self._modified = True
```
#             标记文档已修改

```python

```
# 空行

```python
    def duplicate_layer(self, layer: Layer) -> Layer:
```
#     定义复制图层方法（接收图层参数，返回图层对象）

```python
        """复制图层"""
```
#         方法文档字符串：复制图层

```python
        new_layer = layer.duplicate()
```
#         调用图层的复制方法创建新图层

```python
        idx = self._layers.index(layer) if layer in self._layers else len(self._layers)
```
#         获取原图层索引，如果不在列表中则使用列表末尾索引

```python
        self._layers.insert(idx + 1, new_layer)
```
#         将新图层插入到原图层索引的下一个位置

```python
        self._active_layer_index = idx + 1
```
#         将活动图层索引设为新图层的索引

```python
        self._modified = True
```
#         标记文档已修改

```python
        return new_layer
```
#         返回复制后的新图层

```python

```
# 空行

```python
    def merge_layers(self, layers: list[Layer]) -> Layer | None:
```
#     定义合并图层方法（接收图层列表参数，返回图层对象或空）

```python
        """合并选定图层（PDF 十八）"""
```
#         方法文档字符串：合并选定图层（PDF 第十八章）

```python
        if len(layers) < 2:
```
#         如果图层数量少于2个（无法合并）

```python
            return None
```
#             返回空

```python
        target = layers[0]
```
#         以第一个图层作为合并目标

```python
        for other in layers[1:]:
```
#         遍历其余图层

```python
            target.merge_from(other)
```
#             将其余图层合并到目标图层

```python
            if other in self._layers:
```
#             如果该图层仍在文档的图层列表中

```python
                self._layers.remove(other)
```
#                 从文档图层列表中移除该图层

```python
        self._active_layer_index = self._layers.index(target)
```
#         将活动图层索引设为目标图层的索引

```python
        self._modified = True
```
#         标记文档已修改

```python
        return target
```
#         返回合并后的目标图层

```python

```
# 空行

```python
    def flatten_artwork(self):
```
#     定义拼合图稿方法（无参数无返回值）

```python
        """拼合图稿：将所有图层合并为一个（PDF 十九）"""
```
#         方法文档字符串：拼合图稿——将所有图层合并为一个（PDF 第十九章）

```python
        if len(self._layers) <= 1:
```
#         如果图层数量不超过1个（无需拼合）

```python
            return
```
#             直接返回

```python
        target = self._layers[0]
```
#         以第一个图层作为合并目标

```python
        for other in self._layers[1:]:
```
#         遍历其余图层

```python
            target.merge_from(other)
```
#             将其余图层合并到目标图层

```python
        self._layers = [target]
```
#         将图层列表替换为只包含目标图层

```python
        self._active_layer_index = 0
```
#         将活动图层索引设为 0

```python
        self._modified = True
```
#         标记文档已修改

```python

```
# 空行

```python
    def collect_in_new_layer(self, items: list[GraphicItem], name: str | None = None) -> Layer:
```
#     定义收集到新图层方法（接收图形项列表和可选名称参数，返回图层对象）

```python
        """收集到新图层：将选中对象自动放入新图层（PDF 十六）"""
```
#         方法文档字符串：收集到新图层——将选中对象自动放入新图层（PDF 第十六章）

```python
        new_layer = self.add_layer(name or "收集图层")
```
#         创建新图层（使用传入名称或默认"收集图层"）

```python
        for item in items:
```
#         遍历每个图形项

```python
            # 从原图层移除
```
#             从原图层移除

```python
            for layer in self._layers:
```
#             遍历文档的所有图层

```python
                if item in layer.items:
```
#                 如果图形项在当前图层的图形项列表中

```python
                    layer.remove_item(item)
```
#                     从该图层移除图形项

```python
                    break
```
#                     找到后跳出循环

```python
            # 添加到新图层
```
#             添加到新图层

```python
            new_layer.add_item(item)
```
#             将图形项添加到新图层

```python
        self._modified = True
```
#         标记文档已修改

```python
        return new_layer
```
#         返回新创建的图层

```python

```
# 空行

```python
    def release_to_layers_sequence(self, group: GroupItem):
```
#     定义释放到图层-顺序模式方法（接收编组项参数）

```python
        """释放到图层 - 顺序模式（PDF 十七 - Sequence）"""
```
#         方法文档字符串：释放到图层-顺序模式（PDF 第十七章 - Sequence）

```python
        if not isinstance(group, GroupItem):
```
#         如果传入参数不是编组项类型

```python
            return
```
#             直接返回

```python
        items = list(group.items)
```
#         获取编组中所有图形项的列表副本

```python
        group._items.clear()
```
#         清空编组的图形项列表

```python
        for i, item in enumerate(items):
```
#         带索引遍历每个图形项

```python
            layer_name = f"Layer {i + 1}"
```
#             生成图层名称为"Layer N"

```python
            new_layer = self.add_layer(layer_name)
```
#             创建新图层

```python
            new_layer.add_item(item)
```
#             将图形项添加到新图层

```python
            item._parent = None
```
#             清除图形项的父项引用

```python
        self._modified = True
```
#         标记文档已修改

```python

```
# 空行

```python
    def release_to_layers_build(self, group: GroupItem):
```
#     定义释放到图层-构建模式方法（接收编组项参数）

```python
        """释放到图层 - 构建模式（PDF 十七 - Build）"""
```
#         方法文档字符串：释放到图层-构建模式（PDF 第十七章 - Build）

```python
        if not isinstance(group, GroupItem):
```
#         如果传入参数不是编组项类型

```python
            return
```
#             直接返回

```python
        items = list(group.items)
```
#         获取编组中所有图形项的列表副本

```python
        group._items.clear()
```
#         清空编组的图形项列表

```python
        for i, item in enumerate(items):
```
#         带索引遍历每个图形项

```python
            layer_name = f"Build {i + 1}"
```
#             生成图层名称为"Build N"

```python
            new_layer = self.add_layer(layer_name)
```
#             创建新图层

```python
            # 累积：前面所有图层的内容也复制到当前图层
```
#             累积模式：前面所有图层的内容也复制到当前图层

```python
            for j in range(i + 1):
```
#             遍历从0到当前索引（含）

```python
                if j == i:
```
#                 如果是当前索引（当前图形项）

```python
                    new_layer.add_item(items[j])
```
#                     直接将当前图形项添加到新图层

```python
                else:
```
#                 否则（之前的图形项）

```python
                    data = items[j].to_dict()
```
#                     将图形项序列化为字典

```python
                    clone = GraphicItem.from_dict(data)
```
#                     从字典反序列化创建克隆副本

```python
                    new_layer.add_item(clone)
```
#                     将克隆副本添加到新图层

```python
            if items[i]._parent:
```
#             如果当前图形项有父项引用

```python
                items[i]._parent = None
```
#                 清除父项引用

```python
        self._modified = True
```
#         标记文档已修改

```python

```
# 空行

```python
    def find_layer_for_item(self, item: GraphicItem) -> Layer | None:
```
#     定义查找图形项所在图层方法（接收图形项参数，返回图层或空）

```python
        """查找对象所在图层（PDF 二十三）"""
```
#         方法文档字符串：查找对象所在图层（PDF 第二十三章）

```python
        for layer in self._layers:
```
#         遍历文档的所有图层

```python
            if item in layer.items:
```
#             如果图形项在当前图层的图形项列表中

```python
                return layer
```
#                 返回该图层

```python
            for sub in layer.sublayers:
```
#             遍历当前图层的子图层

```python
                if item in sub.items:
```
#                 如果图形项在子图层的图形项列表中

```python
                    return sub
```
#                     返回该子图层

```python
        return None
```
#         未找到则返回空

```python

```
# 空行

```python
    # ── 图形项操作 ──
```
#     以下为图形项操作方法

```python

```
# 空行

```python
    def add_item(self, item: GraphicItem, layer: Layer | None = None, record: bool = True):
```
#     定义添加图形项方法（接收图形项参数、目标图层：图层或空默认空、是否记录命令：布尔值默认真）

```python
        """添加图形项到指定图层"""
```
#         方法文档字符串：添加图形项到指定图层

```python
        target = layer or self.active_layer
```
#         如果指定了目标图层则使用，否则使用当前活动图层

```python
        if record:
```
#         如果需要记录命令

```python
            self.execute_command(AddItemCommand(self, item, target))
```
#             执行添加项命令（记录到命令历史以支持撤销）

```python
        else:
```
#         否则（不需要记录命令）

```python
            target.add_item(item)
```
#             直接将图形项添加到目标图层

```python
            self._modified = True
```
#             标记文档已修改

```python

```
# 空行

```python
    def remove_item(self, item: GraphicItem, record: bool = True):
```
#     定义删除图形项方法（接收图形项参数、是否记录命令：布尔值默认真）

```python
        """删除图形项"""
```
#         方法文档字符串：删除图形项

```python
        for layer in self._layers:
```
#         遍历文档的所有图层

```python
            if item in layer.items:
```
#             如果图形项在当前图层的图形项列表中

```python
                if record:
```
#                 如果需要记录命令

```python
                    self.execute_command(RemoveItemCommand(self, item, layer))
```
#                     执行移除项命令（记录到命令历史以支持撤销）

```python
                else:
```
#                 否则（不需要记录命令）

```python
                    layer.remove_item(item)
```
#                     直接从图层移除图形项

```python
                    self._modified = True
```
#                     标记文档已修改

```python
                return
```
#                 找到并处理后返回（停止遍历）

```python

```
# 空行

```python
    def get_selection(self) -> list[GraphicItem]:
```
#     定义获取选中图形项方法（返回图形项列表）

```python
        """获取所有选中的图形项"""
```
#         方法文档字符串：获取所有选中的图形项

```python
        selected = []
```
#         初始化选中列表为空

```python
        for layer in self._layers:
```
#         遍历文档的所有图层

```python
            if layer.visible and not layer.locked:
```
#             如果图层可见且未锁定

```python
                for item in layer.items:
```
#                 遍历图层中的每个图形项

```python
                    if item.selected:
```
#                     如果图形项处于选中状态

```python
                        selected.append(item)
```
#                         将图形项追加到选中列表

```python
        return selected
```
#         返回所有选中的图形项列表

```python

```
# 空行

```python
    def clear_selection(self):
```
#     定义清除选择方法（无参数无返回值）

```python
        for item in self.get_selection():
```
#         遍历所有已选中的图形项

```python
            item.selected = False
```
#             将每个图形项的选中状态设为假

```python

```
# 空行

```python
    def select_all(self):
```
#    定义全选方法（无参数无返回值）

```python
        for layer in self._layers:
```
#         遍历文档的所有图层

```python
            if layer.visible and not layer.locked:
```
#             如果图层可见且未锁定

```python
                for item in layer.items:
```
#                 遍历图层中的每个图形项

```python
                    if not item.locked:
```
#                     如果图形项未锁定

```python
                        item.selected = True
```
#                         将图形项设为选中状态

```python

```
# 空行

```python
    def group_selection(self) -> GroupItem | None:
```
#     定义编组选中项方法（返回编组项或空）

```python
        """将选中项编组"""
```
#         方法文档字符串：将选中项编组

```python
        selected = self.get_selection()
```
#         获取所有选中的图形项

```python
        if len(selected) < 2:
```
#         如果选中项少于2个（无法编组）

```python
            return None
```
#             返回空

```python
        group = GroupItem()
```
#         创建新的编组项

```python
        for item in selected:
```
#         遍历每个选中的图形项

```python
            item.selected = False
```
#             取消图形项的选中状态

```python
            for layer in self._layers:
```
#             遍历文档的所有图层

```python
                if item in layer.items:
```
#                 如果图形项在当前图层的图形项列表中

```python
                    layer.remove_item(item)
```
#                     从该图层移除图形项

```python
                    break
```
#                     找到后跳出循环

```python
            group.add_item(item)
```
#             将图形项添加到编组

```python
        self.active_layer.add_item(group)
```
#         将编组添加到当前活动图层

```python
        group.selected = True
```
#         将编组设为选中状态

```python
        self._modified = True
```
#         标记文档已修改

```python
        return group
```
#         返回创建的编组

```python

```
# 空行

```python
    def ungroup(self, group: GroupItem):
```
#     定义取消编组方法（接收编组项参数）

```python
        """取消编组"""
```
#         方法文档字符串：取消编组

```python
        if not isinstance(group, GroupItem):
```
#         如果传入参数不是编组项类型

```python
            return
```
#             直接返回

```python
        for layer in self._layers:
```
#         遍历文档的所有图层

```python
            if group in layer.items:
```
#             如果编组在当前图层的图形项列表中

```python
                layer.remove_item(group)
```
#                 从图层移除编组

```python
                for item in group.items:
```
#                 遍历编组中的每个图形项

```python
                    item._parent = None
```
#                     清除图形项的父项引用

```python
                    layer.add_item(item)
```
#                     将图形项添加回图层

```python
                self._modified = True
```
#                 标记文档已修改

```python
                return
```
#                 处理完毕后返回

```python

```
# 空行

```python
    def get_item_at(self, x: float, y: float) -> GraphicItem | None:
```
#     定义获取指定坐标处图形项方法（接收X坐标：浮点数、Y坐标：浮点数，返回图形项或空）

```python
        """从最上层开始查找点击位置的图形项"""
```
#         方法文档字符串：从最上层开始查找点击位置的图形项

```python
        for layer in reversed(self._layers):
```
#         从后向前（即从最上层向下）遍历图层列表

```python
            if layer.visible and not layer.locked:
```
#             如果图层可见且未锁定

```python
                item = layer.get_item_at(x, y)
```
#                 在该图层中查找指定坐标处的图形项

```python
                if item:
```
#                 如果找到图形项

```python
                    return item
```
#                     返回该图形项

```python
        return None
```
#         未找到则返回空

```python

```
# 空行

```python
    # ── 序列化 ──
```
#     以下为序列化方法（将文档数据保存/加载）

```python

```
# 空行

```python
    def to_dict(self) -> dict:
```
#     定义序列化为字典方法（返回字典）

```python
        return {
```
#         返回包含以下字段的数据字典：

```python
            "version": "2.0",
```
#             文件格式版本号 "2.0"

```python
            "name": self.name,
```
#             文档名称

```python
            "width": self.width,
```
#             文档宽度

```python
            "height": self.height,
```
#             文档高度

```python
            "color_mode": self.color_mode.name,
```
#             颜色模式名称字符串

```python
            "layers": [layer.to_dict() for layer in self._layers],
```
#             图层列表（每个图层递归序列化为字典）

```python
            "active_layer": self._active_layer_index,
```
#             活动图层索引

```python
        }
```
#         数据字典定义结束

```python

```
# 空行

```python
    def save(self, file_path: str):
```
#     定义保存文档方法（接收文件路径参数：字符串）

```python
        data = self.to_dict()
```
#         将文档序列化为字典数据

```python
        with open(file_path, "w", encoding="utf-8") as f:
```
#         以UTF-8编码模式打开文件进行写入

```python
            json.dump(data, f, ensure_ascii=False, indent=2)
```
#             将字典数据以JSON格式写入文件（禁用ASCII转义，缩进2空格）

```python
        self._file_path = file_path
```
#         设置文档的文件路径

```python
        self._modified = False
```
#         重置修改标志为假（已保存未修改）

```python
        layer_count = len(self._layers)
```
#         获取图层数量

```python
        logger.info(f"文档已保存: {file_path} ({layer_count} 个图层)")
```
#         记录信息日志：文档已保存（包含文件路径和图层数量）

```python

```
# 空行

```python
    @staticmethod
```
#     静态方法装饰器

```python
    def load(file_path: str) -> Document:
```
#     定义加载文档的静态方法（接收文件路径参数：字符串，返回文档对象）

```python
        import os
```
#         导入 os 操作系统模块（用于路径处理）

```python
        with open(file_path, "r", encoding="utf-8") as f:
```
#         以UTF-8编码模式打开文件进行读取

```python
            data = json.load(f)
```
#             从文件中加载JSON数据为字典

```python
        name = data.get("name") or os.path.splitext(os.path.basename(file_path))[0]
```
#         获取文档名称（从数据中获取，如果不存在则从文件名中提取不带扩展名的部分）

```python
        doc = Document(
```
#         创建文档实例，传入以下参数：

```python
            width=data.get("width", 800),
```
#             宽度（从数据获取，默认800）

```python
            height=data.get("height", 600),
```
#             高度（从数据获取，默认600）

```python
            name=name,
```
#             名称

```python
        )
```
#         文档实例创建完成

```python
        doc._file_path = file_path
```
#         设置文档的文件路径

```python
        doc._modified = False
```
#         重置修改标志为假

```python
        doc._layers = [Layer.from_dict(l) for l in data.get("layers", [])]
```
#         从数据中反序列化图层列表（每个图层从字典恢复，默认空列表）

```python
        doc._active_layer_index = data.get("active_layer", 0)
```
#         设置活动图层索引（从数据获取，默认0）

```python
        logger.info(f"文档已加载: {file_path} ({len(doc._layers)} 个图层, {doc.width}x{doc.height})")
```
#         记录信息日志：文档已加载（包含文件路径、图层数量和尺寸）

```python
        return doc
```
#         返回加载后的文档对象
