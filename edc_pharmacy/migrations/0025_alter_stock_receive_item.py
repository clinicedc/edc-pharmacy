# Generated by Django 5.1.2 on 2024-11-15 01:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0024_allocation_assignment_containerunits_dispense_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stock",
            name="receive_item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_pharmacy.receiveitem",
            ),
        ),
    ]
