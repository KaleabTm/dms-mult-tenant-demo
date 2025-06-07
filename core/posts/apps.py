from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.posts"

    def ready(self):
        from core.common.utils import register_tenant_only_model

        from .models import Post

        register_tenant_only_model(Post)
