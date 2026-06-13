@echo off
title Servidor Flask - Plataforma de Entregas Unificada
echo Lanzando entorno virtual y arrancando servidor principal...

REM Cambia al directorio raíz del proyecto si es necesario y ejecuta el app.py principal
cd /d "%~dp0"
..\\..\\.venv\\Scripts\\python.exe ..\\..\\app.py

pause
