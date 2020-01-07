# Generated by Django 2.2.9 on 2020-01-07 20:07

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models

import django_auth_adfs_db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ADFSConfig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "enabled",
                    models.BooleanField(
                        default=False,
                        help_text="Master switch if ADFS login/SSO is enabled or not.",
                        verbose_name="enable",
                    ),
                ),
                (
                    "server",
                    models.CharField(
                        blank=True,
                        help_text="Example: adfs.example.com. Ignored if you use Azure",
                        max_length=255,
                        verbose_name="server (on premise)",
                    ),
                ),
                (
                    "tenant_id",
                    models.CharField(
                        blank=True,
                        help_text="Your tenant ID - this is the 'Directory ID' field in the Azure AD properties.",
                        max_length=50,
                        verbose_name="Azure Tenant ID",
                    ),
                ),
                (
                    "client_id",
                    models.CharField(
                        blank=True,
                        help_text="This is the Azure 'Application ID' or the on-premise 'Client Identifier' value.",
                        max_length=50,
                        verbose_name="client ID",
                    ),
                ),
                (
                    "relying_party_id",
                    models.CharField(
                        help_text="For Azure AD, this can be found in the manifest under 'identifierUris', for on-premise this is the identifier of the web application.",
                        max_length=255,
                        verbose_name="relying party ID",
                    ),
                ),
                (
                    "claim_mapping",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        default=django_auth_adfs_db.models.get_claim_mapping,
                        help_text="Mapping from user-model fields to ADFS claims",
                        verbose_name="claim mapping",
                    ),
                ),
                (
                    "username_claim",
                    models.CharField(
                        blank=True,
                        help_text="Claim to use for the username. If left blank, 'winaccountname' is used for on-premise or 'upn' is for Azure AD.",
                        max_length=50,
                        verbose_name="username claim",
                    ),
                ),
            ],
            options={"verbose_name": "ADFS Configuration",},
        ),
    ]
