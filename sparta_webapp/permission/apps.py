# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PermissionConfig(AppConfig):
    name = 'permission'
    verbose_name = _("Permissions")

    def ready(self):
        try:
            import sparta_webapp.users.signals  # noqa F401
        except ImportError:
            pass
