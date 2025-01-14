import os
import django
import pandas as pd
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analyz_vacancy.settings')
django.setup()

from pages.models import Vacancy

web_dev_keywords = [
    'web develop', 'веб разработчик', 'web разработчик', 'web programmer',
    'web программист', 'веб программист', 'битрикс разработчик', 'bitrix разработчик',
    'drupal разработчик', 'cms разработчик', 'wordpress разработчик',
    'wp разработчик', 'joomla разработчик', 'drupal developer',
    'cms developer', 'wordpress developer', 'wp developer', 'joomla developer'
]

csv_data = "vacancies_2024.csv"
reader = pd.read_csv(csv_data)

for index, row in reader.iterrows():
    if any(keyword.lower() in row['name'].lower() for keyword in web_dev_keywords):
        published_at = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z')
        if not Vacancy.objects.filter(name=row['name'], published_at=published_at).exists():
            Vacancy.objects.create(
                name=row['name'],
                key_skills=row['key_skills'] if pd.notna(row['key_skills']) else '',
                salary_from=float(row['salary_from']) if pd.notna(row['salary_from']) else None,
                salary_to=float(row['salary_to']) if pd.notna(row['salary_to']) else None,
                salary_currency=row['salary_currency'] if pd.notna(row['salary_currency']) else None,
                area_name=row['area_name'],
                published_at=published_at,
            )
            print(f'Вакансия {row["name"]} успешно загружена.')
        break

print("Все вакансии успешно загружены")
