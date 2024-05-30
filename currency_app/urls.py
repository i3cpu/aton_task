from django.urls import path
from currency_app import views

urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('currencys', views.currencys_page, name="currencys_page"),
    path('currency_rates/<str:currency>', views.currency_rates, name="currency_rates"),
    path('relative_changes/<str:currency>', views.show_relative_changes, name="show_relative_changes"),
    path('country_currencys', views.country_currencys_page, name="country_currencys_page"),


]
