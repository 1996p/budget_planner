from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
# Create your views here.


def empty(request):
    """Заглушка, которая редикректит с '/' на 'cost_accounting'"""
    return redirect('index')


@login_required
def index(request):
    spendings = Spending.objects.filter(payer=request.user)
    amount = spendings.aggregate(Sum('amount'))['amount__sum']
    categories = Category.objects.filter()
    return render(request, 'spendings.html', {'request': request, 'spendings': spendings,
                                              'amount': amount})


class RegistrationView(CreateView):
    """Обрабатывает GET и POST запросы, отвечает за регистрацию пользователей"""
    template_name = 'register-page.html'
    success_url = '/'
    form_class = UserRegister

    def form_valid(self, form):
        """Создает запись модели ExtendedUser, связанную с User"""
        user = form.save()
        extended_user = ExtendedUser.objects.create(user=user)
        extended_user.save()
        login(self.request, user)
        return redirect('index')


class AuthenticationView(LoginView):
    """Обрабатывает GET и POST запросы, отвечает за аутентификацию пользователей"""
    template_name = 'login-page.html'
    form_class = UserAuthentication


def logout_user(request):
    """Отвечает за выход пользователя из аккаунта"""
    logout(request)
    return redirect('/')



