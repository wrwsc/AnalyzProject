import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
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


filtered_data = data[(data['salary_from'] <= 10_000_000) & (data['salary_to'] <= 10_000_000)].copy()
filtered_data['salary_rub'] = filtered_data.apply(convert_to_rub, axis=1)
filtered_data.dropna(subset=['salary_rub'], inplace=True)
# city_salary = filtered_data.groupby('area_name')['salary_rub'].mean().reset_index()
# city_salary = city_salary.sort_values(by='salary_rub', ascending=False).head(10)
# plt.figure(figsize=(12, 8))
# plt.barh(city_salary['area_name'], city_salary['salary_rub'])
# plt.title('Уровень зарплат по городам')
# plt.xlabel('Средняя зарплата (руб)')
# plt.ylabel('Город')
# plt.ticklabel_format(axis='x', style='plain')
# plt.gca().invert_yaxis()
# plt.savefig('city_salary.png')
# plt.close()


# salary_trend = filtered_data.groupby('year')['salary_rub'].mean().reset_index()
# print(salary_trend)
# plt.figure(figsize=(10, 6))
# plt.bar(salary_trend['year'], salary_trend['salary_rub'])
# plt.title('Динамика уровня зарплат по годам')
# plt.xlabel('Год')
# plt.ylabel('Средняя зарплата (руб)')
# plt.ylim(0, 400_000)
# plt.savefig('salary_trend.png')
# plt.close()


# vacancy_count_by_city = data['area_name'].fillna('Неизвестно').value_counts().head(10).reset_index()
# vacancy_count_by_city.columns = ['area_name', 'vacancy_count']
# vacancy_count_by_city['vacancy_share'] = vacancy_count_by_city['vacancy_count'] / vacancy_count_by_city['vacancy_count'].sum() * 100
#
# plt.figure(figsize=(12, 8))
# plt.barh(vacancy_count_by_city['area_name'], vacancy_count_by_city['vacancy_share'])
# plt.title('Доля вакансий по городам')
# plt.xlabel('Доля вакансий (%)')
# plt.ylabel('Город')
# plt.gca().invert_yaxis()
# plt.xlim(0, 70)
# plt.savefig('vacancy_share_by_city.png')
# plt.close()
#
# vacancy_trend = data.groupby('year').size().reset_index(name='vacancy_count')
# plt.figure(figsize=(10, 6))
# plt.bar(vacancy_trend['year'], vacancy_trend['vacancy_count'])
# plt.title('Динамика количества вакансий по годам')
# plt.xlabel('Год')
# plt.ylabel('Количество вакансий')
# plt.savefig('vacancy_trend.png')
# plt.close()
# skills_separated = data['key_skills'].str.split('\n', expand=True).stack().reset_index(drop=True)
# skills_separated = skills_separated.str.strip()
# skills_separated = skills_separated[skills_separated != '']
# skills_count = skills_separated.value_counts().reset_index()
# skills_count.columns = ['key_skills', 'skill_count']
# skills_count_sorted = skills_count.sort_values(by='skill_count', ascending=False)
# top_20_skills = skills_count_sorted.head(20)
# print(top_20_skills)
#
# plt.figure(figsize=(10, 8))
# plt.pie(
#     top_20_skills['skill_count'],
#     labels=top_20_skills['key_skills'],
#     autopct='%1.1f%%',
#     startangle=140,
#     textprops={'fontsize': 10}
# )
# plt.title('ТОП-20 навыков по годам')
# plt.tight_layout()
# plt.savefig('top_20_skills.png')
# plt.close()

