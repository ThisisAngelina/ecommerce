from django.urls import path
from django.shortcuts import render
from . import views as v

app_name = 'account'


urlpatterns = [
    path('register', v.register, name='register'),
    path('verify-email', lambda request: render(request, 'account/email/verify_email.html'), name='verify_email'),
    path('login', v.login, name='login'),
    
]