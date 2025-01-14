from django.contrib import admin
from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'area_name', 'salary_from', 'salary_to', 'salary_currency', 'published_at')
    list_filter = ('area_name', 'salary_currency', 'published_at')
    search_fields = ('name', 'area_name', 'key_skills')
    ordering = ('-published_at',)
