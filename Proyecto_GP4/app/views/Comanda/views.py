from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.models import Comanda  
from app.forms import ComandaForm 
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404

def imprimir_comanda(request, pk):
    comanda = get_object_or_404(Comanda, id_comanda=pk)
    
    if comanda.estado != 'Entregado':
        comanda.estado = 'Entregado'
        comanda.save()
        
        comanda.pedido.estado = 'Entregado'
        comanda.pedido.save()
    return render(request, 'Comanda/imprimir.html', {'comanda': comanda})
# Listar todas las comandas
class ComandaListView(PermissionRequiredMixin,ListView):
    model = Comanda
    template_name = 'Comanda/listar.html'
    paginate_by = 5
    permission_required = "app.view_categoria"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Comandas'
        context['icono'] = 'fa-solid fa-clipboard-list'
        context['crear_url'] = reverse_lazy('app:crear_comanda')
        context['buscar'] = self.request.GET.get('buscar', '')
        context['fecha'] = self.request.GET.get('fecha', '')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  # Cambia esta URL por la de tu dashboard
            },
            {
                'nombre': 'Comandas',
                'url': None
            }
        ]

        return context
        
    
    def get_queryset(self):
        queryset = Comanda.objects.select_related(
            "pedido",
            "pedido__mesa",
            "pedido__usuario"
        ).prefetch_related(
            "pedido__detalle_platos__plato",
            "pedido__detalle_productos__producto"
        ).order_by('-id_comanda')
        
        estado = self.request.GET.get('buscar')
        fecha = self.request.GET.get('fecha')

        if estado:
            queryset = queryset.filter(estado__icontains=estado)
        
        
        if fecha: 
            queryset = queryset.filter(fecha_hora__date=fecha)


        return queryset
        
        


class ComandaUpdateView(PermissionRequiredMixin,UpdateView):
    model = Comanda
    form_class = ComandaForm
    template_name = 'Comanda/crear.html' 
    success_url = reverse_lazy('app:listar_comandas')
    permission_required = "app.change_categoria"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Comanda'
        context['listar_url'] = reverse_lazy('app:listar_comandas')
        return context

# Eliminar comanda
class ComandaDeleteView(PermissionRequiredMixin,DeleteView):
    model = Comanda
    template_name = 'Comanda/eliminar.html'
    success_url = reverse_lazy('app:listar_comandas')
    permission_required = "app.delete_categoria"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = '¿Eliminar Comanda?'
        context['listar_url'] = reverse_lazy('app:listar_comandas')
        return context