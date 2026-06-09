# main.py — 逐行注解翻译

---

```python
"""
简易 Illustrator 应用入口 (Python 3.10+) — DeepSeek AI 驱动版
```
# 文件文档字符串：简易 Illustrator 应用程序入口（Python 3.10以上版本）—— DeepSeek 人工智能驱动版本

```python
基于 PyQt5 实现的矢量图形编辑器，集成 DeepSeek 大模型交互式对话。
```
# 基于 PyQt5 图形界面框架实现的矢量图形编辑器，集成了 DeepSeek 大型语言模型的交互式对话功能

```python
支持：选择、矩形、椭圆、钢笔路径、文字工具
```
# 功能支持：选择工具、矩形绘制、椭圆绘制、钢笔路径绘制、文字工具

```python
AI功能：自然语言对话生成矢量文本海报（6种模板，9种配色方案）
```
# 人工智能功能：通过自然语言对话来生成矢量文本海报（提供6种模板样式，9种配色方案）

```python
功能：图层管理、属性编辑、颜色填充/描边、编组、导出PNG/SVG
```
# 功能：图层管理操作、属性编辑、颜色填充与描边、图形编组、导出为PNG/SVG格式

```python
启动方式：
    python main.py                                    # 默认启动
    python main.py --api-key sk-xxx                   # 指定 API Key
    python main.py --model deepseek-reasoner          # 指定模型
    set DEEPSEEK_API_KEY=sk-xxx && python main.py     # 环境变量方式
```
# 启动方式说明：
# python main.py                                       默认启动方式
# python main.py --api-key sk-xxx                      指定应用程序接口密钥
# python main.py --model deepseek-reasoner             指定使用的模型名称
# set DEEPSEEK_API_KEY=sk-xxx && python main.py        通过环境变量设置密钥方式

```python
要求: Python 3.10+
```
# 运行环境要求：Python 版本 3.10 及以上

```python
"""
```
# 文档字符串结束

---

```python
from __future__ import annotations
```
# 从未来版本特性中导入注解支持（启用前向引用类型注解）

```python
import sys
```
# 导入系统相关功能模块

```python
import os
```
# 导入操作系统接口模块

```python
import logging
```
# 导入日志记录模块

```python
import argparse
```
# 导入命令行参数解析模块

```python
from PyQt5.QtWidgets import QApplication
```
# 从 PyQt5 图形界面的窗口部件模块中导入应用程序类

```python
from PyQt5.QtCore import Qt
```
# 从 PyQt5 图形界面的核心模块中导入 Qt 命名空间

---

```python
# Python 版本检查
```
# 注释：Python 版本检查

```python
if sys.version_info < (3, 10):
```
# 如果当前 Python 版本信息小于 3.10 版本：

```python
    sys.exit("❌ 本应用需要 Python 3.10 或更高版本。当前版本: " + sys.version)
```
#     调用系统退出函数并提示：本应用需要 Python 3.10 或更高版本，显示当前版本号

---

```python
from illustrator_app.logging_config import setup_logging, get_logger
```
# 从 illustrator_app 包的日志配置模块中导入设置日志函数和获取日志记录器函数

```python
from illustrator_app.ui.main_window import MainWindow
```
# 从 illustrator_app 包的用户界面模块中导入主窗口类

```python
logger = get_logger(__name__)
```
# 获取当前模块的日志记录器实例

---

```python
def parse_args() -> argparse.Namespace:
```
# 定义解析命令行参数函数，返回参数命名空间对象

```python
    """解析命令行参数"""
```
#     函数文档字符串：解析命令行参数

```python
    parser = argparse.ArgumentParser(
```
#     创建命令行参数解析器实例

```python
        description="简易 Illustrator — DeepSeek AI 驱动矢量图形编辑器 (Python 3.10+)",
```
#         描述信息：简易 Illustrator —— DeepSeek 人工智能驱动矢量图形编辑器（Python 3.10以上版本）

```python
        formatter_class=argparse.RawDescriptionHelpFormatter,
```
#         格式化类：使用原始描述帮助格式化器

```python
        epilog="""
示例:
  python main.py
  python main.py --api-key sk-your-deepseek-key
  python main.py --model deepseek-reasoner --api-key sk-xxx
        """,
```
#         结尾说明文本：包含使用示例

```python
    )
```
#     参数解析器创建完毕

```python
    parser.add_argument(
```
#     添加命令行参数定义

```python
        "--api-key", "-k", type=str, default=None,
```
#         参数名：--api-key，短名称：-k，类型：字符串，默认值：无

```python
        help="DeepSeek API Key (也可通过 DEEPSEEK_API_KEY 环境变量设置)",
```
#         帮助信息：DeepSeek 应用程序接口密钥（也可通过环境变量 DEEPSEEK_API_KEY 设置）

```python
    )
```
#     参数添加完毕

```python
    parser.add_argument(
```
#     添加命令行参数定义

```python
        "--model", "-m", type=str, default="deepseek-chat",
```
#         参数名：--model，短名称：-m，类型：字符串，默认值：deepseek-chat

```python
        choices=["deepseek-chat", "deepseek-reasoner"],
```
#         可选值列表：deepseek-chat 或 deepseek-reasoner

```python
        help="DeepSeek 模型 (默认: deepseek-chat)",
```
#         帮助信息：DeepSeek 模型选择（默认使用 deepseek-chat）

```python
    )
```
#     参数添加完毕

```python
    parser.add_argument(
```
#     添加命令行参数定义

```python
        "--base-url", type=str, default=None,
```
#         参数名：--base-url，类型：字符串，默认值：无

```python
        help="API Base URL (默认: https://api.deepseek.com/v1)",
```
#         帮助信息：应用程序接口基础地址（默认地址：https://api.deepseek.com/v1）

```python
    )
```
#     参数添加完毕

```python
    parser.add_argument(
```
#     添加命令行参数定义

```python
        "--debug", "-d", action="store_true", default=False,
```
#         参数名：--debug，短名称：-d，动作：存储为真值，默认值：假

```python
        help="开启调试模式（控制台输出 DEBUG 级别日志）",
```
#         帮助信息：开启调试模式（控制台将输出调试级别的日志信息）

```python
    )
```
#     参数添加完毕

```python
    return parser.parse_args()
```
#     返回解析后的命令行参数结果

---

```python
def _global_exception_handler(exc_type, exc_value, exc_tb):
```
# 定义全局异常处理函数（接收异常类型、异常值、异常追踪对象）

```python
    """全局异常捕获，输出详细错误信息"""
```
#     函数文档字符串：全局异常捕获，输出详细的错误信息

```python
    import traceback
```
#     导入异常追踪模块

```python
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
```
#     调用格式化异常函数，将异常类型、异常值、追踪对象格式化为字符串列表

```python
    error_msg = "".join(tb_lines)
```
#     将追踪字符串列表拼接为完整的错误信息字符串

```python
    print(f"[FATAL ERROR]\n{error_msg}", file=sys.stderr)
```
#     在标准错误输出中打印致命错误标记和完整错误信息

```python
    # 写入日志文件
```
#     注释：将错误信息写入日志文件

```python
    try:
```
#     尝试执行以下代码块：

```python
        logging.getLogger(__name__).critical(f"未捕获的异常:\n{error_msg}")
```
#         获取当前模块的日志记录器，记录严重级别的日志：未捕获的异常及详情

```python
    except Exception:
```
#     如果发生任何异常：

```python
        pass
```
#         忽略异常，继续执行

```python
    # 尝试弹窗显示错误
```
#     注释：尝试弹出窗口显示错误信息

```python
    try:
```
#     尝试执行以下代码块：

```python
        from PyQt5.QtWidgets import QMessageBox
```
#         从 PyQt5 图形界面部件模块中导入消息框类

```python
        QMessageBox.critical(None, "应用错误", f"发生未捕获的异常:\n\n{exc_value}\n\n详情已输出到控制台。")
```
#         显示严重错误消息框，标题为"应用错误"，内容包含异常值和提示信息

```python
    except Exception:
```
#     如果发生任何异常：

```python
        pass
```
#         忽略异常，继续执行

```python
    sys.__excepthook__(exc_type, exc_value, exc_tb)
```
#     调用系统原始的异常钩子函数，传递异常信息

---

```python
def main():
```
# 定义主函数

```python
    args = parse_args()
```
#     调用解析命令行参数函数，获取参数对象

```python
    # ── 初始化日志系统 ─────────────────────────────────
```
#     注释：初始化日志系统

```python
    setup_logging(debug_mode=args.debug)
```
#     调用设置日志函数，根据调试模式参数配置日志系统

```python
    logger.info("应用程序启动")
```
#     记录信息级别日志：应用程序启动

```python
    # 安装全局异常捕获
```
#     注释：安装全局异常捕获处理

```python
    sys.excepthook = _global_exception_handler
```
#     将系统的异常钩子设置为自定义的全局异常处理函数

```python
    # API Key 优先级: 命令行 > 环境变量
```
#     注释：应用程序接口密钥优先级：命令行参数优先于环境变量

```python
    api_key = args.api_key or os.environ.get("DEEPSEEK_API_KEY", "")
```
#     获取接口密钥：优先使用命令行参数中的密钥，否则从环境变量 DEEPSEEK_API_KEY 获取，都没有则为空字符串

```python
    if api_key:
```
#     如果接口密钥存在（非空）：

```python
        logger.info(f"API Key 已配置 (来源: {'命令行' if args.api_key else '环境变量'})")
```
#         记录信息级别日志：接口密钥已配置，显示来源是命令行还是环境变量

```python
    else:
```
#     否则（密钥为空）：

```python
        logger.warning("未设置 API Key，AI 功能将不可用")
```
#         记录警告级别日志：未设置接口密钥，人工智能功能将不可用

```python
    # 高DPI支持
```
#     注释：启用高分辨率显示器支持

```python
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
```
#     设置应用程序属性：启用高分辨率缩放（使界面在高DPI屏幕上清晰显示）

```python
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
```
#     设置应用程序属性：使用高分辨率像素图（图标和图片在高DPI下保持清晰）

```python
    app = QApplication(sys.argv)
```
#     创建应用程序实例，传入系统命令行参数

```python
    app.setApplicationName("简易 Illustrator — AI 驱动")
```
#     设置应用程序名称：简易 Illustrator —— 人工智能驱动

```python
    app.setOrganizationName("MiniIllustrator")
```
#     设置组织名称：MiniIllustrator

```python
    # 应用程序设置样式表
```
#     注释：为应用程序设置全局样式表

```python
    app.setStyleSheet("""
```
#     设置应用程序的层叠样式表（CSS风格）：

```python
        QToolTip {
            background-color: #333; color: #ddd;
            border: 1px solid #555; padding: 4px;
        }
```
#         工具提示样式：背景色深灰(#333)、文字色浅灰(#ddd)、边框1像素实线灰色(#555)、内边距4像素

```python
        QScrollBar:vertical { background: #2d2d2d; width: 10px; }
```
#         垂直滚动条样式：背景色深灰(#2d2d2d)、宽度10像素

```python
        QScrollBar::handle:vertical {
            background: #555; border-radius: 5px; min-height: 20px;
        }
```
#         垂直滚动条滑块样式：背景色灰色(#555)、圆角半径5像素、最小高度20像素

```python
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
```
#         垂直滚动条上下箭头按钮样式：高度设为0像素（隐藏箭头）

```python
    """)
```
#     样式表设置完毕

```python
    window = MainWindow()
```
#     创建主窗口实例

```python
    if api_key:
```
#     如果接口密钥存在：

```python
        window._chat_panel.set_api_key(api_key)
```
#         调用主窗口的聊天面板对象的设置接口密钥方法

```python
        if args.model:
```
#         如果命令行指定了模型参数：

```python
            window._chat_panel.set_model(args.model)
```
#             调用主窗口的聊天面板对象的设置模型方法

```python
    window.show()
```
#     显示主窗口

```python
    sys.exit(app.exec_())
```
#     进入应用程序事件循环，程序退出时返回退出码

---

```python
if __name__ == "__main__":
```
# 如果当前脚本作为主程序运行（而非被导入为模块）：

```python
    main()
```
#     调用主函数启动应用程序
