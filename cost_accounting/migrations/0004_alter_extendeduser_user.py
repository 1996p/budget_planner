# Generated by Django 4.0.6 on 2022-07-13 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cost_accounting', '0003_alter_extendeduser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
