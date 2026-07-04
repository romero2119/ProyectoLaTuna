"""Vistas  dashboard  permisos y grupos."""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


class AdminOrSuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('login:login')
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated and (
                user.is_superuser or getattr(getattr(user, 'perfil', None), 'rol', '') == 'administrador'
            )
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied('No tiene permiso para acceder a esta seccion.')


class ListarPermisosView(AdminOrSuperuserRequiredMixin, View):
    """Dashboard personalizado para gestionar roles y permisos."""
    
    def get(self, request):
        grupos = Group.objects.prefetch_related('permissions').all()
        context = {
            'titulo': 'Panel de Permisos y Roles',
            'grupos': grupos,
            'total_grupos': grupos.count(),
        }
        return render(request, 'usuarios/permisos_dashboard.html', context)


class EditarPermisosGrupoView(AdminOrSuperuserRequiredMixin, View):
    """Permite editar los permisos asignados a un grupo."""
    
    def get(self, request, pk):
        grupo = get_object_or_404(Group, pk=pk)
        # Obtener todos los permisos disponibles
        todos_permisos = Permission.objects.all()
        permisos_asignados = grupo.permissions.all()
        
        # Agrupar permisos por aplicación
        permisos_por_app = {}
        for permiso in todos_permisos:
            app_label = permiso.content_type.app_label
            if app_label not in permisos_por_app:
                permisos_por_app[app_label] = []
            
            permiso_data = {
                'id': permiso.id,
                'nombre': permiso.name,
                'descripcion': f"{permiso.content_type.name} - {permiso.codename}",
                'asignado': permiso in permisos_asignados,
            }
            permisos_por_app[app_label].append(permiso_data)
        
        context = {
            'titulo': f'Editar Permisos - {grupo.name}',
            'grupo': grupo,
            'permisos_por_app': dict(sorted(permisos_por_app.items())),
            'total_permisos': len(permisos_asignados),
        }
        return render(request, 'usuarios/editar_permisos.html', context)
    
    def post(self, request, pk):
        grupo = get_object_or_404(Group, pk=pk)
        
        # Obtener los IDs de permisos seleccionados
        permisos_ids = request.POST.getlist('permisos')
        
        # Limpiar permisos actuales y asignar los nuevos
        grupo.permissions.clear()
        permisos_nuevos = Permission.objects.filter(id__in=permisos_ids)
        grupo.permissions.set(permisos_nuevos)
        
        messages.success(request, f'Permisos del grupo "{grupo.name}" actualizados correctamente.')
        return redirect('usuarios:listar_permisos')
