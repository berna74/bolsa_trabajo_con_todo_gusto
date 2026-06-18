from django.apps import AppConfig


class ConfiguracionJobs(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jobs"

    def ready(self):
        # Importa señales al iniciar la app.
        from . import signals  # noqa: F401
