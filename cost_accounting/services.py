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
    print(Category.objects.filter(Q(creator__isnull=True) | Q(creator=request.user)
                                  | Q(group__user=User.objects.get(username=request.user.username))).distinct())
    # print(User.objects.get(username=request.user.username))
    # print(Group.objects.get(pk=1).user_set.filter(username=request.user.username))
    # print(Group.objects.get(user=User.objects.get(username=request.user.username)))
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

