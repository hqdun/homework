# Generated by Django 2.2 on 2021-03-31 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_auto_20210331_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='deadline',
            field=models.DateField(null=True, verbose_name='截止时间'),
        ),
    ]