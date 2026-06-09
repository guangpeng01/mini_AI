"""
工具系统 (Python 3.10+) —— 选择、矩形、椭圆、钢笔、文字工具

架构优化:
- 使用 __slots__ 减少内存占用
- 使用 X | None 替代 Optional[X]
- 使用 match-case 替代 if-elif 链
- 使用 @override 风格注释 (PEP 698 ready)
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from enum import Enum, auto

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen

from .graphics import (
    GraphicItem, RectangleItem, EllipseItem, TextFrame,
    PathItem, GraphicStyle, AnchorPoint, AnchorPointType,
    Command, MoveItemsCommand, ModifyAnchorCommand, ResizeItemCommand,
)
from .document import Document, Layer


class ToolType(Enum):
    """工具类型"""
    SELECTION = auto()              # 选择工具 (V)
    DIRECT_SELECT = auto()          # 直接选择工具 (A)
    RECTANGLE = auto()              # 矩形工具 (M)
    ELLIPSE = auto()                # 椭圆工具 (L)
    PEN = auto()                    # 钢笔工具 (P)
    ADD_ANCHOR = auto()             # 添加锚点工具 (+)
    DELETE_ANCHOR = auto()          # 删除锚点工具 (-)
    CONVERT_ANCHOR = auto()         # 转换锚点工具 (Shift+C)
    TEXT = auto()                   # 文字工具 (T)
    HAND = auto()                   # 抓手工具 (H)
    ZOOM = auto()                   # 缩放工具 (Z)


class BaseTool(ABC):
    """工具基类（抽象）"""
    __slots__ = ('tool_type', '_document', '_is_drawing')

    def __init__(self, tool_type: ToolType):
        self.tool_type = tool_type
        self._document: Document | None = None
        self._is_drawing: bool = False

    def set_document(self, doc: Document):
        # 将传入的文档赋值给实例的私有文档引用
        self._document = doc

    @property
    def document(self) -> Document | None:
        return self._document

    def mouse_press(self, pos: QPointF, modifiers: int):
        pass

    def mouse_move(self, pos: QPointF, modifiers: int):
        pass

    def mouse_release(self, pos: QPointF, modifiers: int):
        pass

    def mouse_double_click(self, pos: QPointF, modifiers: int):
        pass

    def key_press(self, key: int, modifiers: int):
        pass

    def draw_preview(self, painter: QPainter, editing_text=None):
        pass

    def cancel(self):
        self._is_drawing = False


# ── 缩放手柄类型 ───────────────────────────────────────────

class ResizeHandleType(Enum):
    """缩放手柄位置类型"""
    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()
    MIDDLE_LEFT = auto()
    MIDDLE_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_RIGHT = auto()


# ── 选择工具 ──────────────────────────────────────────────

class SelectionTool(BaseTool):
    """选择工具 —— 点击选择 / 框选 / 多选拖拽 / 缩放 / 旋转"""
    __slots__ = ('_drag_start', '_drag_current', '_dragging_item',
                 '_drag_offset', '_is_marquee',
                 '_dragging_items', '_drag_offsets',
                 '_total_dx', '_total_dy',
                 '_is_scaling', '_scale_handle',
                 '_scale_orig_rect', '_scale_orig_br',
                 '_scale_pivot', '_scale_keep_ratio',
                 '_is_rotating', '_rotation_center',
                 '_rotation_start_angle')

    def __init__(self):
        super().__init__(ToolType.SELECTION)
        self._drag_start: QPointF | None = None
        self._drag_current: QPointF | None = None
        self._dragging_item: GraphicItem | None = None
        self._drag_offset = QPointF(0, 0)
        self._is_marquee: bool = False
        # 多选拖拽支持
        self._dragging_items: list[GraphicItem] = []
        self._drag_offsets: list[QPointF] = []
        self._total_dx: float = 0.0
        self._total_dy: float = 0.0
        # 缩放支持
        self._is_scaling: bool = False
        self._scale_handle: ResizeHandleType | None = None
        self._scale_orig_rect = QRectF()
        self._scale_orig_br = QRectF()  # 缩放前 bounding_rect
        self._scale_pivot = QPointF()   # 缩放锚点（对角的那个固定点）
        self._scale_keep_ratio: bool = False
        # 问题4：旋转支持
        self._is_rotating: bool = False
        self._rotation_center = QPointF()
        self._rotation_start_angle: float = 0.0

    # ── 手柄检测 ──

    ROTATE_HANDLE_DISTANCE = 30  # 旋转手柄距离选中框顶部的距离（像素）

    @staticmethod
    def _get_handle_at(item: GraphicItem, pos: QPointF, tolerance: float = 8) -> ResizeHandleType | None:
        """检测鼠标是否在缩放手柄上（pos 为世界坐标，使用变换后的实际角点）"""
        # 获取变换后的四个角点
        local_rect = item.painter_path().boundingRect()
        tl = item._transform.map(local_rect.topLeft())
        tr = item._transform.map(local_rect.topRight())
        bl = item._transform.map(local_rect.bottomLeft())
        br = item._transform.map(local_rect.bottomRight())
        hs = tolerance  # 手柄命中容差
        corners = {
            ResizeHandleType.TOP_LEFT: tl,
            ResizeHandleType.TOP_RIGHT: tr,
            ResizeHandleType.BOTTOM_LEFT: bl,
            ResizeHandleType.BOTTOM_RIGHT: br,
        }
        edges = {
            ResizeHandleType.TOP_CENTER: QPointF((tl.x() + tr.x()) / 2, (tl.y() + tr.y()) / 2),
            ResizeHandleType.BOTTOM_CENTER: QPointF((bl.x() + br.x()) / 2, (bl.y() + br.y()) / 2),
            ResizeHandleType.MIDDLE_LEFT: QPointF((tl.x() + bl.x()) / 2, (tl.y() + bl.y()) / 2),
            ResizeHandleType.MIDDLE_RIGHT: QPointF((tr.x() + br.x()) / 2, (tr.y() + br.y()) / 2),
        }

        for htype, pt in corners.items():
            if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:
                return htype
        for htype, pt in edges.items():
            if abs(pos.x() - pt.x()) < hs and abs(pos.y() - pt.y()) < hs:
                return htype
        return None

    @staticmethod
    def _is_on_rotate_handle(item: GraphicItem, pos: QPointF, tolerance: float = 8) -> bool:
        """检测鼠标是否在旋转手柄上（pos 为世界坐标，使用变换后的实际角点）
        旋转手柄位于选中框顶部中心的上方
        """
        local_rect = item.painter_path().boundingRect()
        tl = item._transform.map(local_rect.topLeft())
        tr = item._transform.map(local_rect.topRight())
        # 顶部中心：使用变换后的左上和右上角点的中点
        top_center = QPointF((tl.x() + tr.x()) / 2, (tl.y() + tr.y()) / 2)
        # 旋转手柄位于顶部中心上方
        rotate_center = QPointF(top_center.x(), top_center.y() - SelectionTool.ROTATE_HANDLE_DISTANCE)
        return abs(pos.x() - rotate_center.x()) < tolerance and abs(pos.y() - rotate_center.y()) < tolerance

    # ── 鼠标事件 ──

    def mouse_press(self, pos: QPointF, modifiers: int):
        if not self._document:
            return
        self._drag_start = QPointF(pos)
        self._drag_current = QPointF(pos)
        self._total_dx = 0.0
        self._total_dy = 0.0
        self._is_scaling = False
        self._scale_handle = None
        self._scale_keep_ratio = bool(modifiers & Qt.ShiftModifier)
        self._is_rotating = False

        # 检查是否点击了已选中项的缩放手柄；检查是否点击了已选中图形项的缩放手柄
        sel = self._document.get_selection()
        if len(sel) == 1:
            # 问题4：优先检测旋转手柄
            if self._is_on_rotate_handle(sel[0], pos):
                self._dragging_item = sel[0]
                self._is_rotating = True
                # 旋转中心使用变换后的实际中心（世界坐标）
                local_rect = sel[0].painter_path().boundingRect()
                self._rotation_center = sel[0]._transform.map(local_rect.center())
                self._rotation_start_angle = math.atan2(
                    pos.y() - self._rotation_center.y(),
                    pos.x() - self._rotation_center.x()
                )
                return

            handle = self._get_handle_at(sel[0], pos)
            if handle is not None:
                self._dragging_item = sel[0]
                self._is_scaling = True
                self._scale_handle = handle
                # 使用世界坐标系的 bounding_rect（已含 item 变换）
                world_rect = sel[0].bounding_rect()
                self._scale_orig_rect = QRectF(world_rect)
                self._scale_orig_br = QRectF(world_rect)
                # 缩放的固定锚点是对角；缩放的固定锚点为对角位置
                self._scale_pivot = self._get_opposite_corner(handle, self._scale_orig_rect)
                return
    
        item = self._document.get_item_at(pos.x(), pos.y())
        if item:
            self._is_marquee = False  # 点击了物体，不是框选
            # 如果点击的项未被选中，先清除选择并选中它
            if not item.selected:
                if not (modifiers & Qt.ShiftModifier):
                    self._document.clear_selection()
                item.selected = True
            
            # 准备拖拽
            sel = self._document.get_selection()
            if len(sel) > 1:
                # 多选状态 → 多选拖拽模式
                self._dragging_items = list(sel)
                self._drag_offsets = [pos - it.bounding_rect().topLeft() for it in sel]
                self._dragging_item = None
            else:
                # 单选或仅选中了一项 → 单项拖拽（不要清除再重新选中）
                self._dragging_item = item
                self._drag_offset = pos - item.bounding_rect().topLeft()
                self._dragging_items = []
        else:
            if not (modifiers & Qt.ShiftModifier):
                self._document.clear_selection()
            self._dragging_item = None
            self._dragging_items = []
            self._is_marquee = True

    def mouse_move(self, pos: QPointF, modifiers: int):
        # 定义鼠标移动事件处理方法
        if self._drag_start is None:
            return
        self._drag_current = QPointF(pos)

        # 问题4：旋转模式 —— Illustrator 标准旋转交互
        if self._is_rotating and self._dragging_item:
            current_angle = math.atan2(
                pos.y() - self._rotation_center.y(),
                pos.x() - self._rotation_center.x()
            )
            delta_angle = math.degrees(current_angle - self._rotation_start_angle)
            # Shift 约束：每次15度
            if modifiers & Qt.ShiftModifier:
                delta_angle = round(delta_angle / 15) * 15
            # 使用 rotate 方法在世界坐标系中绕中心点旋转
            self._dragging_item.rotate(delta_angle, self._rotation_center)
            self._rotation_start_angle = current_angle
            if self._document:
                self._document.modified = True
            return

        # 缩放模式
        if self._is_scaling and self._dragging_item:
            self._apply_resize(pos, bool(modifiers & Qt.ShiftModifier))
            if self._document:
                self._document.modified = True
            return

        dx = pos.x() - self._drag_start.x()
        dy = pos.y() - self._drag_start.y()
        # Shift 约束水平/垂直移动
        if modifiers & Qt.ShiftModifier:
            dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)

        if self._dragging_items:
            for item in self._dragging_items:
                item.move_by(dx, dy)
            self._total_dx += dx
            self._total_dy += dy
            self._drag_start = QPointF(pos)
            if self._document:
                self._document.modified = True
        elif self._dragging_item and not self._is_scaling and not self._is_rotating:
            self._dragging_item.move_by(dx, dy)
            self._total_dx += dx
            self._total_dy += dy
            self._drag_start = QPointF(pos)
            if self._document:
                self._document.modified = True

    def mouse_release(self, pos: QPointF, modifiers: int):
        # 问题4：旋转完成
        if self._is_rotating and self._dragging_item:
            self._is_rotating = False
            self._dragging_item = None
            self._drag_start = None
            self._drag_current = None
            self._total_dx = 0.0
            self._total_dy = 0.0
            return

        # 缩放完成：记录命令（通过 execute_command 统一入口）
        if self._is_scaling and self._dragging_item and self._document:
            new_world_rect = self._dragging_item.bounding_rect()
            if new_world_rect != self._scale_orig_br:
                # 通过尺寸变化记录（使用世界坐标矩形）
                cmd = ResizeItemCommand(
                    self._document, self._dragging_item,
                    self._scale_orig_br, new_world_rect,
                )
                self._document.execute_command(cmd)
            self._is_scaling = False
            self._scale_handle = None
            self._dragging_item = None
            self._drag_start = None
            self._drag_current = None
            self._total_dx = 0.0
            self._total_dy = 0.0
            return

        # 多选拖拽完成后记录移动命令（移动已在 mouse_move 中实时完成）
        moved_items = self._dragging_items if self._dragging_items else (
            [self._dragging_item] if self._dragging_item else []
        )
        if moved_items and self._document and (self._total_dx != 0 or self._total_dy != 0):
            cmd = MoveItemsCommand(
                self._document, moved_items,
                self._total_dx, self._total_dy,
                already_moved=True,  # 移动已在 mouse_move 中实时完成
            )
            self._document.execute_command(cmd)

        if self._is_marquee and self._drag_start and self._document:
            rect = QRectF(self._drag_start, pos).normalized()
            if rect.width() > 2 and rect.height() > 2:
                for layer in self._document.layers:
                    items = layer.get_items_in_rect(
                        rect.x(), rect.y(), rect.width(), rect.height(),
                    )
                    for item in items:
                        item.selected = True

        self._drag_start = None
        self._drag_current = None
        self._dragging_item = None
        self._dragging_items = []
        self._is_marquee = False
        self._is_scaling = False
        self._scale_handle = None
        self._is_rotating = False
        self._total_dx = 0.0
        self._total_dy = 0.0

    # ── 缩放核心 ──

    @staticmethod
    def _get_opposite_corner(handle: ResizeHandleType, rect: QRectF) -> QPointF:
        """获取缩放手柄对面的固定锚点"""
        # 文档字符串——获取缩放手柄对面的固定描点坐标
        match handle:
            case ResizeHandleType.TOP_LEFT:
                return rect.bottomRight()
            case ResizeHandleType.TOP_CENTER:
                return QPointF(rect.center().x(), rect.bottom())
            case ResizeHandleType.TOP_RIGHT:
                return rect.bottomLeft()
            case ResizeHandleType.MIDDLE_LEFT:
                return QPointF(rect.right(), rect.center().y())
            case ResizeHandleType.MIDDLE_RIGHT:
                return QPointF(rect.left(), rect.center().y())
            case ResizeHandleType.BOTTOM_LEFT:
                return rect.topRight()
            case ResizeHandleType.BOTTOM_CENTER:
                return QPointF(rect.center().x(), rect.top())
            case ResizeHandleType.BOTTOM_RIGHT:
                return rect.topLeft()

    def _apply_resize(self, mouse_pos: QPointF, keep_ratio: bool):
        """根据手柄类型和鼠标位置调整图形大小
        
        ★ 核心修复：直接在**世界坐标系**中计算目标矩形，
        然后通过逆变换转换为局部坐标写入 item.rect。
        
        旧代码的 Bug：
        1. mouse_press 存储的世界坐标 bounding_rect 被直接当局部坐标用 → 移动后缩放产生位移跳跃
        2. pivot < center 的比较对边缘手柄（坐标恰好相等）判断错误 → Y/X 坐标偏移
        """
        if not self._dragging_item:
            return
        pivot = self._scale_pivot          # 世界坐标 —— 固定不动的锚点
        orig = self._scale_orig_rect       # 世界坐标 —— 缩放前的包围盒
        mx, my = mouse_pos.x(), mouse_pos.y()
        px, py = pivot.x(), pivot.y()

        # ── 根据手柄类型，在世界坐标系中计算目标矩形 ──
        match self._scale_handle:
            case ResizeHandleType.TOP_LEFT:
                target = QRectF(mx, my, px - mx, py - my)
            case ResizeHandleType.TOP_CENTER:
                target = QRectF(orig.left(), my, orig.width(), py - my)
            case ResizeHandleType.TOP_RIGHT:
                target = QRectF(px, my, mx - px, py - my)
            case ResizeHandleType.MIDDLE_LEFT:
                target = QRectF(mx, orig.top(), px - mx, orig.height())
            case ResizeHandleType.MIDDLE_RIGHT:
                target = QRectF(px, orig.top(), mx - px, orig.height())
            case ResizeHandleType.BOTTOM_LEFT:
                target = QRectF(mx, py, px - mx, my - py)
            case ResizeHandleType.BOTTOM_CENTER:
                target = QRectF(orig.left(), py, orig.width(), my - py)
            case ResizeHandleType.BOTTOM_RIGHT:
                target = QRectF(px, py, mx - px, my - py)
            case _:
                return

        # 最小尺寸限制
        if target.width() < 10:
            if self._scale_handle in (ResizeHandleType.TOP_LEFT, ResizeHandleType.BOTTOM_LEFT,
                                       ResizeHandleType.MIDDLE_LEFT):
                target.setLeft(px - 10)
            else:
                target.setRight(px + 10)
        if target.height() < 10:
            if self._scale_handle in (ResizeHandleType.TOP_LEFT, ResizeHandleType.TOP_RIGHT,
                                       ResizeHandleType.TOP_CENTER):
                target.setTop(py - 10)
            else:
                target.setBottom(py + 10)

        # 等比约束
        if keep_ratio:
            aspect = orig.width() / max(orig.height(), 0.001)
            tw, th = target.width(), target.height()
            if self._scale_handle in (
                ResizeHandleType.TOP_CENTER, ResizeHandleType.BOTTOM_CENTER,
            ):
                th = tw / max(aspect, 0.001) if tw > 0 else th
                target.setHeight(th)
                # 调整位置保持锚点固定
                if self._scale_handle == ResizeHandleType.TOP_CENTER:
                    target.setTop(py - th)
                else:
                    target.setBottom(py + th)
            elif self._scale_handle in (
                ResizeHandleType.MIDDLE_LEFT, ResizeHandleType.MIDDLE_RIGHT,
            ):
                tw = th * aspect if th > 0 else tw
                target.setWidth(tw)
                if self._scale_handle == ResizeHandleType.MIDDLE_LEFT:
                    target.setLeft(px - tw)
                else:
                    target.setRight(px + tw)
            else:
                # 角手柄
                aspect_w = th * aspect
                aspect_h = tw / max(aspect, 0.001)
                if abs(tw - aspect_w) < abs(th - aspect_h):
                    th = tw / max(aspect, 0.001)
                    target.setHeight(th)
                else:
                    tw = th * aspect
                    target.setWidth(tw)
                # 调整角点位置
                self._adjust_corner_rect(target, self._scale_handle, px, py)

        # 应用缩放（世界坐标 → 局部坐标转换）
        self._resize_item_to_world_rect(self._dragging_item, target)

    @staticmethod
    def _adjust_corner_rect(rect: QRectF, handle, px: float, py: float):
        """等比缩放时调整角手柄矩形的位置，确保对角锚点固定"""
        match handle:
            case ResizeHandleType.TOP_LEFT:
                rect.moveBottomRight(QPointF(px, py))
            case ResizeHandleType.TOP_RIGHT:
                rect.moveBottomLeft(QPointF(px, py))
            case ResizeHandleType.BOTTOM_LEFT:
                rect.moveTopRight(QPointF(px, py))
            case ResizeHandleType.BOTTOM_RIGHT:
                rect.moveTopLeft(QPointF(px, py))

    def _resize_item_to_world_rect(self, item: GraphicItem, target_world: QRectF):
        """将世界坐标系的目标矩形应用到图形项上
        
        ★ 关键步骤：通过逆变换将世界坐标转为局部坐标，
        再写入 item.rect（局部属性）。
        这样无论元素是否被移动/旋转过，缩放都不会产生位移。
        """
        # 世界坐标 → 局部坐标
        inv, ok = item._transform.inverted()
        if not ok:
            return
        local_target = inv.mapRect(target_world)

        if isinstance(item, (RectangleItem, EllipseItem, TextFrame)):
            item.rect = local_target
        elif isinstance(item, PathItem):
            # 路径项：基于局部空间的尺寸变化缩放所有锚点
            local_orig = item.painter_path().boundingRect()
            scale_x = local_target.width() / max(local_orig.width(), 0.001)
            scale_y = local_target.height() / max(local_orig.height(), 0.001)
            ref_x = local_target.x() if scale_x > 0 else local_orig.right()
            ref_y = local_target.y() if scale_y > 0 else local_orig.bottom()
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
        else:
            # 通用缩放：使用 scale 方法
            local_orig = item.bounding_rect()
            sx = target_world.width() / max(local_orig.width(), 0.001)
            sy = target_world.height() / max(local_orig.height(), 0.001)
            item.scale(sx, sy)

    # ── 绘制 ──

    def draw_preview(self, painter: QPainter, editing_text=None):
        # 绘制缩放手柄和旋转手柄
        # 编辑中的文本框不绘制选中边框和手柄（Illustrator 标准行为）
        if self._document:
            for layer in self._document.layers:
                if not layer.visible:
                    continue
                for item in layer.items:
                    if item.selected and item.visible:
                        # 跳过正在编辑的文本框
                        if isinstance(item, TextFrame) and item == editing_text:
                            continue
                        self._draw_resize_handles(painter, item)
                        # 问题4：绘制旋转手柄
                        self._draw_rotate_handle(painter, item)

        if self._is_marquee and self._drag_start and self._drag_current:
            # 获取当前视图缩放比例
            scale = max(painter.transform().m11(), 0.001)
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(QColor(0, 120, 215, 30))
            painter.drawRect(QRectF(self._drag_start, self._drag_current))
    # 定义绘制缩放手柄的私有方法，接收参数：绘制器对象、图形项对象
    def _get_transformed_corners(self, item: GraphicItem) -> tuple[QPointF, QPointF, QPointF, QPointF]:
        """获取元素四个角在世界坐标系中的实际位置（考虑旋转）"""
        local_rect = item.painter_path().boundingRect()
        tl = item._transform.map(local_rect.topLeft())
        tr = item._transform.map(local_rect.topRight())
        bl = item._transform.map(local_rect.bottomLeft())
        br = item._transform.map(local_rect.bottomRight())
        return (tl, tr, bl, br)

    def _get_transformed_center(self, item: GraphicItem) -> QPointF:
        """获取元素中心在世界坐标系中的实际位置"""
        local_rect = item.painter_path().boundingRect()
        return item._transform.map(local_rect.center())

    def _draw_resize_handles(self, painter: QPainter, item: GraphicItem):
        """绘制 8 个缩放手柄（世界坐标系，使用变换后的实际角点位置）"""
        tl, tr, bl, br = self._get_transformed_corners(item)
        scale = max(painter.transform().m11(), 0.001)
        handle_size = 7 / scale
        half_hs = handle_size / 2

        pen = QPen(QColor(0, 120, 215), 1.0 / scale)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 255, 255))

        # 四个角 —— 使用变换后的实际角点
        corners = [tl, tr, bl, br]

        # 四条边的中点 —— 基于变换后角点计算
        edges = [
            QPointF((tl.x() + tr.x()) / 2, (tl.y() + tr.y()) / 2),      # top center
            QPointF((bl.x() + br.x()) / 2, (bl.y() + br.y()) / 2),      # bottom center
            QPointF((tl.x() + bl.x()) / 2, (tl.y() + bl.y()) / 2),      # middle left
            QPointF((tr.x() + br.x()) / 2, (tr.y() + br.y()) / 2),      # middle right
        ]
        # 遍历所有手柄位置；绘制手柄小方块
        for pt in corners + edges:
            painter.drawRect(QRectF(
                pt.x() - half_hs, pt.y() - half_hs,
                handle_size, handle_size,
            ))

    def _draw_rotate_handle(self, painter: QPainter, item: GraphicItem):
        """绘制旋转手柄 —— 位于选中框顶部中心上方（使用变换后的实际角点）"""
        tl, tr, bl, br = self._get_transformed_corners(item)
        scale = max(painter.transform().m11(), 0.001)

        # 顶部中心：使用变换后的左上和右上角点的中点
        top_center = QPointF((tl.x() + tr.x()) / 2, (tl.y() + tr.y()) / 2)
        # 旋转手柄位置：顶部中心上方
        rotate_center = QPointF(top_center.x(), top_center.y() - self.ROTATE_HANDLE_DISTANCE)

        # 绘制连接线（虚线）
        line_pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
        painter.setPen(line_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(top_center, rotate_center)

        # 绘制旋转手柄（圆形，带箭头效果）
        handle_r = 5 / scale
        painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(rotate_center, handle_r, handle_r)

        # 绘制旋转箭头指示符（小弧线）
        arc_pen = QPen(QColor(0, 120, 215), 1.0 / scale)
        painter.setPen(arc_pen)
        painter.setBrush(Qt.NoBrush)
        arc_r = handle_r * 0.6
        painter.drawArc(QRectF(
            rotate_center.x() - arc_r, rotate_center.y() - arc_r,
            arc_r * 2, arc_r * 2
        ), 0, 270 * 16)


# ── 直接选择工具 ──────────────────────────────────────────

class DirectSelectTool(BaseTool):
    """直接选择工具（A）—— 对照 Adobe Illustrator 1:1 复原
    
    AI 中的 Direct Selection Tool (白箭头) 行为：
    1. 点击已选中路径的锚点/手柄 → 选中并进入拖拽
    2. 点击已选中路径的线段 → 选中该路径（显示所有锚点），不添加锚点
    3. 按住 Alt/Option 拖拽手柄 → 断开手柄对称约束（转为角点）
    4. 拖拽平滑点的手柄 → 自动对称约束
    5. 未选中路径 → 点击选中（显示锚点），可拖拽整项
    6. 按住 Shift → 多选
    7. 框选 → 选中范围内的图形项
    """
    __slots__ = (
        '_drag_start', '_drag_current',
        '_dragging_anchor_idx', '_dragging_handle_idx',
        '_dragging_handle_type', '_dragging_item',
        '_drag_offset', '_selected_anchor_idx',
        '_is_marquee', '_old_anchors',
        '_has_moved',
        '_press_alt',           # 按下时 Alt 是否已激活（用于断手柄）
        '_original_anchor_type', # 记录拖拽前锚点类型
    )

    # 基础容差（100%缩放下的像素值，与 AI 一致）
    ANCHOR_TOLERANCE = 5.0       # 锚点点击容差
    HANDLE_TOLERANCE = 4.0       # 手柄点击容差  
    SEGMENT_TOLERANCE = 4.0      # 路径段点击容差
    DRAG_THRESHOLD = 3.0         # 最小拖拽阈值（像素）

    def __init__(self):
        super().__init__(ToolType.DIRECT_SELECT)
        self._drag_start: QPointF | None = None
        self._drag_current: QPointF | None = None
        self._dragging_anchor_idx: int = -1
        self._dragging_handle_idx: int = -1
        self._dragging_handle_type: str = ''
        self._dragging_item: GraphicItem | None = None
        self._drag_offset = QPointF(0, 0)
        self._selected_anchor_idx: int = -1
        self._is_marquee: bool = False
        self._old_anchors: list[AnchorPoint] = []
        self._has_moved: bool = False
        self._press_alt: bool = False
        # 初始化 原始锚点类型为None
        self._original_anchor_type: AnchorPointType | None = None

    # ── 辅助方法 ──

    @staticmethod
    def _safe_inverted(transform):
        """安全获取逆变换矩阵，返回 (inverted_transform, success)"""
        try:
            inv, ok = transform.inverted()
            return (inv, ok)
        except Exception:
            return (transform, False)

    def _find_path_at(self, pos: QPointF, must_be_selected: bool = False) -> tuple[PathItem | None, QPointF | None]:
        """从文档中查找点击位置的 PathItem，返回 (item, local_pos)"""
        # 文档字符串——从文档找点击位置的路径项
        if not self._document:
            return (None, None)
        for layer in reversed(self._document.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                if not isinstance(item, PathItem) or not item.anchors:
                    continue
                if must_be_selected and not item.selected:
                # 如果要求已选中但图形项未被选中
                    continue
                inv, ok = self._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
                # 用 bounding_rect 快速判断（放宽一点）
                br = item.bounding_rect()
                if not br.contains(local_pos):
                    continue
                # 找到匹配的路径项.返回(图形项，本地坐标)
                return (item, local_pos)
        return (None, None)

    # ── 鼠标事件 ──

    def mouse_press(self, pos: QPointF, modifiers: int):
        if not self._document:
            return
        self._drag_start = QPointF(pos)
        self._drag_current = QPointF(pos)
        self._has_moved = False
        self._press_alt = bool(modifiers & Qt.AltModifier)
        self._original_anchor_type = None

        shift = bool(modifiers & Qt.ShiftModifier)

        # ── 1. 优先检测已选中路径的手柄 ──
        for layer in reversed(self._document.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
                inv, ok = self._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
                idx, htype = item.get_handle_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.HANDLE_TOLERANCE,
                )
                if idx >= 0:
                    self._dragging_item = item
                    self._dragging_handle_idx = idx
                    self._dragging_handle_type = htype
                    self._selected_anchor_idx = idx
                    # 深拷贝当前所有锚点保存为旧状态
                    self._old_anchors = [a.copy() for a in item.anchors]
                    # 记录原始锚点类型（Alt 拖拽时断开约束）
                    self._original_anchor_type = item.anchors[idx].anchor_type
                    # 如果按 Alt，将锚点转为角点（断开对称约束）
                    if self._press_alt:
                        item.anchors[idx].convert_to_corner()
                    return

        # ── 2. 检测已选中路径的锚点 ──
        for layer in reversed(self._document.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
                # 获取图形变换矩阵的逆矩阵
                inv, ok = self._safe_inverted(item._transform)
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
                    self._selected_anchor_idx = idx
                    self._old_anchors = [a.copy() for a in item.anchors]
                    self._original_anchor_type = item.anchors[idx].anchor_type
                    # 记录拖拽前该锚点的类型
                    return

        # ── 3. 检测已选中路径的线段（AI：点击线段选中路径但不添加锚点）──
        for layer in reversed(self._document.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
                inv, ok = self._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
                # 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标
                seg = item.get_segment_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.SEGMENT_TOLERANCE,
                )
                if seg >= 0:
                    # AI 行为：点击已选中路径的线段，选中该路径用于整体拖拽
                    self._dragging_item = item
                    self._selected_anchor_idx = -1  # 不选中特定锚点
                    # 重置选中锚点索引为-1，（表示无选中锚点）
                    return

        # ── 4. 检测未选中路径 → 选中它并准备整体拖拽 ──
        # AI 行为：用 Direct Select 工具点击未选中路径的任意位置 → 选中路径显示锚点
        for layer in reversed(self._document.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                if not isinstance(item, PathItem) or item.selected or not item.anchors:
                    continue
                inv, ok = self._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
                
                # 先检查是否在路径段附近
                seg = item.get_segment_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.SEGMENT_TOLERANCE,
                )
                if seg >= 0:
                    if not shift:
                        self._document.clear_selection()
                        # 清除文档中所有图形项的选中状态
                    item.selected = True
                    self._dragging_item = item
                    self._selected_anchor_idx = -1
                    return
                
                # 再检查是否在锚点附近，检测本地坐标处是否有锚点，获取本地坐标系分量
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
                    # 深拷贝当前所有锚点保存为旧状态
                    self._original_anchor_type = item.anchors[idx].anchor_type
                    # 记录拖拽前该锚点的类型
                    return
                
                # 最后检查填充区域
                if item.contains_point(local_pos):
                    if not shift:
                        self._document.clear_selection()
                    item.selected = True
                    self._dragging_item = item
                    self._selected_anchor_idx = -1
                    return

        # ── 5. 检测普通图形项 ──
        item = self._document.get_item_at(pos.x(), pos.y())
        if item:
            if not shift:
                self._document.clear_selection()
            item.selected = True
            self._dragging_item = item
            # 设置当前图形项为单项拖拽目标
            self._selected_anchor_idx = -1
            return

        # ── 6. 框选 ──
        if not shift:
            self._document.clear_selection()
        self._is_marquee = True

    def mouse_move(self, pos: QPointF, modifiers: int):
        # 鼠标位置坐标，修饰键标志位
        if self._drag_start is None:
            return
        self._drag_current = QPointF(pos)

        dx_total = pos.x() - self._drag_start.x()
        dy_total = pos.y() - self._drag_start.y()
        dist = math.sqrt(dx_total * dx_total + dy_total * dy_total)
        alt_held = bool(modifiers & Qt.AltModifier)

        # ── 手柄拖拽 ──
        if self._dragging_handle_idx >= 0 and self._dragging_item:
            if isinstance(self._dragging_item, PathItem):
                inv, ok = self._safe_inverted(self._dragging_item._transform)
                if not ok:
                    return
                # 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标
                local_pos = inv.map(pos)
                # 获取被拖拽手柄所属的锚点
                anchor = self._dragging_item.anchors[self._dragging_handle_idx]
                rel_x = local_pos.x() - anchor.x
                rel_y = local_pos.y() - anchor.y

                # 平滑点约束：不按 Alt 时自动对称；是平滑锚点 并且 没有按住Alt键
                constrain = (anchor.anchor_type == AnchorPointType.SMOOTH and not alt_held)

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
                if self._document:
                    self._document.modified = True

        # ── 锚点拖拽（超过阈值后移动）──
        elif self._dragging_anchor_idx >= 0 and self._dragging_item:
            if not self._has_moved:
                # 如果尚未确认开始有效拖拽
                if dist < self.DRAG_THRESHOLD:
                    return
                self._has_moved = True

            if isinstance(self._dragging_item, PathItem):
                inv, ok = self._safe_inverted(self._dragging_item._transform)
                if not ok:
                    return
                local_pos = inv.map(pos)
                # 将鼠标世界坐标通过逆矩阵转换为图形项的局部坐标；
                # 指定索引的锚点移动到新位置，同时更新路径形状
                self._dragging_item.move_anchor(
                    self._dragging_anchor_idx, local_pos.x(), local_pos.y(),
                )
                if self._document:
                    self._document.modified = True

        # ── 整项拖拽（非锚点/手柄拖拽模式）──；自身._拖动项且非自身._是选框
        elif self._dragging_item and not self._is_marquee:
            if not self._has_moved:
                if dist < self.DRAG_THRESHOLD:
                    return
                self._has_moved = True

            dx = pos.x() - self._drag_start.x()
            dy = pos.y() - self._drag_start.y()
            if modifiers & Qt.ShiftModifier:
                dx, dy = (dx, 0) if abs(dx) > abs(dy) else (0, dy)
            self._dragging_item.move_by(dx, dy)
            self._drag_start = QPointF(pos)
            if self._document:
                self._document.modified = True

    def mouse_release(self, pos: QPointF, modifiers: int):
        # ── 如果拖拽了手柄且按了 Alt，需要恢复锚点类型为角点 ──
        if self._dragging_handle_idx >= 0 and self._dragging_item:
            # 如果正在拖拽手柄且有目标图形项
            if isinstance(self._dragging_item, PathItem):
                if self._press_alt or self._has_moved:
                    # Alt+拖拽：断开对称约束，转为角点
                    anchor = self._dragging_item.anchors[self._dragging_handle_idx]
                    if self._press_alt:
                        anchor.anchor_type = AnchorPointType.CORNER
                    self._dragging_item._build_path()

        # ── 记录撤销命令（通过 execute_command 统一入口）──
        if self._old_anchors and self._dragging_item and self._document:
            if isinstance(self._dragging_item, PathItem):
                new_anchors = [a.copy() for a in self._dragging_item.anchors]
                if self._has_moved and len(self._old_anchors) == len(new_anchors):
                    # 检查是否真的有变化
                    changed = False
                    # 逐一对比创建修改命令
                    for old, new in zip(self._old_anchors, new_anchors):
                        if (old.x != new.x or old.y != new.y or
                            old.handle_in != new.handle_in or
                            old.handle_out != new.handle_out or
                            old.anchor_type != new.anchor_type):
                            changed = True
                            break
                    # 如果确实存在变化
                    if changed:
                        cmd = ModifyAnchorCommand(
                            self._document, self._dragging_item,
                            self._old_anchors, new_anchors,
                        )
                        self._document.execute_command(cmd)

        # ── 框选 ──
        if self._is_marquee and self._drag_start and self._document:
            rect = QRectF(self._drag_start, pos).normalized()
            if rect.width() > 2 and rect.height() > 2:
                for layer in self._document.layers:
                    items = layer.get_items_in_rect(
                        rect.x(), rect.y(), rect.width(), rect.height(),
                    )
                    for item in items:
                        item.selected = True

        # ── 重置状态 ──
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

    # ── 键盘 ──

    def key_press(self, key: int, modifiers: int):
        """键盘操作对照 AI 行为"""
        # Delete/Backspace 删除选中的锚点（AI：Delete Anchor Point）
        if key in (Qt.Key_Delete, Qt.Key_Backspace):
            if self._selected_anchor_idx >= 0 and self._dragging_item:
                if isinstance(self._dragging_item, PathItem):
                    if self._dragging_item.anchor_count > 2:
                        old_anchors = [a.copy() for a in self._dragging_item.anchors]
                        self._dragging_item.remove_anchor(self._selected_anchor_idx)
                        if self._document:
                            new_anchors = [a.copy() for a in self._dragging_item.anchors]
                            cmd = ModifyAnchorCommand(
                                self._document, self._dragging_item,
                                old_anchors, new_anchors,
                            )
                            self._document.execute_command(cmd)
                        self._selected_anchor_idx = max(0, min(
                            self._selected_anchor_idx,
                            self._dragging_item.anchor_count - 1,
                        ))
            return

        # Plus/Equal 在选中锚点后添加新锚点（段中点）
        if key in (Qt.Key_Plus, Qt.Key_Equal):
            if self._selected_anchor_idx >= 0 and self._dragging_item:
                if isinstance(self._dragging_item, PathItem):
                    self._add_anchor_after_selected(self._dragging_item)
            return

    def _add_anchor_after_selected(self, item: PathItem):
        """在选中锚点之后的段中点添加新锚点"""
        anchors = item.anchors
        i = self._selected_anchor_idx
        if i < 0 or len(anchors) < 2:
            return
        n = len(anchors)
        j = (i + 1) % n
        if not item.closed and i == n - 1:
            return
        
        # 在贝塞尔曲线段的中点添加锚点
        prev, curr = anchors[i], anchors[j]
        
        # 使用贝塞尔采样获取真正的中点
        samples = PathItem._sample_bezier_segment(prev, curr, num_samples=4)
        if len(samples) >= 2:
            # 取中点
            mid_idx = len(samples) // 2
            mx, my = samples[mid_idx]
        else:
            mx = (prev.x + curr.x) / 2
            my = (prev.y + curr.y) / 2
        
        old_anchors = [a.copy() for a in anchors]
        new_anchor = AnchorPoint(mx, my)
        item.insert_anchor(i + 1, new_anchor)
        self._selected_anchor_idx = i + 1
        self._dragging_item = item
        
        if self._document:
            new_anchors = [a.copy() for a in item.anchors]
            # 创建修改锚点撤销命令
            cmd = ModifyAnchorCommand(
                self._document, item, old_anchors, new_anchors,
            )
            # 通过文档统一入口执行命令对象
            self._document.execute_command(cmd)

    # ── 绘制预览 ──

    def draw_preview(self, painter: QPainter, editing_text=None):
        if not self._document:
            return
        for layer in self._document.layers:
            if not layer.visible:
                continue
            for item in layer.items:
                if isinstance(item, PathItem) and item.selected:
                    # 绘制路径上所有锚点和贝塞尔手柄的视觉表示
                    self._draw_anchor_handles(painter, item)

        if self._is_marquee and self._drag_start and self._drag_current:
            scale = max(painter.transform().m11(), 0.001)
            # 创建蓝色虚线画笔；
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(QColor(0, 120, 215, 30))
            painter.drawRect(QRectF(self._drag_start, self._drag_current))

    def _draw_anchor_handles(self, painter: QPainter, item: PathItem):
        """绘制锚点和贝塞尔手柄，对照 AI 的视觉风格
        
        AI 锚点渲染规则：
        - 未选中锚点：白色填充方形，蓝色边框
        - 选中锚点：蓝色填充方形，深蓝边框
        - 手柄线：灰色虚线（handle_in）/ 实线（handle_out）
        - 手柄端点：白色填充圆形，灰色边框
        - 平滑点 vs 角点使用相同视觉表示
        """
        if not item.anchors:
            return

        scale = max(painter.transform().m11(), 0.001)
        handle_r = 3.5 / scale        # 手柄端点半径
        anchor_half = 3.5 / scale     # 锚点半边长
        highlight_half = 4.5 / scale  # 选中锚点半边长

        transform = item._transform
        anchor_color = QColor(0, 120, 215)       # AI 蓝
        anchor_border = QColor(0, 80, 180)
        handle_color = QColor(120, 120, 120)     # 手柄线颜色

        for i, anchor in enumerate(item.anchors):
            ax_local, ay_local = anchor.x, anchor.y
            ax = transform.map(QPointF(ax_local, ay_local)).x()
            ay = transform.map(QPointF(ax_local, ay_local)).y()

            # ── 绘制 handle_in 线和端点 ──
            if anchor.handle_in:
                hx_local = ax_local + anchor.handle_in.x()
                hy_local = ay_local + anchor.handle_in.y()
                # 将手柄端点的局部坐标通过变换矩阵映射到世界坐标系，得到手柄在世界空间中的位置
                hx_pt = transform.map(QPointF(hx_local, hy_local))
                hx, hy = hx_pt.x(), hx_pt.y()
                
                # 手柄线
                handle_pen = QPen(handle_color, 1.0 / scale, Qt.DashLine)
                painter.setPen(handle_pen)
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))
                
                # 手柄端点（圆形）
                painter.setBrush(QColor(255, 255, 255))
                # 设置画笔样式(颜色，线宽，虚实线类型)，用于后续的描边绘制
                painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))
                # 在指定矩形内绘制内切椭圆（用于锚点和手柄端点的图形表示）
                painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)

            # ── 绘制 handle_out 线和端点 ──
            if anchor.handle_out:
                hx_local = ax_local + anchor.handle_out.x()
                hy_local = ay_local + anchor.handle_out.y()
                # 将手柄端点的局部坐标通过图形项变换矩阵映射到世界坐标系
                hx_pt = transform.map(QPointF(hx_local, hy_local))
                hx, hy = hx_pt.x(), hx_pt.y()
                
                # 手柄线
                handle_pen = QPen(handle_color, 1.0 / scale, Qt.SolidLine)
                painter.setPen(handle_pen)
                painter.setBrush(Qt.NoBrush)
                # 绘制从起点到终点的线段
                painter.drawLine(QPointF(ax, ay), QPointF(hx, hy))
                
                # 手柄端点（圆形）；在指定矩形内绘制内切椭圆
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(80, 80, 80), 1.0 / scale))
                painter.drawEllipse(QPointF(hx, hy), handle_r, handle_r)

            # ── 绘制锚点（方形）──；判断当前遍历到的锚点是否为高亮选中状态
            is_highlighted = (i == self._selected_anchor_idx)
            
            if is_highlighted:
                # 选中锚点：蓝色填充
                painter.setBrush(anchor_color)
                painter.setPen(QPen(anchor_border, 1.5 / scale))
                # 绘制高亮选中锚点方框
                painter.drawRect(QRectF(
                    ax - highlight_half, ay - highlight_half,
                    highlight_half * 2, highlight_half * 2,
                ))
            else:
                # 未选中锚点：白色填充
                painter.setBrush(QColor(255, 255, 255))
                # 设置画笔样式,用于后续的描边绘制
                painter.setPen(QPen(anchor_color, 1.5 / scale))
                # 绘制未选中锚点方框
                painter.drawRect(QRectF(
                    ax - anchor_half, ay - anchor_half,
                    anchor_half * 2, anchor_half * 2,
                ))
    # 取消当前操作并重置状态；
    def cancel(self):
        self._selected_anchor_idx = -1
        self._dragging_anchor_idx = -1
        self._dragging_handle_idx = -1
        self._dragging_item = None
        super().cancel()

    @staticmethod
    def _draw_single_anchor(painter: QPainter, item: PathItem, 
                             anchor_idx: int, highlighted: bool = True):
        # 定义绘制单个锚点的静态方法，接收绘图引擎，贝塞尔路径，锚点索引，是否高亮选中
        """绘制单个锚点（供其他锚点工具使用）"""
        if anchor_idx < 0 or anchor_idx >= len(item.anchors):
            return
        scale = max(painter.transform().m11(), 0.001)
        # 根据是否高亮选择锚点尺寸：选中时稍大，未选中时稍小
        anchor_half = 4.5 / scale if highlighted else 3.5 / scale
        transform = item._transform
        anchor = item.anchors[anchor_idx]
        ax = transform.map(QPointF(anchor.x, anchor.y)).x()
        ay = transform.map(QPointF(anchor.x, anchor.y)).y()
        # 如果当前锚点为高亮状态
        if highlighted:
            painter.setBrush(QColor(0, 120, 215))
            painter.setPen(QPen(QColor(0, 80, 180), 1.5 / scale))
        else:
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
        # 绘制锚点方块
        painter.drawRect(QRectF(
            ax - anchor_half, ay - anchor_half,
            anchor_half * 2, anchor_half * 2,
        ))


# ── 形状工具 ──────────────────────────────────────────────

class ShapeTool(BaseTool, ABC):
    """形状工具基类（矩形/椭圆）"""
    # 类/方法文档字符串
    __slots__ = ('_drag_start', '_drag_current', '_preview_item')
    # 构造函数
    def __init__(self, tool_type: ToolType):
        super().__init__(tool_type)
        self._drag_start: QPointF | None = None
        self._drag_current: QPointF | None = None
        self._preview_item: GraphicItem | None = None
        # 拖拽绘制过程中暂存预览对象，用于绘制预览
    @abstractmethod
    def _create_item(self, rect: QRectF) -> GraphicItem:
        ...
    # 鼠标按下事件处理方法，接收自身引用
    def mouse_press(self, pos: QPointF, modifiers: int):
        self._drag_start = QPointF(pos)
        # 记录拖拽起始坐标，记录拖拽当前坐标，绘制状态标志初始化为True
        self._drag_current = QPointF(pos)
        self._is_drawing = True
        if self._document:
            self._document.clear_selection()
    # 鼠标移动事件处理方法，接收自身引用，
    def mouse_move(self, pos: QPointF, modifiers: int):
        if self._is_drawing:
            self._drag_current = QPointF(pos)
    # 鼠标释放事件处理方法
    def mouse_release(self, pos: QPointF, modifiers: int):
        if not self._is_drawing or not self._document or not self._drag_start:
            return
        # 记录拖拽当前坐标
        self._drag_current = QPointF(pos)
        # 创建矩形区域对象
        rect = QRectF(self._drag_start, self._drag_current).normalized()

        # Shift 约束等比（正方形/正圆）
        if modifiers & Qt.ShiftModifier:
            size = max(rect.width(), rect.height())
            if rect.width() < rect.height():
                rect.setWidth(size)
            else:
                rect.setHeight(size)

        if rect.width() > 2 and rect.height() > 2:
            # 如果矩形尺寸足够大，调用子类工厂方法
            item = self._create_item(rect)
            item.selected = True
            self._document.add_item(item)
        # 清空拖拽起始点，清空拖拽当前坐标，将绘制状态标志重置为False
        self._drag_start = None
        self._drag_current = None
        self._is_drawing = False

    def draw_preview(self, painter: QPainter, editing_text=None):
        if self._is_drawing and self._drag_start and self._drag_current:
            rect = QRectF(self._drag_start, self._drag_current).normalized()
            scale = max(painter.transform().m11(), 0.001)
            # 创建蓝色虚线画笔 + 半透明蓝色填充，用于绘制形状工具拖拽预览矩形
            pen = QPen(QColor(0, 120, 215), 1.0 / scale, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(QColor(0, 120, 215, 20))
            painter.drawRect(rect)


class RectangleTool(ShapeTool):
    """矩形工具"""
    __slots__ = ()

    def __init__(self):
        super().__init__(ToolType.RECTANGLE)

    def _create_item(self, rect: QRectF) -> GraphicItem:
        # 创建具体图形项，接收自身引用，矩形区域
        item = RectangleItem(rect.x(), rect.y(), rect.width(), rect.height())
        item.style.fill_color = QColor(200, 200, 200)
        item.style.stroke_color = QColor(50, 50, 50)
        item.style.stroke_width = 2.0
        return item


class EllipseTool(ShapeTool):
    """椭圆工具"""
    __slots__ = ()

    def __init__(self):
        super().__init__(ToolType.ELLIPSE)

    def _create_item(self, rect: QRectF) -> GraphicItem:
        item = EllipseItem(rect.x(), rect.y(), rect.width(), rect.height())
        item.style.fill_color = QColor(200, 200, 200)
        item.style.stroke_color = QColor(50, 50, 50)
        item.style.stroke_width = 2.0
        return item


# ── 添加锚点工具 (Add Anchor Point Tool, +) ──────────────────

class AddAnchorPointTool(BaseTool):
    # 类文档字符串续行：描述工具功能，在路径段上点击添加新锚点
    """添加锚点工具 —— 在路径段上点击添加新锚点
    
    对照 AI 行为：
    - 点击路径段 → 在最近位置添加新锚点（不进入拖拽）
    - 只对已选中的路径有效
    """
    __slots__ = ('_selected_anchor_idx', '_dragging_item')

    SEGMENT_TOLERANCE = 4.0

    def __init__(self):
        super().__init__(ToolType.ADD_ANCHOR)
        self._selected_anchor_idx: int = -1
        self._dragging_item: GraphicItem | None = None
        # 初始化单选拖拽目标图形项为None，表示当前无活跃的拖拽目标
    # 鼠标按下事件处理方法，接收自身引用
    def mouse_press(self, pos: QPointF, modifiers: int):
        if not self._document:
            return
        
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
                # 获取本地坐标系中的x坐标分量
                seg = item.get_segment_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.SEGMENT_TOLERANCE,
                )
                # 如果命中了路径段
                if seg >= 0:
                    # 找到最近点；获取段落上最近坐标
                    closest = item.get_closest_point_on_segment(seg, local_pos.x(), local_pos.y())
                    # 对路径中每个锚点执行深拷贝，生成操作前的锚点状态快照
                    old_anchors = [a.copy() for a in item.anchors]
                    # 计算坐标
                    new_anchor = AnchorPoint(closest[0], closest[1])
                    # 计算新锚点的插入位置索引
                    insert_idx = seg + 1
                    # 在路径的指定位置插入新锚点
                    item.insert_anchor(insert_idx, new_anchor)
                    # 将新锚点的插入索引设为当前选中锚点索引
                    self._selected_anchor_idx = insert_idx
                    # 设置当前图形项为单项拖拽目标
                    self._dragging_item = item
                    
                    if self._document:
                        # 对每个锚点执行深拷贝，生成锚点列表的副本
                        new_anchors = [a.copy() for a in item.anchors]
                        # 创建修改锚点撤销命令，文档对象，目标路径
                        cmd = ModifyAnchorCommand(
                            self._document, item, old_anchors, new_anchors,
                        )
                        self._document.execute_command(cmd)
                    return

    def mouse_move(self, pos: QPointF, modifiers: int):
        pass  # 不拖拽

    def mouse_release(self, pos: QPointF, modifiers: int):
        pass

    def draw_preview(self, painter: QPainter, editing_text=None):
        """高亮显示新添加的锚点"""
        # 类/方法文档字符串：高亮显示新添加的锚点，如果有选中锚点和目标图形项
        if self._selected_anchor_idx >= 0 and self._dragging_item:
            if isinstance(self._dragging_item, PathItem):
                # 绘制单个锚点及其手柄的预览
                DirectSelectTool._draw_single_anchor(
                    painter, self._dragging_item, self._selected_anchor_idx, True
                )

    def cancel(self):
        self._selected_anchor_idx = -1
        self._dragging_item = None
        super().cancel()


# ── 删除锚点工具 (Delete Anchor Point Tool, -) ────────────────

class DeleteAnchorPointTool(BaseTool):
    """删除锚点工具 —— 点击锚点直接删除
    
    对照 AI 行为：
    - 点击锚点 → 删除该锚点（保留路径连续性）
    - 至少保留 2 个锚点
    - 只对已选中的路径有效
    """
    __slots__ = ('_selected_anchor_idx', '_dragging_item')
    # 定义锚点命中检测容器为5.0
    ANCHOR_TOLERANCE = 5.0

    def __init__(self):
        # 调用父类构造函数，传入删除锚点工具类型
        super().__init__(ToolType.DELETE_ANCHOR)
        self._selected_anchor_idx: int = -1
        # 初始化单选拖拽目标图形项为None
        self._dragging_item: GraphicItem | None = None

    def mouse_press(self, pos: QPointF, modifiers: int):
        if not self._document:
            return
        
        for layer in reversed(self._document.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                # 只处理贝塞尔路径类型的图形项
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
                if item.anchor_count <= 2:
                    continue
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
                # 检测本地坐标处是否有锚点；获取本地坐标系中的x坐标分量
                idx = item.get_anchor_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.ANCHOR_TOLERANCE,
                )
                if idx >= 0:
                    old_anchors = [a.copy() for a in item.anchors]
                    item.remove_anchor(idx)
                    
                    self._dragging_item = item
                    # 重置选中锚点索引为-1
                    self._selected_anchor_idx = -1
                    # 如果工具关联了文档
                    if self._document:
                        # 对每个锚点执行深拷贝，生成锚点列表的副本
                        new_anchors = [a.copy() for a in item.anchors]
                        # 创建修改锚点撤销命令
                        cmd = ModifyAnchorCommand(
                            self._document, item, old_anchors, new_anchors,
                        )
                        self._document.execute_command(cmd)
                    return
    # 鼠标移动时不处理
    def mouse_move(self, pos: QPointF, modifiers: int):
        pass
    # 鼠标释放时不处理
    def mouse_release(self, pos: QPointF, modifiers: int):
        pass
    # 预览方法
    def draw_preview(self, painter: QPainter, editing_text=None):
        pass  # AI 的删除锚点工具在悬停时显示 - 图标，这里简化处理
    # 取消方法
    def cancel(self):
        self._selected_anchor_idx = -1
        # 清空拖拽目标
        self._dragging_item = None
        super().cancel()


# ── 转换锚点工具 (Convert Anchor Point Tool, Shift+C) ─────────

class ConvertAnchorPointTool(BaseTool):
    """转换锚点工具 —— 切换锚点类型 / 拖拽拉出手柄
    
    对照 AI 行为：
    - 点击平滑点 → 转为角点（移除手柄）
    - 点击角点并拖拽 → 拉出手柄转为平滑点
    - 拖拽手柄 → 断开对称约束
    """
    # 拖拽起始坐标，拖拽中图形项，拖拽中锚点索引，是否正在拖拽，旧锚点列表
    __slots__ = (
        '_drag_start', '_dragging_item', '_dragging_anchor_idx',
        '_is_dragging', '_old_anchors',
    )

    ANCHOR_TOLERANCE = 5.0
    DRAG_THRESHOLD = 3.0
    
    def __init__(self):
        super().__init__(ToolType.CONVERT_ANCHOR)
        self._drag_start: QPointF | None = None
        self._dragging_item: GraphicItem | None = None
        self._dragging_anchor_idx: int = -1
        self._is_dragging: bool = False
        self._old_anchors: list[AnchorPoint] = []

    def mouse_press(self, pos: QPointF, modifiers: int):
        if not self._document:
            return
        self._drag_start = QPointF(pos)
        self._is_dragging = False
        
        for layer in reversed(self._document.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                # 如果该项不是路径项实例，或该项未被选中，或该项无锚点：
                if not isinstance(item, PathItem) or not item.selected or not item.anchors:
                    continue
                # 获取逆变换矩阵
                inv, ok = DirectSelectTool._safe_inverted(item._transform)
                if not ok:
                    continue
                local_pos = inv.map(pos)
                idx = item.get_anchor_at(
                    local_pos.x(), local_pos.y(),
                    tolerance=self.ANCHOR_TOLERANCE,
                )
                if idx >= 0:
                    # 如果命中了锚点/手柄；设置当前图形项为单项拖拽目标
                    self._dragging_item = item
                    # 记录被拖拽的锚点索引
                    self._dragging_anchor_idx = idx
                    self._old_anchors = [a.copy() for a in item.anchors]
                    return

    def mouse_move(self, pos: QPointF, modifiers: int):
        # 没有正在拖拽的项目，或者 拖拽锚点索引小于 0
        if not self._dragging_item or self._dragging_anchor_idx < 0:
            return
        if self._drag_start is None:
            return
        
        dx = pos.x() - self._drag_start.x()
        dy = pos.y() - self._drag_start.y()
        dist = math.sqrt(dx*dx + dy*dy)
        # 检测是否开始拖拽
        if not self._is_dragging:
            if dist < self.DRAG_THRESHOLD:
                return
            self._is_dragging = True
        
        # 拖拽：从锚点拉出手柄；
        if isinstance(self._dragging_item, PathItem):
            inv, ok = DirectSelectTool._safe_inverted(self._dragging_item._transform)
            if not ok:
                return
            local_pos = inv.map(pos)
            # 获取当前拖拽的锚点对象
            anchor = self._dragging_item.anchors[self._dragging_anchor_idx]
            # 计算手柄相对锚点的水平偏移
            rel_x = local_pos.x() - anchor.x
            rel_y = local_pos.y() - anchor.y
            
            # 拉出双向对称手柄（平滑点）；设置出方向手柄坐标为鼠标相对于锚点的偏移量
            anchor.handle_out = QPointF(rel_x, rel_y)
            anchor.handle_in = QPointF(-rel_x, -rel_y)
            anchor.anchor_type = AnchorPointType.SMOOTH
            # 根据当前锚点数据重新构建绘制路径；
            self._dragging_item._build_path()
            if self._document:
                self._document.modified = True
    # 鼠标释放时
    def mouse_release(self, pos: QPointF, modifiers: int):
        if not self._dragging_item or self._dragging_anchor_idx < 0:
            self._drag_start = None
            return
        
        if isinstance(self._dragging_item, PathItem):
            # 获取被拖拽手柄所属的锚点对象，保存到局部变量anchor
            anchor = self._dragging_item.anchors[self._dragging_anchor_idx]
            
            if not self._is_dragging:
                # 点击（未拖拽）：切换锚点类型
                if anchor.has_handles:
                    # 有手柄 → 转为角点（移除手柄）
                    anchor.remove_handles()
                # 无手柄的角点 → 点击不产生变化（AI 行为）
                self._dragging_item._build_path()
            
            # 记录撤销命令（通过 execute_command 统一入口）
            # 如果存在旧锚点
            if self._document and self._old_anchors:
                new_anchors = [a.copy() for a in self._dragging_item.anchors]
                # 创建修改锚点撤销命令
                cmd = ModifyAnchorCommand(
                    self._document, self._dragging_item,
                    self._old_anchors, new_anchors,
                )
                self._document.execute_command(cmd)
        
        self._drag_start = None
        self._dragging_item = None
        self._dragging_anchor_idx = -1
        self._is_dragging = False
        self._old_anchors = []

    def draw_preview(self, painter: QPainter, editing_text=None):
        """拖拽时显示预览手柄线"""
        # 接收自身引用，绘图引擎
        if self._is_dragging and self._dragging_item and self._dragging_anchor_idx >= 0:
            if isinstance(self._dragging_item, PathItem):
                DirectSelectTool._draw_single_anchor(
                    painter, self._dragging_item, self._dragging_anchor_idx, True
                )
    # 取消时
    def cancel(self):
        self._dragging_item = None
        self._dragging_anchor_idx = -1
        self._is_dragging = False
        super().cancel()


# ── 钢笔工具 ──────────────────────────────────────────────

class PenTool(BaseTool):
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
    
    DRAG_THRESHOLD = 3  # 拖拽阈值（像素），小于此值视为单击
    CLOSE_TOLERANCE = 8  # 闭合路径检测容差
    HANDLE_TOLERANCE = 5  # 手柄命中容差
    ANCHOR_TOLERANCE = 6  # 锚点命中容差
    SEGMENT_TOLERANCE = 5  # 路径段命中容差
    SHIFT_ANGLE_STEP = 45  # Shift约束角度步长（度）

    __slots__ = (
        '_current_path', '_drawing', '_hover_state',
        '_drag_start_pos', '_is_dragging_handle',
        '_dragged_anchor_idx', '_dragged_handle_side',
        '_alt_adjusting', '_space_moving', '_space_start_pos',
        '_ctrl_temp_select', '_ctrl_drag_start',
    )

    # ── 钢笔光标状态枚举 ──
    PEN_DEFAULT = 0        # 默认钢笔
    PEN_PLUS = 1           # Pen+  添加锚点
    PEN_MINUS = 2          # Pen-  删除锚点
    PEN_CLOSE = 3          # Pen○  闭合路径
    PEN_CONTINUE = 4       # Pen/  继续路径

    def __init__(self):
        super().__init__(ToolType.PEN)
        self._current_path: PathItem | None = None
        self._drawing: bool = False          # 正在拖拽中（创建平滑点）
        # 初始化钢笔光标悬停状态为默认PEN_DEFAULT
        self._hover_state: int = PenTool.PEN_DEFAULT
        
        # 拖拽状态；初始化起始位置，初始化手柄拖拽标志，初始化被拖拽手柄所属的锚点索引
        self._drag_start_pos: QPointF | None = None
        self._is_dragging_handle: bool = False
        self._dragged_anchor_idx: int = -1
        self._dragged_handle_side: str = ''
        
        # 隐藏功能状态
        self._alt_adjusting: bool = False     # Alt 调整单侧方向线
        self._space_moving: bool = False       # Space 移动当前锚点
        self._space_start_pos: QPointF | None = None
        self._ctrl_temp_select: bool = False   # Ctrl 临时直接选择
        self._ctrl_drag_start: QPointF | None = None

    # ── 辅助方法 ──

    def _snap_angle(self, dx: float, dy: float) -> tuple[float, float]:
        """Shift约束角度到最近的45度增量"""
        angle = math.atan2(dy, dx)
        step_rad = math.radians(PenTool.SHIFT_ANGLE_STEP)
        snapped = round(angle / step_rad) * step_rad
        length = math.sqrt(dx*dx + dy*dy)
        return (math.cos(snapped) * length, math.sin(snapped) * length)

    def _detect_hover_state(self, pos: QPointF, doc) -> int:
        """检测悬停位置，返回钢笔光标状态"""
        # 遍历所有可见图层的路径项
        for layer in reversed(doc.layers):
            if not layer.visible or layer.locked:
                continue
            for item in layer.items:
                if not isinstance(item, PathItem) or not item.visible or item.locked:
                    continue
                
                # 1) 检测锚点 → Pen-
                anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
                if anchor_idx >= 0:
                    # 如果是当前正在绘制的路径的锚点，继续判断
                    if item is self._current_path:
                        # 起始锚点 → Pen○ 闭合
                        if anchor_idx == 0 and len(item.anchors) >= 2:
                            return PenTool.PEN_CLOSE
                        # 端点 → Pen/ 继续
                        if anchor_idx == len(item.anchors) - 1:
                            return PenTool.PEN_CONTINUE
                    return PenTool.PEN_MINUS
                
                # 2) 检测路径段 → Pen+；检查鼠标局部坐标是否命中某条路径段
                seg_idx = item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)
                if seg_idx >= 0:
                    return PenTool.PEN_PLUS
        
        # 3) 如果当前有路径且接近起始点 → Pen○
        if self._current_path and len(self._current_path.anchors) >= 2:
            first = self._current_path.anchors[0]
            dist = math.sqrt((pos.x() - first.x)**2 + (pos.y() - first.y)**2)
            if dist < PenTool.CLOSE_TOLERANCE:
                return PenTool.PEN_CLOSE
        
        return PenTool.PEN_DEFAULT

    # ── 鼠标事件 ──

    def mouse_press(self, pos: QPointF, modifiers: int):
        if not self._document:
            return

        doc = self._document
        is_alt = bool(modifiers & Qt.AltModifier)
        is_ctrl = bool(modifiers & Qt.ControlModifier)
        is_shift = bool(modifiers & Qt.ShiftModifier)

        # ── Ctrl/Cmd 临时切换直接选择工具 ──
        if is_ctrl:
            self._ctrl_temp_select = True
            self._ctrl_drag_start = QPointF(pos)
            # 查找点击位置的路径项和锚点
            for layer in reversed(doc.layers):
                if not layer.visible or layer.locked:
                    continue
                for item in layer.items:
                    if not isinstance(item, PathItem) or not item.visible or item.locked:
                        continue
                    anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
                    if anchor_idx >= 0:
                        # 记录被拖拽手柄所属的锚点索引
                        self._dragged_anchor_idx = anchor_idx
                        # 临时将该路径设为当前编辑路径
                        self._current_path = item
                        return
            return

        # ── 检测悬停状态决定行为 ──
        # 检测悬停状态决定行为
        hover = self._detect_hover_state(pos, doc)

        # 悬停已有路径的锚点（非当前路径） → 删除锚点（Pen-）
        if hover == PenTool.PEN_MINUS:
            self._try_delete_anchor(pos, doc)
            return

        # 悬停已有路径段 → 添加锚点（Pen+）
        if hover == PenTool.PEN_PLUS:
            self._try_add_anchor(pos, doc)
            return

        # 悬停当前路径起始锚点 → 闭合路径（Pen○）
        if hover == PenTool.PEN_CLOSE and self._current_path:
            self._close_path()
            return

        # ── 正常绘制模式 ──
        # 如果没有当前路径，创建新路径
        if self._current_path is None:
            # 创建新的空白路径作为钢笔工具的当前绘制路径
            self._current_path = PathItem()
            self._current_path.style.fill_color = QColor(200, 200, 200, 100)
            self._current_path.style.stroke_color = QColor(50, 50, 50)
            self._current_path.style.stroke_width = 2.0
            doc.add_item(self._current_path)

        # 记录拖拽起始位置
        self._drag_start_pos = QPointF(pos)
        self._drawing = True

    def mouse_move(self, pos: QPointF, modifiers: int):
        if not self._document:
            return
        # 转换为布尔值，用于断开手柄对称约束
        is_alt = bool(modifiers & Qt.AltModifier)
        is_ctrl = bool(modifiers & Qt.ControlModifier)
        is_shift = bool(modifiers & Qt.ShiftModifier)
        is_space = bool(modifiers & Qt.Key_Space if hasattr(Qt, 'Key_Space') else False)

        # ── Ctrl 临时直接选择：移动锚点 ──
        if self._ctrl_temp_select and self._current_path and self._ctrl_drag_start:
            dx = pos.x() - self._ctrl_drag_start.x()
            dy = pos.y() - self._ctrl_drag_start.y()
            if self._dragged_anchor_idx >= 0 and self._dragged_anchor_idx < self._current_path.anchor_count:
                # 将钢笔工具正在绘制的路径上指定锚点移动到新位置
                self._current_path.move_anchor(
                    self._dragged_anchor_idx,
                    self._current_path.anchors[self._dragged_anchor_idx].x + dx,
                    self._current_path.anchors[self._dragged_anchor_idx].y + dy,
                )
            # 记录拖拽起始位置
            self._ctrl_drag_start = QPointF(pos)
            # 标记文档已被修改
            self._document.modified = True
            return

        # ── Space 移动当前锚点（仅在拖拽中） ──
        if self._space_moving and self._current_path and self._space_start_pos:
            dx = pos.x() - self._space_start_pos.x()
            dy = pos.y() - self._space_start_pos.y()
            last_idx = self._current_path.anchor_count - 1
            if last_idx >= 0:
                anchor = self._current_path.anchors[last_idx]
                self._current_path.move_anchor(last_idx, anchor.x + dx, anchor.y + dy)
            # 将钢笔工具正在绘制的路径上指定锚点移动到新位置
            self._space_start_pos = QPointF(pos)
            # 记录拖拽起始位置
            self._document.modified = True
            return

        # ── 更新悬停光标状态 ──
        if not self._drawing:
            # 获取当前缩放手柄对角的固定锚点坐标，作为缩放的固定参照点
            self._hover_state = self._detect_hover_state(pos, self._document)
            return

        # ── 拖拽中：实时更新最后一个锚点的手柄 ──，如果正在绘制中
        if self._drawing and self._drag_start_pos and self._current_path:
            # 计算当前路径最后一个锚点的索引
            last_idx = self._current_path.anchor_count - 1
            # 如果命中了锚点，手柄
            if last_idx >= 0:
                dx = pos.x() - self._drag_start_pos.x()
                dy = pos.y() - self._drag_start_pos.y()
                
                # Shift 约束角度
                if is_shift and (dx != 0 or dy != 0):
                    dx, dy = self._snap_angle(dx, dy)
                
                # 拖拽距离小于阈值：视为角点（无手柄）
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < PenTool.DRAG_THRESHOLD:
                    self._current_path.remove_handles(last_idx)
                else:
                    # 创建/更新手柄（平滑点）
                    if is_alt:
                        # Alt 键：仅设置 handle_out（单侧控制），handle_in 置空；
                        # 获取当前路径的最后一个锚点，保存到局部变量anchor用于修改手柄方向
                        anchor = self._current_path.anchors[last_idx]
                        anchor.handle_out = QPointF(dx, dy)
                        anchor.handle_in = None
                        anchor.anchor_type = AnchorPointType.CORNER
                        self._current_path._build_path()
                    else:
                        # 正常拖拽：创建对称平滑点；设置钢笔工具路径锚点的出方向贝塞尔控制手柄位置
                        self._current_path.set_handle_out(
                            last_idx, dx, dy, constrain_smooth=True
                        )
                # 标记文档已被修改
                self._document.modified = True

    def mouse_release(self, pos: QPointF, modifiers: int):
        if not self._document:
            return

        # ── Ctrl 临时直接选择：释放 ──
        if self._ctrl_temp_select:
            self._ctrl_temp_select = False
            self._ctrl_drag_start = None
            self._dragged_anchor_idx = -1
            return

        # ── Space 移动锚点：释放 ──
        if self._space_moving:
            self._space_moving = False
            self._space_start_pos = None
            return

        if not self._drawing or self._drag_start_pos is None:
            return

        is_alt = bool(modifiers & Qt.AltModifier)
        is_shift = bool(modifiers & Qt.ShiftModifier)

        dx = pos.x() - self._drag_start_pos.x()
        dy = pos.y() - self._drag_start_pos.y()
        
        # Shift 约束角度
        if is_shift and (dx != 0 or dy != 0):
            dx, dy = self._snap_angle(dx, dy)
        
        dist = math.sqrt(dx*dx + dy*dy)

        if self._current_path is None:
            # 不应该到这里
            self._drawing = False
            self._drag_start_pos = None
            return

        if dist < PenTool.DRAG_THRESHOLD:
            # ── 短拖拽/单击：创建角点（无手柄） ──
            anchor = AnchorPoint(pos.x(), pos.y(), anchor_type=AnchorPointType.CORNER)
            self._current_path.add_anchor(anchor)
        else:
            if is_alt:
                # ── Alt+拖拽：创建不对称点（只有 handle_out） ──；创建新锚点对象
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
        
        self._document.modified = True
        self._drawing = False
        self._drag_start_pos = None

    def mouse_double_click(self, pos: QPointF, modifiers: int):
        """双击结束路径（不闭合）"""
        if self._current_path:
            self._current_path.closed = False
            # 根据钢笔工具路径的锚点数据重新构建几何路径
            self._current_path._build_path()
            self._current_path = None
            self._drawing = False
            self._drag_start_pos = None

    # ── 键盘事件 ──

    def key_press(self, key: int, modifiers: int):
        # 键盘事件处理方法
        if key == Qt.Key_Escape:
            # Escape：取消当前路径
            if self._current_path and self._document:
                self._document.remove_item(self._current_path)
            self._current_path = None
            self._drawing = False
            self._drag_start_pos = None
            # 重置悬停状态默认钢笔
            self._hover_state = PenTool.PEN_DEFAULT
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            # Enter/Return：结束路径（不闭合）
            if self._current_path:
                self._current_path.closed = False
                self._current_path._build_path()
                self._current_path = None
                self._drawing = False
                self._drag_start_pos = None
                self._hover_state = PenTool.PEN_DEFAULT

    # ── 辅助操作 ──

    def _close_path(self):
        # 闭合当前正在绘制的路径，接收自身引用
        """闭合当前路径"""
        if self._current_path and len(self._current_path.anchors) >= 2:
            self._current_path.closed = True
            self._current_path._build_path()
        self._current_path = None
        self._drawing = False
        self._drag_start_pos = None

    def _try_delete_anchor(self, pos: QPointF, doc):
        # 尝试删除悬停位置的锚点
        """尝试删除悬停的锚点（Pen-行为）"""
        for layer in reversed(doc.layers):
            if not layer.visible or layer.locked:
                continue
            for item in list(layer.items):
                if not isinstance(item, PathItem) or not item.visible or item.locked:
                    continue
                # 检测鼠标局部坐标是否命中某个锚点，idx为命中锚点的索引
                anchor_idx = item.get_anchor_at(pos.x(), pos.y(), PenTool.ANCHOR_TOLERANCE)
                if anchor_idx >= 0 and item.anchor_count > 2:
                    old_anchors = [a.copy() for a in item.anchors]
                    item.remove_anchor(anchor_idx)
                    new_anchors = [a.copy() for a in item.anchors]
                    cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)
                    doc.execute_command(cmd)
                    return

    def _try_add_anchor(self, pos: QPointF, doc):
        """尝试在路径段上添加锚点（Pen+行为）"""
        for layer in reversed(doc.layers):
        # 逆序遍历文档的图层，优先处理顶层可见元素
            if not layer.visible or layer.locked:
                continue
            for item in list(layer.items):
                if not isinstance(item, PathItem) or not item.visible or item.locked:
                    continue
                # 检测鼠标局部坐标是否命中某条路径段
                seg_idx = item.get_segment_at(pos.x(), pos.y(), PenTool.SEGMENT_TOLERANCE)
                if seg_idx >= 0:
                    # 找到段上的精确插入位置
                    cx, cy = item.get_closest_point_on_segment(seg_idx, pos.x(), pos.y())
                    # 在段后插入新锚点
                    old_anchors = [a.copy() for a in item.anchors]
                    # 使用计算出的坐标创建新的角点锚点对象
                    new_anchor = AnchorPoint(cx, cy, anchor_type=AnchorPointType.CORNER)
                    item.insert_anchor(seg_idx + 1, new_anchor)
                    new_anchors = [a.copy() for a in item.anchors]
                    cmd = ModifyAnchorCommand(doc, item, old_anchors, new_anchors)
                    doc.execute_command(cmd)
                    return

    # ── 绘制预览 ──

    def draw_preview(self, painter: QPainter, editing_text=None):
        """绘制钢笔工具预览：
        - 已放置的锚点
        - 路径线段
        - 拖拽中的手柄预览
        - 悬停光标指示
        """
        if not self._current_path:
            return
        
        anchors = self._current_path.anchors
        if not anchors:
            return
        
        scale = max(painter.transform().m11(), 0.001)
        
        # ── 绘制已放置的锚点 ──；当前锚点序号，锚点对象
        for i, anchor in enumerate(anchors):
            pt = QPointF(anchor.x, anchor.y)
            
            # 锚点圆圈
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
            painter.setBrush(QColor(255, 255, 255))
            # 在指定矩形内绘制内切椭圆
            painter.drawEllipse(pt, 3 / scale, 3 / scale)
            
            # 手柄线（handle_in）；
            if anchor.handle_in:
                hin = QPointF(anchor.x + anchor.handle_in.x(), 
                             anchor.y + anchor.handle_in.y())
                pen = QPen(QColor(0, 120, 215), 0.8 / scale)
                pen.setStyle(Qt.DashLine)
                painter.setPen(pen)
                painter.drawLine(pt, hin)
                # 手柄端点
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))
                painter.drawEllipse(hin, 2.5 / scale, 2.5 / scale)
            
            # 手柄线（handle_out）
            if anchor.handle_out:
                hout = QPointF(anchor.x + anchor.handle_out.x(), 
                              anchor.y + anchor.handle_out.y())
                painter.setPen(QPen(QColor(0, 120, 215), 0.8 / scale))
                painter.drawLine(pt, hout)
                # 手柄端点
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(0, 120, 215), 1 / scale))
                painter.drawEllipse(hout, 2.5 / scale, 2.5 / scale)
        
        # ── 绘制路径线段 ──
        if len(anchors) >= 2:
            pen = QPen(QColor(0, 120, 215), 1.5 / scale)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            
            for i in range(len(anchors) - 1):
                prev, curr = anchors[i], anchors[i + 1]
                # 对相邻锚点构成的贝塞尔曲线段进行30次均匀采样
                samples = PathItem._sample_bezier_segment(prev, curr, num_samples=30)
                for k in range(len(samples) - 1):
                    p1 = QPointF(samples[k][0], samples[k][1])
                    p2 = QPointF(samples[k+1][0], samples[k+1][1])
                    painter.drawLine(p1, p2)
        
        # ── 拖拽中：绘制从最后一个锚点出发的预览手柄 ──
        if self._drawing and self._drag_start_pos:
            last_anchor = anchors[-1]
            # 将最后一个锚点的世界坐标保存到last_pt
            last_pt = QPointF(last_anchor.x, last_anchor.y)
            
            # 手柄线预览
            painter.setPen(QPen(QColor(0, 120, 215, 150), 0.8 / scale, Qt.DashLine))
            painter.drawLine(last_pt, self._drag_start_pos)
            
            # 预览锚点
            painter.setPen(QPen(QColor(0, 120, 215), 1.5 / scale))
            painter.setBrush(QColor(0, 120, 215, 100))
            painter.drawEllipse(self._drag_start_pos, 3 / scale, 3 / scale)
        
        # ── 悬停光标指示（在第一个锚点上绘制闭合图标） ──
        if self._hover_state == PenTool.PEN_CLOSE and len(anchors) >= 2:
            first_pt = QPointF(anchors[0].x, anchors[0].y)
            painter.setPen(QPen(QColor(0, 120, 215), 2 / scale))
            painter.setBrush(Qt.NoBrush)
            r = 6 / scale
            painter.drawEllipse(first_pt, r, r)
            # 在指定矩形内绘制内切椭圆

    def cancel(self):
        # 取消当前操作并重置状态
        if self._current_path and self._document:
            self._document.remove_item(self._current_path)
        self._current_path = None
        self._drawing = False
        self._drag_start_pos = None
        self._hover_state = PenTool.PEN_DEFAULT
        self._ctrl_temp_select = False
        self._space_moving = False
        super().cancel()


# ── 文字工具 ──────────────────────────────────────────────

class TextTool(BaseTool):
    """文字工具 —— 点击创建文字，再次点击已有文本框则进入编辑"""
    __slots__ = ('_pending_edit_item',)

    def __init__(self):
        super().__init__(ToolType.TEXT)
        self._pending_edit_item: TextFrame | None = None

    def mouse_press(self, pos: QPointF, modifiers: int):
        if not self._document:
            return
        # 先检测点击位置是否已有文本框
        item = self._document.get_item_at(pos.x(), pos.y())
        if isinstance(item, TextFrame):
            # 点击已有文本框 → 进入编辑状态，不创建新文本框
            self._document.clear_selection()
            item.selected = False  # 编辑状态下不显示选中边框
            self._pending_edit_item = item
            self._document.modified = True
            return
        # 点击空白区域 → 创建新文本框
        text_frame = TextFrame(pos.x(), pos.y())
        text_frame.contents = "文字"
        text_frame.char_attrs.font_size = 24
        text_frame.char_attrs.fill_color = QColor(50, 50, 50)
        text_frame.style.fill_color = None
        text_frame.selected = True
        self._document.clear_selection()
        self._document.add_item(text_frame)
        self._document.modified = True

    def mouse_double_click(self, pos: QPointF, modifiers: int):
        pass  # 由 UI 层处理

    def consume_pending_edit_item(self) -> TextFrame | None:
        """消费并返回待编辑的文本框（由 CanvasWidget 调用）"""
        item = self._pending_edit_item
        self._pending_edit_item = None
        return item

    @property
    def pending_edit_item(self) -> TextFrame | None:
        """返回需要进入编辑状态的文本框（只读，不消费）"""
        return self._pending_edit_item


# ── 抓手工具 ──────────────────────────────────────────────

class HandTool(BaseTool):
    """抓手工具 —— 拖拽平移画布"""
    __slots__ = ()

    def __init__(self):
        super().__init__(ToolType.HAND)
