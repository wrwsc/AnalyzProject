import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import requests
from xml.etree import ElementTree as ET
from datetime import datetime
from multiprocessing import Pool, cpu_count

exchange_rate_cache = {}


def get_exchange_rates(date):
    formatted_date = date.strftime("%d/%m/%Y")
    if formatted_date in exchange_rate_cache:
        return exchange_rate_cache[formatted_date]
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={formatted_date}"
    response = requests.get(url)
    exchange_rates = {"RUB":{"rate":1.0}}
    if response.status_code == 200:
        tree = ET.fromstring(response.content)
        for currency in tree.findall(".//Valute"):
            char_code = currency.find("CharCode").text
            rate = float(currency.find("Value").text.replace(",", "."))
            nominal = int(currency.find("Nominal").text)
            exchange_rates[char_code] = {"rate": rate / nominal}
    exchange_rate_cache[formatted_date] = exchange_rates
    return exchange_rates


def convert_to_rub(row, exchange_rates):
    if pd.notnull(row['salary_from']) or pd.notnull(row['salary_to']):
        avg_salary = np.nanmean([row['salary_from'], row['salary_to']])
        currency = row['salary_currency']
        if currency in exchange_rates:
            return avg_salary * exchange_rates[currency]['rate']
    return np.nan


def process_chunk(chunk):
    chunk['published_at'] = pd.to_datetime(chunk['published_at'], errors = 'coerce', utc = True)
    chunk['year'] = chunk['published_at'].dt.year
    chunk['salary_rub'] = np.nan
    chunk['area_salary_rub'] = np.nan
    for date, sub_chunk in chunk.groupby(chunk['published_at'].dt.to_period('M')):
        rates = get_exchange_rates(date.to_timestamp())
        chunk.loc[sub_chunk.index, 'salary_rub'] = sub_chunk.apply(lambda row:convert_to_rub(row, rates), axis = 1)
        for area, area_chunk in sub_chunk.groupby('area_name'):
            area_rate = area_chunk.apply(lambda row:convert_to_rub(row, rates), axis = 1)
            chunk.loc[area_chunk.index, 'area_salary_rub'] = area_rate
    chunk = chunk[(chunk['salary_rub'] > 0) & (chunk['salary_rub'] <= 10_000_000)]
    chunk = chunk[(chunk['area_salary_rub'] > 0) & (chunk['area_salary_rub'] <= 10_000_000)]
    return chunk


def process_chunks_in_parallel(file_path, chunksize):
    pool = Pool(cpu_count())
    chunk_list = []
    for chunk in pd.read_csv(file_path, chunksize = chunksize, low_memory = False):
        chunk_list.append(pool.apply_async(process_chunk, args = (chunk,)))
    pool.close()
    pool.join()
    processed_chunks = [res.get() for res in chunk_list]
    return pd.concat(processed_chunks)


def main():
    file_path = '../statistics/vacancies_2024.csv'
    chunksize = 100000
    data = process_chunks_in_parallel(file_path, chunksize)
    salary_trend = data.groupby('year')['salary_rub'].mean().reset_index()
    salary_trend['salary_rub'] = salary_trend['salary_rub'].round().astype(int)
    print(salary_trend)
    plt.figure(figsize = (10, 6))
    plt.bar(salary_trend['year'], salary_trend['salary_rub'])
    plt.title('Динамика уровня зарплат по годам')
    plt.xlabel('Год')
    plt.ylabel('Средняя зарплата (руб)')
    plt.ylim(0, 220_000)
    plt.savefig('salary_trend.png')
    plt.close()
    vacancy_count_trend = data.groupby('year').size().reset_index(name = 'vacancy_count')
    print(vacancy_count_trend)
    plt.figure(figsize = (10, 6))
    plt.bar(vacancy_count_trend['year'], vacancy_count_trend['vacancy_count'])
    plt.title('Динамика количества вакансий по годам')
    plt.xlabel('Год')
    plt.ylabel('Количество вакансий')
    plt.savefig('vacancy_count_trend.png')
    plt.close()
    area_salary_trend = data.groupby('area_name')['area_salary_rub'].mean().reset_index()
    area_salary_trend = area_salary_trend.sort_values(by = 'area_salary_rub', ascending = False)
    area_salary_trend['area_salary_rub'] = area_salary_trend['area_salary_rub'].round().astype(int)
    top_10_area_salary = area_salary_trend.head(10)
    print(top_10_area_salary)
    average_salary_top_10 = top_10_area_salary['area_salary_rub'].mean()
    plt.figure(figsize = (12, 8))
    plt.barh(top_10_area_salary['area_name'], top_10_area_salary['area_salary_rub'])
    plt.title('Топ 10 городов по уровню зарплат')
    plt.xlabel('Средняя зарплата (руб)')
    plt.ylabel('Город')
    plt.savefig('top_10_area_salary.png')
    plt.close()


if __name__ == '__main__':
    main()