# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-13 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_pharma', '0007_auto_20160913_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispense',
            name='number_of_tablets',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='dispense',
            name='number_of_teaspoons',
            field=models.IntegerField(blank=True),
        ),
    ]
