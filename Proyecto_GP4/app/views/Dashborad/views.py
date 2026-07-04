from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy


class dashboardView(TemplateView):
    template_name = 'Dashboard/dashboard.html'
    
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
        context['titulo'] = 'Inicio'
        context['icono'] = 'list'
        context['breadcrumb'] = [
            {
                'nombre': 'Inicio',
                'url': reverse_lazy('app:dashboard')  # Cambia esta URL por la de tu dashboard
            },
            {
                'nombre': '',
                'url': None
            }
        ]
        return context