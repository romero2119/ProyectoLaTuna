from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import PlatoForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.views import View
from app.utils import exportar_pdf, exportar_excel
def index(request):
    return render(request, 'main.html')
# Create your views here.
def listar_platos(request):
    nombre = {
        
        'platos': Plato.objects.all()
    }
    return render(request, 'plato/listar.html', nombre)

class PlatoListView(PermissionRequiredMixin, listView):
    model = Plato
    template_name = 'plato/listar.html'
    permission_required = "app.view_plato"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    #METODO DISPATCH
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #if request.method == 'GET':
            #return redirect('app:listar_categorias')    
        return super().dispatch(request, *args, **kwargs)
        
    
    #METODO POST
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    #METODO GET CONTEXT DATA
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Platos'
        context['icono'] = 'fa-solid fa-utensils'
        context['crear_url'] = reverse_lazy('app:crear_plato')
        context['buscar'] = self.request.GET.get('buscar', '')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Platos',
                'url': None
            }
        ]
        return context
    
    def get_queryset(self):
        queryset = Plato.objects.all()
        nombre = self.request.GET.get('buscar', '')
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        return queryset
class PlatoCreateView(PermissionRequiredMixin, CreateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'plato/crear.html'
    success_url = reverse_lazy('app:listar_platos')
    permission_required = "app.add_plato"
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
        context['titulo'] = 'Crear Plato'
        context['icono'] = 'fas fa-utensils'
        context['listar_url'] = reverse_lazy('app:listar_platos')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Platos',
                'url': reverse_lazy('app:listar_platos')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        return context
    
    
class PlatoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'plato/crear.html'
    success_url = reverse_lazy('app:listar_platos')
    permission_required = "app.change_plato"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = self.request.FILES  # ← agrega esto
        return kwargs
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Plato'
        context['icono'] = 'fa-solid fa-pen-to-square'
        context['listar_url'] = reverse_lazy('app:listar_platos')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Platos',
                'url': reverse_lazy('app:listar_platos')
            },
            {
                'nombre': 'Editar',
                'url': None
            }
        ]
        return context
    
      
class PlatoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Plato
    template_name = 'plato/eliminar.html'
    success_url = reverse_lazy('app:listar_platos')
    permission_required = "app.delete_plato"
    raise_exception = True

    def handle_no_permission(self):
        return redirect("app:acceso_denegado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Plato'
        context['icono'] = 'fa-solid fa-trash'
        context['listar_url'] = reverse_lazy('app:listar_platos')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Platos',
                'url': reverse_lazy('app:listar_platos')
            },
            {
                'nombre': 'Eliminar',
                'url': None
            }
        ]
        return context
    
class ExportarPlatoPDF(View):

    def get(self, request):
        buscar = request.GET.get("buscar", "")

        platos = Plato.objects.all()

        if buscar:
            platos = platos.filter(nombre__icontains=buscar)

        columnas = [
            "ID",
            "Categoría",
            "Nombre",
            "Descripción",
            "Precio",
        ]

        datos = [
            (
                plato.id_plato,
                plato.categoria.nombre if plato.categoria else "",
                plato.nombre,
                plato.descripcion,
                plato.precio,
            )
            for plato in platos
        ]

        return exportar_pdf(
            "Reporte de Platos",
            columnas,
            datos,
            "platos"
        )


class ExportarPlatoExcel(View):

    def get(self, request):
        buscar = request.GET.get("buscar", "")

        platos = Plato.objects.all()

        if buscar:
            platos = platos.filter(nombre__icontains=buscar)

        columnas = [
            "ID",
            "Categoría",
            "Nombre",
            "Descripción",
            "Precio",
        ]

        datos = [
            (
                plato.id_plato,
                plato.categoria.nombre if plato.categoria else "",
                plato.nombre,
                plato.descripcion,
                plato.precio,
            )
            for plato in platos
        ]

        return exportar_excel(
            "Reporte de Platos",
            columnas,
            datos,
            "platos"
        )
