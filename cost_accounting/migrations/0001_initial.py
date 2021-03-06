# Generated by Django 4.0.6 on 2022-07-12 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название категории')),
            ],
            options={
                'db_table': 'spending_category',
            },
        ),
        migrations.CreateModel(
            name='Spending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name='Потраченная сумма')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cost_accounting.category', verbose_name='Категория товара')),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Плательщик')),
            ],
            options={
                'db_table': 'spending',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название группы')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Участники группы')),
            ],
            options={
                'db_table': 'user_group',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cost_accounting.group', verbose_name='Трата на группу'),
        ),
    ]
