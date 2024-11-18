# Generated by Django 5.1.2 on 2024-11-16 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0031_historicalrepackrequest_task_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalstockrequest",
            name="task_id",
            field=models.UUIDField(null=True),
        ),
        migrations.AddField(
            model_name="stockrequest",
            name="task_id",
            field=models.UUIDField(null=True),
        ),
    ]
