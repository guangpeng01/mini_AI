@echo off
:: ============================================================
::  简易 Illustrator — 一键打包脚本 (Windows)
::  
::  使用方式: 双击运行或在项目根目录命令行执行 build.bat
::  
::  前置条件:
::    1. Python 3.10+ 已安装
::    2. pip 可用
::  
::  输出:
::    dist\MiniIllustrator.exe  (单文件，约 80-120MB)
:: ============================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================================
echo   简易 Illustrator 打包工具
echo ============================================================
echo.

:: ── 检查 Python ──
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未检测到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

echo [1/4] Python 版本:
python --version
echo.

:: ── 升级 pip ──
echo [2/4] 安装/更新 PyInstaller...
python -m pip install --upgrade pip --quiet
python -m pip install pyinstaller --quiet
python -m pip install -r requirements.txt --quiet
echo    -> PyInstaller 及依赖安装完成.
echo.

:: ── 清理旧构建 ──
echo [3/4] 清理旧构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist"  rmdir /s /q "dist"
echo    -> 清理完成.
echo.

:: ── 开始打包 ──
echo [4/4] 开始打包（预计 2-5 分钟，请耐心等待）...
echo.
pyinstaller MiniIllustrator.spec --noconfirm

if errorlevel 1 (
    echo.
    echo [FAIL] 打包失败，请检查上方错误信息。
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   打包完成！
echo   输出文件: dist\MiniIllustrator.exe
echo   文件大小: 
dir "dist\MiniIllustrator.exe" 2>nul | find "MiniIllustrator.exe"
echo ============================================================
echo.
echo 使用方式:
echo   双击运行: dist\MiniIllustrator.exe
echo   或命令行: dist\MiniIllustrator.exe --api-key sk-你的KEY
echo.
pause
