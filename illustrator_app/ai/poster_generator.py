"""
海报生成器 — 根据 AI 参数在文档中生成矢量海报元素

根据模板和配色方案自动创建背景、标题、副标题等元素。
"""

from __future__ import annotations

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor

from ..core.graphics import (
    GraphicItem, RectangleItem, EllipseItem, TextFrame,
    GraphicStyle, Justification,
)


class PosterGenerator:
    """海报生成器 —— 在文档中创建矢量海报"""
    # 类的文档字符串：海报生成器，在文档中创建矢量海报
    def __init__(self, document):
        self._document = document

    def generate(self, params: dict) -> dict:
        """根据参数生成海报

        Args:
            params: {
                "template": str,
                "title": str,
                "subtitle": str | None,
                "description": str | None,
                "color_scheme": str,
                "cta_text": str | None,
                "badge_text": str | None,
            }

        Returns:
            {"success": bool, "message": str}
        """
        # 如果文档对象 _document 为空，则执行以下返回
        if not self._document:
            return {"success": False, "message": "文档未初始化"}
        # 模版名称，标题，副标题，描述，配色方案，行动号召文字，徽章文字
        template = params.get("template", "social_media")
        title = params.get("title", "新海报")
        subtitle = params.get("subtitle", "")
        description = params.get("description", "")
        color_scheme = params.get("color_scheme", "modern_blue")
        cta_text = params.get("cta_text", "")
        badge_text = params.get("badge_text", "")

        from .deepseek_client import POSTER_TEMPLATES, COLOR_SCHEMES
        # 
        tmpl = POSTER_TEMPLATES.get(template)
        if tmpl:
            self._document.width = tmpl["width"]
            self._document.height = tmpl["height"]
        # 根据配色方案名称获取对应配色，若未找到则回退使用
        # 主色，次色，强调色，背景色，文字色，暗色
        scheme = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["modern_blue"])
        primary = QColor(scheme["primary"])
        secondary = QColor(scheme["secondary"])
        accent = QColor(scheme["accent"])
        bg_color = QColor(scheme["bg"])
        text_color = QColor(scheme["text"])
        dark_color = QColor(scheme["dark"])
        # 将文字的宽度和高度分别赋值给变量w 和 h
        w, h = self._document.width, self._document.height
        # 将文档的宽度和高度分别赋值给变量w 和 h

        # 清空现有内容（保留第一个默认图层）
        for layer in self._document.layers:
            for item in list(layer.items):
                layer.remove_item(item)

        # 1. 背景矩形
        bg = RectangleItem(0, 0, w, h)
        bg.style.fill_color = bg_color
        bg.style.stroke_color = None
        bg.style.stroke_width = 0
        bg.name = "背景"
        self._document.add_item(bg)

        # 2. 顶部装饰条
        top_bar_h = h * 0.08
        top_bar = RectangleItem(0, 0, w, top_bar_h)
        top_bar.style.fill_color = primary
        top_bar.style.stroke_color = None
        top_bar.style.stroke_width = 0
        top_bar.name = "顶部装饰"
        self._document.add_item(top_bar)

        # 3. 底部装饰区
        bottom_h = h * 0.12
        bottom_bar = RectangleItem(0, h - bottom_h, w, bottom_h)
        bottom_bar.style.fill_color = dark_color
        bottom_bar.style.stroke_color = None
        bottom_bar.style.stroke_width = 0
        bottom_bar.name = "底部装饰"
        self._document.add_item(bottom_bar)

        # 4. 主标题
        title_y = h * 0.22
        # 创建文本框作为主标题容器
        title_font_size = min(w * 0.055, 72)
        # 创建文本框作为主标题容器
        title_frame = TextFrame(w * 0.05, title_y)
        # 设置主标题文本框的矩形区域
        title_frame._rect = QRectF(w * 0.05, title_y, w * 0.9, title_font_size * 1.8)
        title_frame.contents = title
        title_frame.char_attrs.font_family = "微软雅黑"
        title_frame.char_attrs.font_size = title_font_size
        title_frame.char_attrs.bold = True
        title_frame.char_attrs.fill_color = text_color
        # 设置主标题的段落对齐方式
        title_frame.para_attrs.justification = Justification.CENTER
        # 设置主标题文本框的填充颜色
        title_frame.style.fill_color = None
        title_frame.name = "主标题"
        self._document.add_item(title_frame)

        # 5. 副标题；创建副标题文本框
        if subtitle:
            sub_y = title_y + title_font_size * 2
            sub_font_size = title_font_size * 0.55
            sub_frame = TextFrame(w * 0.1, sub_y)
            sub_frame._rect = QRectF(w * 0.1, sub_y, w * 0.8, sub_font_size * 1.5)
            sub_frame.contents = subtitle
            sub_frame.char_attrs.font_family = "微软雅黑"
            sub_frame.char_attrs.font_size = sub_font_size
            sub_frame.char_attrs.fill_color = text_color
            sub_frame.para_attrs.justification = Justification.CENTER
            sub_frame.style.fill_color = None
            sub_frame.name = "副标题"
            self._document.add_item(sub_frame)

        # 6. 描述文字；
        if description:
            desc_y = (title_y + title_font_size * 2.2 +
                      (subtitle and (title_font_size * 0.55 * 1.5 + 20) or 0))
            desc_font_size = title_font_size * 0.35
            desc_frame = TextFrame(w * 0.12, desc_y)
            desc_frame._rect = QRectF(w * 0.12, desc_y, w * 0.76, desc_font_size * 3)
            desc_frame.contents = description
            desc_frame.char_attrs.font_family = "微软雅黑"
            desc_frame.char_attrs.font_size = desc_font_size
            desc_frame.char_attrs.fill_color = QColor(
                min(text_color.red() + 80, 255),
                min(text_color.green() + 80, 255),
                min(text_color.blue() + 80, 255),
            )
            desc_frame.para_attrs.justification = Justification.CENTER
            desc_frame.style.fill_color = None
            desc_frame.name = "描述"
            self._document.add_item(desc_frame)

        # 7. CTA 按钮（行动号召）
        if cta_text:
            btn_w = w * 0.3
            btn_h = h * 0.07
            btn_x = (w - btn_w) / 2
            btn_y = h * 0.78
            btn_bg = RectangleItem(btn_x, btn_y, btn_w, btn_h)
            btn_bg.style.fill_color = accent
            btn_bg.style.stroke_color = None
            btn_bg.style.stroke_width = 0
            btn_bg._corner_radius = btn_h / 2
            btn_bg.name = "CTA按钮背景"
            self._document.add_item(btn_bg)

            cta_font_size = btn_h * 0.5
            cta_frame = TextFrame(btn_x, btn_y)
            cta_frame._rect = QRectF(btn_x, btn_y, btn_w, btn_h)
            cta_frame.contents = cta_text
            cta_frame.char_attrs.font_family = "微软雅黑"
            cta_frame.char_attrs.font_size = cta_font_size
            cta_frame.char_attrs.bold = True
            cta_frame.char_attrs.fill_color = QColor(255, 255, 255)
            cta_frame.para_attrs.justification = Justification.CENTER
            cta_frame.style.fill_color = None
            cta_frame.name = "CTA文字"
            self._document.add_item(cta_frame)

        # 8. 徽章；计算徽章尺寸；计算徽章坐标；
        if badge_text:
            badge_size = min(w, h) * 0.1
            badge_x = w * 0.8
            badge_y = h * 0.15
            badge_circle = EllipseItem(badge_x, badge_y, badge_size, badge_size)
            badge_circle.style.fill_color = secondary
            badge_circle.style.stroke_color = QColor(255, 255, 255)
            badge_circle.style.stroke_width = 2.0
            badge_circle.name = "徽章背景"
            self._document.add_item(badge_circle)

            badge_font_size = badge_size * 0.3
            badge_frame = TextFrame(badge_x, badge_y)
            badge_frame._rect = QRectF(badge_x, badge_y, badge_size, badge_size)
            badge_frame.contents = badge_text
            badge_frame.char_attrs.font_family = "微软雅黑"
            badge_frame.char_attrs.font_size = badge_font_size
            badge_frame.char_attrs.bold = True
            badge_frame.char_attrs.fill_color = QColor(255, 255, 255)
            badge_frame.para_attrs.justification = Justification.CENTER
            badge_frame.style.fill_color = None
            badge_frame.name = "徽章文字"
            self._document.add_item(badge_frame)

        # 9. 装饰圆点（左下角）
        # 计算装饰圆点的尺寸和位置；
        dot_size = min(w, h) * 0.04
        dot_x = w * 0.05
        dot_y = h - bottom_h - dot_size - 10
        dot = EllipseItem(dot_x, dot_y, dot_size, dot_size)
        dot.style.fill_color = accent
        dot.style.stroke_color = None
        dot.style.stroke_width = 0
        dot.name = "装饰圆点"
        self._document.add_item(dot)

        # 第二个装饰圆点
        dot2_size = dot_size * 0.6
        dot2 = EllipseItem(dot_x + dot_size + 10, dot_y + dot_size * 0.2, dot2_size, dot2_size)
        dot2.style.fill_color = secondary
        dot2.style.stroke_color = None
        dot2.style.stroke_width = 0
        dot2.name = "装饰圆点2"
        self._document.add_item(dot2)
        # 将文档的修改标记设为True
        self._document.modified = True
        return {"success": True, "message": f"海报「{title}」已生成"}
