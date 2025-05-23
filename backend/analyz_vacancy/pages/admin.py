from django.contrib import admin
from .models import (
    Page, Statistics, StatisticsTable, SalaryDynamics,
    VacancyDynamics, SalaryByCity, VacancyShareByCity, TopSkillsByYear, Vacancy, DemandStatisticsTable,
    DemandStatistics, GeoStatistics, GeoStatisticsTable, SkillStatisticsTable, SkillStatistics
)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class StatisticsTableInline(admin.TabularInline):
    model = StatisticsTable
    extra = 1


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [StatisticsTableInline]


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'area_name', 'salary_from', 'salary_to', 'salary_currency', 'published_at')
    list_filter = ('area_name', 'salary_currency', 'published_at')
    search_fields = ('name', 'area_name', 'key_skills')
    ordering = ('-published_at',)


class DemandStatisticsTableInline(admin.TabularInline):
    model = DemandStatisticsTable
    extra = 1


@admin.register(DemandStatistics)
class DemandStatisticsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [DemandStatisticsTableInline]


class GeoStatisticsTableInline(admin.TabularInline):
    model = GeoStatisticsTable
    extra = 1


@admin.register(GeoStatistics)
class GeoStatisticsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [GeoStatisticsTableInline]


class SkillStatisticsTableInline(admin.TabularInline):
    model = SkillStatisticsTable
    extra = 1


@admin.register(SkillStatistics)
class SkillStatisticsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [SkillStatisticsTableInline]

