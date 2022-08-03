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

    for spending in spendings:
        category_amount[spending.category.title] += spending.amount

    context = {
        'request': request,
        'spendings': spendings,
        'amount': amount,
        'add_category_form': add_category_form,
        'add_spending_form': add_spending_form,
        'category_titles': category_amount.keys(),
        'category_amounts': category_amount.values()
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
