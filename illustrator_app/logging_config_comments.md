# illustrator_app/logging_config.py — 逐行注解翻译

---

```python
"""
统一日志配置模块 (Python 3.10+)
```
# 文件文档字符串：统一日志配置模块（Python 3.10以上版本）

```python
为整个 Illustrator 应用提供统一的日志记录功能。
```
# 为整个 Illustrator 应用程序提供统一的日志记录功能

```python
支持：
- 控制台输出（开发调试）
- 文件输出（持久化记录）
- 按模块分级控制日志级别
- 自动轮转日志文件，防止无限增长
```
# 功能支持：
# - 控制台输出（用于开发调试）
# - 文件输出（用于持久化记录）
# - 按模块分级控制日志输出级别
# - 自动轮转日志文件，防止文件无限增长

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
import logging
```
# 导入日志记录模块

```python
import logging.handlers
```
# 导入日志处理器子模块（包含轮转文件处理器等）

```python
import os
```
# 导入操作系统接口模块

```python
import sys
```
# 导入系统相关功能模块

```python
from pathlib import Path
```
# 从路径处理库中导入路径类

```python
from typing import Optional
```
# 从类型提示模块中导入可选类型

---

```python
# ── 默认配置 ───────────────────────────────────────────
```
# 注释：默认配置参数区域

```python
DEFAULT_LOG_DIR = Path.home() / ".mini_illustrator" / "logs"
```
# 默认日志目录：用户主目录下的 .mini_illustrator/logs 路径

```python
DEFAULT_LOG_FILE = "app.log"
```
# 默认日志文件名：app.log

```python
DEFAULT_MAX_BYTES = 5 * 1024 * 1024  # 5MB 单个文件上限
```
# 默认最大字节数：5乘以1024乘以1024等于5MB（单个日志文件的大小上限）

```python
DEFAULT_BACKUP_COUNT = 3              # 保留最近 3 个备份
```
# 默认备份文件数量：3（保留最近3个轮转备份文件）

```python
DEFAULT_CONSOLE_LEVEL = logging.INFO
```
# 默认控制台日志级别：信息级别

```python
DEFAULT_FILE_LEVEL = logging.DEBUG
```
# 默认文件日志级别：调试级别（最详细）

---

```python
def setup_logging(
```
# 定义设置日志系统函数

```python
    log_dir: str | Path | None = None,
```
#     日志目录参数：类型为字符串、路径对象或空，默认值为空

```python
    log_file: str = DEFAULT_LOG_FILE,
```
#     日志文件名参数：字符串类型，默认使用 DEFAULT_LOG_FILE

```python
    console_level: int = DEFAULT_CONSOLE_LEVEL,
```
#     控制台输出级别参数：整数类型，默认使用 DEFAULT_CONSOLE_LEVEL

```python
    file_level: int = DEFAULT_FILE_LEVEL,
```
#     文件输出级别参数：整数类型，默认使用 DEFAULT_FILE_LEVEL

```python
    max_bytes: int = DEFAULT_MAX_BYTES,
```
#     最大字节数参数：整数类型，默认使用 DEFAULT_MAX_BYTES

```python
    backup_count: int = DEFAULT_BACKUP_COUNT,
```
#     备份数量参数：整数类型，默认使用 DEFAULT_BACKUP_COUNT

```python
    debug_mode: bool = False,
```
#     调试模式参数：布尔类型，默认值为假

```python
) -> None:
```
# 函数返回类型：无返回值

```python
    """配置全局日志系统。
```
#     函数文档字符串：配置全局日志系统

```python
    Args:
        log_dir: 日志文件目录，默认为 ~/.mini_illustrator/logs
        log_file: 日志文件名
        console_level: 控制台输出级别
        file_level: 文件输出级别
        max_bytes: 单个日志文件最大字节数
        backup_count: 保留的备份文件数量
        debug_mode: 如果为 True，控制台级别设为 DEBUG
    """
```
#     参数说明：
#         log_dir：日志文件目录，默认路径为用户主目录下的 .mini_illustrator/logs
#         log_file：日志文件名
#         console_level：控制台输出级别
#         file_level：文件输出级别
#         max_bytes：单个日志文件最大字节数
#         backup_count：保留的备份文件数量
#         debug_mode：如果为真，控制台级别设为调试级别

```python
    if log_dir is None:
```
#     如果日志目录参数为空：

```python
        log_dir = DEFAULT_LOG_DIR
```
#         将日志目录设为默认日志目录

```python
    log_dir = Path(log_dir)
```
#     将日志目录转换为路径对象

```python
    log_dir.mkdir(parents=True, exist_ok=True)
```
#     创建日志目录（递归创建父目录，如果已存在则不报错）

```python
    if debug_mode:
```
#     如果启用了调试模式：

```python
        console_level = logging.DEBUG
```
#         将控制台日志级别设为调试级别

```python
    # ── 根 logger ──────────────────────────────────────
```
#     注释：配置根日志记录器

```python
    root_logger = logging.getLogger()
```
#     获取根日志记录器实例

```python
    root_logger.setLevel(logging.DEBUG)  # 根 logger 捕获所有级别
```
#     设置根日志记录器级别为调试（根记录器捕获所有级别的日志消息）

```python
    # 清除已有的 handlers（避免重复添加）
```
#     注释：清除已有的处理器（避免重复添加导致日志重复输出）

```python
    root_logger.handlers.clear()
```
#     清空根日志记录器的处理器列表

```python
    # ── 日志格式 ───────────────────────────────────────
```
#     注释：配置日志输出格式

```python
    # 控制台：简洁格式，带颜色标记（ANSI）
```
#     注释：控制台输出使用简洁格式，带ANSI颜色标记

```python
    console_formatter = logging.Formatter(
```
#     创建控制台日志格式化器实例

```python
        fmt="%(asctime)s [%(levelname)-5s] %(name)s: %(message)s",
```
#         格式模板：时间戳、级别名称（左对齐5字符）、记录器名称、日志消息

```python
        datefmt="%H:%M:%S",
```
#         日期时间格式：时:分:秒

```python
    )
```
#     控制台格式化器创建完毕

```python
    # 文件：详细格式，含文件名和行号
```
#     注释：文件输出使用详细格式，包含文件名和行号

```python
    file_formatter = logging.Formatter(
```
#     创建文件日志格式化器实例

```python
        fmt="%(asctime)s [%(levelname)-5s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
```
#         格式模板：时间戳、级别名称、记录器名称、文件名、行号、日志消息

```python
        datefmt="%Y-%m-%d %H:%M:%S",
```
#         日期时间格式：年-月-日 时:分:秒

```python
    )
```
#     文件格式化器创建完毕

```python
    # ── 控制台 Handler ─────────────────────────────────
```
#     注释：配置控制台日志处理器

```python
    console_handler = logging.StreamHandler(sys.stdout)
```
#     创建控制台流处理器，输出目标为标准输出

```python
    console_handler.setLevel(console_level)
```
#     设置控制台处理器的日志级别

```python
    console_handler.setFormatter(console_formatter)
```
#     设置控制台处理器的格式化器

```python
    root_logger.addHandler(console_handler)
```
#     将控制台处理器添加到根日志记录器

```python
    # ── 文件 Handler（轮转） ────────────────────────────
```
#     注释：配置文件日志处理器（支持轮转）

```python
    log_path = log_dir / log_file
```
#     拼接完整的日志文件路径

```python
    file_handler = logging.handlers.RotatingFileHandler(
```
#     创建轮转文件处理器实例

```python
        filename=str(log_path),
```
#         文件名参数：将路径对象转为字符串

```python
        maxBytes=max_bytes,
```
#         最大字节数参数：单文件大小上限

```python
        backupCount=backup_count,
```
#         备份数量参数：保留的轮转备份文件数

```python
        encoding="utf-8",
```
#         编码参数：使用 UTF-8 编码

```python
    )
```
#     轮转文件处理器创建完毕

```python
    file_handler.setLevel(file_level)
```
#     设置文件处理器的日志级别

```python
    file_handler.setFormatter(file_formatter)
```
#     设置文件处理器的格式化器

```python
    root_logger.addHandler(file_handler)
```
#     将文件处理器添加到根日志记录器

```python
    # ── 按模块调整日志级别 ─────────────────────────────
```
#     注释：按模块调整日志输出级别

```python
    # 第三方库默认只显示 WARNING 及以上
```
#     注释：第三方库默认只显示警告级别及以上的日志

```python
    _suppress_third_party_loggers()
```
#     调用抑制第三方库日志函数

```python
    # ── 记录启动信息 ───────────────────────────────────
```
#     注释：记录系统启动信息

```python
    logger = logging.getLogger(__name__)
```
#     获取当前模块的日志记录器

```python
    logger.info("=" * 50)
```
#     记录信息级别日志：50个等号作为分隔线

```python
    logger.info(f"日志系统已初始化")
```
#     记录信息级别日志：日志系统已初始化

```python
    logger.info(f"  日志目录: {log_dir}")
```
#     记录信息级别日志：显示日志目录路径

```python
    logger.info(f"  控制台级别: {logging.getLevelName(console_level)}")
```
#     记录信息级别日志：显示控制台日志级别名称

```python
    logger.info(f"  文件级别:   {logging.getLevelName(file_level)}")
```
#     记录信息级别日志：显示文件日志级别名称

```python
    logger.info(f"  Python:     {sys.version}")
```
#     记录信息级别日志：显示当前 Python 版本

```python
    logger.info("=" * 50)
```
#     记录信息级别日志：50个等号作为分隔线

---

```python
def _suppress_third_party_loggers() -> None:
```
# 定义抑制第三方库日志函数，返回类型为无

```python
    """降低第三方库的日志输出级别，减少噪音。"""
```
#     函数文档字符串：降低第三方库的日志输出级别，减少不必要的日志噪音

```python
    noisy_loggers = [
```
#     定义噪音日志记录器名称列表：

```python
        "urllib3",
```
#         urllib3 网络库

```python
        "requests",
```
#         requests 网络请求库

```python
        "httpx",
```
#         httpx 网络客户端库

```python
        "openai",
```
#         openai 人工智能接口库

```python
        "httpcore",
```
#         httpcore 底层HTTP库

```python
        "PIL",
```
#         PIL 图像处理库

```python
        "matplotlib",
```
#         matplotlib 绘图库

```python
    ]
```
#     列表定义完毕

```python
    for name in noisy_loggers:
```
#     遍历噪音日志记录器名称列表中的每个名称：

```python
        logging.getLogger(name).setLevel(logging.WARNING)
```
#         获取对应名称的日志记录器，将其级别设为警告级别

```python
    # PyQt5 内部日志
```
#     注释：PyQt5 图形界面框架的内部日志

```python
    logging.getLogger("PyQt5").setLevel(logging.WARNING)
```
#     获取 PyQt5 日志记录器，将其级别设为警告级别

---

```python
def get_logger(name: str) -> logging.Logger:
```
# 定义获取日志记录器函数，参数为字符串类型的名称，返回日志记录器对象

```python
    """获取指定模块的 logger。
```
#     函数文档字符串：获取指定模块的日志记录器

```python
    推荐用法：
        from illustrator_app.logging_config import get_logger
        logger = get_logger(__name__)
    """
```
#     推荐用法示例：
#         从 illustrator_app.logging_config 模块导入 get_logger 函数
#         调用 get_logger(__name__) 获取当前模块的日志记录器

```python
    return logging.getLogger(name)
```
#     返回指定名称的日志记录器实例

---

```python
def enable_debug_for_module(module_name: str) -> None:
```
# 定义启用模块调试日志函数，参数为字符串类型的模块名称，返回类型为无

```python
    """临时开启某个模块的 DEBUG 级别日志，方便调试。
```
#     函数文档字符串：临时开启某个模块的调试级别日志，方便调试

```python
    Args:
        module_name: 模块名，如 "illustrator_app.core.tools"
    """
```
#     参数说明：
#         module_name：模块名称，例如 "illustrator_app.core.tools"

```python
    logging.getLogger(module_name).setLevel(logging.DEBUG)
```
#     获取指定模块名称的日志记录器，将其级别设为调试级别

```python
    logging.getLogger(__name__).info(f"已为模块 '{module_name}' 开启 DEBUG 日志")
```
#     获取当前模块的日志记录器，记录信息级别日志：已为指定模块开启调试日志

---

```python
def get_log_file_path() -> Path:
```
# 定义获取日志文件路径函数，返回类型为路径对象

```python
    """返回当前日志文件的路径。"""
```
#     函数文档字符串：返回当前日志文件的路径

```python
    return DEFAULT_LOG_DIR / DEFAULT_LOG_FILE
```
#     返回默认日志目录与默认日志文件名拼接后的完整路径
