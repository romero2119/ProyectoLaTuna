#!/usr/bin/env python
# Diagnostico completo de email
# Uso: python email_diagnostico.py

import os
import sys
import subprocess

print("=" * 80)
print("DIAGNOSTICO COMPLETO DE EMAIL")
print("=" * 80)

# Test 1: Python basico
print("\n[PASO 1/4] Test simple de SMTP (sin Django)")
print("-" * 80)

result = subprocess.run(
    [sys.executable, "simple_email_test.py"],
    capture_output=False
)

if result.returncode != 0:
    print("\nERROR: El test simple fallo")
    print("Verifica que:")
    print("  1. Tengas internet conectado")
    print("  2. La contraseña de Gmail sea correcta")
    print("  3. Hayas generado contraseña de aplicacion en https://myaccount.google.com/apppasswords")
    sys.exit(1)

# Test 2: Django + Email
print("\n[PASO 2/4] Test con Django")
print("-" * 80)

try:
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    from django.conf import settings
    print(f"✓ Django cargado correctamente")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  EMAIL_TIMEOUT: {getattr(settings, 'EMAIL_TIMEOUT', 10)}")
    
except Exception as e:
    print(f"✗ Error al cargar Django: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Enviar email con Django
print("\n[PASO 3/4] Enviar email con Django")
print("-" * 80)

try:
    from django.core.mail import send_mail
    
    send_mail(
        subject='[DIAGNOSTICO] Test Django - Sociedad Creativa',
        message='Este es un email de prueba con Django.\n\nSi recibes este correo, Django puede enviar emails correctamente.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False,
        timeout=settings.EMAIL_TIMEOUT,
    )
    print("✓ Email enviado con Django exitosamente")
    
except Exception as e:
    print(f"✗ Error al enviar email con Django: {type(e).__name__}")
    print(f"  Detalles: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Probar comando Django
print("\n[PASO 4/4] Verificar comando verificar_vencimientos")
print("-" * 80)

try:
    from app.models import Producto, Notificacion
    from app.utils_email import enviar_alerta_stock_bajo, enviar_alerta_vencimiento
    
    # Obtener un producto de prueba
    producto = Producto.objects.first()
    
    if producto:
        print(f"✓ BD conectada correctamente")
        print(f"  Total de productos: {Producto.objects.count()}")
        print(f"  Total de notificaciones: {Notificacion.objects.count()}")
        print(f"\n  Producto de prueba: {producto.nombre}")
        print(f"  Stock: {producto.stock}")
        print(f"  Vencimiento: {producto.fecha_vencimiento}")
    else:
        print("⚠ Advertencia: No hay productos en la BD")
        
except Exception as e:
    print(f"✗ Error al conectar BD: {type(e).__name__}")
    print(f"  Detalles: {str(e)}")
    sys.exit(1)

print("\n" + "=" * 80)
print("DIAGNOSTICO COMPLETADO EXITOSAMENTE")
print("=" * 80)
print("""
El sistema de email esta funcionando correctamente.

PROXIMOS PASOS:
1. Verifica que hayas recibido 2 emails de prueba
2. Ejecuta: python manage.py verificar_vencimientos
3. Si es necesario, configura el Programador de Tareas
4. Consulta logs en: logs/notificaciones.log

Si falta algun email, revisa:
- Gmail en carpeta SPAM
- Verifica que EMAIL_HOST_PASSWORD sea correcto
- Usa contraseña de aplicacion, NO contraseña de Gmail
""")
