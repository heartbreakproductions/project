from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['profile_image']
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'phone_number', 'country', 'state']

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    country = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'country', 'state', 'password1', 'password2']
