# Generated by Django 5.0.6 on 2024-05-29 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrycurrency',
            name='currency_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='currencyrate',
            name='date',
            field=models.CharField(max_length=200),
        ),
    ]
