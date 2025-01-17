from django.urls import path
from django.shortcuts import render
from . import views as v

app_name = 'account'


urlpatterns = [
    path('register', v.register, name='register'),
    path('verify-email', lambda request: render(request, 'account/email/verify_email.html'), name='verify_email'),
    path('login', v.login_user, name='login'),
    path('logout', v.logout_user, name='logout'),

    path('dashboard/', v.view_dashboard, name='view_dashboard'),
    path('profile-management', v.manage_profile, name='manage_profile'),
    path('delete-account', v.delete_user, name='delete_account'),

    
]