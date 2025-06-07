from .filters import BaseUserFilter
from .models import User


def user_list(current_user=User, filters=None):
    filters = filters or {}

    qs = User.objects.prefetch_related("user_profile", "users_permissions").all()

    return BaseUserFilter(filters, qs, current_user=current_user).qs


def user_profile_details(*, user_id):
    return User.objects.prefetch_related("user_profile", "users_permissions", "user_settings").get(
        id=user_id,
    )
