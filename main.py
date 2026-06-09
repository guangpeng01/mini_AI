"""
简易 Illustrator 应用入口 (Python 3.10+) — DeepSeek AI 驱动版

基于 PyQt5 实现的矢量图形编辑器，集成 DeepSeek 大模型交互式对话。
支持：选择、矩形、椭圆、钢笔路径、文字工具
AI功能：自然语言对话生成矢量文本海报（6种模板，9种配色方案）
功能：图层管理、属性编辑、颜色填充/描边、编组、导出PNG/SVG

启动方式：
    python main.py                                    # 默认启动
    python main.py --api-key sk-xxx                   # 指定 API Key
    python main.py --model deepseek-reasoner          # 指定模型
    set DEEPSEEK_API_KEY=sk-xxx && python main.py     # 环境变量方式

要求: Python 3.10+
"""

from __future__ import annotations

import sys
import os
import logging
import argparse
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
# 图形界面的窗口部件模块 、 图形界面的核心模块
# Python 版本检查
if sys.version_info < (3, 10):
    sys.exit("❌ 本应用需要 Python 3.10 或更高版本。当前版本: " + sys.version)

from illustrator_app.logging_config import setup_logging, get_logger
from illustrator_app.ui.main_window import MainWindow

logger = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        # 描述信息 / 格式化類 / 説明文本
        description="简易 Illustrator — DeepSeek AI 驱动矢量图形编辑器 (Python 3.10+)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py
  python main.py --api-key sk-your-deepseek-key
  python main.py --model deepseek-reasoner --api-key sk-xxx
        """,
    )
    parser.add_argument(
        "--api-key", "-k", type=str, default=None,
        help="DeepSeek API Key (也可通过 DEEPSEEK_API_KEY 环境变量设置)",
    )
    parser.add_argument(
        "--model", "-m", type=str, default="deepseek-chat",
        choices=["deepseek-chat", "deepseek-reasoner"],
        help="DeepSeek 模型 (默认: deepseek-chat)",
    )
    parser.add_argument(
        "--base-url", type=str, default=None,
        help="API Base URL (默认: https://api.deepseek.com/v1)",
    )
    parser.add_argument(
        "--debug", "-d", action="store_true", default=False,
        help="开启调试模式（控制台输出 DEBUG 级别日志）",
    )
    return parser.parse_args()


def _global_exception_handler(exc_type, exc_value, exc_tb):
    """全局异常捕获，输出详细错误信息"""
    import traceback
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
    error_msg = "".join(tb_lines)
    # 在标准错误输出中打印致命错误标记和完整错误信息
    print(f"[FATAL ERROR]\n{error_msg}", file=sys.stderr)
    # 写入日志文件
    try:
        # 获取当前模块的日志记录器，记录严重级别的日志
        logging.getLogger(__name__).critical(f"未捕获的异常:\n{error_msg}")
    except Exception:
        pass
    # 尝试弹窗显示错误
    try:
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(None, "应用错误", f"发生未捕获的异常:\n\n{exc_value}\n\n详情已输出到控制台。")
    except Exception:
        pass
    sys.__excepthook__(exc_type, exc_value, exc_tb)


def main():
    # 调用解析命令行函数，获取参数对象
    args = parse_args()

    # ── 初始化日志系统 ─────────────────────────────────
    setup_logging(debug_mode=args.debug)
    logger.info("应用程序启动")

    # 安装全局异常捕获
    sys.excepthook = _global_exception_handler

    # API Key 优先级: 命令行 > 环境变量
    api_key = args.api_key or os.environ.get("DEEPSEEK_API_KEY", "")

    if api_key:
        logger.info(f"API Key 已配置 (来源: {'命令行' if args.api_key else '环境变量'})")
    else:
        logger.warning("未设置 API Key，AI 功能将不可用")

    # 高DPI支持；设置应用程序属性：启用高分辨率缩放（使界面在高DPI屏幕上清晰显示）
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # 设置应用程序属性：使用高分辨率像素图
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    # 创建应用程序实例，传入系统命令行参数 、 设置应用程序名称 ，设置组织名称
    app = QApplication(sys.argv)
    app.setApplicationName("简易 Illustrator — AI 驱动")
    app.setOrganizationName("MiniIllustrator")
    # 应用程序设置样式表；工具提示样式，垂直滚动条样式，垂直滚动条滑块，垂直滚动条上下箭头按钮样式
    app.setStyleSheet("""
        QToolTip {
            background-color: #333; color: #ddd;
            border: 1px solid #555; padding: 4px;
        }
        QScrollBar:vertical { background: #2d2d2d; width: 10px; }
        QScrollBar::handle:vertical {
            background: #555; border-radius: 5px; min-height: 20px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
    """)
    # 创建主窗口实例
    window = MainWindow()
    # 如果接口秘钥存在
    if api_key:
        # 调用主窗口的设置接口密钥方法
        window._chat_panel.set_api_key(api_key)
        if args.model:
            window._chat_panel.set_model(args.model)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
