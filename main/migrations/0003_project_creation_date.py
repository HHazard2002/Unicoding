# Generated by Django 4.0.2 on 2022-03-08 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_project_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 8, 18, 44, 42, 142943), verbose_name='date published'),
        ),
    ]
