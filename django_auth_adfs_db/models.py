from typing import Dict

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext, gettext_lazy as _

from solo.models import SingletonModel


def get_claim_mapping() -> Dict[str, str]:
    return {
        "first_name": "given_name",
        "last_name": "family_name",
        "email": "email",
    }


class ADFSConfig(SingletonModel):
    enabled = models.BooleanField(
        _("enable"),
        default=False,
        help_text=_("Master switch if ADFS login/SSO is enabled or not."),
    )

    # on premise settings
    server = models.CharField(
        _("server (on premise)"),
        max_length=255,
        blank=True,
        help_text=_("Example: adfs.example.com. Ignored if you use Azure"),
    )

    # azure settings
    tenant_id = models.CharField(
        _("Azure Tenant ID"),
        max_length=50,
        blank=True,
        help_text=_("Your Azure tenant ID, you can find this on the overview page."),
    )
    client_secret = models.CharField(
        _("client secret"),
        max_length=200,
        blank=True,
        help_text=_("This is a client secret created for the Azure AD application."),
    )

    # shared settings
    client_id = models.CharField(
        _("client ID"),
        max_length=50,
        blank=True,
        help_text=_(
            "This is the Azure 'Client ID' or the on-premise 'Client Identifier' value."
        ),
    )
    relying_party_id = models.CharField(
        _("relying party ID"),
        max_length=255,
        help_text=_(
            "For Azure AD, this is the client ID, "
            "for on-premise this is the identifier of the web application."
        ),
    )
    claim_mapping = JSONField(
        _("claim mapping"),
        default=get_claim_mapping,
        help_text=("Mapping from user-model fields to ADFS claims"),
    )
    username_claim = models.CharField(
        _("username claim"),
        max_length=50,
        blank=True,
        help_text=_(
            "Claim to use for the username. If left blank, 'winaccountname' is used "
            "for on-premise or 'upn' is for Azure AD."
        ),
    )
    sync_groups = models.BooleanField(
        _("synchronize groups?"),
        default=True,
        help_text=_(
            "Synchronize the local user groups with the ADFS groups. Note that this "
            "means a user is removed from all groups if there is no group claim. "
            "Uncheck to manage groups manually."
        ),
    )

    class Meta:
        verbose_name = _("ADFS Configuration")

    def __str__(self):
        type_ = _("On-premise") if self.server else "Azure"
        return gettext("{type} ADFS configuration").format(type=type_)

    def clean(self):
        super().clean()

        # validate claim mapping
        User = get_user_model()
        for field in self.claim_mapping.keys():
            try:
                User._meta.get_field(field)
            except models.FieldDoesNotExist:
                raise ValidationError(
                    {
                        "claim_mapping": _(
                            "Field {field} does not exist on the user model"
                        ).format(field=field)
                    }
                )

        if User.USERNAME_FIELD in self.claim_mapping:
            raise ValidationError(
                {
                    "claim_mapping": _(
                        "The username field may not be in the claim mapping"
                    ),
                }
            )

    def as_settings(self) -> dict:
        """
        Return the configuration as a dict suitable to pass to django-auth-adfs
        """
        from django_auth_adfs.config import AZURE_AD_SERVER

        on_premise = bool(self.server)

        default_groups_claim = "group" if on_premise else "roles"
        groups_claim = None if not self.sync_groups else default_groups_claim

        settings = {
            "CLIENT_ID": self.client_id,
            "RELYING_PARTY_ID": self.relying_party_id,
            "CA_BUNDLE": True,
            "CLAIM_MAPPING": self.claim_mapping.copy(),
            "GROUPS_CLAIM": groups_claim,
            "MIRROR_GROUPS": self.sync_groups,
        }

        if on_premise:
            settings.update(
                {
                    "SERVER": self.server,
                    "TENANT_ID": "adfs",
                    "AUDIENCE": f"microsoft:identityserver:{self.relying_party_id}",
                    "USERNAME_CLAIM": self.username_claim or "winaccountname",
                }
            )
        else:  # Azure AD
            settings.update(
                {
                    "SERVER": AZURE_AD_SERVER,
                    "CLIENT_SECRET": self.client_secret,
                    "TENANT_ID": self.tenant_id,
                    "AUDIENCE": self.relying_party_id,
                    "USERNAME_CLAIM": self.username_claim or "upn",
                }
            )

        return settings


@receiver(post_save, sender=ADFSConfig)
def clear_provider_config_cache(sender: ADFSConfig, **kwargs):
    # clear provider cache - local import because of circular dependency
    if kwargs["created"]:
        return

    from django_auth_adfs.config import provider_config

    provider_config._config_timestamp = None
