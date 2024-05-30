import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from django.shortcuts import render, redirect
from currency_app.models import CurrencyRate, RelativeChange, ParamTable, CountryCurrency

import plotly.graph_objs as go
import plotly.io as pio


def main_page(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        try:
            read_and_sync_rates(start_date, end_date)
        except Exception as e:
            return render(request, 'currency_app/main_page.html', {'error': str(e)})
        return redirect('currencys_page')
    return render(request, 'currency_app/main_page.html')

def read_and_sync_rates(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Некорректный формат даты")

    currency_id = {
        "dollar": 52148,
        "euro": 52170,
        "pounds": 52146,
        "yen": 52246,
        "lira": 52158,
        "rupee": 52238,
        "CNY": 52207
    }
    
    for currency_name, id in currency_id.items():
        url = f'https://www.finmarket.ru/currency/rates/?id=10148&pv=1&cur={id}&bd={start_date.day}&bm={start_date.month}&by={start_date.year}&ed={end_date.day}&em={end_date.month}&ey={end_date.year}&x=48&y=13#archive'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Не удалось получить данные для {currency_name}")

        soup = bs(response.content, 'html.parser')
        table = soup.find('table', class_="karramba")
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    date = datetime.strptime(cells[0].get_text().strip(), '%d.%m.%Y').date()
                    rate = cells[2].get_text().strip().replace(',', '.')
                    try:
                        rate = float(rate)
                    except ValueError:
                        continue
                    
                    currency_rate, created = CurrencyRate.objects.get_or_create(
                        currency=currency_name,
                        date=date,
                        defaults={'rate': rate}
                    )
                    if not created and currency_rate.rate != rate:
                        currency_rate.rate = rate
                        currency_rate.save()


def read_and_sync_country_currencys():
    url = 'https://www.iban.ru/currency-codes'
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    table = soup.find('table', class_="table table-bordered downloads tablesorter")
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 4:
                CountryCurrency.objects.update_or_create(
                    country = cells[0].get_text().strip(),
                    currency = cells[1].get_text().strip(),
                    currency_code = cells[2].get_text().strip(),
                )


def country_currencys_page(request):
    read_and_sync_country_currencys()
    post = CountryCurrency.objects.all()
    return render(request, "currency_app/country_currencys_page.html", {'post':post})


def currencys_page(request):
    if request.method == 'POST':
        countries = request.POST.getlist('countries')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        try:
            read_and_sync_rates(start_date, end_date)
            calculate_relative_changes()
        except Exception as e:
            return render(request, 'currency_app/relative_changes_graph_form_page.html', {'error': str(e)})

        country_currencies_dic = {
            "Austria": 'euro',
            "Greece": 'euro',
            "Italy": 'euro',
            "Spain": 'euro',
            "USA": 'dollar',
            "Salvador": 'dollar',
            "Bonaire": 'dollar',
            "Haiti": 'dollar',
            "Monaco": 'euro',
            "Germany": 'euro',
            "China": 'CNY',
            "Malvinas Islands": 'pounds',
            "Japan": 'yen',
            "Turkey": 'lira',
            "India": 'rupee'
        }

        relative_changes_data = {}
        for country in countries:
            currency = country_currencies_dic.get(country)
            if currency:
                relative_changes = RelativeChange.objects.filter(currency=currency, date__range=[start_date, end_date]).values('date', 'change_percent')
                relative_changes_data[country] = list(relative_changes)

        graph_data = relative_changes_graph(relative_changes_data)
        return render(request, 'currency_app/relative_changes_graph_page.html', {'graph_data': graph_data})
    
    return render(request, 'currency_app/currencys_page.html')


def currency_rates(request, currency):
    rates = CurrencyRate.objects.filter(currency=currency).all()
    return render(request, 'currency_app/currency_rates_page.html', {'currency': currency, 'rates': rates})


def calculate_relative_changes():
    base_date_param, created = ParamTable.objects.get_or_create(name='base_date')
    if created:
        base_date_param.value = '2023-02-01'
        base_date_param.save()
    base_rate_dic = {
        "dollar": 70.5174,
        "euro": 76.3004,
        "pounds": 87.2935,
        "yen": 54.0736,
        "lira": 37.5001,
        "rupee": 8.64163,
        "CNY": 10.4259
    }
    for rate in CurrencyRate.objects.all():
        base_rate = base_rate_dic[rate.currency]
        actual_rate = float((rate.rate).replace(',', '.'))
        change_percent = ( actual_rate - base_rate) / base_rate * 100
        existing_record, created = RelativeChange.objects.get_or_create(
            currency=rate.currency,
            date=rate.date,
            defaults={'change_percent': change_percent}
        )
        if not created and existing_record.change_percent != change_percent:
            existing_record.change_percent = change_percent
            existing_record.save()

def show_relative_changes(request, currency):
    calculate_relative_changes()
    relative_changes = RelativeChange.objects.filter(currency=currency).all()
    return render(request, 'currency_app/relative_changes_page.html', {'relative_changes': relative_changes, 'currency': currency})



def relative_changes_graph(relative_changes_data):
    traces = []
    for country, data in relative_changes_data.items():
        x_values = [entry['date'] for entry in data]
        y_values = [entry['change_percent'] for entry in data]
        traces.append(go.Scatter(x=x_values, y=y_values, mode='lines', name=country))
    layout = go.Layout(
        title='Относительные изменения курсов валют',
        xaxis=dict(title='Дата'),
        yaxis=dict(title='Относительное изменение курса (%)')
    )
    fig = go.Figure(data=traces, layout=layout)
    graph_data = pio.to_html(fig, full_html=False)
    return graph_data
