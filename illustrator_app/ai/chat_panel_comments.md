# chat_panel.py 中文注解翻译

---

```python
"""
```
# 模块文档字符串开始

```python
Illustrator AI 聊天面板 — DeepSeek 交互式对话 UI
```
# Illustrator AI 聊天面板 — DeepSeek 交互式对话用户界面

```python

```
# （空行）

```python
集成了 DeepSeek 大模型对话、海报生成工具调用、流式输出等功能。
```
# 集成了 DeepSeek 大模型对话、海报生成工具调用、流式输出等功能。

```python
用户可以在 Illustrator 中直接与 AI 对话，生成矢量海报。
```
# 用户可以在 Illustrator 中直接与 AI 对话，生成矢量海报。

```python
"""
```
# 模块文档字符串结束

---

```python
import json
```
# 导入 json（JavaScript 对象表示法）序列化/反序列化库

```python
import logging
```
# 导入 logging（日志记录）库

```python
import threading
```
# 导入 threading（线程）库，用于多线程编程

```python
from typing import Optional, List, Dict, Any
```
# 从 typing（类型注解）库导入：可选类型、列表类型、字典类型、任意类型

---

```python
from PyQt5.QtCore import (
```
# 从 PyQt5.QtCore（Qt核心模块）导入以下类：

```python
    Qt, QThread, pyqtSignal, QTimer, QSize, QDateTime, QUrl,
```
# Qt（Qt命名空间枚举）、QThread（线程类）、pyqtSignal（Qt信号）、QTimer（定时器）、QSize（尺寸）、QDateTime（日期时间）、QUrl（统一资源定位符）

```python
)
```
# 结束导入元组

```python
from PyQt5.QtGui import (
```
# 从 PyQt5.QtGui（Qt图形界面模块）导入以下类：

```python
    QColor, QFont, QTextCursor, QTextCharFormat, QDesktopServices,
```
# QColor（颜色）、QFont（字体）、QTextCursor（文本光标）、QTextCharFormat（文本字符格式）、QDesktopServices（桌面服务）

```python
    QIcon, QPixmap, QPainter,
```
# QIcon（图标）、QPixmap（像素图/图像）、QPainter（绘图器）

```python
)
```
# 结束导入元组

```python
from PyQt5.QtWidgets import (
```
# 从 PyQt5.QtWidgets（Qt控件模块）导入以下类：

```python
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
```
# QWidget（部件基类）、QVBoxLayout（垂直布局）、QHBoxLayout（水平布局）、QTextEdit（文本编辑器）、QLineEdit（单行文本输入框）

```python
    QPushButton, QLabel, QScrollArea, QFrame, QSplitter,
```
# QPushButton（按钮）、QLabel（标签）、QScrollArea（滚动区域）、QFrame（框架/边框容器）、QSplitter（分割器）

```python
    QComboBox, QCheckBox, QSizePolicy, QMessageBox, QApplication,
```
# QComboBox（下拉选择框）、QCheckBox（复选框）、QSizePolicy（尺寸策略）、QMessageBox（消息对话框）、QApplication（应用程序）

```python
    QGroupBox, QGridLayout, QProgressBar,
```
# QGroupBox（分组框）、QGridLayout（网格布局）、QProgressBar（进度条）

```python
)
```
# 结束导入元组

---

```python
from .deepseek_client import (
```
# 从当前包的 deepseek_client（DeepSeek客户端）模块导入以下内容：

```python
    DeepSeekClient, SYSTEM_PROMPT, build_tools_for_deepseek,
```
# DeepSeekClient（DeepSeek客户端类）、SYSTEM_PROMPT（系统提示词）、build_tools_for_deepseek（构建DeepSeek工具函数）

```python
    POSTER_TEMPLATES, COLOR_SCHEMES,
```
# POSTER_TEMPLATES（海报模板）、COLOR_SCHEMES（配色方案）

```python
)
```
# 结束导入元组

```python
from .poster_generator import PosterGenerator
```
# 从当前包的 poster_generator（海报生成器）模块导入 PosterGenerator（海报生成器类）

---

```python
logger = logging.getLogger(__name__)
```
# 创建一个以当前模块名命名的日志记录器实例

---

```python
class AIWorker(QThread):
```
# 定义 AI 工作线程类（继承自 Qt 线程类），用于在后台执行大语言模型调用

```python
    """AI 工作线程 — 在后台执行 LLM 调用"""
```
#     类文档字符串：AI 工作线程 — 在后台执行大语言模型调用

```python

```
# （空行）

```python
    response_chunk = pyqtSignal(str)          # 流式文字片段
```
#     定义流式文字片段信号（参数类型为字符串），用于逐块发送AI回复文本

```python
    response_done = pyqtSignal(dict)           # 完整回复
```
#     定义完整回复信号（参数类型为字典），用于发送AI完成的完整响应

```python
    response_error = pyqtSignal(str)           # 错误信息
```
#     定义错误信息信号（参数类型为字符串），用于发送调用过程中的错误

```python
    poster_ready = pyqtSignal(dict)            # 海报参数就绪
```
#     定义海报参数就绪信号（参数类型为字典），用于通知海报生成参数已准备好

```python

```
# （空行）

```python
    def __init__(self, client: DeepSeekClient, messages: List[Dict],
```
#     定义构造方法，接收 DeepSeek 客户端实例和消息列表（类型分别为 DeepSeekClient 和 List[Dict]）

```python
                 tools: List[Dict], parent=None):
```
#              以及工具列表（类型为 List[Dict]）和可选的父对象（默认为 None）

```python
        super().__init__(parent)
```
#         调用父类 QThread 的构造方法，传入父对象

```python
        self.client = client
```
#         将传入的客户端实例保存为实例属性 client（客户端）

```python
        self.messages = messages
```
#         将传入的消息列表保存为实例属性 messages（消息列表）

```python
        self.tools = tools
```
#         将传入的工具列表保存为实例属性 tools（工具列表）

```python

```
# （空行）

```python
    def run(self):
```
#     定义线程运行方法（线程启动时自动执行的主方法）

```python
        try:
```
#         开始 try 异常捕获块

```python
            response = self.client.chat_sync(
```
#             调用客户端的同步聊天方法 chat_sync，获取响应并赋值给 response（响应）

```python
                messages=self.messages,
```
#                 传入消息列表参数 messages（消息）

```python
                tools=self.tools,
```
#                 传入工具列表参数 tools（工具）

```python
                temperature=0.7,
```
#                 设置温度参数 temperature（温度）为 0.7，控制生成文本的随机性

```python
            )
```
#             结束 chat_sync 方法调用

```python

```
# （空行）

```python
            choice = response.get("choices", [{}])[0]
```
#             从响应中获取 choices（选项）列表的第一个选项，赋值给 choice（选项）

```python
            message = choice.get("message", {})
```
#             从选项中获取 message（消息）字典，赋值给 message（消息）

```python
            finish_reason = choice.get("finish_reason", "")
```
#             从选项中获取 finish_reason（结束原因）字符串，赋值给 finish_reason（结束原因）

```python

```
# （空行）

```python
            # 检查工具调用
```
#             检查是否存在工具调用

```python
            if finish_reason == "tool_calls" or message.get("tool_calls"):
```
#             如果结束原因为 "tool_calls"（工具调用）或消息中包含 tool_calls（工具调用）

```python
                tool_calls = message.get("tool_calls", [])
```
#                 从消息中获取 tool_calls（工具调用）列表，赋值给 tool_calls（工具调用列表）

```python
                # 发送文字内容
```
#                 发送文字内容

```python
                text_content = message.get("content", "")
```
#                 从消息中获取 content（文本内容），赋值给 text_content（文本内容）

```python
                if text_content:
```
#                 如果文本内容非空

```python
                    self.response_chunk.emit(text_content)
```
#                     发射流式文字片段信号，传递文本内容

```python

```
# （空行）

```python
                # 处理工具调用
```
#                 处理每一个工具调用

```python
                for tc in tool_calls:
```
#                 遍历工具调用列表，每次迭代取出一个工具调用 tc（工具调用）

```python
                    func = tc.get("function", {})
```
#                     从工具调用中获取 function（函数）字典，赋值给 func（函数）

```python
                    tool_name = func.get("name", "")
```
#                     从函数字典中获取 name（工具名称），赋值给 tool_name（工具名称）

```python
                    arguments = json.loads(func.get("arguments", "{}"))
```
#                     从函数字典中获取 arguments（参数）JSON字符串，解析为字典后赋值给 arguments（参数）

```python

```
# （空行）

```python
                    if tool_name == "generate_poster":
```
#                     如果工具名称为 "generate_poster"（生成海报）

```python
                        self.poster_ready.emit(arguments)
```
#                         发射海报参数就绪信号，传递海报参数

```python
                        self.response_chunk.emit(
```
#                         发射流式文字片段信号，拼接以下提示信息：

```python
                            f"\n\n✅ 已生成矢量海报！模板: {arguments.get('template', '?')}, "
```
#                             换行 + "已生成矢量海报！" + 模板名称（从参数中获取，默认为"?"）

```python
                            f"标题: {arguments.get('title', '?')}"
```
#                             + 标题名称（从参数中获取，默认为"?"）

```python
                        )
```
#                         结束发射信号调用

```python
                    else:
```
#                     否则（未知工具名称）

```python
                        self.response_chunk.emit(
```
#                         发射流式文字片段信号，拼接以下警告信息：

```python
                            f"\n\n⚠️ 未知工具: {tool_name}"
```
#                             换行 + "未知工具:" + 工具名称

```python
                        )
```
#                         结束发射信号调用

```python

```
# （空行）

```python
                self.response_done.emit({
```
#                 发射完整回复信号，传递包含以下内容的字典：

```python
                    "text": text_content,
```
#                     "text"（文本）：文本内容

```python
                    "tool_calls": [
```
#                     "tool_calls"（工具调用）：通过列表推导式构建工具调用列表

```python
                        {"name": tc["function"]["name"],
```
#                         每个元素包含 "name"（名称）：从工具调用的函数中获取名称

```python
                         "args": json.loads(tc["function"]["arguments"])}
```
#                         和 "args"（参数）：将函数参数JSON字符串解析为字典

```python
                        for tc in tool_calls
```
#                         遍历所有工具调用

```python
                    ],
```
#                     列表结束

```python
                })
```
#                 结束发射信号调用

```python
            else:
```
#             否则（纯文本回复，无工具调用）

```python
                # 纯文本回复
```
#                 处理纯文本回复

```python
                assistant_content = message.get("content", "")
```
#                 从消息中获取 content（助手回复内容），赋值给 assistant_content（助手回复内容）

```python
                self.response_chunk.emit(assistant_content)
```
#                 发射流式文字片段信号，传递助手回复内容

```python
                self.response_done.emit({
```
#                 发射完整回复信号，传递包含以下内容的字典：

```python
                    "text": assistant_content,
```
#                     "text"（文本）：助手回复内容

```python
                    "tool_calls": [],
```
#                     "tool_calls"（工具调用）：空列表（无工具调用）

```python
                })
```
#                 结束发射信号调用

```python

```
# （空行）

```python
        except Exception as e:
```
#         捕获所有异常，将异常实例赋值给 e（异常）

```python
            self.response_error.emit(str(e))
```
#             发射错误信息信号，传递异常的字符串表示

---

```python
class ChatBubble(QFrame):
```
# 定义聊天气泡类（继承自 Qt 框架容器类），用于显示单条聊天消息

```python
    """聊天气泡"""
```
#     类文档字符串：聊天气泡

```python

```
# （空行）

```python
    def __init__(self, text: str, is_user: bool = False, parent=None):
```
#     定义构造方法，接收文本内容（字符串类型）、是否为用户消息（布尔值，默认为 False）和可选的父对象

```python
        super().__init__(parent)
```
#         调用父类 QFrame 的构造方法，传入父对象

```python
        self._text = text
```
#         将传入的文本内容保存为私有属性 _text（文本）

```python
        self._is_user = is_user
```
#         将传入的用户标识保存为私有属性 _is_user（是否为用户消息）

```python
        self._init_ui()
```
#         调用界面初始化方法 _init_ui（初始化用户界面）

```python

```
# （空行）

```python
    def _init_ui(self):
```
#     定义私有界面初始化方法 _init_ui（初始化用户界面）

```python
        layout = QVBoxLayout(self)
```
#         创建一个垂直布局，以自身为父容器，赋值给 layout（布局）

```python
        layout.setContentsMargins(8, 4, 8, 4)
```
#         设置布局的内容边距为：左8、上4、右8、下4像素

```python

```
# （空行）

```python
        label = QLabel(self._text)
```
#         创建一个标签控件，显示文本内容，赋值给 label（标签）

```python
        label.setWordWrap(True)
```
#         启用标签的自动换行功能

```python
        label.setTextFormat(Qt.RichText)
```
#         设置标签的文本格式为富文本模式，支持HTML渲染

```python
        label.setOpenExternalLinks(True)
```
#         启用标签中外部链接的自动打开功能

```python
        # 启用文本选择和复制
```
#         启用文本选择和复制功能

```python
        label.setTextInteractionFlags(
```
#         设置标签的文本交互标志为：

```python
            Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard
```
#             支持鼠标选择文本 | 支持键盘选择文本

```python
        )
```
#         结束设置交互标志调用

```python
        label.setCursor(Qt.IBeamCursor)
```
#         设置标签的鼠标光标为文本编辑光标（I型光标）

```python

```
# （空行）

```python
        if self._is_user:
```
#         如果是用户消息

```python
            label.setStyleSheet("""
```
#             设置标签的样式表为：

```python
                QLabel {
```
#                 对 QLabel 控件设置以下样式：

```python
                    background-color: #0d6efd;
```
#                     背景色设为蓝色（#0d6efd）

```python
                    color: white;
```
#                     文字颜色设为白色

```python
                    border-radius: 12px;
```
#                     圆角半径设为12像素

```python
                    padding: 10px 14px;
```
#                     内边距设为上下10像素、左右14像素

```python
                    font-size: 13px;
```
#                     字体大小设为13像素

```python
                }
```
#                 样式块结束

```python
            """)
```
#             结束样式表字符串

```python
            layout.setAlignment(Qt.AlignRight)
```
#             设置布局对齐方式为右对齐

```python
        else:
```
#         否则（AI助手消息）

```python
            label.setStyleSheet("""
```
#             设置标签的样式表为：

```python
                QLabel {
```
#                 对 QLabel 控件设置以下样式：

```python
                    background-color: #3c3c3c;
```
#                     背景色设为深灰色（#3c3c3c）

```python
                    color: #ddd;
```
#                     文字颜色设为浅灰色（#ddd）

```python
                    border-radius: 12px;
```
#                     圆角半径设为12像素

```python
                    padding: 10px 14px;
```
#                     内边距设为上下10像素、左右14像素

```python
                    font-size: 13px;
```
#                     字体大小设为13像素

```python
                }
```
#                 样式块结束

```python
            """)
```
#             结束样式表字符串

```python
            layout.setAlignment(Qt.AlignLeft)
```
#             设置布局对齐方式为左对齐

```python

```
# （空行）

```python
        layout.addWidget(label)
```
#         将标签控件添加到布局中

---

```python
class ChatPanel(QWidget):
```
# 定义聊天面板类（继承自 Qt 部件基类），作为右侧停靠面板显示AI对话界面

```python
    """AI 聊天面板 — 右侧 Dock 面板"""
```
#     类文档字符串：AI 聊天面板 — 右侧 Dock 面板

```python

```
# （空行）

```python
    # 信号
```
#     信号定义区域

```python
    poster_generated = pyqtSignal(dict)   # 海报生成参数
```
#     定义海报生成信号（参数类型为字典），用于通知外部海报已生成并传递海报参数

```python

```
# （空行）

```python
    def __init__(self, parent=None):
```
#     定义构造方法，接收可选的父对象（默认为 None）

```python
        super().__init__(parent)
```
#         调用父类 QWidget 的构造方法，传入父对象

```python

```
# （空行）

```python
        # AI 客户端
```
#         初始化 AI 客户端相关属性

```python
        self._api_key = ""
```
#         初始化 API 密钥为空字符串

```python
        self._model = "deepseek-chat"
```
#         初始化模型名称为 "deepseek-chat"（DeepSeek聊天模型）

```python
        self._client: Optional[DeepSeekClient] = None
```
#         初始化 DeepSeek 客户端实例为 None（可选类型，可为空）

```python
        self._worker: Optional[AIWorker] = None
```
#         初始化 AI 工作线程实例为 None（可选类型，可为空）

```python
        self._conversation: List[Dict] = []
```
#         初始化对话历史列表为空列表

```python
        self._document = None  # Illustrator 文档引用
```
#         初始化 Illustrator 文档引用为 None（当前无关联文档）

```python

```
# （空行）

```python
        self._init_ui()
```
#         调用界面初始化方法 _init_ui（初始化用户界面）

```python
        self._reset_conversation()
```
#         调用对话重置方法 _reset_conversation（重置对话）

```python

```
# （空行）

```python
    def set_document(self, doc):
```
#     定义设置文档方法 set_document（设置文档），接收文档对象参数 doc（文档）

```python
        """设置关联的 Illustrator 文档"""
```
#         方法文档字符串：设置关联的 Illustrator 文档

```python
        self._document = doc
```
#         将传入的文档对象保存为私有属性 _document（文档）

```python

```
# （空行）

```python
    def set_api_key(self, key: str):
```
#     定义设置 API 密钥方法 set_api_key（设置API密钥），接收密钥字符串参数 key（密钥）

```python
        """设置 API Key"""
```
#         方法文档字符串：设置 API Key

```python
        self._api_key = key
```
#         将传入的密钥保存为私有属性 _api_key（API密钥）

```python
        self._client = DeepSeekClient(
```
#         创建 DeepSeek 客户端实例，传入以下参数：

```python
            api_key=key,
```
#             API 密钥为传入的 key（密钥）

```python
            model=self._model,
```
#             模型名称为当前模型 _model（模型）

```python
        )
```
#         结束客户端实例化

```python
        self._reset_conversation()
```
#         重置对话历史

```python

```
# （空行）

```python
    def set_model(self, model: str):
```
#     定义设置模型方法 set_model（设置模型），接收模型名称字符串参数 model（模型）

```python
        """设置模型"""
```
#         方法文档字符串：设置模型

```python
        self._model = model
```
#         将传入的模型名称保存为私有属性 _model（模型）

```python
        if self._api_key:
```
#         如果 API 密钥已设置（非空）

```python
            self._client = DeepSeekClient(
```
#             创建 DeepSeek 客户端实例，传入以下参数：

```python
                api_key=self._api_key,
```
#                 API 密钥为当前密钥 _api_key（API密钥）

```python
                model=model,
```
#                 模型名称为传入的 model（模型）

```python
            )
```
#             结束客户端实例化

```python
            self._reset_conversation()
```
#             重置对话历史

```python

```
# （空行）

```python
    def _reset_conversation(self):
```
#     定义私有对话重置方法 _reset_conversation（重置对话）

```python
        """重置对话"""
```
#         方法文档字符串：重置对话

```python
        self._conversation = [
```
#         将对话历史重新初始化为一个包含系统消息的列表：

```python
            {"role": "system", "content": SYSTEM_PROMPT}
```
#             系统消息字典：角色为 "system"（系统），内容为 SYSTEM_PROMPT（系统提示词）

```python
        ]
```
#         列表结束

```python

```
# （空行）

```python
    # ── UI 初始化 ──
```
#     ── UI 初始化部分 ──

```python

```
# （空行）

```python
    def _init_ui(self):
```
#     定义私有界面初始化方法 _init_ui（初始化用户界面）

```python
        layout = QVBoxLayout(self)
```
#         创建一个垂直布局，以自身为父容器，赋值给 layout（布局）

```python
        layout.setContentsMargins(4, 4, 4, 4)
```
#         设置布局的内容边距为：左4、上4、右4、下4像素

```python
        layout.setSpacing(4)
```
#         设置布局中各控件之间的间距为4像素

```python

```
# （空行）

```python
        # 标题栏
```
#         构建标题栏

```python
        title_layout = QHBoxLayout()
```
#         创建一个水平布局，赋值给 title_layout（标题布局）

```python
        title_label = QLabel("🤖 AI 助手")
```
#         创建一个标签控件，显示 "🤖 AI 助手"，赋值给 title_label（标题标签）

```python
        title_label.setStyleSheet("color: #ddd; font-weight: bold; font-size: 14px;")
```
#         设置标题标签的样式：浅灰色文字、粗体、14像素字号

```python
        title_layout.addWidget(title_label)
```
#         将标题标签添加到标题布局中

```python
        title_layout.addStretch()
```
#         在标题布局末尾添加弹性间距（将后续控件推到右侧）

```python

```
# （空行）

```python
        self._clear_btn = QPushButton("清空")
```
#         创建一个按钮控件，显示 "清空"，赋值给私有属性 _clear_btn（清空按钮）

```python
        self._clear_btn.setFixedSize(50, 24)
```
#         设置清空按钮的固定大小为宽50、高24像素

```python
        self._clear_btn.clicked.connect(self._on_clear)
```
#         将清空按钮的点击信号连接到 _on_clear（清空处理）方法

```python
        title_layout.addWidget(self._clear_btn)
```
#         将清空按钮添加到标题布局中

```python
        layout.addLayout(title_layout)
```
#         将标题布局添加到主垂直布局中

```python

```
# （空行）

```python
        # 模型选择
```
#         构建模型选择区域

```python
        config_layout = QHBoxLayout()
```
#         创建一个水平布局，赋值给 config_layout（配置布局）

```python
        config_layout.setSpacing(4)
```
#         设置配置布局中控件间距为4像素

```python

```
# （空行）

```python
        self._model_combo = QComboBox()
```
#         创建一个下拉选择框控件，赋值给私有属性 _model_combo（模型选择框）

```python
        self._model_combo.addItems([
```
#         向模型选择框添加以下选项：

```python
            "deepseek-chat", "deepseek-reasoner",
```
#             "deepseek-chat"（DeepSeek聊天模型）和 "deepseek-reasoner"（DeepSeek推理模型）

```python
        ])
```
#         选项列表结束

```python
        self._model_combo.setCurrentText("deepseek-chat")
```
#         设置模型选择框的当前选项为 "deepseek-chat"

```python
        self._model_combo.currentTextChanged.connect(self.set_model)
```
#         将模型选择框的文本变化信号连接到 set_model（设置模型）方法

```python
        self._model_combo.setToolTip("选择 DeepSeek 模型")
```
#         设置模型选择框的工具提示为 "选择 DeepSeek 模型"

```python
        config_layout.addWidget(QLabel("模型:"))
```
#         向配置布局中添加一个 "模型:" 标签

```python
        config_layout.addWidget(self._model_combo, 1)
```
#         将模型选择框添加到配置布局中，拉伸因子为1（占据剩余空间）

```python

```
# （空行）

```python
        layout.addLayout(config_layout)
```
#         将配置布局添加到主垂直布局中

```python

```
# （空行）

```python
        # API Key 输入
```
#         构建 API 密钥输入区域

```python
        api_layout = QHBoxLayout()
```
#         创建一个水平布局，赋值给 api_layout（API布局）

```python
        api_layout.setSpacing(4)
```
#         设置 API 布局中控件间距为4像素

```python

```
# （空行）

```python
        self._api_input = QLineEdit()
```
#         创建一个单行文本输入框控件，赋值给私有属性 _api_input（API输入框）

```python
        self._api_input.setPlaceholderText("输入 DeepSeek API Key...")
```
#         设置 API 输入框的占位提示文字为 "输入 DeepSeek API Key..."

```python
        self._api_input.setEchoMode(QLineEdit.Password)
```
#         设置 API 输入框的回显模式为密码模式（输入内容显示为星号/圆点）

```python
        self._api_input.setToolTip("从 platform.deepseek.com 获取")
```
#         设置 API 输入框的工具提示为 "从 platform.deepseek.com 获取"

```python
        api_layout.addWidget(self._api_input, 1)
```
#         将 API 输入框添加到 API 布局中，拉伸因子为1

```python

```
# （空行）

```python
        self._connect_btn = QPushButton("连接")
```
#         创建一个按钮控件，显示 "连接"，赋值给私有属性 _connect_btn（连接按钮）

```python
        self._connect_btn.setFixedSize(50, 24)
```
#         设置连接按钮的固定大小为宽50、高24像素

```python
        self._connect_btn.clicked.connect(self._on_connect)
```
#         将连接按钮的点击信号连接到 _on_connect（连接处理）方法

```python
        api_layout.addWidget(self._connect_btn)
```
#         将连接按钮添加到 API 布局中

```python

```
# （空行）

```python
        layout.addLayout(api_layout)
```
#         将 API 布局添加到主垂直布局中

```python

```
# （空行）

```python
        # 快捷提示
```
#         构建快捷提示按钮区域

```python
        quick_layout = QHBoxLayout()
```
#         创建一个水平布局，赋值给 quick_layout（快捷布局）

```python
        quick_layout.setSpacing(4)
```
#         设置快捷布局中控件间距为4像素

```python
        quick_label = QLabel("快捷:")
```
#         创建一个标签控件，显示 "快捷:"，赋值给 quick_label（快捷标签）

```python
        quick_label.setStyleSheet("color: #888; font-size: 11px;")
```
#         设置快捷标签的样式：灰色文字、11像素字号

```python
        quick_layout.addWidget(quick_label)
```
#         将快捷标签添加到快捷布局中

```python

```
# （空行）

```python
        for text, prompt in [
```
#         遍历以下快捷提示按钮配置列表，每次取出按钮显示文本 text（文本）和对应提示词 prompt（提示词）：

```python
            ("🔥促销", "帮我做一个618促销海报，全场5折，红色风格"),
```
#             （"🔥促销"，"帮我做一个618促销海报，全场5折，红色风格"）

```python
            ("📱社交", "做一个社交媒体宣传海报，新产品发布"),
```
#             （"📱社交"，"做一个社交媒体宣传海报，新产品发布"）

```python
            ("✨极简", "做一个极简风格的品牌宣传海报"),
```
#             （"✨极简"，"做一个极简风格的品牌宣传海报"）

```python
        ]:
```
#         列表结束

```python
            btn = QPushButton(text)
```
#             创建一个按钮控件，显示当前 text（文本），赋值给 btn（按钮）

```python
            btn.setFixedHeight(22)
```
#             设置按钮的固定高度为22像素

```python
            btn.setStyleSheet("""
```
#             设置按钮的样式表为：

```python
                QPushButton {
```
#                 对 QPushButton 控件设置以下样式：

```python
                    background-color: #4a4a4a; color: #ddd;
```
#                     背景色设为深灰色（#4a4a4a），文字颜色设为浅灰色（#ddd）

```python
                    border: 1px solid #555; border-radius: 3px;
```
#                     边框设为1像素深灰色（#555），圆角半径设为3像素

```python
                    padding: 2px 6px; font-size: 11px;
```
#                     内边距设为上下2像素、左右6像素，字体大小设为11像素

```python
                }
```
#                 正常状态样式块结束

```python
                QPushButton:hover { background-color: #5a5a5a; }
```
#                 鼠标悬停状态：背景色设为稍浅的深灰色（#5a5a5a）

```python
            """)
```
#             结束样式表字符串

```python
            btn.clicked.connect(lambda checked, p=prompt: self._send_message(p))
```
#             将按钮的点击信号连接到匿名函数：调用 _send_message（发送消息）方法并传入当前 prompt（提示词）

```python
            quick_layout.addWidget(btn)
```
#             将按钮添加到快捷布局中

```python

```
# （空行）

```python
        quick_layout.addStretch()
```
#         在快捷布局末尾添加弹性间距

```python
        layout.addLayout(quick_layout)
```
#         将快捷布局添加到主垂直布局中

```python

```
# （空行）

```python
        # 聊天区域
```
#         构建聊天消息显示区域

```python
        self._chat_scroll = QScrollArea()
```
#         创建一个滚动区域控件，赋值给私有属性 _chat_scroll（聊天滚动区域）

```python
        self._chat_scroll.setWidgetResizable(True)
```
#         设置滚动区域的子控件可随滚动区域大小自动调整

```python
        self._chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
```
#         设置水平滚动条策略为始终关闭（不显示水平滚动条）

```python

```
# （空行）

```python
        self._chat_container = QWidget()
```
#         创建一个部件容器，赋值给私有属性 _chat_container（聊天容器）

```python
        self._chat_layout = QVBoxLayout(self._chat_container)
```
#         创建一个垂直布局，以聊天容器为父容器，赋值给私有属性 _chat_layout（聊天布局）

```python
        self._chat_layout.setAlignment(Qt.AlignTop)
```
#         设置聊天布局的对齐方式为顶部对齐

```python
        self._chat_layout.setSpacing(4)
```
#         设置聊天布局中控件间距为4像素

```python
        self._chat_layout.addStretch()
```
#         在聊天布局末尾添加弹性间距（将消息推到顶部）

```python

```
# （空行）

```python
        self._chat_scroll.setWidget(self._chat_container)
```
#         将聊天容器设置为滚动区域的子控件

```python
        layout.addWidget(self._chat_scroll, 1)
```
#         将聊天滚动区域添加到主垂直布局中，拉伸因子为1（占据主要空间）

```python

```
# （空行）

```python
        # 进度条
```
#         构建进度条区域

```python
        self._progress = QProgressBar()
```
#         创建一个进度条控件，赋值给私有属性 _progress（进度条）

```python
        self._progress.setRange(0, 0)  # 不确定模式
```
#         设置进度条范围为0到0，启用不确定模式（显示滚动动画而不显示具体进度）

```python
        self._progress.setVisible(False)
```
#         设置进度条初始状态为不可见

```python
        self._progress.setFixedHeight(4)
```
#         设置进度条的固定高度为4像素

```python
        self._progress.setStyleSheet("""
```
#         设置进度条的样式表为：

```python
            QProgressBar { border: none; background: #2d2d2d; }
```
#             进度条无边框，背景色设为深灰色（#2d2d2d）

```python
            QProgressBar::chunk { background: #0d6efd; }
```
#             进度条填充块颜色设为蓝色（#0d6efd）

```python
        """)
```
#         结束样式表字符串

```python
        layout.addWidget(self._progress)
```
#         将进度条添加到主垂直布局中

```python

```
# （空行）

```python
        # 输入区域
```
#         构建消息输入区域

```python
        input_layout = QHBoxLayout()
```
#         创建一个水平布局，赋值给 input_layout（输入布局）

```python
        input_layout.setSpacing(4)
```
#         设置输入布局中控件间距为4像素

```python

```
# （空行）

```python
        self._input = QLineEdit()
```
#         创建一个单行文本输入框控件，赋值给私有属性 _input（输入框）

```python
        self._input.setPlaceholderText("描述你想要的海报... (Enter 发送)")
```
#         设置输入框的占位提示文字为 "描述你想要的海报... (Enter 发送)"

```python
        self._input.returnPressed.connect(self._on_send)
```
#         将输入框的回车键按下信号连接到 _on_send（发送处理）方法

```python
        input_layout.addWidget(self._input, 1)
```
#         将输入框添加到输入布局中，拉伸因子为1

```python

```
# （空行）

```python
        self._send_btn = QPushButton("发送")
```
#         创建一个按钮控件，显示 "发送"，赋值给私有属性 _send_btn（发送按钮）

```python
        self._send_btn.setFixedSize(50, 28)
```
#         设置发送按钮的固定大小为宽50、高28像素

```python
        self._send_btn.clicked.connect(self._on_send)
```
#         将发送按钮的点击信号连接到 _on_send（发送处理）方法

```python
        self._send_btn.setStyleSheet("""
```
#         设置发送按钮的样式表为：

```python
            QPushButton {
```
#             对 QPushButton 控件设置以下正常状态样式：

```python
                background-color: #0d6efd; color: white;
```
#                 背景色设为蓝色（#0d6efd），文字颜色设为白色

```python
                border: none; border-radius: 4px;
```
#                 无边框，圆角半径设为4像素

```python
                font-weight: bold;
```
#                 字体设为粗体

```python
            }
```
#             正常状态样式块结束

```python
            QPushButton:hover { background-color: #0b5ed7; }
```
#             鼠标悬停状态：背景色设为深蓝色（#0b5ed7）

```python
            QPushButton:disabled { background-color: #555; color: #888; }
```
#             禁用状态：背景色设为深灰色（#555），文字颜色设为灰色（#888）

```python
        """)
```
#         结束样式表字符串

```python
        input_layout.addWidget(self._send_btn)
```
#         将发送按钮添加到输入布局中

```python

```
# （空行）

```python
        layout.addLayout(input_layout)
```
#         将输入布局添加到主垂直布局中

```python

```
# （空行）

```python
        # 样式
```
#         设置面板整体样式

```python
        self.setStyleSheet("""
```
#         设置面板的样式表为：

```python
            QWidget {
```
#             对所有 QWidget 控件设置以下样式：

```python
                background-color: #2d2d2d;
```
#                 背景色设为深灰色（#2d2d2d）

```python
            }
```
#             样式块结束

```python
            QLabel {
```
#             对所有 QLabel 控件设置以下样式：

```python
                color: #bbb;
```
#                 文字颜色设为浅灰色（#bbb）

```python
                font-size: 12px;
```
#                 字体大小设为12像素

```python
            }
```
#             样式块结束

```python
            QLineEdit {
```
#             对所有 QLineEdit 控件设置以下样式：

```python
                background-color: #3c3c3c;
```
#                 背景色设为中灰色（#3c3c3c）

```python
                color: #ddd;
```
#                 文字颜色设为浅灰色（#ddd）

```python
                border: 1px solid #555;
```
#                 边框设为1像素深灰色（#555）

```python
                border-radius: 4px;
```
#                 圆角半径设为4像素

```python
                padding: 6px 10px;
```
#                 内边距设为上下6像素、左右10像素

```python
                font-size: 13px;
```
#                 字体大小设为13像素

```python
            }
```
#             样式块结束

```python
            QLineEdit:focus {
```
#             对 QLineEdit 的聚焦状态设置以下样式：

```python
                border-color: #0d6efd;
```
#                 边框颜色设为蓝色（#0d6efd）

```python
            }
```
#             样式块结束

```python
            QComboBox {
```
#             对所有 QComboBox 控件设置以下样式：

```python
                background-color: #3c3c3c;
```
#                 背景色设为中灰色（#3c3c3c）

```python
                color: #ddd;
```
#                 文字颜色设为浅灰色（#ddd）

```python
                border: 1px solid #555;
```
#                 边框设为1像素深灰色（#555）

```python
                border-radius: 3px;
```
#                 圆角半径设为3像素

```python
                padding: 2px 6px;
```
#                 内边距设为上下2像素、左右6像素

```python
                font-size: 12px;
```
#                 字体大小设为12像素

```python
            }
```
#             样式块结束

```python
            QComboBox:hover { border-color: #0d6efd; }
```
#             对 QComboBox 的鼠标悬停状态：边框颜色设为蓝色（#0d6efd）

```python
            QComboBox QAbstractItemView {
```
#             对 QComboBox 的下拉列表视图设置以下样式：

```python
                background-color: #3c3c3c;
```
#                 背景色设为中灰色（#3c3c3c）

```python
                color: #ddd;
```
#                 文字颜色设为浅灰色（#ddd）

```python
                selection-background-color: #0d6efd;
```
#                 选中项的背景色设为蓝色（#0d6efd）

```python
            }
```
#             样式块结束

```python
            QScrollArea {
```
#             对所有 QScrollArea 控件设置以下样式：

```python
                border: 1px solid #444;
```
#                 边框设为1像素深灰色（#444）

```python
                background-color: #252525;
```
#                 背景色设为更深的灰色（#252525）

```python
            }
```
#             样式块结束

```python
        """)
```
#         结束样式表字符串

```python

```
# （空行）

```python
        self.setMinimumWidth(280)
```
#         设置面板的最小宽度为280像素

```python

```
# （空行）

```python
    # ── 消息管理 ──
```
#     ── 消息管理部分 ──

```python

```
# （空行）

```python
    def _add_bubble(self, text: str, is_user: bool):
```
#     定义私有添加气泡方法 _add_bubble（添加气泡），接收文本内容 text（文本，字符串类型）和是否为用户消息 is_user（是否为用户，布尔类型）

```python
        """添加聊天气泡"""
```
#         方法文档字符串：添加聊天气泡

```python
        # 移除底部的 stretch（安全移除，确保最后一项确实是 spacer）
```
#         移除底部的弹性间距（安全移除，确保最后一项确实是间隔项）

```python
        if self._chat_layout.count() > 0:
```
#         如果聊天布局中有子项（数量大于0）

```python
            item = self._chat_layout.takeAt(self._chat_layout.count() - 1)
```
#             取出聊天布局中最后一个子项，赋值给 item（布局项）

```python
            if item.spacerItem():
```
#             如果取出的项是间隔项（spacer）

```python
                del item
```
#                 删除该间隔项

```python
            else:
```
#             否则（不是间隔项）

```python
                # 不是 spacer，放回去
```
#                 不是间隔项，将其放回布局

```python
                self._chat_layout.addItem(item)
```
#                 将布局项重新添加回聊天布局

```python

```
# （空行）

```python
        bubble = ChatBubble(text, is_user)
```
#         创建一个聊天气泡实例，传入文本和用户标识，赋值给 bubble（气泡）

```python
        self._chat_layout.addWidget(bubble)
```
#         将气泡控件添加到聊天布局中

```python

```
# （空行）

```python
        # 重新添加 stretch
```
#         重新添加弹性间距

```python
        self._chat_layout.addStretch()
```
#         在聊天布局末尾添加弹性间距（将后续消息推到顶部）

```python

```
# （空行）

```python
        # 滚动到底部
```
#         延迟50毫秒后滚动到底部

```python
        QTimer.singleShot(50, self._scroll_to_bottom)
```
#         使用定时器延迟50毫秒调用 _scroll_to_bottom（滚动到底部）方法

```python

```
# （空行）

```python
    def _scroll_to_bottom(self):
```
#     定义私有滚动到底部方法 _scroll_to_bottom（滚动到底部）

```python
        """滚动到底部"""
```
#         方法文档字符串：滚动到底部

```python
        scrollbar = self._chat_scroll.verticalScrollBar()
```
#         获取聊天滚动区域的垂直滚动条，赋值给 scrollbar（滚动条）

```python
        scrollbar.setValue(scrollbar.maximum())
```
#         将滚动条的值设置为最大值（滚动到最底部）

```python

```
# （空行）

```python
    def _add_system_message(self, text: str):
```
#     定义私有添加系统消息方法 _add_system_message（添加系统消息），接收文本内容 text（文本，字符串类型）

```python
        """添加系统消息"""
```
#         方法文档字符串：添加系统消息

```python
        if self._chat_layout.count() > 0:
```
#         如果聊天布局中有子项（数量大于0）

```python
            item = self._chat_layout.takeAt(self._chat_layout.count() - 1)
```
#             取出聊天布局中最后一个子项，赋值给 item（布局项）

```python
            if item.spacerItem():
```
#             如果取出的项是间隔项（spacer）

```python
                del item
```
#                 删除该间隔项

```python
            else:
```
#             否则（不是间隔项）

```python
                self._chat_layout.addItem(item)
```
#                 将布局项重新添加回聊天布局

```python

```
# （空行）

```python
        label = QLabel(text)
```
#         创建一个标签控件，显示系统消息文本，赋值给 label（标签）

```python
        label.setWordWrap(True)
```
#         启用标签的自动换行功能

```python
        label.setTextInteractionFlags(
```
#         设置标签的文本交互标志为：

```python
            Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard
```
#             支持鼠标选择文本 | 支持键盘选择文本

```python
        )
```
#         结束设置交互标志调用

```python
        label.setCursor(Qt.IBeamCursor)
```
#         设置标签的鼠标光标为文本编辑光标（I型光标）

```python
        label.setStyleSheet("""
```
#         设置标签的样式表为：

```python
            QLabel {
```
#             对 QLabel 控件设置以下样式：

```python
                color: #888;
```
#                 文字颜色设为灰色（#888）

```python
                font-size: 11px;
```
#                 字体大小设为11像素

```python
                padding: 4px 12px;
```
#                 内边距设为上下4像素、左右12像素

```python
            }
```
#             样式块结束

```python
        """)
```
#         结束样式表字符串

```python
        label.setAlignment(Qt.AlignCenter)
```
#         设置标签的对齐方式为居中对齐

```python
        self._chat_layout.addWidget(label)
```
#         将标签添加到聊天布局中

```python
        self._chat_layout.addStretch()
```
#         在聊天布局末尾添加弹性间距

```python
        QTimer.singleShot(50, self._scroll_to_bottom)
```
#         延迟50毫秒后调用 _scroll_to_bottom（滚动到底部）方法

```python

```
# （空行）

```python
    # ── 事件处理 ──
```
#     ── 事件处理部分 ──

```python

```
# （空行）

```python
    def _on_connect(self):
```
#     定义私有连接处理方法 _on_connect（连接处理），处理用户点击连接按钮的事件

```python
        """连接 API"""
```
#         方法文档字符串：连接 API

```python
        key = self._api_input.text().strip()
```
#         获取 API 输入框的文本内容并去除首尾空白，赋值给 key（密钥）

```python
        if not key:
```
#         如果密钥为空

```python
            QMessageBox.warning(self, "提示", "请输入 DeepSeek API Key")
```
#             弹出警告消息框，标题为 "提示"，内容为 "请输入 DeepSeek API Key"

```python
            return
```
#             提前返回，不执行后续操作

```python
        self.set_api_key(key)
```
#         调用 set_api_key（设置API密钥）方法，传入密钥

```python
        self._add_system_message("✅ 已连接到 DeepSeek API")
```
#         添加系统消息 "✅ 已连接到 DeepSeek API"

```python
        self._connect_btn.setText("已连接")
```
#         将连接按钮的文字更新为 "已连接"

```python
        self._connect_btn.setStyleSheet("""
```
#         设置连接按钮的样式表为：

```python
            QPushButton {
```
#             对 QPushButton 控件设置以下样式：

```python
                background-color: #198754; color: white;
```
#                 背景色设为绿色（#198754），文字颜色设为白色

```python
                border: none; border-radius: 3px;
```
#                 无边框，圆角半径设为3像素

```python
                font-size: 11px;
```
#                 字体大小设为11像素

```python
            }
```
#             样式块结束

```python
        """)
```
#         结束样式表字符串

```python

```
# （空行）

```python
    def _on_send(self):
```
#     定义私有发送处理方法 _on_send（发送处理），处理用户点击发送按钮或按下回车键的事件

```python
        """发送消息"""
```
#         方法文档字符串：发送消息

```python
        text = self._input.text().strip()
```
#         获取输入框的文本内容并去除首尾空白，赋值给 text（文本）

```python
        if not text:
```
#         如果文本为空

```python
            return
```
#             提前返回，不执行后续操作

```python

```
# （空行）

```python
        if not self._api_key:
```
#         如果 API 密钥未设置

```python
            QMessageBox.warning(self, "提示",
```
#             弹出警告消息框，标题为 "提示"：

```python
                              "请先输入 DeepSeek API Key 并点击「连接」")
```
#             内容为 "请先输入 DeepSeek API Key 并点击「连接」"

```python
            return
```
#             提前返回，不执行后续操作

```python

```
# （空行）

```python
        self._input.clear()
```
#         清空输入框的文本内容

```python
        self._send_message(text)
```
#         调用 _send_message（发送消息）方法，传入文本

```python

```
# （空行）

```python
    def _send_message(self, text: str):
```
#     定义私有发送消息方法 _send_message（发送消息），接收消息文本 text（文本，字符串类型）

```python
        """处理消息发送"""
```
#         方法文档字符串：处理消息发送

```python
        # 显示用户消息
```
#         显示用户消息气泡

```python
        self._add_bubble(text, is_user=True)
```
#         调用 _add_bubble（添加气泡）方法，传入文本并将 is_user（是否为用户）设为 True

```python

```
# （空行）

```python
        # 添加到对话历史
```
#         将用户消息添加到对话历史中

```python
        self._conversation.append({"role": "user", "content": text})
```
#         向对话历史列表末尾追加一条用户消息字典：角色为 "user"（用户），内容为文本

```python

```
# （空行）

```python
        # 显示加载状态
```
#         显示加载状态（禁用输入和发送按钮，显示进度条）

```python
        self._progress.setVisible(True)
```
#         将进度条设置为可见

```python
        self._send_btn.setEnabled(False)
```
#         禁用发送按钮

```python
        self._input.setEnabled(False)
```
#         禁用输入框

```python

```
# （空行）

```python
        # 创建 AI 响应气泡（稍后更新）
```
#         创建 AI 响应气泡（稍后通过流式更新内容）

```python
        if self._chat_layout.count() > 0:
```
#         如果聊天布局中有子项（数量大于0）

```python
            item = self._chat_layout.takeAt(self._chat_layout.count() - 1)
```
#             取出聊天布局中最后一个子项，赋值给 item（布局项）

```python
            if item.spacerItem():
```
#             如果取出的项是间隔项（spacer）

```python
                del item
```
#                 删除该间隔项

```python
            else:
```
#             否则（不是间隔项）

```python
                self._chat_layout.addItem(item)
```
#                 将布局项重新添加回聊天布局

```python

```
# （空行）

```python
        self._ai_response_label = QLabel("🤔 思考中...")
```
#         创建一个标签控件，显示 "🤔 思考中..."，赋值给私有属性 _ai_response_label（AI响应标签）

```python
        self._ai_response_label.setWordWrap(True)
```
#         启用 AI 响应标签的自动换行功能

```python
        self._ai_response_label.setTextFormat(Qt.RichText)
```
#         设置 AI 响应标签的文本格式为富文本模式

```python
        # 启用文本选择和复制
```
#         启用文本选择和复制功能

```python
        self._ai_response_label.setTextInteractionFlags(
```
#         设置 AI 响应标签的文本交互标志为：

```python
            Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard
```
#             支持鼠标选择文本 | 支持键盘选择文本

```python
        )
```
#         结束设置交互标志调用

```python
        self._ai_response_label.setCursor(Qt.IBeamCursor)
```
#         设置 AI 响应标签的鼠标光标为文本编辑光标（I型光标）

```python
        self._ai_response_label.setStyleSheet("""
```
#         设置 AI 响应标签的样式表为：

```python
            QLabel {
```
#             对 QLabel 控件设置以下样式：

```python
                background-color: #3c3c3c;
```
#                 背景色设为中灰色（#3c3c3c）

```python
                color: #ddd;
```
#                 文字颜色设为浅灰色（#ddd）

```python
                border-radius: 12px;
```
#                 圆角半径设为12像素

```python
                padding: 10px 14px;
```
#                 内边距设为上下10像素、左右14像素

```python
                font-size: 13px;
```
#                 字体大小设为13像素

```python
            }
```
#             样式块结束

```python
        """)
```
#         结束样式表字符串

```python
        ai_layout = QHBoxLayout()
```
#         创建一个水平布局，赋值给 ai_layout（AI布局）

```python
        ai_layout.addWidget(self._ai_response_label)
```
#         将 AI 响应标签添加到 AI 布局中

```python
        ai_layout.addStretch()
```
#         在 AI 布局末尾添加弹性间距（将AI响应推到左侧）

```python
        self._chat_layout.addLayout(ai_layout)
```
#         将 AI 布局添加到聊天布局中

```python
        self._chat_layout.addStretch()
```
#         在聊天布局末尾添加弹性间距

```python

```
# （空行）

```python
        # 构建工具定义
```
#         构建 DeepSeek 工具定义列表

```python
        tools = build_tools_for_deepseek()
```
#         调用 build_tools_for_deepseek（构建DeepSeek工具）函数，返回工具列表，赋值给 tools（工具）

```python

```
# （空行）

```python
        # 启动工作线程
```
#         创建并启动 AI 工作线程

```python
        self._worker = AIWorker(
```
#         创建 AI 工作线程实例，传入以下参数：

```python
            self._client, self._conversation, tools
```
#             DeepSeek 客户端、对话历史列表、工具列表

```python
        )
```
#         结束工作线程实例化

```python
        self._worker.response_chunk.connect(self._on_chunk)
```
#         将工作线程的流式文字片段信号连接到 _on_chunk（片段处理）方法

```python
        self._worker.response_done.connect(self._on_done)
```
#         将工作线程的完整回复信号连接到 _on_done（完成处理）方法

```python
        self._worker.response_error.connect(self._on_error)
```
#         将工作线程的错误信息信号连接到 _on_error（错误处理）方法

```python
        self._worker.poster_ready.connect(self._on_poster_ready)
```
#         将工作线程的海报参数就绪信号连接到 _on_poster_ready（海报就绪处理）方法

```python
        self._worker.start()
```
#         启动工作线程

```python

```
# （空行）

```python
    def _on_chunk(self, text: str):
```
#     定义私有片段处理方法 _on_chunk（片段处理），接收流式文本片段 text（文本，字符串类型）

```python
        """收到流式文字片段"""
```
#         方法文档字符串：收到流式文字片段

```python
        # 更新 AI 响应气泡
```
#         更新 AI 响应气泡的文本内容

```python
        current = self._ai_response_label.text()
```
#         获取 AI 响应标签当前文本，赋值给 current（当前文本）

```python
        if current == "🤔 思考中...":
```
#         如果当前文本是 "🤔 思考中..."（初始占位文本）

```python
            current = ""
```
#             将当前文本重置为空字符串

```python
        current += text
```
#         将新的文本片段追加到当前文本中

```python
        # 简单 Markdown 渲染
```
#         进行简单的 Markdown 格式渲染转换

```python
        current = current.replace("\n\n", "<br><br>").replace("\n", "<br>")
```
#         将双换行替换为两个 HTML 换行标签，将单换行替换为一个 HTML 换行标签

```python
        current = current.replace("**", "<b>").replace("</b><b>", "")
```
#         将双星号（加粗标记）替换为 HTML 粗体标签，并清理连续粗体标签

```python
        self._ai_response_label.setText(current)
```
#         将渲染后的文本设置到 AI 响应标签中

```python
        QTimer.singleShot(20, self._scroll_to_bottom)
```
#         延迟20毫秒后调用 _scroll_to_bottom（滚动到底部）方法

```python

```
# （空行）

```python
    def _on_poster_ready(self, params: Dict):
```
#     定义私有海报就绪处理方法 _on_poster_ready（海报就绪处理），接收海报参数 params（参数，字典类型）

```python
        """海报参数就绪 — 在文档中生成"""
```
#         方法文档字符串：海报参数就绪 — 在文档中生成

```python
        if self._document:
```
#         如果已关联 Illustrator 文档（文档不为 None）

```python
            generator = PosterGenerator(self._document)
```
#             创建海报生成器实例，传入文档对象，赋值给 generator（生成器）

```python
            result = generator.generate(params)
```
#             调用生成器的 generate（生成）方法，传入海报参数，将结果赋值给 result（结果）

```python
            self.poster_generated.emit(params)
```
#             发射海报生成信号，传递海报参数

```python

```
# （空行）

```python
    def _on_done(self, response: Dict):
```
#     定义私有完成处理方法 _on_done（完成处理），接收完整响应字典 response（响应，字典类型）

```python
        """AI 回复完成"""
```
#         方法文档字符串：AI 回复完成

```python
        self._progress.setVisible(False)
```
#         隐藏进度条

```python
        self._send_btn.setEnabled(True)
```
#         重新启用发送按钮

```python
        self._input.setEnabled(True)
```
#         重新启用输入框

```python

```
# （空行）

```python
        text = response.get("text", "")
```
#         从响应字典中获取 "text"（文本）字段，默认为空字符串，赋值给 text（文本）

```python

```
# （空行）

```python
        # 格式化最终回复
```
#         格式化最终回复文本

```python
        formatted = text.replace("\n\n", "<br><br>").replace("\n", "<br>")
```
#         将双换行替换为两个 HTML 换行标签，将单换行替换为一个 HTML 换行标签

```python
        formatted = formatted.replace("**", "<b>").replace("</b><b>", "")
```
#         将双星号（加粗标记）替换为 HTML 粗体标签，并清理连续粗体标签

```python
        if formatted:
```
#         如果格式化后的文本非空

```python
            self._ai_response_label.setText(formatted)
```
#             将格式化后的文本设置到 AI 响应标签中

```python
        else:
```
#         否则（格式化后文本为空）

```python
            self._ai_response_label.setText("操作已完成。")
```
#             将 AI 响应标签文本设置为 "操作已完成。"

```python

```
# （空行）

```python
        # 添加到对话历史
```
#         将 AI 回复添加到对话历史中

```python
        self._conversation.append({
```
#         向对话历史列表末尾追加一条助手消息字典：

```python
            "role": "assistant",
```
#             角色为 "assistant"（助手）

```python
            "content": text,
```
#             内容为 AI 回复的原始文本

```python
        })
```
#         字典和列表追加结束

```python

```
# （空行）

```python
        self._input.setFocus()
```
#         将输入焦点设置回输入框

```python

```
# （空行）

```python
    def _on_error(self, error: str):
```
#     定义私有错误处理方法 _on_error（错误处理），接收错误信息 error（错误，字符串类型）

```python
        """AI 调用出错"""
```
#         方法文档字符串：AI 调用出错

```python
        self._progress.setVisible(False)
```
#         隐藏进度条

```python
        self._send_btn.setEnabled(True)
```
#         重新启用发送按钮

```python
        self._input.setEnabled(True)
```
#         重新启用输入框

```python

```
# （空行）

```python
        self._ai_response_label.setText(
```
#         将错误提示信息设置到 AI 响应标签中：

```python
            f"❌ 出错了: {error}<br><br>请检查 API Key 是否正确，或稍后重试。"
```
#             "❌ 出错了:" + 错误信息 + "请检查 API Key 是否正确，或稍后重试。"（含HTML换行）

```python
        )
```
#         结束设置文本调用

```python
        self._ai_response_label.setStyleSheet("""
```
#         设置 AI 响应标签的错误样式表为：

```python
            QLabel {
```
#             对 QLabel 控件设置以下样式：

```python
                background-color: #5c1a1a;
```
#                 背景色设为深红色（#5c1a1a）

```python
                color: #f88;
```
#                 文字颜色设为浅红色（#f88）

```python
                border-radius: 12px;
```
#                 圆角半径设为12像素

```python
                padding: 10px 14px;
```
#                 内边距设为上下10像素、左右14像素

```python
                font-size: 13px;
```
#                 字体大小设为13像素

```python
            }
```
#             样式块结束

```python
        """)
```
#         结束样式表字符串

```python

```
# （空行）

```python
        logger.error(f"AI error: {error}")
```
#         使用日志记录器记录错误信息："AI error:" + 错误信息

```python

```
# （空行）

```python
    def _on_clear(self):
```
#     定义私有清空处理方法 _on_clear（清空处理），处理用户点击清空按钮的事件

```python
        """清空对话"""
```
#         方法文档字符串：清空对话

```python
        self._reset_conversation()
```
#         调用 _reset_conversation（重置对话）方法，重置对话历史

```python

```
# （空行）

```python
        # 清空聊天区域 - 安全的清理方式
```
#         清空聊天区域 — 采用安全的清理方式

```python
        while self._chat_layout.count() > 0:
```
#         当聊天布局中还有子项时（循环执行直到清空）

```python
            item = self._chat_layout.takeAt(0)
```
#             取出聊天布局中第一个子项，赋值给 item（布局项）

```python
            if item.widget():
```
#             如果取出的项是控件（widget）

```python
                widget = item.widget()
```
#                 获取该控件实例，赋值给 widget（控件）

```python
                widget.setParent(None)  # 先解除父子关系
```
#                 解除控件与父容器之间的父子关系（防止删除时引发异常）

```python
                widget.deleteLater()
```
#                 延迟删除控件（在事件循环空闲时安全销毁）

```python
            elif item.layout():
```
#             否则如果取出的项是子布局（layout）

```python
                self._clear_layout(item.layout())
```
#                 递归调用 _clear_layout（清空布局）方法，清空该子布局

```python
            # spacerItem 不需要特殊处理
```
#             间隔项（spacerItem）不需要特殊处理，自动丢弃

```python

```
# （空行）

```python
        self._chat_layout.addStretch()
```
#         在聊天布局末尾添加弹性间距

```python

```
# （空行）

```python
        self._add_system_message("对话已清空，可以开始新的对话。")
```
#         添加系统消息 "对话已清空，可以开始新的对话。"

```python

```
# （空行）

```python

```
# （空行）

```python
    def _clear_layout(self, layout):
```
#     定义私有清空布局方法 _clear_layout（清空布局），接收布局对象 layout（布局），递归清空布局中的所有子项

```python
        """递归清空布局"""
```
#         方法文档字符串：递归清空布局

```python
        while layout.count():
```
#         当布局中还有子项时（循环执行直到清空）

```python
            item = layout.takeAt(0)
```
#             取出布局中第一个子项，赋值给 item（布局项）

```python
            if item.widget():
```
#             如果取出的项是控件（widget）

```python
                widget = item.widget()
```
#                 获取该控件实例，赋值给 widget（控件）

```python
                widget.setParent(None)
```
#                 解除控件与父容器之间的父子关系

```python
                widget.deleteLater()
```
#                 延迟删除控件

```python
            elif item.layout():
```
#             否则如果取出的项是子布局（layout）

```python
                self._clear_layout(item.layout())
```
#                 递归调用 _clear_layout（清空布局）方法，清空该子布局
