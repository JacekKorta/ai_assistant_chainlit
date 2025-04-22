from django.urls import path
from . import api 

app_name = 'accounts_api' # Ważne dla reverse w testach

urlpatterns = [
    path('verify-credentials/', api.VerifyCredentialsAPIView.as_view(), name='verify_credentials'),
] 