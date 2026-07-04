# app/context_processors.py

from .models import *
from django.utils import timezone   

def notificaciones_admin(request):
    contador = Notificacion.objects.filter(leido=False).count()
    notificaciones_recientes = Notificacion.objects.filter(
        leido=False
    ).order_by('-fecha')[:5]  # últimas 5 no leídas

    return {
        'contador_notificaciones': contador,
        'notificaciones_recientes': notificaciones_recientes,
    }

def notificaciones_admin(request):
    hoy = timezone.now().date()
    contador = Notificacion.objects.filter(leido=False).count()
    notificaciones_recientes = Notificacion.objects.filter(
        leido=False
    ).order_by('-fecha')[:5]

    # Productos próximos a vencer para el contador
    proximos = Producto.objects.filter(
        fecha_vencimiento__isnull=False
    ).order_by('fecha_vencimiento')

    productos_por_vencer = []
    for p in proximos:
        dias = (p.fecha_vencimiento - hoy).days
        if dias <= 8:
            productos_por_vencer.append({
                'nombre': p.nombre,
                'dias': dias,
                'fecha': p.fecha_vencimiento,
            })

    return {
        'contador_notificaciones': contador,
        'notificaciones_recientes': notificaciones_recientes,
        'productos_por_vencer': productos_por_vencer,
    }