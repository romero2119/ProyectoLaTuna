from django.urls import path
from . import views
from .views import (
    ListarUsuariosView,
    CrearUsuarioView,
    EditarUsuarioView,
    DesactivarUsuarioView,
    CambiarEstadoUsuarioView,
    ExportarUsuariosPDF,
    ExportarUsuariosExcel,
)
from .backup import backup_usuarios
from .permisos_views import (
    ListarPermisosView,
    EditarPermisosGrupoView,
)

app_name = "usuarios"

urlpatterns = [
    # Usuarios
    path("listar/", ListarUsuariosView.as_view(), name="listar"),
    path("crear/", CrearUsuarioView.as_view(), name="crear"),
    path("editar/<int:pk>/", EditarUsuarioView.as_view(), name="editar"),
    path("desactivar/<int:pk>/", DesactivarUsuarioView.as_view(), name="desactivar"),
    path("estado/<int:pk>/", CambiarEstadoUsuarioView.as_view(), name="cambiar_estado"),

    # Exportaciones
    path("exportar_pdf/", ExportarUsuariosPDF.as_view(), name="exportar_pdf"),
    path("exportar_excel/", ExportarUsuariosExcel.as_view(), name="exportar_excel"),

    # Permisos
    path("permisos/", ListarPermisosView.as_view(), name="listar_permisos"),
    path(
        "permisos/editar/<int:pk>/",
        EditarPermisosGrupoView.as_view(),
        name="editar_permisos",
    ),

    # Backup
    path("backup/", backup_usuarios, name="backup_usuarios"),
]