"""
DeepSeek LLM 客户端 — 封装 API 调用

DeepSeek API 兼容 OpenAI 接口格式：
- Base URL: https://api.deepseek.com/v1
- 推荐模型: deepseek-chat (V3), deepseek-reasoner (R1)
"""

import json
import logging
from typing import Dict, Any, List, Optional, Callable

logger = logging.getLogger(__name__)


class DeepSeekClient:
    """DeepSeek API 客户端"""
    # 类属性；
    DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
    DEFAULT_MODEL = "deepseek-chat"

    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = None,
    ):
        self.api_key = api_key or ""
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.model = model or self.DEFAULT_MODEL

    def chat_sync(
        self,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> Dict:
        """同步调用 Chat API"""
        import urllib.request
        import urllib.error
        # 构建请求头字典，授权字段使用Bearer令牌加接口秘钥
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        # 构建请求头字典：内容类型为json，并添加API密钥
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"
        # 构建请求对象，请求地址为基础地址拼接聊天补全路径，请求体为JSON格式的UTF-8编码，设置请求头，使用POST方法
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            # 发送HTTP请求，并获取响应，超时时间设为120秒，使用上下文管理器
            with urllib.request.urlopen(req, timeout=120) as resp:
                # 读取响应内容并解码为UTF-8字符串，解析JSON后返回字典
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            # 若错误响应存在文件指针则读取并解码错误体，否则为空字符串
            error_body = e.read().decode("utf-8") if e.fp else ""
            logger.error(f"DeepSeek API HTTP {e.code}: {error_body}")
            raise RuntimeError(f"API 请求失败 ({e.code}): {error_body[:200]}")
        except Exception as e:
            # 记录错误日志：深度求索API发生异常及异常信息
            logger.error(f"DeepSeek API error: {e}")
            # 抛出运行时错误：API连接失败，附带异常信息
            raise RuntimeError(f"API 连接失败: {e}")
    # 同步流式聊天方法
    def chat_sync_stream(
        self,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        on_chunk: Callable[[str], None] = None,
    ) -> str:
        """同步流式调用（通过 SSE 模拟）"""
        import urllib.request
        import urllib.error

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        body = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"

        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        # 初始化完整文本变量为空字符串，用于累积所有流式片段
        full_text = ""
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                for line in resp:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
                            if "content" in delta and delta["content"]:
                                text = delta["content"]
                                full_text += text
                                # 如果提供了分块回调函数，调用
                                if on_chunk:
                                    on_chunk(text)
                        except json.JSONDecodeError:
                            # 捕获JSON解码错误异常
                            continue
        except urllib.error.HTTPError as e:
            # 捕获HTTP错误异常，赋值给变量e
            error_body = e.read().decode("utf-8") if e.fp else ""
            # 抛出运行时错误：API流式请求失败，附带状态码
            raise RuntimeError(f"API 流式请求失败 ({e.code}): {error_body[:200]}")
        except Exception as e:
            raise RuntimeError(f"API 连接失败: {e}")

        return full_text


# ── 海报生成工具（纯 Python，不依赖 MCP） ──────────────

POSTER_TEMPLATES = {
    "social_media": {
        "name": "高考宣传海报", "description": "适合校园张贴，简约干净",
        "width": 1280, "height": 1620, "layout": "centered",
    },
    "event_banner": {
        "name": "活动横幅海报", "description": "适合活动宣传、横幅广告",
        "width": 1920, "height": 1080, "layout": "banner",
    },
    "product_showcase": {
        "name": "产品展示海报", "description": "适合电商产品展示",
        "width": 1200, "height": 1600, "layout": "vertical",
    },
    "minimalist": {
        "name": "极简海报", "description": "简约现代风格",
        "width": 1200, "height": 800, "layout": "minimal",
    },
    "promotion": {
        "name": "促销海报", "description": "适合促销活动、限时优惠",
        "width": 1200, "height": 900, "layout": "promo",
    },
    "poster_a4": {
        "name": "A4 竖版海报", "description": "标准A4尺寸，适合打印",
        "width": 2480, "height": 3508, "layout": "portrait",
    },
}

COLOR_SCHEMES = {
    "modern_blue": {
        "name": "现代蓝",
        "primary": "#2563EB", "secondary": "#3B82F6", "accent": "#F59E0B",
        "bg": "#F0F4FF", "text": "#1E3A5F", "light": "#DBEAFE", "dark": "#1E40AF",
    },
    "warm_sunset": {
        "name": "暖橙日落",
        "primary": "#EA580C", "secondary": "#F97316", "accent": "#FCD34D",
        "bg": "#FFF7ED", "text": "#431407", "light": "#FED7AA", "dark": "#9A3412",
    },
    "elegant_dark": {
        "name": "优雅暗黑",
        "primary": "#1F2937", "secondary": "#374151", "accent": "#F59E0B",
        "bg": "#111827", "text": "#F9FAFB", "light": "#4B5563", "dark": "#030712",
    },
    "fresh_green": {
        "name": "清新绿",
        "primary": "#059669", "secondary": "#10B981", "accent": "#FBBF24",
        "bg": "#ECFDF5", "text": "#064E3B", "light": "#A7F3D0", "dark": "#065F46",
    },
    "vibrant_purple": {
        "name": "活力紫",
        "primary": "#7C3AED", "secondary": "#8B5CF6", "accent": "#F472B6",
        "bg": "#F5F3FF", "text": "#2E1065", "light": "#DDD6FE", "dark": "#5B21B6",
    },
    "corporate_red": {
        "name": "企业红",
        "primary": "#DC2626", "secondary": "#EF4444", "accent": "#FCD34D",
        "bg": "#FEF2F2", "text": "#7F1D1D", "light": "#FECACA", "dark": "#991B1B",
    },
    "ocean_teal": {
        "name": "海洋青",
        "primary": "#0D9488", "secondary": "#14B8A6", "accent": "#F97316",
        "bg": "#F0FDFA", "text": "#134E4A", "light": "#99F6E4", "dark": "#115E59",
    },
    "rose_gold": {
        "name": "玫瑰金",
        "primary": "#BE185D", "secondary": "#EC4899", "accent": "#FCD34D",
        "bg": "#FFF1F2", "text": "#4C0519", "light": "#FBCFE8", "dark": "#831843",
    },
    "deepseek_blue": {
        "name": "DeepSeek 蓝",
        "primary": "#4D6BFE", "secondary": "#6B8AFF", "accent": "#00D4AA",
        "bg": "#F5F7FF", "text": "#1A1A2E", "light": "#E0E7FF", "dark": "#3730A3",
    },
}

SYSTEM_PROMPT = """你是一个专业的 Illustrator 矢量设计 AI 助手，运行在桌面矢量图形编辑器中。

## 核心能力

### 1. 矢量海报生成
你可以一键生成专业矢量海报。当用户提到"海报"、"banner"、"宣传图"、"封面"、"促销图"等关键词时使用。

**可用海报模板：**
- social_media (1080×1080): Instagram/微博方形海报
- event_banner (1920×1080): 活动横幅广告
- product_showcase (1200×1600): 产品展示竖版海报
- minimalist (1200×800): 极简现代风格海报
- promotion (1200×900): 促销优惠海报
- poster_a4 (2480×3508): A4打印竖版海报

**可用颜色方案：**
- modern_blue: 现代蓝（科技/商务）
- warm_sunset: 暖橙日落（活力/温暖）
- elegant_dark: 优雅暗黑（高端/奢华）
- fresh_green: 清新绿（自然/健康）
- vibrant_purple: 活力紫（创意/时尚）
- corporate_red: 企业红（促销/活动）
- ocean_teal: 海洋青（清爽/专业）
- rose_gold: 玫瑰金（女性/精致）
- deepseek_blue: DeepSeek蓝（AI/科技）

### 2. 矢量图形绘制
你可以在画布上绘制矢量图形：矩形、椭圆、文字、钢笔、线条等。

### 3. 交互式问答
当用户描述模糊时，主动追问关键信息：
1. 海报用途/场景 → 选择合适的模板
2. 标题文字 → 主标题内容
3. 风格偏好 → 选择合适的颜色方案
4. 额外信息 → 副标题、描述、CTA按钮等

## 工具使用

**生成海报时：**
调用 generate_poster 工具，参数包括 template, title, subtitle, description, color_scheme, cta_text, badge_text

**示例对话：**
用户："帮我做个促销海报"
助手："好的！请告诉我：1. 促销内容？2. 折扣力度？3. 喜欢的颜色风格？4. 需要什么行动号召？"

用户："618大促，全场5折，红色风格，立即抢购"
助手：调用 generate_poster(template="promotion", title="618年中大促", subtitle="全场5折", color_scheme="corporate_red", cta_text="立即抢购")

**回复要求：**
- 用中文回复
- 简洁清晰地说明操作结果
- 描述生成的海报内容"""

# parameters
def build_tools_for_deepseek() -> List[Dict]:
    """构建 DeepSeek 可用的工具定义"""
    return [{
        "type": "function",
        "function": {
            "name": "generate_poster",
            "description": "一键生成矢量海报。根据模板和参数自动完成背景、排版、装饰元素。支持6种模板和9种配色方案。",
            "parameters": {
                "type": "object",
                "properties": {
                    "template": {
                        "type": "string",
                        "description": "海报模板",
                        "enum": list(POSTER_TEMPLATES.keys()),
                    },
                    "title": {
                        "type": "string",
                        "description": "主标题文字",
                    },
                    "subtitle": {
                        "type": "string",
                        "description": "副标题/辅助文字",
                    },
                    "description": {
                        "type": "string",
                        "description": "描述文字",
                    },
                    "color_scheme": {
                        "type": "string",
                        "description": "颜色方案",
                        "enum": list(COLOR_SCHEMES.keys()),
                    },
                    "cta_text": {
                        "type": "string",
                        "description": "行动号召按钮文字（如'立即抢购'）",
                    },
                    "badge_text": {
                        "type": "string",
                        "description": "徽章/标签文字（如'NEW'、'限时'）",
                    },
                },
                "required": ["template", "title"],
            },
        },
    }]
