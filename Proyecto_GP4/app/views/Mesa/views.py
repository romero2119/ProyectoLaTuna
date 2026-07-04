from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.models import Mesa
from app.forms import MesaForm 
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404

class MesaListView(PermissionRequiredMixin, ListView):
    model = Mesa
    template_name = 'Mesa/listar.html'
    context_object_name = 'mesas'
    permission_required = "app.view_mesa"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Mesas'
        context['icono'] = 'fas fa-table'
        context['crear_url'] = reverse_lazy('app:crear_mesa')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  # Cambia esta URL por la de tu dashboard
            },
            {
                'nombre': 'Mesas',
                'url': None
            }
        ]
        return context
    
    def get_queryset(self):
        queryset = Mesa.objects.all()
        buscar = self.request.GET.get('buscar')

        if buscar:
            queryset = queryset.filter(numero_mesa__icontains=buscar)

        return queryset

class MesaCreateView(PermissionRequiredMixin, CreateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'Mesa/crear.html'
    success_url = reverse_lazy('app:listar_mesas')
    permission_required = "app.add_mesa"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nueva Mesa'
        context['icono'] = 'fas fa-table'
        context['listar_url'] = reverse_lazy('app:listar_mesas')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Mesas',
                'url': reverse_lazy('app:listar_mesas')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        return context

class MesaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'Mesa/crear.html' 
    success_url = reverse_lazy('app:listar_mesas')
    permission_required = "app.change_mesa"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Mesa'
        context['icono'] = 'fas fa-table'
        context['listar_url'] = reverse_lazy('app:listar_mesas')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Mesas',
                'url': reverse_lazy('app:listar_mesas')
            },
            {
                'nombre': 'Editar',
                'url': None
            }
        ]
        return context

# Eliminar mesa
class MesaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Mesa
    permission_required = "app.delete_mesa"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")
    template_name = 'Mesa/eliminar.html'
    success_url = reverse_lazy('app:listar_mesas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fas fa-table'
        context['titulo'] = '¿Eliminar Mesa?'
        context['listar_url'] = reverse_lazy('app:listar_mesas')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Mesas',
                'url': reverse_lazy('app:listar_mesas')
            },
            {
                'nombre': 'Eliminar',
                'url': None
            }
        ]
        return context