from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import CreateView

from .forms import *
# Create your views here.


def empty(request):
    """Заглушка, которая редикректит с '/' на 'cost_accounting'"""
    return redirect('index')


def index(request):
    return render(request, 'base.html', {})


class RegistrationView(CreateView):
    """Обрабатывает GET и POST запросы, отвечает за регистрацию пользователей"""
    template_name = 'register-page.html'
    success_url = '/'
    form_class = UserRegister

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class AuthenticationView(LoginView):
    """Обрабатывает GET и POST запросы, отвечает за аутентификацию пользователей"""
    template_name = 'login-page.html'
    form_class = UserAuthentication


def logout_user(request):
    """Отвечает за выход пользователя из аккаунта"""
    logout(request)
    return redirect('/')



