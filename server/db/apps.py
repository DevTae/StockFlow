from django.apps import AppConfig


class DbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db'
    
    # django 시작 시 호출되는 함수 (server/settings.py 바탕)
    def ready(self):
        import db.signals.signals
