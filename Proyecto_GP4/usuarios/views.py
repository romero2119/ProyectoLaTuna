from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Usuario
from .forms import UserForm, PerfilForm, UserEditForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.http import Http404
from django.db.models import Q
from app.utils import exportar_pdf, exportar_excel



class AdminOrSuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('login:login')
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated and (
                user.is_superuser or getattr(
                    getattr(user, 'perfil', None), 'rol', '') == 'administrador'
            )
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("app:acceso_denegado")

#  LISTAR USUARIOS
class ListarUsuariosView(AdminOrSuperuserRequiredMixin, ListView):

    model = User
    template_name = 'usuarios/listar.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        queryset = User.objects.filter(
            is_superuser=False
        ).select_related('perfil')

        buscar = self.request.GET.get("buscar")
        estado = self.request.GET.get("estado")
        rol = self.request.GET.get("rol")

        # Buscar por usuario, nombre, apellido o cédula
        if buscar:
            queryset = queryset.filter(
                Q(username__icontains=buscar) |
                Q(first_name__icontains=buscar) |
                Q(last_name__icontains=buscar) |
                Q(perfil__cedula__icontains=buscar)
            )

        # Filtrar por estado
        if estado == "activo":
            queryset = queryset.filter(is_active=True)
        elif estado == "inactivo":
            queryset = queryset.filter(is_active=False)

        # Filtrar por rol
        if rol:
            queryset = queryset.filter(perfil__rol=rol)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["titulo"] = "Listado de Usuarios"
        context["icono"] = "fas fa-cash-register"

        context["buscar"] = self.request.GET.get("buscar", "")
        context["estado"] = self.request.GET.get("estado", "")
        context["rol"] = self.request.GET.get("rol", "")

        # Enviar los roles al template
        context["roles"] = Usuario._meta.get_field("rol").choices
        
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  # Cambia esta URL por la de tu dashboard
            },
            {
                'nombre': 'Usuarios',
                'url': None
            }
        ]

        return context

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("app:acceso_denegado")

#  CREAR USUARIO


class CrearUsuarioView(AdminOrSuperuserRequiredMixin, View):
    def get(self, request):
        context = {
            'titulo': 'Crear Nuevo Usuario',
            'user_form': UserForm(),
            'perfil_form': PerfilForm()
        }
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Usuarios',
                'url': reverse_lazy('usuarios:listar')
            },
            {
                'nombre': 'Crear',
                'url': None
            }
        ]
        return render(request, 'usuarios/crear.html', context)

    def post(self, request):
        #  datos de los dos formularios
        user_form = UserForm(request.POST)
        perfil_form = PerfilForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            # 1. Guardamos el User pero sin commit
            user = user_form.save(commit=False)
            # Encriptamos la contraseña
            user.set_password(user_form.cleaned_data['password'])
            user.save()  # Ahora  guardamos el usuario

            # 2. Guardamos el Perfil y lo enlazamos al User creado
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()

            grupo = Group.objects.get(name=perfil.rol)
            user.groups.set([grupo])  # Asignamos el grupo al usuario

            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios:listar')

        # Si hay errores, recargamos
        context = {
            'titulo': 'Crear Nuevo Usuario',
            'user_form': user_form,
            'perfil_form': perfil_form
        }
        return render(request, 'usuarios/crear.html', context)

#  EDITAR USUARIO


class EditarUsuarioView(AdminOrSuperuserRequiredMixin, View):
    def get(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)
        # Obtenemos el perfil, o lo creamos si por alguna razon no existe
        perfil, created = Usuario.objects.get_or_create(user=usuario)

        context = {
            'titulo': 'Editar Usuario',
            'user_form': UserEditForm(instance=usuario),
            'perfil_form': PerfilForm(instance=perfil),
            'usuario': usuario
        }
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')
            },
            {
                'nombre': 'Usuarios',
                'url': reverse_lazy('usuarios:listar')
            },
            {
                'nombre': 'Editar',
                'url': None
            }
        ]
        return render(request, 'usuarios/editar.html', context)

    def post(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)
        perfil = get_object_or_404(Usuario, user=usuario)

        user_form = UserEditForm(request.POST, instance=usuario)
        perfil_form = PerfilForm(request.POST, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)

            # Solo actualizamos la contraseña si el usuario escribio una nueva
            nueva_password = user_form.cleaned_data.get('password')
            if nueva_password:
                user.set_password(nueva_password)

            user.save()
            perfil_form.save()

            grupo = Group.objects.get(name=perfil.rol)
            user.groups.set([grupo])  # Actualizamos el grupo del usuario

            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios:listar')

        context = {
            'titulo': 'Editar Usuario',
            'user_form': user_form,
            'perfil_form': perfil_form,
            'usuario': usuario
        }
        return render(request, 'usuarios/editar.html', context)

# DESACTIVAR USUARIO


class DesactivarUsuarioView(AdminOrSuperuserRequiredMixin, View):
    def get(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)
        context = {
            'titulo': 'Desactivar Usuario',
            'object': usuario,
            'listar_url': reverse_lazy('usuarios:listar')
        }
        return render(request, 'usuarios/eliminar.html', context)

    def post(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)

        # En lugar de usuario.delete(), lo desactivamos:
        usuario.is_active = False
        usuario.save()

        messages.success(request, 'Usuario desactivado correctamente.')
        return redirect('usuarios:listar')


class CambiarEstadoUsuarioView(View):
    def post(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)

        # Invertimos el estado
        usuario.is_active = not usuario.is_active
        usuario.save()

        # Mensaje dinamico
        estado = "activado" if usuario.is_active else "desactivado"
        messages.success(request, f'Usuario {estado} correctamente.')

        return redirect('usuarios:listar')

class ExportarUsuariosPDF(View):

    def get(self, request):
        buscar = request.GET.get('buscar', '')
        estado = request.GET.get('estado', '')
        rol = request.GET.get('rol', '')

        usuarios = User.objects.select_related('perfil')

        if buscar:
            usuarios = usuarios.filter(
                Q(username__icontains=buscar) |
                Q(first_name__icontains=buscar) |
                Q(last_name__icontains=buscar) |
                Q(perfil__cedula__icontains=buscar)
            )

        if estado == "activo":
            usuarios = usuarios.filter(is_active=True)

        elif estado == "inactivo":
            usuarios = usuarios.filter(is_active=False)

        if rol:
            usuarios = usuarios.filter(perfil__rol=rol)

        columnas = [
            "Usuario",
            "Nombre",
            "Rol",
            "Cédula",
            "Estado"
        ]

        datos = [
            (
                u.username,
                f"{u.first_name} {u.last_name}",
                u.perfil.get_rol_display() if hasattr(u, "perfil") else "",
                u.perfil.cedula if hasattr(u, "perfil") else "",
                "Activo" if u.is_active else "Inactivo",
            )
            for u in usuarios
        ]

        return exportar_pdf(
            "Reporte de Usuarios",
            columnas,
            datos,
            "usuarios"
        )
        
class ExportarUsuariosExcel(View):

    def get(self, request):
        buscar = request.GET.get('buscar', '')
        estado = request.GET.get('estado', '')
        rol = request.GET.get('rol', '')

        usuarios = User.objects.select_related('perfil')

        if buscar:
            usuarios = usuarios.filter(
                Q(username__icontains=buscar) |
                Q(first_name__icontains=buscar) |
                Q(last_name__icontains=buscar) |
                Q(perfil__cedula__icontains=buscar)
            )

        if estado == "activo":
            usuarios = usuarios.filter(is_active=True)
        elif estado == "inactivo":
            usuarios = usuarios.filter(is_active=False)

        if rol:
            usuarios = usuarios.filter(perfil__rol=rol)

        columnas = [
            "Usuario",
            "Nombre",
            "Rol",
            "Cédula",
            "Estado"
        ]

        datos = [
            (
                u.username,
                f"{u.first_name} {u.last_name}",
                u.perfil.get_rol_display() if hasattr(u, "perfil") else "",
                u.perfil.cedula if hasattr(u, "perfil") else "",
                "Activo" if u.is_active else "Inactivo",
            )
            for u in usuarios
        ]

        return exportar_excel(
            "Reporte de Usuarios",
            columnas,
            datos,
            "usuarios"
        )