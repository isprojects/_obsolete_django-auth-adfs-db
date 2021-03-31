import logging
from typing import Any

from django.db.utils import ProgrammingError
from django.shortcuts import render

from .models import ADFSConfig

# TODO: settings need to be cleared/re-evaluated on update of database object

logger = logging.getLogger(__name__)


class DynamicSetting:
    def __init__(self, required=True):
        self.required = required

    def __set_name__(self, owner, setting: str):
        self.setting = setting

    def __get__(self, instance, owner) -> Any:
        try:
            config = ADFSConfig.get_solo()
        except ProgrammingError:
            logger.warning("Database table ADFSConfig not (fully) synced (yet)")
            return None
        _settings = config.as_settings()
        if self.required and self.setting not in _settings:
            raise KeyError(f"Setting {self.setting} is required but not present")
        return _settings.get(self.setting)


def default_failed_response_view(request, error_message=None, status=None):
    return render(
        request,
        "django_auth_adfs/login_failed.html",
        {"error_message": error_message},
        status=status,
    )


class Settings:

    # defaults
    BOOLEAN_CLAIM_MAPPING = {}
    CLIENT_SECRET = None
    CONFIG_RELOAD_INTERVAL = 24  # hours
    CREATE_NEW_USERS = True
    DISABLE_SSO = False
    GROUP_TO_FLAG_MAPPING = {}
    LOGIN_EXEMPT_URLS = []
    MIRROR_GROUPS = False
    RETRIES = 3
    TIMEOUT = 5
    JWT_LEEWAY = 0
    CUSTOM_FAILED_RESPONSE_VIEW = staticmethod(default_failed_response_view)

    SERVER = DynamicSetting(required=False)
    CLIENT_ID = DynamicSetting()
    CLIENT_SECRET = DynamicSetting(required=False)
    TENANT_ID = DynamicSetting(required=False)
    RELYING_PARTY_ID = DynamicSetting()
    AUDIENCE = DynamicSetting()
    CA_BUNDLE = DynamicSetting()
    CLAIM_MAPPING = DynamicSetting()
    USERNAME_CLAIM = DynamicSetting()
    GROUPS_CLAIM = DynamicSetting()
