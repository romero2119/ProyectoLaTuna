from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from app.forms import PagoForm
from django.contrib import messages
from itertools import groupby
from django.db.models.functions import TruncMonth
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.db.models import Q


class PagoListView(PermissionRequiredMixin, ListView):
    model = Pago
    template_name = 'pago/listar.html'
    context_object_name = 'pagos'
    paginate_by = 5
    ordering = ('-fecha',)
    permission_required = "app.view_pago"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")
    
    def get_queryset(self):
        queryset = Pago.objects.select_related(
            'venta',
            'venta__usuario',
            'venta__pedido'
        )

        usuario = self.request.GET.get('usuario')
        fecha = self.request.GET.get('fecha')
        estado = self.request.GET.get('estado')

        hoy = timezone.now()
        queryset = queryset.filter(
            fecha__year=hoy.year,
            fecha__month=hoy.month
        )

        if usuario:
            queryset = queryset.filter(
                Q(venta__usuario__user__username__icontains=usuario) |
                Q(venta__usuario__user__first_name__icontains=usuario) |
                Q(venta__usuario__user__last_name__icontains=usuario)
            )

        if fecha:
            queryset = queryset.filter(fecha__date=fecha)

        if estado == 'pagado':
                queryset = queryset.filter(activo=True)
        elif estado == 'pendiente':
            queryset = queryset.filter(activo=False)

    # Mostrar alerta cuando no hay resultados
        if (usuario or fecha or estado) and not queryset.exists():
            if usuario and fecha:
                mensaje = f'No se encontraron pagos del usuario "{usuario}" para la fecha {fecha}.'
            elif usuario:
                mensaje = f'No se encontraron pagos del usuario "{usuario}".'
            elif fecha:
                mensaje = f'No se encontraron pagos para la fecha {fecha}.'
            elif estado:
                mensaje = f'No se encontraron pagos con estado "{estado}".'

            messages.warning(self.request, mensaje)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Pagos'
        context['icono'] = 'fas fa-cash-register'
        context['usuario'] = self.request.GET.get('usuario', '')
        context['fecha'] = self.request.GET.get('fecha', '')
        context['estado'] = self.request.GET.get('estado', '')
        context['mes_actual'] = timezone.now().strftime('%B %Y').capitalize()
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Pagos',
                'url': reverse_lazy('app:listar_pagos')
            }
        ]
        return context


class PagoCreateView(PermissionRequiredMixin, CreateView):
    model = Pago
    template_name = 'pago/crear.html'
    form_class = PagoForm
    success_url = reverse_lazy('app:listar_pagos')
    permission_required = "app.add_pago"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_venta = self.kwargs.get('id_venta')  #  nombre correcto
        venta = get_object_or_404(Venta, id_venta=id_venta)
        context['venta'] = venta
        context['titulo'] = 'Registrar Pago'
        context['icono'] = 'fas fa-cash-register'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Pagos',
                'url': reverse_lazy('app:listar_pagos')
            },
            {
                'nombre': 'Registrar',
                'url': None
            }
        ]
        return context

    def form_valid(self, form):
        id_venta = self.kwargs.get('id_venta')  #  nombre correcto
        venta = get_object_or_404(Venta, id_venta=id_venta)

        pago = form.save(commit=False)
        pago.venta = venta
        pago.monto = venta.total
        pago.save()

        #  Marcar el pedido como pagado
        pedido = venta.pedido
        pedido.pago = True
        pedido.save()

        messages.success(self.request, "Pago registrado correctamente.")
        return redirect(self.success_url)


class EliminarPagoView(PermissionRequiredMixin, DeleteView):
    model = Pago
    template_name = 'pago/eliminar.html'
    context_object_name = 'object'
    success_url = reverse_lazy('app:listar_pagos')
    pk_url_kwarg = 'pk'
    permission_required = "app.delete_pago"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        id_pago = self.object.id_pago
        id_venta = self.object.venta.id_venta if self.object.venta else None
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Pago #{id_pago} de la venta #{id_venta} eliminado correctamente.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pago'
        context['listar_url'] = reverse_lazy('app:listar_ventas')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Pagos',
                'url': reverse_lazy('app:listar_pagos')
            },
            {
                'nombre': 'Eliminar',
                'url': None
            }
        ]
        return context


def registrar_pago(request, venta_id):
    venta = get_object_or_404(Venta, id_venta=venta_id)

    if request.method == "POST":
        metodo = request.POST.get('metodo_pago')

        if not metodo:
            messages.error(request, " Debes seleccionar un método de pago.")
            return redirect('app:crear_pago', venta_id=venta.id_venta)

        Pago.objects.create(
            venta=venta,
            monto=venta.total,
            metodo_pago=metodo
        )

        #  Marcar el pedido como pagado
        pedido = venta.pedido
        pedido.pago = True
        pedido.save()

        messages.success(request, f"Pago registrado correctamente para la venta #{venta.id_venta}.")
        return redirect('app:listar_pagos')

    return render(request, 'pago/crear.html', {'venta': venta})



class PagoHistorialView(ListView):
    model = Pago
    template_name = 'pago/historial.html'
    context_object_name = 'pagos'
    paginate_by = 5
    ordering = ('-fecha_venta',)

    def get_queryset(self):
        queryset = Pago.objects.select_related('venta').order_by('-fecha')

        mes = self.request.GET.get('mes')

        if mes:
            año, mes_num = mes.split('-')
            queryset = queryset.filter(
                fecha__year=año,
                fecha__month=mes_num
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Historial de Pagos por Mes'
        context['icono'] = 'fas fa-cash-register'

        pagos = context['pagos']
        historial = {}

        for pago in pagos:
            clave = pago.fecha.strftime('%B %Y').capitalize()
            if clave not in historial:
                historial[clave] = []
            historial[clave].append(pago)

        context['historial'] = historial
        context['mes_seleccionado'] = self.request.GET.get('mes', '')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Pagos',
                'url': reverse_lazy('app:listar_pagos')
            },
            {
                'nombre': 'Historial',
                'url': None
            }
        ]

        return context