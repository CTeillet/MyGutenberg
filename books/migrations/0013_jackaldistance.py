# Generated by Django 4.0.1 on 2022-01-31 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_rename_blacklist_blacklistwords'),
    ]

    operations = [
        migrations.CreateModel(
            name='JackalDistance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.IntegerField(default=0)),
                ('idBook1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book1', to='books.book')),
                ('idBook2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book2', to='books.book')),
            ],
            options={
                'unique_together': {('idBook1', 'idBook2')},
            },
        ),
    ]
