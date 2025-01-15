import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import requests
from xml.etree import ElementTree as ET
from datetime import datetime
from multiprocessing import Pool, cpu_count


countries = [
    "Россия", "Украина", "Казахстан", "Беларусь", "Грузия", "Армения", "Азербайджан", "Узбекистан", "Таджикистан",
    "Кыргызстан", "Туркменистан", "Молдова", "Латвия", "Литва", "Эстония", "Польша", "Чехия", "Словакия", "Венгрия",
    "Румыния", "Болгария", "Сербия", "Хорватия", "Словения", "Босния и Герцеговина", "Черногория", "Северная Македония",
    "Албания", "Греция", "Турция", "Кипр", "Израиль", "Ливан", "Сирия", "Иордания", "Ирак", "Иран", "Саудовская Аравия",
    "ОАЭ", "Катар", "Бахрейн", "Кувейт", "Оман", "Йемен", "Египет", "Ливия", "Тунис", "Алжир", "Марокко",
    "Западная Сахара",
    "Мавритания", "Мали", "Нигер", "Чад", "Судан", "Южный Судан", "Эритрея", "Джибути", "Сомали", "Эфиопия", "Кения",
    "Уганда", "Руанда", "Бурунди", "Танзания", "Сейшелы", "Мадагаскар", "Маврикий", "Коморы", "Мозамбик", "Замбия",
    "Зимбабве",
    "Ботсвана", "ЮАР", "Лесото", "Свазиленд", "Намибия", "Ангола", "Конго", "Демократическая Республика Конго", "Габон",
    "Экваториальная Гвинея", "Сан-Томе и Принсипи", "Камерун", "Центральноафриканская Республика", "Нигерия", "Гана",
    "Кот-д'Ивуар", "Буркина-Фасо", "Того", "Бенин", "Сьерра-Леоне", "Либерия", "Гвинея", "Гвинея-Бисау", "Сенегал",
    "Гамбия",
    "Кабо-Верде", "Мексика", "Гватемала", "Белиз", "Сальвадор", "Гондурас", "Никарагуа", "Коста-Рика", "Панама", "Куба",
    "Гаити", "Доминиканская Республика", "Ямайка", "Тринидад и Тобаго", "Багамы", "Барбадос", "Сент-Люсия", "Гренада",
    "Сент-Винсент и Гренадины", "Антигуа и Барбуда", "Доминика", "Сент-Китс и Невис", "Канада", "США", "Гренландия",
    "Бермуды", "Бразилия", "Аргентина", "Уругвай", "Парагвай", "Чили", "Боливия", "Перу", "Эквадор", "Колумбия",
    "Венесуэла",
    "Гайана", "Суринам", "Французская Гвиана", "Австралия", "Новая Зеландия", "Папуа - Новая Гвинея", "Фиджи",
    "Соломоновы Острова",
    "Вануату", "Новая Каледония", "Французская Полинезия", "Самоа", "Тонга", "Кирибати", "Тувалу", "Науру",
    "Маршалловы Острова",
    "Палау", "Филиппины", "Малайзия", "Сингапур", "Индонезия", "Вьетнам", "Таиланд", "Мьянма", "Камбоджа", "Лаос",
    "Бруней",
    "Тимор-Лесте", "Китай", "Монголия", "Северная Корея", "Южная Корея", "Япония", "Индия", "Пакистан", "Бангладеш",
    "Шри-Ланка",
    "Непал", "Бутан", "Мальдивы", "Россия", "Украина", "Германия", "Франция", "Италия", "Испания", "Великобритания",
    "Нидерланды",
    "Бельгия", "Люксембург", "Швейцария", "Австрия", "Португалия", "Швеция", "Норвегия", "Дания", "Финляндия",
    "Исландия",
    "Ирландия", "Эстония", "Латвия", "Литва", "Польша", "Чехия", "Словакия", "Венгрия", "Румыния", "Болгария", "Сербия",
    "Хорватия", "Босния и Герцеговина", "Словения", "Черногория", "Северная Македония", "Албания", "Греция", "Турция",
    "Кипр",
    "Израиль", "Ливан", "Сирия", "Иордания", "Ирак", "Иран", "Саудовская Аравия", "ОАЭ", "Катар", "Бахрейн", "Кувейт",
    "Оман",
    "Йемен", "Египет", "Ливия", "Тунис", "Алжир", "Марокко"
]

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
            exchange_rates[char_code] = {"rate":rate / nominal}
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
    file_path = '../statistics/filtered_vacancies.csv'
    chunksize = 100000
    data = process_chunks_in_parallel(file_path, chunksize)
    data = data[~data['area_name'].isin(countries)]
    area_salary_trend = data.groupby('area_name')['area_salary_rub'].mean().reset_index()
    area_salary_trend = area_salary_trend.sort_values(by = 'area_salary_rub', ascending = False)
    area_salary_trend['area_salary_rub'] = area_salary_trend['area_salary_rub'].round().astype(int)
    top_10_area_salary = area_salary_trend.head(10)
    print(top_10_area_salary)
    plt.figure(figsize = (12, 10))
    plt.barh(top_10_area_salary['area_name'], top_10_area_salary['area_salary_rub'])
    plt.title('Топ 10 городов по уровню зарплат')
    plt.xlabel('Средняя зарплата (руб)')
    plt.ylabel('Город')
    plt.savefig('top_10_area_salary.png')
    plt.close()
    vacancy_count_by_city = data['area_name'].fillna('Неизвестно').value_counts().head(10).reset_index()
    vacancy_count_by_city.columns = ['area_name', 'vacancy_count']
    vacancy_count_by_city['vacancy_share'] = vacancy_count_by_city['vacancy_count'] / vacancy_count_by_city[
        'vacancy_count'].sum() * 100
    for index, row in vacancy_count_by_city.iterrows():
        print(f"Город: {row['area_name']}, Доля вакансий: {row['vacancy_share']:.2f}%")
    plt.figure(figsize = (12, 8))
    plt.barh(vacancy_count_by_city['area_name'], vacancy_count_by_city['vacancy_share'])
    plt.title('Доля вакансий по городам')
    plt.xlabel('Доля вакансий (%)')
    plt.ylabel('Город')
    plt.gca().invert_yaxis()
    plt.xlim(0, 70)
    plt.savefig('vacancy_share_by_city.png')
    plt.close()


if __name__ == '__main__':
    main()
