import tkinter as tk
from tkinter import font
import math

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.resizable(0, 0)
        self.root.configure(bg='#f0f0f0')
        
        # Configurar fuentes
        self.fuente = font.Font(size=12)
        self.fuente_botones = font.Font(size=10)
        self.fuente_pantalla = font.Font(size=18)
        
        # Variables
        self.operacion = ""
        self.memoria = None
        # Pantalla de la calculadora
        self.pantalla = tk.Entry(root, font=self.fuente_pantalla, borderwidth=3, 
                                relief="sunken", justify="right", state='readonly',
                                bg='#ffffff', fg='#333333')
        self.pantalla.grid(row=1, column=0, columnspan=6, padx=10, pady=10, ipady=15, sticky="nsew")
        # Fila superior con funciones trigonométricas inversas
        botones_superiores = [
            ('asin', 2, 0, '#ccffff'), ('acos', 2, 1, '#ccffff'), ('atan', 2, 2, '#ccffff'),
            ('π', 2, 3, '#e6ccff'), ('M+', 2, 4, '#ffcc99'), ('MC', 2, 5, '#ffcc99')
        ]
        
        for (texto, fila, columna, color) in botones_superiores:
            tk.Button(root, text=texto, font=self.fuente_botones, padx=5, pady=8, 
                     bg=color, relief="raised", command=lambda t=texto: self.click_boton(t)
                     ).grid(row=fila, column=columna, sticky="nsew", padx=2, pady=2)
        
        
        
        # Fila inferior a la pantalla con funciones trigonométricas
        botones_trig = [
            ('sin', 3, 0, '#e6ccff'), ('cos', 3, 1, '#e6ccff'), ('tan', 3, 2, '#e6ccff'),
            ('log', 3, 3, '#e6ccff'), ('ln', 3, 4, '#e6ccff'), ('MR', 3, 5, '#ffcc99')
        ]
        
        for (texto, fila, columna, color) in botones_trig:
            tk.Button(root, text=texto, font=self.fuente_botones, padx=5, pady=8, 
                     bg=color, relief="raised", command=lambda t=texto: self.click_boton(t)
                     ).grid(row=fila, column=columna, sticky="nsew", padx=2, pady=2)
        
        # Creación de botones numéricos y operaciones básicas
        self.crear_botones_numericos()
        
        # Configurar el grid
        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.root.grid_columnconfigure(i, weight=1)
    
    def crear_botones_numericos(self):
        # Configuración de botones básicos
        botones_basicos = [
            ('7', 4, 0, '#e6e6e6'), ('8', 4, 1, '#e6e6e6'), ('9', 4, 2, '#e6e6e6'), ('/', 4, 3, '#d9d9d9'), ('C', 4, 4, '#ff9999'), ('⌫', 4, 5, '#ff9999'),
            ('4', 5, 0, '#e6e6e6'), ('5', 5, 1, '#e6e6e6'), ('6', 5, 2, '#e6e6e6'), ('*', 5, 3, '#d9d9d9'), ('(', 5, 4, '#ccccff'), (')', 5, 5, '#ccccff'),
            ('1', 6, 0, '#e6e6e6'), ('2', 6, 1, '#e6e6e6'), ('3', 6, 2, '#e6e6e6'), ('-', 6, 3, '#d9d9d9'), ('x²', 6, 4, '#ccccff'), ('√', 6, 5, '#ccccff'),
            ('0', 7, 0, '#e6e6e6'), ('.', 7, 1, '#e6e6e6'), ('=', 7, 2, '#99ccff'), ('+', 7, 3, '#d9d9d9'), ('x^y', 7, 4, '#ccccff'), ('n!', 7, 5, '#ccccff')
        ]
        
        # Crear botones básicos
        for (texto, fila, columna, color) in botones_basicos:
            boton = tk.Button(self.root, text=texto, font=self.fuente, 
                             padx=10, pady=10, bg=color, relief="raised",
                             command=lambda t=texto: self.click_boton(t))
            boton.grid(row=fila, column=columna, sticky="nsew", padx=2, pady=2)
    
    def click_boton(self, valor):
        if valor == 'C':
            self.operacion = ""
        elif valor == '⌫':
            self.operacion = self.operacion[:-1]
        elif valor == '=':
            try:
                # Reemplazar símbolos especiales antes de evaluar
                expr = self.operacion.replace('^', '**').replace('√', 'math.sqrt')
                resultado = str(eval(expr))
                self.operacion = resultado
            except Exception as e:
                self.operacion = "Error"
        elif valor == 'x²':
            self.operacion += '**2'
        elif valor == 'x^y':
            self.operacion += '^'
        elif valor == '√':
            self.operacion += 'math.sqrt('
        elif valor == 'n!':
            try:
                num = eval(self.operacion)
                resultado = str(math.factorial(int(num)))
                self.operacion = resultado
            except:
                self.operacion = "Error"
        elif valor == 'sin':
            self.operacion += 'math.sin(math.radians('
        elif valor == 'cos':
            self.operacion += 'math.cos(math.radians('
        elif valor == 'tan':
            self.operacion += 'math.tan(math.radians('
        elif valor == 'asin':
            self.operacion += 'math.degrees(math.asin('
        elif valor == 'acos':
            self.operacion += 'math.degrees(math.acos('
        elif valor == 'atan':
            self.operacion += 'math.degrees(math.atan('
        elif valor == 'log':
            self.operacion += 'math.log10('
        elif valor == 'ln':
            self.operacion += 'math.log('
        elif valor == 'π':
            self.operacion += str(math.pi)
        elif valor == 'M+':
            try:
                self.memoria = eval(self.operacion)
            except:
                self.operacion = "Error"
        elif valor == 'MR':
            if self.memoria is not None:
                self.operacion += str(self.memoria)
        elif valor == 'MC':
            self.memoria = None
        else:
            # Concatenar el valor al string de la operación
            self.operacion += str(valor)
        
        # Actualizar pantalla
        self.actualizar_pantalla()
    
    def actualizar_pantalla(self):
        # Habilitar temporalmente para modificar
        self.pantalla.config(state='normal')
        self.pantalla.delete(0, tk.END)
        self.pantalla.insert(0, self.operacion)
        self.pantalla.config(state='readonly')

if __name__ == "__main__":
    root = tk.Tk()
    calculadora = Calculadora(root)
    root.mainloop()