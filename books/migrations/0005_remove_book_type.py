# Generated by Django 4.0.1 on 2022-01-16 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_book_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='type',
        ),
    ]
