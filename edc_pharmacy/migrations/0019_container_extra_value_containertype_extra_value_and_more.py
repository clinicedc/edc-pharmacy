# Generated by Django 4.2.3 on 2023-08-02 23:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_pharmacy", "0018_alter_rxrefill_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="extra_value",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="containertype",
            name="extra_value",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="formulationtype",
            name="extra_value",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="frequencyunits",
            name="extra_value",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="route",
            name="extra_value",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="units",
            name="extra_value",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="unittype",
            name="extra_value",
            field=models.CharField(max_length=250, null=True),
        ),
    ]
