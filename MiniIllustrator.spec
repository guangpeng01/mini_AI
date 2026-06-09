# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件 — 简易 Illustrator (AI 驱动版)
打包命令: pyinstaller MiniIllustrator.spec
"""

import os
import sys
from pathlib import Path

# 项目根目录（SPECPATH 由 PyInstaller 运行时提供）
PROJECT_ROOT = Path(SPECPATH)  # pyright: ignore

a = Analysis(
    # ★ 入口文件
    [str(PROJECT_ROOT / 'main.py')],

    pathex=[str(PROJECT_ROOT)],

    binaries=[],
    datas=[],

    # ★ 隐式依赖（PyInstaller 可能自动检测不到的动态导入模块）
    hiddenimports=[
        # PyQt5 核心模块
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtSvg',

        # 标准库（部分可能被遗漏）
        'logging.handlers',
        'urllib.request',
        'urllib.error',
        'json',
        'uuid',
        'copy',
        'math',
        'abc',
        'enum',
        'dataclasses',
        'threading',
        'argparse',
        'pathlib',
        'traceback',

        # 项目内部包（确保三层包都被收集）
        'illustrator_app',
        'illustrator_app.core',
        'illustrator_app.ui',
        'illustrator_app.ai',
        'illustrator_app.core.graphics',
        'illustrator_app.core.document',
        'illustrator_app.core.tools',
        'illustrator_app.core.scene_graph',
        'illustrator_app.ui.main_window',
        'illustrator_app.ui.canvas',
        'illustrator_app.ui.panels',
        'illustrator_app.ui.collapsible_panel',
        'illustrator_app.ai.chat_panel',
        'illustrator_app.ai.deepseek_client',
        'illustrator_app.ai.poster_generator',
        'illustrator_app.logging_config',
    ],

    hookspath=[],
    hooksconfig={},

    runtime_hooks=[],
    excludes=[
        # 排除不需要的大型模块以减小体积
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'setuptools',
        'pip',
    ],

    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    # ★ 应用名称
    name='MiniIllustrator',

    # ★ 控制台窗口默认关闭（纯 GUI 应用），调试时可改为 True
    console=False,

    # ★ 生成单文件 .exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                # 使用 UPX 压缩减小体积（需安装 upx）
    upx_exclude=[],
    runtime_tmpdir=None,
    icon=None,               # 如需图标，改为 str(PROJECT_ROOT / 'app.ico')
    target_arch=None,
)
