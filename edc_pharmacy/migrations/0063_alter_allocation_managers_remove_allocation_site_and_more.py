# Generated by Django 6.0 on 2025-03-12 14:01

import edc_pharmacy.models.stock.allocation
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0062_auto_20250312_1433"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="allocation",
            managers=[
                ("objects", edc_pharmacy.models.stock.allocation.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name="allocation",
            name="site",
        ),
        migrations.RemoveField(
            model_name="historicalallocation",
            name="site",
        ),
    ]
