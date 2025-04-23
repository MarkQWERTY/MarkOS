import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit

class TerminalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejecutar Comandos")
        self.setGeometry(100, 100, 600, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Campo de entrada para comandos
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Introduce un comando...")
        layout.addWidget(self.command_input)

        # Botón para ejecutar el comando
        self.execute_button = QPushButton("Ejecutar", self)
        self.execute_button.clicked.connect(self.execute_command)
        layout.addWidget(self.execute_button)

        # Área de texto para mostrar la salida
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

        # Contenedor principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def execute_command(self):
        command = self.command_input.text()
        if command.strip():
            try:
                # Ejecutar el comando y capturar la salida
                result = subprocess.run(command, shell=True, text=True, capture_output=True)
                output = result.stdout if result.returncode == 0 else result.stderr
                self.output_area.setText(output)
            except Exception as e:
                self.output_area.setText(f"Error al ejecutar el comando: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TerminalApp()
    window.show()
    sys.exit(app.exec_())
