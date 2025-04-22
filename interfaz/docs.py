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