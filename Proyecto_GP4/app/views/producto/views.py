from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

from app.models import *
from app.forms import *


class ProductoListView(PermissionRequiredMixin, listView):
    model = Producto
    template_name = 'producto/listar.html'
    context_object_name = 'object_list'
    paginate_by = 7
    permission_required = "app.view_producto"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    # ================= FILTROS =================
    def get_queryset(self):
        queryset = super().get_queryset().select_related('categoria')

        categoria = self.request.GET.get('categoria')
        stock_bajo = self.request.GET.get('stock_bajo')
        orden = self.request.GET.get('orden')

        if categoria:
            queryset = queryset.filter(categoria_id=categoria)

        if stock_bajo == "1":
            queryset = queryset.filter(stock__lt=5)

        if orden == "desc":
            queryset = queryset.order_by('-stock')
        elif orden == "asc":
            queryset = queryset.order_by('stock')

        return queryset

    # ==========================================

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crear_url'] = reverse_lazy('app:crear_producto')
        context['icono'] = 'fa-solid fa-boxes-stacked'
        context['titulo'] = 'Listado de Productos'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  # Cambia esta URL por la de tu dashboard
            },
            {
                'nombre': 'Productos',
                'url': None
            }
        ]

        for obj in context['object_list']:
            umbral = 10

            if obj.stock <= 0:
                obj.estado_stock = {
                    'texto': f'Agotado ({obj.stock})',
                    'clase': 'bg-danger'
                }
            elif obj.stock <= (umbral / 4):
                obj.estado_stock = {
                    'texto': f'Crítico ({obj.stock})',
                    'clase': 'bg-danger'
                }
            elif obj.stock <= umbral:
                obj.estado_stock = {
                    'texto': f'Bajo ({obj.stock})',
                    'clase': 'bg-warning text-dark'
                }
            else:
                obj.estado_stock = {
                    'texto': f'Normal ({obj.stock})',
                    'clase': 'bg-success'
                }

        context.update({
            'titulo': 'Listado de Productos',
            'icono': 'fa-solid fa-boxes-stacked',
            'crear_url': reverse_lazy('app:crear_producto'),

            'categorias': Categoria.objects.all(),

            'categoria_seleccionada': self.request.GET.get('categoria', ''),
            'stock_bajo': self.request.GET.get('stock_bajo', ''),
            'orden': self.request.GET.get('orden', ''),

            'conteo_stock_bajo_real': Producto.objects.filter(stock__lt=5).count()
        })

        return context


# ===================== CREAR =====================

class ProductoCreateView(PermissionRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    success_url = reverse_lazy('app:listar_productos')
    permission_required = "app.add_producto"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = self.request.FILES
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Producto'
        context['listar_url'] = reverse_lazy('app:listar_productos')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Productos',
                'url': reverse_lazy('app:listar_productos')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        context['icono'] = 'fa-solid fa-boxes-stacked'
        return context


# ===================== EDITAR =====================

class ProductoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    success_url = reverse_lazy('app:listar_productos')
    permission_required = "app.change_producto"
    raise_exception = True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = self.request.FILES
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Producto'
        context['icono'] = 'fa-solid fa-pen-to-square'
        return context


# ===================== ELIMINAR =====================

class ProductoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Producto
    template_name = 'producto/eliminar.html'
    success_url = reverse_lazy('app:listar_productos')
    permission_required = "app.delete_producto"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Producto'
        context['icono'] = 'fa-solid fa-trash'
        context['listar_url'] = reverse_lazy('app:listar_productos')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Productos',
                'url': reverse_lazy('app:listar_productos')
            },
            {
                'nombre': 'Eliminar',
                'url': None
            }
        ]
        return context


class ProductoUpdateView(PermissionRequiredMixin, UpdateView):   
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear.html'
    success_url = reverse_lazy('app:listar_productos')
    permission_required = "app.change_producto"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = self.request.FILES  # ← agrega esto
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Producto'
        context['icono'] = 'fa-solid fa-pen-to-square'
        context['listar_url'] = reverse_lazy('app:listar_productos')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Productos',
                'url': reverse_lazy('app:listar_productos')
            },
            {
                'nombre': 'Editar',
                'url': None
            }
        ]
        return context