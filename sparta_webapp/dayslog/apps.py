from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DaysLogAppConfig(AppConfig):
    name = "sparta_webapp.dayslog"
    verbose_name = _("DaysLogs")

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
