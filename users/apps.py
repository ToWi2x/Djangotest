from django.apps import AppConfig


class USersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    def ready(self):
        from .signals import create_profile

