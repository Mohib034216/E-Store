# Generated by Django 4.1.1 on 2024-03-21 11:55

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_account_first_name_remove_account_last_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='addressbook',
            managers=[
                ('obj', django.db.models.manager.Manager()),
            ],
        ),
    ]
