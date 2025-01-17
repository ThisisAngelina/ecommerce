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

        # get data from the form
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

        # create a new user account 
            new_user = User.objects.create_user(username=username, email=user_email, password=password)
        
        # keep the user inactive for the moment, until they confirm their email address
            new_user.is_active = False
    else:
        form = UserCreateForm()
    return render(request, 'account/register.html', {'form': form})

