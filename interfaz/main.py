import sys
import os
import time
import subprocess
import psutil
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFrame, QMenu, QSystemTrayIcon, 
                            QGridLayout, QMessageBox, QTabWidget, QLineEdit, 
                            QComboBox, QCheckBox, QColorDialog, QFontDialog,
                            QSpinBox, QFileDialog, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt, QTimer, QPoint, QSettings
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont

class ConfigWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Configuración de MarkOS")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setFixedSize(800, 600)
        self.dragging = False  # Estado para detectar si se está arrastrando la ventana
        
        # Inicializar atributos de configuración
        self.bg_color_value = QColor(255, 236, 139)
        self.btn_color_value = QColor(128, 128, 128)
        self.btn_hover_value = QColor(77, 77, 77)
        self.taskbar_color_value = QColor(45, 45, 45)
        self.font_value = QFont("Segoe UI", 12)
        
        # Configurar interfaz
        self.setup_ui()
        
        # Cargar configuración actual (mover aquí después de inicializar la interfaz)
        self.settings = QSettings("MarkOS", "Configuracion")
        self.load_settings()
        
    def mousePressEvent(self, event):
        """Detectar el inicio del arrastre."""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Mover la ventana mientras se arrastra."""
        if self.dragging:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Finalizar el arrastre."""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Pestañas de configuración
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Pestaña de Apariencia
        appearance_tab = QWidget()
        tabs.addTab(appearance_tab, "Apariencia")
        self.setup_appearance_tab(appearance_tab)
        
        # Pestaña de Aplicaciones
        apps_tab = QWidget()
        tabs.addTab(apps_tab, "Aplicaciones")
        self.setup_apps_tab(apps_tab)
        
        # Pestaña de Sistema
        system_tab = QWidget()
        tabs.addTab(system_tab, "Sistema")
        self.setup_system_tab(system_tab)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)
        
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(cancel_btn)
        
        reset_btn = QPushButton("Restaurar predeterminados")
        reset_btn.clicked.connect(self.reset_defaults)
        btn_layout.addWidget(reset_btn)
    
    def setup_appearance_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Grupo de colores
        colors_group = QGroupBox("Colores")
        colors_layout = QFormLayout()
        colors_group.setLayout(colors_layout)
        layout.addWidget(colors_group)
        
        self.bg_color_btn = QPushButton("Color de fondo")
        self.bg_color_btn.clicked.connect(lambda: self.choose_color("bg_color"))
        colors_layout.addRow("Fondo principal:", self.bg_color_btn)
        
        self.btn_color_btn = QPushButton("Color de botones")
        self.btn_color_btn.clicked.connect(lambda: self.choose_color("btn_color"))
        colors_layout.addRow("Botones principales:", self.btn_color_btn)
        
        self.btn_hover_btn = QPushButton("Color hover")
        self.btn_hover_btn.clicked.connect(lambda: self.choose_color("btn_hover"))
        colors_layout.addRow("Botones (hover):", self.btn_hover_btn)
        
        self.taskbar_color_btn = QPushButton("Color barra tareas")
        self.taskbar_color_btn.clicked.connect(lambda: self.choose_color("taskbar_color"))
        colors_layout.addRow("Barra de tareas:", self.taskbar_color_btn)
        
        # Grupo de fuentes
        font_group = QGroupBox("Fuentes")
        font_layout = QFormLayout()
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        self.font_btn = QPushButton("Seleccionar fuente")
        self.font_btn.clicked.connect(self.choose_font)
        font_layout.addRow("Fuente principal:", self.font_btn)
        
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        font_layout.addRow("Tamaño fuente:", self.font_size)
        
        # Inicializar self.show_clock, self.show_app_names y self.rounded_corners
        self.show_clock = QCheckBox("Mostrar reloj")
        layout.addWidget(self.show_clock)
        
        self.show_app_names = QCheckBox("Mostrar nombres de aplicaciones")
        layout.addWidget(self.show_app_names)
        
        self.rounded_corners = QCheckBox("Esquinas redondeadas")
        layout.addWidget(self.rounded_corners)
    
    def setup_apps_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Rutas de aplicaciones
        paths_group = QGroupBox("Rutas de aplicaciones")
        paths_layout = QFormLayout()
        paths_group.setLayout(paths_layout)
        layout.addWidget(paths_group)
        
        self.terminal_path = QLineEdit()
        paths_layout.addRow("Terminal:", self.terminal_path)
        
        self.file_manager_path = QLineEdit()
        paths_layout.addRow("Gestor de archivos:", self.file_manager_path)
        
        self.browser_path = QLineEdit()
        paths_layout.addRow("Navegador web:", self.browser_path)
        
        # Comportamiento de aplicaciones
        behavior_group = QGroupBox("Comportamiento")
        behavior_layout = QVBoxLayout()
        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)
        
        self.minimize_on_close = QCheckBox("Minimizar en lugar de cerrar")
        behavior_layout.addWidget(self.minimize_on_close)
        
        self.confirm_app_close = QCheckBox("Confirmar antes de cerrar aplicaciones")
        behavior_layout.addWidget(self.confirm_app_close)
        
        self.remember_open_apps = QCheckBox("Recordar aplicaciones abiertas")
        behavior_layout.addWidget(self.remember_open_apps)
    
    def setup_system_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Comportamiento del sistema
        system_group = QGroupBox("Comportamiento del sistema")
        system_layout = QFormLayout()
        system_group.setLayout(system_layout)
        layout.addWidget(system_group)
        
        self.start_maximized = QCheckBox("Iniciar maximizado")
        system_layout.addRow(self.start_maximized)
        
        self.show_taskbar = QCheckBox("Mostrar barra de tareas")
        system_layout.addRow(self.show_taskbar)
        
        self.animations = QCheckBox("Habilitar animaciones")
        system_layout.addRow(self.animations)
        
        # Inicializar self.animation_speed
        self.animation_speed = QComboBox()
        self.animation_speed.addItems(["Rápido", "Normal", "Lento"])
        system_layout.addRow("Velocidad animaciones:", self.animation_speed)
        
        # Opciones de energía
        power_group = QGroupBox("Opciones de energía")
        power_layout = QVBoxLayout()
        power_group.setLayout(power_layout)
        layout.addWidget(power_group)
        
        self.confirm_shutdown = QCheckBox("Confirmar antes de apagar")
        power_layout.addWidget(self.confirm_shutdown)
        
        self.confirm_reboot = QCheckBox("Confirmar antes de reiniciar")
        power_layout.addWidget(self.confirm_reboot)
    
    def choose_color(self, setting_name):
        color = QColorDialog.getColor()
        if color.isValid():
            setattr(self, f"{setting_name}_value", color)
            btn = getattr(self, f"{setting_name}_btn")
            btn.setStyleSheet(f"background-color: {color.name()}; color: {'white' if color.lightness() < 150 else 'black'};")
    
    def choose_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.font_value = font
            self.font_btn.setText(f"{font.family()} {font.pointSize()}pt")
    
    def load_settings(self):
        # Cargar configuración desde QSettings o usar valores por defecto
        self.bg_color_value = QColor(self.settings.value("colors/bg", QColor(255, 236, 139)))
        self.btn_color_value = QColor(self.settings.value("colors/btn", QColor(128, 128, 128)))
        self.btn_hover_value = QColor(self.settings.value("colors/btn_hover", QColor(77, 77, 77)))
        self.taskbar_color_value = QColor(self.settings.value("colors/taskbar", QColor(45, 45, 45)))
        
        font_str = self.settings.value("font/main", "Segoe UI,12")
        font_parts = font_str.split(",")
        self.font_value = QFont(font_parts[0], int(font_parts[1]))
        
        self.font_size.setValue(self.settings.value("font/size", 12, type=int))
        self.show_clock.setChecked(self.settings.value("display/show_clock", True, type=bool))
        self.show_app_names.setChecked(self.settings.value("display/show_app_names", True, type=bool))
        self.rounded_corners.setChecked(self.settings.value("display/rounded_corners", True, type=bool))
        
        self.terminal_path.setText(self.settings.value("apps/terminal", "gnome-terminal" if os.name != 'nt' else "cmd.exe"))
        self.file_manager_path.setText(self.settings.value("apps/file_manager", "nautilus" if os.name != 'nt' else "explorer"))
        self.browser_path.setText(self.settings.value("apps/browser", "firefox"))
        
        self.minimize_on_close.setChecked(self.settings.value("behavior/minimize_on_close", False, type=bool))
        self.confirm_app_close.setChecked(self.settings.value("behavior/confirm_app_close", True, type=bool))
        self.remember_open_apps.setChecked(self.settings.value("behavior/remember_open_apps", False, type=bool))
        
        self.start_maximized.setChecked(self.settings.value("system/start_maximized", True, type=bool))
        self.show_taskbar.setChecked(self.settings.value("system/show_taskbar", True, type=bool))
        self.animations.setChecked(self.settings.value("system/animations", True, type=bool))
        self.animation_speed.setCurrentText(self.settings.value("system/animation_speed", "Normal"))
        
        self.confirm_shutdown.setChecked(self.settings.value("power/confirm_shutdown", True, type=bool))
        self.confirm_reboot.setChecked(self.settings.value("power/confirm_reboot", True, type=bool))
        
        # Actualizar botones de color
        self.update_color_buttons()
        self.update_font_button()
    
    def update_color_buttons(self):
        for color_type in ["bg_color", "btn_color", "btn_hover", "taskbar_color"]:
            color = getattr(self, f"{color_type}_value")
            btn = getattr(self, f"{color_type}_btn")
            btn.setStyleSheet(f"background-color: {color.name()}; color: {'white' if color.lightness() < 150 else 'black'};")
    
    def update_font_button(self):
        self.font_btn.setText(f"{self.font_value.family()} {self.font_value.pointSize()}pt")
    
    def save_settings(self):
        # Guardar configuración en QSettings
        self.settings.setValue("colors/bg", self.bg_color_value)
        self.settings.setValue("colors/btn", self.btn_color_value)
        self.settings.setValue("colors/btn_hover", self.btn_hover_value)
        self.settings.setValue("colors/taskbar", self.taskbar_color_value)
        
        self.settings.setValue("font/main", f"{self.font_value.family()},{self.font_value.pointSize()}")
        self.settings.setValue("font/size", self.font_size.value())
        self.settings.setValue("display/show_clock", self.show_clock.isChecked())
        self.settings.setValue("display/show_app_names", self.show_app_names.isChecked())
        self.settings.setValue("display/rounded_corners", self.rounded_corners.isChecked())
        
        self.settings.setValue("apps/terminal", self.terminal_path.text())
        self.settings.setValue("apps/file_manager", self.file_manager_path.text())
        self.settings.setValue("apps/browser", self.browser_path.text())
        
        self.settings.setValue("behavior/minimize_on_close", self.minimize_on_close.isChecked())
        self.settings.setValue("behavior/confirm_app_close", self.confirm_app_close.isChecked())
        self.settings.setValue("behavior/remember_open_apps", self.remember_open_apps.isChecked())
        
        self.settings.setValue("system/start_maximized", self.start_maximized.isChecked())
        self.settings.setValue("system/show_taskbar", self.show_taskbar.isChecked())
        self.settings.setValue("system/animations", self.animations.isChecked())
        self.settings.setValue("system/animation_speed", self.animation_speed.currentText())
        
        self.settings.setValue("power/confirm_shutdown", self.confirm_shutdown.isChecked())
        self.settings.setValue("power/confirm_reboot", self.confirm_reboot.isChecked())
        
        # Aplicar cambios en tiempo real
        if self.parent:
            self.parent.apply_settings()
        
        QMessageBox.information(self, "Configuración", "Los cambios se han guardado correctamente.")
        self.close()
    
    def reset_defaults(self):
        reply = QMessageBox.question(
            self, 'Restaurar predeterminados', 
            '¿Está seguro que desea restaurar todos los valores predeterminados?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.settings.clear()
            self.load_settings()
            QMessageBox.information(self, "Configuración", "Se han restaurado los valores predeterminados.")

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
        self.settings = QSettings("MarkOS", "Configuracion")
        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint | Qt.FramelessWindowHint)
        self.showMaximized()  # Mostrar en pantalla maximizada en lugar de pantalla completa

        # Configuración inicial
        self.load_initial_settings()
        
        self.window_manager = WindowManager()
        self.open_apps = {}
        self.app_counter = 0

        self.PYROUTE = "python3"
        self.SYS_PATH = os.path.dirname(os.path.abspath(__file__))
        
        # Configurar el widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sección de aplicaciones
        self.apps_section = QWidget()
        self.update_apps_section_style()
        main_layout.addWidget(self.apps_section, 1)
        
        # Barra de tareas
        self.taskbar = QFrame()
        self.update_taskbar_style()
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
        
        # Mostrar según configuración
        if self.settings.value("system/start_maximized", True, type=bool):
            self.showMaximized()
        else:
            self.show()
    
    def load_initial_settings(self):
        """Cargar configuración inicial desde QSettings"""
        self.BG_COLOR = QColor(self.settings.value("colors/bg", QColor(255, 236, 139)))
        self.BTN_COLOR = QColor(self.settings.value("colors/btn", QColor(128, 128, 128)))
        self.BTN_HOVER = QColor(self.settings.value("colors/btn_hover", QColor(77, 77, 77)))
        self.TASKBAR_COLOR = QColor(self.settings.value("colors/taskbar", QColor(45, 45, 45)))
        
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
        QApplication.instance().setPalette(palette)
    
    def apply_settings(self):
        """Aplicar cambios de configuración en tiempo real"""
        self.load_initial_settings()
        self.update_apps_section_style()
        self.update_taskbar_style()
        
        # Actualizar visibilidad del reloj
        self.clock_label.setVisible(self.settings.value("display/show_clock", True, type=bool))
        
        # Reconstruir la sección de aplicaciones si es necesario
        if hasattr(self, 'show_app_names'):
            self.setup_apps_section()
    
    def update_apps_section_style(self):
        """Actualizar el estilo de la sección de aplicaciones"""
        radius = "15px" if self.settings.value("display/rounded_corners", True, type=bool) else "0px"
        self.apps_section.setStyleSheet(f"""
            background-color: {self.BG_COLOR.name()};
            border-radius: {radius};
            margin: 20px;
        """)
    
    def update_taskbar_style(self):
        """Actualizar el estilo de la barra de tareas"""
        self.taskbar.setStyleSheet(f"""
            background-color: {self.TASKBAR_COLOR.name()};
            border-top: 1px solid #444;
        """)
    
    def open_settings(self):
        if hasattr(self, 'config_window') and self.config_window.isVisible():
            self.config_window.raise_()
            self.config_window.activateWindow()
        else:
            self.config_window = ConfigWindow(self)
            self.config_window.show()

    def setup_apps_section(self):
        layout = QGridLayout(self.apps_section)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        
        apps = [
            ("⚙️ Configuración", lambda: self.open_settings()),
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
        if hasattr(self, 'config_window') and self.config_window.isVisible():
            self.config_window.raise_()
            self.config_window.activateWindow()
        else:
            self.config_window = ConfigWindow(self)
            self.config_window.show()
    
    def open_app(self, module_name):
        try:
            if module_name == "terminal":
                if os.name == 'nt':
                    process = subprocess.Popen(["cmd.exe", "/k", "bash shell_interactiva.sh"])
                else:
                    script_path = os.path.join(self.SYS_PATH, "shell_interactiva.sh")
                    process = subprocess.Popen(["gnome-terminal", "--", "bash", script_path])
                self.add_app_to_taskbar("Terminal", process)
                
            elif module_name == "file":
                folder_path = os.path.expanduser("~")
                try:
                    if os.name == 'nt':
                        process = subprocess.Popen(["explorer", folder_path])
                    else:
                        process = subprocess.Popen(["nautilus", folder_path])
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
            elif module_name == "config":
                self.config_window = ConfigApp()
                self.config_window.show()
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
            if app_info["window_state"] == "minimized":
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
                self.raise_()
                self.activateWindow()
            else:
                # Ya está visible, no hacer nada (o podrías enfocarla otra vez si quieres)
                self.window_manager.focus_window(app_name)
        except Exception as e:
            print(f"Error al enfocar ventana: {e}")
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

class ConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración de MarkOS")
        self.setFixedSize(400, 300)
        self.settings = QSettings("MarkOS", "Configuracion")
        
        # Configurar interfaz
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Configuración de colores
        colors_group = QGroupBox("Colores")
        colors_layout = QFormLayout()
        colors_group.setLayout(colors_layout)
        layout.addWidget(colors_group)

        self.bg_color_btn = QPushButton("Color de fondo")
        self.bg_color_btn.clicked.connect(lambda: self.choose_color("bg_color"))
        colors_layout.addRow("Fondo del escritorio:", self.bg_color_btn)

        self.btn_color_btn = QPushButton("Color de botones")
        self.btn_color_btn.clicked.connect(lambda: self.choose_color("btn_color"))
        colors_layout.addRow("Botones de apps:", self.btn_color_btn)

        self.taskbar_color_btn = QPushButton("Color barra de tareas")
        self.taskbar_color_btn.clicked.connect(lambda: self.choose_color("taskbar_color"))
        colors_layout.addRow("Barra de tareas:", self.taskbar_color_btn)

        # Configuración de tipografía
        font_group = QGroupBox("Tipografía")
        font_layout = QFormLayout()
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)

        self.font_btn = QPushButton("Seleccionar fuente")
        self.font_btn.clicked.connect(self.choose_font)
        font_layout.addRow("Fuente principal:", self.font_btn)

        # Botones de acción
        action_layout = QHBoxLayout()
        layout.addLayout(action_layout)

        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save_settings)
        action_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.close)
        action_layout.addWidget(cancel_btn)

    def choose_color(self, setting_name):
        color = QColorDialog.getColor()
        if color.isValid():
            setattr(self, f"{setting_name}_value", color)
            btn = getattr(self, f"{setting_name}_btn")
            btn.setStyleSheet(f"background-color: {color.name()}; color: {'white' if color.lightness() < 150 else 'black'};")

    def choose_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.font_value = font
            self.font_btn.setText(f"{font.family()} {font.pointSize()}pt")

    def load_settings(self):
        self.bg_color_value = QColor(self.settings.value("colors/bg", QColor(255, 236, 139)))
        self.btn_color_value = QColor(self.settings.value("colors/btn", QColor(128, 128, 128)))
        self.taskbar_color_value = QColor(self.settings.value("colors/taskbar", QColor(45, 45, 45)))

        font_str = self.settings.value("font/main", "Segoe UI,12")
        font_parts = font_str.split(",")
        self.font_value = QFont(font_parts[0], int(font_parts[1]))

        self.update_color_buttons()
        self.font_btn.setText(f"{self.font_value.family()} {self.font_value.pointSize()}pt")

    def update_color_buttons(self):
        for color_type in ["bg", "btn", "taskbar"]:
            color = getattr(self, f"{color_type}_value")
            btn = getattr(self, f"{color_type}_btn")
            btn.setStyleSheet(f"background-color: {color.name()}; color: {'white' if color.lightness() < 150 else 'black'};")

    def save_settings(self):
        self.settings.setValue("colors/bg", self.bg_color_value)
        self.settings.setValue("colors/btn", self.btn_color_value)
        self.settings.setValue("colors/taskbar", self.taskbar_color_value)
        self.settings.setValue("font/main", f"{self.font_value.family()},{self.font_value.pointSize()}")

        QMessageBox.information(self, "Configuración", "Los cambios se han guardado correctamente.")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Establecer estilo fusion para mejor apariencia
    app.setStyle("Fusion")
    main_window = MarkOS()
    sys.exit(app.exec_())