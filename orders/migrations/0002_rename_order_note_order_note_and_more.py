# Generated by Django 4.1.1 on 2023-01-26 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_note',
            new_name='note',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='phone',
            new_name='phoneno',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='country',
            new_name='pin',
        ),
    ]