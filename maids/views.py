from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import LoginForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'D:/ShantaBaiWeb/maids/templates/register.html', {'form':form })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.error_messages)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate the user
            user = authenticate(request, username=email, password=password)  # Use username if using default User model
            # If using CustomUser  model, you may need to adjust the authentication backend
            
            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, "Login successful!")
                return redirect('dashboard')  # Redirect to a dashboard or home page
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'D:/ShantaBaiWeb/maids/templates/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(request, 'login')

@login_required
def dashboard(request):
    user = request.user
    context = {
        'current_money': user.current_money,
        'average_earning': user.average_earnings
    }
    return render(request, 'dashboard.html', context)

