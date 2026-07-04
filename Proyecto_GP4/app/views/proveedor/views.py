from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.db.models import Q


class ProveedorListView(PermissionRequiredMixin, listView):
    model = Proveedor
    template_name = 'proveedor/listar.html'
    context_object_name = 'object_list'
    paginate_by = 7
    permission_required = "app.view_proveedor"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_queryset(self):
            queryset = Proveedor.objects.all().order_by("id_proveedor")

            buscar = self.request.GET.get("buscar")

            if buscar:
                queryset = queryset.filter(
                    Q(nombre_proveedor__icontains=buscar) |
                    Q(telefono__icontains=buscar) |
                    Q(correo_electronico__icontains=buscar) |
                    Q(direccion__icontains=buscar)
                )

            return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crear_url'] = reverse_lazy('app:crear_proveedor')
        context['icono'] = 'fas fa-truck'
        context['titulo'] = 'Listado de Proveedor'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Proveedores',
                'url': None
            }
        ]   
        return context
    


    


class ProveedorCreateView(PermissionRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/crear.html'
    success_url = reverse_lazy('app:listar_proveedores')
    permission_required = "app.add_proveedor"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Proveedor'
        context['icono'] = 'fas fa-plus-circle'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Proveedores',
                'url': reverse_lazy('app:listar_proveedores')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        return context
    


class ProveedorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Proveedor
    template_name = 'proveedor/eliminar.html'
    success_url = reverse_lazy('app:listar_proveedores')
    permission_required = "app.delete_proveedor"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Proveedor'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Proveedores',
                'url': reverse_lazy('app:listar_proveedores')
            },
            {
                'nombre': 'Eliminar',
                'url': None
            }
        ]
        return context


class ProveedorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/crear.html'
    success_url = reverse_lazy('app:listar_proveedores')
    permission_required = "app.change_proveedor"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fas fa-edit'
        context['titulo'] = 'Editar Proveedor'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Proveedores',
                'url': reverse_lazy('app:listar_proveedores')
            },
            {
                'nombre': 'Editar',
                'url': None
            }
        ]
        return context