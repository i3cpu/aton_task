# Generated by Django 5.0.6 on 2024-05-29 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_app', '0002_alter_countrycurrency_currency_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyrate',
            name='rate',
            field=models.CharField(max_length=200),
        ),
    ]
