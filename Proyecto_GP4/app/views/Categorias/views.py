from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages

from app.models import Categoria
from app.forms import CategoriaForm


def index(request):
    return render(request, 'main.html')


def listar_categorias(request):
    context = {
        'categorias': Categoria.objects.all()
    }
    return render(request, 'Categoria/listar.html', context)


class CategoriaListView(PermissionRequiredMixin, ListView):
    model = Categoria
    template_name = 'Categoria/listar.html'
    permission_required = 'app.view_categoria'
    raise_exception = True

    def handle_no_permission(self):
        return redirect('app:acceso_denegado')

    def get_queryset(self):
        queryset = Categoria.objects.all()

        nombre = self.request.GET.get('buscar', '')
        estado = self.request.GET.get('estado', '')

        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)

        if estado:
            queryset = queryset.filter(estado__icontains=estado)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Listado de Categorías'
        context['icono'] = 'list'
        context['crear_url'] = reverse_lazy('app:crear_categoria')
        context['buscar'] = self.request.GET.get('buscar', '')
        context['estado'] = self.request.GET.get('estado', '')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  # Cambia esta URL por la de tu dashboard
            },
            {
                'nombre': 'Categorías',
                'url': None
            }
        ]

        return context


class CategoriaCreateView(PermissionRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'Categoria/crear.html'
    success_url = reverse_lazy('app:listar_categorias')

    permission_required = 'app.add_categoria'
    raise_exception = True

    def handle_no_permission(self):
        return redirect('app:acceso_denegado')

    def form_valid(self, form):
        messages.success(self.request, 'La categoría fue creada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'No fue posible crear la categoría.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Crear Categoría'
        context['icono'] = 'plus'
        context['listar_url'] = reverse_lazy('app:listar_categorias')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  
            },
            {
                'nombre': 'Categorías',
                'url': reverse_lazy('app:listar_categorias')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        return context


class CategoriaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'Categoria/crear.html'
    success_url = reverse_lazy('app:listar_categorias')

    permission_required = 'app.change_categoria'
    raise_exception = True

    def handle_no_permission(self):
        return redirect('app:acceso_denegado')

    def form_valid(self, form):
        messages.success(self.request, 'La categoría fue actualizada correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'No fue posible actualizar la categoría.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Categoría'
        context['icono'] = 'edit'
        context['listar_url'] = reverse_lazy('app:listar_categorias')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Categorías',
                'url': reverse_lazy('app:listar_categorias')
            },
            {
                'nombre': 'Editar',
                'url': None
            }
        ]
        return context


class CategoriaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'Categoria/eliminar.html'
    success_url = reverse_lazy('app:listar_categorias')

    permission_required = 'app.delete_categoria'
    raise_exception = True

    def handle_no_permission(self):
        return redirect('app:acceso_denegado')

    def form_valid(self, form):
        messages.success(self.request, 'La categoría fue eliminada correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Eliminar Categoría'
        context['icono'] = 'trash'
        context['listar_url'] = reverse_lazy('app:listar_categorias')
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Categorías',
                'url': reverse_lazy('app:listar_categorias')
            },
            {
                'nombre': 'Eliminar',
                'url': None
            }
        ]
        return context