# Generated by Django 2.2 on 2021-03-31 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_homework_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='deadline',
            field=models.DateTimeField(null=True, verbose_name='截止时间'),
        ),
    ]
