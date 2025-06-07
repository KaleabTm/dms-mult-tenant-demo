from django.db import models

from core.common.models import BaseModel


class UserSetting(BaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="user_settings")
    is_2fa_enabled = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name: str = "User Setting"
        verbose_name_plural: str = "User Settings"

    def __str__(self) -> str:
        return f"{self.user} - {self.is_2fa_enabled} - {self.is_verified} "
