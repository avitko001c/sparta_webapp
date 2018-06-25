from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EventLogAppConfig(AppConfig):
    name = "sparta_webapp.eventlog"
    verbose_name = _("EventLogs")

    def ready(self):
        """Override this to put in:
            Eventlog signal registration
        """
        try:
            import sparta_webapp.eventlog.signals  # noqa F401
        except ImportError:
            pass
