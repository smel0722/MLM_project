from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QFileDialog, QMessageBox, QCheckBox, 
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from functions.MainTab_functions import MainTabFunctions
from settings_handler import SettingsHandler

class MainTab(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.functions = MainTabFunctions()
        self.settings_handler = SettingsHandler()  # 新增
        self.main_window = parent  # 新增
        self.initUI()
        self.load_settings()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 設定整體樣式
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QPushButton {
                background-color: #3742fa;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1e90ff;
            }
            QPushButton:pressed {
                background-color: #2e86de;
            }
            QLabel {
                color: #2f3542;
                font-size: 14px;
            }
            QLineEdit {
                border: 1px solid #dfe4ea;
                border-radius: 4px;
                padding: 8px;
                background-color: #f1f2f6;
                color: #2f3542;
                font-size: 14px;
            }
            QLineEdit:disabled {
                background-color: #f1f2f6;
                color: #747d8c;
            }
            QCheckBox {
                color: #2f3542;
                font-size: 14px;
                spacing: 8px;
            }
            QTableWidget {
                border: 1px solid #dfe4ea;
                border-radius: 4px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f1f2f6;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        # 第一組：程式執行
        group1_layout = self.create_program_execution_group()
        layout.addLayout(group1_layout)
        
        # 分隔線
        separator1 = QWidget()
        separator1.setFixedHeight(1)
        separator1.setStyleSheet("background-color: #dfe4ea;")
        layout.addWidget(separator1)
        
        # 第二組：視窗管理
        group2_layout = self.create_window_management_group()
        layout.addLayout(group2_layout)
        
        # 分隔線
        separator2 = QWidget()
        separator2.setFixedHeight(1)
        separator2.setStyleSheet("background-color: #dfe4ea;")
        layout.addWidget(separator2)
        
        # 第三組：視窗列表
        self.create_window_list_group(layout)
        
        layout.addStretch()

    def create_program_execution_group(self):
        """創建程式執行區域"""
        group_layout = QVBoxLayout()
        
        # 創建標題
        title_label = QLabel("開啟程式")
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #2f3542;
                font-size: 16px;
                margin-bottom: 5px;
            }
        """)
        group_layout.addWidget(title_label)
        
        # 創建路徑選擇區域
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)
        
        # 程式路徑顯示
        self.path_display = QLineEdit()
        self.path_display.setReadOnly(True)
        self.path_display.setPlaceholderText("請選擇程式路徑...")
        
        # 選擇按鈕
        self.select_btn = QPushButton("選擇")
        self.select_btn.clicked.connect(self.select_program)
        
        path_layout.addWidget(self.path_display)
        path_layout.addWidget(self.select_btn)
        
        # 執行次數設定區域
        count_layout = QHBoxLayout()
        count_layout.setSpacing(10)
        
        count_label = QLabel("執行次數:")
        self.count_input = QLineEdit()
        self.count_input.setValidator(QIntValidator(1, 999))
        self.count_input.setFixedWidth(80)
        self.count_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_input.setText("1")
        
        self.execute_btn = QPushButton("執行程式")
        self.execute_btn.clicked.connect(self.execute_program)
        
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.count_input)
        count_layout.addWidget(self.execute_btn)
        count_layout.addStretch()
        
        # 將所有元件加入群組布局
        group_layout.addLayout(path_layout)
        group_layout.addLayout(count_layout)
        
        return group_layout

    def create_window_management_group(self):
        """創建視窗管理區域"""
        group_layout = QVBoxLayout()
        
        # 標題
        title_label = QLabel("視窗管理")
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #2f3542;
                font-size: 16px;
                margin-bottom: 5px;
            }
        """)
        group_layout.addWidget(title_label)
        
        # 視窗標題設定
        title_layout = QHBoxLayout()
        title_label = QLabel("視窗標題:")
        self.window_title_input = QLineEdit()
        self.window_title_input.setPlaceholderText("輸入要管理的視窗標題...")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.window_title_input)
        group_layout.addLayout(title_layout)
        
        # 視窗大小設定
        size_layout = QHBoxLayout()
        width_label = QLabel("視窗寬度:")
        self.width_input = QLineEdit()
        self.width_input.setValidator(QIntValidator())
        self.width_input.setText("480")
        self.width_input.setFixedWidth(80)
        
        height_label = QLabel("視窗高度:")
        self.height_input = QLineEdit()
        self.height_input.setValidator(QIntValidator())
        self.height_input.setText("344")
        self.height_input.setFixedWidth(80)
        
        size_layout.addWidget(width_label)
        size_layout.addWidget(self.width_input)
        size_layout.addWidget(height_label)
        size_layout.addWidget(self.height_input)
        size_layout.addStretch()
        group_layout.addLayout(size_layout)
        
        # 視窗樣式選項
        style_layout = QHBoxLayout()
        self.remove_title_checkbox = QCheckBox("移除標題欄")
        self.remove_border_checkbox = QCheckBox("移除邊框")
        self.bypass_limit_checkbox = QCheckBox("解除視窗限制")
        self.dont_movewindow_checkbox = QCheckBox("不排序視窗")
        style_layout.addWidget(self.remove_title_checkbox)
        style_layout.addWidget(self.remove_border_checkbox)
        style_layout.addWidget(self.bypass_limit_checkbox)
        style_layout.addWidget(self.dont_movewindow_checkbox)
        style_layout.addStretch()
        group_layout.addLayout(style_layout)
        
        # 執行按鈕
        btn_layout = QHBoxLayout()
        self.manage_btn = QPushButton("套用設定")
        self.manage_btn.clicked.connect(self.manage_windows)
        btn_layout.addStretch()
        btn_layout.addWidget(self.manage_btn)
        group_layout.addLayout(btn_layout)
        
        return group_layout

    def load_settings(self):
        """載入設定"""
        settings = self.settings_handler.load_settings()
        
        self.path_display.setText(settings["program_path"])
        self.count_input.setText(settings["execution_count"])
        self.window_title_input.setText(settings["window_title"])
        self.width_input.setText(settings["window_width"])
        self.height_input.setText(settings["window_height"])
        
        self.remove_title_checkbox.setChecked(settings["remove_title"])
        self.remove_border_checkbox.setChecked(settings["remove_border"])
        self.bypass_limit_checkbox.setChecked(settings["bypass_limit"])

    def save_settings(self):
        """儲存設定"""
        settings = {
            "program_path": self.path_display.text(),
            "execution_count": self.count_input.text(),
            "window_title": self.window_title_input.text(),
            "window_width": self.width_input.text(),
            "window_height": self.height_input.text(),
            "remove_title": self.remove_title_checkbox.isChecked(),
            "remove_border": self.remove_border_checkbox.isChecked(),
            "bypass_limit": self.bypass_limit_checkbox.isChecked()
        }
        self.settings_handler.save_settings(settings)
        
    def create_window_list_group(self, layout):
        """創建視窗列表區域"""
        # 建立表格
        self.window_table = QTableWidget()
        self.window_table.setColumnCount(8)
        self.window_table.setHorizontalHeaderLabels(['序號', '視窗名稱', 'HWND',"X","Y", '標題欄', '邊框', '操作'])
        
        # 設定表格樣式
        header = self.window_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # 序號
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)          # 視窗名稱
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # HWND
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # X
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Y
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # 標題欄
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # 邊框
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # 操作


        self.window_table.setMinimumHeight(200)
        layout.addWidget(self.window_table)

    def select_program(self):
        """選擇程式檔案"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "選擇執行程式",
            "",
            "執行檔 (*.exe);;所有檔案 (*.*)"
        )
        if file_path:
            self.path_display.setText(file_path)
            # 自動設定視窗標題為程式名稱
            import os
            program_name = os.path.splitext(os.path.basename(file_path))[0]
            self.window_title_input.setText(program_name)

    def execute_program(self):
        """執行程式"""
        program_path = self.path_display.text()
        count = self.count_input.text()
        
        if not program_path:
            QMessageBox.warning(self, "錯誤", "請先選擇程式")
            return
            
        try:
            execution_count = int(count)
            success, message = self.functions.execute_program(program_path, execution_count)
            if success:
                QMessageBox.information(self, "成功", message)
            else:
                QMessageBox.warning(self, "錯誤", message)
        except ValueError:
            QMessageBox.warning(self, "錯誤", "請輸入有效的執行次數")

    def manage_windows(self):
        """管理視窗"""
        # 獲取輸入值
        title = self.window_title_input.text()
        try:
            width = int(self.width_input.text())
            height = int(self.height_input.text())
            remove_title = self.remove_title_checkbox.isChecked()
            remove_border = self.remove_border_checkbox.isChecked()
            bypass_limit = self.bypass_limit_checkbox.isChecked()
            dont_movewindow = self.dont_movewindow_checkbox.isChecked()
        except ValueError:
            QMessageBox.warning(self, "錯誤", "請輸入有效的視窗大小")
            return

        # 調用功能
        success, message = self.functions.manage_windows(title, width, height,remove_title,remove_border,bypass_limit,dont_movewindow)
        
        # 更新視窗列表
        if success:
            self.update_window_list()
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.warning(self, "錯誤", message)

    def update_window_list(self):
        """更新視窗列表"""
        window_list = self.functions.get_window_list()
        self.window_table.setRowCount(len(window_list))
        
        # 首先设置整个表格的列宽
        header = self.window_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        for row, window in enumerate(window_list):
            # 序號
            self.window_table.setItem(row, 0, QTableWidgetItem(str(window['order'])))
            
            # 視窗名稱
            title_edit = QLineEdit(window['title'])
            self.window_table.setCellWidget(row, 1, title_edit)
            self.window_table.setColumnWidth(1, 50)

            # HWND
            self.window_table.setItem(row, 2, QTableWidgetItem(str(window['hwnd'])))
            
            self.window_table.setItem(row, 3, QTableWidgetItem(str(window['X'])))
            self.window_table.setItem(row, 4, QTableWidgetItem(str(window['Y'])))
            # 標題欄 Checkbox
            title_check = QCheckBox()
            title_check.setChecked(not window['has_caption'])
            self.window_table.setCellWidget(row, 5, title_check)
            
            # 邊框 Checkbox
            border_check = QCheckBox()
            border_check.setChecked(not window['has_border'])
            self.window_table.setCellWidget(row, 6, border_check)
            
            # 應用按鈕
            apply_btn = QPushButton("應用")
            apply_btn.clicked.connect(lambda checked, r=row: self.apply_window_changes(r))
            self.window_table.setCellWidget(row, 7, apply_btn)

    def apply_window_changes(self, row):
        """應用視窗變更"""
        hwnd = int(self.window_table.item(row, 2).text())
        new_title = self.window_table.cellWidget(row, 1).text()
        remove_title = self.window_table.cellWidget(row, 5).isChecked()
        remove_border = self.window_table.cellWidget(row, 6).isChecked()
        
        # 更新標題
        success, message = self.functions.update_window_title(hwnd, new_title)
        if not success:
            QMessageBox.warning(self, "錯誤", f"更新標題失敗: {message}")
            return
            
        # 更新樣式
        success, message = self.functions.update_window_style(hwnd, remove_title, remove_border)
        if not success:
            QMessageBox.warning(self, "錯誤", f"更新樣式失敗: {message}")
            return
        
        # 更新位置
        x = int(self.window_table.item(row, 3).text())
        y = int(self.window_table.item(row, 4).text())
        width = int(self.width_input.text())
        height = int(self.height_input.text())
        
        success, message = self.functions.update_window_position(hwnd, x, y, width, height)
        if not success:
            QMessageBox.warning(self, "錯誤", f"更新位置失敗: {message}")
            return


        QMessageBox.information(self, "成功", "已更新視窗設定")


    # AccountTab 類別
class AccountTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)
        
        # 帳號管理相關的UI元件將在這裡添加

        layout.addStretch()

# OtherTab 類別
class OtherTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QPushButton {
                background-color: #ff6b81;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff4757;
            }
            QPushButton:pressed {
                background-color: #ee5253;
            }
        """)
        
        # 其他功能相關的UI元件將在這裡添加
        btn_settings = QPushButton('設定')
        btn_about = QPushButton('關於')
        
        layout.addWidget(btn_settings)
        layout.addWidget(btn_about)
        layout.addStretch()