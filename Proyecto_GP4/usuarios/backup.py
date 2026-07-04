import os
import subprocess
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from app.views.Backup.backup import generar_archivo_descarga
from django.contrib import messages
from django.shortcuts import redirect


# ========== OBTENER DATOS DE LA BD ==========
def obtener_credenciales_mysql():
    """Obtiene las credenciales de MySQL desde settings.py"""
    db_config = settings.DATABASES["default"]
    return {
        "host": db_config.get("HOST", "localhost"),
        "user": db_config.get("USER", "root"),
        "password": db_config.get("PASSWORD", " "),
        "database": db_config.get("NAME", "la_tuna"),
        "port": db_config.get("PORT", 3306),
        "mysql_path": r"C:\Program Files\MySQL\MySQL Server 8.0\bin",
    }


def probar_conexion_mysql():
    """Prueba la conexión a MySQL"""
    creds = obtener_credenciales_mysql()
    try:
        cmd = [
            os.path.join(creds["mysql_path"], "mysql.exe"),
            "-h",
            creds["host"],
            "-u",
            creds["user"],
            "-P",
            str(creds["port"]),
            "--password=" + creds["password"],
            "-e",
            "SELECT 1;",
            creds["database"],
        ]

        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        return resultado.returncode == 0
    except:
        return False


# ========== VISTA PARA MOSTRAR OPCIONES DE RESPALDO ==========
def backup_usuarios(request):
    if not validar_password_backup(request):
        messages.error(
            request, "la contraseña de respaldo es incorrecta intentelo nuevamente"
        )
        return redirect('app:backup')
    """Exporta solo los datos de la tabla usuario"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    if not probar_conexion_mysql():
        return JsonResponse({"error": "No se puede conectar a MySQL"}, status=400)

    try:
        creds = obtener_credenciales_mysql()
        cmd = [
            os.path.join(creds["mysql_path"], "mysqldump.exe"),
            "-h",
            creds["host"],
            "-u",
            creds["user"],
            "-P",
            str(creds["port"]),
            "--password=" + creds["password"],
            creds["database"],
            "perfil_usuario",  # solo esta tabla
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if resultado.returncode != 0:
            raise Exception(f"Error mysqldump: {resultado.stderr}")

        sql_content = (
            f"-- Backup usuarios\n-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            + resultado.stdout
        )
        return generar_archivo_descarga(sql_content, "backup_usuarios")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def validar_password_backup(request):

    password = request.POST.get("backup_password")
    print("PASSWORD:", password)
    return password == settings.BACKUP_PASSWORD