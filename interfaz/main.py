import tkinter as tk
from tkinter import messagebox
import time
import os
import subprocess
from PIL import Image, ImageTk

class MarkOS:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkOS")
        self.root.attributes("-fullscreen", True)
        self.root.configure()

        # Diccionario para rastrear aplicaciones abiertas
        self.open_apps = {}  # {app_id: {"name": str, "frame": tk.Frame, "close_fn": callable}}
        self.app_counter = 0  # Contador para IDs únicos

        self.PYROUTE =  "C:/Users/cuent/AppData/Local/Microsoft/WindowsApps/python3.11.exe"
        self.SYS_PATH = os.path.dirname(os.path.abspath(__file__))
        self.BG_COLOR = 'khaki1'
        self.BTN_COLOR = 'gray'
        self.BTN_HOVER = 'gray30'
        self.root.configure(bg=self.BG_COLOR)

        # Configuración del grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_apps_section()
        self.create_taskbar()
        self.update_clock()

    def create_apps_section(self):
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR, bd=0)
        main_frame.grid(row=0, column=0, sticky="nsew")

        inner_frame = tk.Frame(main_frame, bg=self.BG_COLOR, bd=0)
        inner_frame.pack(expand=True, padx=100, pady=100)

        for i in range(2):
            inner_frame.grid_rowconfigure(i, weight=1)
            inner_frame.grid_columnconfigure(i, weight=1)

        apps = [
            ("⚙️ Configuración", self.open_settings),
            ("🌐 Navegador", lambda: self.open_app("Navegador", "webs")),
            ("📁 Archivos", self.open_file_manager),
            ("📟 Terminal", self.open_terminal),
            ("🧮 Calculadora", lambda: self.open_app("Calculadora", "calc"))
        ]

        btn_style = {
            'font': ('Segoe UI', 18),
            "bg": self.BTN_COLOR,
            'fg': 'white',
            'bd': 0,
            'relief': 'flat',
            'highlightthickness': 0
        }

        for i, (app, command) in enumerate(apps):
            row, col = divmod(i, 2)
            btn = tk.Button(inner_frame, text=app, **btn_style, command=command)
            btn.grid(row=row, column=col, padx=30, pady=30, sticky="nsew")

            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='gray30'))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.BTN_COLOR))

    def create_taskbar(self):
        # Barra de tareas más alta (120px) con mejor diseño
        self.taskbar = tk.Frame(self.root, bg='seagreen2', height=120)
        self.taskbar.grid(row=1, column=0, sticky="sew")

        # Botón Inicio con menú (diseño mejorado)
        start_btn = tk.Menubutton(
            self.taskbar,
            text=" Inicio ",
            bg='seagreen3',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            relief='flat',
            padx=10,
            pady=5
        )
        start_menu = tk.Menu(start_btn, tearoff=0, bg='gray20', fg='white')

        power_menu = tk.Menu(start_menu, tearoff=0, bg='gray20', fg='white')
        power_menu.add_command(label="Apagar", command=self.shutdown)
        power_menu.add_command(label="Reiniciar", command=self.reboot)

        start_menu.add_cascade(label="Energía", menu=power_menu)
        start_menu.add_command(label="Salir", command=self.root.quit)
        start_btn.config(menu=start_menu)
        start_btn.pack(side='left', padx=10, pady=10)

        # Frame para aplicaciones abiertas (con scrollbar si es necesario)
        self.apps_container = tk.Frame(self.taskbar, bg='seagreen2')
        self.apps_container.pack(side='left', expand=True, fill='both')

        # Hora y fecha con mejor diseño
        self.time_label = tk.Label(
            self.taskbar,
            font=('Segoe UI', 12, 'bold'),
            bg='seagreen3',
            fg='white',
            padx=15,
            pady=5
        )
        self.time_label.pack(side='right', padx=10, pady=10)

    def add_app_to_taskbar(self, app_name, close_command=None):
        """Añade una aplicación a la barra de tareas con botón de cierre"""
        app_id = f"{app_name}_{self.app_counter}"
        self.app_counter += 1

        # Frame para cada aplicación
        app_frame = tk.Frame(self.apps_container, bg='seagreen2')
        app_frame.pack(side='left', padx=5)

        # Botón de la aplicación
        app_btn = tk.Button(
            app_frame,
            text=app_name,
            bg='seagreen3',
            fg='white',
            font=('Segoe UI', 10),
            bd=0,
            relief='flat',
            padx=10,
            pady=5,
            command=lambda: self.focus_app(app_id)
        )
        app_btn.pack(side='left')

        # Botón de cerrar
        close_btn = tk.Button(
            app_frame,
            text=" × ",
            bg='seagreen3',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            relief='flat',
            command=lambda: self.close_app(app_id)
        )
        close_btn.pack(side='left', padx=(0,5))

        # Guardar referencia en el diccionario
        self.open_apps[app_id] = {
            "name": app_name,
            "frame": app_frame,
            "buttons": (app_btn, close_btn),
            "close_fn": close_command
        }

        return app_id

    def close_app(self, app_id):
        """Cierra una aplicación y la remueve de la barra de tareas"""
        if app_id in self.open_apps:
            app_data = self.open_apps[app_id]

            # try:
            #     subprocess.run(["taskkill", "/F", "/IM", app_id], check=True)
            #     print(f"Proceso {app_id} terminado.")
            # except subprocess.CalledProcessError:
            #     print(f"No se pudo terminar {app_id}.")

            # Eliminar widgets de la barra
            app_data["frame"].destroy()

            # Eliminar del diccionario
            del self.open_apps[app_id]

    def focus_app(self, app_id):
        """Enfoca la aplicación (placeholder para implementación futura)"""
        print(f"Enfocando aplicación: {app_id}")

    def update_clock(self):
        """Actualiza la hora en la barra de tareas"""
        self.time_label.config(text=time.strftime("%H:%M | %d/%m/%Y"))
        self.root.after(1000, self.update_clock)

    # Funciones de aplicaciones
    def open_settings(self):
        messagebox.showinfo("Configuración", "Sistema de configuración abierto")
        self.add_app_to_taskbar("Configuración")

    def open_file_manager(self):
        try:
            if os.name == 'nt':
                os.startfile(os.path.expanduser("~"))
            else:
                subprocess.Popen(["xdg-open", os.path.expanduser("~")])
            self.add_app_to_taskbar("Archivos")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el gestor de archivos: {str(e)}")

    def open_terminal(self):
        try:
            if os.name == 'nt':
                os.system("start cmd")
            else:
                subprocess.Popen(["x-terminal-emulator"])
            self.add_app_to_taskbar("Terminal")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la terminal: {str(e)}")

    def open_app(self, display_name, module_name):
        subprocess.Popen([f"{self.PYROUTE}", f"{self.SYS_PATH}/{module_name}.py"])
        app_id = self.add_app_to_taskbar(display_name, lambda: self.close_app(app_id))
        while True:
            comando = input("->")  # Simula una terminal tipo Unix
            if comando == f"salir {display_name}":
                self.close_app(app_id)
                break

    # Funciones de energía
    def shutdown(self):
        if messagebox.askyesno("Apagar", "¿Desea apagar el sistema?"):
            try:
                if os.name == 'nt':
                    os.system("shutdown /s /t 1")
                else:
                    os.system("shutdown now")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo apagar el sistema: {str(e)}")

    def reboot(self):
        if messagebox.askyesno("Reiniciar", "¿Desea reiniciar el sistema?"):
            try:
                if os.name == 'nt':
                    os.system("shutdown /r /t 1")
                else:
                    os.system("reboot")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo reiniciar el sistema: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkOS(root)
    root.mainloop()