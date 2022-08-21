from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Spending(models.Model):
    """Описывает расходы, принадлежащие к какой-то категории товаров"""
    payer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Плательщик')
    amount = models.PositiveIntegerField(verbose_name='Потраченная сумма')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория товара')
    short_description = models.CharField(max_length=1000, verbose_name='Краткое описание', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания расходов', null=True)

    class Meta:
        db_table = 'spending'

    def __str__(self):
        return f'{self.payer} -> {self.category} | {self.amount}'


class Category(models.Model):
    """Описывает категории товаров, на которые человек тратит деньги"""
    title = models.CharField(max_length=50, verbose_name='Название категории')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Трата на группу", blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Создатель категории')

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


class InviteToGroup(models.Model):
    """Описывает сущность приглашения в пользовательскую группу"""
    class InviteStatus(models.TextChoices):
        accepted = 'AC', _('ACCEPTED')
        denied = 'DN', _('DENIED')
        not_checked = 'NC', _('NOT CHECKED')

    to_group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='В какую группу')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Приглашенный', related_name="related_guest")
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Тот, кто приглашает', related_name="related_inviter")
    status = models.CharField(max_length=2, verbose_name='Статус приглашения', choices=InviteStatus.choices, default=InviteStatus.not_checked)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания приглашения')

    def __str__(self):
        return f'{self.inviter.username} приглашает {self.guest.username} -> {self.to_group.name}'

    class Meta:
        db_table = 'invite_to_group'
        unique_together = ('guest', 'inviter')