# Generated by Django 2.2.5 on 2019-12-22 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manuals', '0007_auto_20191222_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manual',
            name='last_update',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Last Update'),
        ),
    ]
