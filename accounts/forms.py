# agrinest/accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    region = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'region', 'password1', 'password2')

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, required=True)
