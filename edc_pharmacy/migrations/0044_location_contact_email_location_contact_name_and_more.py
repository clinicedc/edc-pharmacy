# Generated by Django 5.1.2 on 2024-11-19 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0043_stockproxy_alter_historicallot_lot_no_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="contact_email",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="location",
            name="contact_name",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="location",
            name="contact_tel",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
