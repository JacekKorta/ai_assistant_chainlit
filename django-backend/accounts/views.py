from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# Create your views here.

class LoginPageView(LoginView):
    template_name = 'accounts/login.html'

class LogoutPageView(LogoutView):
    next_page = reverse_lazy('login')

class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'
