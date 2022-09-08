# Generated by Django 3.2.13 on 2022-09-06 22:57

import uuid

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0011_auto_20220826_0406"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="rxrefill",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="historicalrxrefill",
            name="visit_code",
        ),
        migrations.RemoveField(
            model_name="historicalrxrefill",
            name="visit_code_sequence",
        ),
        migrations.RemoveField(
            model_name="rxrefill",
            name="visit_code",
        ),
        migrations.RemoveField(
            model_name="rxrefill",
            name="visit_code_sequence",
        ),
        migrations.RenameField(
            model_name="historicalrxrefill",
            old_name="refill_date",
            new_name="refill_start_datetime",
        ),
        migrations.RenameField(
            model_name="rxrefill",
            old_name="refill_date",
            new_name="refill_start_datetime",
        ),
    ]
