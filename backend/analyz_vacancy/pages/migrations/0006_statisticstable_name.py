# Generated by Django 5.1.4 on 2025-01-14 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_remove_statisticstable_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='statisticstable',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Название таблицы'),
        ),
    ]
