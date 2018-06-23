from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    name = "sparta_webapp.apis"
    verbose_name = "APIS"

    def ready(self):
        try:
            import user.signals  # noqa F401
        except ImportError:
            pass
