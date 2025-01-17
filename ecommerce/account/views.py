from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email

User = get_user_model()

from .forms import UserCreateForm, LoginForm, UserUpdateForm

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



def login_user(request):

    # if the user is already logged in:
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
     
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"You are now logged in as {username}")
            return redirect('/')
        
        else: 
            messages.info(request, 'Username or password is incorrect')
            return redirect('account:login')


    else:
        form = LoginForm()
        return render(request, 'account/login/login.html', {'form': form})
    
def logout_user(request):

    # delete the session if the user logs out
    session_keys = list(request.session.keys())
    for key in session_keys:
        if key == 'session_key':
            continue
        del request.session[key]
    logout(request)
    return redirect('/')

@login_required
def view_dashboard(request):
    return render(request,'account/dashboard/view_dashboard.html')

@login_required
def manage_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('account:view_dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'account/dashboard/manage_profile.html', {'form': form})


@login_required
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('/')
    return render(request, 'account/dashboard/delete_account.html')