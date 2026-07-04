from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.

class LoginView(LoginView):
    template_name = 'login/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('app:dashboard')
    
class LogoutView(LogoutView):
    next_page = reverse_lazy('login:login')    

# Create your views here.
