# Generated by Django 5.1.4 on 2025-01-14 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_statisticstable_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statisticstable',
            name='name',
        ),
    ]
