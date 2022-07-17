from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class UserRegister(UserCreationForm):
    """Форма регистрации пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Login'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'fadeIn third', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'placeholder': 'Repeat you password'}))
    policy_agree = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'policyAgree'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'policy_agree')


class UserAuthentication(AuthenticationForm):
    """Форма атуентификации пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'placeholder': 'Password'}))


class AddCategory(forms.ModelForm):
    """Форма добавления новой категории трат"""
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    group = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Название'}))

    class Meta:
        model = Category
        exclude = ('author', )


