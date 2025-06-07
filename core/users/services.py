from typing import Optional

from django.contrib.auth.hashers import make_password
from django.db import transaction

from .models import User, UserPermissions, UserPreference, UserProfile, UserSetting


@transaction.atomic
def user_create(
    *,
    email: str,
    password: Optional[str] = None,
    first_name_en: str,
    middle_name_en: str,
    last_name_en: str,
    first_name_am: str,
    middle_name_am: str,
    last_name_am: str,
    job_title: str,
    department: str,
    phone_number: int,
    is_admin: bool = False,
    is_staff: bool = False,
    is_kiosk: bool = False,
) -> User:
    existing_user = User.objects.filter(email=email).first()
    # department_instance = Department.objects.get(department_name_en=department)
    # job_title_instance = JobTitle.objects.get(title_en=job_title)

    if not existing_user:
        user_instance = User.objects.create_user(email=email, password=password)
    else:
        user_instance = existing_user

    UserProfile.objects.get_or_create(
        user=user_instance,
        defaults={
            "first_name_en": first_name_en,
            "middle_name_en": middle_name_en,
            "last_name_en": last_name_en,
            "first_name_am": first_name_am,
            "middle_name_am": middle_name_am,
            "last_name_am": last_name_am,
            "job_title_id": job_title,
            "department_id": department,
            "phone_number": phone_number,
        },
    )

    UserPermissions.objects.get_or_create(
        user=user_instance,
        defaults={
            "is_admin": is_admin,
            "is_staff": is_staff,
            "is_kiosk": is_kiosk,
        },
    )

    UserSetting.objects.get_or_create(user=user_instance)

    UserPreference.objects.get_or_create(user=user_instance)

    return user_instance


def superuser_create(
    *,
    email: str,
    password: Optional[str] = None,
    first_name_en: str,
    middle_name_en: str,
    last_name_en: str,
    first_name_am: str,
    middle_name_am: str,
    last_name_am: str,
    job_title: str,
    department: str,
    phone_number: int,
) -> User:
    existing_user = User.objects.filter(email=email).first()

    if not existing_user:
        user_instance = User.objects.create_user(email=email, password=password)
    else:
        user_instance = existing_user

    UserProfile.objects.get_or_create(
        user=user_instance,
        defaults={
            "first_name_en": first_name_en,
            "middle_name_en": middle_name_en,
            "last_name_en": last_name_en,
            "first_name_am": first_name_am,
            "middle_name_am": middle_name_am,
            "last_name_am": last_name_am,
            "job_title_id": job_title,
            "department_id": department,
            "phone_number": phone_number,
        },
    )

    user_permissions, created = UserPermissions.objects.get_or_create(
        user=user_instance,
        defaults={
            "is_admin": True,
            "is_staff": True,
            "is_superuser": True,
        },
    )

    if not created:
        user_permissions.is_admin = True
        user_permissions.is_staff = True
        user_permissions.is_superuser = True
        user_permissions.save()

    UserSetting.objects.get_or_create(user=user_instance)

    UserPreference.objects.get_or_create(user=user_instance)

    return user_instance


@transaction.atomic
def user_update(
    *,
    user_instance: User,
    first_name_en: str = None,
    middle_name_en: str = None,
    last_name_en: str = None,
    first_name_am: str = None,
    middle_name_am: str = None,
    last_name_am: str = None,
    phone_number: int = None,
    use_email: bool = None,
    use_sms: bool = None,
) -> User:
    # Update UserProfile
    user_profile = user_instance.user_profile

    if user_profile:
        # Update existing profile fields
        if first_name_en is not None:
            user_profile.first_name_en = first_name_en
        if middle_name_en is not None:
            user_profile.middle_name_en = middle_name_en
        if last_name_en is not None:
            user_profile.last_name_en = last_name_en
        if first_name_am is not None:
            user_profile.first_name_am = first_name_am
        if middle_name_am is not None:
            user_profile.middle_name_am = middle_name_am
        if last_name_am is not None:
            user_profile.last_name_am = last_name_am
        if phone_number is not None:
            user_profile.phone_number = phone_number
    else:
        # Create a new profile
        user_profile = UserProfile.objects.create(
            user=user_instance,
            first_name_en=first_name_en,
            middle_name_en=middle_name_en,
            last_name_en=last_name_en,
            first_name_am=first_name_am,
            middle_name_am=middle_name_am,
            last_name_am=last_name_am,
        )

    user_profile.save()

    # Update or create user preferences
    user_preference, _ = UserPreference.objects.get_or_create(user=user_instance)
    if use_email is not None:
        user_preference.use_email = bool(use_email)
    if use_sms is not None:
        user_preference.use_sms = bool(use_sms)
    user_preference.save()

    return user_instance


def hash_password_if_needed(user):
    """Hashes the password if it's not already hashed."""
    if user.password and not user.password.startswith("pbkdf2_sha256$"):  # Avoid double hashing
        user.password = make_password(user.password)
    return user


def process_imported_user_data(row: dict) -> dict:
    """Ensure imported passwords are hashed."""
    if "password" in row and row["password"]:
        row["password"] = make_password(row["password"])
    return row
