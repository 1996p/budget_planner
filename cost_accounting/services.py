import datetime

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
        'joined_groups': joined_groups,
        'category_amount': category_amount.items()
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
    spendings_per_day = defaultdict(list)
    for spending in spendings:
        spendings_per_day[spending.creation_date.date()].append(spending)

    context = {
        'spendings_per_day': spendings_per_day.items(),
        'today': datetime.datetime.today().date(),
        'yesterday': datetime.datetime.today().date() - datetime.timedelta(1),
    }
    return context


def display_user_groups(request: HttpRequest) -> dict:
    """Описывает бизнес-логику отображения групп пользователя"""
    groups = Group.objects.filter(user=User.objects.get(username=request.user.username))
    form = CreateGroup()
    context = {
        'groups': groups,
        'form': form,
    }

    return context


def create_user_group(request: HttpRequest) -> None:
    """Отвечает за создания новой группы пользователем
       По дефолту в ней один участник - ее создатель
    """
    new_group = Group.objects.create(name=request.POST['name'])
    user = User.objects.get(username=request.user.username)
    user.groups.add(new_group)
    user.save()
    new_group.save()


def display_certain_user_group(request: HttpRequest, pk: int) -> dict:
    """Отвечает за создание контекстных переменных
    для отображения инфомарции о конкретной пользовательской группе"""
    payers = defaultdict(int)
    group = Group.objects.get(pk=pk)
    spendings = Spending.objects.filter(category__group=group).order_by('-creation_date')
    spendings_per_day = defaultdict(list)
    common_category_amount = defaultdict(int)

    create_invite_form = CreateGroupInviteForm()

    for spending in spendings:
        payers[spending.payer.username] += spending.amount
        spendings_per_day[spending.creation_date.date()].append(spending)
        common_category_amount[spending.category.title] += spending.amount

    context = {
        'payers_name': payers.keys(),
        'amounts': payers.values(),
        'spendings_per_day': spendings_per_day.items(),
        'today': datetime.datetime.today().date(),
        'yesterday': datetime.datetime.today().date() - datetime.timedelta(1),
        'amount': spendings.aggregate(Sum('amount')).get('amount__sum'),
        'category_amount': common_category_amount.items(),
        'form': create_invite_form,
        'group_id': group.id
    }
    return context


def create_invite_into_group(request: HttpRequest, group_id: int) -> dict:
    """Отвечает за создания в БД приглашения пользователя в группу
       Значения новой контекстной переменной 'creation_invite_status':
       "0" - приглашение было создано,
       "1" - приглашение уже создано, но пользователь на него не ответил,
       "2" - нет такого пользователя, чтобы пригласить его
    """
    group = Group.objects.get(pk=group_id)
    context = display_certain_user_group(request, group_id)
    try:
        guest = User.objects.get(username=request.POST['guest'])
    except Exception:
        context['creation_invite_status'] = 2
        context['guest_username'] = request.POST['guest']
        context['group_name'] = group.name
        return context

    inviter = User.objects.get(username=request.user.username)
    try:
        invite = InviteToGroup.objects.get(
            to_group=group,
            guest=guest
        )
    except Exception:
        invite = InviteToGroup.objects.create(
            to_group=group,
            inviter=inviter,
            guest=guest
        )

    else:
        if invite.status == 'NC':
            context['creation_invite_status'] = 1
            context['guest_username'] = request.POST['guest']
            context['group_name'] = group.name
            return context
        else:
            invite = InviteToGroup.objects.create(
                to_group=group,
                inviter=inviter,
                guest=guest
            )

    invite.save()
    context['creation_invite_status'] = 0
    context['guest_username'] = request.POST['guest']
    context['group_name'] = group.name
    return context
