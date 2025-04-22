import tkinter as tk
from tkinter import messagebox
import time
import os
import subprocess
import psutil

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
                    # Primero restaurar si está minimizada
                    win32gui.ShowWindow(window, win32con.SW_RESTORE)
                    # Luego traer al frente
                    win32gui.SetForegroundWindow(window)
                    # Forzar el enfoque (técnica adicional)
                    win32gui.BringWindowToTop(window)
                    win32gui.SetWindowPos(window, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                    win32gui.SetWindowPos(window, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
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
    
    def get_window_state(self, window_title):
        """Obtiene el estado de una ventana"""
        try:
            if os.name == 'nt':
                import win32gui
                window = win32gui.FindWindow(None, window_title)
                if window:
                    return "exists"
                return "not_found"
            else:
                result = subprocess.run(["xdotool", "search", "--name", window_title], 
                                      capture_output=True, text=True)
                return "exists" if result.stdout else "not_found"
        except Exception as e:
            print(f"Error al verificar estado de ventana: {e}")
            return "error"

class MarkOS:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkOS")
        self.root.attributes('-fullscreen', True)
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        
        self.window_manager = WindowManager()
        self.open_apps = {}
        self.app_counter = 0

        self.PYROUTE = "python3"
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
            ("🌐 Navegador", lambda: self.open_app("webs")),
            ("📁 Archivos", lambda: self.open_app("file")),
            ("📟 Terminal", lambda: self.open_app("terminal")),
            ("🧮 Calculadora", lambda: self.open_app("calc")),
            ("Ejecutar", lambda: self.open_app("ejecutar")),
            ("Spotify", lambda: self.open_app("spotify")),
            ("Telegram", lambda: self.open_app("telegram-desktop")),
            ("Office", lambda: self.open_app("docs"))
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
        self.taskbar = tk.Frame(self.root, bg='#2d2d2d', height=75)
        self.taskbar.grid(row=1, column=0, sticky="sew")

        start_btn = tk.Menubutton(
            self.taskbar,
            text=" 🏠 ",
            bg='#2d2d2d',
            fg='white',
            font=('Segoe UI', 10),
            bd=0,
            relief='flat',
            padx=10,
            pady=0
        )
        start_menu = tk.Menu(start_btn, tearoff=0, bg='#2d2d2d', fg='white')

        power_menu = tk.Menu(start_menu, tearoff=0, bg='#2d2d2d', fg='white')
        power_menu.add_command(label="Apagar", command=self.shutdown)
        power_menu.add_command(label="Reiniciar", command=self.reboot)

        start_menu.add_cascade(label="Energía", menu=power_menu)
        start_menu.add_command(label="Salir", command=self.root.quit)
        start_btn.config(menu=start_menu)
        start_btn.pack(side='left', padx=(5,0))

        self.apps_frame = tk.Frame(self.taskbar, bg='#2d2d2d', height=80)
        self.apps_frame.pack(side='left', padx=(5,0), fill='y')
        
        self.time_label = tk.Label(
            self.taskbar,
            font=('Segoe UI', 9),
            bg='#2d2d2d',
            fg='white',
            padx=10,
            pady=0
        )
        self.time_label.pack(side='right')

    def add_app_to_taskbar(self, app_name, process):
        app_id = self.app_counter
        self.app_counter += 1
        
        btn_frame = tk.Frame(self.apps_frame, bg='#2d2d2d', padx=0, pady=0)
        btn_frame.pack(side='left', padx=(0,1))
        
        btn = tk.Button(
            btn_frame,
            text=f" {app_name[:12]} ",
            bg='#3e3e3e',
            fg='white',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat',
            padx=10,
            pady=2,
            command=lambda: self.toggle_application(app_id)
        )
        btn.pack(side='left')
        
        close_btn = tk.Button(
            btn_frame,
            text="×",
            bg='#3e3e3e',
            fg='white',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat',
            padx=10,
            pady=0,
            width=2,
            command=lambda: self.close_app(app_id)
        )
        close_btn.pack(side='left', padx=(0,2))
        
        self.open_apps[app_id] = {
            "name": app_name,
            "process": process,
            "button": btn,
            "close_btn": close_btn,
            "frame": btn_frame,
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
                app_info["button"].config(bg='#2d2d2d')  # Cambia color cuando está minimizado
            else:
                self.window_manager.focus_window(app_name)
                app_info["window_state"] = "visible"
                app_info["button"].config(bg='#3e3e3e')  # Color normal cuando está visible
                # Forzar el enfoque de la ventana principal de MarkOS
                self.root.attributes('-topmost', True)
                self.root.attributes('-topmost', False)
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
            
            app_info["frame"].destroy()
            del self.open_apps[app_id]

    def update_clock(self):
        self.time_label.config(text=time.strftime("%H:%M | %d/%m/%Y"))
        self.root.after(1000, self.update_clock)

    def open_settings(self):
        messagebox.showinfo("Configuración", "Sistema de configuración abierto")

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
                        process = subprocess.Popen(["nautilus", folder_path])
                    self.add_app_to_taskbar("Archivos", process)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir la carpeta: {str(e)}")
                    
            elif module_name == "spotify":
                try:
                    if os.name == 'nt':
                        process = subprocess.Popen(["spotify.exe"])
                    else:
                        process = subprocess.Popen(["spotify", "--title=Spotify"])
                    self.add_app_to_taskbar("Spotify", process)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir Spotify: {str(e)}")
                    
            elif module_name == "telegram-desktop":
                try:
                    if os.name == 'nt':
                        process = subprocess.Popen(["telegram.exe"])
                    else:
                        process = subprocess.Popen(["telegram-desktop", "--title=Telegram"])
                    self.add_app_to_taskbar("Telegram", process)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir Telegram: {str(e)}")       
            else:
                script_path = os.path.join(self.SYS_PATH, f"{module_name}.py")
                if os.name == 'nt':
                    process = subprocess.Popen(["python", script_path])
                else:
                    process = subprocess.Popen(["python3", script_path])
                self.add_app_to_taskbar(module_name.capitalize(), process)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la aplicación: {str(e)}")

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