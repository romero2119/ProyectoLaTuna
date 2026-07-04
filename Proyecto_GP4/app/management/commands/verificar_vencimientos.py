# app/management/commands/verificar_vencimientos.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import Producto, Notificacion
from app.utils_email import enviar_alerta_vencimiento
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Verifica productos proximos a vencer y envia alertas por correo'

    def handle(self, *args, **kwargs):
        hoy = timezone.now().date()
        productos_procesados = 0
        correos_enviados = 0

        for producto in Producto.objects.all():
            if not producto.fecha_vencimiento:
                continue

            dias_restantes = (producto.fecha_vencimiento - hoy).days
            productos_procesados += 1

            # Determinar tipo de notificacion (sin emojis)
            if dias_restantes < 0:
                tipo = "Producto vencido"
                mensaje = f"VENCIDO: '{producto.nombre}' vencio el {producto.fecha_vencimiento}."
            elif dias_restantes == 0:
                tipo = "Vence hoy"
                mensaje = f"'{producto.nombre}' vence HOY {producto.fecha_vencimiento}."
            elif dias_restantes <= 8:
                tipo = "Proximo a vencer"
                mensaje = f"'{producto.nombre}' vence en {dias_restantes} dias ({producto.fecha_vencimiento})."
            else:
                continue  # No esta proximo a vencer

            # Evitar duplicados (notificacion no leida)
            ya_existe = Notificacion.objects.filter(
                producto=producto,
                tipo_notificacion=tipo,
                leido=False
            ).exists()

            if not ya_existe:
                # Crear notificacion en la BD
                Notificacion.objects.create(
                    producto=producto,
                    tipo_notificacion=tipo,
                    mensaje=mensaje
                )
                # Enviar correo
                if enviar_alerta_vencimiento(producto, dias_restantes):
                    correos_enviados += 1
                    self.stdout.write(f"Correo enviado: {producto.nombre}")
                else:
                    self.stdout.write(self.style.ERROR(f"Fallo envio de correo: {producto.nombre}"))

        # Cambia el emoji ✅ por texto plano
        self.stdout.write(self.style.SUCCESS(
            f"Verificacion completada. Productos procesados: {productos_procesados}, Correos enviados: {correos_enviados}"
        ))