import sys
from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, 
                             QLineEdit, QPushButton, QVBoxLayout, 
                             QWidget, QStatusBar)
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Word")
        self.showMaximized()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(1, 1, 800, 800) 

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLabel {
                color: #ffffff;
                font-size: 18px;
            }
        """)

        # Configurar la vista web
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://docs.google.com/"))
        
        # # Barra de navegación
        # navbar = QToolBar()
        # self.addToolBar(navbar)
        
        # # Botones
        # back_btn = QPushButton("←")
        # back_btn.clicked.connect(self.browser.back)
        # navbar.addWidget(back_btn)
        
        # forward_btn = QPushButton("→")
        # forward_btn.clicked.connect(self.browser.forward)
        # navbar.addWidget(forward_btn)
        
        # reload_btn = QPushButton("↻")
        # reload_btn.clicked.connect(self.browser.reload)
        # navbar.addWidget(reload_btn)

        # home_btn = QPushButton("🔍")
        # home_btn.clicked.connect(self.home)
        # navbar.addWidget(home_btn)
        
        # self.url_bar = QLineEdit()
        # self.url_bar.returnPressed.connect(self.navigate_to_url)
        # navbar.addWidget(self.url_bar)
        
        # go_btn = QPushButton("Ir")
        # go_btn.clicked.connect(self.navigate_to_url)
        # navbar.addWidget(go_btn)

        # close_btn = QPushButton("❌")
        # close_btn.clicked.connect(self.close)
        # navbar.addWidget(close_btn)

        # maximize_btn = QPushButton("⛶")
        # maximize_btn.clicked.connect(self.showFullScreen)
        # navbar.addWidget(maximize_btn)
        
        
        # minimize_btn = QPushButton("➖")
        # minimize_btn.clicked.connect(self.custom_minimize)
        # navbar.addWidget(minimize_btn)
        
        self.browser.urlChanged.connect(self.update_url)
        
        # self.status = QStatusBar()
        # self.setStatusBar(self.status)
        
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())