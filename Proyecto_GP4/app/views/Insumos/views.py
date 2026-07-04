from django.shortcuts import render, redirect
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from app.models import *
from app.forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from app.signals import obtener_umbral
from django.contrib import messages

class InsumosListView(PermissionRequiredMixin, listView):
    model = insumo
    template_name = 'insumos/listar.html'
    context_object_name = 'object_list'
    paginate_by = 7
    permission_required = "app.view_categoria"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")
    
    def get_queryset(self):
        queryset = super().get_queryset()
        categoria = self.request.GET.get('categoria')
        stock_bajo = self.request.GET.get('stock_bajo')
        orden = self.request.GET.get('orden')

        if categoria:
            queryset = queryset.filter(categoria_id=categoria)

        if stock_bajo == "1":
            # Filtramos los que tienen menos de 5 unidades (ajusta el umbral si es necesario)
            queryset = queryset.filter(stock__lt=5)

        if orden == "desc":
            queryset = queryset.order_by('-stock')
        elif orden == "asc":
            queryset = queryset.order_by('stock')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sincronización con el Template: Creamos el objeto m.estado_stock
        for obj in context['object_list']:

            umbral = obtener_umbral(obj.unidad)

            if obj.stock <= 0:
                obj.estado_stock = {
                    'texto': f'Agotado ({obj.stock} {obj.unidad})',
                    'clase': 'bg-danger'
                }

            elif obj.stock <= (umbral / 4):
                obj.estado_stock = {
                    'texto': f'Crítico ({obj.stock} {obj.unidad})',
                    'clase': 'bg-danger'
                }

            elif obj.stock <= umbral:
                obj.estado_stock = {
                    'texto': f'Bajo ({obj.stock} {obj.unidad})',
                    'clase': 'bg-warning text-dark'
                }

            else:
                obj.estado_stock = {
                    'texto': f'Normal ({obj.stock} {obj.unidad})',
                    'clase': 'bg-success'
                }
        
        context.update({
            'titulo': 'Listado de insumos',
            'icono': 'fa-solid fa-boxes-stacked',
            'crear_url': reverse_lazy('app:crear_insumos'),
            'Categoria': Categoria.objects.all(),
            'categoria_seleccionada': self.request.GET.get('categoria', ''),
            'stock_bajo': self.request.GET.get('stock_bajo', ''),
            'orden': self.request.GET.get('orden', ''),
            'conteo_stock_bajo_real': insumo.objects.filter(stock__lt=5).count()
        })
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  # Cambia esta URL por la de tu dashboard
            },
            {
                'nombre': 'Insumos',
                'url': None
            }
        ]
        
        return context
    
class InsumosCreateView(PermissionRequiredMixin,CreateView):
    model = insumo
    template_name = 'insumos/crear.html'
    form_class = InsumosForm
    success_url = reverse_lazy('app:listar_insumos')
    permission_required = "app.add_categoria"
    raise_exception = True
    
    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Insumo'
        context['icono'] = 'fa-solid fa-plus'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Insumos',
                'url': reverse_lazy('app:listar_insumos')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        return context
    
    
    
class InsumosUpdateView(PermissionRequiredMixin,UpdateView):
    model = insumo
    form_class = InsumosForm
    template_name = 'insumos/crear.html'
    success_url = reverse_lazy('app:listar_insumos')
    permission_required = "app.change_categoria"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Insumo'
        context['icono'] = 'fa-solid fa-edit'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Insumos',
                'url': reverse_lazy('app:listar_insumos')
            },
            {
                'nombre': 'Editar',
                'url': None
            }
        ]
        return context
    
    
class InsumosDeleteView(PermissionRequiredMixin,DeleteView):
    model = insumo
    template_name = 'insumos/eliminar.html'
    success_url = reverse_lazy('app:listar_insumos')
    permission_required = "app.delete_categoria"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Insumo'
        context['icono'] = 'fa-solid fa-trash'
        context['listar_url'] = reverse_lazy('app:listar_insumos')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Insumos',
                'url': reverse_lazy('app:listar_insumos')
            },
            {
                'nombre': 'Eliminar',
                'url': None
            }
        ]
        return context