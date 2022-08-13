# Generated by Django 4.0.6 on 2022-08-07 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('cost_accounting', '0007_spending_creation_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteToGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('AC', 'ACCEPTED'), ('DN', 'DENIED'), ('NC', 'NOT CHECKED')], default='NC', max_length=2, verbose_name='Статус приглашения')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания приглашения')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_guest', to=settings.AUTH_USER_MODEL, verbose_name='Приглашенный')),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_inviter', to=settings.AUTH_USER_MODEL, verbose_name='Тот, кто приглашает')),
                ('to_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='В какую группу')),
            ],
            options={
                'db_table': 'invite_to_group',
            },
        ),
    ]