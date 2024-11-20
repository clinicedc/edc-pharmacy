# Generated by Django 5.1.2 on 2024-11-19 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0046_remove_historicalrx_slug_remove_rx_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalstockrequest",
            name="cancel",
            field=models.CharField(
                default=None,
                max_length=6,
                null=True,
                verbose_name="To cancel this request, type the word 'CANCEL' here and save the form:",
            ),
        ),
        migrations.AddField(
            model_name="stockrequest",
            name="cancel",
            field=models.CharField(
                default=None,
                max_length=6,
                null=True,
                verbose_name="To cancel this request, type the word 'CANCEL' here and save the form:",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstockrequest",
            name="status",
            field=models.CharField(
                choices=[("open", "Open"), ("closed", "Closed"), ("cancelled", "Cancelled")],
                default="open",
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name="stockrequest",
            name="status",
            field=models.CharField(
                choices=[("open", "Open"), ("closed", "Closed"), ("cancelled", "Cancelled")],
                default="open",
                max_length=25,
            ),
        ),
    ]
