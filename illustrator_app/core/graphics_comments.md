# graphics.py 中文注解翻译

---

```python
"""
Illustrator 核心图形引擎 (Python 3.10+)
```
# 模块文档字符串：Illustrator 核心图形引擎（要求 Python 3.10 及以上版本）

```python

定义所有图形对象的数据模型：路径、矩形、椭圆、文字、编组等
```
# 定义所有图形对象的数据模型：路径、矩形、椭圆、文字、编组等

```python
支持贝塞尔曲线、渐变、布尔运算等高级特性
```
# 支持贝塞尔曲线、渐变、布尔运算等高级特性

```python

架构优化 (v2.0):
```
# 架构优化（版本 2.0）：

```python
- 使用 __slots__ 减少内存占用
```
# - 使用 \_\_slots\_\_ 减少内存占用

```python
- 使用 dataclass(slots=True) (Python 3.10+)
```
# - 使用 dataclass(slots=True)（Python 3.10+）

```python
- 使用 X | None 替代 Optional[X] (Python 3.10+)
```
# - 使用 X | None 替代 Optional[X]（Python 3.10+）

```python
- 使用 match-case 替代 if-elif 链 (Python 3.10+)
```
# - 使用 match-case 替代 if-elif 链（Python 3.10+）

```python
- 使用 KW_ONLY 改善 dataclass 可读性 (Python 3.10+)
```
# - 使用 KW_ONLY 改善 dataclass 可读性（Python 3.10+）

```python
- 统一的 ABC 基类设计
```
# - 统一的抽象基类（ABC）设计

```python
- 命令模式 + 撤销/重做系统
```
# - 命令模式 + 撤销/重做系统

```python
"""
```
# 模块文档字符串结束

---

```python
from __future__ import annotations
```
# 从 \_\_future\_\_ 模块导入 annotations，启用延迟注解求值（允许在类型注解中使用未定义的类型）

```python

import math
```
# 导入 math 数学运算库

```python
import uuid
```
# 导入 uuid 通用唯一标识符生成库

```python
import copy
```
# 导入 copy 对象拷贝库

```python
from abc import ABC, abstractmethod
```
# 从 abc 模块导入抽象基类（ABC）和抽象方法装饰器（abstractmethod）

```python
from dataclasses import dataclass, field, KW_ONLY
```
# 从 dataclasses 模块导入数据类装饰器（dataclass）、字段默认工厂（field）和仅关键字参数标记（KW_ONLY）

```python
from enum import Enum, auto
```
# 从 enum 模块导入枚举类（Enum）和自动赋值工具（auto）

```python
from typing import TypeAlias
```
# 从 typing 模块导入类型别名工具（TypeAlias）

```python

from PyQt5.QtCore import QPointF, QRectF
```
# 从 PyQt5.QtCore 导入二维浮点坐标点（QPointF）和浮点矩形区域（QRectF）

```python
from PyQt5.QtGui import (
```
# 从 PyQt5.QtGui 导入以下图形相关类：

```python
    QColor, QPainterPath, QTransform, QPen, QBrush,
```
#     颜色类（QColor）、绘图路径类（QPainterPath）、变换矩阵类（QTransform）、画笔类（QPen）、画刷类（QBrush）、

```python
    QFont, QLinearGradient, QRadialGradient, QGradient,
```
#     字体类（QFont）、线性渐变类（QLinearGradient）、径向渐变类（QRadialGradient）、渐变基类（QGradient）

```python
)
```
# 结束多行导入语句

---

```python

# ── 类型别名 (Python 3.10+) ──────────────────────────────────
```
# ── 类型别名（Python 3.10+）分隔线 ──

```python

ColorTuple: TypeAlias = tuple[int, int, int, int]
```
# 定义颜色元组类型别名：由四个整数组成的元组（红、绿、蓝、透明度，各 0-255）

```python
PointTuple: TypeAlias = tuple[float, float]
```
# 定义点坐标元组类型别名：由两个浮点数组成的元组（x、y 坐标）

---

```python

# ── 枚举常量 ────────────────────────────────────────────────
```
# ── 枚举常量分隔线 ──

```python

class BlendMode(Enum):
```
# 定义混合模式枚举类，继承自 Enum

```python
    """混合模式"""
```
#     类文档字符串：混合模式

```python
    NORMAL = auto()
```
#     正常模式，自动赋值

```python
    MULTIPLY = auto()
```
#     正片叠底模式，自动赋值

```python
    SCREEN = auto()
```
#     滤色模式，自动赋值

```python
    OVERLAY = auto()
```
#     叠加模式，自动赋值

```python
    DARKEN = auto()
```
#     变暗模式，自动赋值

```python
    LIGHTEN = auto()
```
#     变亮模式，自动赋值

```python
    COLOR_DODGE = auto()
```
#     颜色减淡模式，自动赋值

```python
    COLOR_BURN = auto()
```
#     颜色加深模式，自动赋值

```python
    HARD_LIGHT = auto()
```
#     强光模式，自动赋值

```python
    SOFT_LIGHT = auto()
```
#     柔光模式，自动赋值

```python
    DIFFERENCE = auto()
```
#     差值模式，自动赋值

```python
    EXCLUSION = auto()
```
#     排除模式，自动赋值

---

```python

class TextType(Enum):
```
# 定义文字类型枚举类，继承自 Enum

```python
    """文字类型"""
```
#     类文档字符串：文字类型

```python
    POINT_TEXT = auto()
```
#     点文字（无边界框），自动赋值

```python
    AREA_TEXT = auto()
```
#     区域文字（有边界框），自动赋值

```python
    PATH_TEXT = auto()
```
#     路径文字（沿路径排列），自动赋值

---

```python

class Justification(Enum):
```
# 定义对齐方式枚举类，继承自 Enum

```python
    """对齐方式"""
```
#     类文档字符串：对齐方式

```python
    LEFT = auto()
```
#     左对齐，自动赋值

```python
    CENTER = auto()
```
#     居中对齐，自动赋值

```python
    RIGHT = auto()
```
#     右对齐，自动赋值

```python
    JUSTIFY = auto()
```
#     两端对齐，自动赋值

---

```python

class StrokeCap(Enum):
```
# 定义线端点样式枚举类，继承自 Enum

```python
    """线端点样式"""
```
#     类文档字符串：线端点样式

```python
    BUTT = auto()
```
#     平头端点（无延伸），自动赋值

```python
    ROUND = auto()
```
#     圆头端点（半圆延伸），自动赋值

```python
    SQUARE = auto()
```
#     方头端点（方形延伸），自动赋值

---

```python

class StrokeJoin(Enum):
```
# 定义线连接样式枚举类，继承自 Enum

```python
    """线连接样式"""
```
#     类文档字符串：线连接样式

```python
    MITER = auto()
```
#     尖角连接（斜接），自动赋值

```python
    ROUND = auto()
```
#     圆角连接，自动赋值

```python
    BEVEL = auto()
```
#     斜角连接（平切），自动赋值

---

```python

class FillRule(Enum):
```
# 定义填充规则枚举类，继承自 Enum

```python
    """填充规则"""
```
#     类文档字符串：填充规则

```python
    NON_ZERO = auto()
```
#     非零绕组规则，自动赋值

```python
    EVEN_ODD = auto()
```
#     奇偶规则，自动赋值

---

```python

class GradientType(Enum):
```
# 定义渐变类型枚举类，继承自 Enum

```python
    """渐变类型"""
```
#     类文档字符串：渐变类型

```python
    LINEAR = auto()
```
#     线性渐变，自动赋值

```python
    RADIAL = auto()
```
#     径向渐变，自动赋值

---

```python

class AnchorPointType(Enum):
```
# 定义锚点类型枚举类，继承自 Enum

```python
    """锚点类型"""
```
#     类文档字符串：锚点类型

```python
    CORNER = auto()
```
#     角点（手柄独立控制），自动赋值

```python
    SMOOTH = auto()
```
#     平滑点（手柄共线等距），自动赋值

```python
    ASYMMETRIC = auto()
```
#     不对称点（手柄共线但不等距），自动赋值

---

```python

# ── 渐变系统 ────────────────────────────────────────────────
```
# ── 渐变系统分隔线 ──

```python

@dataclass(slots=True)
class GradientStop:
```
# 使用 dataclass 装饰器（启用 slots 优化）定义渐变色标类

```python
    """渐变色标"""
```
#     类文档字符串：渐变色标

```python
    position: float     # 0.0 ~ 1.0
```
#     色标位置（浮点数），取值范围 0.0 到 1.0

```python
    color: QColor
```
#     色标颜色（QColor 颜色对象）

```python
    opacity: float = 1.0
```
#     色标不透明度（浮点数），默认值为 1.0（完全不透明）

---

```python

@dataclass
class Gradient:
```
# 使用 dataclass 装饰器定义渐变定义类

```python
    """渐变定义"""
```
#     类文档字符串：渐变定义

```python
    gradient_type: GradientType = GradientType.LINEAR
```
#     渐变类型（GradientType 枚举），默认为线性渐变

```python
    stops: list[GradientStop] = field(default_factory=list)
```
#     色标列表（GradientStop 列表），使用工厂函数默认创建空列表

```python
    angle: float = 0.0
```
#     渐变角度（浮点数），默认为 0.0 度

```python
    start_point: QPointF = field(default_factory=lambda: QPointF(0, 0))
```
#     渐变起始点（QPointF 坐标），默认为 (0, 0)

```python
    end_point: QPointF = field(default_factory=lambda: QPointF(1, 1))
```
#     渐变终止点（QPointF 坐标），默认为 (1, 1)

```python
    center: QPointF = field(default_factory=lambda: QPointF(0.5, 0.5))
```
#     径向渐变中心点（QPointF 坐标），默认为 (0.5, 0.5)

```python
    radius: float = 0.5
```
#     径向渐变半径（浮点数），默认为 0.5

```python

    @staticmethod
    def default_linear() -> Gradient:
```
#     定义静态方法：创建默认线性渐变，返回渐变对象

```python
        return Gradient(
```
#         返回一个渐变实例，配置如下：

```python
            stops=[
```
#             色标列表包含：

```python
                GradientStop(0.0, QColor(255, 255, 255)),
```
#                 位置 0.0 处的白色色标

```python
                GradientStop(1.0, QColor(0, 0, 0)),
```
#                 位置 1.0 处的黑色色标

```python
            ],
```
#             色标列表结束

```python
        )
```
#         渐变实例构造结束

```python

    @staticmethod
    def default_radial() -> Gradient:
```
#     定义静态方法：创建默认径向渐变，返回渐变对象

```python
        return Gradient(
```
#         返回一个渐变实例，配置如下：

```python
            gradient_type=GradientType.RADIAL,
```
#             渐变类型设为径向渐变

```python
            stops=[
```
#             色标列表包含：

```python
                GradientStop(0.0, QColor(255, 255, 255)),
```
#                 位置 0.0 处的白色色标

```python
                GradientStop(1.0, QColor(0, 0, 0)),
```
#                 位置 1.0 处的黑色色标

```python
            ],
```
#             色标列表结束

```python
            center=QPointF(0.5, 0.5),
```
#             中心点设为 (0.5, 0.5)

```python
            radius=0.5,
```
#             半径设为 0.5

```python
        )
```
#         渐变实例构造结束

```python

    def to_qgradient(self, rect: QRectF) -> QGradient:
```
#     定义实例方法：根据目标矩形创建 Qt 渐变对象（接收目标矩形参数，返回 QGradient 对象）

```python
        """根据目标矩形创建 QGradient"""
```
#         方法文档字符串：根据目标矩形创建 QGradient

```python
        if self.gradient_type is GradientType.LINEAR:
```
#         如果渐变类型为线性渐变：

```python
            rad = math.radians(self.angle)
```
#             将角度转换为弧度

```python
            cx, cy = rect.center().x(), rect.center().y()
```
#             获取矩形中心的 x、y 坐标

```python
            half_w, half_h = rect.width() / 2, rect.height() / 2
```
#             计算矩形的半宽和半高

```python
            dx = math.cos(rad) * half_w
```
#             根据弧度计算 x 方向偏移量

```python
            dy = math.sin(rad) * half_h
```
#             根据弧度计算 y 方向偏移量

```python
            start = QPointF(cx - dx, cy - dy)
```
#             计算线性渐变起始点坐标

```python
            end = QPointF(cx + dx, cy + dy)
```
#             计算线性渐变终止点坐标

```python
            grad = QLinearGradient(start, end)
```
#             创建线性渐变对象

```python
        else:
```
#         否则（径向渐变）：

```python
            grad = QRadialGradient(
```
#             创建径向渐变对象，参数如下：

```python
                rect.x() + self.center.x() * rect.width(),
```
#                 径向渐变中心 x 坐标

```python
                rect.y() + self.center.y() * rect.height(),
```
#                 径向渐变中心 y 坐标

```python
                self.radius * max(rect.width(), rect.height()),
```
#                 径向渐变半径

```python
            )
```
#             径向渐变构造结束

```python
        for stop in self.stops:
```
#         遍历所有色标：

```python
            c = QColor(stop.color)
```
#             复制色标颜色

```python
            c.setAlphaF(stop.opacity)
```
#             设置色标不透明度

```python
            grad.setColorAt(stop.position, c)
```
#             在渐变对象的指定位置设置颜色

```python
        return grad
```
#         返回 Qt 渐变对象

---

```python

# ── 贝塞尔曲线锚点 ──────────────────────────────────────────
```
# ── 贝塞尔曲线锚点分隔线 ──

```python

@dataclass(slots=True)
class AnchorPoint:
```
# 使用 dataclass 装饰器（启用 slots 优化）定义贝塞尔曲线锚点类

```python
    """贝塞尔曲线锚点（含两个控制手柄）
```
#     类文档字符串：贝塞尔曲线锚点（含两个控制手柄）

```python
    
    对照 Adobe Illustrator 锚点行为：
```
#     对照 Adobe Illustrator 锚点行为：

```python
    - CORNER（角点）：handle_in 和 handle_out 独立控制，方向任意
```
#     - CORNER（角点）：入控制手柄和出控制手柄独立控制，方向任意

```python
    - SMOOTH（平滑点）：handle_in 和 handle_out 共线等距，保持对称
```
#     - SMOOTH（平滑点）：入控制手柄和出控制手柄共线且等距，保持对称

```python
    - ASYMMETRIC（不对称点）：handle_in 和 handle_out 共线但不等距
```
#     - ASYMMETRIC（不对称点）：入控制手柄和出控制手柄共线但不等距

```python
    
    handle_in/out 存储的是相对于锚点的偏移量。
```
#     handle_in/handle_out 存储的是相对于锚点的偏移量。

```python
    例如：锚点在 (100,100)，handle_out = (50, -30)，则手柄在世界空间位于 (150, 70)
```
#     例如：锚点在 (100,100)，handle_out = (50, -30)，则手柄在世界空间位于 (150, 70)

```python
    """
```
#     类文档字符串结束

```python
    x: float = 0.0
```
#     锚点 x 坐标（浮点数），默认为 0.0

```python
    y: float = 0.0
```
#     锚点 y 坐标（浮点数），默认为 0.0

```python
    handle_in: QPointF | None = None
```
#     入控制手柄偏移量（QPointF 或 None），默认为 None（无手柄）

```python
    handle_out: QPointF | None = None
```
#     出控制手柄偏移量（QPointF 或 None），默认为 None（无手柄）

```python
    anchor_type: AnchorPointType = AnchorPointType.CORNER
```
#     锚点类型（AnchorPointType 枚举），默认为角点

```python

    @property
    def pos(self) -> QPointF:
```
#     定义只读属性：获取锚点位置坐标，返回 QPointF

```python
        return QPointF(self.x, self.y)
```
#         返回由 x、y 坐标构造的 QPointF 对象

```python

    @property
    def has_handles(self) -> bool:
```
#     定义只读属性：判断是否有贝塞尔手柄，返回布尔值

```python
        """是否有贝塞尔手柄"""
```
#         属性文档字符串：是否有贝塞尔手柄

```python
        return self.handle_in is not None or self.handle_out is not None
```
#         返回入控制手柄或出控制手柄是否存在

```python

    def handle_in_abs(self) -> QPointF | None:
```
#     定义实例方法：获取入控制手柄的绝对世界坐标，返回 QPointF 或 None

```python
        """获取 handle_in 的绝对世界坐标"""
```
#         方法文档字符串：获取 handle_in 的绝对世界坐标

```python
        if self.handle_in is None:
```
#         如果入控制手柄为 None：

```python
            return None
```
#             返回 None

```python
        return QPointF(self.x + self.handle_in.x(), self.y + self.handle_in.y())
```
#         返回锚点坐标加上手柄偏移量得到的绝对世界坐标

```python

    def handle_out_abs(self) -> QPointF | None:
```
#     定义实例方法：获取出控制手柄的绝对世界坐标，返回 QPointF 或 None

```python
        """获取 handle_out 的绝对世界坐标"""
```
#         方法文档字符串：获取 handle_out 的绝对世界坐标

```python
        if self.handle_out is None:
```
#         如果出控制手柄为 None：

```python
            return None
```
#             返回 None

```python
        return QPointF(self.x + self.handle_out.x(), self.y + self.handle_out.y())
```
#         返回锚点坐标加上手柄偏移量得到的绝对世界坐标

```python

    def copy(self) -> AnchorPoint:
```
#     定义实例方法：复制锚点，返回新的 AnchorPoint 对象

```python
        return AnchorPoint(
```
#         返回一个新的锚点实例，参数如下：

```python
            self.x, self.y,
```
#             x、y 坐标复制自当前锚点

```python
            QPointF(self.handle_in) if self.handle_in else None,
```
#             入控制手柄：若存在则复制，否则为 None

```python
            QPointF(self.handle_out) if self.handle_out else None,
```
#             出控制手柄：若存在则复制，否则为 None

```python
            self.anchor_type,
```
#             锚点类型复制自当前锚点

```python
        )
```
#         锚点实例构造结束

```python

    # ── 锚点类型转换（对照 AI 的 Convert Anchor Point Tool 行为）──
```
#     注释：锚点类型转换（对照 AI 的转换锚点工具行为）

```python

    def convert_to_corner(self):
```
#     定义实例方法：转换为角点

```python
        """转换为角点：保留现有手柄但允许独立控制
```
#         方法文档字符串：转换为角点：保留现有手柄但允许独立控制

```python
        
        在 AI 中，Convert Anchor Point Tool 点击平滑点会变为角点
```
#         在 AI 中，转换锚点工具点击平滑点会变为角点

```python
        （手柄保留但不再受对称约束）
```
#         （手柄保留但不再受对称约束）

```python
        """
```
#         方法文档字符串结束

```python
        self.anchor_type = AnchorPointType.CORNER
```
#         将锚点类型设为角点

```python

    def convert_to_smooth(self):
```
#     定义实例方法：转换为平滑点

```python
        """转换为平滑点：使两个手柄共线等距
```
#         方法文档字符串：转换为平滑点：使两个手柄共线等距

```python
        
        在 AI 中，Convert Anchor Point Tool 拖拽角点会拉出手柄并转为平滑点。
```
#         在 AI 中，转换锚点工具拖拽角点会拉出手柄并转为平滑点。

```python
        如果只有一个手柄，则镜像生成另一个。
```
#         如果只有一个手柄，则镜像生成另一个。

```python
        如果两个手柄都存在，则让它们共线且等距。
```
#         如果两个手柄都存在，则让它们共线且等距。

```python
        """
```
#         方法文档字符串结束

```python
        if self.handle_in is None and self.handle_out is None:
```
#         如果入控制手柄和出控制手柄都为 None：

```python
            # 没有手柄：不创建（需要在工具层拖拽创建）
```
#             注释：没有手柄：不创建（需要在工具层拖拽创建）

```python
            self.anchor_type = AnchorPointType.SMOOTH
```
#             仅将锚点类型设为平滑点

```python
            return
```
#             提前返回

```python
        
        if self.handle_in is None and self.handle_out is not None:
```
#         如果只有出控制手柄：

```python
            # 只有 handle_out：镜像生成 handle_in
```
#             注释：只有出控制手柄：镜像生成入控制手柄

```python
            self.handle_in = QPointF(-self.handle_out.x(), -self.handle_out.y())
```
#             将出控制手柄取反生成入控制手柄

```python
        elif self.handle_out is None and self.handle_in is not None:
```
#         否则如果只有入控制手柄：

```python
            # 只有 handle_in：镜像生成 handle_out
```
#             注释：只有入控制手柄：镜像生成出控制手柄

```python
            self.handle_out = QPointF(-self.handle_in.x(), -self.handle_in.y())
```
#             将入控制手柄取反生成出控制手柄

```python
        else:
```
#         否则（两个手柄都存在）：

```python
            # 两个都有：让它们共线等距
```
#             注释：两个都有：让它们共线等距

```python
            # 取两个手柄的平均方向，让它们等距分布
```
#             注释：取两个手柄的平均方向，让它们等距分布

```python
            in_len = math.sqrt(self.handle_in.x()**2 + self.handle_in.y()**2)
```
#             计算入控制手柄的长度

```python
            out_len = math.sqrt(self.handle_out.x()**2 + self.handle_out.y()**2)
```
#             计算出控制手柄的长度

```python
            avg_len = (in_len + out_len) / 2.0 if (in_len > 0 and out_len > 0) else max(in_len, out_len)
```
#             计算平均长度（若两个手柄都大于 0 则取平均值，否则取较大值）

```python
            if out_len > 0:
```
#             如果出控制手柄长度大于 0：

```python
                dx = self.handle_out.x()
```
#                 获取出控制手柄 x 分量

```python
                dy = self.handle_out.y()
```
#                 获取出控制手柄 y 分量

```python
                ol = math.sqrt(dx*dx + dy*dy)
```
#                 计算出控制手柄的长度

```python
                if ol > 0.001:
```
#                 如果长度大于极小值 0.001（避免除零）：

```python
                    dx, dy = dx / ol, dy / ol
```
#                     将方向向量归一化

```python
                    self.handle_out = QPointF(dx * avg_len, dy * avg_len)
```
#                     设置出控制手柄为归一化方向乘以平均长度

```python
                    self.handle_in = QPointF(-dx * avg_len, -dy * avg_len)
```
#                     设置入控制手柄为反方向等长
        
```python
        self.anchor_type = AnchorPointType.SMOOTH
```
#         将锚点类型设为平滑点

```python

    def enforce_smooth_constraint(self, moved_handle: str):
```
#     定义实例方法：平滑点约束——当拖拽一个手柄时自动调整另一个手柄保持共线等距（接收被移动手柄标识字符串）

```python
        """平滑点约束：当拖拽一个手柄时，自动调整另一个手柄保持共线等距
```
#         方法文档字符串：平滑点约束：当拖拽一个手柄时，自动调整另一个手柄保持共线等距

```python
        
        Args:
```
#         参数说明：

```python
            moved_handle: 'in' 或 'out'，表示哪个手柄被移动
```
#             moved_handle：'in' 或 'out'，表示哪个手柄被移动

```python
        """
```
#         方法文档字符串结束

```python
        if self.anchor_type != AnchorPointType.SMOOTH:
```
#         如果锚点类型不是平滑点：

```python
            return
```
#             提前返回（无需约束）

```python
        
        if moved_handle == 'out' and self.handle_out is not None:
```
#         如果出控制手柄被移动且不为 None：

```python
            # handle_out 被移动，同步 handle_in
```
#             注释：出控制手柄被移动，同步入控制手柄

```python
            dx, dy = self.handle_out.x(), self.handle_out.y()
```
#             获取出控制手柄的 x、y 偏移分量

```python
            length = math.sqrt(dx*dx + dy*dy)
```
#             计算出控制手柄长度

```python
            if length > 0.001:
```
#             如果长度大于极小值 0.001：

```python
                dx, dy = dx / length, dy / length
```
#                 将方向向量归一化

```python
                # handle_in 是反方向，等长
```
#                 注释：入控制手柄是反方向，等长

```python
                in_len = math.sqrt(
```
#                 计算入控制手柄当前长度：

```python
                    self.handle_in.x()**2 + self.handle_in.y()**2
```
#                     入控制手柄 x、y 分量的平方和再开方

```python
                ) if self.handle_in else length
```
#                 若入控制手柄存在则计算，否则使用出控制手柄长度

```python
                # 使用 handle_out 的长度（AI 行为：以拖拽的手柄为准）
```
#                 注释：使用出控制手柄的长度（AI 行为：以拖拽的手柄为准）

```python
                self.handle_in = QPointF(-dx * length, -dy * length)
```
#                 设置入控制手柄为反方向等长
        
```python
        elif moved_handle == 'in' and self.handle_in is not None:
```
#         否则如果入控制手柄被移动且不为 None：

```python
            # handle_in 被移动，同步 handle_out
```
#             注释：入控制手柄被移动，同步出控制手柄

```python
            dx, dy = self.handle_in.x(), self.handle_in.y()
```
#             获取入控制手柄的 x、y 偏移分量

```python
            length = math.sqrt(dx*dx + dy*dy)
```
#             计算入控制手柄长度

```python
            if length > 0.001:
```
#             如果长度大于极小值 0.001：

```python
                dx, dy = dx / length, dy / length
```
#                 将方向向量归一化

```python
                self.handle_out = QPointF(-dx * length, -dy * length)
```
#                 设置出控制手柄为反方向等长

```python

    def remove_handles(self):
```
#     定义实例方法：移除所有手柄，转换为角点

```python
        """移除所有手柄，转换为角点（AI：点击角点工具点击锚点）"""
```
#         方法文档字符串：移除所有手柄，转换为角点（AI：点击角点工具点击锚点）

```python
        self.handle_in = None
```
#         将入控制手柄设为 None

```python
        self.handle_out = None
```
#         将出控制手柄设为 None

```python
        self.anchor_type = AnchorPointType.CORNER
```
#         将锚点类型设为角点

```python

    def to_dict(self) -> dict:
```
#     定义实例方法：将锚点序列化为字典，返回字典

```python
        return {
```
#         返回包含以下键值对的字典：

```python
            "x": self.x, "y": self.y,
```
#             x 坐标和 y 坐标

```python
            "handle_in": [self.handle_in.x(), self.handle_in.y()] if self.handle_in else None,
```
#             入控制手柄坐标列表（若存在），否则为 None

```python
            "handle_out": [self.handle_out.x(), self.handle_out.y()] if self.handle_out else None,
```
#             出控制手柄坐标列表（若存在），否则为 None

```python
            "type": self.anchor_type.name,
```
#             锚点类型名称字符串

```python
        }
```
#         字典构造结束

```python

    @staticmethod
    def from_dict(data: dict) -> AnchorPoint:
```
#     定义静态方法：从字典反序列化为锚点对象（接收字典参数，返回 AnchorPoint）

```python
        hi = data.get("handle_in")
```
#         获取字典中的入控制手柄数据

```python
        ho = data.get("handle_out")
```
#         获取字典中的出控制手柄数据

```python
        return AnchorPoint(
```
#         返回一个锚点实例，参数如下：

```python
            data.get("x", 0), data.get("y", 0),
```
#             x、y 坐标（默认为 0）

```python
            QPointF(hi[0], hi[1]) if hi else None,
```
#             入控制手柄（若存在则构造 QPointF，否则为 None）

```python
            QPointF(ho[0], ho[1]) if ho else None,
```
#             出控制手柄（若存在则构造 QPointF，否则为 None）

```python
            AnchorPointType[data.get("type", "CORNER")],
```
#             锚点类型（默认为角点）

```python
        )
```
#         锚点实例构造结束

---

```python

# ── 样式系统 ────────────────────────────────────────────────
```
# ── 样式系统分隔线 ──

```python

@dataclass(slots=True)
class GraphicStyle:
```
# 使用 dataclass 装饰器（启用 slots 优化）定义图形样式类

```python
    """图形样式"""
```
#     类文档字符串：图形样式

```python
    fill_color: QColor | None = None
```
#     填充颜色（QColor 或 None），默认为 None

```python
    fill_gradient: Gradient | None = None
```
#     填充渐变（Gradient 或 None），默认为 None

```python
    fill_opacity: float = 1.0
```
#     填充不透明度（浮点数），默认为 1.0

```python
    stroke_color: QColor | None = None
```
#     描边颜色（QColor 或 None），默认为 None

```python
    stroke_width: float = 1.0
```
#     描边宽度（浮点数），默认为 1.0

```python
    stroke_opacity: float = 1.0
```
#     描边不透明度（浮点数），默认为 1.0

```python
    stroke_cap: StrokeCap = StrokeCap.BUTT
```
#     线端点样式（StrokeCap 枚举），默认为平头

```python
    stroke_join: StrokeJoin = StrokeJoin.MITER
```
#     线连接样式（StrokeJoin 枚举），默认为尖角

```python
    stroke_dash: list[float] = field(default_factory=list)
```
#     虚线模式（浮点数列表），使用工厂函数默认创建空列表

```python
    fill_rule: FillRule = FillRule.NON_ZERO
```
#     填充规则（FillRule 枚举），默认为非零绕组规则

```python

    def copy(self) -> GraphicStyle:
```
#     定义实例方法：复制图形样式，返回新的 GraphicStyle 对象

```python
        return copy.deepcopy(self)
```
#         返回当前样式对象的深拷贝

```python

    def to_qpen(self) -> QPen:
```
#     定义实例方法：转换为 Qt 画笔对象，返回 QPen

```python
        pen = QPen()
```
#         创建一个空画笔对象

```python
        if self.stroke_color:
```
#         如果设置了描边颜色：

```python
            c = QColor(self.stroke_color)
```
#             复制描边颜色

```python
            c.setAlphaF(self.stroke_opacity)
```
#             设置颜色的不透明度

```python
            pen.setColor(c)
```
#             将颜色应用到画笔

```python
        else:
```
#         否则（无描边颜色）：

```python
            pen.setColor(QColor(0, 0, 0, 0))
```
#             设置画笔颜色为全透明（不可见）

```python
        pen.setWidthF(self.stroke_width)
```
#         设置画笔宽度

```python
        pen.setCapStyle(_cap_to_qt(self.stroke_cap))
```
#         设置画笔端点样式（通过辅助函数转换）

```python
        pen.setJoinStyle(_join_to_qt(self.stroke_join))
```
#         设置画笔连接样式（通过辅助函数转换）

```python
        if self.stroke_dash:
```
#         如果设置了虚线模式：

```python
            pen.setStyle(0x02)  # DashLine
```
#             设置画笔样式为虚线（0x02 为 Qt 虚线常量）

```python
            pen.setDashPattern(self.stroke_dash)
```
#             设置虚线间距模式

```python
        return pen
```
#         返回配置好的画笔对象

```python

    def to_qbrush(self) -> QBrush:
```
#     定义实例方法：转换为 Qt 画刷对象，返回 QBrush

```python
        if self.fill_color:
```
#         如果设置了填充颜色：

```python
            c = QColor(self.fill_color)
```
#             复制填充颜色

```python
            c.setAlphaF(self.fill_opacity)
```
#             设置颜色的不透明度

```python
            return QBrush(c)
```
#             返回使用该颜色构造的画刷

```python
        return QBrush()
```
#         否则返回空画刷（无填充）

```python

    def has_fill(self) -> bool:
```
#     定义实例方法：判断是否有填充，返回布尔值

```python
        return self.fill_color is not None or self.fill_gradient is not None
```
#         返回填充颜色或填充渐变是否存在

---

```python

def _cap_to_qt(cap: StrokeCap) -> int:
```
# 定义模块级辅助函数：将线端点样式枚举转换为 Qt 常量整数（接收 StrokeCap 枚举参数，返回 int）

```python
    """将 StrokeCap 转换为 Qt 常量 (match-case, Python 3.10+)"""
```
#     函数文档字符串：将 StrokeCap 转换为 Qt 常量（使用 match-case，Python 3.10+）

```python
    match cap:
```
#     使用 match-case 匹配线端点样式：

```python
        case StrokeCap.BUTT:
```
#         当为平头端点时：

```python
            return 0x00
```
#             返回 Qt 平头常量 0x00

```python
        case StrokeCap.ROUND:
```
#         当为圆头端点时：

```python
            return 0x01
```
#             返回 Qt 圆头常量 0x01

```python
        case StrokeCap.SQUARE:
```
#         当为方头端点时：

```python
            return 0x02
```
#             返回 Qt 方头常量 0x02

---

```python

def _join_to_qt(join: StrokeJoin) -> int:
```
# 定义模块级辅助函数：将线连接样式枚举转换为 Qt 常量整数（接收 StrokeJoin 枚举参数，返回 int）

```python
    """将 StrokeJoin 转换为 Qt 常量 (match-case, Python 3.10+)"""
```
#     函数文档字符串：将 StrokeJoin 转换为 Qt 常量（使用 match-case，Python 3.10+）

```python
    match join:
```
#     使用 match-case 匹配线连接样式：

```python
        case StrokeJoin.MITER:
```
#         当为尖角连接时：

```python
            return 0x00
```
#             返回 Qt 尖角常量 0x00

```python
        case StrokeJoin.ROUND:
```
#         当为圆角连接时：

```python
            return 0x01
```
#             返回 Qt 圆角常量 0x01

```python
        case StrokeJoin.BEVEL:
```
#         当为斜角连接时：

```python
            return 0x02
```
#             返回 Qt 斜角常量 0x02

---

```python

@dataclass(slots=True)
class CharacterAttributes:
```
# 使用 dataclass 装饰器（启用 slots 优化）定义字符属性类

```python
    """字符属性"""
```
#     类文档字符串：字符属性

```python
    font_family: str = "Arial"
```
#     字体族名称（字符串），默认为 "Arial"

```python
    font_size: float = 12.0
```
#     字号大小（浮点数），默认为 12.0

```python
    bold: bool = False
```
#     是否加粗（布尔值），默认为否

```python
    italic: bool = False
```
#     是否斜体（布尔值），默认为否

```python
    underline: bool = False
```
#     是否下划线（布尔值），默认为否

```python
    strikethrough: bool = False
```
#     是否删除线（布尔值），默认为否

```python
    fill_color: QColor | None = None
```
#     字符填充颜色（QColor 或 None），默认为 None

```python
    tracking: float = 0.0
```
#     字符间距（浮点数），默认为 0.0

```python
    leading: float = 0.0
```
#     行距（浮点数），默认为 0.0

```python
    baseline_shift: float = 0.0
```
#     基线偏移（浮点数），默认为 0.0

```python

    def to_qfont(self) -> QFont:
```
#     定义实例方法：转换为 Qt 字体对象，返回 QFont

```python
        font = QFont(self.font_family, int(self.font_size))
```
#         使用字体族和字号构造 QFont 对象

```python
        font.setBold(self.bold)
```
#         设置是否加粗

```python
        font.setItalic(self.italic)
```
#         设置是否斜体

```python
        font.setUnderline(self.underline)
```
#         设置是否有下划线

```python
        font.setStrikeOut(self.strikethrough)
```
#         设置是否有删除线

```python
        return font
```
#         返回配置好的字体对象

---

```python

@dataclass(slots=True)
class ParagraphAttributes:
```
# 使用 dataclass 装饰器（启用 slots 优化）定义段落属性类

```python
    """段落属性"""
```
#     类文档字符串：段落属性

```python
    justification: Justification = Justification.LEFT
```
#     对齐方式（Justification 枚举），默认为左对齐

```python
    first_line_indent: float = 0.0
```
#     首行缩进（浮点数），默认为 0.0

```python
    space_before: float = 0.0
```
#     段前间距（浮点数），默认为 0.0

```python
    space_after: float = 0.0
```
#     段后间距（浮点数），默认为 0.0

---

```python

# ── 图形项基类 ──────────────────────────────────────────────
```
# ── 图形项基类分隔线 ──

```python

class GraphicItem:
```
# 定义图形项基类（对应 Adobe Illustrator 的 PageItem）

```python
    """所有图形项的基类（对应 Ai PageItem）
```
#     类文档字符串：所有图形项的基类（对应 AI 的 PageItem）

```python

    使用 __slots__ 优化内存占用
```
#     使用 \_\_slots\_\_ 优化内存占用

```python
    """
```
#     类文档字符串结束

```python
    __slots__ = (
```
#     定义 \_\_slots\_\_ 元组以优化内存，包含以下属性名：

```python
        '_id', 'item_type', 'name', 'visible', 'locked',
```
#         内部标识符、元素类型、名称、可见性、锁定状态

```python
        'selected', 'style', '_transform', '_opacity',
```
#         选中状态、样式、变换矩阵、不透明度

```python
        '_blend_mode', '_parent', '_layer',
```
#         混合模式、父级引用、所属图层引用

```python
    )
```
#     \_\_slots\_\_ 元组结束

```python

    def __init__(self, item_type: str = "GraphicItem"):
```
#     定义初始化方法（接收元素类型字符串参数，默认为 "GraphicItem"）

```python
        self._id = str(uuid.uuid4())
```
#         生成 UUID 并转换为字符串作为唯一标识符

```python
        self.item_type = item_type
```
#         设置元素类型

```python
        self.name: str = ""
```
#         设置名称为空字符串

```python
        self.visible: bool = True
```
#         设置默认可见

```python
        self.locked: bool = False
```
#         设置默认未锁定

```python
        self.selected: bool = False
```
#         设置默认未选中

```python
        self.style = GraphicStyle()
```
#         创建默认图形样式实例

```python
        self._transform = QTransform()
```
#         创建默认变换矩阵（单位矩阵）

```python
        self._opacity: float = 1.0
```
#         设置默认不透明度为 1.0

```python
        self._blend_mode: BlendMode = BlendMode.NORMAL
```
#         设置默认混合模式为正常

```python
        self._parent: GroupItem | None = None
```
#         设置父级编组引用为 None

```python
        self._layer = None  # Layer | None (避免循环导入，运行时赋值)
```
#         设置所属图层引用为 None（避免循环导入，运行时赋值）

```python

    @property
    def id(self) -> str:
```
#     定义只读属性：获取唯一标识符，返回字符串

```python
        return self._id
```
#         返回内部标识符

```python

    @property
    def opacity(self) -> float:
```
#     定义只读属性：获取不透明度，返回浮点数

```python
        return self._opacity
```
#         返回内部不透明度值

```python

    @opacity.setter
    def opacity(self, value: float):
```
#     定义不透明度设置器（接收浮点数值参数）

```python
        self._opacity = max(0.0, min(1.0, value))
```
#         将值限制在 0.0 到 1.0 范围内后赋值

```python

    @property
    def blend_mode(self) -> BlendMode:
```
#     定义只读属性：获取混合模式，返回 BlendMode 枚举

```python
        return self._blend_mode
```
#         返回内部混合模式值

```python

    @blend_mode.setter
    def blend_mode(self, value: BlendMode):
```
#     定义混合模式设置器（接收 BlendMode 枚举值参数）

```python
        self._blend_mode = value
```
#         设置内部混合模式值

```python

    @property
    def parent(self):
```
#     定义只读属性：获取父级编组引用

```python
        return self._parent
```
#         返回内部父级引用

```python

    def bounding_rect(self) -> QRectF:
```
#     定义实例方法：获取包围矩形，返回 QRectF（子类需重写）

```python
        raise NotImplementedError
```
#         抛出未实现异常（要求子类必须重写）

```python

    def painter_path(self) -> QPainterPath:
```
#     定义实例方法：获取绘图路径，返回 QPainterPath（子类需重写）

```python
        raise NotImplementedError
```
#         抛出未实现异常（要求子类必须重写）

```python

    def contains_point(self, point: QPointF) -> bool:
```
#     定义实例方法：判断点是否在图形内（接收 QPointF 点参数，返回布尔值）

```python
        return self.bounding_rect().contains(point)
```
#         通过包围矩形的 contains 方法判断（默认实现）

```python

    def move_by(self, dx: float, dy: float):
```
#     定义实例方法：平移图形（接收 x 方向偏移量 dx 和 y 方向偏移量 dy）

```python
        self._transform.translate(dx, dy)
```
#         在变换矩阵上应用平移

```python

    def rotate(self, angle: float, center: QPointF | None = None):
```
#     定义实例方法：旋转图形（接收旋转角度和可选旋转中心点参数）

```python
        if center is None:
```
#         如果未指定旋转中心：

```python
            r = self.bounding_rect()
```
#             获取包围矩形

```python
            center = r.center()
```
#             使用包围矩形中心作为旋转中心

```python
        self._transform.translate(center.x(), center.y())
```
#         平移变换矩阵到旋转中心

```python
        self._transform.rotate(angle)
```
#         应用旋转

```python
        self._transform.translate(-center.x(), -center.y())
```
#         平移变换矩阵回原点

```python

    def scale(self, sx: float, sy: float, center: QPointF | None = None):
```
#     定义实例方法：缩放图形（接收 x 缩放比例 sx、y 缩放比例 sy 和可选缩放中心点参数）

```python
        if center is None:
```
#         如果未指定缩放中心：

```python
            r = self.bounding_rect()
```
#             获取包围矩形

```python
            center = r.center()
```
#             使用包围矩形中心作为缩放中心

```python
        self._transform.translate(center.x(), center.y())
```
#         平移变换矩阵到缩放中心

```python
        self._transform.scale(sx, sy)
```
#         应用缩放

```python
        self._transform.translate(-center.x(), -center.y())
```
#         平移变换矩阵回原点

```python

    def to_dict(self) -> dict:
```
#     定义实例方法：将图形项序列化为字典，返回字典

```python
        style = self.style
```
#         获取样式引用

```python
        fc = style.fill_color
```
#         获取填充颜色引用

```python
        sc = style.stroke_color
```
#         获取描边颜色引用

```python
        return {
```
#         返回包含以下键值对的字典：

```python
            "id": self._id,
```
#             唯一标识符

```python
            "type": self.item_type,
```
#             元素类型

```python
            "name": self.name,
```
#             名称

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
            "blend_mode": self._blend_mode.name,
```
#             混合模式名称字符串

```python
            "fill_color": [fc.red(), fc.green(), fc.blue(), fc.alpha()] if fc else None,
```
#             填充颜色 RGBA 列表（若存在），否则为 None

```python
            "fill_opacity": style.fill_opacity,
```
#             填充不透明度

```python
            "stroke_color": [sc.red(), sc.green(), sc.blue(), sc.alpha()] if sc else None,
```
#             描边颜色 RGBA 列表（若存在），否则为 None

```python
            "stroke_width": style.stroke_width,
```
#             描边宽度

```python
            "stroke_opacity": style.stroke_opacity,
```
#             描边不透明度

```python
            "stroke_cap": style.stroke_cap.name,
```
#             线端点样式名称字符串

```python
            "stroke_join": style.stroke_join.name,
```
#             线连接样式名称字符串

```python
            "stroke_dash": style.stroke_dash,
```
#             虚线模式列表

```python
            "transform": {
```
#             变换矩阵字典，包含：

```python
                "m11": self._transform.m11(), "m12": self._transform.m12(),
```
#                 变换矩阵第 1 行第 1、2 列元素

```python
                "m13": self._transform.m13(), "m21": self._transform.m21(),
```
#                 变换矩阵第 1 行第 3 列元素、第 2 行第 1 列元素

```python
                "m22": self._transform.m22(), "m23": self._transform.m23(),
```
#                 变换矩阵第 2 行第 2、3 列元素

```python
                "m31": self._transform.m31(), "m32": self._transform.m32(),
```
#                 变换矩阵第 3 行第 1、2 列元素

```python
                "m33": self._transform.m33(),
```
#                 变换矩阵第 3 行第 3 列元素

```python
            },
```
#             变换矩阵字典结束

```python
        }
```
#         序列化字典结束

```python

    @staticmethod
    def from_dict(data: dict) -> GraphicItem:
```
#     定义静态方法：从字典反序列化为图形项（接收字典参数，返回 GraphicItem）

```python
        """使用 match-case (Python 3.10+) 进行类型分发"""
```
#         方法文档字符串：使用 match-case（Python 3.10+）进行类型分发

```python
        item_type = data.get("type", "GraphicItem")
```
#         从字典获取元素类型（默认为 "GraphicItem"）

```python
        match item_type:
```
#         使用 match-case 根据类型分发创建对应实例：

```python
            case "PathItem":
```
#             当类型为路径项时：

```python
                item = PathItem()
```
#                 创建路径项实例

```python
            case "RectangleItem":
```
#             当类型为矩形项时：

```python
                item = RectangleItem()
```
#                 创建矩形项实例

```python
            case "EllipseItem":
```
#             当类型为椭圆项时：

```python
                item = EllipseItem()
```
#                 创建椭圆项实例

```python
            case "TextFrame":
```
#             当类型为文本框时：

```python
                item = TextFrame()
```
#                 创建文本框实例

```python
            case "GroupItem":
```
#             当类型为编组项时：

```python
                item = GroupItem()
```
#                 创建编组项实例

```python
            case _:
```
#             其他类型（默认分支）：

```python
                item = GraphicItem()
```
#                 创建通用图形项实例

```python

        item._id = data.get("id", str(uuid.uuid4()))
```
#         从字典获取标识符（默认生成新 UUID）

```python
        item.name = data.get("name", "")
```
#         从字典获取名称（默认为空字符串）

```python
        item.visible = data.get("visible", True)
```
#         从字典获取可见性（默认为可见）

```python
        item.locked = data.get("locked", False)
```
#         从字典获取锁定状态（默认为未锁定）

```python
        item._opacity = data.get("opacity", 1.0)
```
#         从字典获取不透明度（默认为 1.0）

```python

        fc = data.get("fill_color")
```
#         从字典获取填充颜色数据

```python
        item.style.fill_color = QColor(*fc) if fc else None
```
#         若存在则构造 QColor，否则为 None

```python
        item.style.fill_opacity = data.get("fill_opacity", 1.0)
```
#         从字典获取填充不透明度（默认为 1.0）

```python
        sc = data.get("stroke_color")
```
#         从字典获取描边颜色数据

```python
        item.style.stroke_color = QColor(*sc) if sc else None
```
#         若存在则构造 QColor，否则为 None

```python
        item.style.stroke_width = data.get("stroke_width", 1.0)
```
#         从字典获取描边宽度（默认为 1.0）

```python
        item.style.stroke_opacity = data.get("stroke_opacity", 1.0)
```
#         从字典获取描边不透明度（默认为 1.0）

```python
        item.style.stroke_cap = StrokeCap[data.get("stroke_cap", "BUTT")]
```
#         从字典获取线端点样式（默认为平头）

```python
        item.style.stroke_join = StrokeJoin[data.get("stroke_join", "MITER")]
```
#         从字典获取线连接样式（默认为尖角）

```python
        item.style.stroke_dash = data.get("stroke_dash", [])
```
#         从字典获取虚线模式（默认为空列表）

```python

        t = data.get("transform", {})
```
#         从字典获取变换矩阵数据（默认为空字典）

```python
        if t:
```
#         如果存在变换矩阵数据：

```python
            item._transform = QTransform(
```
#             使用矩阵元素构造 QTransform：

```python
                t.get("m11", 1), t.get("m12", 0), t.get("m13", 0),
```
#                 第 1 行三个元素（默认分别为 1、0、0）

```python
                t.get("m21", 0), t.get("m22", 1), t.get("m23", 0),
```
#                 第 2 行三个元素（默认分别为 0、1、0）

```python
                t.get("m31", 0), t.get("m32", 0), t.get("m33", 1),
```
#                 第 3 行三个元素（默认分别为 0、0、1）

```python
            )
```
#             QTransform 构造结束

```python

        return item
```
#         返回反序列化后的图形项对象

---

```python

# ── 具体图形项 ──────────────────────────────────────────────
```
# ── 具体图形项分隔线 ──

```python

class PathItem(GraphicItem):
```
# 定义路径项类，继承自 GraphicItem

```python
    """路径项 —— 贝塞尔曲线路径，支持锚点手柄编辑"""
```
#     类文档字符串：路径项——贝塞尔曲线路径，支持锚点手柄编辑

```python

    __slots__ = ('_path', '_points', '_anchors', 'closed')
```
#     定义 \_\_slots\_\_：内部路径对象、点坐标列表、锚点列表、是否闭合

```python

    def __init__(self):
```
#     定义初始化方法（无额外参数）

```python
        super().__init__("PathItem")
```
#         调用父类初始化，传入类型名 "PathItem"

```python
        self._path = QPainterPath()
```
#         创建空的绘图路径对象

```python
        self._points: list[PointTuple] = []
```
#         初始化点坐标列表为空列表

```python
        self._anchors: list[AnchorPoint] = []
```
#         初始化锚点列表为空列表

```python
        self.closed: bool = False
```
#         设置路径默认为开放（未闭合）

```python

    # ── 属性 ──
```
#     注释：属性

```python

    @property
    def path_points(self) -> list[PointTuple]:
```
#     定义只读属性：获取路径点列表，返回点坐标元组列表

```python
        return self._points
```
#         返回内部点坐标列表

```python

    @property
    def anchors(self) -> list[AnchorPoint]:
```
#     定义只读属性：获取锚点列表，返回 AnchorPoint 列表

```python
        return self._anchors
```
#         返回内部锚点列表

```python

    @property
    def anchor_count(self) -> int:
```
#     定义只读属性：获取锚点数量，返回整数

```python
        return len(self._anchors)
```
#         返回锚点列表的长度

```python

    # ── 路径构建 ──
```
#     注释：路径构建

```python

    def set_path_points(self, points: list[PointTuple], closed: bool = False):
```
#     定义实例方法：设置路径点——简单折线模式（接收点坐标列表和可选闭合标志参数）

```python
        """设置路径点（简单折线）"""
```
#         方法文档字符串：设置路径点（简单折线）

```python
        self._points = points
```
#         设置内部点坐标列表

```python
        self.closed = closed
```
#         设置是否闭合

```python
        self._anchors = [AnchorPoint(x, y) for x, y in points]
```
#         根据点坐标列表创建锚点列表（每个点生成无手柄的角点）

```python
        self._build_path()
```
#         重新构建绘图路径

```python

    def add_point(self, x: float, y: float):
```
#     定义实例方法：添加一个点（接收 x、y 坐标参数）

```python
        self._points.append((x, y))
```
#         将坐标元组追加到点列表

```python
        self._anchors.append(AnchorPoint(x, y))
```
#         创建新锚点并追加到锚点列表

```python
        self._build_path()
```
#         重新构建绘图路径

```python

    def add_anchor(self, anchor: AnchorPoint):
```
#     定义实例方法：添加一个锚点（接收 AnchorPoint 锚点参数）

```python
        self._anchors.append(anchor)
```
#         将锚点追加到锚点列表

```python
        self._points.append((anchor.x, anchor.y))
```
#         将锚点坐标追加到点列表

```python
        self._build_path()
```
#         重新构建绘图路径

```python

    def insert_anchor(self, index: int, anchor: AnchorPoint):
```
#     定义实例方法：在指定位置插入锚点（接收插入索引和 AnchorPoint 锚点参数）

```python
        self._anchors.insert(index, anchor)
```
#         在锚点列表的指定位置插入锚点

```python
        self._points.insert(index, (anchor.x, anchor.y))
```
#         在点列表的对应位置插入坐标

```python
        self._build_path()
```
#         重新构建绘图路径

```python

    def remove_anchor(self, index: int):
```
#     定义实例方法：移除指定位置的锚点（接收索引参数）

```python
        if 0 <= index < len(self._anchors):
```
#         如果索引在有效范围内：

```python
            self._anchors.pop(index)
```
#             从锚点列表中移除

```python
            self._points.pop(index)
```
#             从点列表中移除

```python
            self._build_path()
```
#             重新构建绘图路径

```python

    # ── 锚点编辑 ──
```
#     注释：锚点编辑

```python

    def move_anchor(self, index: int, x: float, y: float):
```
#     定义实例方法：移动锚点到新位置（接收锚点索引和新 x、y 坐标参数）

```python
        """移动锚点到新位置，贝塞尔手柄保持相对于锚点的偏移不变
```
#         方法文档字符串：移动锚点到新位置，贝塞尔手柄保持相对于锚点的偏移不变

```python
        
        对照 Adobe Illustrator：移动锚点时，handle_in 和 handle_out 
```
#         对照 Adobe Illustrator：移动锚点时，handle_in 和 handle_out

```python
        保持相对于锚点的偏移不变（手柄跟随锚点一起移动）。
```
#         保持相对于锚点的偏移不变（手柄跟随锚点一起移动）。

```python
        handle_in/out 存储的是相对于锚点的偏移量，所以只需更新锚点坐标。
```
#         handle_in/out 存储的是相对于锚点的偏移量，所以只需更新锚点坐标。

```python
        """
```
#         方法文档字符串结束

```python
        if 0 <= index < len(self._anchors):
```
#         如果索引在有效范围内：

```python
            self._anchors[index].x = x
```
#             更新锚点的 x 坐标

```python
            self._anchors[index].y = y
```
#             更新锚点的 y 坐标

```python
            self._points[index] = (x, y)
```
#             同步更新点列表

```python
            self._build_path()
```
#             重新构建绘图路径

```python

    def set_handle_in(self, index: int, hx: float, hy: float, 
```
#     定义实例方法：设置入控制手柄的偏移量（接收锚点索引、手柄 x 偏移 hx、手柄 y 偏移 hy、

```python
                       constrain_smooth: bool = True):
```
#                                              是否约束平滑点标志参数，默认为 True）

```python
        """设置 handle_in 的偏移量
```
#         方法文档字符串：设置 handle_in 的偏移量

```python
        
        Args:
```
#         参数说明：

```python
            constrain_smooth: 如果锚点是平滑类型，是否自动约束 handle_out
```
#             constrain_smooth：如果锚点是平滑类型，是否自动约束 handle_out

```python
        """
```
#         方法文档字符串结束

```python
        if 0 <= index < len(self._anchors):
```
#         如果索引在有效范围内：

```python
            anchor = self._anchors[index]
```
#             获取目标锚点

```python
            anchor.handle_in = QPointF(hx, hy)
```
#             设置入控制手柄偏移量

```python
            if anchor.anchor_type != AnchorPointType.SMOOTH:
```
#             如果锚点类型不是平滑点：

```python
                anchor.anchor_type = AnchorPointType.SMOOTH
```
#                 将锚点类型改为平滑点

```python
            if constrain_smooth:
```
#             如果需要约束平滑：

```python
                anchor.enforce_smooth_constraint('in')
```
#                 执行平滑约束（入控制手柄被移动）

```python
            self._build_path()
```
#             重新构建绘图路径

```python

    def set_handle_out(self, index: int, hx: float, hy: float,
```
#     定义实例方法：设置出控制手柄的偏移量（接收锚点索引、手柄 x 偏移 hx、手柄 y 偏移 hy、

```python
                        constrain_smooth: bool = True):
```
#                                              是否约束平滑点标志参数，默认为 True）

```python
        """设置 handle_out 的偏移量
```
#         方法文档字符串：设置 handle_out 的偏移量

```python
        
        Args:
```
#         参数说明：

```python
            constrain_smooth: 如果锚点是平滑类型，是否自动约束 handle_in
```
#             constrain_smooth：如果锚点是平滑类型，是否自动约束 handle_in

```python
        """
```
#         方法文档字符串结束

```python
        if 0 <= index < len(self._anchors):
```
#         如果索引在有效范围内：

```python
            anchor = self._anchors[index]
```
#             获取目标锚点

```python
            anchor.handle_out = QPointF(hx, hy)
```
#             设置出控制手柄偏移量

```python
            if anchor.anchor_type != AnchorPointType.SMOOTH:
```
#             如果锚点类型不是平滑点：

```python
                anchor.anchor_type = AnchorPointType.SMOOTH
```
#                 将锚点类型改为平滑点

```python
            if constrain_smooth:
```
#             如果需要约束平滑：

```python
                anchor.enforce_smooth_constraint('out')
```
#                 执行平滑约束（出控制手柄被移动）

```python
            self._build_path()
```
#             重新构建绘图路径

```python

    def remove_handles(self, index: int):
```
#     定义实例方法：移除指定锚点的所有手柄（接收锚点索引参数）

```python
        """移除指定锚点的所有手柄（转为角点）"""
```
#         方法文档字符串：移除指定锚点的所有手柄（转为角点）

```python
        if 0 <= index < len(self._anchors):
```
#         如果索引在有效范围内：

```python
            self._anchors[index].remove_handles()
```
#             调用锚点的 remove_handles 方法

```python
            self._build_path()
```
#             重新构建绘图路径

```python

    def convert_anchor_type(self, index: int, to_type: AnchorPointType):
```
#     定义实例方法：转换锚点类型（接收锚点索引和目标类型参数）

```python
        """转换锚点类型（对照 AI 的 Convert Anchor Point Tool）"""
```
#         方法文档字符串：转换锚点类型（对照 AI 的转换锚点工具）

```python
        if 0 <= index < len(self._anchors):
```
#         如果索引在有效范围内：

```python
            anchor = self._anchors[index]
```
#             获取目标锚点

```python
            if to_type == AnchorPointType.CORNER:
```
#             如果目标类型为角点：

```python
                anchor.convert_to_corner()
```
#                 调用转换为角点方法

```python
            elif to_type == AnchorPointType.SMOOTH:
```
#             否则如果目标类型为平滑点：

```python
                anchor.convert_to_smooth()
```
#                 调用转换为平滑点方法

```python
            self._build_path()
```
#             重新构建绘图路径

```python

    # ── 碰撞检测 ──
```
#     注释：碰撞检测

```python

    def get_anchor_at(self, x: float, y: float, tolerance: float = 5.0) -> int:
```
#     定义实例方法：检测指定坐标处的锚点索引（接收 x、y 坐标和容差参数，返回锚点索引，-1 表示未命中）

```python
        """检测坐标 (x,y) 处的锚点索引，返回 -1 表示未命中
```
#         方法文档字符串：检测坐标 (x,y) 处的锚点索引，返回 -1 表示未命中

```python
        
        Args:
```
#         参数说明：

```python
            tolerance: 命中容差（本地坐标空间中的像素值）
```
#             tolerance：命中容差（本地坐标空间中的像素值）

```python
        """
```
#         方法文档字符串结束

```python
        for i, anchor in enumerate(self._anchors):
```
#         遍历所有锚点：

```python
            if abs(anchor.x - x) < tolerance and abs(anchor.y - y) < tolerance:
```
#             如果锚点坐标与目标坐标在容差范围内：

```python
                return i
```
#                 返回当前锚点索引

```python
        return -1
```
#         所有锚点都不匹配，返回 -1

```python

    def get_handle_at(self, x: float, y: float, tolerance: float = 4.0) -> tuple[int, str]:
```
#     定义实例方法：检测指定坐标处的手柄（接收 x、y 坐标和容差参数，返回 (锚点索引, 'in'/'out') 元组，未命中返回 (-1, '')）

```python
        """检测坐标 (x,y) 处的手柄，返回 (anchor_index, 'in'|'out') 或 (-1, '')
```
#         方法文档字符串：检测坐标 (x,y) 处的手柄，返回 (锚点索引, 'in'|'out') 或 (-1, '')

```python
        
        Args:
```
#         参数说明：

```python
            tolerance: 命中容差（本地坐标空间中的像素值）
```
#             tolerance：命中容差（本地坐标空间中的像素值）

```python
        """
```
#         方法文档字符串结束

```python
        for i, anchor in enumerate(self._anchors):
```
#         遍历所有锚点：

```python
            if anchor.handle_in:
```
#             如果存在入控制手柄：

```python
                hx = anchor.x + anchor.handle_in.x()
```
#                 计算入控制手柄的绝对 x 坐标

```python
                hy = anchor.y + anchor.handle_in.y()
```
#                 计算入控制手柄的绝对 y 坐标

```python
                if abs(hx - x) < tolerance and abs(hy - y) < tolerance:
```
#                 如果手柄坐标与目标坐标在容差范围内：

```python
                    return (i, 'in')
```
#                     返回 (锚点索引, 'in')

```python
            if anchor.handle_out:
```
#             如果存在出控制手柄：

```python
                hx = anchor.x + anchor.handle_out.x()
```
#                 计算出控制手柄的绝对 x 坐标

```python
                hy = anchor.y + anchor.handle_out.y()
```
#                 计算出控制手柄的绝对 y 坐标

```python
                if abs(hx - x) < tolerance and abs(hy - y) < tolerance:
```
#                 如果手柄坐标与目标坐标在容差范围内：

```python
                    return (i, 'out')
```
#                     返回 (锚点索引, 'out')

```python
        return (-1, '')
```
#         所有手柄都不匹配，返回 (-1, '')

```python

    def get_segment_at(self, x: float, y: float, 
```
#     定义实例方法：检测点击位置在路径的哪一段上（接收 x、y 坐标、

```python
                        tolerance: float = 4.0) -> int:
``
#                                             容差参数，返回段起始锚点索引，-1 表示未命中）

```python
        """检测点击位置在路径的哪一段（贝塞尔曲线段）上，返回段起始锚点索引
```
#         方法文档字符串：检测点击位置在路径的哪一段（贝塞尔曲线段）上，返回段起始锚点索引

```python
        
        对照 AI：考虑贝塞尔曲线而非仅直线段。
```
#         对照 AI：考虑贝塞尔曲线而非仅直线段。

```python
        对曲线段采样多个点进行距离检测。
```
#         对曲线段采样多个点进行距离检测。

```python
        
        Args:
```
#         参数说明：

```python
            tolerance: 命中容差
```
#             tolerance：命中容差

```python
        Returns:
```
#         返回值说明：

```python
            段起始锚点索引，-1 表示未命中
```
#             段起始锚点索引，-1 表示未命中

```python
        """
```
#         方法文档字符串结束

```python
        if len(self._anchors) < 2:
```
#         如果锚点数量少于 2 个：

```python
            return -1
```
#             返回 -1（无法构成路径段）

```python
        n = len(self._anchors)
```
#         获取锚点总数

```python
        end = n if self.closed else n - 1
```
#         设置遍历终止索引（闭合路径遍历所有段，开放路径遍历到倒数第二段）

```python
        for i in range(end):
```
#         遍历每一段：

```python
            j = (i + 1) % n
```
#             计算下一段锚点索引（闭合时取模循环）

```python
            prev = self._anchors[i]
```
#             获取当前段的起始锚点

```python
            curr = self._anchors[j]
```
#             获取当前段的终止锚点
            
```python
            # 采样贝塞尔曲线段上的点
```
#             注释：采样贝塞尔曲线段上的点

```python
            samples = self._sample_bezier_segment(prev, curr, num_samples=20)
```
#             对该贝塞尔曲线段采样 20 个点
            
```python
            # 检测点到折线（采样点连接）的距离
```
#             注释：检测点到折线（采样点连接）的距离

```python
            for k in range(len(samples) - 1):
```
#             遍历每对相邻采样点：

```python
                p1, p2 = samples[k], samples[k + 1]
```
#                 获取当前采样点和下一个采样点

```python
                dx = p2[0] - p1[0]
```
#                 计算线段 x 方向增量

```python
                dy = p2[1] - p1[1]
```
#                 计算线段 y 方向增量

```python
                len_sq = dx*dx + dy*dy
```
#                 计算线段长度的平方

```python
                if len_sq < 0.001:
```
#                 如果线段长度极短：

```python
                    dist = math.sqrt((x - p1[0])**2 + (y - p1[1])**2)
```
#                     计算点到起点的欧氏距离

```python
                else:
```
#                 否则：

```python
                    t = max(0.0, min(1.0, ((x - p1[0])*dx + (y - p1[1])*dy) / len_sq))
```
#                     计算投影参数 t（限制在 0 到 1 之间）

```python
                    closest_x = p1[0] + t * dx
```
#                     计算线段上最近点的 x 坐标

```python
                    closest_y = p1[1] + t * dy
```
#                     计算线段上最近点的 y 坐标

```python
                    dist = math.sqrt((x - closest_x)**2 + (y - closest_y)**2)
```
#                     计算点到最近点的欧氏距离
                
```python
                if dist < tolerance:
```
#                 如果距离在容差范围内：

```python
                    return i
```
#                     返回当前段起始锚点索引
        
```python
        return -1
```
#         所有段都不匹配，返回 -1

```python

    @staticmethod
    def _sample_bezier_segment(prev: AnchorPoint, curr: AnchorPoint,
```
#     定义静态方法：对一段贝塞尔曲线进行采样（接收前一个锚点和当前锚点参数、

```python
                                num_samples: int = 20) -> list[tuple[float, float]]:
```
#                                                采样数量参数，返回采样点坐标列表）

```python
        """对一段贝塞尔曲线进行采样，返回采样点列表"""
```
#         方法文档字符串：对一段贝塞尔曲线进行采样，返回采样点列表

```python
        points = []
```
#         初始化采样点列表

```python
        p0 = (prev.x, prev.y)
```
#         获取曲线起点坐标

```python
        p3 = (curr.x, curr.y)
```
#         获取曲线终点坐标
        
```python
        # 控制点
```
#         注释：控制点

```python
        if prev.handle_out is not None:
```
#         如果前一个锚点有出控制手柄：

```python
            p1 = (prev.x + prev.handle_out.x(), prev.y + prev.handle_out.y())
```
#             计算第一个控制点的绝对坐标

```python
        else:
```
#         否则：

```python
            p1 = p0
```
#             第一个控制点与起点重合（退化为直线）

```python
        
        if curr.handle_in is not None:
```
#         如果当前锚点有入控制手柄：

```python
            p2 = (curr.x + curr.handle_in.x(), curr.y + curr.handle_in.y())
```
#             计算第二个控制点的绝对坐标

```python
        else:
```
#         否则：

```python
            p2 = p3
```
#             第二个控制点与终点重合（退化为直线）
        
```python
        # 如果两端都没有手柄，退化为直线
```
#         注释：如果两端都没有手柄，退化为直线

```python
        if prev.handle_out is None and curr.handle_in is None:
```
#         如果两个锚点都没有手柄：

```python
            return [p0, p3]
```
#             仅返回起点和终点
        
```python
        # 三次贝塞尔采样
```
#         注释：三次贝塞尔采样

```python
        for k in range(num_samples + 1):
```
#         从 0 到 num_samples 进行采样：

```python
            t_val = k / num_samples
```
#             计算参数 t 值（0 到 1）

```python
            # B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
```
#             注释：贝塞尔曲线公式 B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3

```python
            mt = 1 - t_val
```
#             计算 (1 - t)

```python
            mt2 = mt * mt
```
#             计算 (1 - t)²

```python
            mt3 = mt2 * mt
```
#             计算 (1 - t)³

```python
            t2 = t_val * t_val
```
#             计算 t²

```python
            t3 = t2 * t_val
```
#             计算 t³
            
```python
            bx = mt3 * p0[0] + 3 * mt2 * t_val * p1[0] + 3 * mt * t2 * p2[0] + t3 * p3[0]
```
#             计算 x 坐标的贝塞尔插值

```python
            by = mt3 * p0[1] + 3 * mt2 * t_val * p1[1] + 3 * mt * t2 * p2[1] + t3 * p3[1]
```
#             计算 y 坐标的贝塞尔插值

```python
            points.append((bx, by))
```
#             将采样点添加到列表
        
```python
        return points
```
#         返回所有采样点

```python

    def get_closest_point_on_segment(self, seg_idx: int, 
```
#     定义实例方法：返回路径段上距指定坐标最近的点（接收段索引、

```python
                                      x: float, y: float) -> tuple[float, float]:
```
#                                                    x 坐标、y 坐标参数，返回最近点坐标元组）

```python
        """返回路径段上距 (x,y) 最近的点坐标"""
```
#         方法文档字符串：返回路径段上距 (x,y) 最近的点坐标

```python
        if seg_idx < 0 or seg_idx >= len(self._anchors):
```
#         如果段索引无效：

```python
            return (x, y)
```
#             返回原始坐标
        
```python
        n = len(self._anchors)
```
#         获取锚点总数

```python
        j = (seg_idx + 1) % n
```
#         计算段终点锚点索引

```python
        prev = self._anchors[seg_idx]
```
#         获取段起始锚点

```python
        curr = self._anchors[j]
```
#         获取段终止锚点
        
```python
        samples = self._sample_bezier_segment(prev, curr, num_samples=50)
```
#         对该段采样 50 个点（提高精度）
        
```python
        best_dist = float('inf')
```
#         初始化最佳距离为正无穷

```python
        best_pt = (x, y)
```
#         初始化最佳点为原始坐标
        
```python
        for k in range(len(samples) - 1):
```
#         遍历每对相邻采样点：

```python
            p1, p2 = samples[k], samples[k + 1]
```
#             获取当前采样点和下一个采样点

```python
            dx = p2[0] - p1[0]
```
#             计算线段 x 方向增量

```python
            dy = p2[1] - p1[1]
```
#             计算线段 y 方向增量

```python
            len_sq = dx*dx + dy*dy
```
#             计算线段长度的平方

```python
            if len_sq < 0.001:
```
#             如果线段长度极短：

```python
                t = 0.0
```
#                 投影参数设为 0

```python
            else:
```
#             否则：

```python
                t = max(0.0, min(1.0, ((x - p1[0])*dx + (y - p1[1])*dy) / len_sq))
```
#                 计算投影参数 t（限制在 0 到 1 之间）

```python
            closest_x = p1[0] + t * dx
```
#             计算最近点 x 坐标

```python
            closest_y = p1[1] + t * dy
```
#             计算最近点 y 坐标

```python
            dist = (x - closest_x)**2 + (y - closest_y)**2
```
#             计算距离的平方（用于比较，无需开方）

```python
            if dist < best_dist:
```
#             如果当前距离优于最佳距离：

```python
                best_dist = dist
```
#                 更新最佳距离

```python
                best_pt = (closest_x, closest_y)
```
#                 更新最佳点坐标
        
```python
        return best_pt
```
#         返回最佳最近点

```python

    # ── 内部 ──
```
#     注释：内部方法

```python

    def _build_path(self):
```
#     定义内部方法：从锚点列表构建 QPainterPath（支持贝塞尔曲线）

```python
        """从锚点列表构建 QPainterPath（支持贝塞尔曲线）"""
```
#         方法文档字符串：从锚点列表构建 QPainterPath（支持贝塞尔曲线）

```python
        self._path = QPainterPath()
```
#         创建新的空绘图路径

```python
        if not self._anchors:
```
#         如果没有锚点：

```python
            return
```
#             提前返回

```python
        first = self._anchors[0]
```
#         获取第一个锚点

```python
        self._path.moveTo(first.x, first.y)
```
#         将绘图路径起点移动到第一个锚点

```python
        for i in range(1, len(self._anchors)):
```
#         从第二个锚点开始遍历：

```python
            self._add_segment(self._anchors[i - 1], self._anchors[i])
```
#             添加相邻锚点之间的路径段

```python
        if self.closed and len(self._anchors) > 2:
```
#         如果路径闭合且锚点多于 2 个：

```python
            self._add_segment(self._anchors[-1], self._anchors[0])
```
#             添加最后锚点到第一个锚点的闭合段

```python
            self._path.closeSubpath()
```
#             闭合子路径

```python

    def _add_segment(self, prev: AnchorPoint, curr: AnchorPoint):
```
#     定义内部方法：添加路径段（接收前一个锚点和当前锚点参数）

```python
        """使用 match-case (Python 3.10+) 处理贝塞尔段类型"""
```
#         方法文档字符串：使用 match-case（Python 3.10+）处理贝塞尔段类型

```python
        match (prev.handle_out, curr.handle_in):
```
#         使用 match-case 匹配两端手柄的组合：

```python
            case (out, inp) if out is not None and inp is not None:
```
#             当两端都有手柄时（三次贝塞尔曲线）：

```python
                self._path.cubicTo(
```
#                 添加三次贝塞尔曲线段：

```python
                    prev.x + out.x(), prev.y + out.y(),
```
#                     第一个控制点绝对坐标

```python
                    curr.x + inp.x(), curr.y + inp.y(),
```
#                     第二个控制点绝对坐标

```python
                    curr.x, curr.y,
```
#                     终点坐标

```python
                )
```
#                 三次贝塞尔曲线添加结束

```python
            case (out, _) if out is not None:
```
#             当只有前一个锚点有出控制手柄时（二次贝塞尔曲线）：

```python
                self._path.quadTo(
```
#                 添加二次贝塞尔曲线段：

```python
                    prev.x + out.x(), prev.y + out.y(),
```
#                     控制点绝对坐标

```python
                    curr.x, curr.y,
```
#                     终点坐标

```python
                )
```
#                 二次贝塞尔曲线添加结束

```python
            case (_, inp) if inp is not None:
```
#             当只有当前锚点有入控制手柄时（二次贝塞尔曲线）：

```python
                self._path.quadTo(
```
#                 添加二次贝塞尔曲线段：

```python
                    curr.x + inp.x(), curr.y + inp.y(),
```
#                     控制点绝对坐标

```python
                    curr.x, curr.y,
```
#                     终点坐标

```python
                )
```
#                 二次贝塞尔曲线添加结束

```python
            case _:
```
#             其他情况（两端都无手柄）：

```python
                self._path.lineTo(curr.x, curr.y)
```
#                 添加直线段到终点

```python

    def _rebuild_from_anchors(self):
```
#     定义内部方法：从锚点列表重建点列表和绘图路径

```python
        self._points = [(a.x, a.y) for a in self._anchors]
```
#         从锚点列表重新生成点坐标列表

```python
        self._build_path()
```
#         重新构建绘图路径

```python

    # ── GraphicItem 接口 ──
```
#     注释：GraphicItem 接口实现

```python

    def painter_path(self) -> QPainterPath:
```
#     重写实例方法：获取绘图路径，返回 QPainterPath

```python
        return self._path
```
#         返回内部绘图路径

```python

    def bounding_rect(self) -> QRectF:
```
#     重写实例方法：获取包围矩形，返回 QRectF

```python
        return self._path.boundingRect()
```
#         返回绘图路径的包围矩形

```python

    def contains_point(self, point: QPointF) -> bool:
```
#     重写实例方法：判断点是否在路径内（接收 QPointF 点参数，返回布尔值）

```python
        return self._path.contains(point)
```
#         使用绘图路径的 contains 方法判断

```python

    def to_dict(self) -> dict:
```
#     重写实例方法：序列化为字典，返回字典

```python
        d = super().to_dict()
```
#         调用父类的序列化方法获取基础字典

```python
        d["points"] = self._points
```
#         添加点坐标列表

```python
        d["closed"] = self.closed
```
#         添加是否闭合标志

```python
        d["anchors"] = [a.to_dict() for a in self._anchors]
```
#         添加锚点列表（每个锚点序列化为字典）

```python
        return d
```
#         返回完整的序列化字典

```python

    @staticmethod
    def from_dict(data: dict) -> PathItem:
```
#     定义静态方法：从字典反序列化为路径项（接收字典参数，返回 PathItem）

```python
        item = GraphicItem.from_dict.__func__(None, data)
```
#         通过父类的 from_dict 方法解析通用属性

```python
        item.__class__ = PathItem
```
#         将实例的类改为 PathItem

```python
        item.item_type = "PathItem"
```
#         设置元素类型为 "PathItem"

```python
        item._points = data.get("points", [])
```
#         从字典获取点坐标列表（默认为空列表）

```python
        item.closed = data.get("closed", False)
```
#         从字典获取闭合标志（默认为 False）

```python
        anchors_data = data.get("anchors", [])
```
#         从字典获取锚点数据列表

```python
        if anchors_data:
```
#         如果存在锚点数据：

```python
            item._anchors = [AnchorPoint.from_dict(a) for a in anchors_data]
```
#             反序列化每个锚点

```python
        else:
```
#         否则：

```python
            item._anchors = [AnchorPoint(x, y) for x, y in item._points]
```
#             从点坐标列表创建无手柄锚点

```python
        item._build_path()
```
#         重建绘图路径

```python
        return item
```
#         返回反序列化后的路径项

---

```python

class RectangleItem(GraphicItem):
```
# 定义矩形项类，继承自 GraphicItem

```python
    """矩形项"""
```
#     类文档字符串：矩形项

```python

    __slots__ = ('_rect', '_corner_radius')
```
#     定义 \_\_slots\_\_：内部矩形对象、圆角半径

```python

    def __init__(self, x: float = 0, y: float = 0, w: float = 100, h: float = 100):
```
#     定义初始化方法（接收 x 坐标、y 坐标、宽度 w、高度 h 参数，各有默认值）

```python
        super().__init__("RectangleItem")
```
#         调用父类初始化，传入类型名 "RectangleItem"

```python
        self._rect = QRectF(x, y, w, h)
```
#         使用参数构造矩形对象

```python
        self._corner_radius: float = 0.0
```
#         初始化圆角半径为 0.0（直角）

```python

    @property
    def rect(self) -> QRectF:
```
#     定义只读属性：获取矩形，返回 QRectF

```python
        return self._rect
```
#         返回内部矩形对象

```python

    @rect.setter
    def rect(self, value: QRectF):
```
#     定义矩形设置器（接收 QRectF 矩形参数）

```python
        self._rect = value
```
#         设置内部矩形对象

```python

    @property
    def corner_radius(self) -> float:
```
#     定义只读属性：获取圆角半径，返回浮点数

```python
        return self._corner_radius
```
#         返回内部圆角半径值

```python

    @corner_radius.setter
    def corner_radius(self, value: float):
```
#     定义圆角半径设置器（接收浮点数值参数）

```python
        self._corner_radius = max(0, value)
```
#         确保圆角半径不小于 0

```python

    def painter_path(self) -> QPainterPath:
```
#     重写实例方法：获取绘图路径，返回 QPainterPath

```python
        path = QPainterPath()
```
#         创建新的空绘图路径

```python
        if self._corner_radius > 0:
```
#         如果圆角半径大于 0：

```python
            path.addRoundedRect(self._rect, self._corner_radius, self._corner_radius)
```
#             添加圆角矩形

```python
        else:
```
#         否则：

```python
            path.addRect(self._rect)
```
#             添加普通矩形

```python
        return path
```
#         返回绘图路径

```python

    def bounding_rect(self) -> QRectF:
```
#     重写实例方法：获取包围矩形，返回 QRectF

```python
        return self._rect
```
#         返回内部矩形对象

```python

    def contains_point(self, point: QPointF) -> bool:
```
#     重写实例方法：判断点是否在矩形内（接收 QPointF 点参数，返回布尔值）

```python
        return self.painter_path().contains(point)
```
#         使用绘图路径的 contains 方法判断

```python

    def to_dict(self) -> dict:
```
#     重写实例方法：序列化为字典，返回字典

```python
        d = super().to_dict()
```
#         调用父类的序列化方法获取基础字典

```python
        d.update(x=self._rect.x(), y=self._rect.y(),
```
#         更新字典：添加矩形 x、y 坐标

```python
                 width=self._rect.width(), height=self._rect.height(),
```
#                 添加矩形宽度、高度

```python
                 corner_radius=self._corner_radius)
```
#                 添加圆角半径

```python
        return d
```
#         返回完整的序列化字典

```python

    @staticmethod
    def from_dict(data: dict) -> RectangleItem:
```
#     定义静态方法：从字典反序列化为矩形项（接收字典参数，返回 RectangleItem）

```python
        item = GraphicItem.from_dict.__func__(None, data)
```
#         通过父类的 from_dict 方法解析通用属性

```python
        item.__class__ = RectangleItem
```
#         将实例的类改为 RectangleItem

```python
        item.item_type = "RectangleItem"
```
#         设置元素类型为 "RectangleItem"

```python
        item._rect = QRectF(
```
#         使用字典数据构造矩形：

```python
            data.get("x", 0), data.get("y", 0),
```
#             x、y 坐标（默认为 0）

```python
            data.get("width", 100), data.get("height", 100),
```
#             宽度、高度（默认为 100）

```python
        )
```
#         矩形构造结束

```python
        item._corner_radius = data.get("corner_radius", 0.0)
```
#         从字典获取圆角半径（默认为 0.0）

```python
        return item
```
#         返回反序列化后的矩形项

---

```python

class EllipseItem(GraphicItem):
```
# 定义椭圆项类，继承自 GraphicItem

```python
    """椭圆项"""
```
#     类文档字符串：椭圆项

```python

    __slots__ = ('_rect',)
```
#     定义 \_\_slots\_\_：内部矩形对象（椭圆的外接矩形）

```python

    def __init__(self, x: float = 0, y: float = 0, w: float = 100, h: float = 100):
```
#     定义初始化方法（接收 x 坐标、y 坐标、宽度 w、高度 h 参数，各有默认值）

```python
        super().__init__("EllipseItem")
```
#         调用父类初始化，传入类型名 "EllipseItem"

```python
        self._rect = QRectF(x, y, w, h)
```
#         使用参数构造外接矩形对象

```python

    @property
    def rect(self) -> QRectF:
```
#     定义只读属性：获取外接矩形，返回 QRectF

```python
        return self._rect
```
#         返回内部矩形对象

```python

    @rect.setter
    def rect(self, value: QRectF):
```
#     定义外接矩形设置器（接收 QRectF 矩形参数）

```python
        self._rect = value
```
#         设置内部矩形对象

```python

    def painter_path(self) -> QPainterPath:
```
#     重写实例方法：获取绘图路径，返回 QPainterPath

```python
        path = QPainterPath()
```
#         创建新的空绘图路径

```python
        path.addEllipse(self._rect)
```
#         在矩形区域内添加椭圆

```python
        return path
```
#         返回绘图路径

```python

    def bounding_rect(self) -> QRectF:
```
#     重写实例方法：获取包围矩形，返回 QRectF

```python
        return self._rect
```
#         返回外接矩形

```python

    def contains_point(self, point: QPointF) -> bool:
```
#     重写实例方法：使用椭圆方程判断点是否在椭圆内（接收 QPointF 点参数，返回布尔值）

```python
        cx = self._rect.center().x()
```
#         获取椭圆中心 x 坐标

```python
        cy = self._rect.center().y()
```
#         获取椭圆中心 y 坐标

```python
        rx = self._rect.width() / 2
```
#         计算 x 方向半径

```python
        ry = self._rect.height() / 2
```
#         计算 y 方向半径

```python
        if rx == 0 or ry == 0:
```
#         如果任一半径为 0（退化椭圆）：

```python
            return False
```
#             返回 False（不包含任何点）

```python
        return ((point.x() - cx) ** 2 / rx ** 2 + (point.y() - cy) ** 2 / ry ** 2) <= 1
```
#         使用椭圆标准方程判断点是否在椭圆内或边界上

```python

    def to_dict(self) -> dict:
```
#     重写实例方法：序列化为字典，返回字典

```python
        d = super().to_dict()
```
#         调用父类的序列化方法获取基础字典

```python
        d.update(x=self._rect.x(), y=self._rect.y(),
```
#         更新字典：添加外接矩形 x、y 坐标

```python
                 width=self._rect.width(), height=self._rect.height())
```
#                 添加外接矩形宽度、高度

```python
        return d
```
#         返回完整的序列化字典

```python

    @staticmethod
    def from_dict(data: dict) -> EllipseItem:
```
#     定义静态方法：从字典反序列化为椭圆项（接收字典参数，返回 EllipseItem）

```python
        item = GraphicItem.from_dict.__func__(None, data)
```
#         通过父类的 from_dict 方法解析通用属性

```python
        item.__class__ = EllipseItem
```
#         将实例的类改为 EllipseItem

```python
        item.item_type = "EllipseItem"
```
#         设置元素类型为 "EllipseItem"

```python
        item._rect = QRectF(
```
#         使用字典数据构造外接矩形：

```python
            data.get("x", 0), data.get("y", 0),
```
#             x、y 坐标（默认为 0）

```python
            data.get("width", 100), data.get("height", 100),
```
#             宽度、高度（默认为 100）

```python
        )
```
#         矩形构造结束

```python
        return item
```
#         返回反序列化后的椭圆项

---

```python

class TextFrame(GraphicItem):
```
# 定义文本框类，继承自 GraphicItem

```python
    """文本框"""
```
#     类文档字符串：文本框

```python

    __slots__ = ('_rect', '_contents', '_text_type', 'char_attrs', 'para_attrs')
```
#     定义 \_\_slots\_\_：内部矩形、文本内容、文字类型、字符属性、段落属性

```python

    def __init__(self, x: float = 0, y: float = 0):
```
#     定义初始化方法（接收 x 坐标、y 坐标参数，各有默认值 0）

```python
        super().__init__("TextFrame")
```
#         调用父类初始化，传入类型名 "TextFrame"

```python
        self._rect = QRectF(x, y, 200, 30)
```
#         创建默认文本框矩形（宽 200、高 30）

```python
        self._contents: str = ""
```
#         初始化文本内容为空字符串

```python
        self._text_type: TextType = TextType.POINT_TEXT
```
#         设置默认文字类型为点文字

```python
        self.char_attrs = CharacterAttributes()
```
#         创建默认字符属性实例

```python
        self.para_attrs = ParagraphAttributes()
```
#         创建默认段落属性实例

```python

    @property
    def contents(self) -> str:
```
#     定义只读属性：获取文本内容，返回字符串

```python
        return self._contents
```
#         返回内部文本内容

```python

    @contents.setter
    def contents(self, value: str):
```
#     定义文本内容设置器（接收字符串值参数）

```python
        self._contents = value
```
#         设置内部文本内容

```python

    @property
    def text_type(self) -> TextType:
```
#     定义只读属性：获取文字类型，返回 TextType 枚举

```python
        return self._text_type
```
#         返回内部文字类型

```python

    @property
    def rect(self) -> QRectF:
```
#     定义只读属性：获取文本框矩形，返回 QRectF

```python
        return self._rect
```
#         返回内部矩形对象

```python

    @rect.setter
    def rect(self, value: QRectF):
```
#     定义文本框矩形设置器（接收 QRectF 矩形参数）

```python
        self._rect = value
```
#         设置内部矩形对象

```python

    def painter_path(self) -> QPainterPath:
```
#     重写实例方法：获取绘图路径，返回 QPainterPath

```python
        path = QPainterPath()
```
#         创建新的空绘图路径

```python
        path.addRect(self._rect)
```
#         添加文本框矩形

```python
        return path
```
#         返回绘图路径

```python

    def bounding_rect(self) -> QRectF:
```
#     重写实例方法：获取包围矩形，返回 QRectF

```python
        return self._rect
```
#         返回文本框矩形

```python

    def contains_point(self, point: QPointF) -> bool:
```
#     重写实例方法：判断点是否在文本框内（接收 QPointF 点参数，返回布尔值）

```python
        return self._rect.contains(point)
```
#         使用矩形的 contains 方法判断

```python

    def to_dict(self) -> dict:
```
#     重写实例方法：序列化为字典，返回字典

```python
        d = super().to_dict()
```
#         调用父类的序列化方法获取基础字典

```python
        d.update(
```
#         更新字典，添加以下字段：

```python
            x=self._rect.x(), y=self._rect.y(),
```
#             文本框 x、y 坐标

```python
            width=self._rect.width(), height=self._rect.height(),
```
#             文本框宽度、高度

```python
            contents=self._contents,
```
#             文本内容

```python
            text_type=self._text_type.name,
```
#             文字类型名称字符串

```python
            font_family=self.char_attrs.font_family,
```
#             字体族名称

```python
            font_size=self.char_attrs.font_size,
```
#             字号大小

```python
            bold=self.char_attrs.bold,
```
#             是否加粗

```python
            italic=self.char_attrs.italic,
```
#             是否斜体

```python
            underline=self.char_attrs.underline,
```
#             是否下划线

```python
            justification=self.para_attrs.justification.name,
```
#             对齐方式名称字符串

```python
        )
```
#         字典更新结束

```python
        return d
```
#         返回完整的序列化字典

```python

    @staticmethod
    def from_dict(data: dict) -> TextFrame:
```
#     定义静态方法：从字典反序列化为文本框（接收字典参数，返回 TextFrame）

```python
        item = GraphicItem.from_dict.__func__(None, data)
```
#         通过父类的 from_dict 方法解析通用属性

```python
        item.__class__ = TextFrame
```
#         将实例的类改为 TextFrame

```python
        item.item_type = "TextFrame"
```
#         设置元素类型为 "TextFrame"

```python
        item._rect = QRectF(
```
#         使用字典数据构造文本框矩形：

```python
            data.get("x", 0), data.get("y", 0),
```
#             x、y 坐标（默认为 0）

```python
            data.get("width", 200), data.get("height", 30),
```
#             宽度（默认 200）、高度（默认 30）

```python
        )
```
#         矩形构造结束

```python
        item._contents = data.get("contents", "")
```
#         从字典获取文本内容（默认为空字符串）

```python
        item.char_attrs.font_family = data.get("font_family", "Arial")
```
#         从字典获取字体族名称（默认为 "Arial"）

```python
        item.char_attrs.font_size = data.get("font_size", 12.0)
```
#         从字典获取字号大小（默认为 12.0）

```python
        item.char_attrs.bold = data.get("bold", False)
```
#         从字典获取是否加粗（默认为 False）

```python
        item.char_attrs.italic = data.get("italic", False)
```
#         从字典获取是否斜体（默认为 False）

```python
        item.char_attrs.underline = data.get("underline", False)
```
#         从字典获取是否有下划线（默认为 False）

```python
        return item
```
#         返回反序列化后的文本框

---

```python

class GroupItem(GraphicItem):
```
# 定义编组项类，继承自 GraphicItem

```python
    """编组"""
```
#     类文档字符串：编组

```python

    __slots__ = ('_items',)
```
#     定义 \_\_slots\_\_：子项列表

```python

    def __init__(self):
```
#     定义初始化方法（无额外参数）

```python
        super().__init__("GroupItem")
```
#         调用父类初始化，传入类型名 "GroupItem"

```python
        self._items: list[GraphicItem] = []
```
#         初始化子项列表为空列表

```python

    @property
    def items(self) -> list[GraphicItem]:
```
#     定义只读属性：获取子项列表，返回 GraphicItem 列表

```python
        return self._items
```
#         返回内部子项列表

```python

    def add_item(self, item: GraphicItem):
```
#     定义实例方法：添加子项（接收 GraphicItem 图形项参数）

```python
        item._parent = self
```
#         将子项的父级引用设为当前编组

```python
        self._items.append(item)
```
#         将子项追加到子项列表

```python

    def remove_item(self, item: GraphicItem):
```
#     定义实例方法：移除子项（接收 GraphicItem 图形项参数）

```python
        if item in self._items:
```
#         如果子项存在于列表中：

```python
            item._parent = None
```
#             清除子项的父级引用

```python
            self._items.remove(item)
```
#             从子项列表中移除

```python

    def painter_path(self) -> QPainterPath:
```
#     重写实例方法：获取所有可见子项的合并绘图路径，返回 QPainterPath

```python
        path = QPainterPath()
```
#         创建新的空绘图路径

```python
        for item in self._items:
```
#         遍历所有子项：

```python
            if item.visible:
```
#             如果子项可见：

```python
                path.addPath(item.painter_path())
```
#                 将子项的绘图路径合并到总路径

```python
        return path
```
#         返回合并后的绘图路径

```python

    def bounding_rect(self) -> QRectF:
```
#     重写实例方法：获取所有子项的合并包围矩形，返回 QRectF

```python
        if not self._items:
```
#         如果没有子项：

```python
            return QRectF()
```
#             返回空矩形

```python
        rect = self._items[0].bounding_rect()
```
#         以第一个子项的包围矩形为初始值

```python
        for item in self._items[1:]:
```
#         从第二个子项开始遍历：

```python
            rect = rect.united(item.bounding_rect())
```
#             将当前子项的包围矩形合并到总矩形

```python
        return rect
```
#         返回合并后的包围矩形

```python

    def contains_point(self, point: QPointF) -> bool:
```
#     重写实例方法：判断点是否在任一子项内（接收 QPointF 点参数，返回布尔值）

```python
        return any(item.contains_point(point) for item in self._items)
```
#         使用 any 判断是否有任一子项包含该点

```python

    def to_dict(self) -> dict:
```
#     重写实例方法：序列化为字典，返回字典

```python
        d = super().to_dict()
```
#         调用父类的序列化方法获取基础字典

```python
        d["items"] = [item.to_dict() for item in self._items]
```
#         添加子项列表（每个子项序列化为字典）

```python
        return d
```
#         返回完整的序列化字典

```python

    @staticmethod
    def from_dict(data: dict) -> GroupItem:
```
#     定义静态方法：从字典反序列化为编组项（接收字典参数，返回 GroupItem）

```python
        item = GraphicItem.from_dict.__func__(None, data)
```
#         通过父类的 from_dict 方法解析通用属性

```python
        item.__class__ = GroupItem
```
#         将实例的类改为 GroupItem

```python
        item.item_type = "GroupItem"
```
#         设置元素类型为 "GroupItem"

```python
        item._items = [GraphicItem.from_dict(i) for i in data.get("items", [])]
```
#         递归反序列化所有子项

```python
        for sub in item._items:
```
#         遍历所有子项：

```python
            sub._parent = item
```
#             设置子项的父级引用为当前编组

```python
        return item
```
#         返回反序列化后的编组项

---

```python

# ── 色板 ────────────────────────────────────────────────────
```
# ── 色板分隔线 ──

```python

@dataclass(slots=True)
class Swatch:
```
# 使用 dataclass 装饰器（启用 slots 优化）定义色板类

```python
    """色板"""
```
#     类文档字符串：色板

```python
    name: str
```
#     色板名称（字符串）

```python
    color: QColor
```
#     色板颜色（QColor 颜色对象）

```python

    @staticmethod
    def default_swatches() -> list[Swatch]:
```
#     定义静态方法：创建默认色板列表，返回 Swatch 列表

```python
        colors = [
```
#         定义颜色列表，包含以下颜色元组：

```python
            ("黑色", QColor(0, 0, 0)),
```
#             黑色

```python
            ("白色", QColor(255, 255, 255)),
```
#             白色

```python
            ("红色", QColor(255, 0, 0)),
```
#             红色

```python
            ("绿色", QColor(0, 255, 0)),
```
#             绿色

```python
            ("蓝色", QColor(0, 0, 255)),
```
#             蓝色

```python
            ("黄色", QColor(255, 255, 0)),
```
#             黄色

```python
            ("青色", QColor(0, 255, 255)),
```
#             青色

```python
            ("品红", QColor(255, 0, 255)),
```
#             品红

```python
            ("灰色", QColor(128, 128, 128)),
```
#             灰色

```python
            ("橙色", QColor(255, 165, 0)),
```
#             橙色

```python
            ("紫色", QColor(128, 0, 128)),
```
#             紫色

```python
            ("棕色", QColor(139, 69, 19)),
```
#             棕色

```python
            ("粉色", QColor(255, 192, 203)),
```
#             粉色

```python
            ("深蓝", QColor(0, 0, 139)),
```
#             深蓝

```python
            ("森林绿", QColor(34, 139, 34)),
```
#             森林绿

```python
            ("金色", QColor(255, 215, 0)),
```
#             金色

```python
        ]
```
#         颜色列表定义结束

```python
        return [Swatch(name, color) for name, color in colors]
```
#         将颜色列表转换为色板对象列表并返回

---

```python

# ── 命令模式（撤销/重做） ──────────────────────────────────
```
# ── 命令模式（撤销/重做）分隔线 ──

```python

class Command(ABC):
```
# 定义命令抽象基类，继承自 ABC

```python
    """可撤销的命令基类（抽象基类）"""
```
#     类文档字符串：可撤销的命令基类（抽象基类）

```python
    __slots__ = ()
```
#     定义空 \_\_slots\_\_（无实例属性）

```python

    @abstractmethod
    def execute(self):
```
#     定义抽象方法：执行命令（子类必须实现）

```python
        ...
```
#         省略号占位符（抽象方法无默认实现）

```python

    @abstractmethod
    def undo(self):
```
#     定义抽象方法：撤销命令（子类必须实现）

```python
        ...
```
#         省略号占位符（抽象方法无默认实现）

```python

    def description(self) -> str:
```
#     定义实例方法：获取命令描述，返回字符串

```python
        return "操作"
```
#         返回默认描述 "操作"

---

```python

class AddItemCommand(Command):
```
# 定义添加图形项命令类，继承自 Command

```python
    """添加图形项"""
```
#     类文档字符串：添加图形项

```python
    __slots__ = ('document', 'item', 'layer')
```
#     定义 \_\_slots\_\_：文档引用、图形项、图层引用

```python

    def __init__(self, document, item, layer):
```
#     定义初始化方法（接收文档、图形项、图层参数）

```python
        self.document = document
```
#         保存文档引用

```python
        self.item = item
```
#         保存图形项引用

```python
        self.layer = layer
```
#         保存图层引用

```python

    def execute(self):
```
#     重写执行方法：执行添加操作

```python
        self.layer.add_item(self.item)
```
#         将图形项添加到图层

```python

    def undo(self):
```
#     重写撤销方法：撤销添加操作

```python
        self.layer.remove_item(self.item)
```
#         从图层中移除图形项

```python

    def description(self) -> str:
```
#     重写描述方法：获取命令描述，返回字符串

```python
        return f"添加 {self.item.item_type}"
```
#         返回 "添加 [元素类型]" 格式的描述

---

```python

class RemoveItemCommand(Command):
```
# 定义删除图形项命令类，继承自 Command

```python
    """删除图形项"""
```
#     类文档字符串：删除图形项

```python
    __slots__ = ('document', 'item', 'layer')
```
#     定义 \_\_slots\_\_：文档引用、图形项、图层引用

```python

    def __init__(self, document, item, layer):
```
#     定义初始化方法（接收文档、图形项、图层参数）

```python
        self.document = document
```
#         保存文档引用

```python
        self.item = item
```
#         保存图形项引用

```python
        self.layer = layer
```
#         保存图层引用

```python

    def execute(self):
```
#     重写执行方法：执行删除操作

```python
        self.layer.remove_item(self.item)
```
#         从图层中移除图形项

```python

    def undo(self):
```
#     重写撤销方法：撤销删除操作

```python
        self.layer.add_item(self.item)
```
#         将图形项重新添加到图层

```python

    def description(self) -> str:
```
#     重写描述方法：获取命令描述，返回字符串

```python
        return f"删除 {self.item.item_type}"
```
#         返回 "删除 [元素类型]" 格式的描述

---

```python

class MoveItemsCommand(Command):
```
# 定义移动图形项命令类，继承自 Command

```python
    """移动图形项"""
```
#     类文档字符串：移动图形项

```python
    __slots__ = ('document', 'items', 'dx', 'dy')
```
#     定义 \_\_slots\_\_：文档引用、图形项列表、x 偏移量、y 偏移量

```python

    def __init__(self, document, items, dx, dy):
```
#     定义初始化方法（接收文档、图形项列表、x 偏移量、y 偏移量参数）

```python
        self.document = document
```
#         保存文档引用

```python
        self.items = items
```
#         保存图形项列表

```python
        self.dx = dx
```
#         保存 x 方向偏移量

```python
        self.dy = dy
```
#         保存 y 方向偏移量

```python

    def execute(self):
```
#     重写执行方法：执行移动操作

```python
        for item in self.items:
```
#         遍历所有图形项：

```python
            item.move_by(self.dx, self.dy)
```
#             对每个图形项应用平移

```python

    def undo(self):
```
#     重写撤销方法：撤销移动操作

```python
        for item in self.items:
```
#         遍历所有图形项：

```python
            item.move_by(-self.dx, -self.dy)
```
#             对每个图形项应用反向平移

```python

    def description(self) -> str:
```
#     重写描述方法：获取命令描述，返回字符串

```python
        return f"移动 ({self.dx:.0f}, {self.dy:.0f})"
```
#         返回 "移动 (x偏移, y偏移)" 格式的描述（取整显示）

---

```python

class ChangeStyleCommand(Command):
```
# 定义修改样式命令类，继承自 Command

```python
    """修改样式"""
```
#     类文档字符串：修改样式

```python
    __slots__ = ('document', 'item', 'old_style', 'new_style')
```
#     定义 \_\_slots\_\_：文档引用、图形项、旧样式、新样式

```python

    def __init__(self, document, item, old_style, new_style):
```
#     定义初始化方法（接收文档、图形项、旧样式、新样式参数）

```python
        self.document = document
```
#         保存文档引用

```python
        self.item = item
```
#         保存图形项引用

```python
        self.old_style = old_style
```
#         保存旧样式

```python
        self.new_style = new_style
```
#         保存新样式

```python

    def execute(self):
```
#     重写执行方法：执行样式修改

```python
        self.item.style = self.new_style
```
#         将图形项的样式设为新样式

```python

    def undo(self):
```
#     重写撤销方法：撤销样式修改

```python
        self.item.style = self.old_style
```
#         将图形项的样式恢复为旧样式

```python

    def description(self) -> str:
```
#     重写描述方法：获取命令描述，返回字符串

```python
        return "修改样式"
```
#         返回 "修改样式"

---

```python

class ModifyAnchorCommand(Command):
```
# 定义修改贝塞尔锚点命令类，继承自 Command

```python
    """修改贝塞尔锚点"""
```
#     类文档字符串：修改贝塞尔锚点

```python
    __slots__ = ('document', 'item', 'old_anchors', 'new_anchors')
```
#     定义 \_\_slots\_\_：文档引用、图形项、旧锚点列表、新锚点列表

```python

    def __init__(self, document, item, old_anchors, new_anchors):
```
#     定义初始化方法（接收文档、图形项、旧锚点列表、新锚点列表参数）

```python
        self.document = document
```
#         保存文档引用

```python
        self.item = item
```
#         保存图形项引用

```python
        self.old_anchors = old_anchors
```
#         保存旧锚点列表

```python
        self.new_anchors = new_anchors
```
#         保存新锚点列表

```python

    def execute(self):
```
#     重写执行方法：执行锚点修改

```python
        self.item._anchors = [a.copy() for a in self.new_anchors]
```
#         将图形项的锚点列表设为新锚点列表的副本

```python
        self.item._rebuild_from_anchors()
```
#         从锚点列表重建路径

```python

    def undo(self):
```
#     重写撤销方法：撤销锚点修改

```python
        self.item._anchors = [a.copy() for a in self.old_anchors]
```
#         将图形项的锚点列表恢复为旧锚点列表的副本

```python
        self.item._rebuild_from_anchors()
```
#         从锚点列表重建路径

```python

    def description(self) -> str:
```
#     重写描述方法：获取命令描述，返回字符串

```python
        return "修改锚点"
```
#         返回 "修改锚点"

---

```python

class ResizeItemCommand(Command):
```
# 定义缩放图形项命令类，继承自 Command

```python
    """缩放图形项命令"""
```
#     类文档字符串：缩放图形项命令

```python
    __slots__ = ('document', 'item', 'old_rect', 'new_rect')
```
#     定义 \_\_slots\_\_：文档引用、图形项、旧矩形、新矩形

```python

    def __init__(self, document, item, old_rect: QRectF, new_rect: QRectF):
```
#     定义初始化方法（接收文档、图形项、旧矩形 QRectF、新矩形 QRectF 参数）

```python
        self.document = document
```
#         保存文档引用

```python
        self.item = item
```
#         保存图形项引用

```python
        self.old_rect = QRectF(old_rect)
```
#         拷贝旧矩形（避免引用共享）

```python
        self.new_rect = QRectF(new_rect)
```
#         拷贝新矩形（避免引用共享）

```python

    def execute(self):
```
#     重写执行方法：执行缩放

```python
        self._apply_rect(self.new_rect)
```
#         应用新矩形尺寸

```python

    def undo(self):
```
#     重写撤销方法：撤销缩放

```python
        self._apply_rect(self.old_rect)
```
#         恢复旧矩形尺寸

```python

    def description(self) -> str:
```
#     重写描述方法：获取命令描述，返回字符串

```python
        return "缩放"
```
#         返回 "缩放"

```python

    def _apply_rect(self, target: QRectF):
```
#     定义内部方法：根据目标矩形恢复尺寸（接收目标 QRectF 矩形参数）

```python
        """根据目标矩形恢复尺寸"""
```
#         方法文档字符串：根据目标矩形恢复尺寸

```python
        item = self.item
```
#         获取目标图形项引用

```python
        scale_x = target.width() / max(self.old_rect.width(), 0.001) if self.old_rect.width() > 0 else 1
```
#         计算 x 方向缩放比例（避免除零，默认缩放比为 1）

```python
        scale_y = target.height() / max(self.old_rect.height(), 0.001) if self.old_rect.height() > 0 else 1
```
#         计算 y 方向缩放比例（避免除零，默认缩放比为 1）

```python

        if isinstance(item, RectangleItem):
```
#         如果目标图形项是矩形项：

```python
            item.rect = QRectF(target.x(), target.y(), target.width(), target.height())
```
#             直接设置矩形为目标尺寸

```python
        elif isinstance(item, EllipseItem):
```
#         否则如果目标图形项是椭圆项：

```python
            item.rect = QRectF(target.x(), target.y(), target.width(), target.height())
```
#             直接设置外接矩形为目标尺寸

```python
        elif isinstance(item, PathItem):
```
#         否则如果目标图形项是路径项：

```python
            ref_x = target.x() if scale_x > 0 else target.right()
```
#             确定 x 方向参考点（正缩放用左边，负缩放用右边）

```python
            ref_y = target.y() if scale_y > 0 else target.bottom()
```
#             确定 y 方向参考点（正缩放用上边，负缩放用下边）

```python
            for anchor in item.anchors:
```
#             遍历所有锚点：

```python
                anchor.x = ref_x + (anchor.x - ref_x) * scale_x
```
#                 根据缩放比例调整锚点 x 坐标

```python
                anchor.y = ref_y + (anchor.y - ref_y) * scale_y
```
#                 根据缩放比例调整锚点 y 坐标

```python
                if anchor.handle_in:
```
#                 如果锚点有入控制手柄：

```python
                    anchor.handle_in = QPointF(
```
#                     按缩放比例调整手柄偏移：

```python
                        anchor.handle_in.x() * scale_x,
```
#                         手柄 x 偏移量乘以 x 缩放比

```python
                        anchor.handle_in.y() * scale_y,
```
#                         手柄 y 偏移量乘以 y 缩放比

```python
                    )
```
#                     QPointF 构造结束

```python
                if anchor.handle_out:
```
#                 如果锚点有出控制手柄：

```python
                    anchor.handle_out = QPointF(
```
#                     按缩放比例调整手柄偏移：

```python
                        anchor.handle_out.x() * scale_x,
```
#                         手柄 x 偏移量乘以 x 缩放比

```python
                        anchor.handle_out.y() * scale_y,
```
#                         手柄 y 偏移量乘以 y 缩放比

```python
                    )
```
#                     QPointF 构造结束

```python
            item._rebuild_from_anchors()
```
#             从锚点列表重建路径

```python
        elif isinstance(item, TextFrame):
```
#         否则如果目标图形项是文本框：

```python
            item.rect = QRectF(target.x(), target.y(), target.width(), target.height())
```
#             直接设置文本框矩形为目标尺寸

---

```python

class CommandHistory:
```
# 定义命令历史类（撤销/重做管理器）

```python
    """命令历史（撤销/重做管理）"""
```
#     类文档字符串：命令历史（撤销/重做管理）

```python
    __slots__ = ('_undo_stack', '_redo_stack', '_max_size')
```
#     定义 \_\_slots\_\_：撤销栈、重做栈、最大历史记录数

```python

    def __init__(self, max_size: int = 100):
```
#     定义初始化方法（接收最大历史记录数参数，默认为 100）

```python
        self._undo_stack: list[Command] = []
```
#         初始化撤销栈为空列表

```python
        self._redo_stack: list[Command] = []
```
#         初始化重做栈为空列表

```python
        self._max_size = max_size
```
#         保存最大历史记录数

```python

    def execute(self, command: Command):
```
#     定义实例方法：执行命令并加入历史（接收 Command 命令参数）

```python
        command.execute()
```
#         执行命令

```python
        self._undo_stack.append(command)
```
#         将命令压入撤销栈

```python
        self._redo_stack.clear()
```
#         清空重做栈（新操作后无法重做之前的操作）

```python
        if len(self._undo_stack) > self._max_size:
```
#         如果撤销栈超过最大记录数：

```python
            self._undo_stack.pop(0)
```
#             移除最旧的操作记录

```python

    def undo(self) -> Command | None:
```
#     定义实例方法：撤销操作，返回被撤销的命令或 None

```python
        if not self._undo_stack:
```
#         如果撤销栈为空：

```python
            return None
```
#             返回 None（无法撤销）

```python
        command = self._undo_stack.pop()
```
#         从撤销栈弹出最近的命令

```python
        command.undo()
```
#         执行命令的撤销操作

```python
        self._redo_stack.append(command)
```
#         将命令压入重做栈

```python
        return command
```
#         返回被撤销的命令

```python

    def redo(self) -> Command | None:
```
#     定义实例方法：重做操作，返回被重做的命令或 None

```python
        if not self._redo_stack:
```
#         如果重做栈为空：

```python
            return None
```
#             返回 None（无法重做）

```python
        command = self._redo_stack.pop()
```
#         从重做栈弹出最近的命令

```python
        command.execute()
```
#         重新执行命令

```python
        self._undo_stack.append(command)
```
#         将命令压回撤销栈

```python
        return command
```
#         返回被重做的命令

```python

    @property
    def can_undo(self) -> bool:
```
#     定义只读属性：判断是否可以撤销，返回布尔值

```python
        return len(self._undo_stack) > 0
```
#         返回撤销栈是否非空

```python

    @property
    def can_redo(self) -> bool:
```
#     定义只读属性：判断是否可以重做，返回布尔值

```python
        return len(self._redo_stack) > 0
```
#         返回重做栈是否非空

```python

    @property
    def undo_description(self) -> str:
```
#     定义只读属性：获取撤销操作的描述文本，返回字符串

```python
        return self._undo_stack[-1].description() if self._undo_stack else ""
```
#         如果撤销栈非空则返回栈顶命令的描述，否则返回空字符串

```python

    @property
    def redo_description(self) -> str:
```
#     定义只读属性：获取重做操作的描述文本，返回字符串

```python
        return self._redo_stack[-1].description() if self._redo_stack else ""
```
#         如果重做栈非空则返回栈顶命令的描述，否则返回空字符串

```python

    def clear(self):
```
#     定义实例方法：清空所有历史记录

```python
        self._undo_stack.clear()
```
#         清空撤销栈

```python
        self._redo_stack.clear()
```
#         清空重做栈
