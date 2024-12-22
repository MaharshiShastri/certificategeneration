from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, MaidRequirementForm
from .models import MaidRequirements

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password2'])
                user.save()
                return render(request, 'dashboard.html')
            except Exception as e:
                print(form.errors)
    else:
        messages.error(request, "Please correct the errors below.")
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form':form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
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
    address = user.street + "," + user.city + "," + user.state + "," + user.zip
    context = {
        'address': user.address
    }
    return render(request, 'dashboard.html', context)

@login_required
def hire_maids(request):
    if request.method == 'POST':
        form = MaidRequirementForm(request.POST, user = request.user)
        if form.is_valid():
            requirement = form.save(commit=False)
            saved_address =  form.cleaned_data.get('saved_address')
            if saved_address:
                requirement.description += f"\nLocation: {saved_address.address}"
            requirement.save()
            return redirect('hire_maids')
    else:
        form = MaidRequirementForm(request.POST)
    
    requirements = MaidRequirements.objects.all().oreder_by('-created_at')
    return render(request, 'hire_maids.html', {'form': form, 'requirements': requirements})
        