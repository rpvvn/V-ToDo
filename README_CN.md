# 📝 TODO 待办事项应用

<div align="center">

![Version](https://img.shields.io/badge/版本-3.2-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-orange)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Build](https://github.com/rpvvn/VV_TODO/actions/workflows/build-release.yml/badge.svg)

一个现代化、美观的桌面待办事项应用程序，使用 PyQt5 构建

[English](README.md) | 简体中文

</div>

## ✨ 主要特性

### 📋 待办管理
- ✅ 添加新的待办事项
- ✅ 标记事项为已完成/未完成
- ✅ 删除单个事项
- ✅ 一键全部标记为完成
- ✅ 清除所有已完成的事项
- 📝 支持多行文本输入

### 📅 日期功能
- 📆 弹出式日历选择器
- 🗓️ 快速选择今天
- 🔄 清除日期功能
- 📌 日期显示在事项下方

### ⚙️ 设置功能
- 🌓 深色/浅色模式切换
- 🔒 锁定窗口位置（防止拖动）
- 📌 窗口置顶功能
- 🎨 可调节窗口透明度（30%-100%）
- 🚀 开机自启动功能
- 🔄 在线检查更新（从 GitHub 获取）
- 💾 所有设置自动保存

### 🎨 现代化 UI
- 🪟 无边框圆角窗口设计
- 💳 卡片式布局
- 🌈 精美的配色方案（深色/浅色主题）
- 💫 柔和的阴影效果
- 📱 清晰的视觉层次
- 🎯 SVG 矢量图标，清晰锐利
- 📏 自适应窗口高度

### 💾 数据持久化
- 自动保存待办事项到本地 JSON 文件
- 自动保存用户设置（主题、透明度、窗口位置等）
- 重启应用后自动恢复所有数据

## 📸 界面预览

### 浅色模式
- 清新的白色背景
- 纯白色卡片设计
- 现代紫色主题色 (#7c4dff)

### 深色模式
- 护眼的深色背景
- 柔和的灰色卡片
- 同样的紫色主题色

## 🚀 快速开始

### 方法一：使用可执行文件（推荐）

1. 从 [Releases](../../releases) 下载最新版本的 `TODO待办事项.exe`
2. 双击运行
3. 开始使用！

### 方法二：从源码运行

#### 1. 克隆仓库
```bash
git clone https://github.com/yourusername/todo-app.git
cd todo-app
```

#### 2. 安装依赖
```bash
pip install -r requirements.txt
```

或者手动安装：
```bash
pip install PyQt5>=5.15.0
```

#### 3. 运行应用
```bash
python todo_app.py
```

## 📦 打包成可执行文件

### 使用 GitHub Actions 自动构建（推荐）

本项目配置了 GitHub Actions 自动构建和发布：

1. **创建新版本**：
   ```bash
   git tag v3.2
   git push origin v3.2
   ```

2. **等待自动构建**：
   - GitHub Actions 会自动构建 Windows/Linux/macOS 版本
   - 构建完成后在 [Releases](../../releases) 页面下载

3. **手动触发构建**：
   - 访问 [Actions](../../actions) 页面
   - 选择工作流并点击 "Run workflow"

详细说明请查看 [.github/RELEASE_GUIDE.md](.github/RELEASE_GUIDE.md)

### Windows 快速打包

双击运行批处理文件：
```bash
快速打包.bat
```

### 手动打包

```bash
# 1. 安装 PyInstaller
pip install pyinstaller>=5.0.0

# 2. 打包应用
pyinstaller --name=TODO待办事项 --onefile --windowed --icon=app_icon.ico --clean todo_app.py

# 3. 在 dist 文件夹中找到生成的 exe 文件
```

## 📖 使用指南

### 添加待办事项
1. 点击顶部的 ➕ 按钮打开添加面板
2. 在文本框中输入待办内容（支持多行）
3. （可选）点击"选择日期"按钮选择截止日期
4. 点击 ✓ 按钮确认添加

### 管理待办事项
- **标记完成**：点击事项左侧的复选框
- **删除事项**：点击事项右侧的删除按钮
- **全部完成**：点击底部的"全部完成"按钮
- **清除已完成**：点击底部的"删除已完成"按钮

### 日历选择
1. 在添加面板中点击"选择日期"按钮
2. 在弹出的日历中选择日期
3. 点击"今天"快速选择今天的日期
4. 点击"清除"移除已选日期
5. 点击"确定"确认选择

### 设置
点击右上角的 ⚙️ 按钮进入设置面板：

- **深色模式**：切换应用主题（深色/浅色）
- **锁定窗口位置**：启用后窗口无法拖动
- **窗口置顶**：窗口始终显示在其他窗口上方
- **窗口透明度**：拖动滑块调节透明度（30%-100%）
- **开机自启动**：系统启动时自动运行应用
- **启动时隐藏**：启动时自动隐藏到系统托盘
- **检查更新**：从 GitHub Releases 检查最新版本

### 拖动窗口
- 在顶部标题区域按住鼠标左键拖动
- 启用"锁定窗口位置"后无法拖动

## 🎨 技术特点

### 架构设计
- **模块化设计**：清晰的组件分离（TodoItem、AddTodoPanel、SettingsPanel、TodoListPanel）
- **图标管理**：独立的 IconManager 类管理所有 SVG 图标
- **主题系统**：统一的主题切换机制
- **数据持久化**：JSON 格式存储待办事项，QSettings 存储用户配置

### UI/UX 特性
- **无边框窗口**：使用 Qt.FramelessWindowHint 实现现代化外观
- **透明背景**：Qt.WA_TranslucentBackground 实现圆角窗口
- **自适应高度**：根据待办事项数量自动调整窗口高度
- **SVG 图标**：矢量图标在任何分辨率下都清晰锐利
- **平滑动画**：流畅的界面切换体验

## 📁 项目结构

```
todo-app/
├── .github/
│   ├── workflows/              # GitHub Actions 工作流
│   │   ├── build-release.yml   # Windows 快速发布
│   │   └── build-multi-platform.yml  # 多平台构建
│   ├── RELEASE_GUIDE.md        # 发布指南
│   ├── QUICK_REFERENCE.md      # 快速参考
│   └── RELEASE_TEMPLATE.md     # 发布模板
├── todo_app.py                 # 主应用程序
├── icons.py                    # 图标管理模块
├── update_checker.py           # 在线更新检查模块
├── todos.json                  # 待办事项数据（自动生成）
├── requirements.txt            # Python 依赖
├── app_icon.ico               # 应用程序图标（Windows）
├── app_icon.png               # 应用程序图标（PNG）
├── README.md                  # 英文说明文档
├── README_CN.md               # 中文说明文档
├── 快速打包.bat                # Windows 打包脚本
└── dist/                      # 打包输出目录
    └── TODO待办事项.exe        # 可执行文件
```

## 🔧 技术栈

- **Python 3.7+** - 编程语言
- **PyQt5 5.15+** - GUI 框架
- **PyInstaller 5.0+** - 打包工具

## 💡 核心功能实现

### 1. 主题系统
- 深色模式和浅色模式完整支持
- 所有组件统一的主题切换
- 主题设置持久化保存

### 2. 窗口管理
- 无边框窗口设计
- 自定义拖动区域
- 窗口位置锁定
- 窗口置顶功能
- 可调节透明度

### 3. 数据管理
- JSON 格式存储待办事项
- QSettings 存储用户配置
- 自动保存机制
- 数据恢复功能

### 4. 图标系统
- SVG 矢量图标
- 动态颜色适配
- 高清显示支持

## 🆕 版本历史

### v3.2 (当前版本)
- ✨ 添加在线更新检查功能（从 GitHub Releases 获取）
- 🔄 自动版本比较和更新通知
- 📥 直接跳转到最新版本下载页面

### v3.1
- ✨ 添加浅色/深色模式切换
- ✨ 添加全部完成和删除已完成按钮
- 🎨 优化窗口高度自适应
- 🎨 改进按钮图标显示
- 🐛 修复主题切换问题

### v3.0
- ✨ 全新现代化 UI 设计
- ✨ 无边框圆角窗口
- ✨ 卡片式布局
- ✨ SVG 矢量图标系统
- ✨ 窗口置顶功能

### v2.0
- ✨ 弹出式日历选择器
- 🔒 修复锁定窗口功能
- 🎨 改进视觉设计

## ⚠️ 注意事项

1. **首次运行**：首次运行时会在程序所在目录创建 `todos.json` 数据文件
2. **数据备份**：建议定期备份 `todos.json` 文件以防数据丢失
3. **杀毒软件**：某些杀毒软件可能误报，需要添加到白名单
4. **系统要求**：Windows 7 及以上版本，或其他支持 PyQt5 的操作系统

## 🐛 常见问题

### Q: 如何卸载应用？
A: 删除 exe 文件和 `todos.json` 文件即可。设置保存在系统注册表中，可选择性清理。

### Q: 数据保存在哪里？
A: 待办事项保存在程序目录下的 `todos.json` 文件中，用户设置保存在系统注册表中（Windows）或配置文件中（其他系统）。

### Q: 如何备份数据？
A: 复制 `todos.json` 文件即可备份所有待办事项。

### Q: 窗口无法拖动？
A: 检查是否启用了"锁定窗口位置"功能。只能在顶部标题区域拖动窗口。

### Q: 如何关闭应用？
A: 点击窗口右上角的关闭按钮，或使用 Alt+F4 快捷键。

### Q: 支持哪些操作系统？
A: 理论上支持所有能运行 PyQt5 的操作系统（Windows、macOS、Linux），但主要在 Windows 上测试。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南
1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 [Issue](../../issues)
- 发起 [Discussion](../../discussions)

## 🙏 致谢

- 感谢 [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) 提供强大的 GUI 框架
- 感谢所有贡献者和用户的支持

---

<div align="center">

**享受高效的待办管理体验！** 🎉

如果这个项目对你有帮助，请给它一个 ⭐️

</div>
