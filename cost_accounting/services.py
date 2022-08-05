from django.db.models import Sum
from django.http import HttpRequest

from .forms import *
from .models import *
from collections import defaultdict


def index_page_logic(request: HttpRequest) -> dict:
    """Описывает создание контекстных переменных для домашней страницы"""
    spendings = Spending.objects.filter(payer=request.user)
    amount = spendings.aggregate(Sum('amount'))['amount__sum']
    add_category_form = AddCategory()
    add_spending_form = AddSpending(user=request.user)
    category_amount = defaultdict(int)
    joined_groups = Group.objects.filter(user=User.objects.get(username=request.user.username)).count

    for spending in spendings:
        category_amount[spending.category.title] += spending.amount

    context = {
        'request': request,
        'spendings': spendings,
        'amount': amount,
        'add_category_form': add_category_form,
        'add_spending_form': add_spending_form,
        'category_titles': category_amount.keys(),
        'category_amounts': category_amount.values(),
        'joined_groups': joined_groups
    }

    return context


def create_new_spending(request: HttpRequest) -> None:
    """Описывает бизнес-логику добавления новых расходов"""
    user = request.user
    _, spending_amount, category_id = request.POST.values()
    category = Category.objects.get(pk=category_id)
    new_spending = Spending.objects.create(payer=user,
                                           amount=spending_amount,
                                           category=category)
    new_spending.save()


def create_new_category(request: HttpRequest) -> None:
    """Описывает бизнес-логику создания новой категории трат"""
    _, title, group_id = request.POST.values()
    user = request.user
    if group_id:
        group = Group.objects.get(pk=group_id)
        new_category = Category.objects.create(title=title,
                                               creator=user,
                                               group=group)
    else:
        new_category = Category.objects.create(title=title,
                                               creator=user)
    new_category.save()


def show_history(request: HttpRequest) -> dict:
    """Описывает бизнес-логику отображение истории расходов,
    создает контекстные переменные для шаблона"""
    spendings = Spending.objects.filter(payer=request.user).order_by('-creation_date')
    context = {
        'spendings': spendings
    }
    return context