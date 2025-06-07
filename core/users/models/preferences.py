from django.db import models

from core.common.models import BaseModel


class UserPreference(BaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="user_preferences")
    use_email = models.BooleanField(default=True)
    use_sms = models.BooleanField(default=True)

    class Meta:
        verbose_name: str = "User Preference"
        verbose_name_plural: str = "User Preferences"

    def __str__(self) -> str:
        return f"{self.user} - {self.use_email} - {self.use_sms}"
