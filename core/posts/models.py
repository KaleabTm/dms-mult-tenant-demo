from django.contrib.auth import get_user_model
from django.db import models

from core.common.models import BaseModel

User = get_user_model()


# Create your models here.
class Post(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ("title",)
        permissions = [
            ("can_edit_post", "Can Edit Post"),
            ("can_create_post", "Can Create Post"),
            ("can_view_post", "Can View Post"),
            ("can_publish", "Can Publish Post"),
            ("can_delete_post", "Can Delete Ppost"),
            ("can_share_post", "Can Share Post"),
            ("can_report_post", "Can Report Post"),
            ("can_comment_on_post", "Can Comment On Post"),
        ]

    def __str__(self):
        return self.title
