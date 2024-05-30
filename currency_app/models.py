from django.db import models


class CurrencyRate(models.Model):
    currency = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    rate = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.currency}'


class CountryCurrency(models.Model):
    country = models.CharField(max_length=100)
    currency = models.CharField(max_length=200)
    currency_code = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f'{self.country}'
    
class ParamTable(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.name}'

class RelativeChange(models.Model):
    currency = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    change_percent = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.currency} - change percent'