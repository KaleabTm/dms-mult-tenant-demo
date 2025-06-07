from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel

from .managers import CustomBaseUserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(blank=False, max_length=255, unique=True, verbose_name=_("Email address"))
    otp_secret = models.TextField(editable=False, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = CustomBaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.id} - {self.email}"
