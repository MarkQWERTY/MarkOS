echo "Instalando Dependencias"
apt install toilet jq figlet python3 python3-pip python3-pyqt5 python3-pyqt5.qtsvg python3-pyqt5.qtwebengine python3-pyqt5.qtmultimedia python3-pyqt5.qtquickcontrols2 python3-pyqt5.qtwebchannel -y
echo "Instalando sistema operativo..."
git clone "https://github.com/MarkQWERTY/MarkOS"
echo "Instalacion terminada"
#Pregunta si quiere ejecutar el sistema operativo
echo "¿Desea ejecutar el sistema operativo? (s/n)"
read respuesta
if [ "$respuesta" = "s" ]; then
    echo "Ejecutando MarkOS..."
    cd MarkOS/interfaz
    python3 main.py
else
    echo "Saliendo del instalador."
fi
