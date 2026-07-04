#!/usr/bin/env python
# Script independiente para probar email (sin requerir BD)
# Uso: python email_test.py

import os
import sys
import django
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.conf import settings

print("=" * 80)
print("TEST DE CONFIGURACION DE EMAIL")
print("=" * 80)

print("\n[1/4] VERIFICANDO CONFIGURACION DE EMAIL")
print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"  EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NO CONFIGURADA'}")
print(f"  EMAIL_TIMEOUT: {getattr(settings, 'EMAIL_TIMEOUT', 10)}")

# Test 1: Conexion SMTP directa
print("\n[2/4] PROBANDO CONEXION SMTP DIRECTA")
try:
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=settings.EMAIL_TIMEOUT)
    server.starttls()
    print(f"  OK - Conexion exitosa a {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
except smtplib.SMTPException as e:
    print(f"  ERROR - SMTP Error: {str(e)}")
    sys.exit(1)
except Exception as e:
    print(f"  ERROR - {type(e).__name__}: {str(e)}")
    sys.exit(1)

# Test 2: Autenticacion
print("\n[3/4] PROBANDO AUTENTICACION")
try:
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    print(f"  OK - Autenticacion exitosa como {settings.EMAIL_HOST_USER}")
except smtplib.SMTPAuthenticationError:
    print(f"  ERROR - Credenciales incorrectas")
    print(f"  Usuario: {settings.EMAIL_HOST_USER}")
    print(f"  Contraseña: [{len(settings.EMAIL_HOST_PASSWORD)} caracteres]")
    print("\n  SOLUCION:")
    print("  1. Ve a: https://myaccount.google.com/apppasswords")
    print("  2. Genera una contraseña de aplicacion")
    print("  3. Usa esa contraseña en EMAIL_HOST_PASSWORD")
    sys.exit(1)
except Exception as e:
    print(f"  ERROR - {type(e).__name__}: {str(e)}")
    sys.exit(1)

# Test 3: Enviar email
print("\n[4/4] ENVIANDO EMAIL DE PRUEBA")
try:
    mensaje = MIMEMultipart()
    mensaje['From'] = settings.EMAIL_HOST_USER
    mensaje['To'] = settings.EMAIL_HOST_USER
    mensaje['Subject'] = '[PRUEBA] Sistema de Notificaciones - Sociedad Creativa'
    
    cuerpo = """Este es un email de prueba del sistema de notificaciones.

Si recibiste este correo, el sistema SMTP funciona correctamente.

---
Sistema: Django 5.2.8
Fecha: 2026-04-14
"""
    
    mensaje.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
    
    # Enviar
    server.send_message(mensaje)
    server.quit()
    
    print(f"  OK - Email enviado exitosamente a {settings.EMAIL_HOST_USER}")
    print(f"\n  Revisa tu bandeja de entrada en los proximos segundos...")
    
except Exception as e:
    print(f"  ERROR - {type(e).__name__}: {str(e)}")
    try:
        server.quit()
    except:
        pass
    sys.exit(1)

print("\n" + "=" * 80)
print("TEST COMPLETADO EXITOSAMENTE")
print("=" * 80)
print("\nProximos pasos:")
print("  1. Verifica que recibiste el email")
print("  2. Ejecuta: python manage.py verificar_vencimientos")
print("  3. Si el email se envia, configura el Programador de Tareas")
print(f"\nEnviar a:")
print(f"  Remitente (FROM): {settings.EMAIL_HOST_USER}")
print(f"  Destinatario (TO): {settings.EMAIL_HOST_USER}")

