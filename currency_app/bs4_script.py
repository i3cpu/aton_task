import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime


# def get_actual_rate(currency, start_date, end_date):

#     start_date = datetime.strptime(start_date, '%Y-%m-%d')
#     end_date = datetime.strptime(end_date, '%Y-%m-%d')
#     currency_id = { 
#         "dollar" : 52148,
#         "evro": 52170,
#         "pounds": 52146,
#         "yen": 52246,
#         "lira": 52158,
#         "rupee": 52238,
#         "CNY":52207
#     }
#     if currency in currency_id:
#         url = f'https://www.finmarket.ru/currency/rates/?id=10148&pv=1&cur={currency_id[currency]}&bd={start_date.day}&bm={start_date.month}&by={start_date.year}&ed={end_date.day}&em={end_date.month}&ey={end_date.year}&x=48&y=13#archive'

#         response = requests.get(url)
#         soup = bs(response.content, 'html.parser')
#         table = soup.find('table', class_="karramba")
#         if table:
#             rows = table.find_all('tr')
#             data = {
#                 'date':end_date,
#                 'rate':rows[-1].find_all('td')[2].get_text().strip()

#             }
            
#     return data

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
                
                cells[0].get_text().strip()

    print(cells)

read_and_sync_country_currencys()
