#!/usr/bin/env python
"""
Management Command: Enviar Notificaciones por Email
Propósito: Verificar stock bajo y vencimientos, enviar notificaciones por email

Uso: python manage.py enviar_notificaciones
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from app.models import Producto, Notificacion
from app.utils_email import enviar_alerta_vencimiento, enviar_alerta_stock_bajo
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Verifica stock bajo y vencimientos, envia notificaciones por correo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tipo',
            choices=['stock', 'vencimiento', 'ambos'],
            default='ambos',
            help='Tipo de notificación a enviar'
        )
        parser.add_argument(
            '--test',
            action='store_true',
            help='Enviar email de prueba'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=" * 80))
        self.stdout.write(self.style.SUCCESS("ENVIANDO NOTIFICACIONES"))
        self.stdout.write(self.style.SUCCESS("=" * 80))
        
        # Verificar configuración de email
        self.stdout.write("\n[CONFIGURACIÓN EMAIL]")
        self.stdout.write(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        
        # Test email si se solicita
        if options.get('test'):
            self.stdout.write("\n[TEST EMAIL]")
            from django.core.mail import send_mail
            try:
                send_mail(
                    subject='[TEST] Sistema de Notificaciones',
                    message='Este es un email de prueba del sistema de notificaciones.\n\nSi recibiste este correo, el sistema SMTP funciona correctamente.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS("✓ Email de prueba enviado correctamente"))
                logger.info("[TEST] Email de prueba enviado")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Error al enviar email de prueba: {str(e)}"))
                logger.error(f"[TEST ERROR] {type(e).__name__}: {str(e)}")
                return
        
        # Procesar notificaciones según el tipo
        tipo_notificacion = options.get('tipo', 'ambos')
        
        # STOCK BAJO
        if tipo_notificacion in ['stock', 'ambos']:
            self.stdout.write("\n[VERIFICANDO STOCK BAJO]")
            self._procesar_stock_bajo()
        
        # VENCIMIENTOS
        if tipo_notificacion in ['vencimiento', 'ambos']:
            self.stdout.write("\n[VERIFICANDO VENCIMIENTOS]")
            self._procesar_vencimientos()
        
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("✓ PROCESO COMPLETADO"))
        self.stdout.write("=" * 80)

    def _procesar_stock_bajo(self):
        """Procesa alertas de stock bajo"""
        count = 0
        try:
            for producto in Producto.objects.filter(stock__lte=10):
                try:
                    if enviar_alerta_stock_bajo(producto):
                        self.stdout.write(f"  ✓ Email enviado: {producto.nombre} (Stock: {producto.stock})")
                        count += 1
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"  ⚠ Fallo al enviar: {producto.nombre}"
                        ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Error para {producto.nombre}: {str(e)}"
                    ))
                    logger.error(f"Error procesando stock bajo para {producto.nombre}: {str(e)}")
            
            if count == 0:
                self.stdout.write("  Sin productos con stock bajo")
            else:
                self.stdout.write(self.style.SUCCESS(f"  Total: {count} emails enviados"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al procesar stock bajo: {str(e)}"))
            logger.error(f"Error procesando stock bajo: {str(e)}")

    def _procesar_vencimientos(self):
        """Procesa alertas de vencimiento"""
        hoy = timezone.now().date()
        count = 0
        try:
            for producto in Producto.objects.exclude(fecha_vencimiento__isnull=True):
                try:
                    dias_restantes = (producto.fecha_vencimiento - hoy).days
                    
                    # Solo alertar si está próximo a vencer (<=8 días) o vencido
                    if dias_restantes <= 8:
                        if enviar_alerta_vencimiento(producto, dias_restantes):
                            self.stdout.write(f"  ✓ Email enviado: {producto.nombre} (Vence en {dias_restantes} días)")
                            count += 1
                        else:
                            self.stdout.write(self.style.WARNING(
                                f"  ⚠ Fallo al enviar: {producto.nombre}"
                            ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Error para {producto.nombre}: {str(e)}"
                    ))
                    logger.error(f"Error procesando vencimiento para {producto.nombre}: {str(e)}")
            
            if count == 0:
                self.stdout.write("  Sin productos próximos a vencer")
            else:
                self.stdout.write(self.style.SUCCESS(f"  Total: {count} emails enviados"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al procesar vencimientos: {str(e)}"))
            logger.error(f"Error procesando vencimientos: {str(e)}")
