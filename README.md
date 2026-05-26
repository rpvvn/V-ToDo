# 📝 TODO Application

<div align="center">

![Version](https://img.shields.io/badge/version-3.2-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-orange)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Build](https://github.com/rpvvn/VV_TODO/actions/workflows/build-release.yml/badge.svg)

A modern and beautiful desktop TODO application built with PyQt5

English | [简体中文](README_CN.md)

</div>

## ✨ Key Features

### 📋 Task Management
- ✅ Add new TODO items
- ✅ Mark items as completed/uncompleted
- ✅ Delete individual items
- ✅ Mark all items as completed with one click
- ✅ Clear all completed items
- 📝 Multi-line text input support

### 📅 Date Features
- 📆 Pop-up calendar picker
- 🗓️ Quick select today
- 🔄 Clear date functionality
- 📌 Date display below items

### ⚙️ Settings
- 🌓 Dark/Light mode toggle
- 🔒 Lock window position (prevent dragging)
- 📌 Always on top functionality
- 🎨 Adjustable window opacity (30%-100%)
- 🚀 Auto-start on system boot
- 🔄 Online update checking from GitHub
- 💾 Auto-save all settings

### 🎨 Modern UI
- 🪟 Frameless rounded window design
- 💳 Card-based layout
- 🌈 Beautiful color schemes (dark/light themes)
- 💫 Smooth shadow effects
- 📱 Clear visual hierarchy
- 🎯 SVG vector icons for crisp display
- 📏 Adaptive window height

### 💾 Data Persistence
- Auto-save TODO items to local JSON file
- Auto-save user settings (theme, opacity, window position, etc.)
- Automatic data recovery on restart

## 📸 Screenshots

### Light Mode
- Fresh white background
- Pure white card design
- Modern purple theme color (#7c4dff)

### Dark Mode
- Eye-friendly dark background
- Soft gray cards
- Same purple theme color

## 🚀 Quick Start

### Method 1: Use Executable (Recommended)

1. Download the latest `TODO待办事项.exe` from [Releases](../../releases)
2. Double-click to run
3. Start using!

### Method 2: Run from Source

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/todo-app.git
cd todo-app
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install PyQt5>=5.15.0
```

#### 3. Run Application
```bash
python todo_app.py
```

## 📦 Build Executable

### Automated Build with GitHub Actions (Recommended)

This project uses GitHub Actions for automated building and releasing:

1. **Create a new release**:
   ```bash
   git tag v3.2
   git push origin v3.2
   ```

2. **Wait for automatic build**:
   - GitHub Actions will automatically build Windows/Linux/macOS versions
   - Download from [Releases](../../releases) page when complete

3. **Manual trigger**:
   - Visit [Actions](../../actions) page
   - Select workflow and click "Run workflow"

See [.github/RELEASE_GUIDE.md](.github/RELEASE_GUIDE.md) for detailed instructions.

### Windows Quick Build

Double-click the batch file:
```bash
快速打包.bat
```

### Manual Build

```bash
# 1. Install PyInstaller
pip install pyinstaller>=5.0.0

# 2. Build application
pyinstaller --name=TODO待办事项 --onefile --windowed --icon=app_icon.ico --clean todo_app.py

# 3. Find the exe file in the dist folder
```

## 📖 User Guide

### Adding TODO Items
1. Click the ➕ button at the top to open the add panel
2. Enter TODO content in the text box (multi-line supported)
3. (Optional) Click "选择日期" button to select a due date
4. Click ✓ button to confirm

### Managing TODO Items
- **Mark Complete**: Click the checkbox on the left of the item
- **Delete Item**: Click the delete button on the right of the item
- **Complete All**: Click the "全部完成" button at the bottom
- **Clear Completed**: Click the "删除已完成" button at the bottom

### Calendar Selection
1. Click "选择日期" button in the add panel
2. Select a date in the pop-up calendar
3. Click "今天" to quickly select today
4. Click "清除" to remove the selected date
5. Click "确定" to confirm selection

### Settings
Click the ⚙️ button at the top right to enter settings panel:

- **Dark Mode**: Toggle application theme (dark/light)
- **Lock Window Position**: Window cannot be dragged when enabled
- **Always on Top**: Window stays above other windows
- **Window Opacity**: Drag slider to adjust opacity (30%-100%)
- **Auto-start on Boot**: Automatically start the application when system boots
- **Start Hidden**: Hide to system tray on startup
- **Check for Updates**: Check for the latest version from GitHub releases

### Dragging Window
- Hold left mouse button in the top title area to drag
- Cannot drag when "Lock Window Position" is enabled

## 🎨 Technical Highlights

### Architecture Design
- **Modular Design**: Clear component separation (TodoItem, AddTodoPanel, SettingsPanel, TodoListPanel)
- **Icon Management**: Dedicated IconManager class for all SVG icons
- **Theme System**: Unified theme switching mechanism
- **Data Persistence**: JSON format for TODO items, QSettings for user configuration

### UI/UX Features
- **Frameless Window**: Modern appearance using Qt.FramelessWindowHint
- **Transparent Background**: Rounded window using Qt.WA_TranslucentBackground
- **Adaptive Height**: Auto-adjust window height based on number of TODO items
- **SVG Icons**: Vector icons stay crisp at any resolution
- **Smooth Animations**: Fluid interface transitions

## 📁 Project Structure

```
todo-app/
├── .github/
│   ├── workflows/              # GitHub Actions workflows
│   │   ├── build-release.yml   # Windows quick release
│   │   └── build-multi-platform.yml  # Multi-platform build
│   ├── RELEASE_GUIDE.md        # Release guide
│   ├── QUICK_REFERENCE.md      # Quick reference
│   └── RELEASE_TEMPLATE.md     # Release template
├── todo_app.py                 # Main application
├── icons.py                    # Icon management module
├── update_checker.py           # Online update checker
├── todos.json                  # TODO items data (auto-generated)
├── requirements.txt            # Python dependencies
├── app_icon.ico               # Application icon (Windows)
├── app_icon.png               # Application icon (PNG)
├── README.md                  # English documentation
├── README_CN.md               # Chinese documentation
├── 快速打包.bat                # Windows build script
└── dist/                      # Build output directory
    └── TODO待办事项.exe        # Executable file
```

## 🔧 Tech Stack

- **Python 3.7+** - Programming language
- **PyQt5 5.15+** - GUI framework
- **PyInstaller 5.0+** - Packaging tool

## 💡 Core Implementation

### 1. Theme System
- Full support for dark and light modes
- Unified theme switching for all components
- Persistent theme settings

### 2. Window Management
- Frameless window design
- Custom drag area
- Window position locking
- Always on top functionality
- Adjustable opacity

### 3. Data Management
- JSON format for TODO items storage
- QSettings for user configuration
- Auto-save mechanism
- Data recovery functionality

### 4. Icon System
- SVG vector icons
- Dynamic color adaptation
- High-DPI display support

## 🆕 Version History

### v3.2 (Current)
- ✨ Added online update checking from GitHub releases
- 🔄 Automatic version comparison and update notifications
- 📥 Direct download links to latest releases

### v3.1
- ✨ Added light/dark mode toggle
- ✨ Added complete all and clear completed buttons
- 🎨 Optimized adaptive window height
- 🎨 Improved button icon display
- 🐛 Fixed theme switching issues

### v3.0
- ✨ Brand new modern UI design
- ✨ Frameless rounded window
- ✨ Card-based layout
- ✨ SVG vector icon system
- ✨ Always on top functionality

### v2.0
- ✨ Pop-up calendar picker
- 🔒 Fixed window locking functionality
- 🎨 Improved visual design

## ⚠️ Notes

1. **First Run**: Creates `todos.json` data file in program directory on first run
2. **Data Backup**: Recommend regularly backing up `todos.json` file to prevent data loss
3. **Antivirus Software**: Some antivirus software may flag as false positive, add to whitelist if needed
4. **System Requirements**: Windows 7 or higher, or other OS that supports PyQt5

## 🐛 FAQ

### Q: How to uninstall the application?
A: Delete the exe file and `todos.json` file. Settings are saved in system registry (Windows) and can be optionally cleaned.

### Q: Where is data saved?
A: TODO items are saved in `todos.json` file in the program directory. User settings are saved in system registry (Windows) or configuration files (other systems).

### Q: How to backup data?
A: Copy the `todos.json` file to backup all TODO items.

### Q: Cannot drag window?
A: Check if "Lock Window Position" is enabled. Window can only be dragged in the top title area.

### Q: How to close the application?
A: Click the close button at the top right corner, or use Alt+F4 shortcut.

### Q: Which operating systems are supported?
A: Theoretically supports all OS that can run PyQt5 (Windows, macOS, Linux), but primarily tested on Windows.

## 🤝 Contributing

Issues and Pull Requests are welcome!

### Contribution Guidelines
1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 📞 Contact

For questions or suggestions, feel free to contact via:

- Submit an [Issue](../../issues)
- Start a [Discussion](../../discussions)

## 🙏 Acknowledgments

- Thanks to [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the powerful GUI framework
- Thanks to all contributors and users for their support

---

<div align="center">

**Enjoy efficient TODO management!** 🎉

If this project helps you, please give it a ⭐️

</div>
