#!/usr/bin/env python
# Script para probar email de forma muy simple
# Uso: python simple_email_test.py

import smtplib
from email.mime.text import MIMEText

# CONFIGURACION
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'juniosdavidllanos2@gmail.com'
EMAIL_PASSWORD = 'iwng zdpp mjyi kqif'  # Contraseña de aplicacion

print("=" * 80)
print("TEST SIMPLE DE EMAIL")
print("=" * 80)

print(f"\nIntentando conectar a: {EMAIL_HOST}:{EMAIL_PORT}")

try:
    # Conectar
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=10)
    print("✓ Conexion exitosa")
    
    # TLS
    server.starttls()
    print("✓ TLS iniciado")
    
    # Autenticar
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    print("✓ Autenticacion exitosa")
    
    # Crear email
    message = MIMEText("Este es un email de prueba")
    message['Subject'] = "[PRUEBA] Test Simple - Sociedad Creativa"
    message['From'] = EMAIL_USER
    message['To'] = EMAIL_USER
    
    # Enviar
    server.send_message(message)
    print("✓ Email enviado")
    
    # Cerrar
    server.quit()
    print("✓ Conexion cerrada")
    
    print("\n" + "=" * 80)
    print("STATUS: EXITO - EMAIL SE ENVIO CORRECTAMENTE")
    print("=" * 80)
    print(f"\nVerifica tu bandeja de entrada:")
    print(f"  De: {EMAIL_USER}")
    print(f"  Para: {EMAIL_USER}")
    print(f"  Asunto: [PRUEBA] Test Simple - Sociedad Creativa")
    
except smtplib.SMTPAuthenticationError:
    print("\n" + "=" * 80)
    print("ERROR: Credenciales incorrectas")
    print("=" * 80)
    print("\nSOLUCION:")
    print("1. Ve a: https://myaccount.google.com/apppasswords")
    print("2. Genera una contraseña de aplicacion")
    print("3. Actualiza EMAIL_PASSWORD en este script")
    
except Exception as e:
    print("\n" + "=" * 80)
    print(f"ERROR: {type(e).__name__}")
    print("=" * 80)
    print(f"Detalles: {str(e)}")
    import traceback
    traceback.print_exc()
