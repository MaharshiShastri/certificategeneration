from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.urls import reverse


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'dashboard.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form':form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
            print(reverse('dashboard'))
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            print("Forms error:",form.errors)
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

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

