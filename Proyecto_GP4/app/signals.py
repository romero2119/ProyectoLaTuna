# app/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from .utils_email import enviar_alerta_stock_bajo, enviar_alerta_vencimiento
import logging

logger = logging.getLogger(__name__)

# En tu models.py o en un archivo utils.py
class UnidadMedida(models.TextChoices):
    KILO = 'kg', 'Kilogramos'
    GRAMO = 'g', 'Gramos'
    LITRO = 'l', 'Litros'
    MILILITRO = 'ml', 'Mililitros'
    METRO = 'm', 'Metros'
    CENTIMETRO = 'cm', 'Centímetros'
    UNIDAD = 'unidad', 'Unidades'

# Diccionario de conversión a unidad base (gramos, mililitros, metros, unidades)
CONVERSIONES = {
    'kg': {'base': 'g', 'factor': 1000},      # 1 kg = 1000 g
    'g': {'base': 'g', 'factor': 1},
    'l': {'base': 'ml', 'factor': 1000},      # 1 L = 1000 ml
    'ml': {'base': 'ml', 'factor': 1},
    'm': {'base': 'm', 'factor': 1},
    'cm': {'base': 'm', 'factor': 0.01},      # 1 cm = 0.01 m
    'unidad': {'base': 'unidad', 'factor': 1},
}

# Umbrales DINÁMICOS según la unidad de medida
UMBRALES = {
    'kg': 2,      # 2 kg es bajo
    'g': 200,     # 200g es bajo
    'l': 2,       # 2 litros es bajo
    'ml': 200,    # 200 ml es bajo
    'm': 5,       # 5 metros es bajo
    'cm': 50,     # 50 cm es bajo
    'unidad': 10, # 10 unidades es bajo
}

def normalizar_stock(stock, unidad):
    """Convierte cualquier stock a su unidad base para comparar"""
    if unidad in CONVERSIONES:
        return stock * CONVERSIONES[unidad]['factor']
    return stock

def obtener_umbral(unidad):
    """Obtiene el umbral apropiado para la unidad de medida"""
    return UMBRALES.get(unidad, 10)  # Por defecto 10 si no está definido

def formatear_mensaje_stock(nombre, stock, unidad):
    """Genera mensaje contextual según la unidad"""
    if stock == 0:
        return f"SIN STOCK: El insumo '{nombre}' está re paila."
    
    # Umbrales críticos (más estrictos)
    umbrales_criticos = {
        'kg': 0.5,
        'g': 50,
        'l': 0.5,
        'ml': 50,
        'm': 1,
        'cm': 10,
        'unidad': 3,
    }
    
    umbral_critico = umbrales_criticos.get(unidad, 2)
    
    if stock < umbral_critico:
        return f"CRÍTICO: '{nombre}' solo tiene {stock} {unidad}."
    else:
        return f"Stock bajo: '{nombre}' tiene {stock} {unidad}."
# ─────────────────────────────────────────────
#  SIGNALS EXISTENTES (Menu)
# ─────────────────────────────────────────────

@receiver(post_save, sender=Plato)
def crear_menu_plato(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(plato=instance)


@receiver(post_save, sender=Producto)
def crear_menu_producto(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(producto=instance)


# ─────────────────────────────────────────────
#  STOCK BAJO - PRODUCTO
# ─────────────────────────────────────────────

@receiver(post_save, sender=Producto)
def notificacion_stock_producto(sender, instance, **kwargs):
    if instance.stock <= 10:
        # Evita duplicados: solo crea si no hay una notificación activa (no leída)
        ya_existe = Notificacion.objects.filter(
            producto=instance,
            tipo_notificacion="Stock bajo",
            leido=False
        ).exists()

        if not ya_existe:
            if instance.stock == 0:
                mensaje = f"SIN STOCK: El producto '{instance.nombre}' está agotado."
            elif instance.stock < 5:
                mensaje = f"CRÍTICO: '{instance.nombre}' solo tiene {instance.stock} unidades."
            else:
                mensaje = f"Stock bajo: '{instance.nombre}' tiene {instance.stock} unidades."

            # Crear notificación en BD
            Notificacion.objects.create(
                producto=instance,
                tipo_notificacion="Stock bajo",
                mensaje=mensaje
            )
            
            # Enviar email de alerta
            try:
                enviar_alerta_stock_bajo(instance)
                logger.info(f"Email enviado para stock bajo: {instance.nombre}")
            except Exception as e:
                logger.error(f"Error al enviar email de stock bajo para {instance.nombre}: {str(e)}")
    else:
        # Si el stock se recuperó, elimina las notificaciones no leídas de ese producto
        Notificacion.objects.filter(
            producto=instance,
            tipo_notificacion="Stock bajo",
            leido=False
        ).delete()


# ─────────────────────────────────────────────
#  STOCK BAJO - INSUMO
# ─────────────────────────────────────────────

@receiver(post_save, sender=insumo)
def notificacion_stock_insumo(sender, instance, **kwargs):
    # Obtener la unidad de medida (asumiendo que tienes este campo)
    unidad = instance.unidad  # Ajusta según el nombre real de tu campo
    
    # Normalizar el stock para la comparación
    stock_normalizado = normalizar_stock(instance.stock, unidad)
    
    # Obtener el umbral apropiado para esta unidad
    umbral = obtener_umbral(unidad)
    
    # Verificar si el stock normalizado está bajo el umbral
    if stock_normalizado <= umbral:
        ya_existe = Notificacion.objects.filter(
            insumo=instance,
            tipo_notificacion="Stock bajo",
            leido=False
        ).exists()

        if not ya_existe:
            # Usar el mensaje formateado con la unidad original
            mensaje = formatear_mensaje_stock(instance.nombre, instance.stock, unidad)
            
            # Crear notificación en BD
            Notificacion.objects.create(
                insumo=instance,
                tipo_notificacion="Stock bajo",
                mensaje=mensaje
            )
            
            # Enviar email de alerta
            try:
                enviar_alerta_stock_bajo(instance)
                logger.info(f"Email enviado para stock bajo: {instance.nombre}")
            except Exception as e:
                logger.error(f"Error al enviar email de stock bajo para {instance.nombre}: {str(e)}")
    else:
        # Si el stock se recuperó, limpia notificaciones no leídas
        Notificacion.objects.filter(
            insumo=instance,
            tipo_notificacion="Stock bajo",
            leido=False
        ).delete()


# ─────────────────────────────────────────────
#  USUARIOS - Crear / Editar / Eliminar
# ─────────────────────────────────────────────

@receiver(post_save, sender=Usuario)
def notificacion_usuario_guardado(sender, instance, created, **kwargs):
    nombre = instance.user.first_name
    apellido = instance.user.last_name
    username = instance.user.username

    if created:
        Notificacion.objects.create(
            usuario=instance,
            tipo_notificacion="Usuario creado",
            mensaje=f"Nuevo usuario registrado: '{username} {apellido}' con rol '{instance.rol}'."
        )
    else:
        Notificacion.objects.create(
            usuario=instance,
            tipo_notificacion="Usuario editado",
            mensaje=f"El usuario '{nombre} {apellido}' fue modificado."
        )


@receiver(post_delete, sender=Usuario)
def notificacion_usuario_eliminado(sender, instance, **kwargs):
    nombre = instance.user.first_name
    apellido = instance.user.last_name

    Notificacion.objects.create(
        usuario=None,
        tipo_notificacion="Usuario eliminado",
        mensaje=f"El usuario '{nombre} {apellido}' (rol: {instance.rol}) fue eliminado del sistema."
    )