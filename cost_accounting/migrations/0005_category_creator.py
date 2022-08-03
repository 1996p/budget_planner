# Generated by Django 4.0.6 on 2022-07-17 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cost_accounting', '0004_alter_extendeduser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель категории'),
        ),
    ]
