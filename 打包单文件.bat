@echo off
chcp 65001 >nul
echo ========================================
echo TODO 待办事项 - 单文件打包工具
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python！
    echo 请先安装 Python 3.7 或更高版本
    pause
    exit /b 1
)

echo [1/5] 检查依赖...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [警告] PyQt5 未安装，正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败！
        pause
        exit /b 1
    )
)

python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [警告] PyInstaller 未安装，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller 安装失败！
        pause
        exit /b 1
    )
)

echo [2/5] 清理旧的打包文件...
if exist "dist\TODO待办事项.exe" (
    del /f /q "dist\TODO待办事项.exe"
    echo 已删除旧的 exe 文件
)
if exist "build" (
    rmdir /s /q "build"
    echo 已删除 build 目录
)

echo [3/5] 开始打包为单个 EXE 文件...
echo 这可能需要几分钟时间，请耐心等待...
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "TODO待办事项" ^
    --icon "app_icon.ico" ^
    --hidden-import "PyQt5.QtCore" ^
    --hidden-import "PyQt5.QtGui" ^
    --hidden-import "PyQt5.QtWidgets" ^
    --hidden-import "PyQt5.QtSvg" ^
    --add-data "icons.py;." ^
    --noconfirm ^
    todo_app.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    echo 请查看上面的错误信息
    pause
    exit /b 1
)

echo.
echo [4/5] 验证打包结果...
if exist "dist\TODO待办事项.exe" (
    echo ✓ 打包成功！
    echo.
    echo [5/5] 打包信息：
    echo ----------------------------------------
    echo 输出文件: dist\TODO待办事项.exe
    for %%A in ("dist\TODO待办事项.exe") do echo 文件大小: %%~zA 字节
    echo 打包类型: 单文件 (onefile)
    echo ----------------------------------------
    echo.
    echo 提示：
    echo - 可执行文件位于 dist 目录
    echo - 这是一个独立的 exe 文件，可以直接运行
    echo - 首次运行可能需要几秒钟解压临时文件
    echo.
) else (
    echo [错误] 未找到打包后的 exe 文件！
    pause
    exit /b 1
)

echo 是否立即运行打包后的程序？(Y/N)
set /p choice=请选择: 
if /i "%choice%"=="Y" (
    echo.
    echo 正在启动程序...
    start "" "dist\TODO待办事项.exe"
)

echo.
echo 打包完成！
pause
