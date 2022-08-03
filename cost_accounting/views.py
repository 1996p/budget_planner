from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import *
# Create your views here.


def empty(request):
    """Заглушка, которая редикректит с '/' на 'cost_accounting'"""
    return redirect('index')


class IndexPage(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = IndexPageLogic(request)
        return render(request, 'spendings.html', context)


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


class CreateNewSpending(View):
    """Отвечает за создание новых расходов в БД"""

    def post(self, request, *args, **kwargs):
        user = request.user
        _, spending_amount, category_id = request.POST.values()
        category = Category.objects.get(pk=category_id)
        new_spending = Spending.objects.create(payer=user,
                                               amount=spending_amount,
                                               category=category)
        new_spending.save()
        return redirect('index')


