REM Verificar Notificaciones - Script de Diagnostico
REM Uso: Ejecutar en PowerShell para verificar que todo esté configurado

@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

set PROJECT_ROOT=E:\Docs\OneDrive - Sociedad creativa boyaca s.a\Escritorio\Proyecto\Proyecto_GP4
set VENV_PATH=%PROJECT_ROOT%\.venv
set PYTHON=%VENV_PATH%\Scripts\python.exe

echo.
echo ================================================================================
echo DIAGNOSTICO DEL SISTEMA DE NOTIFICACIONES
echo ================================================================================
echo.

REM Verificar .venv
echo [1/5] Verificando entorno virtual...
if exist "%VENV_PATH%" (
    echo   Status: OK - Entorno virtual encontrado
) else (
    echo   Status: ERROR - Entorno virtual no encontrado en %VENV_PATH%
    exit /b 1
)

REM Verificar Python
echo.
echo [2/5] Verificando Python...
if exist "%PYTHON%" (
    echo   Status: OK - Python encontrado
    "%PYTHON%" --version
) else (
    echo   Status: ERROR - Python no encontrado en %PYTHON%
    exit /b 1
)

REM Verificar archivos críticos
echo.
echo [3/5] Verificando archivos necesarios...
set OK=1
for %%F in (manage.py config\settings.py app\signals.py app\utils_email.py) do (
    if exist "%PROJECT_ROOT%\%%F" (
        echo   OK: %%F
    ) else (
        echo   ERROR: %%F no encontrado
        set OK=0
    )
)

if !OK! equ 0 (
    exit /b 1
)

REM Verificar carpeta de logs
echo.
echo [4/5] Verificando carpeta de logs...
if exist "%PROJECT_ROOT%\logs" (
    echo   Status: OK - Carpeta logs existe
) else (
    echo   Status: CREAR - Creando carpeta logs...
    mkdir "%PROJECT_ROOT%\logs"
)

REM Prueba de configuración
echo.
echo [5/5] Probando configuracion de Django...
cd /d "%PROJECT_ROOT%"
"%PYTHON%" -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); import django; django.setup(); from django.conf import settings; print('  EMAIL_BACKEND:', settings.EMAIL_BACKEND); print('  EMAIL_HOST:', settings.EMAIL_HOST); print('  EMAIL_TIMEOUT:', getattr(settings, 'EMAIL_TIMEOUT', 'No configurado'))"

echo.
echo ================================================================================
echo DIAGNOSTICO COMPLETADO
echo ================================================================================
echo.
echo Proximos pasos:
echo   1. Revisar: SOLUCION_NOTIFICACIONES.md
echo   2. Probar:  python email_test.py
echo   3. Config:  Programador de Tareas (ver INSTRUCCIONES_NOTIFICACIONES.md)
echo.

pause
