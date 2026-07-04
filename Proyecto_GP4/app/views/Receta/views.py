from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import *
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404

def index(request):
    return render(request, 'main.html')
# Create your views here.
def listar_receta(request):
    nombre = {
        
        'recetas': Receta.objects.all()
    }
    return render(request, 'receta/listar.html', nombre)


class RecetaListView(PermissionRequiredMixin, listView):
    model = Receta
    template_name = 'receta/listar.html'
    form_class = RecetaForm
    success_url = reverse_lazy('app:listar_receta')
    permission_required = "app.view_receta"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_queryset(self):
        # Programación Senior: Evitamos el problema N+1 con prefetch_related
        return Receta.objects.prefetch_related('detalles__insumo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        recetas_data = []
        for receta in context['object_list']:
            detalles_data = []
            for detalle in receta.detalles.all():
                # Traemos los datos crudos y directos de la base de datos
                detalles_data.append({
                    'insumo_nombre': detalle.insumo.nombre,
                    'cantidad': float(detalle.cantidad),
                    'unidad': detalle.insumo.unidad,  # Directo del modelo insumo
                    'precio_unitario': float(detalle.insumo.valor),
                    'stock_suficiente': detalle.insumo.stock >= detalle.cantidad,
                })
            
            recetas_data.append({
                'id': receta.id,
                'plato_nombre': receta.plato.nombre,
                'detalles': detalles_data,
            })
        
        context.update({
            'recetas_data': recetas_data,
            'titulo': 'Gestión de Recetas',
            'crear_url': reverse_lazy('app:crear_receta')
        })
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  # Cambia esta URL por la de tu dashboard
            },
            {
                'nombre': 'Recetas',
                'url': None
            }
        ]
        return context
    
class RecetaCreateView(PermissionRequiredMixin, CreateView):
    model = Receta
    template_name = 'receta/crear.html'
    form_class = RecetaForm
    success_url = reverse_lazy('app:listar_receta')
    permission_required = "app.add_receta"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = DetalleFormSet(self.request.POST or None)
        context['titulo'] = 'Crear Receta'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Recetas',
                'url': reverse_lazy('app:listar_receta')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        return self.render_to_response(context)

        
    
class RecetaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'receta/crear.html'
    success_url = reverse_lazy('app:listar_receta')
    permission_required = "app.change_receta"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = DetalleFormSet(self.request.POST or None, instance=self.object)
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Recetas',
                'url': reverse_lazy('app:listar_receta')
            },
            {
                'nombre': 'Editar',
                'url': None
            }
        ]
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            form.save()
            formset.save()
            return redirect(self.success_url)
        return self.render_to_response(context)
    
class RecetaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Receta
    template_name = 'receta/eliminar.html'
    success_url = reverse_lazy('app:listar_receta')
    permission_required = "app.delete_receta"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Receta'
        context['icono'] = 'fa-solid fa-trash'
        context['listar_url'] = reverse_lazy('app:listar_receta')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Recetas',
                'url': reverse_lazy('app:listar_receta')
            },
            {
                'nombre': 'Eliminar',
                'url': None
            }
        ]
        return context