# Generated by Django 4.0.6 on 2022-08-21 15:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cost_accounting', '0008_invitetogroup'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='invitetogroup',
            unique_together={('guest', 'inviter')},
        ),
    ]
