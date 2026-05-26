"""
TODO 待办事项应用程序 v3.2
- 添加浅色/深色模式切换
- 添加全部完成和删除已完成按钮
- 优化窗口高度
- 改进按钮图标
- 添加系统托盘功能
- 添加开机自启动功能
- 添加在线更新检查功能
"""

import sys
import json
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QScrollArea,
    QLabel,
    QFrame,
    QSlider,
    QCheckBox,
    QLineEdit,
    QPushButton,
    QDialog,
    QGraphicsDropShadowEffect,
    QTextEdit,
    QSizePolicy,
    QSystemTrayIcon,
    QMenu,
    QAction,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QSettings, QPoint, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtSvg import QSvgRenderer
from icons import IconManager
from update_checker import UpdateChecker

# 应用版本号
APP_VERSION = "1.0"
GITHUB_REPO_OWNER = "rpvvn"
GITHUB_REPO_NAME = "V-ToDo"


class UpdateCheckThread(QThread):
    """更新检查线程"""

    update_checked = pyqtSignal(dict)  # 检查完成信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.checker = UpdateChecker(GITHUB_REPO_OWNER, GITHUB_REPO_NAME, APP_VERSION)

    def run(self):
        """执行更新检查"""
        result = self.checker.check_for_updates()
        self.update_checked.emit(result)


class ScrollDatePicker(QDialog):
    """滚动日期选择器"""

    def __init__(self, parent=None, current_date=None, is_dark_mode=True):
        super().__init__(parent)
        self.selected_date = None
        self.is_dark_mode = is_dark_mode
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.current_day = datetime.now().day

        # 解析当前日期
        if current_date:
            try:
                date_obj = datetime.strptime(current_date, "%Y-%m-%d")
                self.current_year = date_obj.year
                self.current_month = date_obj.month
                self.current_day = date_obj.day
            except:
                pass

        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("选择日期")
        self.setModal(True)
        self.setFixedSize(400, 300)

        # 设置对话框样式
        if self.is_dark_mode:
            self.setStyleSheet(
                """
                QDialog {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                    background-color: transparent;
                }
                QPushButton {
                    background-color: #7c4dff;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    background-color: #9575ff;
                }
                QScrollArea {
                    background-color: #3d3d3d;
                    border: 1px solid #555555;
                    border-radius: 8px;
                }
                QScrollArea QWidget {
                    background-color: transparent;
                }
            """
            )
        else:
            self.setStyleSheet(
                """
                QDialog {
                    background-color: #f5f5f5;
                    color: #333333;
                }
                QLabel {
                    color: #333333;
                    background-color: transparent;
                }
                QPushButton {
                    background-color: #7c4dff;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    background-color: #9575ff;
                }
                QScrollArea {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    border-radius: 8px;
                }
                QScrollArea QWidget {
                    background-color: transparent;
                }
            """
            )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题
        title_label = QLabel("选择日期", self)
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 滚动选择区域
        scroll_layout = QHBoxLayout()
        scroll_layout.setSpacing(10)

        # 年份选择
        year_container = QVBoxLayout()
        year_label = QLabel("年", self)
        year_label.setFont(QFont("Microsoft YaHei", 10))
        year_label.setAlignment(Qt.AlignCenter)
        year_container.addWidget(year_label)

        self.year_scroll = self.create_scroll_area()
        self.year_scroll.setFixedSize(80, 120)
        year_widget = QWidget()
        year_layout = QVBoxLayout(year_widget)
        year_layout.setSpacing(0)
        year_layout.setContentsMargins(0, 0, 0, 0)

        # 添加年份选项（当前年份前后10年）
        self.year_buttons = []
        for year in range(self.current_year - 10, self.current_year + 11):
            btn = self.create_date_button(str(year), year == self.current_year)
            btn.clicked.connect(lambda checked, y=year: self.select_year(y))
            self.year_buttons.append(btn)
            year_layout.addWidget(btn)

        self.year_scroll.setWidget(year_widget)
        year_container.addWidget(self.year_scroll)
        scroll_layout.addLayout(year_container)

        # 月份选择
        month_container = QVBoxLayout()
        month_label = QLabel("月", self)
        month_label.setFont(QFont("Microsoft YaHei", 10))
        month_label.setAlignment(Qt.AlignCenter)
        month_container.addWidget(month_label)

        self.month_scroll = self.create_scroll_area()
        self.month_scroll.setFixedSize(80, 120)
        month_widget = QWidget()
        month_layout = QVBoxLayout(month_widget)
        month_layout.setSpacing(0)
        month_layout.setContentsMargins(0, 0, 0, 0)

        # 添加月份选项
        self.month_buttons = []
        for month in range(1, 13):
            btn = self.create_date_button(f"{month:02d}", month == self.current_month)
            btn.clicked.connect(lambda checked, m=month: self.select_month(m))
            self.month_buttons.append(btn)
            month_layout.addWidget(btn)

        self.month_scroll.setWidget(month_widget)
        month_container.addWidget(self.month_scroll)
        scroll_layout.addLayout(month_container)

        # 日期选择
        day_container = QVBoxLayout()
        day_label = QLabel("日", self)
        day_label.setFont(QFont("Microsoft YaHei", 10))
        day_label.setAlignment(Qt.AlignCenter)
        day_container.addWidget(day_label)

        self.day_scroll = self.create_scroll_area()
        self.day_scroll.setFixedSize(80, 120)
        self.update_days()
        day_container.addWidget(self.day_scroll)
        scroll_layout.addLayout(day_container)

        layout.addLayout(scroll_layout)

        # 当前选择显示
        self.current_selection = QLabel(self)
        self.current_selection.setFont(QFont("Microsoft YaHei", 12))
        self.current_selection.setAlignment(Qt.AlignCenter)
        self.update_selection_display()
        layout.addWidget(self.current_selection)

        # 按钮区域
        btn_layout = QHBoxLayout()

        today_btn = QPushButton("今天", self)
        today_btn.clicked.connect(self.select_today)
        btn_layout.addWidget(today_btn)

        clear_btn = QPushButton("清除", self)
        clear_btn.clicked.connect(self.clear_date)
        btn_layout.addWidget(clear_btn)

        btn_layout.addStretch()

        ok_btn = QPushButton("确定", self)
        ok_btn.clicked.connect(self.accept_date)
        btn_layout.addWidget(ok_btn)

        cancel_btn = QPushButton("取消", self)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    def create_scroll_area(self):
        """创建滚动区域"""
        scroll = QScrollArea(self)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        return scroll

    def create_date_button(self, text, selected=False):
        """创建日期按钮"""
        btn = QPushButton(text, self)
        btn.setFixedHeight(30)
        btn.setFont(QFont("Microsoft YaHei", 10))

        if self.is_dark_mode:
            if selected:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #7c4dff;
                        color: #ffffff;
                        border: none;
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #9575ff;
                    }
                """
                )
            else:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: transparent;
                        color: #ffffff;
                        border: none;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #4d4d4d;
                    }
                """
                )
        else:
            if selected:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #7c4dff;
                        color: #ffffff;
                        border: none;
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #9575ff;
                    }
                """
                )
            else:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: transparent;
                        color: #333333;
                        border: none;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;
                    }
                """
                )

        return btn

    def select_year(self, year):
        """选择年份"""
        self.current_year = year
        # 计算正确的按钮索引
        base_year = datetime.now().year - 10  # 基准年份
        year_index = year - base_year
        if 0 <= year_index < len(self.year_buttons):
            self.update_button_selection(self.year_buttons, year_index)
        self.update_days()
        self.update_selection_display()

    def select_month(self, month):
        """选择月份"""
        self.current_month = month
        self.update_button_selection(self.month_buttons, month - 1)
        self.update_days()
        self.update_selection_display()

    def select_day(self, day):
        """选择日期"""
        self.current_day = day
        self.update_button_selection(self.day_buttons, day - 1)
        self.update_selection_display()

    def update_button_selection(self, buttons, selected_index):
        """更新按钮选择状态"""
        for i, btn in enumerate(buttons):
            if i == selected_index:
                if self.is_dark_mode:
                    btn.setStyleSheet(
                        """
                        QPushButton {
                            background-color: #7c4dff;
                            color: #ffffff;
                            border: none;
                            border-radius: 4px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #9575ff;
                        }
                    """
                    )
                else:
                    btn.setStyleSheet(
                        """
                        QPushButton {
                            background-color: #7c4dff;
                            color: #ffffff;
                            border: none;
                            border-radius: 4px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #9575ff;
                        }
                    """
                    )
            else:
                if self.is_dark_mode:
                    btn.setStyleSheet(
                        """
                        QPushButton {
                            background-color: transparent;
                            color: #ffffff;
                            border: none;
                            border-radius: 4px;
                        }
                        QPushButton:hover {
                            background-color: #4d4d4d;
                        }
                    """
                    )
                else:
                    btn.setStyleSheet(
                        """
                        QPushButton {
                            background-color: transparent;
                            color: #333333;
                            border: none;
                            border-radius: 4px;
                        }
                        QPushButton:hover {
                            background-color: #f0f0f0;
                        }
                    """
                    )

    def update_days(self):
        """更新日期选项"""
        # 计算当月天数
        import calendar

        days_in_month = calendar.monthrange(self.current_year, self.current_month)[1]

        # 确保当前选择的日期不超过当月天数
        if self.current_day > days_in_month:
            self.current_day = days_in_month

        day_widget = QWidget()
        day_layout = QVBoxLayout(day_widget)
        day_layout.setSpacing(0)
        day_layout.setContentsMargins(0, 0, 0, 0)

        self.day_buttons = []
        for day in range(1, days_in_month + 1):
            btn = self.create_date_button(f"{day:02d}", day == self.current_day)
            btn.clicked.connect(lambda checked, d=day: self.select_day(d))
            self.day_buttons.append(btn)
            day_layout.addWidget(btn)

        self.day_scroll.setWidget(day_widget)

    def update_selection_display(self):
        """更新选择显示"""
        date_str = (
            f"{self.current_year}-{self.current_month:02d}-{self.current_day:02d}"
        )
        self.current_selection.setText(f"选择的日期: {date_str}")

    def select_today(self):
        """选择今天"""
        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        self.current_day = today.day

        # 更新所有按钮状态
        base_year = today.year - 10  # 基准年份
        year_index = self.current_year - base_year
        if 0 <= year_index < len(self.year_buttons):
            self.update_button_selection(self.year_buttons, year_index)

        self.update_button_selection(self.month_buttons, self.current_month - 1)
        self.update_days()
        self.update_selection_display()

    def clear_date(self):
        """清除日期"""
        self.selected_date = ""
        self.accept()

    def accept_date(self):
        """确认日期"""
        self.selected_date = (
            f"{self.current_year}-{self.current_month:02d}-{self.current_day:02d}"
        )
        self.accept()


class TodoItem(QWidget):
    """单个待办事项组件"""

    def __init__(
        self, parent, text, date="", completed=False, item_id=None, is_dark_mode=True
    ):
        super().__init__(parent)
        self.item_id = item_id or datetime.now().timestamp()
        self.completed = completed
        self.text_content = text
        self.date_content = date
        self.is_dark_mode = is_dark_mode

        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        self.setFixedHeight(75)  # 增加5px高度以适应两行文字

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)

        # 完成状态复选框 - 使用更大的尺寸
        self.checkbox = QCheckBox(self)
        self.checkbox.setChecked(self.completed)
        self.checkbox.stateChanged.connect(self.on_state_changed)
        # 不设置固定大小，让样式表控制
        layout.addWidget(self.checkbox)

        # 文本内容
        content_layout = QVBoxLayout()
        content_layout.setSpacing(2)

        self.text_label = QLabel(self)
        self.text_label.setText(self.text_content)
        self.text_label.setFont(QFont("Microsoft YaHei", 11))
        # 启用文本换行，设置最大宽度
        self.text_label.setWordWrap(True)
        self.text_label.setMaximumWidth(200)  # 限制文本宽度，确保不会过宽
        content_layout.addWidget(self.text_label)

        if self.date_content:
            self.date_label = QLabel(self)
            self.date_label.setText(f"📅 {self.date_content}")
            self.date_label.setFont(QFont("Microsoft YaHei", 9))
            content_layout.addWidget(self.date_label)

        layout.addLayout(content_layout, 1)

        # 状态显示区域（红框位置）
        self.status_label = QLabel(self)
        self.status_label.setFont(QFont("Microsoft YaHei", 9))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFixedSize(120, 40)
        self.status_label.setStyleSheet(
            """
            QLabel {
                border-radius: 8px;
                padding: 5px;
            }
        """
        )
        layout.addWidget(self.status_label)

        self.update_status_display()
        self.update_style()

    def calculate_date_status(self):
        """计算日期状态"""
        if not self.date_content:
            return "无日期", "normal"

        try:
            # 解析日期
            target_date = datetime.strptime(self.date_content, "%Y-%m-%d").date()
            today = datetime.now().date()

            # 计算天数差
            days_diff = (target_date - today).days

            if days_diff < 0:
                # 已过期
                return f"已过期 {abs(days_diff)} 天", "expired"
            elif days_diff == 0:
                # 今天
                return "今天到期", "today"
            elif days_diff <= 3:
                # 即将到期（3天内）
                return f"剩余 {days_diff} 天", "warning"
            else:
                # 正常
                return f"剩余 {days_diff} 天", "normal"
        except:
            return "日期错误", "error"

    def update_status_display(self):
        """更新状态显示"""
        status_text, status_type = self.calculate_date_status()
        self.status_label.setText(status_text)

        # 根据状态类型设置颜色
        if self.is_dark_mode:
            if status_type == "expired":
                # 已过期 - 红色
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        background-color: #ff5252;
                        color: #ffffff;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """
                )
            elif status_type == "today":
                # 今天到期 - 橙色
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        background-color: #ff9800;
                        color: #ffffff;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """
                )
            elif status_type == "warning":
                # 即将到期 - 黄色
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        background-color: #ffc107;
                        color: #333333;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """
                )
            elif status_type == "normal":
                # 正常 - 绿色
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        background-color: #4caf50;
                        color: #ffffff;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """
                )
            else:
                # 无日期或错误 - 灰色
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        background-color: #666666;
                        color: #ffffff;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """
                )
        else:
            # 浅色模式
            if status_type == "expired":
                # 已过期 - 红色
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        background-color: #f44336;
                        color: #ffffff;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """
                )
            elif status_type == "today":
                # 今天到期 - 橙色
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        background-color: #ff9800;
                        color: #ffffff;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """
                )
            elif status_type == "warning":
                # 即将到期 - 黄色
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        background-color: #ffeb3b;
                        color: #333333;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """
                )
            elif status_type == "normal":
                # 正常 - 绿色
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        background-color: #4caf50;
                        color: #ffffff;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """
                )
            else:
                # 无日期或错误 - 灰色
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        background-color: #9e9e9e;
                        color: #ffffff;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """
                )

    def on_state_changed(self, state):
        """复选框状态改变"""
        self.completed = state == Qt.Checked
        self.update_style()
        if hasattr(self.parent(), "save_todos"):
            self.parent().save_todos()
        if hasattr(self.parent(), "update_title"):
            self.parent().update_title()

    def update_style(self):
        """更新样式"""
        if self.is_dark_mode:
            # 复选框样式 - 深色模式，使用更大更明显的样式
            checkbox_style = """
                QCheckBox {
                    spacing: 5px;
                }
                QCheckBox::indicator {
                    width: 22px;
                    height: 22px;
                    border-radius: 5px;
                    border: 2px solid #7c4dff;
                    background-color: #2d2d2d;
                }
                QCheckBox::indicator:hover {
                    border: 2px solid #9575ff;
                    background-color: #3d3d3d;
                }
                QCheckBox::indicator:checked {
                    background-color: #7c4dff;
                    border: 2px solid #7c4dff;
                    image: none;
                }
            """
            self.checkbox.setStyleSheet(checkbox_style)

            if self.completed:
                self.text_label.setStyleSheet(
                    "text-decoration: line-through; color: #666666; background-color: transparent;"
                )
                if hasattr(self, "date_label"):
                    self.date_label.setStyleSheet(
                        "color: #666666; text-decoration: line-through; background-color: transparent;"
                    )
            else:
                self.text_label.setStyleSheet(
                    "color: #ffffff; background-color: transparent;"
                )
                if hasattr(self, "date_label"):
                    self.date_label.setStyleSheet(
                        "color: #999999; background-color: transparent;"
                    )
        else:
            # 复选框样式 - 浅色模式
            checkbox_style = """
                QCheckBox {
                    spacing: 5px;
                }
                QCheckBox::indicator {
                    width: 22px;
                    height: 22px;
                    border-radius: 5px;
                    border: 2px solid #00bfa5;
                    background-color: #ffffff;
                }
                QCheckBox::indicator:hover {
                    border: 2px solid #00d4b8;
                    background-color: #f0f0f0;
                }
                QCheckBox::indicator:checked {
                    background-color: #00bfa5;
                    border: 2px solid #00bfa5;
                    image: none;
                }
            """
            self.checkbox.setStyleSheet(checkbox_style)

            if self.completed:
                self.text_label.setStyleSheet(
                    "text-decoration: line-through; color: #999999; background-color: transparent;"
                )
                if hasattr(self, "date_label"):
                    self.date_label.setStyleSheet(
                        "color: #999999; text-decoration: line-through; background-color: transparent;"
                    )
            else:
                self.text_label.setStyleSheet(
                    "color: #333333; background-color: transparent;"
                )
                if hasattr(self, "date_label"):
                    self.date_label.setStyleSheet(
                        "color: #666666; background-color: transparent;"
                    )

        # 更新状态显示
        if hasattr(self, "status_label"):
            self.update_status_display()

    def set_theme(self, is_dark_mode):
        """设置主题"""
        self.is_dark_mode = is_dark_mode
        self.update_style()

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.item_id,
            "text": self.text_content,
            "date": self.date_content,
            "completed": self.completed,
        }


class AddTodoPanel(QWidget):
    """添加待办面板"""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.selected_date = ""
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题栏
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)

        self.title = QLabel("添加新待办", self)
        self.title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title_layout.addWidget(self.title)

        title_layout.addStretch()

        # 确认按钮
        self.confirm_btn = QPushButton("✓", self)
        self.confirm_btn.setFixedSize(40, 40)
        self.confirm_btn.clicked.connect(self.confirm_add)
        title_layout.addWidget(self.confirm_btn)

        # 取消按钮
        self.cancel_btn = QPushButton("✕", self)
        self.cancel_btn.setFixedSize(40, 40)
        self.cancel_btn.clicked.connect(self.cancel_add)
        title_layout.addWidget(self.cancel_btn)

        layout.addLayout(title_layout)

        # 提示文字
        self.hint = QLabel("请输入待办内容", self)
        self.hint.setFont(QFont("Microsoft YaHei", 10))
        layout.addWidget(self.hint)

        # 输入框
        self.input_field = QTextEdit(self)
        self.input_field.setPlaceholderText("输入待办内容...")
        self.input_field.setFont(QFont("Microsoft YaHei", 11))
        self.input_field.setFixedHeight(120)
        layout.addWidget(self.input_field)

        # 添加更大的分隔间距，让日期选择区域向下移动
        layout.addSpacing(45)

        # 日期选择区域
        self.date_container = QWidget(self)
        self.date_container.setFixedHeight(50)  # 固定高度确保稳定显示
        date_layout = QHBoxLayout(self.date_container)
        date_layout.setContentsMargins(0, 10, 0, 10)
        date_layout.setSpacing(15)

        self.date_display = QLabel("未设置日期", self)
        self.date_display.setFont(QFont("Microsoft YaHei", 10))
        date_layout.addWidget(self.date_display)

        date_layout.addStretch()

        self.select_date_btn = QPushButton("选择日期", self)
        self.select_date_btn.setFixedHeight(30)
        self.select_date_btn.clicked.connect(self.select_date)
        date_layout.addWidget(self.select_date_btn)

        layout.addWidget(self.date_container)
        layout.addStretch()

    def select_date(self):
        """选择日期"""
        dialog = ScrollDatePicker(
            self, self.selected_date, self.main_window.is_dark_mode
        )
        if dialog.exec_() == QDialog.Accepted:
            self.selected_date = dialog.selected_date
            if self.selected_date:
                self.date_display.setText(f"📅 {self.selected_date}")
            else:
                self.date_display.setText("未设置日期")

    def confirm_add(self):
        """确认添加"""
        text = self.input_field.toPlainText().strip()
        if text:
            self.main_window.add_todo(text, self.selected_date)
            self.input_field.clear()
            self.selected_date = ""
            self.date_display.setText("未设置日期")
            self.main_window.toggle_add_panel()

    def cancel_add(self):
        """取消添加"""
        self.input_field.clear()
        self.selected_date = ""
        self.date_display.setText("未设置日期")
        self.main_window.toggle_add_panel()

    def apply_theme(self, is_dark_mode):
        """应用主题"""
        if is_dark_mode:
            self.setStyleSheet("background-color: transparent;")
            self.title.setStyleSheet("color: #ffffff; background-color: transparent;")
            self.hint.setStyleSheet("color: #7c4dff; background-color: transparent;")
            self.date_display.setStyleSheet(
                "color: #999999; background-color: transparent; padding: 5px;"
            )
            # 日期容器样式
            self.date_container.setStyleSheet(
                """
                QWidget {
                    background-color: transparent;
                    border: none;
                }
                """
            )
            self.input_field.setStyleSheet(
                """
                QTextEdit {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: 1px solid #3d3d3d;
                    border-radius: 8px;
                    padding: 10px;
                }
            """
            )
            self.confirm_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #4caf50;
                    color: #ffffff;
                    border: none;
                    border-radius: 20px;
                    font-size: 16pt;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #66bb6a;
                }
            """
            )
            self.cancel_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #f44336;
                    color: #ffffff;
                    border: none;
                    border-radius: 20px;
                    font-size: 16pt;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ef5350;
                }
            """
            )
            self.select_date_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #7c4dff;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    background-color: #9575ff;
                }
            """
            )
        else:
            self.setStyleSheet("background-color: transparent;")
            self.title.setStyleSheet("color: #333333; background-color: transparent;")
            self.hint.setStyleSheet("color: #7c4dff; background-color: transparent;")
            self.date_display.setStyleSheet(
                "color: #666666; background-color: transparent; padding: 5px;"
            )
            # 日期容器样式
            self.date_container.setStyleSheet(
                """
                QWidget {
                    background-color: transparent;
                    border: none;
                }
                """
            )
            self.input_field.setStyleSheet(
                """
                QTextEdit {
                    background-color: #ffffff;
                    color: #333333;
                    border: 1px solid #dddddd;
                    border-radius: 8px;
                    padding: 10px;
                }
            """
            )
            self.confirm_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #4caf50;
                    color: #ffffff;
                    border: none;
                    border-radius: 20px;
                    font-size: 16pt;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #66bb6a;
                }
            """
            )
            self.cancel_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #f44336;
                    color: #ffffff;
                    border: none;
                    border-radius: 20px;
                    font-size: 16pt;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ef5350;
                }
            """
            )
            self.select_date_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #7c4dff;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    background-color: #9575ff;
                }
            """
            )


class SettingsPanel(QWidget):
    """设置面板"""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # 标题
        self.title = QLabel("设置", self)
        self.title.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        layout.addWidget(self.title)
        layout.addSpacing(15)

        # 深色模式
        dark_mode_section = QHBoxLayout()
        dark_mode_section.setSpacing(15)

        # 左侧文字区域
        dark_mode_text = QVBoxLayout()
        dark_mode_text.setSpacing(5)

        self.dark_mode_title = QLabel("深色模式", self)
        self.dark_mode_title.setFont(QFont("Microsoft YaHei", 11))
        dark_mode_text.addWidget(self.dark_mode_title)

        self.dark_mode_desc = QLabel("在深色主题的计算机上提供更佳的视觉效果", self)
        self.dark_mode_desc.setFont(QFont("Microsoft YaHei", 9))
        self.dark_mode_desc.setWordWrap(True)
        dark_mode_text.addWidget(self.dark_mode_desc)

        dark_mode_section.addLayout(dark_mode_text, 1)

        # 右侧复选框
        self.dark_mode_checkbox = QCheckBox(self)
        self.dark_mode_checkbox.setChecked(self.main_window.is_dark_mode)
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        dark_mode_section.addWidget(
            self.dark_mode_checkbox, 0, Qt.AlignRight | Qt.AlignVCenter
        )

        layout.addLayout(dark_mode_section)
        layout.addSpacing(10)

        # 锁定位置
        lock_section = QHBoxLayout()
        lock_section.setSpacing(15)

        # 左侧文字区域
        lock_text = QVBoxLayout()
        lock_text.setSpacing(5)

        self.lock_title = QLabel("锁定位置", self)
        self.lock_title.setFont(QFont("Microsoft YaHei", 11))
        lock_text.addWidget(self.lock_title)

        self.lock_desc = QLabel("阻止拖动窗口以保持位置不变", self)
        self.lock_desc.setFont(QFont("Microsoft YaHei", 9))
        self.lock_desc.setWordWrap(True)
        lock_text.addWidget(self.lock_desc)

        lock_section.addLayout(lock_text, 1)

        # 右侧复选框
        self.lock_checkbox = QCheckBox(self)
        self.lock_checkbox.setChecked(self.main_window.is_locked)
        self.lock_checkbox.stateChanged.connect(self.toggle_lock)
        lock_section.addWidget(self.lock_checkbox, 0, Qt.AlignRight | Qt.AlignVCenter)

        layout.addLayout(lock_section)
        layout.addSpacing(10)

        # 窗口置顶
        stay_on_top_section = QHBoxLayout()
        stay_on_top_section.setSpacing(15)

        # 左侧文字区域
        stay_on_top_text = QVBoxLayout()
        stay_on_top_text.setSpacing(5)

        self.stay_on_top_title = QLabel("窗口置顶", self)
        self.stay_on_top_title.setFont(QFont("Microsoft YaHei", 11))
        stay_on_top_text.addWidget(self.stay_on_top_title)

        self.stay_on_top_desc = QLabel("窗口始终显示在其他窗口上方", self)
        self.stay_on_top_desc.setFont(QFont("Microsoft YaHei", 9))
        self.stay_on_top_desc.setWordWrap(True)
        stay_on_top_text.addWidget(self.stay_on_top_desc)

        stay_on_top_section.addLayout(stay_on_top_text, 1)

        # 右侧复选框
        self.stay_on_top_checkbox = QCheckBox(self)
        self.stay_on_top_checkbox.setChecked(self.main_window.stay_on_top)
        self.stay_on_top_checkbox.stateChanged.connect(self.toggle_stay_on_top)
        stay_on_top_section.addWidget(
            self.stay_on_top_checkbox, 0, Qt.AlignRight | Qt.AlignVCenter
        )

        layout.addLayout(stay_on_top_section)
        layout.addSpacing(10)

        # 启动时隐藏
        start_hidden_section = QHBoxLayout()
        start_hidden_section.setSpacing(15)

        # 左侧文字区域
        start_hidden_text = QVBoxLayout()
        start_hidden_text.setSpacing(5)

        self.start_hidden_title = QLabel("启动时隐藏", self)
        self.start_hidden_title.setFont(QFont("Microsoft YaHei", 11))
        start_hidden_text.addWidget(self.start_hidden_title)

        self.start_hidden_desc = QLabel("启动时自动隐藏到系统托盘", self)
        self.start_hidden_desc.setFont(QFont("Microsoft YaHei", 9))
        self.start_hidden_desc.setWordWrap(True)
        start_hidden_text.addWidget(self.start_hidden_desc)

        start_hidden_section.addLayout(start_hidden_text, 1)

        # 右侧复选框
        self.start_hidden_checkbox = QCheckBox(self)
        start_hidden = self.main_window.settings.value("start_hidden", False, type=bool)
        self.start_hidden_checkbox.setChecked(start_hidden)
        self.start_hidden_checkbox.stateChanged.connect(self.toggle_start_hidden)
        start_hidden_section.addWidget(
            self.start_hidden_checkbox, 0, Qt.AlignRight | Qt.AlignVCenter
        )

        layout.addLayout(start_hidden_section)
        layout.addSpacing(10)

        # 开机自启动
        autostart_section = QHBoxLayout()
        autostart_section.setSpacing(15)

        # 左侧文字区域
        autostart_text = QVBoxLayout()
        autostart_text.setSpacing(5)

        self.autostart_title = QLabel("开机自启动", self)
        self.autostart_title.setFont(QFont("Microsoft YaHei", 11))
        autostart_text.addWidget(self.autostart_title)

        self.autostart_desc = QLabel("开机时自动启动应用程序", self)
        self.autostart_desc.setFont(QFont("Microsoft YaHei", 9))
        self.autostart_desc.setWordWrap(True)
        autostart_text.addWidget(self.autostart_desc)

        autostart_section.addLayout(autostart_text, 1)

        # 右侧复选框
        self.autostart_checkbox = QCheckBox(self)
        self.autostart_checkbox.setChecked(self.check_autostart())
        self.autostart_checkbox.stateChanged.connect(self.toggle_autostart)
        autostart_section.addWidget(
            self.autostart_checkbox, 0, Qt.AlignRight | Qt.AlignVCenter
        )

        layout.addLayout(autostart_section)
        layout.addSpacing(10)

        # 透明度
        opacity_section = QVBoxLayout()
        opacity_section.setSpacing(5)

        self.opacity_title = QLabel("窗口透明度", self)
        self.opacity_title.setFont(QFont("Microsoft YaHei", 11))
        opacity_section.addWidget(self.opacity_title)

        self.opacity_slider = QSlider(Qt.Horizontal, self)
        self.opacity_slider.setMinimum(30)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(int(self.main_window.opacity * 100))
        self.opacity_slider.valueChanged.connect(self.change_opacity)
        opacity_section.addWidget(self.opacity_slider)

        self.opacity_value_label = QLabel(
            f"{int(self.main_window.opacity * 100)}%", self
        )
        self.opacity_value_label.setFont(QFont("Microsoft YaHei", 10))
        self.opacity_value_label.setAlignment(Qt.AlignCenter)
        opacity_section.addWidget(self.opacity_value_label)

        layout.addLayout(opacity_section)
        layout.addSpacing(15)

        # 更新检查部分
        update_section = QHBoxLayout()
        update_section.setSpacing(15)

        # 左侧文字区域
        update_text = QVBoxLayout()
        update_text.setSpacing(5)

        self.update_title = QLabel("检查更新", self)
        self.update_title.setFont(QFont("Microsoft YaHei", 11))
        update_text.addWidget(self.update_title)

        self.update_status = QLabel(f"当前版本: v{APP_VERSION}", self)
        self.update_status.setFont(QFont("Microsoft YaHei", 9))
        self.update_status.setWordWrap(True)
        update_text.addWidget(self.update_status)

        update_section.addLayout(update_text, 1)

        # 右侧按钮
        self.check_update_btn = QPushButton("检查更新", self)
        self.check_update_btn.setFont(QFont("Microsoft YaHei", 9))
        self.check_update_btn.setCursor(Qt.PointingHandCursor)
        self.check_update_btn.setFixedSize(100, 44)
        self.check_update_btn.clicked.connect(self.check_for_updates)
        update_section.addWidget(
            self.check_update_btn, 0, Qt.AlignRight | Qt.AlignVCenter
        )

        layout.addLayout(update_section)
        layout.addSpacing(10)

        # GitHub 链接部分
        github_section = QHBoxLayout()
        github_section.setSpacing(15)

        # 左侧文字区域
        github_text = QVBoxLayout()
        github_text.setSpacing(5)

        self.github_title = QLabel("GitHub 项目", self)
        self.github_title.setFont(QFont("Microsoft YaHei", 11))
        github_text.addWidget(self.github_title)

        self.github_desc = QLabel("喜欢这个项目？给个 Star 吧！", self)
        self.github_desc.setFont(QFont("Microsoft YaHei", 9))
        self.github_desc.setWordWrap(True)
        github_text.addWidget(self.github_desc)

        github_section.addLayout(github_text, 1)

        # 右侧按钮
        self.github_btn = QPushButton("⭐ 前往 GitHub", self)
        self.github_btn.setFont(QFont("Microsoft YaHei", 9))
        self.github_btn.setCursor(Qt.PointingHandCursor)
        self.github_btn.setFixedSize(120, 44)
        self.github_btn.clicked.connect(self.open_github)
        github_section.addWidget(self.github_btn, 0, Qt.AlignRight | Qt.AlignVCenter)

        layout.addLayout(github_section)
        layout.addSpacing(10)

        # 关于信息
        self.about_label = QLabel("基于 PyQt5 编写", self)
        self.about_label.setFont(QFont("Microsoft YaHei", 9))
        self.about_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.about_label)

        layout.addStretch()

    def toggle_dark_mode(self, state):
        """切换深色模式"""
        self.main_window.toggle_dark_mode(state == Qt.Checked)

    def toggle_lock(self, state):
        """切换锁定状态"""
        self.main_window.toggle_lock(state == Qt.Checked)

    def toggle_stay_on_top(self, state):
        """切换窗口置顶"""
        self.main_window.toggle_stay_on_top(state == Qt.Checked)

    def toggle_start_hidden(self, state):
        """切换启动时隐藏"""
        enabled = state == Qt.Checked
        self.main_window.settings.setValue("start_hidden", enabled)

    def check_autostart(self):
        """检查是否已设置开机自启动"""
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ,
            )
            try:
                winreg.QueryValueEx(key, "VV_TODO")
                winreg.CloseKey(key)
                return True
            except WindowsError:
                winreg.CloseKey(key)
                return False
        except:
            return False

    def toggle_autostart(self, state):
        """切换开机自启动"""
        enabled = state == Qt.Checked

        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE,
            )

            if enabled:
                # 获取当前程序路径
                if getattr(sys, "frozen", False):
                    # 打包后的 exe 路径
                    app_path = sys.executable
                else:
                    # 开发环境路径
                    app_path = os.path.abspath(sys.argv[0])

                # 添加到启动项
                winreg.SetValueEx(key, "VV_TODO", 0, winreg.REG_SZ, f'"{app_path}"')

                # 显示成功消息
                self.show_message(
                    "设置成功", "开机自启动已启用\n应用将在系统启动时自动运行", "info"
                )
            else:
                # 从启动项移除
                try:
                    winreg.DeleteValue(key, "VV_TODO")

                    # 显示成功消息
                    self.show_message("设置成功", "开机自启动已禁用", "info")
                except WindowsError:
                    pass

            winreg.CloseKey(key)

        except Exception as e:
            # 显示错误消息
            self.show_message(
                "设置失败", f"无法设置开机自启动\n错误: {str(e)}", "warning"
            )
            # 恢复复选框状态
            self.autostart_checkbox.setChecked(not enabled)

    def show_message(self, title, message, msg_type="info"):
        """显示带样式的消息框"""
        from PyQt5.QtWidgets import QMessageBox

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        if msg_type == "info":
            msg_box.setIcon(QMessageBox.Information)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Warning)
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Critical)

        # 应用样式
        if self.main_window.is_dark_mode:
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QMessageBox QLabel {
                    color: #ffffff;
                    background-color: transparent;
                    min-width: 300px;
                }
                QMessageBox QPushButton {
                    background-color: #7c4dff;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 20px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #9575ff;
                }
            """
            )
        else:
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: #ffffff;
                    color: #333333;
                }
                QMessageBox QLabel {
                    color: #333333;
                    background-color: transparent;
                    min-width: 300px;
                }
                QMessageBox QPushButton {
                    background-color: #00bfa5;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 20px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #00d4b8;
                }
            """
            )

        msg_box.exec_()

    def change_opacity(self, value):
        """改变透明度"""
        opacity = value / 100.0
        self.main_window.set_opacity(opacity)
        self.opacity_value_label.setText(f"{value}%")

    def open_github(self):
        """打开 GitHub 页面"""
        import webbrowser

        webbrowser.open("https://github.com/rpvvn/V-ToDo")

    def check_for_updates(self):
        """检查更新"""
        # 禁用按钮，防止重复点击
        self.check_update_btn.setEnabled(False)
        self.check_update_btn.setText("检查中...")

        # 创建并启动更新检查线程
        self.update_thread = UpdateCheckThread(self)
        self.update_thread.update_checked.connect(self.on_update_checked)
        self.update_thread.start()

    def on_update_checked(self, result):
        """更新检查完成"""
        # 恢复按钮状态
        self.check_update_btn.setEnabled(True)
        self.check_update_btn.setText("检查更新")

        if result["error"]:
            # 显示错误信息
            self.update_status.setText(f"检查失败: {result['error']}")
            self.show_message("检查更新失败", result["error"], "warning")
        elif result["has_update"]:
            # 有新版本
            self.update_status.setText(
                f"发现新版本: v{result['latest_version']}\n当前版本: v{result['current_version']}"
            )
            self.show_update_dialog(result)
        else:
            # 已是最新版本
            self.update_status.setText(
                f"当前已是最新版本: v{result['current_version']}"
            )
            self.show_message(
                "检查更新",
                f"当前已是最新版本 v{result['current_version']}",
                "info",
            )

    def show_update_dialog(self, update_info):
        """显示更新对话框"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("发现新版本")

        # 构建消息文本
        message = f"发现新版本: v{update_info['latest_version']}\n"
        message += f"当前版本: v{update_info['current_version']}\n\n"

        if update_info["published_at"]:
            # 格式化发布时间
            try:
                from datetime import datetime

                pub_date = datetime.strptime(
                    update_info["published_at"], "%Y-%m-%dT%H:%M:%SZ"
                )
                message += f"发布时间: {pub_date.strftime('%Y-%m-%d %H:%M')}\n\n"
            except:
                pass

        if update_info["release_notes"]:
            # 截取更新说明（最多显示前300个字符）
            notes = update_info["release_notes"]
            if len(notes) > 300:
                notes = notes[:300] + "..."
            message += f"更新说明:\n{notes}\n\n"

        message += "是否前往下载页面？"

        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)

        # 应用样式
        if self.main_window.is_dark_mode:
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QMessageBox QLabel {
                    color: #ffffff;
                    background-color: transparent;
                    min-width: 400px;
                }
                QMessageBox QPushButton {
                    background-color: #7c4dff;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 20px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #9575ff;
                }
            """
            )
        else:
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: #ffffff;
                    color: #333333;
                }
                QMessageBox QLabel {
                    color: #333333;
                    background-color: transparent;
                    min-width: 400px;
                }
                QMessageBox QPushButton {
                    background-color: #00bfa5;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 20px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #00d4b8;
                }
            """
            )

        # 显示对话框
        if msg_box.exec_() == QMessageBox.Yes:
            # 打开下载页面
            import webbrowser

            webbrowser.open(update_info["download_url"])

    def apply_theme(self, is_dark_mode):
        """应用主题"""
        if is_dark_mode:
            self.setStyleSheet("background-color: transparent;")
            self.title.setStyleSheet("color: #ffffff; background-color: transparent;")
            self.dark_mode_title.setStyleSheet(
                "color: #ffffff; background-color: transparent;"
            )
            self.dark_mode_desc.setStyleSheet(
                "color: #999999; background-color: transparent;"
            )
            self.lock_title.setStyleSheet(
                "color: #ffffff; background-color: transparent;"
            )
            self.lock_desc.setStyleSheet(
                "color: #999999; background-color: transparent;"
            )
            self.stay_on_top_title.setStyleSheet(
                "color: #ffffff; background-color: transparent;"
            )
            self.stay_on_top_desc.setStyleSheet(
                "color: #999999; background-color: transparent;"
            )
            self.start_hidden_title.setStyleSheet(
                "color: #ffffff; background-color: transparent;"
            )
            self.start_hidden_desc.setStyleSheet(
                "color: #999999; background-color: transparent;"
            )
            self.autostart_title.setStyleSheet(
                "color: #ffffff; background-color: transparent;"
            )
            self.autostart_desc.setStyleSheet(
                "color: #999999; background-color: transparent;"
            )
            self.opacity_title.setStyleSheet(
                "color: #ffffff; background-color: transparent;"
            )
            self.opacity_value_label.setStyleSheet(
                "color: #999999; background-color: transparent;"
            )
            self.update_title.setStyleSheet(
                "color: #ffffff; background-color: transparent;"
            )
            self.update_status.setStyleSheet(
                "color: #999999; background-color: transparent;"
            )
            self.check_update_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #7c4dff;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background-color: #9575ff;
                }
                QPushButton:disabled {
                    background-color: #3d3d3d;
                    color: #666666;
                }
            """
            )
            self.github_desc.setStyleSheet(
                "color: #999999; background-color: transparent;"
            )
            self.github_title.setStyleSheet(
                "color: #ffffff; background-color: transparent;"
            )
            self.github_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #7c4dff;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background-color: #9575ff;
                }
            """
            )
            self.about_label.setStyleSheet(
                "color: #666666; background-color: transparent;"
            )

            checkbox_style = """
                QCheckBox {
                    spacing: 10px;
                }
                QCheckBox::indicator {
                    width: 50px;
                    height: 26px;
                    border-radius: 13px;
                    background-color: #3d3d3d;
                    border: 2px solid #3d3d3d;
                }
                QCheckBox::indicator:checked {
                    background-color: #7c4dff;
                    border: 2px solid #7c4dff;
                }
                QCheckBox::indicator:hover {
                    background-color: #4d4d4d;
                }
                QCheckBox::indicator:checked:hover {
                    background-color: #9575ff;
                    border: 2px solid #9575ff;
                }
            """
            self.dark_mode_checkbox.setStyleSheet(checkbox_style)
            self.lock_checkbox.setStyleSheet(checkbox_style)
            self.stay_on_top_checkbox.setStyleSheet(checkbox_style)
            self.start_hidden_checkbox.setStyleSheet(checkbox_style)
            self.autostart_checkbox.setStyleSheet(checkbox_style)

            self.opacity_slider.setStyleSheet(
                """
                QSlider::groove:horizontal {
                    border: none;
                    height: 6px;
                    background: #3d3d3d;
                    border-radius: 3px;
                }
                QSlider::handle:horizontal {
                    background: #7c4dff;
                    border: none;
                    width: 18px;
                    height: 18px;
                    margin: -6px 0;
                    border-radius: 9px;
                }
                QSlider::handle:horizontal:hover {
                    background: #9575ff;
                }
            """
            )
        else:
            self.setStyleSheet("background-color: transparent;")
            self.title.setStyleSheet("color: #333333; background-color: transparent;")
            self.dark_mode_title.setStyleSheet(
                "color: #333333; background-color: transparent;"
            )
            self.dark_mode_desc.setStyleSheet(
                "color: #666666; background-color: transparent;"
            )
            self.lock_title.setStyleSheet(
                "color: #333333; background-color: transparent;"
            )
            self.lock_desc.setStyleSheet(
                "color: #666666; background-color: transparent;"
            )
            self.stay_on_top_title.setStyleSheet(
                "color: #333333; background-color: transparent;"
            )
            self.stay_on_top_desc.setStyleSheet(
                "color: #666666; background-color: transparent;"
            )
            self.start_hidden_title.setStyleSheet(
                "color: #333333; background-color: transparent;"
            )
            self.start_hidden_desc.setStyleSheet(
                "color: #666666; background-color: transparent;"
            )
            self.autostart_title.setStyleSheet(
                "color: #333333; background-color: transparent;"
            )
            self.autostart_desc.setStyleSheet(
                "color: #666666; background-color: transparent;"
            )
            self.opacity_title.setStyleSheet(
                "color: #333333; background-color: transparent;"
            )
            self.opacity_value_label.setStyleSheet(
                "color: #666666; background-color: transparent;"
            )
            self.update_title.setStyleSheet(
                "color: #333333; background-color: transparent;"
            )
            self.update_status.setStyleSheet(
                "color: #666666; background-color: transparent;"
            )
            self.check_update_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #00bfa5;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background-color: #00d4b8;
                }
                QPushButton:disabled {
                    background-color: #dddddd;
                    color: #999999;
                }
            """
            )
            self.github_desc.setStyleSheet(
                "color: #666666; background-color: transparent;"
            )
            self.github_title.setStyleSheet(
                "color: #333333; background-color: transparent;"
            )
            self.github_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #00bfa5;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background-color: #00d4b8;
                }
            """
            )
            self.about_label.setStyleSheet(
                "color: #999999; background-color: transparent;"
            )

            checkbox_style = """
                QCheckBox {
                    spacing: 10px;
                }
                QCheckBox::indicator {
                    width: 50px;
                    height: 26px;
                    border-radius: 13px;
                    background-color: #dddddd;
                    border: 2px solid #dddddd;
                }
                QCheckBox::indicator:checked {
                    background-color: #00bfa5;
                    border: 2px solid #00bfa5;
                }
                QCheckBox::indicator:hover {
                    background-color: #cccccc;
                }
                QCheckBox::indicator:checked:hover {
                    background-color: #00d4b8;
                    border: 2px solid #00d4b8;
                }
            """
            self.dark_mode_checkbox.setStyleSheet(checkbox_style)
            self.lock_checkbox.setStyleSheet(checkbox_style)
            self.stay_on_top_checkbox.setStyleSheet(checkbox_style)
            self.start_hidden_checkbox.setStyleSheet(checkbox_style)
            self.autostart_checkbox.setStyleSheet(checkbox_style)

            self.opacity_slider.setStyleSheet(
                """
                QSlider::groove:horizontal {
                    border: none;
                    height: 6px;
                    background: #dddddd;
                    border-radius: 3px;
                }
                QSlider::handle:horizontal {
                    background: #00bfa5;
                    border: none;
                    width: 18px;
                    height: 18px;
                    margin: -6px 0;
                    border-radius: 9px;
                }
                QSlider::handle:horizontal:hover {
                    background: #00d4b8;
                }
            """
            )


class TodoListPanel(QWidget):
    """待办事项列表面板"""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.todo_items = []
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 分类标题
        self.category_container = QWidget(self)
        self.category_container.setFixedHeight(60)

        category_layout = QHBoxLayout(self.category_container)
        category_layout.setContentsMargins(20, 0, 20, 0)

        self.category_label = QLabel("全部待办", self)
        self.category_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        category_layout.addWidget(self.category_label)

        category_layout.addStretch()

        layout.addWidget(self.category_container)
        layout.addSpacing(10)

        # 待办事项容器 - 移除滚动区域，直接使用垂直布局
        self.todo_container = QWidget(self)
        self.todo_container.setStyleSheet("background-color: transparent;")
        self.todo_layout = QVBoxLayout(self.todo_container)
        self.todo_layout.setContentsMargins(0, 0, 0, 0)
        self.todo_layout.setSpacing(2)
        # 添加顶部对齐，确保待办事项从上方开始显示
        self.todo_layout.setAlignment(Qt.AlignTop)

        layout.addWidget(self.todo_container, 1)  # 添加stretch factor

        # 底部按钮区域
        self.bottom_buttons = QWidget(self)
        self.bottom_buttons.setFixedHeight(60)

        bottom_layout = QHBoxLayout(self.bottom_buttons)
        bottom_layout.setContentsMargins(15, 10, 15, 10)
        bottom_layout.setSpacing(10)

        bottom_layout.addStretch()

        # 全部完成按钮 - 使用SVG图标
        self.complete_all_btn = QPushButton(self)
        self.complete_all_btn.setFixedSize(40, 40)
        self.complete_all_btn.setToolTip("全部完成")
        self.complete_all_btn.clicked.connect(self.complete_all)
        bottom_layout.addWidget(self.complete_all_btn)

        # 删除已完成按钮 - 使用SVG图标
        self.clear_completed_btn = QPushButton(self)
        self.clear_completed_btn.setFixedSize(40, 40)
        self.clear_completed_btn.setToolTip("删除已完成")
        self.clear_completed_btn.clicked.connect(self.clear_completed)
        bottom_layout.addWidget(self.clear_completed_btn)

        layout.addWidget(self.bottom_buttons)

    def complete_all(self):
        """全部标记为完成"""
        for item in self.todo_items:
            if not item.completed:
                item.checkbox.setChecked(True)
        self.save_todos()

    def clear_completed(self):
        """清除已完成的事项"""
        items_to_remove = [item for item in self.todo_items if item.completed]
        for item in items_to_remove:
            self.remove_todo(item)
        # 调整窗口高度
        if hasattr(self.main_window, "adjust_window_height"):
            self.main_window.adjust_window_height()

    def add_todo_item(self, text, date=""):
        """添加待办事项"""
        todo_item = TodoItem(
            self.todo_container, text, date, False, None, self.main_window.is_dark_mode
        )
        self.todo_items.append(todo_item)

        # 直接添加到布局中
        self.todo_layout.addWidget(todo_item)

        # 更新标题
        self.update_title()

        # 保存
        self.save_todos()

        # 调整窗口高度
        if hasattr(self.main_window, "adjust_window_height"):
            self.main_window.adjust_window_height()

    def remove_todo(self, todo_item):
        """移除待办事项"""
        if todo_item in self.todo_items:
            self.todo_items.remove(todo_item)
            self.todo_layout.removeWidget(todo_item)
            todo_item.deleteLater()
            self.update_title()
            self.save_todos()
            # 调整窗口高度
            if hasattr(self.main_window, "adjust_window_height"):
                self.main_window.adjust_window_height()

    def update_title(self):
        """更新标题显示待办数量"""
        count = len([item for item in self.todo_items if not item.completed])
        self.main_window.update_todo_count(count)

    def save_todos(self):
        """保存待办事项到文件"""
        data = [item.to_dict() for item in self.todo_items]
        try:
            with open("todos.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存失败: {e}")

    def load_todos(self):
        """从文件加载待办事项"""
        try:
            with open("todos.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for item_data in data:
                    todo_item = TodoItem(
                        self.todo_container,
                        item_data.get("text", ""),
                        item_data.get("date", ""),
                        item_data.get("completed", False),
                        item_data.get("id"),
                        self.main_window.is_dark_mode,
                    )
                    self.todo_items.append(todo_item)
                    self.todo_layout.addWidget(todo_item)
                self.update_title()
                # 加载完成后调整窗口高度
                if hasattr(self.main_window, "adjust_window_height"):
                    self.main_window.adjust_window_height()
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"加载失败: {e}")

    def apply_theme(self, is_dark_mode):
        """应用主题"""
        if is_dark_mode:
            self.category_container.setStyleSheet(
                "background-color: #2d2d2d; border-radius: 12px;"
            )
            self.category_label.setStyleSheet(
                "color: #ffffff; background-color: transparent;"
            )
            self.bottom_buttons.setStyleSheet("background-color: transparent;")

            # 设置按钮图标（深色模式）
            self.complete_all_btn.setIcon(IconManager.get_complete_icon("#ffffff", 24))
            self.clear_completed_btn.setIcon(IconManager.get_clear_icon("#ffffff", 24))

            btn_style = """
                QPushButton {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: none;
                    border-radius: 20px;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                }
            """
            self.complete_all_btn.setStyleSheet(btn_style)
            self.clear_completed_btn.setStyleSheet(btn_style)
            self.complete_all_btn.setIconSize(self.complete_all_btn.size())
            self.clear_completed_btn.setIconSize(self.clear_completed_btn.size())

            # 设置滚动区域背景透明
            self.setStyleSheet("background-color: transparent;")
        else:
            self.category_container.setStyleSheet(
                "background-color: #ffffff; border-radius: 12px;"
            )
            self.category_label.setStyleSheet(
                "color: #333333; background-color: transparent;"
            )
            self.bottom_buttons.setStyleSheet("background-color: transparent;")

            # 设置按钮图标（浅色模式）
            self.complete_all_btn.setIcon(IconManager.get_complete_icon("#333333", 24))
            self.clear_completed_btn.setIcon(IconManager.get_clear_icon("#333333", 24))

            btn_style = """
                QPushButton {
                    background-color: #ffffff;
                    color: #333333;
                    border: 1px solid #dddddd;
                    border-radius: 20px;
                }
                QPushButton:hover {
                    background-color: #f5f5f5;
                }
            """
            self.complete_all_btn.setStyleSheet(btn_style)
            self.clear_completed_btn.setStyleSheet(btn_style)
            self.complete_all_btn.setIconSize(self.complete_all_btn.size())
            self.clear_completed_btn.setIconSize(self.clear_completed_btn.size())

            # 设置滚动区域背景透明
            self.setStyleSheet("background-color: transparent;")

        # 更新所有待办事项的主题
        for item in self.todo_items:
            item.set_theme(is_dark_mode)


class TodoApp(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()

        # 设置
        self.settings = QSettings("TodoApp", "Settings")
        self.is_dark_mode = self.settings.value("dark_mode", True, type=bool)
        self.is_locked = self.settings.value("locked", False, type=bool)
        self.stay_on_top = self.settings.value("stay_on_top", False, type=bool)
        self.opacity = self.settings.value("opacity", 0.95, type=float)
        self.dragging = False

        # 面板显示状态
        self.add_panel_visible = False
        self.settings_panel_visible = False

        self.setup_window()
        self.setup_ui()
        self.load_settings()
        self.apply_theme()

    def setup_window(self):
        """设置窗口"""
        self.setWindowTitle("TODO 待办事项")
        # 初始窗口大小 - 会根据内容自动调整（增加宽度以适应设置面板）
        self.setGeometry(100, 100, 360, 140)
        # 设置最小宽度，防止文字折叠（缩减宽度到85%）
        self.setMinimumWidth(360)

        # 设置窗口标志 - 无边框，背景透明，工具窗口（不显示在任务栏）
        flags = Qt.FramelessWindowHint | Qt.Tool
        if self.stay_on_top:
            flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置应用程序图标
        try:
            app_icon = IconManager.get_app_icon(256)
            self.setWindowIcon(app_icon)
        except Exception as e:
            print(f"设置图标失败: {e}")

        # 设置透明度
        self.setWindowOpacity(self.opacity)

        # 创建系统托盘图标
        self.create_tray_icon()

    def setup_ui(self):
        """设置UI"""
        # 中心部件
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet("background-color: transparent;")
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)  # 标题栏和内容区域之间的间隔

        # 顶部栏
        self.create_top_bar()

        # 内容区域容器
        self.content_container = QWidget(self.central_widget)
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(15, 10, 15, 15)
        self.content_layout.setSpacing(10)

        # 创建面板
        self.add_panel = AddTodoPanel(self.content_container, self)
        self.add_panel.hide()

        self.settings_panel = SettingsPanel(self.content_container, self)
        self.settings_panel.hide()

        self.todo_panel = TodoListPanel(self.content_container, self)

        self.content_layout.addWidget(self.add_panel)
        self.content_layout.addWidget(self.settings_panel)
        self.content_layout.addWidget(self.todo_panel, 1)

        self.main_layout.addWidget(self.content_container, 1)

        # 加载待办事项
        self.todo_panel.load_todos()

        # 初始调整窗口大小
        self.adjust_window_height()

    def create_tray_icon(self):
        """创建系统托盘图标"""
        # 创建托盘图标
        try:
            tray_icon = IconManager.get_app_icon(64)
        except:
            # 如果获取图标失败，使用默认图标
            tray_icon = self.style().standardIcon(self.style().SP_ComputerIcon)

        self.tray_icon = QSystemTrayIcon(tray_icon, self)

        # 创建托盘菜单
        tray_menu = QMenu()

        # 显示/隐藏窗口
        self.show_action = QAction("显示窗口", self)
        self.show_action.triggered.connect(self.toggle_window)
        tray_menu.addAction(self.show_action)

        tray_menu.addSeparator()

        # 快速添加待办
        add_action = QAction("➕ 添加待办", self)
        add_action.triggered.connect(self.quick_add_todo)
        tray_menu.addAction(add_action)

        tray_menu.addSeparator()

        # 设置
        settings_action = QAction("⚙️ 设置", self)
        settings_action.triggered.connect(self.show_settings)
        tray_menu.addAction(settings_action)

        tray_menu.addSeparator()

        # 退出
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

        # 双击托盘图标显示/隐藏窗口
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # 显示托盘图标
        self.tray_icon.show()

        # 显示托盘消息
        self.tray_icon.showMessage(
            "TODO 待办事项",
            "应用已在后台运行，双击托盘图标显示窗口",
            QSystemTrayIcon.Information,
            2000,
        )

    def tray_icon_activated(self, reason):
        """托盘图标被激活"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_window()

    def toggle_window(self):
        """显示/隐藏窗口"""
        if self.isVisible():
            self.hide()
            self.show_action.setText("显示窗口")
        else:
            self.show()
            self.activateWindow()
            self.show_action.setText("隐藏窗口")

    def quick_add_todo(self):
        """快速添加待办"""
        self.show()
        self.activateWindow()
        self.toggle_add_panel()

    def show_settings(self):
        """显示设置"""
        self.show()
        self.activateWindow()
        if not self.settings_panel_visible:
            self.toggle_settings_panel()

    def quit_application(self):
        """退出应用程序"""
        # 保存设置
        self.settings.setValue("window_pos", self.pos())
        self.settings.setValue("window_size", self.size())

        # 隐藏托盘图标
        self.tray_icon.hide()

        # 退出应用
        QApplication.quit()

    def create_top_bar(self):
        """创建顶部栏"""
        self.top_bar = QWidget(self.central_widget)
        self.top_bar.setFixedHeight(70)

        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(15)

        # 应用图标
        self.app_icon_label = QLabel(self)
        try:
            icon_pixmap = IconManager.get_app_icon(32).pixmap(32, 32)
            self.app_icon_label.setPixmap(icon_pixmap)
        except:
            self.app_icon_label.setText("📋")
            self.app_icon_label.setFont(QFont("Segoe UI Emoji", 20))
        self.app_icon_label.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.app_icon_label)

        # 待办数量
        self.todo_count_label = QLabel("0个待办事项", self)
        self.todo_count_label.setFont(QFont("Microsoft YaHei", 13))
        layout.addWidget(self.todo_count_label)

        layout.addStretch()

        # 添加按钮 - 使用SVG图标
        self.add_btn = QPushButton(self)
        self.add_btn.setFixedSize(40, 40)
        self.add_btn.clicked.connect(self.toggle_add_panel)
        layout.addWidget(self.add_btn)

        # 菜单按钮 - 使用SVG图标
        self.menu_btn = QPushButton(self)
        self.menu_btn.setFixedSize(40, 40)
        self.menu_btn.clicked.connect(self.toggle_settings_panel)
        layout.addWidget(self.menu_btn)

        self.main_layout.addWidget(self.top_bar)

    def update_todo_count(self, count):
        """更新待办数量显示"""
        self.todo_count_label.setText(f"{count}个待办事项")

    def toggle_add_panel(self):
        """切换添加面板"""
        if self.add_panel_visible:
            self.add_panel.hide()
            self.todo_panel.show()
            self.add_panel_visible = False
        else:
            self.add_panel.show()
            self.todo_panel.hide()
            self.settings_panel.hide()
            self.add_panel_visible = True
            self.settings_panel_visible = False
            self.add_panel.input_field.setFocus()
        self.adjust_window_height()

    def toggle_settings_panel(self):
        """切换设置面板"""
        if self.settings_panel_visible:
            self.settings_panel.hide()
            self.todo_panel.show()
            self.settings_panel_visible = False
        else:
            self.settings_panel.show()
            self.todo_panel.hide()
            self.add_panel.hide()
            self.settings_panel_visible = True
            self.add_panel_visible = False
        self.adjust_window_height()

    def add_todo(self, text, date):
        """添加待办事项"""
        self.todo_panel.add_todo_item(text, date)
        self.adjust_window_height()

    def adjust_window_height(self):
        """根据待办事项数量自动调整窗口高度"""
        # 固定高度部分
        top_bar_height = 70
        spacing = 10  # 标题栏和内容区域之间的间隔

        # 根据显示的面板计算内容高度
        if self.add_panel_visible:
            # 添加面板固定高度 - 调整高度以适应增加的间距
            # 标题栏: 60, 提示文字: 30, 输入框: 120, 间距: 25, 日期选择: 50, 底部间距: 25
            content_height = 320
        elif self.settings_panel_visible:
            # 设置面板 - 根据内容动态计算高度
            # 标题 + 间距: 约 60
            # 5个设置项（每个约 70）: 350
            # 透明度滑块: 80
            # 检查更新区域: 70 (改为水平布局)
            # GitHub区域: 70 (改为水平布局)
            # 关于信息: 40
            # 各种间距: 约 100
            content_height = 50 + 300 + 80 + 70 + 70 + 50 + 90
            # 总计约 710
        else:
            # 待办列表面板 - 根据实际项目数量动态计算（无最大限制）
            category_height = 60
            bottom_buttons_height = 60
            item_height = 77  # 每个待办项的高度（75 + 2间隔）

            todo_count = len(self.todo_panel.todo_items)

            # 至少显示3个项目的空间，但不设置最大限制
            min_items = 3
            display_items = max(min_items, todo_count)

            items_height = display_items * item_height
            content_height = category_height + items_height + bottom_buttons_height + 30

        # 计算总高度
        total_height = top_bar_height + spacing + content_height

        # 设置窗口大小 - 保持最小宽度（增加到480以适应状态显示）
        self.setFixedHeight(total_height)
        if self.width() < 480:
            self.setFixedWidth(480)
        else:
            self.setFixedWidth(self.width())

    def toggle_dark_mode(self, enabled):
        """切换深色模式"""
        self.is_dark_mode = enabled
        self.settings.setValue("dark_mode", enabled)
        self.apply_theme()

    def apply_theme(self):
        """应用主题"""
        if self.is_dark_mode:
            # 深色主题
            self.setStyleSheet("background-color: transparent;")

            # 顶部栏样式 - 独立圆角
            self.top_bar.setStyleSheet(
                """
                QWidget {
                    background-color: #2d2d2d;
                    border-radius: 16px;
                }
                """
            )

            # 内容区域样式 - 独立圆角
            self.content_container.setStyleSheet(
                """
                QWidget {
                    background-color: #1a1a1a;
                    border-radius: 16px;
                }
                """
            )

            self.todo_count_label.setStyleSheet(
                "color: #ffffff; background-color: transparent;"
            )

            # 设置按钮图标（深色模式）
            self.add_btn.setIcon(IconManager.get_add_icon("#ffffff", 24))
            self.menu_btn.setIcon(IconManager.get_settings_icon("#ffffff", 24))

            btn_style = """
                QPushButton {
                    background-color: transparent;
                    color: #ffffff;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                    border-radius: 20px;
                }
            """
            self.add_btn.setStyleSheet(btn_style)
            self.menu_btn.setStyleSheet(btn_style)
            self.add_btn.setIconSize(self.add_btn.size())
            self.menu_btn.setIconSize(self.menu_btn.size())
        else:
            # 浅色主题
            self.setStyleSheet("background-color: transparent;")

            # 顶部栏样式 - 独立圆角
            self.top_bar.setStyleSheet(
                """
                QWidget {
                    background-color: #ffffff;
                    border-radius: 16px;
                }
                """
            )

            # 内容区域样式 - 独立圆角
            self.content_container.setStyleSheet(
                """
                QWidget {
                    background-color: #f5f5f5;
                    border-radius: 16px;
                }
                """
            )

            self.todo_count_label.setStyleSheet(
                "color: #333333; background-color: transparent;"
            )

            # 设置按钮图标（浅色模式）
            self.add_btn.setIcon(IconManager.get_add_icon("#333333", 24))
            self.menu_btn.setIcon(IconManager.get_settings_icon("#333333", 24))

            btn_style = """
                QPushButton {
                    background-color: transparent;
                    color: #333333;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border-radius: 20px;
                }
            """
            self.add_btn.setStyleSheet(btn_style)
            self.menu_btn.setStyleSheet(btn_style)
            self.add_btn.setIconSize(self.add_btn.size())
            self.menu_btn.setIconSize(self.menu_btn.size())

        # 应用主题到各个面板
        self.add_panel.apply_theme(self.is_dark_mode)
        self.settings_panel.apply_theme(self.is_dark_mode)
        self.todo_panel.apply_theme(self.is_dark_mode)

    def toggle_lock(self, enabled):
        """切换锁定状态"""
        self.is_locked = enabled
        self.settings.setValue("locked", enabled)

    def toggle_stay_on_top(self, enabled):
        """切换窗口置顶"""
        self.stay_on_top = enabled
        self.settings.setValue("stay_on_top", enabled)

        # 更新窗口标志
        flags = Qt.FramelessWindowHint | Qt.Tool
        if enabled:
            flags |= Qt.WindowStaysOnTopHint

        # 保存当前位置
        pos = self.pos()

        # 重新设置窗口标志
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 恢复位置并显示
        self.move(pos)
        self.show()

    def set_opacity(self, opacity):
        """设置透明度"""
        self.opacity = opacity
        self.setWindowOpacity(opacity)
        self.settings.setValue("opacity", opacity)

    def load_settings(self):
        """加载设置"""
        # 恢复窗口位置
        pos = self.settings.value("window_pos")
        if pos:
            self.move(pos)

        size = self.settings.value("window_size")
        if size:
            self.resize(size)

    def closeEvent(self, event):
        """关闭事件 - 最小化到托盘而不是退出"""
        if self.tray_icon.isVisible():
            # 隐藏窗口到托盘
            event.ignore()
            self.hide()
            self.show_action.setText("显示窗口")

            # 首次最小化时显示提示
            if not hasattr(self, "_tray_tip_shown"):
                self.tray_icon.showMessage(
                    "TODO 待办事项",
                    "应用已最小化到托盘，双击托盘图标可重新打开",
                    QSystemTrayIcon.Information,
                    2000,
                )
                self._tray_tip_shown = True
        else:
            # 保存窗口位置和大小
            self.settings.setValue("window_pos", self.pos())
            self.settings.setValue("window_size", self.size())
            event.accept()

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if not self.is_locked and event.button() == Qt.LeftButton:
            # 只在顶部栏区域允许拖动
            if event.pos().y() < 70:
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                self.dragging = True
                event.accept()
            else:
                self.dragging = False
        else:
            self.dragging = False

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if not self.is_locked and self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        self.dragging = False


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 设置应用信息
    app.setApplicationName("TODO 待办事项")
    app.setOrganizationName("TodoApp")

    # 创建主窗口
    window = TodoApp()

    # 检查是否启动时隐藏
    start_hidden = window.settings.value("start_hidden", False, type=bool)
    if start_hidden:
        # 如果设置了启动时隐藏，则不显示窗口
        window.hide()
    else:
        # 默认显示窗口
        window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
