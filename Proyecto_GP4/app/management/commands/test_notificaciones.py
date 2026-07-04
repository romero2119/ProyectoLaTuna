#!/usr/bin/env python
# app/management/commands/test_notificaciones.py
"""
Script para probar el sistema de notificaciones por correo.
Uso: python manage.py test_notificaciones
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from app.models import Producto, Notificacion
from app.utils_email import enviar_alerta_vencimiento, enviar_alerta_stock_bajo
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test del sistema de notificaciones por correo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--producto-id',
            type=int,
            help='ID del producto para testear',
        )
        parser.add_argument(
            '--tipo',
            choices=['stock', 'vencimiento'],
            help='Tipo de notificación a testear',
        )

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS("=" * 80))
            self.stdout.write(self.style.SUCCESS("TEST DE NOTIFICACIONES POR CORREO"))
            self.stdout.write(self.style.SUCCESS("=" * 80))
            
            # Verificar configuración de email
            self.stdout.write("\n[EMAIL CONFIG]")
            self.stdout.write(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
            self.stdout.write(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
            self.stdout.write(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
            self.stdout.write(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
            self.stdout.write(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            self.stdout.write(f"  EMAIL_TIMEOUT: {getattr(settings, 'EMAIL_TIMEOUT', 'No configurado')}")
            
            # Verificar logging
            self.stdout.write("\n[LOGGING CONFIG]")
            if hasattr(settings, 'LOGGING'):
                self.stdout.write(f"  LOGGING: Configurado")
            else:
                self.stdout.write(self.style.WARNING(f"  LOGGING: No configurado"))
            
            # Test 1: Enviar email de prueba
            self.stdout.write("\n" + "=" * 80)
            self.stdout.write("TEST 1: Enviar Email de Prueba")
            self.stdout.write("=" * 80)
            
            from django.core.mail import send_mail
            try:
                send_mail(
                    subject='[TEST] Sistema de Notificaciones - Sociedad Creativa',
                    message='Este es un email de prueba del sistema de notificaciones.\n\nSi recibiste este correo, el sistema SMTP funciona correctamente.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                    timeout=settings.EMAIL_TIMEOUT,
                )
                self.stdout.write(self.style.SUCCESS("OK - Email de prueba enviado"))
                logger.info("[TEST] Email de prueba enviado")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"ERROR: {str(e)}"))
                logger.error(f"[TEST ERROR] {type(e).__name__}: {str(e)}")
            
            # Test 2: Test de stock bajo detectado
            if options.get('producto_id') or options.get('tipo') == 'stock':
                self.stdout.write("\n" + "=" * 80)
                self.stdout.write("TEST 2: Notificación de Stock Bajo")
                self.stdout.write("=" * 80)
                
                if options.get('producto_id'):
                    try:
                        producto = Producto.objects.get(id_producto=options['producto_id'])
                    except Producto.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Producto ID {options['producto_id']} no encontrado"))
                        return
                else:
                    # Obtener el primer producto con stock bajo
                    producto = Producto.objects.filter(stock__lte=10).first()
                    if not producto:
                        self.stdout.write(self.style.WARNING("No hay productos con stock bajo para testear"))
                        return
                
                self.stdout.write(f"Producto: {producto.nombre}")
                self.stdout.write(f"Stock actual: {producto.stock}")
                
                resultado = enviar_alerta_stock_bajo(producto)
                if resultado:
                    self.stdout.write(self.style.SUCCESS(f"OK - Alerta de stock enviada"))
                else:
                    self.stdout.write(self.style.ERROR(f"ERROR - Fallo al enviar alerta de stock"))
            
            # Test 3: Test de vencimiento
            if options.get('tipo') == 'vencimiento' or options.get('producto_id'):
                self.stdout.write("\n" + "=" * 80)
                self.stdout.write("TEST 3: Notificación de Vencimiento")
                self.stdout.write("=" * 80)
                
                if options.get('producto_id'):
                    try:
                        producto = Producto.objects.get(id_producto=options['producto_id'])
                    except Producto.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Producto ID {options['producto_id']} no encontrado"))
                        return
                else:
                    producto = Producto.objects.filter(fecha_vencimiento__isnull=False).first()
                    if not producto:
                        self.stdout.write(self.style.WARNING("No hay productos con fecha de vencimiento para testear"))
                        return
                
                if producto.fecha_vencimiento:
                    hoy = timezone.now().date()
                    dias_restantes = (producto.fecha_vencimiento - hoy).days
                    
                    self.stdout.write(f"Producto: {producto.nombre}")
                    self.stdout.write(f"Fecha de vencimiento: {producto.fecha_vencimiento}")
                    self.stdout.write(f"Dias restantes: {dias_restantes}")
                    
                    resultado = enviar_alerta_vencimiento(producto, dias_restantes)
                    if resultado:
                        self.stdout.write(self.style.SUCCESS(f"OK - Alerta de vencimiento enviada"))
                    else:
                        self.stdout.write(self.style.ERROR(f"ERROR - Fallo al enviar alerta de vencimiento"))
                else:
                    self.stdout.write(self.style.WARNING("Producto sin fecha de vencimiento"))
            
            # Estadísticas
            self.stdout.write("\n" + "=" * 80)
            self.stdout.write("[ESTADISTICAS]")
            self.stdout.write("=" * 80)
            
            total_productos = Producto.objects.count()
            productos_stock_bajo = Producto.objects.filter(stock__lte=10).count()
            productos_vencidos = Producto.objects.filter(fecha_vencimiento__lte=timezone.now().date()).count()
            total_notificaciones = Notificacion.objects.count()
            notificaciones_no_leidas = Notificacion.objects.filter(leido=False).count()
            
            self.stdout.write(f"Total de productos: {total_productos}")
            self.stdout.write(f"Productos con stock bajo (≤10): {productos_stock_bajo}")
            self.stdout.write(f"Productos vencidos: {productos_vencidos}")
            self.stdout.write(f"Total de notificaciones: {total_notificaciones}")
            self.stdout.write(f"Notificaciones no leídas: {notificaciones_no_leidas}")
            
            self.stdout.write("\n" + self.style.SUCCESS("=" * 80))
            self.stdout.write(self.style.SUCCESS("TEST COMPLETADO"))
            self.stdout.write(self.style.SUCCESS("=" * 80))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"ERROR CRÍTICO: {str(e)}"))
            logger.critical(f"[TEST ERROR] {type(e).__name__}: {str(e)}")
