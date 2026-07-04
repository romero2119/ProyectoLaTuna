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


class CompraListView(PermissionRequiredMixin,listView):        
    model = Compra
    template_name = 'compra/listar.html'
    context_object_name = 'object_list'
    paginate_by = 7
    permission_required = "app.view_compra"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")
    

    def get_queryset(self):
            queryset = Compra.objects.all().order_by("id_compra")

            buscar = self.request.GET.get("buscar")

            if buscar:
                queryset = queryset.filter(
                    Q(proveedor__nombre_proveedor__icontains=buscar) |
                    Q(usuario__user__username__icontains=buscar) |
                    Q(producto__nombre__icontains=buscar) |
                    Q(insumo__nombre__icontains=buscar) |
                    Q(estado_pago__contains=buscar)
                )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crear_url'] = reverse_lazy('app:crear_compra')
        context['icono'] = 'fa-solid fa-cart-shopping'
        context['titulo'] = 'Listado de Compras'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  # Cambia esta URL por la de tu dashboard
            },
            {
                'nombre': 'Compras',
                'url': None
            }
        ]
        context['buscar'] = self.request.GET.get("buscar", "")
        return context

class CompraCreateView(PermissionRequiredMixin,CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compra/crear.html'
    success_url = reverse_lazy('app:listar_compras')
    permission_required = "app.add_compra"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fa-solid fa-cart-plus'
        context['titulo'] = 'Crear Compra'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Compras',
                'url': reverse_lazy('app:listar_compras')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        return context


class CompraDeleteView(PermissionRequiredMixin,DeleteView):
    model = Compra
    template_name = 'compra/eliminar.html'
    success_url = reverse_lazy('app:listar_compras')
    permission_required = "app.delete_compra"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fa-solid fa-cart-xmark'
        context['titulo'] = 'Eliminar Compra'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Compras',
                'url': reverse_lazy('app:listar_compras')
            },
            {
                'nombre': 'Eliminar',
                'url': None
            }
        ]
        return context
    
class CompraUpdateView(PermissionRequiredMixin,UpdateView):   
    model = Compra
    form_class = CompraForm
    template_name = 'compra/crear.html'
    success_url = reverse_lazy('app:listar_compras')
    permission_required = "app.change_compra"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fa-solid fa-cart-edit'
        context['titulo'] = 'Editar Compra'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Compras',
                'url': reverse_lazy('app:listar_compras')
            },
            {
                'nombre': 'Editar',
                'url': None
            }
        ]
        return context
        