from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
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

# Password reset - extending Django's auth standard class-based views
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password/password_reset.html',
        email_template_name='account/password/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')),
        name='password_reset'),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password/password_reset_done.html'),
        name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')),
        name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password_reset_complete.html'),
        name='password_reset_complete'),
    
]