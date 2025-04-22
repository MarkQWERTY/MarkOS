import sys
import os
import time
import subprocess
import psutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFrame, QMenu, QSystemTrayIcon, 
                            QGridLayout, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QIcon, QPalette, QColor

class WindowManager:
    def __init__(self):
        pass
    
    def focus_window(self, window_title):
        """Enfoca una ventana por su título"""
        try:
            if os.name == 'nt':
                import win32gui
                import win32con
                window = win32gui.FindWindow(None, window_title)
                if window:
                    win32gui.ShowWindow(window, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(window)
            else:
                subprocess.run(["wmctrl", "-a", window_title])
        except Exception as e:
            print(f"Error al enfocar ventana: {e}")
    
    def minimize_window(self, window_title):
        """Minimiza una ventana por su título"""
        try:
            if os.name == 'nt':
                import win32gui
                import win32con
                window = win32gui.FindWindow(None, window_title)
                if window:
                    win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
            else:
                subprocess.run(["xdotool", "search", "--name", window_title, "windowminimize"])
        except Exception as e:
            print(f"Error al minimizar ventana: {e}")

class MarkOS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarkOS")
        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint | Qt.FramelessWindowHint)
        self.showMaximized()  # Mostrar en pantalla maximizada en lugar de pantalla completa
        
        self.window_manager = WindowManager()
        self.open_apps = {}
        self.app_counter = 0

        self.PYROUTE = "python3"
        self.SYS_PATH = os.path.dirname(os.path.abspath(__file__))
        self.BG_COLOR = QColor(255, 236, 139)  # khaki1 equivalente
        self.BTN_COLOR = QColor(128, 128, 128)  # gray
        self.BTN_HOVER = QColor(77, 77, 77)    # gray30
        
        # Configurar el widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sección de aplicaciones
        self.apps_section = QWidget()
        self.apps_section.setStyleSheet(f"""
            background-color: {self.BG_COLOR.name()};
            border-radius: 15px;
            margin: 20px;
        """)
        main_layout.addWidget(self.apps_section, 1)
        
        # Barra de tareas
        self.taskbar = QFrame()
        self.taskbar.setStyleSheet("""
            background-color: #2d2d2d;
            border-top: 1px solid #444;
        """)
        self.taskbar.setFixedHeight(50)
        main_layout.addWidget(self.taskbar)
        
        # Configurar las secciones
        self.setup_apps_section()
        self.setup_taskbar()
        
        # Temporizador para el reloj
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        
        # Mostrar la hora inicial
        self.update_clock()
    
    def setup_apps_section(self):
        layout = QGridLayout(self.apps_section)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        
        apps = [
            ("⚙️ Configuración", self.open_settings),
            ("🌐 Navegador", lambda: self.open_app("webs")),
            ("📁 Archivos", lambda: self.open_app("file")),
            ("📟 Terminal", lambda: self.open_app("terminal")),
            ("🧮 Calculadora", lambda: self.open_app("calc")),
            ("Ejecutar", lambda: self.open_app("ejecutar")),
            ("Spotify", lambda: self.open_app("spotify")),
            ("Telegram", lambda: self.open_app("telegram-desktop")),
            ("Office", lambda: self.open_app("docs"))
        ]
        
        for i, (app_name, callback) in enumerate(apps):
            btn = QPushButton(app_name)
            btn.setFixedSize(400, 120)  # Tamaño cuadrado para los botones
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.BTN_COLOR.name()};
                    color: white;
                    border: none;
                    border-radius: 15px;
                    padding: 15px;
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    background-color: {self.BTN_HOVER.name()};
                    border: 2px solid #fff;
                }}
            """)
            btn.clicked.connect(callback)
            
            # Distribución en grid 3x3
            row = i // 3
            col = i % 3
            layout.addWidget(btn, row, col, Qt.AlignCenter)
    
    def setup_taskbar(self):
        taskbar_layout = QHBoxLayout(self.taskbar)
        taskbar_layout.setContentsMargins(5, 0, 5, 0)
        
        # Botón de inicio con menú mejorado
        start_btn = QPushButton(" 🏠 Inicio")
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 5px 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
            }
        """)
        
        # Menú de inicio con más opciones
        start_menu = QMenu()
        
        # Menú de energía expandido
        power_menu = QMenu("Energía", self)
        power_menu.setStyleSheet("""
            QMenu {
                background-color: #3e3e3e;
                color: white;
                border: 1px solid #555;
            }
            QMenu::item:selected {
                background-color: #555;
            }
        """)
        
        power_menu.addAction("Apagar", self.shutdown)
        power_menu.addAction("Reiniciar", self.reboot)
        power_menu.addAction("Cerrar sesión", self.logout)
        start_menu.addMenu(power_menu)
        
        # Separador
        start_menu.addSeparator()
        
        # Otras opciones
        start_menu.addAction("Salir", self.close)
        
        start_btn.setMenu(start_menu)
        taskbar_layout.addWidget(start_btn)
        
        # Área de aplicaciones abiertas
        self.apps_area = QHBoxLayout()
        self.apps_area.setSpacing(2)
        taskbar_layout.addLayout(self.apps_area, 1)
        
        # Reloj
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet("""
            color: white; 
            font-size: 12px;
            padding: 0 10px;
        """)
        taskbar_layout.addWidget(self.clock_label)
    
    def update_clock(self):
        current_time = time.strftime("%H:%M | %d/%m/%Y")
        self.clock_label.setText(current_time)
    
    def logout(self):
        reply = QMessageBox.question(
            self, 'Cerrar sesión', 
            '¿Desea cerrar la sesión actual?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if os.name == 'nt':
                    os.system("shutdown /l")  # Cerrar sesión en Windows
                else:
                    os.system("gnome-session-quit --no-prompt")  # Para GNOME
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cerrar sesión: {str(e)}")
    
    def open_settings(self):
        QMessageBox.information(self, "Configuración", "Sistema de configuración abierto")
    
    def open_app(self, module_name):
        try:
            if module_name == "terminal":
                if os.name == 'nt':
                    process = subprocess.Popen(["cmd.exe", "/k", "title Terminal"])
                else:
                    process = subprocess.Popen(["gnome-terminal", "--title=Terminal"])
                self.add_app_to_taskbar("Terminal", process)
                
            elif module_name == "file":
                folder_path = os.path.expanduser("~")
                try:
                    if os.name == 'nt':
                        process = subprocess.Popen(["explorer", folder_path])
                    else:
                        process = subprocess.Popen(["nautilus", folder_path, "--title=Archivos"])
                    self.add_app_to_taskbar("Archivos", process)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo abrir la carpeta: {str(e)}")
                    
            elif module_name == "spotify":
                try:
                    if os.name == 'nt':
                        process = subprocess.Popen(["spotify.exe"])
                    else:
                        process = subprocess.Popen(["spotify", "--title=Spotify"])
                    self.add_app_to_taskbar("Spotify", process)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo abrir Spotify: {str(e)}")
                    
            elif module_name == "telegram-desktop":
                try:
                    if os.name == 'nt':
                        process = subprocess.Popen(["telegram.exe"])
                    else:
                        process = subprocess.Popen(["telegram-desktop", "--title=Telegram"])
                    self.add_app_to_taskbar("Telegram", process)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo abrir Telegram: {str(e)}")       
            else:
                script_path = os.path.join(self.SYS_PATH, f"{module_name}.py")
                if os.name == 'nt':
                    process = subprocess.Popen(["python", script_path])
                else:
                    process = subprocess.Popen(["python3", script_path])
                self.add_app_to_taskbar(module_name.capitalize(), process)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la aplicación: {str(e)}")
    
    def add_app_to_taskbar(self, app_name, process):
        app_id = self.app_counter
        self.app_counter += 1
        
        # Crear botón para la aplicación
        app_btn = QPushButton(f" {app_name[:12]} ")
        app_btn.setStyleSheet("""
            QPushButton {
                background-color: #3e3e3e;
                color: white;
                border: none;
                padding: 5px 10px;
                font-size: 11px;
                max-height: 25px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4e4e4e;
            }
        """)
        app_btn.clicked.connect(lambda: self.toggle_application(app_id))
        
        # Botón de cerrar
        close_btn = QPushButton("×")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #3e3e3e;
                color: white;
                border: none;
                padding: 5px;
                font-size: 11px;
                max-width: 20px;
                max-height: 25px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #ff5555;
            }
        """)
        close_btn.clicked.connect(lambda: self.close_app(app_id))
        
        # Contenedor para los botones
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_layout.addWidget(app_btn)
        container_layout.addWidget(close_btn)
        
        self.apps_area.addWidget(container)
        
        self.open_apps[app_id] = {
            "name": app_name,
            "process": process,
            "button": app_btn,
            "close_btn": close_btn,
            "container": container,
            "window_state": "visible"
        }
    
    def toggle_application(self, app_id):
        if app_id not in self.open_apps:
            return
            
        app_info = self.open_apps[app_id]
        app_name = app_info["name"]
        
        try:
            if app_info["window_state"] == "visible":
                self.window_manager.minimize_window(app_name)
                app_info["window_state"] = "minimized"
                app_info["button"].setStyleSheet("""
                    QPushButton {
                        background-color: #2d2d2d;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        font-size: 11px;
                        max-height: 25px;
                        border-radius: 3px;
                    }
                """)
            else:
                self.window_manager.focus_window(app_name)
                app_info["window_state"] = "visible"
                app_info["button"].setStyleSheet("""
                    QPushButton {
                        background-color: #3e3e3e;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        font-size: 11px;
                        max-height: 25px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #4e4e4e;
                    }
                """)
                # Forzar el enfoque
                self.raise_()
                self.activateWindow()
        except Exception as e:
            print(f"Error al alternar ventana: {e}")
            self.window_manager.focus_window(app_name)
    
    def close_app(self, app_id):
        if app_id in self.open_apps:
            app_info = self.open_apps[app_id]
            try:
                parent = psutil.Process(app_info["process"].pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
            except Exception as e:
                print(f"Error al cerrar la aplicación: {e}")
            
            app_info["container"].deleteLater()
            del self.open_apps[app_id]
    
    def shutdown(self):
        reply = QMessageBox.question(
            self, 'Apagar', 
            '¿Desea apagar el sistema?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if os.name == 'nt':
                    os.system("shutdown /s /t 1")
                else:
                    os.system("shutdown now")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo apagar el sistema: {str(e)}")
    
    def reboot(self):
        reply = QMessageBox.question(
            self, 'Reiniciar', 
            '¿Desea reiniciar el sistema?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if os.name == 'nt':
                    os.system("shutdown /r /t 1")
                else:
                    os.system("reboot")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo reiniciar el sistema: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Establecer estilo fusion para mejor apariencia
    app.setStyle("Fusion")
    
    # Configurar paleta de colores
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    main_window = MarkOS()
    main_window.show()
    
    sys.exit(app.exec_())