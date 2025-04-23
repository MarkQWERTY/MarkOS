# 🌐 MarkOS - Sistema Operativo Minimalista  

**📌 Un SO educativo con interfaz intuitiva y herramientas integradas**  

![MarkOS Logo](https://raw.githubusercontent.com/MarkQWERTY/MarkOS/main/assets/logo.png)  

🔹 [**Jump to English Version**](#-markos---minimalist-operating-system)  

---

## 🖥️ **Interfaz Principal (`interfaz/main.py`)**  
El corazón del sistema, con:  
- **🔄 Sistema modular** para cargar aplicaciones (navegador, calculadora, etc.)  
- **🎨 Gestión de temas** integrada (colores y disposición visual)  
- **📟 Barra de estado** con información del sistema  
- **⌨️ Soporte para entrada/salida** mediante librerías estándar de Python  

### 📚 **Librerías requeridas**:  
```bash
# Para la interfaz principal:
pip install pygments prompt_toolkit

# Para el navegador web (webs.py):
pip install requests beautifulsoup4

# Para la calculadora (calc.py):
pip install numpy  # Opcional para operaciones avanzadas
```

---

## 🛠️ **Aplicaciones Integradas**  

### 🌍 **Navegador Web (`webs.py`)**  
- **📡 Soporte para HTTP/HTTPS básico**  
- **🔍 Parser de HTML simplificado** (usando BeautifulSoup)  
- **📂 Historial de navegación local**  

### 🧮 **Calculadora (`calc.py`)**  
- **🔢 Operaciones básicas** (+, -, *, /)  
- **📊 Funciones avanzadas** (logaritmos, potencias)  
- **📈 Modo científico** (activado con `--sci`)  

### 🚀 **Ejecutador de Comandos (`ejecutar.py`)**  
- **⚡ Ejecuta archivos `.py` y `.sh`**  
- **📂 Navegación por directorios**  
- **🔧 Permisos básicos** (lectura/escritura)  

---

## ⚙️ **Instalación Automatizada**  
Ejecuta el instalador para configurar todo:  
```bash
chmod +x installer.sh  
./installer.sh  # ✔️ Instala dependencias y configura el entorno
```

---

## 📌 ¿Cómo Contribuir?  
1. 🐞 Reporta bugs en [Issues](https://github.com/MarkQWERTY/MarkOS/issues)  
2. 💡 Sugiere nuevas features  
3. 🛠️ Envía un *Pull Request*  

---

# 🌐 **MarkOS - Minimalist Operating System**  

**📌 An educational OS with intuitive UI & built-in tools**  

🔹 [**Versión en español**](#-markos---sistema-operativo-minimalista)  

---

## 🖥️ **Main Interface (`interfaz/main.py`)**  
The system core features:  
- **🔄 Modular design** to load apps (browser, calculator, etc.)  
- **🎨 Built-in theme engine** (colors & layout)  
- **📟 Status bar** with system info  
- **⌨️ I/O handling** via Python standard libraries  

### 📚 **Required Libraries**:  
```bash
# For main interface:
pip install pygments prompt_toolkit

# For web browser (webs.py):
pip install requests beautifulsoup4

# For calculator (calc.py):
pip install numpy  # Optional for advanced math
```

---

## 🛠️ **Built-in Apps**  

### 🌍 **Web Browser (`webs.py`)**  
- **📡 Basic HTTP/HTTPS support**  
- **🔍 Simplified HTML parser** (BeautifulSoup-based)  
- **📂 Local browsing history**  

### � **Calculator (`calc.py`)**  
- **🔢 Basic operations** (+, -, *, /)  
- **📊 Advanced functions** (logarithms, powers)  
- **📈 Scientific mode** (enable with `--sci`)  

### 🚀 **Command Runner (`ejecutar.py`)**  
- **⚡ Runs `.py` & `.sh` files**  
- **📂 Directory navigation**  
- **🔧 Basic permissions** (read/write)  

---

## ⚙️ **Auto-Installation**  
Run the installer to set up everything:  
```bash
chmod +x installer.sh  
./installer.sh  # ✔️ Sets up dependencies & environment
```

---

## 📌 How to Contribute?  
1. 🐞 Report bugs in [Issues](https://github.com/MarkQWERTY/MarkOS/issues)  
2. 💡 Suggest new features  
3. 🛠️ Submit a *Pull Request*  

--- 

**🎯 ¡Simple, educativo y extensible! / Simple, educational & extensible!**
