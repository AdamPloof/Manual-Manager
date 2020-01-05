# Generated by Django 2.2.5 on 2020-01-03 22:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manuals', '0014_auto_20200103_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manual',
            name='admin',
        ),
        migrations.AddField(
            model_name='manual',
            name='admin',
            field=models.ManyToManyField(related_name='admin_of', to=settings.AUTH_USER_MODEL),
        ),
    ]
