# Generated by Django 4.0.6 on 2022-08-05 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cost_accounting', '0005_category_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='spending',
            name='short_description',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Краткое описание'),
        ),
    ]
