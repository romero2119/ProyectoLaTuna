# app/utils_email.py
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def enviar_alerta_stock_bajo(producto_o_insumo, nombre_producto=None):
    """
    Envia un correo de alerta por stock bajo de producto o insumo.
    Retorna True si se envio correctamente, False en caso de error.
    
    Args:
        producto_o_insumo: Instancia de Producto o Insumo
        nombre_producto: Nombre alternativo (opcional)
    """
    nombre = nombre_producto or producto_o_insumo.nombre
    stock = producto_o_insumo.stock
    
    # Generar mensaje contextual según cantidad de stock
    if stock == 0:
        asunto = f"ALERTA: Sin Stock - {nombre}"
        cuerpo = f"El producto '{nombre}' se ha agotado completamente.\nRevisa el inventario de forma urgente."
    elif stock <= 5:
        asunto = f"ALERTA CRÍTICA: Stock Bajo - {nombre}"
        cuerpo = f"El producto '{nombre}' solo tiene {stock} unidades en stock.\nToma acción inmediata."
    else:
        asunto = f"ALERTA: Stock Bajo - {nombre}"
        cuerpo = f"El producto '{nombre}' tiene {stock} unidades en stock.\nConsider reabastecer pronto."
    
    destinatarios = [settings.EMAIL_HOST_USER]
    
    try:
        send_mail(
            asunto,
            cuerpo,
            settings.EMAIL_HOST_USER,
            destinatarios,
            fail_silently=False,
        )
        logger.info(f"Correo enviado para {nombre} - {asunto}")
        return True
    except Exception as e:
        logger.error(f"Error al enviar correo para {nombre}: {str(e)}")
        return False


def enviar_alerta_vencimiento(producto, dias_restantes):
    """
    Envia un correo de alerta por vencimiento de producto.
    Retorna True si se envio correctamente, False en caso de error.
    """
    if dias_restantes < 0:
        asunto = f"ALERTA: Producto VENCIDO - {producto.nombre}"
        cuerpo = (
            f"El producto '{producto.nombre}' (ID: {producto.id_producto}) vencio el {producto.fecha_vencimiento}.\n"
            f"Por favor retiralo del inventario y actualiza el stock."
        )
    elif dias_restantes == 0:
        asunto = f"ALERTA: Producto vence HOY - {producto.nombre}"
        cuerpo = (
            f"El producto '{producto.nombre}' vence hoy {producto.fecha_vencimiento}.\n"
            f"Toma accion inmediata."
        )
    else:
        asunto = f"ALERTA: Producto proximo a vencer - {producto.nombre}"
        cuerpo = (
            f"El producto '{producto.nombre}' vence en {dias_restantes} dias ({producto.fecha_vencimiento}).\n"
            f"Revisa el inventario y considera su uso o reubicacion."
        )

    # Lista de destinatarios
    destinatarios = [settings.EMAIL_HOST_USER]

    try:
        send_mail(
            asunto,
            cuerpo,
            settings.EMAIL_HOST_USER,
            destinatarios,
            fail_silently=False,
        )
        logger.info(f"Correo enviado para {producto.nombre} - {asunto}")
        return True
    except Exception as e:
        logger.error(f"Error al enviar correo para {producto.nombre}: {str(e)}")
        return False