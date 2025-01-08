from django.apps import AppConfig

class USersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals  # Import the entire signals module, not just one function
