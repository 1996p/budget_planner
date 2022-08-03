from django.db.models import Sum
from django.http import HttpRequest

from .forms import *
from .models import *


def IndexPageLogic(request: HttpRequest) -> dict:
    """Описывает бизнес-логику /cost-acconting, возвращает context"""
    spendings = Spending.objects.filter(payer=request.user)
    amount = spendings.aggregate(Sum('amount'))['amount__sum']
    add_category_form = AddCategory()
    add_spending_form = AddSpending(user=request.user)

    context = {
        'request': request,
        'spendings': spendings,
        'amount': amount,
        'add_category_form': add_category_form,
        'add_spending_form': add_spending_form,
    }

    return context
