"""
统一日志配置模块 (Python 3.10+)

为整个 Illustrator 应用提供统一的日志记录功能。
支持：
- 控制台输出（开发调试）
- 文件输出（持久化记录）
- 按模块分级控制日志级别
- 自动轮转日志文件，防止无限增长
"""

from __future__ import annotations

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional


# ── 默认配置 ───────────────────────────────────────────

DEFAULT_LOG_DIR = Path.home() / ".mini_illustrator" / "logs"
DEFAULT_LOG_FILE = "app.log"
DEFAULT_MAX_BYTES = 5 * 1024 * 1024  # 5MB 单个文件上限
DEFAULT_BACKUP_COUNT = 3              # 保留最近 3 个备份
DEFAULT_CONSOLE_LEVEL = logging.INFO
DEFAULT_FILE_LEVEL = logging.DEBUG


def setup_logging(
    log_dir: str | Path | None = None,
    log_file: str = DEFAULT_LOG_FILE,
    console_level: int = DEFAULT_CONSOLE_LEVEL,
    file_level: int = DEFAULT_FILE_LEVEL,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT,
    debug_mode: bool = False,
) -> None:
    """配置全局日志系统。

    Args:
        log_dir: 日志文件目录，默认为 ~/.mini_illustrator/logs
        log_file: 日志文件名
        console_level: 控制台输出级别
        file_level: 文件输出级别
        max_bytes: 单个日志文件最大字节数
        backup_count: 保留的备份文件数量
        debug_mode: 如果为 True，控制台级别设为 DEBUG
    """
    if log_dir is None:
        log_dir = DEFAULT_LOG_DIR

    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    if debug_mode:
        console_level = logging.DEBUG

    # ── 根 logger ──────────────────────────────────────
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # 根 logger 捕获所有级别

    # 清除已有的 handlers（避免重复添加）
    root_logger.handlers.clear()

    # ── 日志格式 ───────────────────────────────────────
    # 控制台：简洁格式，带颜色标记（ANSI）
    console_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-5s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # 文件：详细格式，含文件名和行号
    file_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-5s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── 控制台 Handler ─────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # ── 文件 Handler（轮转） ────────────────────────────
    log_path = log_dir / log_file
    file_handler = logging.handlers.RotatingFileHandler(
        filename=str(log_path),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # ── 按模块调整日志级别 ─────────────────────────────
    # 第三方库默认只显示 WARNING 及以上
    _suppress_third_party_loggers()

    # ── 记录启动信息 ───────────────────────────────────
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info(f"日志系统已初始化")
    logger.info(f"  日志目录: {log_dir}")
    logger.info(f"  控制台级别: {logging.getLevelName(console_level)}")
    logger.info(f"  文件级别:   {logging.getLevelName(file_level)}")
    logger.info(f"  Python:     {sys.version}")
    logger.info("=" * 50)


def _suppress_third_party_loggers() -> None:
    """降低第三方库的日志输出级别，减少噪音。"""
    noisy_loggers = [
        "urllib3",
        "requests",
        "httpx",
        "openai",
        "httpcore",
        "PIL",
        "matplotlib",
    ]
    for name in noisy_loggers:
        logging.getLogger(name).setLevel(logging.WARNING)

    # PyQt5 内部日志
    logging.getLogger("PyQt5").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    # 获取日志记录器函数，参数为字符串类型的名称返回日志记录器对象
    """获取指定模块的 logger。

    推荐用法：
        from illustrator_app.logging_config import get_logger
        logger = get_logger(__name__)
    """
    # 返回指定名称的日志记录器实例
    return logging.getLogger(name)


def enable_debug_for_module(module_name: str) -> None:
    """临时开启某个模块的 DEBUG 级别日志，方便调试。

    Args:
        module_name: 模块名，如 "illustrator_app.core.tools"
    """
    logging.getLogger(module_name).setLevel(logging.DEBUG)
    logging.getLogger(__name__).info(f"已为模块 '{module_name}' 开启 DEBUG 日志")


def get_log_file_path() -> Path:
    """返回当前日志文件的路径。"""
    return DEFAULT_LOG_DIR / DEFAULT_LOG_FILE
    # 返回默认日志目录与默认日志文件名拼接后的完整路径
