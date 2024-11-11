# Generated by Django 5.1.2 on 2024-11-11 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0046_historicalstockrequest_subject_identifiers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalstockrequest",
            name="excluded_subject_identifiers",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="Exclude these subjects from this request. (Usually left blank)",
            ),
        ),
        migrations.AddField(
            model_name="stockrequest",
            name="excluded_subject_identifiers",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="Exclude these subjects from this request. (Usually left blank)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstockrequest",
            name="subject_identifiers",
            field=models.TextField(
                blank=True,
                help_text="By adding subject identifiers in this box, only these subjects will be included in the request. All others will be ignored.",
                null=True,
                verbose_name="Include ONLY these subjects in this request. (Usually left blank)",
            ),
        ),
        migrations.AlterField(
            model_name="stockrequest",
            name="subject_identifiers",
            field=models.TextField(
                blank=True,
                help_text="By adding subject identifiers in this box, only these subjects will be included in the request. All others will be ignored.",
                null=True,
                verbose_name="Include ONLY these subjects in this request. (Usually left blank)",
            ),
        ),
    ]
