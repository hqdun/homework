# Generated by Django 2.2 on 2021-03-31 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20200714_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='django', max_length=50, verbose_name='标签'),
        ),
    ]
