"""
Scene Graph — 统一的场景节点树 (Python 3.10+)

对照 Adobe Illustrator 的 Scene Graph 架构：
  SceneNode (抽象基类)
  ├── Document (根节点)
  ├── Layer (图层节点，对应 AI Layer)
  ├── GroupItem (编组节点)
  ├── PathItem / RectangleItem / EllipseItem (路径节点)
  └── TextFrame (文字节点)

单一数据源原则：所有画布渲染和图层面板显示都从这棵 N-ary Tree 读取。

AI 标准的 Z-Order：
  - 同一容器内 children 数组 index 越大 = 越靠上 = 后绘制 = 置前
  - children[0] 先绘制（底层），children[-1] 后绘制（顶层）
  - 图层面板从下往上（列表底部 → 顶部）依次渲染
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
import uuid

from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QColor


class NodeType(Enum):
    """场景节点类型（对照 AI NodeType）"""
    DOCUMENT = auto()
    LAYER = auto()
    SUBLAYER = auto()
    GROUP = auto()
    PATH = auto()
    RECTANGLE = auto()
    ELLIPSE = auto()
    TEXT = auto()
    COMPOUND_PATH = auto()
    PLACED_IMAGE = auto()


class BlendMode(Enum):
    """混合模式"""
    NORMAL = auto()
    MULTIPLY = auto()
    SCREEN = auto()
    OVERLAY = auto()
    DARKEN = auto()
    LIGHTEN = auto()
    COLOR_DODGE = auto()
    COLOR_BURN = auto()
    HARD_LIGHT = auto()
    SOFT_LIGHT = auto()
    DIFFERENCE = auto()
    EXCLUSION = auto()


class PreviewMode(Enum):
    """图层预览模式"""
    PREVIEW = auto()   # 正常预览
    OUTLINE = auto()   # 仅轮廓


# ── SceneNode 基类 ──────────────────────────────────────────

class SceneNode(ABC):
    """所有场景节点的抽象基类

    对照 AI：每个节点都有：
    - 唯一 ID (GUID)
    - 名称
    - 可见性 / 锁定状态
    - 不透明度 (0~100)
    - 混合模式
    - 父节点引用
    - 包围盒

    容器节点 (Layer / Group) 额外有 children[]
    """

    __slots__ = (
        '_id', '_name', '_visible', '_locked',
        '_opacity', '_blend_mode', '_parent',
    )

    def __init__(self, name: str = ""):
        self._id: str = str(uuid.uuid4())
        self._name: str = name
        self._visible: bool = True
        self._locked: bool = False
        self._opacity: float = 1.0
        self._blend_mode: BlendMode = BlendMode.NORMAL
        self._parent: SceneNode | None = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value

    @property
    def locked(self) -> bool:
        return self._locked

    @locked.setter
    def locked(self, value: bool):
        self._locked = value

    @property
    def opacity(self) -> float:
        return self._opacity

    @opacity.setter
    def opacity(self, value: float):
        self._opacity = max(0.0, min(1.0, value))

    @property
    def blend_mode(self) -> BlendMode:
        return self._blend_mode

    @blend_mode.setter
    def blend_mode(self, value: BlendMode):
        self._blend_mode = value

    @property
    def parent(self) -> SceneNode | None:
        return self._parent

    @property
    @abstractmethod
    def node_type(self) -> NodeType:
        """节点类型"""
        ...

    @property
    def is_container(self) -> bool:
        """是否为容器节点（有 children）"""
        return False

    @property
    def children(self) -> list[SceneNode]:
        """子节点列表（仅容器节点有）"""
        return []

    def is_ancestor_visible(self) -> bool:
        """检查祖先链上是否有任何节点不可见"""
        node = self._parent
        while node is not None:
            if not node._visible:
                return False
            node = node._parent
        return True

    def is_ancestor_locked(self) -> bool:
        """检查祖先链上是否有任何节点被锁定"""
        node = self._parent
        while node is not None:
            if node._locked:
                return True
            node = node._parent
        return False

    def depth(self) -> int:
        """在树中的深度"""
        d = 0
        node = self._parent
        while node is not None:
            d += 1
            node = node._parent
        return d

    def root(self) -> SceneNode:
        """获取根节点"""
        node = self
        while node._parent is not None:
            node = node._parent
        return node

    @abstractmethod
    def bounding_rect(self) -> QRectF:
        """几何包围盒（世界坐标）"""
        ...

    @abstractmethod
    def contains_point(self, point: QPointF) -> bool:
        """检测点是否在节点内"""
        ...

    def to_dict(self) -> dict:
        """序列化为字典"""
        return {
            "id": self._id,
            "name": self._name,
            "node_type": self.node_type.name,
            "visible": self._visible,
            "locked": self._locked,
            "opacity": self._opacity,
            "blend_mode": self._blend_mode.name,
        }

    def _load_base_from_dict(self, data: dict):
        """从字典加载基础属性"""
        self._id = data.get("id", self._id)
        self._name = data.get("name", "")
        self._visible = data.get("visible", True)
        self._locked = data.get("locked", False)
        self._opacity = data.get("opacity", 1.0)
        bm = data.get("blend_mode", "NORMAL")
        try:
            self._blend_mode = BlendMode[bm]
        except KeyError:
            self._blend_mode = BlendMode.NORMAL


# ── 容器节点 Mixin ─────────────────────────────────────────

class ContainerMixin:
    """容器节点通用操作（Layer / Group 共用）

    对照 AI：
    - children 数组顺序：index 越大 = 越靠上 = 后绘制
    - 拖拽重排：修改 children 数组中的 sibling order
    - 嵌套：Group 可含 Group / Path / Text，Layer 可含 SubLayer / Group / Path / Text
    """

    __slots__ = ('_children',)

    def __init_container__(self):
        self._children: list[SceneNode] = []

    @property
    def children(self) -> list[SceneNode]:
        return self._children

    @property
    def is_container(self) -> bool:
        return True

    def add_child(self, child: SceneNode, index: int | None = None):
        """添加子节点

        Args:
            child: 子节点
            index: 插入位置，None 表示追加到末尾（顶层）
        """
        child._parent = self
        if index is None:
            self._children.append(child)
        else:
            self._children.insert(index, child)

    def remove_child(self, child: SceneNode):
        """移除子节点"""
        if child in self._children:
            child._parent = None
            self._children.remove(child)

    def index_of(self, child: SceneNode) -> int:
        """获取子节点索引"""
        return self._children.index(child) if child in self._children else -1

    def bring_to_front(self, child: SceneNode):
        """置于顶层：移到 children[-1]（后绘制=视觉顶层）"""
        if child in self._children:
            self._children.remove(child)
            self._children.append(child)

    def send_to_back(self, child: SceneNode):
        """置于底层：移到 children[0]（先绘制=视觉底层）"""
        if child in self._children:
            self._children.remove(child)
            self._children.insert(0, child)

    def bring_forward(self, child: SceneNode):
        """上移一层：索引 +1"""
        idx = self.index_of(child)
        if 0 <= idx < len(self._children) - 1:
            self._children[idx], self._children[idx + 1] = (
                self._children[idx + 1], self._children[idx],
            )

    def send_backward(self, child: SceneNode):
        """下移一层：索引 -1"""
        idx = self.index_of(child)
        if idx > 0:
            self._children[idx], self._children[idx - 1] = (
                self._children[idx - 1], self._children[idx],
            )

    def reorder_child(self, child: SceneNode, new_index: int):
        """将子节点移动到指定位置"""
        if child in self._children:
            self._children.remove(child)
            self._children.insert(new_index, child)

    def all_descendants(self) -> list[SceneNode]:
        """深度优先获取所有后代节点"""
        result = []
        for child in self._children:
            result.append(child)
            if child.is_container:
                result.extend(child.all_descendants())
        return result

    def find_child_by_id(self, node_id: str) -> SceneNode | None:
        """按 ID 查找后代节点"""
        for child in self._children:
            if child.id == node_id:
                return child
            if child.is_container:
                found = child.find_child_by_id(node_id)
                if found:
                    return found
        return None


# ── 脏标记系统 ──────────────────────────────────────────────

class DirtyFlag:
    """脏标记 — 用于增量渲染优化

    对照 AI 的 Dirty Flag 机制：
    - 数据变更时设置脏标记
    - 渲染引擎检测脏标记决定是否重绘
    - 支持区域级脏标记（dirty rect）
    """

    __slots__ = ('_is_dirty', '_dirty_rects', '_full_redraw')

    def __init__(self):
        self._is_dirty: bool = False
        self._dirty_rects: list[QRectF] = []
        self._full_redraw: bool = False

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    def mark_dirty(self, rect: QRectF | None = None):
        """标记为脏"""
        self._is_dirty = True
        if rect is not None:
            self._dirty_rects.append(rect)
        else:
            self._full_redraw = True

    def mark_full_redraw(self):
        """标记需要完全重绘"""
        self._is_dirty = True
        self._full_redraw = True

    def clear(self):
        """清除脏标记"""
        self._is_dirty = False
        self._dirty_rects.clear()
        self._full_redraw = False

    def dirty_bounding_rect(self) -> QRectF | None:
        """获取所有脏区域的合并包围盒"""
        if self._full_redraw:
            return None  # None = 完全重绘
        if not self._dirty_rects:
            return None
        result = self._dirty_rects[0]
        for r in self._dirty_rects[1:]:
            result = result.united(r)
        return result


# ── Layer 级渲染缓存 ────────────────────────────────────────

class LayerRenderCache:
    """图层级离屏渲染缓存

    对照 AI 的 Layer 级离线缓存：
    - 图层内容不变时，直接绘制缓存的 pixmap
    - 内容变更时使缓存失效
    - 大幅减少复杂文档的重复光栅化开销
    """

    __slots__ = ('_cached_pixmap', '_cache_version', '_content_version')

    def __init__(self):
        from PyQt5.QtGui import QPixmap
        self._cached_pixmap: QPixmap | None = None
        self._cache_version: int = 0
        self._content_version: int = 0

    @property
    def is_valid(self) -> bool:
        return (self._cached_pixmap is not None
                and self._cache_version == self._content_version)

    def invalidate(self):
        """使缓存失效"""
        self._content_version += 1

    def update(self, pixmap):
        """更新缓存"""
        self._cached_pixmap = pixmap
        self._cache_version = self._content_version

    def get(self):
        """获取缓存的 pixmap（如果有效）"""
        if self.is_valid:
            return self._cached_pixmap
        return None
