from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from core.emails.tasks import email_send_task

from .models.permissions import UserPermissions
from .models.preferences import UserPreference
from .models.settings import UserSetting
from .models.user import User


@receiver(pre_save, sender=User)
def pre_save_handler(sender, instance, *arg, **kwarg):
    if not instance.password:
        instance.password = get_random_string(length=8)


@receiver(post_save, sender=User)
def post_save_handler(sender, instance, created, *args, **kwargs):
    if created:
        UserPermissions.objects.get_or_create(user=instance)

        UserSetting.objects.get_or_create(user=instance)

        UserPreference.objects.get_or_create(user=instance)

        if not instance.password:
            instance.password = get_random_string(length=8)
            email_send_task.delay_on_commit(
                instance.email,
                "Welcome to Our Service",
                "registration",
                context={
                    "username": instance.email,
                    "default_password": instance.password,
                    # "first_name": instance.user_profile.first_name_en,
                    "first_name": "",
                },
            )
        else:
            email_send_task.delay_on_commit(
                instance.email,
                "Welcome to Our Service",
                "welcome",
                context={
                    "first_name": "",
                    # "first_name": instance.user_profile.first_name_en,
                },
            )
