# Generated by Django 6.0 on 2025-03-01 12:29

import _socket
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import edc_pharmacy.models.scan_duplicates
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "edc_pharmacy",
            "0056_rename_manufacture_date_historicallot_manufactured_date_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="ScanDuplicates",
            fields=[
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "user_created",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                        verbose_name="Hostname created",
                    ),
                ),
                (
                    "hostname_modified",
                    django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                        verbose_name="Hostname modified",
                    ),
                ),
                (
                    "device_created",
                    models.CharField(blank=True, max_length=10, verbose_name="Device created"),
                ),
                (
                    "device_modified",
                    models.CharField(
                        blank=True, max_length=10, verbose_name="Device modified"
                    ),
                ),
                (
                    "locale_created",
                    models.CharField(
                        blank=True,
                        help_text="Auto-updated by Modeladmin",
                        max_length=10,
                        null=True,
                        verbose_name="Locale created",
                    ),
                ),
                (
                    "locale_modified",
                    models.CharField(
                        blank=True,
                        help_text="Auto-updated by Modeladmin",
                        max_length=10,
                        null=True,
                        verbose_name="Locale modified",
                    ),
                ),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("identifier", models.CharField(max_length=36, unique=True)),
            ],
            options={
                "verbose_name": "Scan Duplicates",
                "verbose_name_plural": "Scan Duplicates",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "default_manager_name": "objects",
                "indexes": [
                    models.Index(
                        fields=["modified", "created"], name="edc_pharmac_modifie_a4e353_idx"
                    ),
                    models.Index(
                        fields=["user_modified", "user_created"],
                        name="edc_pharmac_user_mo_42b210_idx",
                    ),
                ],
            },
            managers=[
                ("objects", edc_pharmacy.models.scan_duplicates.Manager()),
            ],
        ),
    ]
