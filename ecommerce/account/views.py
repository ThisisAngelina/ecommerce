from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email

User = get_user_model()

from .forms import UserCreateForm

def register(request):

    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            #Create new user
            user = User.objects.create_user(
                username=username, email=email, password=password
            )

            user.is_active = False

            send_email(user)
            
            return redirect('/account/verify-email')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form}) 



def login(request):
    return render(request, 'account/login/login.html')