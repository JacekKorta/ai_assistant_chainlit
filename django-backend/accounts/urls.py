from django.urls import path
from .views import LoginPageView, LogoutPageView, DashboardView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
] 