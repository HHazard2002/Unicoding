# Generated by Django 4.0.2 on 2022-03-16 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_message_senttime_alter_project_creation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='developer',
        ),
    ]
