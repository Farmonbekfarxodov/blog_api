from django.apps import AppConfig


class AppPostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_posts'

    def ready(self):
        from . import signals  # noqa: F401
