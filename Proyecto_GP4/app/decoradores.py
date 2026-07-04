from functools import wraps
from django.shortcuts import render


def solo_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # Si no está autenticado
        if not request.user.is_authenticated:
            return render(
                request,
                "Errores/403.html",
                status=403
            )

        # Si no tiene perfil o no es administrador
        try:
            if request.user.perfil.rol != "administrador":
                return render(
                    request,
                    "Errores/403.html",
                    status=403
                )
        except Exception:
            return render(
                request,
                "Errores/403.html",
                status=403
            )

        return view_func(request, *args, **kwargs)

    return wrapper