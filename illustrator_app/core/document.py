"""
文档和图层管理 (Python 3.10+)

对应 Ai Document, Layers, Layer

架构优化:
- 使用 __slots__ 减少内存占用
- 使用 X | None 替代 Optional[X]
- 使用 match-case 替代 if-elif
- 命令模式集成撤销/重做
"""

from __future__ import annotations

import json
import uuid
from enum import Enum, auto

from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QColor

from ..logging_config import get_logger
from .graphics import (
    GraphicItem, PathItem, RectangleItem, EllipseItem,
    TextFrame, GroupItem, BlendMode, Swatch,
    Command, CommandHistory, AddItemCommand, RemoveItemCommand,
    MoveItemsCommand, ChangeStyleCommand, ModifyAnchorCommand,
    ResizeItemCommand,
)
from .scene_graph import DirtyFlag, LayerRenderCache, ContainerMixin

logger = get_logger(__name__)


class DocumentColorMode(Enum):
    """文档颜色模式"""
    CMYK = auto()
    RGB = auto()


class Layer:
    """图层（对应 Ai Layer）—— 1:1 对照 Adobe Illustrator 图层面板
    
    对照 PDF 各章功能：
    第三章 - 新建图层：Name/Color/Template/Print/Preview 选项
    第四章 - 重命名图层
    第七章 - 显示与隐藏图层（visible）
    第八章 - 锁定与解锁图层（locked）
    第十章 - 子图层（sublayers）
    第十一章 - 展开与折叠（expanded）
    第十九章 - 模板模式（is_template）：自动锁定+降低透明度
    第二十章 - 图层颜色（color）：选区/路径边框颜色
    第二十一章 - 打印控制（printable）
    第二十二章 - 预览模式（preview_mode）：preview/outline
    第二十五章 - 图层与外观系统：图层级效果
    """
    __slots__ = (
        '_id', 'name', 'visible', 'locked', '_items', '_opacity',
        '_color', '_is_template', '_printable', '_preview_mode',
        '_expanded', '_sublayers', '_parent_layer',
        '_layer_effects',  # 第二十五章：图层级效果
    )

    def __init__(self, name: str = "图层 1"):
        self._id = str(uuid.uuid4())
        self.name = name
        self.visible: bool = True
        self.locked: bool = False
        self._items: list[GraphicItem] = []
        self._opacity: float = 1.0
        # 新增字段
        self._color: QColor | None = None          # 图层颜色（用于路径边框标识）
        self._is_template: bool = False             # 模板模式
        self._printable: bool = True                # 打印状态
        self._preview_mode: str = "preview"         # "preview" 或 "outline"
        self._expanded: bool = True                 # 图层面板展开状态
        self._sublayers: list[Layer] = []           # 子图层列表
        self._parent_layer: Layer | None = None     # 父图层
        # 第二十五章：图层级效果
        self._layer_effects: dict = {
            "drop_shadow": {"enabled": False, "offset_x": 5, "offset_y": 5, "blur": 4, "color": QColor(0, 0, 0, 100)},
            "blur": {"enabled": False, "radius": 5},
            "transform": {"enabled": False, "scale_x": 1.0, "scale_y": 1.0, "rotate": 0.0},
        }

    @property
    def id(self) -> str:
        return self._id

    @property
    def items(self) -> list[GraphicItem]:
        return self._items

    @property
    def opacity(self) -> float:
        return self._opacity

    @opacity.setter
    def opacity(self, value: float):
        self._opacity = max(0.0, min(1.0, value))

    # ── 新增属性 ──

    @property
    def color(self) -> QColor | None:
        """图层识别颜色"""
        return self._color

    @color.setter
    def color(self, value: QColor | None):
        self._color = value

    @property
    def is_template(self) -> bool:
        """模板模式：自动锁定 + 降低透明度"""
        return self._is_template

    @is_template.setter
    def is_template(self, value: bool):
        self._is_template = value
        if value:
            self.locked = True
            self._opacity = 0.5

    @property
    def printable(self) -> bool:
        """是否参与打印"""
        return self._printable

    @printable.setter
    def printable(self, value: bool):
        self._printable = value

    @property
    def preview_mode(self) -> str:
        """预览模式：'preview' 或 'outline'"""
        return self._preview_mode

    @preview_mode.setter
    def preview_mode(self, value: str):
        if value in ("preview", "outline"):
            self._preview_mode = value

    @property
    def expanded(self) -> bool:
        return self._expanded

    @expanded.setter
    def expanded(self, value: bool):
        self._expanded = value

    @property
    def sublayers(self) -> list[Layer]:
        return self._sublayers

    @property
    def parent_layer(self) -> Layer | None:
        return self._parent_layer

    @property
    def is_sublayer(self) -> bool:
        return self._parent_layer is not None

    @property
    def layer_effects(self) -> dict:
        """图层级效果（第二十五章）
        
        可对整个图层应用：
        - Drop Shadow（阴影）
        - Blur（模糊）
        - Transform（变换）
        """
        return self._layer_effects

    @property
    def all_items_recursive(self) -> list[GraphicItem]:
        """获取所有嵌套对象（包括子图层及其子子图层）用于选择整个图层（第十四章）
        
        对应 AI Scene Graph 的深度优先遍历：递归收集当前图层 items + 所有嵌套子图层的 items
        """
        result = list(self._items)
        for sub in self._sublayers:
            result.extend(sub.all_items_recursive)
        return result

    # ── 子图层管理 ──

    def add_sublayer(self, name: str | None = None) -> Layer:
        """添加子图层"""
        if name is None:
            name = f"子图层 {len(self._sublayers) + 1}"
        sub = Layer(name)
        sub._parent_layer = self
        self._sublayers.append(sub)
        return sub

    def remove_sublayer(self, sublayer: Layer):
        """移除子图层"""
        if sublayer in self._sublayers:
            sublayer._parent_layer = None
            self._sublayers.remove(sublayer)

    def all_items(self) -> list[GraphicItem]:
        """获取图层及所有子图层的图形项"""
        result = list(self._items)
        for sub in self._sublayers:
            result.extend(sub.all_items())
        return result

    # ── 复制图层 ──

    def duplicate(self) -> Layer:
        """复制图层（包含所有图形项和子图层）"""
        new_layer = Layer(self.name + " 拷贝")
        new_layer.visible = self.visible
        new_layer.locked = self.locked
        new_layer._opacity = self._opacity
        new_layer._color = QColor(self._color) if self._color else None
        new_layer._is_template = self._is_template
        new_layer._printable = self._printable
        new_layer._preview_mode = self._preview_mode
        # 深拷贝图形项
        for item in self._items:
            data = item.to_dict()
            cloned = GraphicItem.from_dict(data)
            new_layer.add_item(cloned)
        # 深拷贝子图层
        for sub in self._sublayers:
            cloned_sub = sub.duplicate()
            cloned_sub._parent_layer = new_layer
            new_layer._sublayers.append(cloned_sub)
        return new_layer

    # ── 合并 ──

    def merge_from(self, other: Layer):
        """将另一个图层的所有图形项合并到当前图层"""
        for item in list(other._items):
            other.remove_item(item)
            self.add_item(item)
        for sub in list(other._sublayers):
            other._sublayers.remove(sub)
            sub._parent_layer = self
            self._sublayers.append(sub)

    # ── 图形项管理 ──

    def add_item(self, item: GraphicItem, index: int = -1):
        """添加图形项到图层
        
        对照 AI 行为：新创建的对象应出现在视觉最顶层（最后绘制）
        items[0] = 面板上方 = 视觉顶层（后绘制）
        items[-1] = 面板下方 = 视觉底层（先绘制）
        因此新对象插入到 items[0] 位置
        """
        item._layer = self
        if index < 0 or index >= len(self._items):
            self._items.insert(0, item)  # 插入到开头 = 视觉顶层
        else:
            self._items.insert(index, item)

    def remove_item(self, item: GraphicItem):
        """从图层中移除图形项"""
        if item in self._items:
            item._layer = None
            self._items.remove(item)

    # ── 排列操作 ──
    # 新语义：items[0] = 面板上方 = 视觉顶层（后绘制）
    #         items[-1] = 面板下方 = 视觉底层（先绘制）
    # bring_* 操作让对象向列表开头移动（面板上方/视觉上层）
    # send_* 操作让对象向列表末尾移动（面板下方/视觉下层）

    def bring_to_front(self, item: GraphicItem):
        """置顶：移到 items[0]（面板最上方/视觉最顶层）"""
        if item in self._items:
            self._items.remove(item)
            self._items.insert(0, item)

    def send_to_back(self, item: GraphicItem):
        """置底：移到 items[-1]（面板最下方/视觉最底层）"""
        if item in self._items:
            self._items.remove(item)
            self._items.append(item)

    def bring_forward(self, item: GraphicItem):
        """上移一层：向列表开头移动一位（面板向上）"""
        if item in self._items:
            idx = self._items.index(item)
            if idx > 0:
                self._items[idx], self._items[idx - 1] = (
                    self._items[idx - 1], self._items[idx],
                )

    def send_backward(self, item: GraphicItem):
        """下移一层：向列表末尾移动一位（面板向下）"""
        if item in self._items:
            idx = self._items.index(item)
            if idx < len(self._items) - 1:
                self._items[idx], self._items[idx + 1] = (
                    self._items[idx + 1], self._items[idx],
                )

    # ── 碰撞检测 ──

    def get_item_at(self, x: float, y: float) -> GraphicItem | None:
        """获取指定坐标处最上层的图形项（考虑对象变换 _transform）
        
        新语义：items[0] = 视觉顶层，items[-1] = 视觉底层
        正序遍历 self._items，先遇到 items[0](顶层) 的命中优先返回
        """
        pt = QPointF(x, y)
        for item in self._items:  # 正序：items[0](顶层)优先检测
            if not item.visible or item.locked:
                continue
            # contains_point 内部已做逆变换，直接传入世界坐标
            if item.contains_point(pt):
                return item
        return None

    def get_items_in_rect(
        self, x: float, y: float, w: float, h: float,
    ) -> list[GraphicItem]:
        """获取矩形选区内的所有图形项（考虑对象变换 _transform）"""
        rect = QRectF(x, y, w, h).normalized()
        result = []
        for item in self._items:
            if item.visible and not item.locked:
                # 使用世界坐标系中的 bounding_rect 进行相交检测
                world_br = item._transform.mapRect(item.bounding_rect())
                if rect.intersects(world_br):
                    result.append(item)
        return result

    # ── 序列化 ──

    def to_dict(self) -> dict:
        # 序列化 layer_effects
        effects = {}
        for name, effect in self._layer_effects.items():
            eff_copy = dict(effect)
            if "color" in eff_copy and isinstance(eff_copy["color"], QColor):
                c = eff_copy["color"]
                eff_copy["color"] = [c.red(), c.green(), c.blue(), c.alpha()]
            effects[name] = eff_copy
        
        return {
            "id": self._id,
            "name": self.name,
            "visible": self.visible,
            "locked": self.locked,
            "opacity": self._opacity,
            "color": [self._color.red(), self._color.green(), self._color.blue()] if self._color else None,
            "is_template": self._is_template,
            "printable": self._printable,
            "preview_mode": self._preview_mode,
            "expanded": self._expanded,
            "items": [item.to_dict() for item in self._items],
            "sublayers": [sub.to_dict() for sub in self._sublayers],
            "layer_effects": effects,
        }

    @staticmethod
    def from_dict(data: dict) -> Layer:
        layer = Layer(data.get("name", "图层"))
        layer._id = data.get("id", str(uuid.uuid4()))
        layer.visible = data.get("visible", True)
        layer.locked = data.get("locked", False)
        layer._opacity = data.get("opacity", 1.0)
        color_data = data.get("color")
        layer._color = QColor(*color_data) if color_data else None
        layer._is_template = data.get("is_template", False)
        layer._printable = data.get("printable", True)
        layer._preview_mode = data.get("preview_mode", "preview")
        layer._expanded = data.get("expanded", True)
        layer._items = [GraphicItem.from_dict(i) for i in data.get("items", [])]
        for item in layer._items:
            item._layer = layer
        # 子图层
        layer._sublayers = [Layer.from_dict(s) for s in data.get("sublayers", [])]
        for sub in layer._sublayers:
            sub._parent_layer = layer
        # 图层级效果
        effects_data = data.get("layer_effects", {})
        if effects_data:
            for name, eff in effects_data.items():
                if name in layer._layer_effects:
                    layer._layer_effects[name].update(eff)
                    if "color" in eff and isinstance(eff["color"], list) and len(eff["color"]) >= 3:
                        alpha = eff["color"][3] if len(eff["color"]) > 3 else 255
                        layer._layer_effects[name]["color"] = QColor(*eff["color"][:3], alpha)
        return layer


class Document:
    """文档（对应 Ai Document）"""
    __slots__ = (
        '_id', 'name', 'width', 'height', 'color_mode',
        '_layers', '_swatches', '_file_path', '_modified',
        '_history', '_active_layer_index',
        '_dirty_flag',
    )

    def __init__(
        self,
        width: float = 800,
        height: float = 600,
        color_mode: DocumentColorMode = DocumentColorMode.RGB,
        name: str = "未命名-1",
    ):
        self._id = str(uuid.uuid4())
        self.name = name
        self.width = width
        self.height = height
        self.color_mode = color_mode
        self._layers: list[Layer] = []
        self._swatches: list[Swatch] = Swatch.default_swatches()
        self._file_path: str | None = None
        self._modified: bool = False
        self._history = CommandHistory()
        self._active_layer_index = 0
        self._dirty_flag = DirtyFlag()

        # 默认创建一个图层
        self._layers.append(Layer("图层 1"))
        logger.debug(f"文档已创建: {name} ({width}x{height}, {color_mode.name})")

    # ── 属性 ──

    @property
    def id(self) -> str:
        return self._id

    @property
    def layers(self) -> list[Layer]:
        return self._layers

    @property
    def active_layer(self) -> Layer:
        return self._layers[self._active_layer_index]

    @property
    def active_layer_index(self) -> int:
        return self._active_layer_index

    @active_layer_index.setter
    def active_layer_index(self, value: int):
        if 0 <= value < len(self._layers):
            self._active_layer_index = value

    @property
    def swatches(self) -> list[Swatch]:
        return self._swatches

    @property
    def dirty_flag(self) -> DirtyFlag:
        """脏标记 — 用于增量渲染优化（对照 AI Dirty Flag 机制）"""
        return self._dirty_flag

    def mark_dirty(self, rect: QRectF | None = None):
        """标记文档需要重绘"""
        self._dirty_flag.mark_dirty(rect)

    @property
    def modified(self) -> bool:
        return self._modified

    @modified.setter
    # 修改状态属性设置装饰器
    def modified(self, value: bool):
        self._modified = value

    @property
    def file_path(self) -> str | None:
        return self._file_path

    @file_path.setter
    def file_path(self, value: str):
        self._file_path = value

    @property
    def history(self) -> CommandHistory:
        return self._history

    @property
    def can_undo(self) -> bool:
        return self._history.can_undo

    @property
    def can_redo(self) -> bool:
        return self._history.can_redo

    # ── 命令模式 ──

    def execute_command(self, command: Command):
        """执行命令并记录到历史"""
        logger.debug(f"执行命令: {command.description()}")
        self._history.execute(command)
        self._modified = True
        self._dirty_flag.mark_dirty()

    def undo(self) -> bool:
        cmd = self._history.undo()
        if cmd:
            self._modified = True
            self._dirty_flag.mark_dirty()
            return True
        return False

    def redo(self) -> bool:
        cmd = self._history.redo()
        if cmd:
            self._modified = True
            self._dirty_flag.mark_dirty()
            return True
        return False

    # ── 图层操作 ──

    def add_layer(self, name: str | None = None) -> Layer:
        # 添加图层
        if name is None:
            name = f"图层 {len(self._layers) + 1}"
        layer = Layer(name)
        self._layers.append(layer)
        self._active_layer_index = len(self._layers) - 1
        self._modified = True
        return layer

    def remove_layer(self, layer: Layer):
        if layer in self._layers and len(self._layers) > 1:
            self._layers.remove(layer)
            if self._active_layer_index >= len(self._layers):
                self._active_layer_index = len(self._layers) - 1
            self._modified = True

    def reorder_layer(self, layer: Layer, new_index: int):
        """重新排序图层
        
        Args:
            layer: 要移动的图层
            new_index: 目标位置索引（0-based，移除 layer 后在剩余列表中的位置）
                       0 = 最底层（最先绘制），len(layers)-1 = 最顶层（最后绘制）
        """
        if layer in self._layers:
            old_index = self._layers.index(layer)
            self._layers.remove(layer)
            # 移除后列表长度减1，clamp new_index 到有效范围
            new_index = max(0, min(new_index, len(self._layers)))
            self._layers.insert(new_index, layer)
            self._active_layer_index = new_index
            self._modified = True
            self._dirty_flag.mark_dirty()

    def duplicate_layer(self, layer: Layer) -> Layer:
        """复制图层"""
        new_layer = layer.duplicate()
        idx = self._layers.index(layer) if layer in self._layers else len(self._layers)
        self._layers.insert(idx + 1, new_layer)
        self._active_layer_index = idx + 1
        self._modified = True
        return new_layer

    def merge_layers(self, layers: list[Layer]) -> Layer | None:
        """合并选定图层（PDF 十八）"""
        if len(layers) < 2:
            return None
        target = layers[0]
        for other in layers[1:]:
            target.merge_from(other)
            if other in self._layers:
                self._layers.remove(other)
        self._active_layer_index = self._layers.index(target)
        self._modified = True
        return target

    def flatten_artwork(self):
        """拼合图稿：将所有图层合并为一个（PDF 十九）"""
        if len(self._layers) <= 1:
            return
        target = self._layers[0]
        for other in self._layers[1:]:
            target.merge_from(other)
        self._layers = [target]
        self._active_layer_index = 0
        self._modified = True

    def collect_in_new_layer(self, items: list[GraphicItem], name: str | None = None) -> Layer:
        """收集到新图层：将选中对象自动放入新图层（PDF 十六）"""
        new_layer = self.add_layer(name or "收集图层")
        for item in items:
            # 从原图层移除
            for layer in self._layers:
                if item in layer.items:
                    layer.remove_item(item)
                    break
            # 添加到新图层
            new_layer.add_item(item)
        self._modified = True
        return new_layer

    def release_to_layers_sequence(self, group: GroupItem):
        """释放到图层 - 顺序模式（PDF 十七 - Sequence）"""
        if not isinstance(group, GroupItem):
            return
        items = list(group.items)
        group._items.clear()
        for i, item in enumerate(items):
            layer_name = f"Layer {i + 1}"
            new_layer = self.add_layer(layer_name)
            new_layer.add_item(item)
            item._parent = None
        self._modified = True

    def release_to_layers_build(self, group: GroupItem):
        """释放到图层 - 构建模式（PDF 十七 - Build）"""
        if not isinstance(group, GroupItem):
            return
        items = list(group.items)
        group._items.clear()
        for i, item in enumerate(items):
            layer_name = f"Build {i + 1}"
            new_layer = self.add_layer(layer_name)
            # 累积：前面所有图层的内容也复制到当前图层
            for j in range(i + 1):
                if j == i:
                    new_layer.add_item(items[j])
                else:
                    data = items[j].to_dict()
                    clone = GraphicItem.from_dict(data)
                    new_layer.add_item(clone)
            if items[i]._parent:
                items[i]._parent = None
        self._modified = True

    def find_layer_for_item(self, item: GraphicItem) -> Layer | None:
        # 定义查找图形项所在图层方法
        """查找对象所在图层（PDF 二十三）"""
        for layer in self._layers:
            if item in layer.items:
                return layer
            for sub in layer.sublayers:
                if item in sub.items:
                    return sub
        return None

    # ── 图形项操作 ──

    def add_item(self, item: GraphicItem, layer: Layer | None = None, record: bool = True):
        """添加图形项到指定图层"""
        target = layer or self.active_layer
        if record:
            self.execute_command(AddItemCommand(self, item, target))
        else:
            target.add_item(item)
            self._modified = True

    def remove_item(self, item: GraphicItem, record: bool = True):
        """删除图形项"""
        for layer in self._layers:
            if item in layer.items:
                if record:
                    self.execute_command(RemoveItemCommand(self, item, layer))
                else:
                    layer.remove_item(item)
                    self._modified = True
                return

    def get_selection(self) -> list[GraphicItem]:
        """获取所有选中的图形项"""
        selected = []
        for layer in self._layers:
            if layer.visible and not layer.locked:
                for item in layer.items:
                    if item.selected:
                        selected.append(item)
        return selected

    def clear_selection(self):
        for item in self.get_selection():
            item.selected = False

    def select_all(self):
        for layer in self._layers:
            if layer.visible and not layer.locked:
                for item in layer.items:
                    if not item.locked:
                        item.selected = True

    def group_selection(self) -> GroupItem | None:
        """将选中项编组"""
        selected = self.get_selection()
        if len(selected) < 2:
            return None
        group = GroupItem()
        for item in selected:
            item.selected = False
            for layer in self._layers:
                if item in layer.items:
                    layer.remove_item(item)
                    break
            group.add_item(item)
        self.active_layer.add_item(group)
        group.selected = True
        self._modified = True
        return group

    def ungroup(self, group: GroupItem):
        """取消编组"""
        if not isinstance(group, GroupItem):
            return
        for layer in self._layers:
            if group in layer.items:
                layer.remove_item(group)
                for item in group.items:
                    item._parent = None
                    layer.add_item(item)
                self._modified = True
                return

    def get_item_at(self, x: float, y: float) -> GraphicItem | None:
        """从最上层开始查找点击位置的图形项（考虑对象变换 _transform）
        
        新语义：layers[-1] = 最新图层 = 视觉顶层
        反序遍历 self._layers，优先检测顶层图层的对象
        """
        for layer in reversed(self._layers):  # 反序：layers[-1](顶层)优先
            if layer.visible and not layer.locked:
                item = layer.get_item_at(x, y)
                if item:
                    return item
        return None

    # ── 序列化 ──

    def to_dict(self) -> dict:
        return {
            "version": "2.0",
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "color_mode": self.color_mode.name,
            "layers": [layer.to_dict() for layer in self._layers],
            "active_layer": self._active_layer_index,
        }

    def save(self, file_path: str):
        data = self.to_dict()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self._file_path = file_path
        self._modified = False
        layer_count = len(self._layers)
        logger.info(f"文档已保存: {file_path} ({layer_count} 个图层)")

    @staticmethod
    def load(file_path: str) -> Document:
        import os
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        name = data.get("name") or os.path.splitext(os.path.basename(file_path))[0]
        doc = Document(
            width=data.get("width", 800),
            height=data.get("height", 600),
            name=name,
        )
        doc._file_path = file_path
        doc._modified = False
        doc._layers = [Layer.from_dict(l) for l in data.get("layers", [])]
        doc._active_layer_index = data.get("active_layer", 0)
        logger.info(f"文档已加载: {file_path} ({len(doc._layers)} 个图层, {doc.width}x{doc.height})")
        return doc
