# Generated by Django 2.2 on 2021-03-31 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='deadline',
            field=models.DateField(null=True, verbose_name='截止时间'),
        ),
    ]
