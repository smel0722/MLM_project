from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QTabWidget, QPushButton, 
                           QLabel, QFrame)
from PyQt6.QtCore import Qt
from tab_ui import MainTab, AccountTab, OtherTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 設定主視窗
        self.setWindowTitle('多功能管理程式')
        self.setGeometry(100, 100, 800, 600)
        self.setupStyles()
        
        # 創建中央視窗
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 創建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 創建分頁視窗
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 創建三個分頁，並傳遞 self 作為 parent
        self.main_tab = MainTab(self)
        self.account_tab = AccountTab()
        self.other_tab = OtherTab()
        
        # 將分頁加入分頁視窗
        self.tab_widget.addTab(self.main_tab, "主要功能")
        self.tab_widget.addTab(self.account_tab, "帳號管理")
        self.tab_widget.addTab(self.other_tab, "其他功能")
        
        # 創建狀態列
        self.status_label = QLabel('就緒')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #2f3542;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        main_layout.addWidget(self.status_label)
        
    def setupStyles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QTabWidget::pane {
                border: 2px solid #dfe4ea;
                border-radius: 8px;
                background-color: white;
                margin: 2px;
            }
            QTabBar::tab {
                background-color: #f1f2f6;
                color: #2f3542;
                padding: 10px 20px;
                margin: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid #dfe4ea;
                min-width: 100px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #3742fa;
                color: white;
                border-bottom: none;
            }
            QTabBar::tab:hover:!selected {
                background-color: #dfe4ea;
            }
        """)

    def update_status(self, message: str):
        """更新狀態列訊息"""
        self.status_label.setText(message)