# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-12 10:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edc_pharma', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispense',
            name='iv_duration',
        ),
    ]
