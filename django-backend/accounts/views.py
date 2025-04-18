from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# Create your views here.

class LoginPageView(LoginView):
    template_name = 'accounts/login.html'

class LogoutPageView(LogoutView):
    next_page = reverse_lazy('accounts:login')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url = reverse_lazy('accounts:login')
