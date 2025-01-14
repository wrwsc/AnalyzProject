from django.db import models


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

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
