import pandas as pd
import numpy as np
import requests
from xml.etree import ElementTree as ET

def get_exchange_rates():
    url = "https://www.cbr-xml-daily.ru/daily_utf8.xml"
    response = requests.get(url)
    if response.status_code == 200:
        tree = ET.fromstring(response.content)
        exchange_rates = {"RUB": {"rate": 1.0}}
        date = tree.attrib.get('Date', 'Неизвестно')
        print(f"Дата обновления курсов: {date}")
        for currency in tree.findall(".//Valute"):
            char_code = currency.find("CharCode").text
            rate = float(currency.find("Value").text.replace(",", "."))
            nominal = int(currency.find("Nominal").text)
            exchange_rates[char_code] = {"rate": rate / nominal}
        return exchange_rates


file_path = '../statistics/vacancies_2024.csv'
data = pd.read_csv(file_path, low_memory=False)
data['published_at'] = pd.to_datetime(data['published_at'], errors='coerce', utc=True)
data = data.dropna(subset=['published_at'])
data['year'] = data['published_at'].dt.year
exchange_rates = get_exchange_rates()


def convert_to_rub(row, exchange_rates):
    if pd.notnull(row['salary_from']) or pd.notnull(row['salary_to']):
        avg_salary = np.nanmean([row['salary_from'], row['salary_to']])
        currency = row['salary_currency']
        if currency in exchange_rates:
            return avg_salary * exchange_rates[currency]['rate']
    return np.nan


filtered_data = data[(data['salary_from'] <= 10_000_000) & (data['salary_to'] <= 10_000_000)]
filtered_data['salary_rub'] = filtered_data.apply(lambda row: convert_to_rub(row, exchange_rates), axis=1)
salary_trend = filtered_data.groupby('year')['salary_rub'].mean().reset_index()
salary_trend['year'] = salary_trend['year'].astype(int)
file_path_output = 'salary_by_year.txt'

with open(file_path_output, 'w') as f:
    for index, row in salary_trend.iterrows():
        f.write(f"Год: {row['year']}, Средняя зарплата: {row['salary_rub']:.2f} руб\n")

print(f"Данные сохранены в файл {file_path_output}")
