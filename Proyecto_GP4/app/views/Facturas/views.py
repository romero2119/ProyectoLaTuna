from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView,DetailView, View, DeleteView, ListView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from itertools import groupby
from django.db.models.functions import TruncMonth
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.db.models import Q
from django.utils import timezone

class FacturaListView(PermissionRequiredMixin, ListView):
    model = Factura
    template_name = 'facturas/listar.html'
    context_object_name = 'facturas'
    paginate_by = 5
    ordering = ('-fecha_hora',)
    permission_required = "app.view_factura"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_queryset(self):

        queryset = Factura.objects.select_related(
            'venta',
            'venta__usuario',
            'venta__pedido'
        )

        usuario = self.request.GET.get('usuario')
        fecha = self.request.GET.get('fecha')
        estado = self.request.GET.get('estado')

        # Mostrar únicamente las facturas del mes actual
        hoy = timezone.now()

        queryset = queryset.filter(
            fecha_hora__year=hoy.year,
            fecha_hora__month=hoy.month
        )

        # Buscar por usuario
        if usuario:
            queryset = queryset.filter(
                Q(venta__usuario__user__username__icontains=usuario) |
                Q(venta__usuario__user__first_name__icontains=usuario) |
                Q(venta__usuario__user__last_name__icontains=usuario)
            )

        # Buscar por fecha
        if fecha:
            queryset = queryset.filter(
                fecha_hora__date=fecha
            )

        # Filtrar por estado
        if estado == "activa":
            queryset = queryset.filter(activo=True)

        elif estado == "inactiva":
            queryset = queryset.filter(activo=False)

        # Mostrar alerta cuando no haya resultados
        if (usuario or fecha or estado) and not queryset.exists():

            if usuario and fecha:
                mensaje = f'No se encontraron facturas del usuario "{usuario}" para la fecha {fecha}.'

            elif usuario:
                mensaje = f'No se encontraron facturas del usuario "{usuario}".'

            elif fecha:
                mensaje = f'No se encontraron facturas para la fecha {fecha}.'

            else:
                mensaje = f'No se encontraron facturas con estado "{estado}".'

            messages.warning(self.request, mensaje)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Listado de Facturas'
        context['icono'] = 'fa-solid fa-file-invoice-dollar'

        context['usuario'] = self.request.GET.get('usuario', '')
        context['fecha'] = self.request.GET.get('fecha', '')
        context['estado'] = self.request.GET.get('estado', '')

        context['mes_actual'] = timezone.now().strftime('%B %Y').capitalize()
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  # Cambia esta URL por la de tu dashboard
            },
            {
                'nombre': 'Facturas',
                'url': None
            }
        ]
        return context

class FacturaCreateView(PermissionRequiredMixin,CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'facturas/crear.html'
    success_url = reverse_lazy('app:listar_facturas')
    permission_required = "app.add_factura"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fa-solid fa-file-invoice-dollar'
        context['titulo'] = 'Crear Nueva Factura'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Facturas',
                'url': reverse_lazy('app:listar_facturas')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        return context
    

class FacturaDesactivarView(View):
    
    def get(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk)
        if not factura.activo:
            messages.warning(request, "Esta factura ya está desactivada.")
            return redirect('app:listar_facturas')
        return render(request, 'facturas/desactivar.html', {
            'object': factura,
            'titulo': 'Desactivar Factura',      # ← añadir
            'icono': 'fa-solid fa-ban',           # ← añadir
            'breadcrumb': [
                {
                    'nombre': 'Inicio',
                    'url': reverse_lazy('app:dashboard')
                },
                {
                    'nombre': 'Facturas',
                    'url': reverse_lazy('app:listar_facturas')
                },
                {
                    'nombre': 'Desactivar',
                    'url': None
                }
            ]
        })

    def post(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk)

        observacion = request.POST.get('observacion', '').strip()
        if not observacion:
            messages.error(request, "Debes ingresar una observación para desactivar la factura.")
            return render(request, 'facturas/desactivar.html', {
                'object': factura,
                'titulo': 'Desactivar Factura',  # ← añadir también aquí
                'icono': 'fa-solid fa-ban',
            })
        
        #aca esta la modificcion pra devolver
        pedido = factura.venta.pedido
        for detalle in pedido.detalle_productos.all():
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()


        factura.activo = False
        factura.observacion = observacion
        factura.save()

        Pago.objects.filter(venta=factura.venta).update(activo=False)

        factura.venta.activo = False
        factura.venta.save()

        messages.success(request, f"Factura #{factura.id} desactivada correctamente.")
        return redirect('app:listar_facturas')



class FacturaUpdateView(PermissionRequiredMixin,UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'facturas/editar.html'
    success_url = reverse_lazy('app:listar_facturas')
    permission_required = "app.change_factura"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Factura'
        context['icono'] = 'fa-solid fa-file-invoice-dollar'
        context['listar_url'] = reverse_lazy('app:listar_facturas')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Facturas',
                'url': reverse_lazy('app:listar_facturas')
            },
            {
                'nombre': 'Editar',
                'url': None
            }
        ]
        return context


class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'facturas/detalle.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Factura'
        context['icono'] = 'fa-solid fa-file-invoice-dollar'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Facturas',
                'url': reverse_lazy('app:listar_facturas')
            },
            {
                'nombre': 'Detalle',
                'url': None
            }
        ]
        return context

class FacturaHistorialView(ListView):
    model = Factura
    template_name = 'facturas/historial.html'
    context_object_name = 'facturas'
    paginate_by = 5


    def get_queryset(self):
        queryset = Factura.objects.select_related('venta').order_by('-fecha_hora')

        mes = self.request.GET.get('mes')

        if mes:
            año, mes_num = mes.split('-')
            queryset = queryset.filter(
                fecha_hora__year=año,
                fecha_hora__month=mes_num
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Historial de Facturas por Mes'
        context['icono'] = 'fa-solid fa-file-invoice-dollar'

        facturas = context['facturas']
        historial = {}

        for factura in facturas:
            clave = factura.fecha_hora.strftime('%B %Y').capitalize()
            if clave not in historial:
                historial[clave] = []
            historial[clave].append(factura)

        context['historial'] = historial
        context['mes_seleccionado'] = self.request.GET.get('mes', '')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Facturas',
                'url': reverse_lazy('app:listar_facturas')
            },
            {
                'nombre': 'Historial',
                'url': None
            }
        ]

        return context
    
def crear_factura(request, pago_id):
    pago = get_object_or_404(Pago, id_pago=pago_id)

    if pago.factura:
        messages.warning(request, "Este pago ya tiene factura generada.")
        return redirect('app:listar_pagos')

    if pago.venta and Factura.objects.filter(venta=pago.venta, activo=True).exists():
        messages.warning(request, "Esta venta ya tiene una factura activa.")
        return redirect('app:listar_pagos')

    factura = Factura.objects.create(
        venta=pago.venta,
        valor_total=pago.monto,
        metodo_pago=pago.metodo_pago
    )

    pago.factura = str(factura.id)
    pago.save()

    messages.success(request, f"Factura #{factura.id} creada correctamente.")
    return redirect('app:listar_facturas')