@echo off
chcp 65001 >nul
echo ========================================
echo 测试 TODO 应用
echo ========================================
echo.

echo 正在测试 Python 脚本...
python todo_app.py

if errorlevel 1 (
    echo.
    echo [错误] Python 脚本运行失败！
    echo 请查看上面的错误信息
    pause
    exit /b 1
)
