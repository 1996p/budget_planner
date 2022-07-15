from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.


class Spending(models.Model):
    """Описывает расходы, принадлежащие к какой-то категории товаров"""
    payer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Плательщик')
    amount = models.PositiveIntegerField(verbose_name='Потраченная сумма')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория товара')

    class Meta:
        db_table = 'spending'

    def __str__(self):
        return f'{self.payer} -> {self.category} | {self.amount}'


class Category(models.Model):
    """Описывает категории товаров, на которые человек тратит деньги"""
    title = models.CharField(max_length=50, verbose_name='Название категории')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Трата на группу", blank=True, null=True)

    class Meta:
        db_table = 'spending_category'

    def __str__(self):
        return self.title


class ExtendedUser(models.Model):
    """Описывает расширенную версию модели пользователя"""
    profile_image = models.ImageField(verbose_name='Аватарка', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
