# deepseek_client.py 中文注解翻译

---

```python
"""
DeepSeek LLM 客户端 — 封装 API 调用

DeepSeek API 兼容 OpenAI 接口格式：
- Base URL: https://api.deepseek.com/v1
- 推荐模型: deepseek-chat (V3), deepseek-reasoner (R1)
"""
```
# 模块文档字符串：深度求索大语言模型客户端，用于封装API调用
# 深度求索API兼容OpenAI接口格式：
# - 基础地址：https://api.deepseek.com/v1
# - 推荐模型：deepseek-chat（V3版本），deepseek-reasoner（R1版本）

---

```python
import json
```
# 导入json库，用于JSON数据的序列化与反序列化

```python
import logging
```
# 导入logging日志库，用于记录运行日志

```python
from typing import Dict, Any, List, Optional, Callable
```
# 从typing类型注解库中导入：字典类型、任意类型、列表类型、可选类型、可调用类型

---

```python
logger = logging.getLogger(__name__)
```
# 获取当前模块名称的日志记录器实例

---

```python
class DeepSeekClient:
```
# 定义深度求索客户端类

```python
    """DeepSeek API 客户端"""
```
#     类文档字符串：深度求索API客户端

```python
    DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
```
#     类属性：默认基础地址，指向深度求索API的v1版本端点

```python
    DEFAULT_MODEL = "deepseek-chat"
```
#     类属性：默认模型名称，使用deepseek-chat对话模型

```python
    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = None,
    ):
```
#     定义初始化方法（构造函数），接收自身引用、接口密钥字符串（默认为空）、基础地址字符串（默认为空）、模型名称字符串（默认为空）

```python
        self.api_key = api_key or ""
```
#         实例属性：接口密钥，若未提供则使用空字符串

```python
        self.base_url = base_url or self.DEFAULT_BASE_URL
```
#         实例属性：基础请求地址，若未提供则使用默认基础地址

```python
        self.model = model or self.DEFAULT_MODEL
```
#         实例属性：使用的模型名称，若未提供则使用默认模型

---

```python
    def chat_sync(
        self,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> Dict:
```
#     定义同步聊天方法（接收自身引用、消息字典列表、可选的工具字典列表、温度浮点数默认0.7、最大令牌数整数默认4096，返回字典）

```python
        """同步调用 Chat API"""
```
#         方法文档字符串：同步调用聊天API

```python
        import urllib.request
```
#         导入urllib请求库，用于发送HTTP请求

```python
        import urllib.error
```
#         导入urllib错误库，用于处理HTTP错误

```python
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
```
#         构建请求头字典：内容类型为JSON格式，授权字段使用Bearer令牌加接口密钥

```python
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
```
#         构建请求体字典：包含模型名称、消息列表、温度参数、最大令牌数

```python
        if tools:
```
#         如果传入了工具列表

```python
            body["tools"] = tools
```
#             将工具列表添加到请求体中

```python
            body["tool_choice"] = "auto"
```
#             设置工具选择模式为自动

```python
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
```
#         构建HTTP请求对象：请求地址为基础地址拼接聊天补全路径，请求体为JSON编码的UTF-8字节，设置请求头，使用POST方法

```python
        try:
```
#         开始异常处理块

```python
            with urllib.request.urlopen(req, timeout=120) as resp:
```
#             发送HTTP请求并获取响应，超时时间设为120秒，使用上下文管理器

```python
                return json.loads(resp.read().decode("utf-8"))
```
#                 读取响应内容并解码为UTF-8字符串，解析JSON后返回字典

```python
        except urllib.error.HTTPError as e:
```
#         捕获HTTP错误异常，赋值给变量e

```python
            error_body = e.read().decode("utf-8") if e.fp else ""
```
#             若错误响应存在文件指针则读取并解码错误体，否则为空字符串

```python
            logger.error(f"DeepSeek API HTTP {e.code}: {error_body}")
```
#             记录错误日志：深度求索API的HTTP状态码及错误体内容

```python
            raise RuntimeError(f"API 请求失败 ({e.code}): {error_body[:200]}")
```
#             抛出运行时错误：API请求失败，附带状态码和截取前200字符的错误信息

```python
        except Exception as e:
```
#         捕获其他所有异常，赋值给变量e

```python
            logger.error(f"DeepSeek API error: {e}")
```
#             记录错误日志：深度求索API发生异常及异常信息

```python
            raise RuntimeError(f"API 连接失败: {e}")
```
#             抛出运行时错误：API连接失败，附带异常信息

---

```python
    def chat_sync_stream(
        self,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        on_chunk: Callable[[str], None] = None,
    ) -> str:
```
#     定义同步流式聊天方法（接收自身引用、消息字典列表、可选的工具字典列表、温度浮点数默认0.7、可选的分块回调函数接收字符串返回空，返回字符串）

```python
        """同步流式调用（通过 SSE 模拟）"""
```
#         方法文档字符串：同步流式调用（通过服务器发送事件SSE模拟）

```python
        import urllib.request
```
#         导入urllib请求库，用于发送HTTP请求

```python
        import urllib.error
```
#         导入urllib错误库，用于处理HTTP错误

```python
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
```
#         构建请求头字典：内容类型为JSON格式，授权字段使用Bearer令牌加接口密钥

```python
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
```
#         构建请求体字典：包含模型名称、消息列表、温度参数，并启用流式传输

```python
        if tools:
```
#         如果传入了工具列表

```python
            body["tools"] = tools
```
#             将工具列表添加到请求体中

```python
            body["tool_choice"] = "auto"
```
#             设置工具选择模式为自动

```python
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
```
#         构建HTTP请求对象：请求地址为基础地址拼接聊天补全路径，请求体为JSON编码的UTF-8字节，设置请求头，使用POST方法

```python
        full_text = ""
```
#         初始化完整文本变量为空字符串，用于累积所有流式片段

```python
        try:
```
#         开始异常处理块

```python
            with urllib.request.urlopen(req, timeout=120) as resp:
```
#             发送HTTP请求并获取流式响应，超时时间设为120秒，使用上下文管理器

```python
                for line in resp:
```
#                     逐行遍历响应内容

```python
                    line = line.decode("utf-8").strip()
```
#                     将每行字节解码为UTF-8字符串并去除首尾空白

```python
                    if line.startswith("data: "):
```
#                     如果行以"data: "开头（SSE数据格式）

```python
                        data = line[6:]
```
#                         提取"data: "之后的数据部分

```python
                        if data == "[DONE]":
```
#                         如果数据为"[DONE]"，表示流式传输结束

```python
                            break
```
#                             跳出循环，停止读取

```python
                        try:
```
#                         开始内层异常处理块

```python
                            chunk = json.loads(data)
```
#                             将数据片段解析为JSON字典

```python
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
```
#                             从JSON中提取增量内容：获取choices列表第一个元素的delta字段

```python
                            if "content" in delta and delta["content"]:
```
#                             如果增量中包含content字段且内容非空

```python
                                text = delta["content"]
```
#                                 提取文本内容

```python
                                full_text += text
```
#                                 将文本追加到完整文本变量中

```python
                                if on_chunk:
```
#                                 如果提供了分块回调函数

```python
                                    on_chunk(text)
```
#                                     调用回调函数，传入当前文本片段

```python
                        except json.JSONDecodeError:
```
#                         捕获JSON解码错误异常

```python
                            continue
```
#                             跳过当前片段，继续处理下一行

```python
        except urllib.error.HTTPError as e:
```
#         捕获HTTP错误异常，赋值给变量e

```python
            error_body = e.read().decode("utf-8") if e.fp else ""
```
#             若错误响应存在文件指针则读取并解码错误体，否则为空字符串

```python
            raise RuntimeError(f"API 流式请求失败 ({e.code}): {error_body[:200]}")
```
#             抛出运行时错误：API流式请求失败，附带状态码和截取前200字符的错误信息

```python
        except Exception as e:
```
#         捕获其他所有异常，赋值给变量e

```python
            raise RuntimeError(f"API 连接失败: {e}")
```
#             抛出运行时错误：API连接失败，附带异常信息

---

```python
        return full_text
```
#         返回累积的完整文本字符串

---

```python
# ── 海报生成工具（纯 Python，不依赖 MCP） ──────────────
```
# 分隔注释：海报生成工具（纯Python实现，不依赖模型上下文协议MCP）

---

```python
POSTER_TEMPLATES = {
```
# 定义海报模板字典常量

```python
    "social_media": {
```
#     社交媒体模板键

```python
        "name": "社交媒体海报", "description": "适合 Instagram/微博 的方形海报",
```
#         模板名称为社交媒体海报，描述为适合Instagram/微博的方形海报

```python
        "width": 1080, "height": 1080, "layout": "centered",
```
#         宽度1080像素，高度1080像素，布局为居中

```python
    },
```
#     社交媒体模板定义结束

```python
    "event_banner": {
```
#     活动横幅模板键

```python
        "name": "活动横幅海报", "description": "适合活动宣传、横幅广告",
```
#         模板名称为活动横幅海报，描述为适合活动宣传、横幅广告

```python
        "width": 1920, "height": 1080, "layout": "banner",
```
#         宽度1920像素，高度1080像素，布局为横幅

```python
    },
```
#     活动横幅模板定义结束

```python
    "product_showcase": {
```
#     产品展示模板键

```python
        "name": "产品展示海报", "description": "适合电商产品展示",
```
#         模板名称为产品展示海报，描述为适合电商产品展示

```python
        "width": 1200, "height": 1600, "layout": "vertical",
```
#         宽度1200像素，高度1600像素，布局为竖版

```python
    },
```
#     产品展示模板定义结束

```python
    "minimalist": {
```
#     极简模板键

```python
        "name": "极简海报", "description": "简约现代风格",
```
#         模板名称为极简海报，描述为简约现代风格

```python
        "width": 1200, "height": 800, "layout": "minimal",
```
#         宽度1200像素，高度800像素，布局为极简

```python
    },
```
#     极简模板定义结束

```python
    "promotion": {
```
#     促销模板键

```python
        "name": "促销海报", "description": "适合促销活动、限时优惠",
```
#         模板名称为促销海报，描述为适合促销活动、限时优惠

```python
        "width": 1200, "height": 900, "layout": "promo",
```
#         宽度1200像素，高度900像素，布局为促销

```python
    },
```
#     促销模板定义结束

```python
    "poster_a4": {
```
#     A4竖版模板键

```python
        "name": "A4 竖版海报", "description": "标准A4尺寸，适合打印",
```
#         模板名称为A4竖版海报，描述为标准A4尺寸，适合打印

```python
        "width": 2480, "height": 3508, "layout": "portrait",
```
#         宽度2480像素，高度3508像素，布局为竖版

```python
    },
```
#     A4竖版模板定义结束

```python
}
```
# 海报模板字典定义结束

---

```python
COLOR_SCHEMES = {
```
# 定义颜色方案字典常量

```python
    "modern_blue": {
```
#     现代蓝配色键

```python
        "name": "现代蓝",
```
#         配色名称为现代蓝

```python
        "primary": "#2563EB", "secondary": "#3B82F6", "accent": "#F59E0B",
```
#         主色为深蓝色，副色为中蓝色，强调色为琥珀色

```python
        "bg": "#F0F4FF", "text": "#1E3A5F", "light": "#DBEAFE", "dark": "#1E40AF",
```
#         背景色为浅蓝灰，文字色为深蓝，浅色为淡蓝，深色为藏蓝

```python
    },
```
#     现代蓝配色定义结束

```python
    "warm_sunset": {
```
#     暖橙日落配色键

```python
        "name": "暖橙日落",
```
#         配色名称为暖橙日落

```python
        "primary": "#EA580C", "secondary": "#F97316", "accent": "#FCD34D",
```
#         主色为深橙色，副色为橙色，强调色为金黄色

```python
        "bg": "#FFF7ED", "text": "#431407", "light": "#FED7AA", "dark": "#9A3412",
```
#         背景色为暖白，文字色为深棕，浅色为浅橙，深色为棕红

```python
    },
```
#     暖橙日落配色定义结束

```python
    "elegant_dark": {
```
#     优雅暗黑配色键

```python
        "name": "优雅暗黑",
```
#         配色名称为优雅暗黑

```python
        "primary": "#1F2937", "secondary": "#374151", "accent": "#F59E0B",
```
#         主色为深灰，副色为中灰，强调色为琥珀色

```python
        "bg": "#111827", "text": "#F9FAFB", "light": "#4B5563", "dark": "#030712",
```
#         背景色为近黑，文字色为近白，浅色为灰蓝，深色为纯黑

```python
    },
```
#     优雅暗黑配色定义结束

```python
    "fresh_green": {
```
#     清新绿配色键

```python
        "name": "清新绿",
```
#         配色名称为清新绿

```python
        "primary": "#059669", "secondary": "#10B981", "accent": "#FBBF24",
```
#         主色为翠绿，副色为绿松石，强调色为金黄色

```python
        "bg": "#ECFDF5", "text": "#064E3B", "light": "#A7F3D0", "dark": "#065F46",
```
#         背景色为浅绿，文字色为深绿，浅色为薄荷绿，深色为墨绿

```python
    },
```
#     清新绿配色定义结束

```python
    "vibrant_purple": {
```
#     活力紫配色键

```python
        "name": "活力紫",
```
#         配色名称为活力紫

```python
        "primary": "#7C3AED", "secondary": "#8B5CF6", "accent": "#F472B6",
```
#         主色为紫色，副色为淡紫，强调色为粉色

```python
        "bg": "#F5F3FF", "text": "#2E1065", "light": "#DDD6FE", "dark": "#5B21B6",
```
#         背景色为淡紫白，文字色为深紫，浅色为薰衣草，深色为靛紫

```python
    },
```
#     活力紫配色定义结束

```python
    "corporate_red": {
```
#     企业红配色键

```python
        "name": "企业红",
```
#         配色名称为企业红

```python
        "primary": "#DC2626", "secondary": "#EF4444", "accent": "#FCD34D",
```
#         主色为红色，副色为浅红，强调色为金黄色

```python
        "bg": "#FEF2F2", "text": "#7F1D1D", "light": "#FECACA", "dark": "#991B1B",
```
#         背景色为浅红，文字色为暗红，浅色为粉红，深色为深红

```python
    },
```
#     企业红配色定义结束

```python
    "ocean_teal": {
```
#     海洋青配色键

```python
        "name": "海洋青",
```
#         配色名称为海洋青

```python
        "primary": "#0D9488", "secondary": "#14B8A6", "accent": "#F97316",
```
#         主色为青色，副色为浅青，强调色为橙色

```python
        "bg": "#F0FDFA", "text": "#134E4A", "light": "#99F6E4", "dark": "#115E59",
```
#         背景色为浅青白，文字色为深青，浅色为薄荷青，深色为墨青

```python
    },
```
#     海洋青配色定义结束

```python
    "rose_gold": {
```
#     玫瑰金配色键

```python
        "name": "玫瑰金",
```
#         配色名称为玫瑰金

```python
        "primary": "#BE185D", "secondary": "#EC4899", "accent": "#FCD34D",
```
#         主色为玫红，副色为粉色，强调色为金黄色

```python
        "bg": "#FFF1F2", "text": "#4C0519", "light": "#FBCFE8", "dark": "#831843",
```
#         背景色为浅粉白，文字色为暗玫红，浅色为淡粉，深色为深玫红

```python
    },
```
#     玫瑰金配色定义结束

```python
    "deepseek_blue": {
```
#     DeepSeek蓝配色键

```python
        "name": "DeepSeek 蓝",
```
#         配色名称为DeepSeek蓝

```python
        "primary": "#4D6BFE", "secondary": "#6B8AFF", "accent": "#00D4AA",
```
#         主色为亮蓝，副色为淡蓝，强调色为青绿

```python
        "bg": "#F5F7FF", "text": "#1A1A2E", "light": "#E0E7FF", "dark": "#3730A3",
```
#         背景色为浅蓝白，文字色为深蓝黑，浅色为淡靛蓝，深色为靛蓝

```python
    },
```
#     DeepSeek蓝配色定义结束

```python
}
```
# 颜色方案字典定义结束

---

```python
SYSTEM_PROMPT = """你是一个专业的 Illustrator 矢量设计 AI 助手，运行在桌面矢量图形编辑器中。
```
# 定义系统提示词常量字符串：你是一个专业的Illustrator矢量设计AI助手，运行在桌面矢量图形编辑器中

```python

## 核心能力
```
# 核心能力部分标题

```python

### 1. 矢量海报生成
```
# 第一项核心能力：矢量海报生成

```python
你可以一键生成专业矢量海报。当用户提到"海报"、"banner"、"宣传图"、"封面"、"促销图"等关键词时使用。
```
# 说明：你可以一键生成专业矢量海报，当用户提到海报、横幅、宣传图、封面、促销图等关键词时使用

```python

**可用海报模板：**
```
# 提示：可用海报模板列表

```python
- social_media (1080×1080): Instagram/微博方形海报
```
# 社交媒体模板：1080×1080像素，适合Instagram/微博方形海报

```python
- event_banner (1920×1080): 活动横幅广告
```
# 活动横幅模板：1920×1080像素，适合活动横幅广告

```python
- product_showcase (1200×1600): 产品展示竖版海报
```
# 产品展示模板：1200×1600像素，适合产品展示竖版海报

```python
- minimalist (1200×800): 极简现代风格海报
```
# 极简模板：1200×800像素，适合极简现代风格海报

```python
- promotion (1200×900): 促销优惠海报
```
# 促销模板：1200×900像素，适合促销优惠海报

```python
- poster_a4 (2480×3508): A4打印竖版海报
```
# A4竖版模板：2480×3508像素，适合A4打印竖版海报

```python

**可用颜色方案：**
```
# 提示：可用颜色方案列表

```python
- modern_blue: 现代蓝（科技/商务）
```
# 现代蓝配色：适合科技/商务场景

```python
- warm_sunset: 暖橙日落（活力/温暖）
```
# 暖橙日落配色：适合活力/温暖场景

```python
- elegant_dark: 优雅暗黑（高端/奢华）
```
# 优雅暗黑配色：适合高端/奢华场景

```python
- fresh_green: 清新绿（自然/健康）
```
# 清新绿配色：适合自然/健康场景

```python
- vibrant_purple: 活力紫（创意/时尚）
```
# 活力紫配色：适合创意/时尚场景

```python
- corporate_red: 企业红（促销/活动）
```
# 企业红配色：适合促销/活动场景

```python
- ocean_teal: 海洋青（清爽/专业）
```
# 海洋青配色：适合清爽/专业场景

```python
- rose_gold: 玫瑰金（女性/精致）
```
# 玫瑰金配色：适合女性/精致场景

```python
- deepseek_blue: DeepSeek蓝（AI/科技）
```
# DeepSeek蓝配色：适合AI/科技场景

```python

### 2. 矢量图形绘制
```
# 第二项核心能力：矢量图形绘制

```python
你可以在画布上绘制矢量图形：矩形、椭圆、文字、线条等。
```
# 说明：你可以在画布上绘制矢量图形，包括矩形、椭圆、文字、线条等

```python

### 3. 交互式问答
```
# 第三项核心能力：交互式问答

```python
当用户描述模糊时，主动追问关键信息：
```
# 说明：当用户描述模糊时，主动追问关键信息

```python
1. 海报用途/场景 → 选择合适的模板
```
# 第一点：了解海报用途/场景，以选择合适的模板

```python
2. 标题文字 → 主标题内容
```
# 第二点：获取标题文字，即主标题内容

```python
3. 风格偏好 → 选择合适的颜色方案
```
# 第三点：了解风格偏好，以选择合适的颜色方案

```python
4. 额外信息 → 副标题、描述、CTA按钮等
```
# 第四点：收集额外信息，包括副标题、描述、行动号召按钮等

```python

## 工具使用
```
# 工具使用部分标题

```python

**生成海报时：**
```
# 提示：生成海报时的操作说明

```python
调用 generate_poster 工具，参数包括 template, title, subtitle, description, color_scheme, cta_text, badge_text
```
# 说明：调用generate_poster生成海报工具，参数包括模板、标题、副标题、描述、颜色方案、行动号召文字、徽章文字

```python

**示例对话：**
```
# 提示：示例对话

```python
用户："帮我做个促销海报"
```
# 示例用户输入：帮我做个促销海报

```python
助手："好的！请告诉我：1. 促销内容？2. 折扣力度？3. 喜欢的颜色风格？4. 需要什么行动号召？"
```
# 示例助手回复：好的！请告诉我促销内容、折扣力度、喜欢的颜色风格、需要的行动号召

```python

用户："618大促，全场5折，红色风格，立即抢购"
```
# 示例用户输入：618大促，全场5折，红色风格，立即抢购

```python
助手：调用 generate_poster(template="promotion", title="618年中大促", subtitle="全场5折", color_scheme="corporate_red", cta_text="立即抢购")
```
# 示例助手操作：调用generate_poster工具，参数为促销模板、标题618年中大促、副标题全场5折、企业红配色、行动号召立即抢购

```python

**回复要求：**
```
# 提示：回复要求

```python
- 用中文回复
```
# 要求使用中文回复

```python
- 简洁清晰地说明操作结果
```
# 要求简洁清晰地说明操作结果

```python
- 描述生成的海报内容"""
```
# 要求描述生成的海报内容（系统提示词字符串结束）

---

```python
def build_tools_for_deepseek() -> List[Dict]:
```
# 定义构建深度求索工具函数（返回字典列表）

```python
    """构建 DeepSeek 可用的工具定义"""
```
#     函数文档字符串：构建深度求索可用的工具定义

```python
    return [{
```
#         返回一个包含单个工具定义的列表

```python
        "type": "function",
```
#             工具类型为函数

```python
        "function": {
```
#             函数定义对象开始

```python
            "name": "generate_poster",
```
#                 函数名称为生成海报

```python
            "description": "一键生成矢量海报。根据模板和参数自动完成背景、排版、装饰元素。支持6种模板和9种配色方案。",
```
#                 函数描述为一键生成矢量海报，根据模板和参数自动完成背景、排版、装饰元素，支持6种模板和9种配色方案

```python
            "parameters": {
```
#                 参数定义对象开始

```python
                "type": "object",
```
#                     参数类型为对象

```python
                "properties": {
```
#                     属性定义对象开始

```python
                    "template": {
```
#                         模板参数定义开始

```python
                        "type": "string",
```
#                             参数类型为字符串

```python
                        "description": "海报模板",
```
#                             参数描述为海报模板

```python
                        "enum": list(POSTER_TEMPLATES.keys()),
```
#                             枚举值为海报模板字典的所有键列表

```python
                    },
```
#                         模板参数定义结束

```python
                    "title": {
```
#                         标题参数定义开始

```python
                        "type": "string",
```
#                             参数类型为字符串

```python
                        "description": "主标题文字",
```
#                             参数描述为主标题文字

```python
                    },
```
#                         标题参数定义结束

```python
                    "subtitle": {
```
#                         副标题参数定义开始

```python
                        "type": "string",
```
#                             参数类型为字符串

```python
                        "description": "副标题/辅助文字",
```
#                             参数描述为副标题/辅助文字

```python
                    },
```
#                         副标题参数定义结束

```python
                    "description": {
```
#                         描述参数定义开始

```python
                        "type": "string",
```
#                             参数类型为字符串

```python
                        "description": "描述文字",
```
#                             参数描述为描述文字

```python
                    },
```
#                         描述参数定义结束

```python
                    "color_scheme": {
```
#                         颜色方案参数定义开始

```python
                        "type": "string",
```
#                             参数类型为字符串

```python
                        "description": "颜色方案",
```
#                             参数描述为颜色方案

```python
                        "enum": list(COLOR_SCHEMES.keys()),
```
#                             枚举值为颜色方案字典的所有键列表

```python
                    },
```
#                         颜色方案参数定义结束

```python
                    "cta_text": {
```
#                         行动号召文字参数定义开始

```python
                        "type": "string",
```
#                             参数类型为字符串

```python
                        "description": "行动号召按钮文字（如'立即抢购'）",
```
#                             参数描述为行动号召按钮文字（如立即抢购）

```python
                    },
```
#                         行动号召文字参数定义结束

```python
                    "badge_text": {
```
#                         徽章文字参数定义开始

```python
                        "type": "string",
```
#                             参数类型为字符串

```python
                        "description": "徽章/标签文字（如'NEW'、'限时'）",
```
#                             参数描述为徽章/标签文字（如NEW、限时）

```python
                    },
```
#                         徽章文字参数定义结束

```python
                },
```
#                     属性定义对象结束

```python
                "required": ["template", "title"],
```
#                     必填参数列表：模板和标题为必填

```python
            },
```
#                 参数定义对象结束

```python
        },
```
#             函数定义对象结束

```python
    }]
```
#         工具定义列表结束
