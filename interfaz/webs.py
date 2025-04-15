import sys
from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, 
                             QLineEdit, QPushButton, QVBoxLayout, 
                             QWidget, QStatusBar)
from PyQt5.QtWebEngineWidgets import QWebEngineView

_browser_windows = []  # Lista para almacenar las instancias de Browser
class Browser(QMainWindow):
    def __init__(self, tk_root=None, on_close_callback=None):
        super().__init__()
        self.tk_root = tk_root  # Referencia opcional a ventana Tkinter
        self.on_close_callback = on_close_callback 
        self.setWindowTitle("Navegador Python")
        self.showMaximized()
        self.setWindowFlags(Qt.FramelessWindowHint)

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
        self.browser.setUrl(QUrl("https://www.google.com"))
        
        # Barra de navegación
        navbar = QToolBar()
        self.addToolBar(navbar)
        
        # Botones
        back_btn = QPushButton("←")
        back_btn.clicked.connect(self.browser.back)
        navbar.addWidget(back_btn)
        
        forward_btn = QPushButton("→")
        forward_btn.clicked.connect(self.browser.forward)
        navbar.addWidget(forward_btn)
        
        reload_btn = QPushButton("↻")
        reload_btn.clicked.connect(self.browser.reload)
        navbar.addWidget(reload_btn)

        home_btn = QPushButton("🔍")
        home_btn.clicked.connect(self.home)
        navbar.addWidget(home_btn)
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        
        go_btn = QPushButton("Ir")
        go_btn.clicked.connect(self.navigate_to_url)
        navbar.addWidget(go_btn)

        close_btn = QPushButton("❌")
        close_btn.clicked.connect(self.close)
        navbar.addWidget(close_btn)

        maximize_btn = QPushButton("⛶")
        maximize_btn.clicked.connect(self.showFullScreen)
        navbar.addWidget(maximize_btn)
        
        
        minimize_btn = QPushButton("➖")
        minimize_btn.clicked.connect(self.custom_minimize)
        navbar.addWidget(minimize_btn)
        
        self.browser.urlChanged.connect(self.update_url)
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Timer para integración con Tkinter si se proporciona
        if self.tk_root:
            self.timer = QTimer()
            self.timer.timeout.connect(self.check_tkinter_root)
            self.timer.start(100)  # Verificar cada 100ms
    
    def check_tkinter_root(self):
        """Verifica si la ventana Tkinter madre sigue abierta"""
        try:
            if not self.tk_root.winfo_exists():
                self.close()
        except:
            self.close()
    
    def custom_minimize(self):
        if self.isFullScreen():
            self.showNormal()  # Salir de pantalla completa
        self.showMinimized()  # Minimizar
    
    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))
    
    def update_url(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)
    
    def home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))
        
    def closeEvent(self, event):
        """Se ejecuta cuando la ventana se cierra"""
        if self.on_close_callback:
            self.on_close_callback()
        super().closeEvent(event)
        # Eliminar esta ventana de la lista global
        if self in _browser_windows:
            _browser_windows.remove(self)

def launch_browser(tk_root=None, on_close_callback=None):
    # Reutilizar la aplicación existente o crear una nueva
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    browser = Browser(tk_root, on_close_callback)
    browser.show()
    
    # Mantener referencia para evitar garbage collection
    _browser_windows.append(browser)
    
    # Solo ejecutar el event loop si es la primera ventana
    if len(_browser_windows) == 1:
        app.exec_()
            
    return browser