# Generated by Django 4.1.1 on 2024-01-17 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_addess_type_addressbook_address_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressbook',
            name='first_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='addressbook',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
