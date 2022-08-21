import django.forms
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import *
from .serializers import *
from rest_framework import generics
# Create your views here.


def empty(request: HttpRequest):
    """Заглушка, которая редикректит с '/' на 'cost_accounting'"""
    return redirect('index')


class IndexPage(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = index_page_logic(request)
        return render(request, 'spendings.html', context)


class RegistrationView(CreateView):
    """Обрабатывает GET и POST запросы, отвечает за регистрацию пользователей"""
    template_name = 'register-page.html'
    success_url = '/'
    form_class = UserRegister

    def form_valid(self, form: UserRegister):
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


def logout_user(request: HttpRequest):
    """Отвечает за выход пользователя из аккаунта"""
    logout(request)
    return redirect('/')


class CreateNewSpending(View):
    """Отвечает за создание новых расходов в БД"""

    def post(self, request: HttpRequest, *args, **kwargs):
        create_new_spending(request)
        return redirect('index')


class CreateNewCategory(View):
    """Отвечает за создание новых категорий расходов в БД"""

    def post(self, request: HttpRequest):
        create_new_category(request)
        return redirect('index')


class SpendingsHistory(LoginRequiredMixin, View):
    """Отвечает за отображение истории расходов на '/history/' """
    def get(self, request, *args, **kwargs):
        context = show_history(request)
        return render(request, 'spendings-history.html', context)


class GroupsInfo(LoginRequiredMixin, View):
    """Отвечает за отображение информацию о группах пользователя,
        А так же за создание новых пользовательских группах"""
    def get(self, request, *args, **kwargs):
        context = display_user_groups(request)
        return render(request, 'groups.html', context)

    def post(self, request, *args, **kwargs):
        create_user_group(request)
        return redirect('groups')


class CertainGroup(LoginRequiredMixin, View):
    """Отвечает за отображение определенной пользовательской группы,
       А так же за создание приглашений пользователей в эту группу
    """
    def get(self, request, *args, **kwargs):
        context = display_certain_user_group(request, kwargs.get('id'))
        return render(request, 'certain-group.html', context)

    def post(self, request, *args, **kwargs):
        context = create_invite_into_group(request, kwargs.get('id'))
        return render(request, 'certain-group.html', context)


class MyCabinet(View):
    """Отвечает за отображение личного кабинета"""
    def get(self, request, *args, **kwargs):
        context = display_my_cabinet(request, kwargs.get('username'))

        return render(request, 'my-cabinet.html', context)


class LeaveGroup(View):
    """Отвечает за выход пользователя из группы"""
    def get(self, request, *args, **kwargs):
        leave_group(request, kwargs.get('group_id'))
        return redirect('groups')


