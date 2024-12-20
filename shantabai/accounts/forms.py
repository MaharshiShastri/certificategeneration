from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder':'First name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder':'Last name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']  # Adjust fields as needed
