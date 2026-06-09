"""
Illustrator AI 聊天面板 — DeepSeek 交互式对话 UI

集成了 DeepSeek 大模型对话、海报生成工具调用、流式输出等功能。
用户可以在 Illustrator 中直接与 AI 对话，生成矢量海报。
"""

import json
import logging
import threading
from typing import Optional, List, Dict, Any

from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QSize, QDateTime, QUrl,
)
from PyQt5.QtGui import (
    QColor, QFont, QTextCursor, QTextCharFormat, QDesktopServices,
    QIcon, QPixmap, QPainter,
)
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QLabel, QScrollArea, QFrame, QSplitter,
    QComboBox, QCheckBox, QSizePolicy, QMessageBox, QApplication,
    QGroupBox, QGridLayout, QProgressBar, QAbstractScrollArea,
)

from .deepseek_client import (
    DeepSeekClient, SYSTEM_PROMPT, build_tools_for_deepseek,
    POSTER_TEMPLATES, COLOR_SCHEMES,
)
from .poster_generator import PosterGenerator
# 创建一个以当前模块命名的日志记录器实例
logger = logging.getLogger(__name__)


class AIWorker(QThread):
    """AI 工作线程 — 在后台执行 LLM 调用"""

    response_chunk = pyqtSignal(str)          # 流式文字片段，用于逐块发送AI回复文本
    response_done = pyqtSignal(dict)           # 完整回复
    response_error = pyqtSignal(str)           # 错误信息
    poster_ready = pyqtSignal(dict)            # 海报参数就绪

    def __init__(self, client: DeepSeekClient, messages: List[Dict],
                 tools: List[Dict], parent=None):
        # 接收客户端实例和消息列表，工具列表，可选的父对象
        super().__init__(parent)
        self.client = client
        self.messages = messages
        self.tools = tools

    def run(self):
        # 定义线程运行方法
        try:
            response = self.client.chat_sync(
                messages=self.messages,
                tools=self.tools,
                temperature=0.7,
            )
            # 从响应中获取选择，消息，结束原因
            choice = response.get("choices", [{}])[0]
            message = choice.get("message", {})
            finish_reason = choice.get("finish_reason", "")

            # 检查工具调用
            if finish_reason == "tool_calls" or message.get("tool_calls"):
                # 获取工具调用
                tool_calls = message.get("tool_calls", [])
                # 发送文字内容
                text_content = message.get("content", "")
                if text_content:
                    # 如果不为空，发射流失文字片段信号，传递文本内容
                    self.response_chunk.emit(text_content)

                # 处理工具调用；遍历工具调用列表，每次迭代取出一个工具调用
                for tc in tool_calls:
                    func = tc.get("function", {})
                    tool_name = func.get("name", "")
                    arguments = json.loads(func.get("arguments", "{}"))

                    if tool_name == "generate_poster":
                        self.poster_ready.emit(arguments)
                        self.response_chunk.emit(
                            f"\n\n✅ 已生成矢量海报！模板: {arguments.get('template', '?')}, "
                            f"标题: {arguments.get('title', '?')}"
                        )
                    else:
                        self.response_chunk.emit(
                            f"\n\n⚠️ 未知工具: {tool_name}"
                        )
                # 发射完整回复信号，传递包含以下内容的字典；文本内容，工具调用：通过列表推导式构建工具调用列表
                self.response_done.emit({
                    "text": text_content,
                    "tool_calls": [
                        {"name": tc["function"]["name"],
                         "args": json.loads(tc["function"]["arguments"])}
                        for tc in tool_calls
                    ],
                })
            else:
                # 纯文本回复；发射流式文本片段信号，传递助手回复内容；从消息中获取content属性，赋值给ai助手回复内容
                assistant_content = message.get("content", "")
                self.response_chunk.emit(assistant_content)
                self.response_done.emit({
                    "text": assistant_content,
                    "tool_calls": [],
                })

        except Exception as e:
            self.response_error.emit(str(e))


class CopyableLabel(QLabel):
    """支持 Ctrl+C 复制的 QLabel 子类"""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        # 启用文本选择
        self.setTextInteractionFlags(
            Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard
        )
        self.setCursor(Qt.IBeamCursor)

    def keyPressEvent(self, event):
        """处理键盘事件，支持 Ctrl+C 复制"""
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_C:
            # 获取选中的文本并复制到剪贴板
            selected_text = self.selectedText()
            if selected_text:
                clipboard = QApplication.clipboard()
                clipboard.setText(selected_text)
                return  # 事件已处理，不再传递给父类
        super().keyPressEvent(event)

    def mouseDoubleClickEvent(self, event):
        """双击选中单词后，确保可以复制"""
        super().mouseDoubleClickEvent(event)


class ChatBubble(QFrame):
    """聊天气泡"""

    def __init__(self, text: str, is_user: bool = False, parent=None):
        super().__init__(parent)
        self._text = text
        self._is_user = is_user
        self._init_ui()

    def _init_ui(self):
        # 创建一个垂直布局，以自身为父容器，赋值给layout(布局)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        # 使用支持 Ctrl+C 复制的自定义 QLabel
        label = CopyableLabel(self._text)
        label.setWordWrap(True)
        label.setTextFormat(Qt.RichText)
        label.setOpenExternalLinks(True)

        if self._is_user:
            label.setStyleSheet("""
                QLabel {
                    background-color: #0d6efd;
                    color: white;
                    border-radius: 12px;
                    padding: 10px 14px;
                    font-size: 13px;
                }
            """)
            # 设置布局对齐方式为右对齐；
            layout.setAlignment(Qt.AlignRight)
        else:
            label.setStyleSheet("""
                QLabel {
                    background-color: #3c3c3c;
                    color: #ddd;
                    border-radius: 12px;
                    padding: 10px 14px;
                    font-size: 13px;
                }
            """)
            # 设置布局对齐方式为左对齐
            layout.setAlignment(Qt.AlignLeft)
        # 将标签控件添加到布局中
        layout.addWidget(label)


class ChatPanel(QWidget):
    # 定义聊天面板类，作为右侧停靠面板显示AI对话界面
    """AI 聊天面板 — 右侧 Dock 面板"""

    # 信号；定义海报生成信息，用于通知外部海报已生成并传递海报参数
    poster_generated = pyqtSignal(dict)   # 海报生成参数

    def __init__(self, parent=None):
        # 定义构造方法，接收可选的父类对象，定义构造方法，接收可选的父对象
        super().__init__(parent)

        # AI 客户端；初始化AI客户端相关属性；秘钥，模型，客户端，工作线程，对话列表，文档对象
        self._api_key = ""
        self._model = "deepseek-chat"
        self._client: Optional[DeepSeekClient] = None
        self._worker: Optional[AIWorker] = None
        self._conversation: List[Dict] = []
        self._document = None  # Illustrator 文档引用
        # 调用界面初始化方法；调用对话重置方法
        self._init_ui()
        self._reset_conversation()

    def set_document(self, doc):
        # 设置文档方法,接收文档对象参数，接收文档对象参数
        """设置关联的 Illustrator 文档"""
        self._document = doc

    def set_api_key(self, key: str):
        """设置 API Key"""
        # 将传入的密钥保存为私有属性
        self._api_key = key
        self._client = DeepSeekClient(
            api_key=key,
            model=self._model,
        )
        self._reset_conversation()

    def set_model(self, model: str):
        """设置模型"""
        self._model = model
        if self._api_key:
            self._client = DeepSeekClient(
                api_key=self._api_key,
                model=model,
            )
            self._reset_conversation()

    def _reset_conversation(self):
        """重置对话"""
        self._conversation = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    # ── UI 初始化 ──

    def _init_ui(self):
        # 定义私有界面初始化方法；创建一个垂直布局，设置布局的内容边距，设置布局中各个控件之间的间距
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # 标题栏；创建一个水平布局，创建一个标签控件，设置标题标签的样式，在标题布局末尾添加弹性间距
        title_layout = QHBoxLayout()
        title_label = QLabel("🤖 AI 助手")
        title_label.setStyleSheet("color: #ddd; font-weight: bold; font-size: 14px;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        # 创建按钮控件
        self._clear_btn = QPushButton("清空")
        self._clear_btn.setFixedSize(50, 24)
        self._clear_btn.clicked.connect(self._on_clear)
        title_layout.addWidget(self._clear_btn)
        layout.addLayout(title_layout)

        # 模型选择；创建一个水平布局，设置配置布局中控件的间距
        config_layout = QHBoxLayout()
        config_layout.setSpacing(4)
        # 创建一个下拉选择框控件,赋值给私有属性
        self._model_combo = QComboBox()
        self._model_combo.addItems([
            "deepseek-chat", "deepseek-reasoner",
        ])
        # 设置模型选择框的当前选项，选择模型，向配置布局中添加一个模型标签，
        self._model_combo.setCurrentText("deepseek-reasoner")
        self._model_combo.currentTextChanged.connect(self.set_model)
        self._model_combo.setToolTip("选择 DeepSeek 模型")
        config_layout.addWidget(QLabel("模型:"))
        config_layout.addWidget(self._model_combo, 1)

        layout.addLayout(config_layout)

        # API Key 输入
        api_layout = QHBoxLayout()
        api_layout.setSpacing(4)
        # 创建一个单行文本输入框控件,赋值给私有属性
        self._api_input = QLineEdit()
        self._api_input.setPlaceholderText("输入 DeepSeek API Key...")
        self._api_input.setEchoMode(QLineEdit.Password)
        # 设置API输入框的工具提示为从 platform.deepseek.com 获取
        self._api_input.setToolTip("从 platform.deepseek.com 获取")
        # 将API输入框添加到API布局中
        api_layout.addWidget(self._api_input, 1)
        # 创建一个按钮控件
        self._connect_btn = QPushButton("连接")
        self._connect_btn.setFixedSize(50, 24)
        self._connect_btn.clicked.connect(self._on_connect)
        api_layout.addWidget(self._connect_btn)

        layout.addLayout(api_layout)

        # 快捷提示
        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(4)
        quick_label = QLabel("快捷:")
        quick_label.setStyleSheet("color: #888; font-size: 11px;")
        quick_layout.addWidget(quick_label)

        for text, prompt in [
            ("🔥促销", "帮我做一个618促销海报，全场5折，红色风格"),
            ("📱高考宣传海报", "做一个全力以赴，金榜题名社交媒体海报，青春不负梦想，拼搏成就未来，预祝全体考生金榜题名，玫瑰金风格"),
        ]:
            btn = QPushButton(text)
            btn.setFixedHeight(22)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a4a4a; color: #ddd;
                    border: 1px solid #555; border-radius: 3px;
                    padding: 2px 6px; font-size: 11px;
                }
                QPushButton:hover { background-color: #5a5a5a; }
            """)
            # 将按钮的点击信号连接到匿名函数:调用_send_message（发送消息）方法并传入当前prompt（提示词）
            # 按钮点击信号绑定函数：传入勾选状态参数与提示词默认参数，触发时调用自身的发送消息方法并传入提示词变量
            btn.clicked.connect(lambda checked, p=prompt: self._send_message(p))
            quick_layout.addWidget(btn)

        quick_layout.addStretch()
        layout.addLayout(quick_layout)

        # 聊天区域；创建一个滚动区域控件，赋值给私有属性
        self._chat_scroll = QScrollArea()
        self._chat_scroll.setWidgetResizable(True)
        self._chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 创建一个部件容器
        self._chat_container = QWidget()
        # 创建一个垂直布局，以聊天容器为父容器，赋值给私有属性
        self._chat_layout = QVBoxLayout(self._chat_container)
        self._chat_layout.setAlignment(Qt.AlignTop)
        self._chat_layout.setSpacing(4)
        self._chat_layout.addStretch()
        # 将聊天容器设置为滚动区域的子控件；
        self._chat_scroll.setWidget(self._chat_container)
        layout.addWidget(self._chat_scroll, 1)
        # 将聊天滚动区域添加到主垂直布局中，拉伸因子

        # 进度条；
        self._progress = QProgressBar()
        self._progress.setRange(0, 0)  # 不确定模式
        self._progress.setVisible(False)
        self._progress.setFixedHeight(4)
        self._progress.setStyleSheet("""
            QProgressBar { border: none; background: #2d2d2d; }
            QProgressBar::chunk { background: #0d6efd; }
        """)
        # 将进度条添加到垂直布局中
        layout.addWidget(self._progress)

        # 输入区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(4)
        # 创建一个单行文本输入框控件
        self._input = QLineEdit()
        self._input.setPlaceholderText("描述你想要的海报... (Enter 发送)")
        # 将输入框的回车键按下信号连接到_on_send方法
        self._input.returnPressed.connect(self._on_send)
        input_layout.addWidget(self._input, 1)

        self._send_btn = QPushButton("发送")
        self._send_btn.setFixedSize(50, 28)
        self._send_btn.clicked.connect(self._on_send)
        self._send_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd; color: white;
                border: none; border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0b5ed7; }
            QPushButton:disabled { background-color: #555; color: #888; }
        """)
        input_layout.addWidget(self._send_btn)

        layout.addLayout(input_layout)

        # 样式；设置面板整体样式
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
            }
            QLabel {
                color: #bbb;
                font-size: 12px;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #0d6efd;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 2px 6px;
                font-size: 12px;
            }
            # 
            QComboBox:hover { border-color: #0d6efd; }
            # 对象选择框的样式
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #ddd;
                selection-background-color: #0d6efd;
            }
            # 滚动条样式
            QScrollArea {
                border: 1px solid #444;
                background-color: #252525;
            }
        """)

        self.setMinimumWidth(280)

    # ── 消息管理 ──

    def _add_bubble(self, text: str, is_user: bool):
        """添加聊天气泡"""
        # 接收文本内容和是否为用户消息
        # 移除底部的 stretch（安全移除，确保最后一项确实是 spacer）接收文本内容；移除底部的弹性间距
        if self._chat_layout.count() > 0:
            # 如果聊天布局中有子项，取出聊天布局中的最后一个子项
            item = self._chat_layout.takeAt(self._chat_layout.count() - 1)
            if item.spacerItem():
                # 如果取出的项是间隔项
                del item
            else:
                # 不是 spacer，放回去；将布局项重新添加回聊天布局
                self._chat_layout.addItem(item)

        bubble = ChatBubble(text, is_user)
        self._chat_layout.addWidget(bubble)

        # 重新添加 stretch，重新添加弹性间距
        self._chat_layout.addStretch()

        # 滚动到底部
        QTimer.singleShot(50, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        """滚动到底部"""
        # 获取聊天滚动区域的垂直滚动条，将滚动条的值设置为最大值；
        scrollbar = self._chat_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _add_system_message(self, text: str):
        # 定义私有添加系统消息方法；添加系统消息，接收文本内容
        """添加系统消息"""
        # 如果聊天布局中有子项
        if self._chat_layout.count() > 0:
            item = self._chat_layout.takeAt(self._chat_layout.count() - 1)
            if item.spacerItem():
                del item
            else:
                self._chat_layout.addItem(item)
        
        label = CopyableLabel(text)
        # 启用标签的自动换行功能
        label.setWordWrap(True)
        # 设置标签的鼠标光标为文本编辑光标
        label.setCursor(Qt.IBeamCursor)
        # 设置标签的样式
        label.setStyleSheet("""
            QLabel {
                color: #888;
                font-size: 11px;
                padding: 4px 12px;
            }
        """)
        # 设置标签对齐；将标签添加到聊天布局中
        label.setAlignment(Qt.AlignCenter)
        self._chat_layout.addWidget(label)
        self._chat_layout.addStretch()
        QTimer.singleShot(50, self._scroll_to_bottom)

    # ── 事件处理 ──

    def _on_connect(self):
        """连接 API"""
        # 获取API输入框的文本内容并去除首尾空白，赋值给
        key = self._api_input.text().strip()
        if not key:
            QMessageBox.warning(self, "提示", "请输入 DeepSeek API Key")
            return
        self.set_api_key(key)
        self._add_system_message("✅ 已连接到 DeepSeek API")
        self._connect_btn.setText("已连接")
        self._connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #198754; color: white;
                border: none; border-radius: 3px;
                font-size: 11px;
            }
        """)

    def _on_send(self):
        # 定义私有发送处理方法，处理用户点击发送按钮或按下回车键的事件
        """发送消息"""
        text = self._input.text().strip()
        if not text:
            return

        if not self._api_key:
            QMessageBox.warning(self, "提示",
                              "请先输入 DeepSeek API Key 并点击「连接」")
            return

        self._input.clear()
        self._send_message(text)

    def _send_message(self, text: str):
        """处理消息发送"""
        # 显示用户消息，方法文档字符串，处理消息发送
        self._add_bubble(text, is_user=True)

        # 添加到对话历史
        self._conversation.append({"role": "user", "content": text})

        # 显示加载状态；将进度条设置为可见，禁用发送按钮，禁用输入框
        self._progress.setVisible(True)
        self._send_btn.setEnabled(False)
        self._input.setEnabled(False)

        # 创建 AI 响应气泡（稍后更新）
        if self._chat_layout.count() > 0:
            # 取出聊天布局中最后一个子项，
            item = self._chat_layout.takeAt(self._chat_layout.count() - 1)
            if item.spacerItem():
                del item
            else:
                self._chat_layout.addItem(item)
 
        self._ai_response_label = CopyableLabel("🤔 思考中...")
        self._ai_response_label.setWordWrap(True)
        # 设置AI响应标签的文本格式为富文本模式
        self._ai_response_label.setTextFormat(Qt.RichText)
        # 设置AI响应标签的鼠标光标为文本编辑光标
        self._ai_response_label.setCursor(Qt.IBeamCursor)
        self._ai_response_label.setStyleSheet("""
            QLabel {
                background-color: #3c3c3c;
                color: #ddd;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 13px;
            }
        """)
        # 创建水平布局；
        ai_layout = QHBoxLayout()
        # 将AI响应标签添加到AI布局中
        ai_layout.addWidget(self._ai_response_label)
        ai_layout.addStretch()
        # 在将AI布局添加到聊天布局中
        self._chat_layout.addLayout(ai_layout)
        self._chat_layout.addStretch()

        # 构建工具定义
        tools = build_tools_for_deepseek()

        # 创建并启用AI工作线程
        # 启动工作线程；客户端，对话历史列表，工具列表；
        self._worker = AIWorker(
            self._client, self._conversation, tools
        )
        # 将工作线程的流式文本片段信号连接到_on_chunk(片段处理)方法
        self._worker.response_chunk.connect(self._on_chunk)
        self._worker.response_done.connect(self._on_done)
        self._worker.response_error.connect(self._on_error)
        self._worker.poster_ready.connect(self._on_poster_ready)
        self._worker.start()

    def _on_chunk(self, text: str):
        """收到流式文字片段"""
        # 更新 AI 响应气泡
        current = self._ai_response_label.text()
        if current == "🤔 思考中...":
            current = ""
        # 将新的文本片段追加到当前文本中
        current += text
        # 简单 Markdown 渲染
        current = current.replace("\n\n", "<br><br>").replace("\n", "<br>")
        current = current.replace("**", "<b>").replace("</b><b>", "")
        self._ai_response_label.setText(current)
        QTimer.singleShot(20, self._scroll_to_bottom)

    def _on_poster_ready(self, params: Dict):
        """海报参数就绪 — 在文档中生成"""
        # 海报就绪处理方法
        if self._document:
            # 创建海报生成器实例，传入文档对象，赋值给海报生成器
            generator = PosterGenerator(self._document)
            # 调用生成器方法，传入海报参数，将结果赋值给result
            result = generator.generate(params)
            # 发射海报生成信号，传递海报参数
            self.poster_generated.emit(params)

    def _on_done(self, response: Dict):
        # 定义私有完成处理方法(完成处理)，接受完整响应字典
        """AI 回复完成"""
        self._progress.setVisible(False)
        self._send_btn.setEnabled(True)
        self._input.setEnabled(True)
        # 从响应字典中获取文本字段
        text = response.get("text", "")

        # 格式化最终回复
        formatted = text.replace("\n\n", "<br><br>").replace("\n", "<br>")
        formatted = formatted.replace("**", "<b>").replace("</b><b>", "")
        if formatted:
            # 格式化后文本非空，将格式化后的文本设置到AI响应标签中
            self._ai_response_label.setText(formatted)
        else:
            self._ai_response_label.setText("操作已完成。")

        # 添加到对话历史；角色为助手，内容为AI回复的原始文本
        self._conversation.append({
            "role": "assistant",
            "content": text,
        })
        # 将输入焦点设置回输入框
        self._input.setFocus()

    def _on_error(self, error: str):
        """AI 调用出错"""
        self._progress.setVisible(False)
        self._send_btn.setEnabled(True)
        self._input.setEnabled(True)
        # 将错误提示信息设置到AI响应标签中：
        self._ai_response_label.setText(
            f"❌ 出错了: {error}<br><br>请检查 API Key 是否正确，或稍后重试。"
        )
        self._ai_response_label.setStyleSheet("""
            QLabel {
                background-color: #5c1a1a;
                color: #f88;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 13px;
            }
        """)

        logger.error(f"AI error: {error}")

    def _on_clear(self):
        """清空对话"""
        self._reset_conversation()
        # 重置对话历史

        # 清空聊天区域 - 安全的清理方式
        # 当聊天布局中还有子项时，循环执行直到清空
        while self._chat_layout.count() > 0:
            # 取出聊天布局中第一个子项，赋值给item
            item = self._chat_layout.takeAt(0)
            # 取出的项是控件；获取该控件实例
            if item.widget():
                widget = item.widget()
                # 解除控件与父容器之间的父子关系
                widget.setParent(None)  # 先解除父子关系
                widget.deleteLater()
            elif item.layout():
                # 递归调用清空布局，清空该子布局
                self._clear_layout(item.layout())
            # spacerItem 不需要特殊处理
        # 在聊天布局末尾添加弹性间距
        self._chat_layout.addStretch()
        # 添加系统消息，“对话已清空，可以开始新的对话”
        self._add_system_message("对话已清空，可以开始新的对话。")


    def _clear_layout(self, layout):
        """递归清空布局"""
        # 若布局中还有子项时，取出布局中第一个子项
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
