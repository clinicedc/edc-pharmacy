# Generated by Django 5.1.2 on 2024-11-09 22:35

import _socket
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0036_remove_historicalrepackrequest_label_configuration_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="location",
            options={
                "default_manager_name": "objects",
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "verbose_name": "Location",
                "verbose_name_plural": "Locations",
            },
        ),
        migrations.AddField(
            model_name="location",
            name="created",
            field=models.DateTimeField(
                blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="device_created",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device created"),
        ),
        migrations.AddField(
            model_name="location",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device modified"),
        ),
        migrations.AddField(
            model_name="location",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
                verbose_name="Hostname created",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="hostname_modified",
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                blank=True,
                help_text="System field. (modified on every save)",
                max_length=50,
                verbose_name="Hostname modified",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="locale_created",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale created",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="locale_modified",
            field=models.CharField(
                blank=True,
                help_text="Auto-updated by Modeladmin",
                max_length=10,
                null=True,
                verbose_name="Locale modified",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="modified",
            field=models.DateTimeField(
                blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="revision",
            field=django_revision.revision_field.RevisionField(
                blank=True,
                editable=False,
                help_text="System field. Git repository tag:branch:commit.",
                max_length=75,
                null=True,
                verbose_name="Revision",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="user_created",
            field=django_audit_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="user_modified",
            field=django_audit_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
    ]
