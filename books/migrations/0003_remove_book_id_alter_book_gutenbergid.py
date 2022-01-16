# Generated by Django 4.0.1 on 2022-01-16 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_rename_desc_book_description_book_downloaded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.AlterField(
            model_name='book',
            name='gutenbergID',
            field=models.IntegerField(default='-1', primary_key=True, serialize=False),
        ),
    ]
