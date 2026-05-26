@echo off
chcp 65001 >nul
echo ========================================
echo TODO 待办事项 - 目录版打包
echo ========================================
echo.
echo 此版本将打包为文件夹形式
echo 更稳定，兼容性更好
echo.
pause

echo.
echo 正在关闭运行中的应用...
taskkill /F /IM "TODO待办事项.exe" >nul 2>&1
timeout /t 2 /nobreak >nul

echo.
echo 正在清理旧文件...
if exist build rmdir /s /q build 2>nul
if exist dist rmdir /s /q dist 2>nul
del /f /q *.spec 2>nul

echo.
echo 开始打包（目录模式）...
echo ========================================

pyinstaller --name=TODO待办事项 ^
    --windowed ^
    --clean ^
    --noconfirm ^
    --icon=app_icon.ico ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=PyQt5.QtSvg ^
    todo_app.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 文件位置: dist\TODO待办事项\TODO待办事项.exe
echo.
echo 说明：
echo - 整个 dist\TODO待办事项 文件夹都需要保留
echo - 运行 dist\TODO待办事项\TODO待办事项.exe
echo - 可以将整个文件夹移动到其他位置
echo.
echo 是否打开文件夹?
pause
explorer "dist\TODO待办事项"
