from django.db import models

from core.common.models import BaseModel


class UserPermissions(BaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="users_permissions")
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_kioskuser = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User Permission"
        verbose_name_plural = "User Permissions"

    def __str__(self):
        return f"Permissions for {self.user.id}: Staff: {self.is_staff}, Superuser: {self.is_superuser}, Admin:{self.is_admin}"  # noqa: E501
