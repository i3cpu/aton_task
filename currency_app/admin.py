from django.contrib import admin
from currency_app.models import CurrencyRate, CountryCurrency, ParamTable, RelativeChange

admin.site.register(CurrencyRate)
admin.site.register(CountryCurrency)
admin.site.register(ParamTable)
admin.site.register(RelativeChange)

