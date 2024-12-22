from django import forms
from .models import CustomUser, MaidRequirements, SavedAdrress 
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    street = forms.CharField(required=True, max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Street address'}))
    city = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    state = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'State'}))
    postal_code = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Postal code'}))
    country = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    password1 = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Password1'}))
    password2 = forms.CharField(required=True,max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Password2'}))
    
    class Meta:
        model = CustomUser 
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'street', 'city', 'state', 'postal_code', 'country']

class MaidRequirementForm(forms.ModelForm):
    saved_address = forms.ModelChoiceField(
        queryset=SavedAdrress.objects.none(),
        required=True,
        widgets = forms.Select(attrs={'class' : 'address-dropdown'})
    )
    class Meta:
        model = MaidRequirements
        fields = ['description', 'location']
        widgets = {'description' : forms.TextInput(attrs={'placeholder' : 'List of activities to be performed:'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['saved_address'].queryset = SavedAdrress.objects.filter(user=user)
            