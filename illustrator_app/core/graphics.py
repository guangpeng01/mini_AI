"""
Illustrator 核心图形引擎 (Python 3.10+)

定义所有图形对象的数据模型：路径、矩形、椭圆、文字、编组等
支持贝塞尔曲线、渐变、布尔运算等高级特性

架构优化 (v2.0):
- 使用 __slots__ 减少内存占用
- 使用 dataclass(slots=True) (Python 3.10+)
- 使用 X | None 替代 Optional[X] (Python 3.10+)
- 使用 match-case 替代 if-elif 链 (Python 3.10+)
- 使用 KW_ONLY 改善 dataclass 可读性 (Python 3.10+)
- 统一的 ABC 基类设计
- 命令模式 + 撤销/重做系统
"""

from __future__ import annotations

import math
import uuid
import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, KW_ONLY
from enum import Enum, auto
from typing import TypeAlias

from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import (
    QColor, QPainterPath, QTransform, QPen, QBrush,
    QFont, QLinearGradient, QRadialGradient, QGradient,
)

# ── 类型别名 (Python 3.10+) ──────────────────────────────────

ColorTuple: TypeAlias = tuple[int, int, int, int]
PointTuple: TypeAlias = tuple[float, float]


# ── 枚举常量 ────────────────────────────────────────────────

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


class TextType(Enum):
    """文字类型"""
    POINT_TEXT = auto()
    AREA_TEXT = auto()
    PATH_TEXT = auto()


class Justification(Enum):
    """对齐方式"""
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()
    JUSTIFY = auto()


class StrokeCap(Enum):
    """线端点样式"""
    BUTT = auto()
    ROUND = auto()
    SQUARE = auto()


class StrokeJoin(Enum):
    """线连接样式"""
    MITER = auto()
    ROUND = auto()
    BEVEL = auto()


class FillRule(Enum):
    """填充规则"""
    NON_ZERO = auto()
    EVEN_ODD = auto()


class GradientType(Enum):
    """渐变类型"""
    LINEAR = auto()
    RADIAL = auto()


class AnchorPointType(Enum):
    """锚点类型"""
    CORNER = auto()
    SMOOTH = auto()
    ASYMMETRIC = auto()


# ── 渐变系统 ────────────────────────────────────────────────

@dataclass(slots=True)
class GradientStop:
    """渐变色标"""
    position: float     # 0.0 ~ 1.0
    color: QColor
    opacity: float = 1.0


@dataclass
class Gradient:
    """渐变定义"""
    gradient_type: GradientType = GradientType.LINEAR
    stops: list[GradientStop] = field(default_factory=list)
    angle: float = 0.0
    start_point: QPointF = field(default_factory=lambda: QPointF(0, 0))
    end_point: QPointF = field(default_factory=lambda: QPointF(1, 1))
    center: QPointF = field(default_factory=lambda: QPointF(0.5, 0.5))
    radius: float = 0.5

    @staticmethod
    def default_linear() -> Gradient:
        return Gradient(
            stops=[
                GradientStop(0.0, QColor(255, 255, 255)),
                GradientStop(1.0, QColor(0, 0, 0)),
            ],
        )

    @staticmethod
    def default_radial() -> Gradient:
        # 创建默认径向渐变，返回渐变对象
        return Gradient(
            gradient_type=GradientType.RADIAL,
            stops=[
                GradientStop(0.0, QColor(255, 255, 255)),
                GradientStop(1.0, QColor(0, 0, 0)),
            ],
            center=QPointF(0.5, 0.5),
            radius=0.5,
        )

    def to_qgradient(self, rect: QRectF) -> QGradient:
        """根据目标矩形创建 QGradient"""
        if self.gradient_type is GradientType.LINEAR:
            rad = math.radians(self.angle)
            cx, cy = rect.center().x(), rect.center().y()
            half_w, half_h = rect.width() / 2, rect.height() / 2
            dx = math.cos(rad) * half_w
            dy = math.sin(rad) * half_h
            start = QPointF(cx - dx, cy - dy)
            end = QPointF(cx + dx, cy + dy)
            grad = QLinearGradient(start, end)
        else:
            grad = QRadialGradient(
                rect.x() + self.center.x() * rect.width(),
                rect.y() + self.center.y() * rect.height(),
                self.radius * max(rect.width(), rect.height()),
            )
        for stop in self.stops:
            c = QColor(stop.color)
            c.setAlphaF(stop.opacity)
            # 在渐变对象的指定位置设置颜色
            grad.setColorAt(stop.position, c)
        return grad


# ── 贝塞尔曲线锚点 ──────────────────────────────────────────

@dataclass(slots=True)
class AnchorPoint:
    """贝塞尔曲线锚点（含两个控制手柄）
    
    对照 Adobe Illustrator 锚点行为：
    - CORNER（角点）：handle_in 和 handle_out 独立控制，方向任意
    - SMOOTH（平滑点）：handle_in 和 handle_out 共线等距，保持对称
    - ASYMMETRIC（不对称点）：handle_in 和 handle_out 共线但不等距
    
    handle_in/out 存储的是相对于锚点的偏移量。
    例如：锚点在 (100,100)，handle_out = (50, -30)，则手柄在世界空间位于 (150, 70)
    """
    x: float = 0.0
    y: float = 0.0
    handle_in: QPointF | None = None
    handle_out: QPointF | None = None
    anchor_type: AnchorPointType = AnchorPointType.CORNER

    @property
    def pos(self) -> QPointF:
        return QPointF(self.x, self.y)

    @property
    def has_handles(self) -> bool:
        """是否有贝塞尔手柄"""
        return self.handle_in is not None or self.handle_out is not None

    def handle_in_abs(self) -> QPointF | None:
        """获取 handle_in 的绝对世界坐标"""
        if self.handle_in is None:
            return None
        return QPointF(self.x + self.handle_in.x(), self.y + self.handle_in.y())

    def handle_out_abs(self) -> QPointF | None:
        """获取 handle_out 的绝对世界坐标"""
        if self.handle_out is None:
            return None
        return QPointF(self.x + self.handle_out.x(), self.y + self.handle_out.y())

    def copy(self) -> AnchorPoint:
        return AnchorPoint(
            self.x, self.y,
            QPointF(self.handle_in) if self.handle_in else None,
            QPointF(self.handle_out) if self.handle_out else None,
            self.anchor_type,
        )

    # ── 锚点类型转换（对照 AI 的 Convert Anchor Point Tool 行为）──

    def convert_to_corner(self):
        """转换为角点：保留现有手柄但允许独立控制
        
        在 AI 中，Convert Anchor Point Tool 点击平滑点会变为角点
        （手柄保留但不再受对称约束）
        """
        self.anchor_type = AnchorPointType.CORNER

    def convert_to_smooth(self):
        """转换为平滑点：使两个手柄共线等距
        
        在 AI 中，Convert Anchor Point Tool 拖拽角点会拉出手柄并转为平滑点。
        如果只有一个手柄，则镜像生成另一个。
        如果两个手柄都存在，则让它们共线且等距。
        """
        if self.handle_in is None and self.handle_out is None:
            # 没有手柄：不创建（需要在工具层拖拽创建）
            self.anchor_type = AnchorPointType.SMOOTH
            return
        
        if self.handle_in is None and self.handle_out is not None:
            # 只有 handle_out：镜像生成 handle_in
            self.handle_in = QPointF(-self.handle_out.x(), -self.handle_out.y())
        elif self.handle_out is None and self.handle_in is not None:
            # 只有 handle_in：镜像生成 handle_out
            self.handle_out = QPointF(-self.handle_in.x(), -self.handle_in.y())
        else:
            # 两个都有：让它们共线等距
            # 取两个手柄的平均方向，让它们等距分布
            in_len = math.sqrt(self.handle_in.x()**2 + self.handle_in.y()**2)
            out_len = math.sqrt(self.handle_out.x()**2 + self.handle_out.y()**2)
            avg_len = (in_len + out_len) / 2.0 if (in_len > 0 and out_len > 0) else max(in_len, out_len)
            if out_len > 0:
                dx = self.handle_out.x()
                dy = self.handle_out.y()
                ol = math.sqrt(dx*dx + dy*dy)
                if ol > 0.001:
                    dx, dy = dx / ol, dy / ol
                    self.handle_out = QPointF(dx * avg_len, dy * avg_len)
                    self.handle_in = QPointF(-dx * avg_len, -dy * avg_len)
        
        self.anchor_type = AnchorPointType.SMOOTH
        # 将锚点类型设为平滑点

    def enforce_smooth_constraint(self, moved_handle: str):
        # 平滑点约束一当拖拽一个手柄时自动调整另一个手柄保持共线等距(接收被移动手柄标识字符串)
        """平滑点约束：当拖拽一个手柄时，自动调整另一个手柄保持共线等距
        方法文档字符串：平滑点约束：当拖拽一个手柄时，自动调整另一个手柄保持共线等距
        
        Args:
            moved_handle: 'in' 或 'out'，表示哪个手柄被移动
        """
        if self.anchor_type != AnchorPointType.SMOOTH:
            return
        
        if moved_handle == 'out' and self.handle_out is not None:
            # handle_out 被移动，同步 handle_in
            dx, dy = self.handle_out.x(), self.handle_out.y()
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0.001:
                dx, dy = dx / length, dy / length
                # handle_in 是反方向，等长
                in_len = math.sqrt(
                    self.handle_in.x()**2 + self.handle_in.y()**2
                ) if self.handle_in else length
                # 使用 handle_out 的长度（AI 行为：以拖拽的手柄为准）
                self.handle_in = QPointF(-dx * length, -dy * length)
        
        elif moved_handle == 'in' and self.handle_in is not None:
            # handle_in 被移动，同步 handle_out
            dx, dy = self.handle_in.x(), self.handle_in.y()
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0.001:
                dx, dy = dx / length, dy / length
                self.handle_out = QPointF(-dx * length, -dy * length)

    def remove_handles(self):
        """移除所有手柄，转换为角点（AI：点击角点工具点击锚点）"""
        self.handle_in = None
        self.handle_out = None
        self.anchor_type = AnchorPointType.CORNER

    def to_dict(self) -> dict:
        return {
            "x": self.x, "y": self.y,
            "handle_in": [self.handle_in.x(), self.handle_in.y()] if self.handle_in else None,
            "handle_out": [self.handle_out.x(), self.handle_out.y()] if self.handle_out else None,
            "type": self.anchor_type.name,
        }

    @staticmethod
    def from_dict(data: dict) -> AnchorPoint:
        hi = data.get("handle_in")
        ho = data.get("handle_out")
        return AnchorPoint(
            data.get("x", 0), data.get("y", 0),
            QPointF(hi[0], hi[1]) if hi else None,
            QPointF(ho[0], ho[1]) if ho else None,
            AnchorPointType[data.get("type", "CORNER")],
        )


# ── 样式系统 ────────────────────────────────────────────────

@dataclass(slots=True)
class GraphicStyle:
    """图形样式"""
    fill_color: QColor | None = None
    fill_gradient: Gradient | None = None
    fill_opacity: float = 1.0
    stroke_color: QColor | None = None
    stroke_width: float = 1.0
    stroke_opacity: float = 1.0
    stroke_cap: StrokeCap = StrokeCap.BUTT
    stroke_join: StrokeJoin = StrokeJoin.MITER
    stroke_dash: list[float] = field(default_factory=list)
    fill_rule: FillRule = FillRule.NON_ZERO

    def copy(self) -> GraphicStyle:
        return copy.deepcopy(self)

    def to_qpen(self) -> QPen:
        pen = QPen()
        if self.stroke_color:
            c = QColor(self.stroke_color)
            c.setAlphaF(self.stroke_opacity)
            pen.setColor(c)
        else:
            pen.setColor(QColor(0, 0, 0, 0))
        pen.setWidthF(self.stroke_width)
        pen.setCapStyle(_cap_to_qt(self.stroke_cap))
        pen.setJoinStyle(_join_to_qt(self.stroke_join))
        if self.stroke_dash:
            pen.setStyle(0x02)  # DashLine
            pen.setDashPattern(self.stroke_dash)
        return pen

    def to_qbrush(self) -> QBrush:
        if self.fill_color:
            c = QColor(self.fill_color)
            c.setAlphaF(self.fill_opacity)
            # 返回使用改颜色构造的画刷
            return QBrush(c)
        # 否则返回空画刷
        return QBrush()

    def has_fill(self) -> bool:
        return self.fill_color is not None or self.fill_gradient is not None


def _cap_to_qt(cap: StrokeCap) -> int:
    """将 StrokeCap 转换为 Qt 常量 (match-case, Python 3.10+)"""
    match cap:
        case StrokeCap.BUTT:
            return 0x00
        case StrokeCap.ROUND:
            return 0x01
        case StrokeCap.SQUARE:
            return 0x02


def _join_to_qt(join: StrokeJoin) -> int:
    """将 StrokeJoin 转换为 Qt 常量 (match-case, Python 3.10+)"""
    match join:
        case StrokeJoin.MITER:
            return 0x00
        case StrokeJoin.ROUND:
            return 0x01
        case StrokeJoin.BEVEL:
            return 0x02


@dataclass(slots=True)
class CharacterAttributes:
    """字符属性"""
    font_family: str = "Arial"
    font_size: float = 12.0
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False
    fill_color: QColor | None = None
    tracking: float = 0.0
    leading: float = 0.0
    baseline_shift: float = 0.0

    def to_qfont(self) -> QFont:
        font = QFont(self.font_family, int(self.font_size))
        font.setBold(self.bold)
        font.setItalic(self.italic)
        font.setUnderline(self.underline)
        font.setStrikeOut(self.strikethrough)
        return font


@dataclass(slots=True)
class ParagraphAttributes:
    """段落属性"""
    justification: Justification = Justification.LEFT
    first_line_indent: float = 0.0
    space_before: float = 0.0
    space_after: float = 0.0


# ── 图形项基类 ──────────────────────────────────────────────

class GraphicItem:
    """所有图形项的基类（对应 Ai PageItem）

    使用 __slots__ 优化内存占用
    """
    __slots__ = (
        '_id', 'item_type', 'name', 'visible', 'locked',
        'selected', 'style', '_transform', '_opacity',
        '_blend_mode', '_parent', '_layer',
    )

    def __init__(self, item_type: str = "GraphicItem"):
        self._id = str(uuid.uuid4())
        self.item_type = item_type
        self.name: str = ""
        self.visible: bool = True
        self.locked: bool = False
        self.selected: bool = False
        self.style = GraphicStyle()
        self._transform = QTransform()
        self._opacity: float = 1.0
        self._blend_mode: BlendMode = BlendMode.NORMAL
        self._parent: GroupItem | None = None
        self._layer = None  # Layer | None (避免循环导入，运行时赋值)

    @property
    def id(self) -> str:
        return self._id

    @property
    def opacity(self) -> float:
        return self._opacity

    @opacity.setter
    def opacity(self, value: float):
        # 定义不透明度设置器
        self._opacity = max(0.0, min(1.0, value))

    @property
    def blend_mode(self) -> BlendMode:
        return self._blend_mode

    @blend_mode.setter
    def blend_mode(self, value: BlendMode):
        # 定义混合模式设置器
        self._blend_mode = value

    @property
    def parent(self):
        # 获取父级引用
        return self._parent

    def bounding_rect(self) -> QRectF:
        # 获取包围矩形
        raise NotImplementedError

    def painter_path(self) -> QPainterPath:
        # 获取绘图路径
        raise NotImplementedError

    def contains_point(self, point: QPointF) -> bool:
        # 判断点是否在图形内
        return self.bounding_rect().contains(point)

    def move_by(self, dx: float, dy: float):
        """世界空间平移 —— 不受元素自身旋转/缩放影响
        
        QTransform.translate() 是 PRE-multiply: T_new = Transl(dx,dy) * T_old
        这意味着 (dx,dy) 在 T_old 之前应用，会被后续的旋转/缩放影响。
        
        我们需要 POST-multiply: T_new = T_old * Transl(dx,dy)
        对于行向量 p: p * (T * Transl) = (p * T) + (dx,dy)
        即 m31' = m31 + dx, m32' = m32 + dy
        """
        t = self._transform
        self._transform.setMatrix(
            t.m11(), t.m12(), t.m13(),
            t.m21(), t.m22(), t.m23(),
            t.m31() + dx, t.m32() + dy, t.m33(),
        )

    def rotate(self, angle: float, center: QPointF | None = None):
        """旋转图形 —— Illustrator 标准：绕指定中心点旋转
        
        使用 QTransform 的旋转功能，在已有变换基础上追加旋转。
        注意：center 是世界坐标系中的点。
        
        ★ QTransform 关键约定：
        - translate(dx,dy) 是 PRE-multiply（左乘）: T_new = Transl(dx,dy) * T_old
        - 因此调用 translate(+c) → rotate → translate(-c) 得到:
          T_final = Transl(-c) * Rot * Transl(+c)
        - 对于行向量 p: p * T_final = (p - c) * Rot + c = Rot(p - c) + c ✓
        - 即先减去中心、绕原点旋转、再加回中心。
        """
        if center is None:
            # ★ 修复：从局部坐标计算中心，再映射到世界空间（避免双重变换）
            # bounding_rect() 返回的是 _transform.mapRect(_rect)，已经是世界坐标
            # 不能再对其结果应用 _transform.map()，否则产生双重变换
            local_center = self.painter_path().boundingRect().center()
            center = self._transform.map(local_center)
        # 注意：translate 是 PRE-multiply，所以先 +c，再 rotate，最后 -c
        # T = Transl(-c) * Rot * Transl(+c)
        self._transform.translate(center.x(), center.y())
        self._transform.rotate(angle)
        self._transform.translate(-center.x(), -center.y())
    # 
    def scale(self, sx: float, sy: float, center: QPointF | None = None):
        """缩放图形 —— 绕指定中心点缩放（与 rotate 同样的 PRE-multiply 约定）"""
        if center is None:
            # ★ 修复：从局部坐标计算中心，再映射到世界空间
            local_center = self.painter_path().boundingRect().center()
            center = self._transform.map(local_center)
        # translate 是 PRE-multiply: T = Transl(-c) * Scale * Transl(+c)
        self._transform.translate(center.x(), center.y())
        self._transform.scale(sx, sy)
        self._transform.translate(-center.x(), -center.y())
    
    def to_dict(self) -> dict:
        style = self.style
        fc = style.fill_color
        sc = style.stroke_color
        return {
            "id": self._id,
            "type": self.item_type,
            "name": self.name,
            "visible": self.visible,
            "locked": self.locked,
            "opacity": self._opacity,
            "blend_mode": self._blend_mode.name,
            "fill_color": [fc.red(), fc.green(), fc.blue(), fc.alpha()] if fc else None,
            "fill_opacity": style.fill_opacity,
            "stroke_color": [sc.red(), sc.green(), sc.blue(), sc.alpha()] if sc else None,
            "stroke_width": style.stroke_width,
            "stroke_opacity": style.stroke_opacity,
            "stroke_cap": style.stroke_cap.name,
            "stroke_join": style.stroke_join.name,
            "stroke_dash": style.stroke_dash,
            "transform": {
                "m11": self._transform.m11(), "m12": self._transform.m12(),
                "m13": self._transform.m13(), "m21": self._transform.m21(),
                "m22": self._transform.m22(), "m23": self._transform.m23(),
                "m31": self._transform.m31(), "m32": self._transform.m32(),
                "m33": self._transform.m33(),
            },
        }

    @staticmethod
    def from_dict(data: dict) -> GraphicItem:
        """使用 match-case (Python 3.10+) 进行类型分发"""
        item_type = data.get("type", "GraphicItem")
        match item_type:
            case "PathItem":
                return PathItem.from_dict(data)
            case "RectangleItem":
                return RectangleItem.from_dict(data)
            case "EllipseItem":
                return EllipseItem.from_dict(data)
            case "TextFrame":
                return TextFrame.from_dict(data)
            case "GroupItem":
                return GroupItem.from_dict(data)
            case _:
                item = GraphicItem()
                _apply_base_dict(item, data)
                return item

    def deep_copy(self) -> GraphicItem:
        """深度复制图形项 —— 确保所有属性完全复制"""
        return GraphicItem.from_dict(self.to_dict())


def _apply_base_dict(item: GraphicItem, data: dict):
    """将通用字典数据应用到图形项基类属性上"""
    item._id = data.get("id", str(uuid.uuid4()))
    item.name = data.get("name", "")
    item.visible = data.get("visible", True)
    item.locked = data.get("locked", False)
    item._opacity = data.get("opacity", 1.0)

    fc = data.get("fill_color")
    item.style.fill_color = QColor(*fc) if fc else None
    item.style.fill_opacity = data.get("fill_opacity", 1.0)
    sc = data.get("stroke_color")
    item.style.stroke_color = QColor(*sc) if sc else None
    item.style.stroke_width = data.get("stroke_width", 1.0)
    item.style.stroke_opacity = data.get("stroke_opacity", 1.0)
    item.style.stroke_cap = StrokeCap[data.get("stroke_cap", "BUTT")]
    item.style.stroke_join = StrokeJoin[data.get("stroke_join", "MITER")]
    item.style.stroke_dash = data.get("stroke_dash", [])

    t = data.get("transform", {})
    if t:
        item._transform = QTransform(
            t.get("m11", 1), t.get("m12", 0), t.get("m13", 0),
            t.get("m21", 0), t.get("m22", 1), t.get("m23", 0),
            t.get("m31", 0), t.get("m32", 0), t.get("m33", 1),
        )


# ── 具体图形项 ──────────────────────────────────────────────

class PathItem(GraphicItem):
    """路径项 —— 贝塞尔曲线路径，支持锚点手柄编辑"""

    __slots__ = ('_path', '_points', '_anchors', 'closed')

    def __init__(self):
        super().__init__("PathItem")
        self._path = QPainterPath()
        self._points: list[PointTuple] = []
        self._anchors: list[AnchorPoint] = []
        self.closed: bool = False

    # ── 属性 ──

    @property
    def path_points(self) -> list[PointTuple]:
        return self._points

    @property
    def anchors(self) -> list[AnchorPoint]:
        return self._anchors

    @property
    def anchor_count(self) -> int:
        return len(self._anchors)

    # ── 路径构建 ──

    def set_path_points(self, points: list[PointTuple], closed: bool = False):
        """设置路径点（简单折线）"""
        self._points = points
        self.closed = closed
        self._anchors = [AnchorPoint(x, y) for x, y in points]
        self._build_path()

    def add_point(self, x: float, y: float):
        self._points.append((x, y))
        self._anchors.append(AnchorPoint(x, y))
        self._build_path()

    def add_anchor(self, anchor: AnchorPoint):
        self._anchors.append(anchor)
        self._points.append((anchor.x, anchor.y))
        self._build_path()

    def insert_anchor(self, index: int, anchor: AnchorPoint):
        self._anchors.insert(index, anchor)
        self._points.insert(index, (anchor.x, anchor.y))
        self._build_path()

    def remove_anchor(self, index: int):
        if 0 <= index < len(self._anchors):
            self._anchors.pop(index)
            self._points.pop(index)
            self._build_path()

    # ── 锚点编辑 ──

    def move_anchor(self, index: int, x: float, y: float):
        """移动锚点到新位置，贝塞尔手柄保持相对于锚点的偏移不变
        
        对照 Adobe Illustrator：移动锚点时，handle_in 和 handle_out 
        保持相对于锚点的偏移不变（手柄跟随锚点一起移动）。
        handle_in/out 存储的是相对于锚点的偏移量，所以只需更新锚点坐标。
        """
        if 0 <= index < len(self._anchors):
            self._anchors[index].x = x
            self._anchors[index].y = y
            self._points[index] = (x, y)
            self._build_path()

    def set_handle_in(self, index: int, hx: float, hy: float, 
                       constrain_smooth: bool = True):
        """设置 handle_in 的偏移量
        
        Args:
            constrain_smooth: 如果锚点是平滑类型，是否自动约束 handle_out
        """
        if 0 <= index < len(self._anchors):
            anchor = self._anchors[index]
            anchor.handle_in = QPointF(hx, hy)
            if anchor.anchor_type != AnchorPointType.SMOOTH:
                anchor.anchor_type = AnchorPointType.SMOOTH
            if constrain_smooth:
                anchor.enforce_smooth_constraint('in')
            self._build_path()

    def set_handle_out(self, index: int, hx: float, hy: float,
                        constrain_smooth: bool = True):
        """设置 handle_out 的偏移量
        
        Args:
            constrain_smooth: 如果锚点是平滑类型，是否自动约束 handle_in
        """
        if 0 <= index < len(self._anchors):
            anchor = self._anchors[index]
            anchor.handle_out = QPointF(hx, hy)
            if anchor.anchor_type != AnchorPointType.SMOOTH:
                anchor.anchor_type = AnchorPointType.SMOOTH
            if constrain_smooth:
                anchor.enforce_smooth_constraint('out')
            self._build_path()

    def remove_handles(self, index: int):
        """移除指定锚点的所有手柄（转为角点）"""
        if 0 <= index < len(self._anchors):
            self._anchors[index].remove_handles()
            self._build_path()

    def convert_anchor_type(self, index: int, to_type: AnchorPointType):
        """转换锚点类型（对照 AI 的 Convert Anchor Point Tool）"""
        if 0 <= index < len(self._anchors):
            anchor = self._anchors[index]
            if to_type == AnchorPointType.CORNER:
                anchor.convert_to_corner()
            elif to_type == AnchorPointType.SMOOTH:
                anchor.convert_to_smooth()
            self._build_path()

    # ── 碰撞检测 ──

    def get_anchor_at(self, x: float, y: float, tolerance: float = 5.0) -> int:
        """检测坐标 (x,y) 处的锚点索引，返回 -1 表示未命中
        
        Args:
            tolerance: 命中容差（本地坐标空间中的像素值）
        """
        for i, anchor in enumerate(self._anchors):
            if abs(anchor.x - x) < tolerance and abs(anchor.y - y) < tolerance:
                return i
        return -1

    def get_handle_at(self, x: float, y: float, tolerance: float = 4.0) -> tuple[int, str]:
        """检测坐标 (x,y) 处的手柄，返回 (anchor_index, 'in'|'out') 或 (-1, '')
        
        Args:
            tolerance: 命中容差（本地坐标空间中的像素值）
        """
        for i, anchor in enumerate(self._anchors):
            if anchor.handle_in:
                hx = anchor.x + anchor.handle_in.x()
                hy = anchor.y + anchor.handle_in.y()
                if abs(hx - x) < tolerance and abs(hy - y) < tolerance:
                    return (i, 'in')
            if anchor.handle_out:
                hx = anchor.x + anchor.handle_out.x()
                hy = anchor.y + anchor.handle_out.y()
                if abs(hx - x) < tolerance and abs(hy - y) < tolerance:
                    return (i, 'out')
        return (-1, '')
    # 检测点击位置在路径的哪一段
    def get_segment_at(self, x: float, y: float, 
                        tolerance: float = 4.0) -> int:
        """检测点击位置在路径的哪一段（贝塞尔曲线段）上，返回段起始锚点索引
        
        对照 AI：考虑贝塞尔曲线而非仅直线段。
        对曲线段采样多个点进行距离检测。
        
        Args:
            tolerance: 命中容差
        Returns:
            段起始锚点索引，-1 表示未命中
        """
        if len(self._anchors) < 2:
            return -1
        n = len(self._anchors)
        end = n if self.closed else n - 1
        
        for i in range(end):
            j = (i + 1) % n
            prev = self._anchors[i]
            curr = self._anchors[j]
            
            # 采样贝塞尔曲线段上的点
            samples = self._sample_bezier_segment(prev, curr, num_samples=20)
            
            # 检测点到折线（采样点连接）的距离
            for k in range(len(samples) - 1):
                p1, p2 = samples[k], samples[k + 1]
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                len_sq = dx*dx + dy*dy
                if len_sq < 0.001:
                    dist = math.sqrt((x - p1[0])**2 + (y - p1[1])**2)
                else:
                    t = max(0.0, min(1.0, ((x - p1[0])*dx + (y - p1[1])*dy) / len_sq))
                    closest_x = p1[0] + t * dx
                    closest_y = p1[1] + t * dy
                    dist = math.sqrt((x - closest_x)**2 + (y - closest_y)**2)
                
                if dist < tolerance:
                    return i
        
        return -1

    @staticmethod
    def _sample_bezier_segment(prev: AnchorPoint, curr: AnchorPoint,
                                num_samples: int = 20) -> list[tuple[float, float]]:
        """对一段贝塞尔曲线进行采样，返回采样点列表"""
        points = []
        p0 = (prev.x, prev.y)
        p3 = (curr.x, curr.y)
        
        # 控制点
        if prev.handle_out is not None:
            p1 = (prev.x + prev.handle_out.x(), prev.y + prev.handle_out.y())
        else:
            p1 = p0
        
        if curr.handle_in is not None:
            p2 = (curr.x + curr.handle_in.x(), curr.y + curr.handle_in.y())
        else:
            p2 = p3
        
        # 如果两端都没有手柄，退化为直线
        if prev.handle_out is None and curr.handle_in is None:
            return [p0, p3]
        
        # 三次贝塞尔采样
        for k in range(num_samples + 1):
            t_val = k / num_samples
            # B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
            mt = 1 - t_val
            mt2 = mt * mt
            mt3 = mt2 * mt
            t2 = t_val * t_val
            t3 = t2 * t_val
            
            bx = mt3 * p0[0] + 3 * mt2 * t_val * p1[0] + 3 * mt * t2 * p2[0] + t3 * p3[0]
            by = mt3 * p0[1] + 3 * mt2 * t_val * p1[1] + 3 * mt * t2 * p2[1] + t3 * p3[1]
            points.append((bx, by))
        
        return points

    def get_closest_point_on_segment(self, seg_idx: int, 
                                      x: float, y: float) -> tuple[float, float]:
        """返回路径段上距 (x,y) 最近的点坐标"""
        if seg_idx < 0 or seg_idx >= len(self._anchors):
            return (x, y)
        
        n = len(self._anchors)
        j = (seg_idx + 1) % n
        prev = self._anchors[seg_idx]
        curr = self._anchors[j]
        
        samples = self._sample_bezier_segment(prev, curr, num_samples=50)
        
        best_dist = float('inf')
        best_pt = (x, y)
        
        for k in range(len(samples) - 1):
            p1, p2 = samples[k], samples[k + 1]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            len_sq = dx*dx + dy*dy
            if len_sq < 0.001:
                t = 0.0
            else:
                t = max(0.0, min(1.0, ((x - p1[0])*dx + (y - p1[1])*dy) / len_sq))
                # 计算投影参数t（限制在0到1之间）；计算最近点x坐标；计算最近点y坐标
            closest_x = p1[0] + t * dx
            closest_y = p1[1] + t * dy
            dist = (x - closest_x)**2 + (y - closest_y)**2
            if dist < best_dist:
                best_dist = dist
                best_pt = (closest_x, closest_y)
        
        return best_pt

    # ── 内部 ──

    def _build_path(self):
        """从锚点列表构建 QPainterPath（支持贝塞尔曲线）"""
        self._path = QPainterPath()
        if not self._anchors:
            return
        # 获取第一个锚点
        first = self._anchors[0]
        self._path.moveTo(first.x, first.y)
        for i in range(1, len(self._anchors)):
            self._add_segment(self._anchors[i - 1], self._anchors[i])
        if self.closed and len(self._anchors) > 2:
            self._add_segment(self._anchors[-1], self._anchors[0])
            self._path.closeSubpath()

    def _add_segment(self, prev: AnchorPoint, curr: AnchorPoint):
        """使用 match-case (Python 3.10+) 处理贝塞尔段类型"""
        match (prev.handle_out, curr.handle_in):
            case (out, inp) if out is not None and inp is not None:
                self._path.cubicTo(
                    prev.x + out.x(), prev.y + out.y(),
                    curr.x + inp.x(), curr.y + inp.y(),
                    curr.x, curr.y,
                )
            case (out, _) if out is not None:
                self._path.quadTo(
                    prev.x + out.x(), prev.y + out.y(),
                    curr.x, curr.y,
                )
            case (_, inp) if inp is not None:
                self._path.quadTo(
                    curr.x + inp.x(), curr.y + inp.y(),
                    curr.x, curr.y,
                )
            case _:
                self._path.lineTo(curr.x, curr.y)

    def _rebuild_from_anchors(self):
        # 从锚点列表重建点列表和绘图路径
        self._points = [(a.x, a.y) for a in self._anchors]
        self._build_path()

    # ── GraphicItem 接口 ──

    def painter_path(self) -> QPainterPath:
        return self._path

    def bounding_rect(self) -> QRectF:
        return self._transform.mapRect(self._path.boundingRect())

    def contains_point(self, point: QPointF) -> bool:
        # 判断点是否在路径内（将点击点逆变换到局部坐标系）
        local_point = self._transform.inverted()[0].map(point)
        return self._path.contains(local_point)

    def deep_copy(self) -> GraphicItem:
        """PathItem 深度复制 —— 直接拷贝 _path 避免序列化丢失

        对照 Adobe Illustrator：路径查找器操作后的复杂路径（布尔运算结果）
        可能没有对应的 _anchors/_points 列表，无法通过 to_dict/from_dict
        序列化链路正确恢复。因此重写 deep_copy 直接进行内存级拷贝。
        """
        item = PathItem()
        # 复制基类属性（不走 to_dict/from_dict 序列化）
        item._id = str(uuid.uuid4())
        item.name = self.name
        item.visible = self.visible
        item.locked = self.locked
        item.selected = False  # 复制出来的项默认不选中
        item._opacity = self._opacity
        item._blend_mode = self._blend_mode
        item.style = self.style.copy()
        item._transform = QTransform(self._transform)
        # 复制 PathItem 特有属性
        item._path = QPainterPath(self._path)       # QPainterPath 深拷贝
        item._points = list(self._points)            # (x, y) 列表浅拷贝即可
        item._anchors = [a.copy() for a in self._anchors]
        item.closed = self.closed
        return item

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["points"] = self._points
        d["closed"] = self.closed
        d["anchors"] = [a.to_dict() for a in self._anchors]
        # 当 _anchors 为空但 _path 有效时（如路径查找器结果），
        # 额外保存 SVG 路径字符串以便反序列化恢复
        if not self._anchors and not self._path.isEmpty():
            # QPainterPath → SVG path data (Qt 6 原生支持)
            try:
                from PyQt5.QtSvg import QGraphicsSvgItem
                raise ImportError  # PyQt5 没有 QPainterPath.toSvgString
            except ImportError:
                # 回退：遍历路径元素，序列化为坐标列表
                elements = []
                n = self._path.elementCount()
                for i in range(n):
                    e = self._path.elementAt(i)
                    if e.isMoveTo():
                        elements.append([0, e.x, e.y])
                    elif e.isLineTo():
                        elements.append([1, e.x, e.y])
                    elif e.isCurveTo():
                        elements.append([2, e.x, e.y])
                if elements:
                    d["_raw_path_elements"] = elements
        return d

    @staticmethod
    def from_dict(data: dict) -> PathItem:
        item = PathItem()
        _apply_base_dict(item, data)
        item._points = data.get("points", [])
        item.closed = data.get("closed", False)
        anchors_data = data.get("anchors", [])
        raw_elements = data.get("_raw_path_elements", [])

        if anchors_data:
            item._anchors = [AnchorPoint.from_dict(a) for a in anchors_data]
            item._build_path()
        elif raw_elements:
            # 从序列化的路径元素恢复（路径查找器结果等）
            item._path = QPainterPath()
            for elem in raw_elements:
                t = elem[0]
                if t == 0:  # MoveTo
                    item._path.moveTo(elem[1], elem[2])
                elif t == 1:  # LineTo
                    item._path.lineTo(elem[1], elem[2])
                elif t == 2:  # CubicTo
                    item._path.lineTo(elem[1], elem[2])
            # 同时填充 _points 以便可能的后续编辑
            if raw_elements:
                item._points = [(e[1], e[2]) for e in raw_elements if e[0] != 2] or \
                               [(raw_elements[0][1], raw_elements[0][2])]
                item._anchors = [AnchorPoint(x, y) for x, y in item._points]
            item.closed = data.get("closed", True)  # 布尔运算结果通常是闭合的
        else:
            item._anchors = [AnchorPoint(x, y) for x, y in item._points]
            item._build_path()
        return item


class RectangleItem(GraphicItem):
    """矩形项"""

    __slots__ = ('_rect', '_corner_radius')

    def __init__(self, x: float = 0, y: float = 0, w: float = 100, h: float = 100):
        super().__init__("RectangleItem")
        self._rect = QRectF(x, y, w, h)
        self._corner_radius: float = 0.0

    @property
    def rect(self) -> QRectF:
        # 只读属性，获取矩形
        return self._rect

    @rect.setter
    def rect(self, value: QRectF):
        # 定义矩形设置器(接收矩形参数)
        self._rect = value

    @property
    def corner_radius(self) -> float:
        return self._corner_radius

    @corner_radius.setter
    def corner_radius(self, value: float):
        # 定义圆角半径设置器
        self._corner_radius = max(0, value)

    def painter_path(self) -> QPainterPath:
        # 重写实例方法，获取绘图路径
        path = QPainterPath()
        if self._corner_radius > 0:
            path.addRoundedRect(self._rect, self._corner_radius, self._corner_radius)
        else:
            path.addRect(self._rect)
        return path

    def bounding_rect(self) -> QRectF:
        # 获取变换后的包围矩形
        return self._transform.mapRect(self._rect)

    def contains_point(self, point: QPointF) -> bool:
        # 判断点是否在矩形内（将点击点逆变换到局部坐标系）
        local_point = self._transform.inverted()[0].map(point)
        return self.painter_path().contains(local_point)

    def to_dict(self) -> dict:
        # 重写实例方法，序列化为字典，调用父类的序列化方法获取基础字典
        d = super().to_dict()
        # 更新字典，添加矩形x,y坐标，添加矩形宽度和高度，添加圆角半径
        d.update(x=self._rect.x(), y=self._rect.y(),
                 width=self._rect.width(), height=self._rect.height(),
                 corner_radius=self._corner_radius)
        return d

    @staticmethod
    def from_dict(data: dict) -> RectangleItem:
        # 反序列化
        item = RectangleItem()
        _apply_base_dict(item, data)
        item._rect = QRectF(
            data.get("x", 0), data.get("y", 0),
            data.get("width", 100), data.get("height", 100),
        )
        item._corner_radius = data.get("corner_radius", 0.0)
        return item


class EllipseItem(GraphicItem):
    """椭圆项"""

    __slots__ = ('_rect',)

    def __init__(self, x: float = 0, y: float = 0, w: float = 100, h: float = 100):
        super().__init__("EllipseItem")
        self._rect = QRectF(x, y, w, h)

    @property
    def rect(self) -> QRectF:
        return self._rect

    @rect.setter
    def rect(self, value: QRectF):
        self._rect = value

    def painter_path(self) -> QPainterPath:
        # 获取绘图路径
        path = QPainterPath()
        path.addEllipse(self._rect)
        # 在矩形区域内添加椭圆
        return path

    def bounding_rect(self) -> QRectF:
        # 重写实例方法，获取变换后的包围矩形
        return self._transform.mapRect(self._rect)

    def contains_point(self, point: QPointF) -> bool:
        # 使用椭圆方程判断点是否在椭圆内（将点击点逆变换到局部坐标系）
        local_point = self._transform.inverted()[0].map(point)
        cx = self._rect.center().x()
        cy = self._rect.center().y()
        rx = self._rect.width() / 2
        ry = self._rect.height() / 2
        if rx == 0 or ry == 0:
            return False
        # 使用椭圆标准方程判断是否在椭圆内
        return ((local_point.x() - cx) ** 2 / rx ** 2 + (local_point.y() - cy) ** 2 / ry ** 2) <= 1

    def to_dict(self) -> dict:
        d = super().to_dict()
        # 更新字典：添加外接矩形
        d.update(x=self._rect.x(), y=self._rect.y(),
                 width=self._rect.width(), height=self._rect.height())
        # 返回完整的序列化字典
        return d
    # 从字典反序列化为椭圆项
    @staticmethod
    def from_dict(data: dict) -> EllipseItem:
        # 
        item = EllipseItem()
        _apply_base_dict(item, data)
        item._rect = QRectF(
            data.get("x", 0), data.get("y", 0),
            data.get("width", 100), data.get("height", 100),
        )
        return item


class TextFrame(GraphicItem):
    """文本框"""

    __slots__ = ('_rect', '_contents', '_text_type', 'char_attrs', 'para_attrs')

    def __init__(self, x: float = 0, y: float = 0):
        super().__init__("TextFrame")
        self._rect = QRectF(x, y, 200, 30)
        self._contents: str = ""
        self._text_type: TextType = TextType.POINT_TEXT
        self.char_attrs = CharacterAttributes()
        self.para_attrs = ParagraphAttributes()

    @property
    def contents(self) -> str:
        return self._contents

    @contents.setter
    def contents(self, value: str):
        # 定义文本内容设置器
        self._contents = value

    @property
    def text_type(self) -> TextType:
        # 文字类型
        return self._text_type

    @property
    def rect(self) -> QRectF:
        return self._rect

    @rect.setter
    def rect(self, value: QRectF):
        # 文本框矩形
        self._rect = value

    def painter_path(self) -> QPainterPath:
        # 获取绘图路径
        path = QPainterPath()
        path.addRect(self._rect)
        return path

    def bounding_rect(self) -> QRectF:
        # 重写实例方法，获取变换后的包围矩形
        return self._transform.mapRect(self._rect)

    def contains_point(self, point: QPointF) -> bool:
        # 将点击点逆变换到局部坐标系
        local_point = self._transform.inverted()[0].map(point)
        return self._rect.contains(local_point)

    def to_dict(self) -> dict:
        d = super().to_dict()
        # 问题3修复：序列化 char_attrs.fill_color
        tfc = self.char_attrs.fill_color
        d.update(
            x=self._rect.x(), y=self._rect.y(),
            width=self._rect.width(), height=self._rect.height(),
            contents=self._contents,
            text_type=self._text_type.name,
            font_family=self.char_attrs.font_family,
            font_size=self.char_attrs.font_size,
            bold=self.char_attrs.bold,
            italic=self.char_attrs.italic,
            underline=self.char_attrs.underline,
            tracking=self.char_attrs.tracking,
            leading=self.char_attrs.leading,
            text_fill_color=[tfc.red(), tfc.green(), tfc.blue(), tfc.alpha()] if tfc else None,
            justification=self.para_attrs.justification.name,
        )
        return d

    @staticmethod
    def from_dict(data: dict) -> TextFrame:
        item = TextFrame()
        _apply_base_dict(item, data)
        item.item_type = "TextFrame"
        item._rect = QRectF(
            data.get("x", 0), data.get("y", 0),
            data.get("width", 200), data.get("height", 30),
        )
        item._contents = data.get("contents", "")
        item.char_attrs.font_family = data.get("font_family", "Arial")
        item.char_attrs.font_size = data.get("font_size", 12.0)
        item.char_attrs.bold = data.get("bold", False)
        item.char_attrs.italic = data.get("italic", False)
        item.char_attrs.underline = data.get("underline", False)
        item.char_attrs.tracking = data.get("tracking", 0.0)
        item.char_attrs.leading = data.get("leading", 0.0)
        # 恢复文本填充颜色
        tfc = data.get("text_fill_color")
        item.char_attrs.fill_color = QColor(*tfc) if tfc else None
        # 恢复段落属性
        just_name = data.get("justification", "LEFT")
        item.para_attrs.justification = Justification[just_name]
        return item


class GroupItem(GraphicItem):
    """编组"""

    __slots__ = ('_items',)

    def __init__(self):
        super().__init__("GroupItem")
        self._items: list[GraphicItem] = []

    @property
    def items(self) -> list[GraphicItem]:
        return self._items

    def add_item(self, item: GraphicItem):
        # 将子项的父级引用设为当前组
        item._parent = self
        self._items.append(item)

    def remove_item(self, item: GraphicItem):
        if item in self._items:
            item._parent = None
            self._items.remove(item)

    def painter_path(self) -> QPainterPath:
        path = QPainterPath()
        for item in self._items:
            if item.visible:
                path.addPath(item.painter_path())
        return path
    # 获取所有子项的合并包围矩形
    def bounding_rect(self) -> QRectF:
        if not self._items:
            return QRectF()
        rect = self._items[0].bounding_rect()
        for item in self._items[1:]:
            rect = rect.united(item.bounding_rect())
        return rect

    def contains_point(self, point: QPointF) -> bool:
        return any(item.contains_point(point) for item in self._items)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["items"] = [item.to_dict() for item in self._items]
        return d

    @staticmethod
    def from_dict(data: dict) -> GroupItem:
        item = GroupItem()
        _apply_base_dict(item, data)
        item.item_type = "GroupItem"
        item._items = [GraphicItem.from_dict(i) for i in data.get("items", [])]
        for sub in item._items:
            sub._parent = item
        return item


# ── 色板 ────────────────────────────────────────────────────

@dataclass(slots=True)
class Swatch:
    """色板"""
    name: str
    color: QColor

    @staticmethod
    def default_swatches() -> list[Swatch]:
        colors = [
            ("黑色", QColor(0, 0, 0)),
            ("白色", QColor(255, 255, 255)),
            ("红色", QColor(255, 0, 0)),
            ("绿色", QColor(0, 255, 0)),
            ("蓝色", QColor(0, 0, 255)),
            ("黄色", QColor(255, 255, 0)),
            ("青色", QColor(0, 255, 255)),
            ("品红", QColor(255, 0, 255)),
            ("灰色", QColor(128, 128, 128)),
            ("橙色", QColor(255, 165, 0)),
            ("紫色", QColor(128, 0, 128)),
            ("棕色", QColor(139, 69, 19)),
            ("粉色", QColor(255, 192, 203)),
            ("深蓝", QColor(0, 0, 139)),
            ("森林绿", QColor(34, 139, 34)),
            ("金色", QColor(255, 215, 0)),
        ]
        return [Swatch(name, color) for name, color in colors]


# ── 命令模式（撤销/重做） ──────────────────────────────────

class Command(ABC):
    """可撤销的命令基类（抽象基类）"""
    __slots__ = ()

    @abstractmethod
    def execute(self):
        ...

    @abstractmethod
    def undo(self):
        ...

    def description(self) -> str:
        return "操作"


class AddItemCommand(Command):
    """添加图形项"""
    __slots__ = ('document', 'item', 'layer')

    def __init__(self, document, item, layer):
        self.document = document
        self.item = item
        self.layer = layer

    def execute(self):
        self.layer.add_item(self.item)

    def undo(self):
        self.layer.remove_item(self.item)

    def description(self) -> str:
        return f"添加 {self.item.item_type}"


class RemoveItemCommand(Command):
    """删除图形项"""
    __slots__ = ('document', 'item', 'layer')

    def __init__(self, document, item, layer):
        self.document = document
        self.item = item
        self.layer = layer

    def execute(self):
        self.layer.remove_item(self.item)

    def undo(self):
        self.layer.add_item(self.item)

    def description(self) -> str:
        return f"删除 {self.item.item_type}"


class CompoundPathfinderCommand(Command):
    """路径查找器复合命令 —— 一次操作包含删除多个旧项 + 添加一个结果项

    对照 Adobe Illustrator：路径查找器操作应作为一个整体支持一步撤销。
    内部维护旧项列表及其所在图层，撤销时恢复旧项并移除结果项。
    """
    __slots__ = ('document', 'old_items', 'result_item', 'mode')

    def __init__(self, document, old_items: list[tuple], result_item, mode: str):
        """Args:
            document: Document 实例
            old_items: [(GraphicItem, Layer), ...] 原始对象及其所在图层
            result_item: 布尔运算结果对象
            mode: 运算模式 ('union'/'intersect'/'subtract')
        """
        self.document = document
        self.old_items = old_items
        self.result_item = result_item
        self.mode = mode

    def execute(self):
        """执行：移除所有旧项，添加结果项"""
        for item, layer in self.old_items:
            layer.remove_item(item)
        # 结果项添加到第一个旧项所在的图层（活动图层）
        if self.old_items:
            _, layer = self.old_items[0]
            layer.add_item(self.result_item)
        else:
            self.document.active_layer.add_item(self.result_item)

    def undo(self):
        """撤销：移除结果项，恢复所有旧项"""
        # 找到结果项所在图层并移除
        for layer in self.document._layers:
            if self.result_item in layer.items:
                layer.remove_item(self.result_item)
                break
        # 恢复所有旧项
        for item, layer in self.old_items:
            layer.add_item(item)

    def description(self) -> str:
        mode_names = {"union": "联集", "intersect": "交集", "subtract": "减去顶层"}
        return f"路径查找器 - {mode_names.get(self.mode, self.mode)}"


class MoveItemsCommand(Command):
    """移动图形项
    
    支持两种使用模式：
    1. 延迟执行：先创建命令，execute() 中执行实际移动（如方向键微调）
    2. 即时执行：移动已在外部完成（如鼠标拖拽），通过 already_moved=True 跳过 execute()
    """
    __slots__ = ('document', 'items', 'dx', 'dy', '_already_moved')

    def __init__(self, document, items, dx, dy, already_moved: bool = False):
        self.document = document
        self.items = items
        self.dx = dx
        self.dy = dy
        self._already_moved = already_moved

    def execute(self):
        """执行移动操作（如果尚未移动）"""
        if not self._already_moved:
            for item in self.items:
                item.move_by(self.dx, self.dy)

    def undo(self):
        """撤销移动"""
        for item in self.items:
            item.move_by(-self.dx, -self.dy)

    def description(self) -> str:
        return f"移动 ({self.dx:.0f}, {self.dy:.0f})"


class ChangeStyleCommand(Command):
    """修改样式"""
    __slots__ = ('document', 'item', 'old_style', 'new_style')

    def __init__(self, document, item, old_style, new_style):
        self.document = document
        self.item = item
        self.old_style = old_style
        self.new_style = new_style

    def execute(self):
        self.item.style = self.new_style

    def undo(self):
        self.item.style = self.old_style

    def description(self) -> str:
        return "修改样式"


class ModifyAnchorCommand(Command):
    """修改贝塞尔锚点"""
    __slots__ = ('document', 'item', 'old_anchors', 'new_anchors')

    def __init__(self, document, item, old_anchors, new_anchors):
        self.document = document
        self.item = item
        self.old_anchors = old_anchors
        self.new_anchors = new_anchors

    def execute(self):
        self.item._anchors = [a.copy() for a in self.new_anchors]
        self.item._rebuild_from_anchors()

    def undo(self):
        self.item._anchors = [a.copy() for a in self.old_anchors]
        self.item._rebuild_from_anchors()

    def description(self) -> str:
        return "修改锚点"


class ResizeItemCommand(Command):
    """缩放图形项命令"""
    __slots__ = ('document', 'item', 'old_rect', 'new_rect')

    def __init__(self, document, item, old_rect: QRectF, new_rect: QRectF):
        self.document = document
        self.item = item
        self.old_rect = QRectF(old_rect)
        self.new_rect = QRectF(new_rect)

    def execute(self):
        # 缩放已在 _apply_resize (mouse_move) 中实时完成，此处仅记录命令用于撤销
        pass

    def undo(self):
        self._apply_rect(self.old_rect)

    def description(self) -> str:
        return "缩放"

    def _apply_rect(self, target: QRectF):
        """根据目标矩形恢复尺寸"""
        item = self.item
        scale_x = target.width() / max(self.old_rect.width(), 0.001) if self.old_rect.width() > 0 else 1
        scale_y = target.height() / max(self.old_rect.height(), 0.001) if self.old_rect.height() > 0 else 1

        if isinstance(item, RectangleItem):
            item.rect = QRectF(target.x(), target.y(), target.width(), target.height())
        elif isinstance(item, EllipseItem):
            item.rect = QRectF(target.x(), target.y(), target.width(), target.height())
        elif isinstance(item, PathItem):
            ref_x = target.x() if scale_x > 0 else target.right()
            ref_y = target.y() if scale_y > 0 else target.bottom()
            for anchor in item.anchors:
                anchor.x = ref_x + (anchor.x - ref_x) * scale_x
                anchor.y = ref_y + (anchor.y - ref_y) * scale_y
                if anchor.handle_in:
                    anchor.handle_in = QPointF(
                        anchor.handle_in.x() * scale_x,
                        anchor.handle_in.y() * scale_y,
                    )
                if anchor.handle_out:
                    anchor.handle_out = QPointF(
                        anchor.handle_out.x() * scale_x,
                        anchor.handle_out.y() * scale_y,
                    )
            item._rebuild_from_anchors()
        elif isinstance(item, TextFrame):
            item.rect = QRectF(target.x(), target.y(), target.width(), target.height())


class CommandHistory:
    """命令历史（撤销/重做管理）"""
    __slots__ = ('_undo_stack', '_redo_stack', '_max_size')

    def __init__(self, max_size: int = 100):
        self._undo_stack: list[Command] = []
        self._redo_stack: list[Command] = []
        self._max_size = max_size

    def execute(self, command: Command):
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()
        if len(self._undo_stack) > self._max_size:
            self._undo_stack.pop(0)

    def undo(self) -> Command | None:
        if not self._undo_stack:
            return None
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        return command

    def redo(self) -> Command | None:
        if not self._redo_stack:
            return None
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
        return command

    @property
    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0

    @property
    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0

    @property
    def undo_description(self) -> str:
        return self._undo_stack[-1].description() if self._undo_stack else ""

    @property
    def redo_description(self) -> str:
        return self._redo_stack[-1].description() if self._redo_stack else ""

    def clear(self):
        self._undo_stack.clear()
        self._redo_stack.clear()
