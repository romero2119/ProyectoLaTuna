from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from app.forms import NotificacionForm


def index(request):
    return render(request, 'main.html')


# ── REEMPLAZA esta función ──────────────────────
def listar_notificaciones(request):
    filtro = request.GET.get('filtro', '')

    if filtro == 'no_leidas':
        notificaciones = Notificacion.objects.filter(leido=False).order_by('-fecha')
    elif filtro == 'leidas':
        notificaciones = Notificacion.objects.filter(leido=True).order_by('-fecha')
    else:
        notificaciones = Notificacion.objects.all().order_by('-fecha')

    return render(request, 'Notificacion/listar.html', {
        'notificaciones': notificaciones,
        'filtro': filtro,
        'contador_no_leidas': Notificacion.objects.filter(leido=False).count(),
        'titulo': 'Listado de Notificaciones',  # ← agrega esto
        'icono': 'fas fa-bell',                  # ← y esto
    })


# ── AGREGA estas dos funciones nuevas ──────────
def marcar_leida(request, pk):
    if request.method == 'POST':
        notif = get_object_or_404(Notificacion, pk=pk)
        notif.leido = True
        notif.save()
    return redirect('app:listar_notificaciones')


def marcar_leidas(request):
    if request.method == 'POST':
        Notificacion.objects.filter(leido=False).update(leido=True)
    return redirect('app:listar_notificaciones')


# ── Todo lo de abajo queda IGUAL ────────────────
class notificacionListView(listView):
    model = Notificacion
    template_name = 'Notificacion/listar.html'

    def get_queryset(self):
        return Notificacion.objects.all()

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Notificaciones'
        context['icono'] = 'fas fa-bell'
        context['crear_url'] = reverse_lazy('app:crear_notificacion')
        return context


class NotificacionCreateView(CreateView):
    model = Notificacion
    template_name = 'Notificacion/crear.html'
    form_class = NotificacionForm
    success_url = reverse_lazy('app:listar_notificaciones')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Notificación'
        context['icono'] = 'fas fa-bell'
        context['listar_url'] = reverse_lazy('app:listar_notificaciones')
        return context


class NotificacionUpdateView(UpdateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'Notificacion/crear.html'
    success_url = reverse_lazy('app:listar_notificaciones')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Notificación'
        context['icono'] = 'fas fa-bell'
        context['listar_url'] = reverse_lazy('app:listar_notificaciones')
        return context


class NotificacionDeleteView(DeleteView):
    model = Notificacion
    template_name = 'Notificacion/eliminar.html'
    success_url = reverse_lazy('app:listar_notificaciones')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Notificación'
        context['icono'] = 'fas fa-bell'
        context['listar_url'] = reverse_lazy('app:listar_notificaciones')
        return context