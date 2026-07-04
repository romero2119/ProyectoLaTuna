from django.db import models
from django.contrib.auth.models import User

# ROLES
ROLES = (
    ('administrador', 'Administrador'),
    ('empleado', 'Empleado'),
)

class Usuario(models.Model):
    # Relación 1 a 1 con el usuario nativo de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='empleado')
    cedula = models.CharField(max_length=20, unique=True, verbose_name='Cédula')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
        db_table = 'perfil_usuario'