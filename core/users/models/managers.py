import pyotp
from django.contrib.auth.models import BaseUserManager

from core.users.models.permissions import UserPermissions


class CustomBaseUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        otp_secret = pyotp.random_base32()

        # Remove fields not belonging to the User model
        is_admin = extra_fields.pop("is_admin", False)
        is_staff = extra_fields.pop("is_staff", False)
        is_superuser = extra_fields.pop("is_superuser", False)

        # Create the User instance
        user = self.model(email=email, otp_secret=otp_secret, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        # Create associated UserPermissions entry
        UserPermissions.objects.get_or_create(
            user=user,
            defaults={
                "is_admin": is_admin,
                "is_staff": is_staff,
                "is_superuser": is_superuser,
            },
        )

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)
