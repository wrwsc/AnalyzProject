from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="HTML-контент")

    def __str__(self):
        return self.title


class Statistics(models.Model):
    title = models.CharField(max_length = 255, verbose_name = "Заголовок статистики")
    description = models.TextField(verbose_name = "Описание статистики")
    image = models.ImageField(upload_to = 'images/', verbose_name = "Изображение статистики", blank = True, null = True)

    def __str__(self):
        return self.title


class StatisticsTable(models.Model):
    statistics = models.ForeignKey(Statistics, on_delete = models.CASCADE, related_name = 'tables',
                                   verbose_name = "Общая статистика")
    name = models.CharField(max_length = 255, verbose_name = "Название таблицы")
    table = models.TextField(verbose_name = "Данные таблицы")
    image = models.ImageField(upload_to = 'images/', verbose_name = "Изображение таблицы", blank = True, null = True)

    def __str__(self):
        return self.name


class SalaryDynamics(models.Model):
    statistics = models.ForeignKey(Statistics, on_delete = models.CASCADE, related_name = 'salary_dynamics',
                                   verbose_name = "Общая статистика")
    year = models.IntegerField(verbose_name = "Год")
    average_salary = models.FloatField(verbose_name = "Средняя зарплата в рублях")
    currency = models.CharField(max_length = 3, verbose_name = "Валюта", blank = True, null = True)
    currency_exchange_rate = models.FloatField(verbose_name = "Курс валюты", blank = True, null = True)

    def __str__(self):
        return f"Динамика зарплат {self.year}"


class VacancyDynamics(models.Model):
    statistics = models.ForeignKey(Statistics, on_delete = models.CASCADE, related_name = 'vacancy_dynamics',
                                   verbose_name = "Общая статистика")
    year = models.IntegerField(verbose_name = "Год")
    vacancy_count = models.IntegerField(verbose_name = "Количество вакансий")

    def __str__(self):
        return f"Динамика вакансий {self.year}"


class SalaryByCity(models.Model):
    statistics = models.ForeignKey(Statistics, on_delete = models.CASCADE, related_name = 'salary_by_city',
                                   verbose_name = "Общая статистика")
    city = models.CharField(max_length = 255, verbose_name = "Город")
    average_salary = models.FloatField(verbose_name = "Средняя зарплата в рублях")

    def __str__(self):
        return f"Зарплата в {self.city}"


class VacancyShareByCity(models.Model):
    statistics = models.ForeignKey(Statistics, on_delete = models.CASCADE, related_name = 'vacancy_share_by_city',
                                   verbose_name = "Общая статистика")
    city = models.CharField(max_length = 255, verbose_name = "Город")
    vacancy_share = models.FloatField(verbose_name = "Доля вакансий")

    def __str__(self):
        return f"Доля вакансий в {self.city}"


class TopSkillsByYear(models.Model):
    statistics = models.ForeignKey(Statistics, on_delete = models.CASCADE, related_name = 'top_skills_by_year',
                                   verbose_name = "Общая статистика")
    year = models.IntegerField(verbose_name = "Год")
    skill_name = models.CharField(max_length = 255, verbose_name = "Название навыка")
    frequency = models.IntegerField(verbose_name = "Частота появления навыка")

    def __str__(self):
        return f"Топ-20 навыков {self.year}"


class Vacancy(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название вакансии")
    key_skills = models.TextField(blank=True, verbose_name="Ключевые навыки")
    salary_from = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Зарплата от")
    salary_to = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Зарплата до")
    salary_currency = models.CharField(max_length=10, blank=True, null=True, verbose_name="Валюта")
    area_name = models.CharField(max_length=255, verbose_name="Регион")
    published_at = models.DateTimeField(verbose_name="Дата публикации")

    def __str__(self):
        return self.name
