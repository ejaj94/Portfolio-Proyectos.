@echo off
title Mantenimiento - Limpieza de Archivos Temporales
echo Iniciando escaneo de documentos antiguos en app_entregador...

REM Forzar a la consola a posicionarse en la carpeta donde reside este archivo .bat
cd /d "%~dp0"

REM Ejecutar el script usando el intérprete de Python de tu entorno virtual unificado
..\\.venv\\Scripts\\python.exe -m services.cleanup

if %ERRORLEVEL% EQU 0 (
    echo [OK] Limpieza completada con exito.
) else (
    echo [ERROR] Hubo un problema al ejecutar el script de limpieza.
)

pause
