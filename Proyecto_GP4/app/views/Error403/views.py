from django.shortcuts import render

def acceso_denegado(request):
    return render(request, "Errores/403.html", status=403)