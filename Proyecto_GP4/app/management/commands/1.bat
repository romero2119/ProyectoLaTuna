@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM Script para Enviar Notificaciones por Email (Stock Bajo y Vencimientos)
REM ============================================================================

echo [INFO] Ruta del proyecto: C:\Users\dd573\Desktop\Proyecto\.venv\Scripts

cd C:\Users\dd573\Desktop\Proyecto\.venv\Scripts

call activate.bat
echo listos

cd C:\Users\dd573\Desktop\Proyecto\Proyecto_GP4
python manage.py enviar_notificaciones

   
exit /b 0