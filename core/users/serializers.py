from rest_framework import serializers

from core.common.utils import inline_serializer
from core.users.models import User


class UserProfileListSerializer(serializers.Serializer):
    full_name_en = serializers.CharField()
    full_name_am = serializers.CharField()

    job_title = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "title_en": serializers.CharField(),
            "title_am": serializers.CharField(),
        },
    )
    department = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "abbreviation_en": serializers.CharField(),
            "abbreviation_am": serializers.CharField(),
            "department_name_en": serializers.CharField(),
            "department_name_am": serializers.CharField(),
        },
    )


class UserProfileDetailSerializer(serializers.Serializer):
    first_name_en = serializers.CharField()
    middle_name_en = serializers.CharField()
    last_name_en = serializers.CharField()

    first_name_am = serializers.CharField()
    middle_name_am = serializers.CharField()
    last_name_am = serializers.CharField()

    full_name_en = serializers.CharField()
    full_name_am = serializers.CharField()

    job_title = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "title_en": serializers.CharField(),
            "title_am": serializers.CharField(),
        },
    )
    department = inline_serializer(
        fields={
            "id": serializers.UUIDField(),
            "abbreviation_en": serializers.CharField(),
            "abbreviation_am": serializers.CharField(),
            "department_name_en": serializers.CharField(),
            "department_name_am": serializers.CharField(),
            "contact_email": serializers.EmailField(),
            "contact_phone": serializers.IntegerField(),
        },
    )
    phone_number = serializers.IntegerField()


class UserPermissionsSerializer(serializers.Serializer):
    is_admin = serializers.BooleanField()
    is_staff = serializers.BooleanField()


class UserSettingsSerializer(serializers.Serializer):
    is_2fa_enabled = serializers.BooleanField()
    is_verified = serializers.BooleanField()


class UserPreferencesSerializer(serializers.Serializer):
    use_email = serializers.BooleanField()
    use_sms = serializers.BooleanField()


class UserListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.SerializerMethodField()
    user_profile = UserProfileDetailSerializer()
    users_permissions = UserPermissionsSerializer()

    def get_email(self, obj):
        user = User.objects.get(id=obj.id)
        return user.email


class UserDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.SerializerMethodField()
    user_profile = UserProfileDetailSerializer()
    users_permissions = UserPermissionsSerializer()
    user_settings = UserSettingsSerializer()

    def get_email(self, obj):
        user = User.objects.get(id=obj.id)
        return user.email


class UserEntrySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user_profile = UserProfileListSerializer()
