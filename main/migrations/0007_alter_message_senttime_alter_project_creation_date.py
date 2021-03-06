# Generated by Django 4.0.2 on 2022-03-09 14:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_project_creation_date_message_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sentTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 9, 14, 33, 11, 970630), verbose_name='time sent'),
        ),
        migrations.AlterField(
            model_name='project',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 9, 14, 33, 11, 970630), verbose_name='date published'),
        ),
    ]
