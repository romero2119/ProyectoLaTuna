from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import Venta, Usuario, Pedido
from django.contrib import messages
from app.forms import VentaForm
from itertools import groupby
from django.db.models.functions import TruncMonth
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.db.models import Q


from django.utils import timezone

class VentaListView(PermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'venta/listar.html'
    context_object_name = 'ventas'
    paginate_by = 5
    ordering = ('-fecha_venta',)  # ← era orden_by, el atributo correcto es ordering
    permission_required = "app.view_venta"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_queryset(self):
        queryset = Venta.objects.select_related('usuario', 'pedido')
        usuario = self.request.GET.get('usuario')
        fecha = self.request.GET.get('fecha')
        estado = self.request.GET.get('estado')

        # Filtrar solo el mes actual por defecto
        hoy = timezone.now()
        queryset = queryset.filter(
            fecha_venta__year=hoy.year,
            fecha_venta__month=hoy.month
        )

        if usuario:
            queryset = queryset.filter(
                Q(usuario__user__username__icontains=usuario) |
                Q(usuario__user__first_name__icontains=usuario) |
                Q(usuario__user__last_name__icontains=usuario)
    )
        if fecha:
            queryset = queryset.filter(fecha_venta__date=fecha)
        if estado == 'pagado':
            queryset = queryset.filter(estado='PAGADA')
        elif estado == 'pendiente':
            queryset = queryset.exclude(estado='PAGADA')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Ventas'
        context['icono'] = 'fas fa-cash-register'
        context['usuario'] = self.request.GET.get('usuario', '')
        context['fecha'] = self.request.GET.get('fecha', '')
        context['estado'] = self.request.GET.get('estado', '')
        context['mes_actual'] = timezone.now().strftime('%B %Y').capitalize()
        context['crear_url'] = reverse_lazy('app:crear_venta')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Ventas',
                'url': None
            }
        ]
        return context

class VentaCreateView(PermissionRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'venta/crear.html'
    success_url = reverse_lazy('app:listar_ventas')
    permission_required = "app.add_venta"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Venta'
        context['icono'] = 'fas fa-cash-register'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Ventas',
                'url': reverse_lazy('app:listar_ventas')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        return context

    def form_valid(self, form):
        pedido = form.cleaned_data['pedido']

        # Validar que el pedido esté entregado
        if pedido.estado != 'Entregado':
            messages.error(
                self.request,
                f"El pedido #{pedido.id_pedido} aún está en preparación. No se puede crear una venta hasta que sea entregado."
            )
            return redirect('app:crear_venta')

        # Validar que no exista venta para ese pedido
        if Venta.objects.filter(pedido=pedido).exists():
            messages.error(
                self.request,
                f"El pedido #{pedido.id_pedido} ya tiene una venta registrada."
            )
            return redirect('app:crear_venta')

        # Validar que el pedido tenga productos o platos
        if not pedido.detalle_productos.exists() and not pedido.detalle_platos.exists():
            messages.error(
                self.request,
                f"No se puede crear una venta sin ítems en el pedido #{pedido.id_pedido}."
            )
            return redirect('app:crear_venta')

        # Obtener el usuario
        usuario = Usuario.objects.first()

        if not usuario:
            messages.error(
                self.request,
                "No hay usuarios disponibles para asignar a la venta."
            )
            return redirect('app:crear_venta')

        # Asignar datos a la venta
        form.instance.usuario = usuario
        form.instance.total = pedido.total

        # Guardar la venta
        response = super().form_valid(form)

        # Mensaje de éxito
        messages.success(
            self.request,
            f"Venta #{self.object.id_venta} creada correctamente."
        )

        return response
    
class VentaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Venta
    fields = '__all__'
    template_name = 'venta/crear.html'
    success_url = reverse_lazy('app:listar_ventas')
    permission_required = "app.change_venta"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")


class VentaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Venta
    template_name = 'venta/eliminar.html'
    success_url = reverse_lazy('app:listar_ventas')
    permission_required = "app.delete_venta"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")


# oagar venta
def pagar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id_venta=venta_id)
    venta.estado = 'PAGADA'
    venta.save()
    return redirect('app:listar_ventas')

def crear_venta_desde_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)

    # Validar que el pedido esté entregado
    if pedido.estado != 'Entregado':
        messages.error(request, f"El pedido #{pedido.id_pedido} aún está en preparación. No se puede crear una venta.")
        return redirect('app:listar_ventas')

    if Venta.objects.filter(pedido=pedido).exists():
        messages.error(request, f"El pedido #{pedido.id_pedido} ya tiene una venta registrada.")
        return redirect('app:listar_ventas')

    if not pedido.detalle_productos.exists() and not pedido.detalle_platos.exists():
        messages.error(request, f"No se puede crear una venta sin items en el pedido #{pedido.id_pedido}.")
        return redirect('app:listar_ventas')

    usuario = Usuario.objects.first()

    Venta.objects.create(
        pedido=pedido,
        usuario=usuario,
        total=pedido.total
    )

    messages.success(request, f"Venta creada correctamente para el pedido #{pedido.id_pedido}.")
    return redirect('app:listar_ventas')

class VentaHistorialView(ListView):
    model = Venta
    template_name = 'venta/historial.html'
    context_object_name = 'ventas'
    
    def get_queryset(self):
        queryset = Venta.objects.select_related('usuario', 'pedido').order_by('-fecha_venta')
        mes = self.request.GET.get('mes')

        if mes:
            # mes viene tipo: 2026-03
            año, mes_num = mes.split('-')
            queryset = queryset.filter(
                fecha_venta__year=año,
                fecha_venta__month=mes_num
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Historial de Ventas por Mes'
        context['icono'] = 'fas fa-cash-register'

        ventas = context['ventas']
        historial = {}

        for venta in ventas:
            clave = venta.fecha_venta.strftime('%B %Y').capitalize()
            if clave not in historial:
                historial[clave] = []
            historial[clave].append(venta)

        context['historial'] = historial

        # Para mantener el valor seleccionado en el input
        context['mes_seleccionado'] = self.request.GET.get('mes', '')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Ventas',
                'url': reverse_lazy('app:listar_ventas')
            },
            {
                'nombre': 'Historial',
                'url': None
            }
        ]

        return context

