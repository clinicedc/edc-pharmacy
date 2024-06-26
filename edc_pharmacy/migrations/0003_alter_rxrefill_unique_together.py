# Generated by Django 3.2.11 on 2022-04-12 20:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("edc_pharmacy", "0002_alter_medication_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="rxrefill",
            unique_together={
                ("rx", "refill_date"),
                ("rx", "visit_code", "visit_code_sequence"),
            },
        ),
    ]
