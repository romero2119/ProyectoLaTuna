@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM Script para Enviar Notificaciones por Email (Stock Bajo y Vencimientos)
REM ============================================================================
REM Este script:
REM - Detecta la ruta del proyecto automáticamente
REM - Busca el entorno virtual en múltiples ubicaciones
REM - Activa el entorno virtual
REM - Ejecuta el comando de Django para enviar notificaciones
REM - Registra logs de ejecución
REM ============================================================================

REM Obtener la ruta donde está el script
set "SCRIPT_DIR=%~dp0"

REM Navegar a la raíz del proyecto (3 directorios hacia arriba)
cd /d "%SCRIPT_DIR%"
cd ..
cd ..
cd ..

REM Obtener ruta absoluta del proyecto
for /f "delims=" %%I in ('cd') do set "PROYECTO_DIR=%%I"

echo.
echo ============================================================================
echo ENVIANDO NOTIFICACIONES POR EMAIL
echo ============================================================================
echo [%date% %time%] Iniciando proceso...
echo [INFO] Ruta del proyecto: %PROYECTO_DIR%

REM Validar que existe manage.py
if not exist "%PROYECTO_DIR%\manage.py" (
    echo [ERROR] No se encontro manage.py en: %PROYECTO_DIR%
    echo [INFO] Por favor, ejecuta este script desde la carpeta del proyecto o verifica su ubicacion
    echo [DEBUG] Script dir: %SCRIPT_DIR%
    pause
    exit /b 1
)

REM Crear carpeta de logs si no existe
if not exist "%PROYECTO_DIR%\logs" mkdir "%PROYECTO_DIR%\logs"

REM Forzar UTF-8
chcp 65001 > nul

REM Detectar y validar entorno virtual
echo [INFO] Buscando entorno virtual...

REM Intentar ubicación 1: .venv en la carpeta del proyecto
set "C:\Users\dd573\Desktop\Proyecto\.venv\Scripts"
if exist "!VENV_PATH!" (
    echo [INFO] Entorno virtual encontrado en: !VENV_PATH!
) else (
    REM Intentar ubicación 2: .venv en la carpeta padre
    set "VENV_PATH=%PROYECTO_DIR%..\Proyecto\.venv"
    if exist "!VENV_PATH!" (
        echo [INFO] Entorno virtual encontrado en: !VENV_PATH!
    ) else (
        REM Intentar ubicación 3: .venv en la carpeta padre (genérico)
        cd /d "%PROYECTO_DIR%.."
        for /f "delims=" %%I in ('cd') do set "PADRE_DIR=%%I"
        set "VENV_PATH=!PADRE_DIR!\.venv"
        
        if exist "!VENV_PATH!" (
            echo [INFO] Entorno virtual encontrado en: !VENV_PATH!
        ) else (
            echo [ERROR] No se encontro la carpeta .venv en ninguna ubicacion esperada:
            echo   - %PROYECTO_DIR%\.venv
            echo   - !PADRE_DIR!\.venv
            echo [INFO] Asegurate de que el proyecto tiene un entorno virtual activado
            pause
            exit /b 1
        )
    )
)

REM Activar entorno virtual usando ruta absoluta
echo [INFO] Activando entorno virtual desde: !VENV_PATH!
call "!VENV_PATH!\Scripts\activate.bat"

if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    echo [DEBUG] Ruta: !VENV_PATH!\Scripts\activate.bat
    pause
    exit /b 1
)

echo [INFO] Entorno virtual activado correctamente
echo [INFO] Ejecutando: python manage.py enviar_notificaciones
echo.

REM Ejecutar comando de Django desde el directorio del proyecto
cd /d "%PROYECTO_DIR%"
python manage.py enviar_notificaciones >> "logs\notificaciones.log" 2>&1

if errorlevel 1 (
    echo [ERROR] Fallo la ejecucion del comando
    echo [INFO] Revisa los logs en: %PROYECTO_DIR%\logs\notificaciones.log
    pause
    exit /b 1
)

echo [%date% %time%] Proceso completado exitosamente
echo ============================================================================
echo.

exit /b 0
