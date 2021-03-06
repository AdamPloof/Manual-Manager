# Generated by Django 2.2.5 on 2019-12-22 03:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manuals', '0006_auto_20191128_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='manual',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='manual',
            name='last_update_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='manual',
            name='next_update',
            field=models.DateTimeField(null=True, verbose_name='Next Update Due'),
        ),
        migrations.AddField(
            model_name='manual',
            name='update_assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='manual',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='manual',
            name='is_archived',
            field=models.BooleanField(default=False, verbose_name='Archived'),
        ),
    ]
