from django.apps import AppConfig


class EduoneConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eduone'
    
    def ready(self):
        import eduone.signals  