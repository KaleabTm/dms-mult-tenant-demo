from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm

from core.users.services import hash_password_if_needed

from .models import User, UserPermissions, UserPreference, UserProfile, UserSetting
from .resources import (
    UserProfileResource,
    UserResource,
)


@admin.register(User)
class UserAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = UserResource
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm
    list_display = [
        "id",
        "email",
        "is_active",
    ]
    fieldsets = (
        (
            "Authentication Info",
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "updated_at",
                ),
            },
        ),
    )
    readonly_fields = [
        "last_login",
        "updated_at",
    ]

    def save_model(self, request, obj, form, change):
        """Ensure password is hashed before saving."""
        obj = hash_password_if_needed(obj)
        super().save_model(request, obj, form, change)


# Admin Configuration for the UserProfile Model
@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = UserProfileResource
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

    list_display = [
        "user",
        "full_name_en",
        "job_title",
        "department",
        "phone_number",
    ]
    search_fields = [
        "first_name_en",
        "middle_name_en",
        "last_name_en",
        "first_name_am",
        "middle_name_am",
        "last_name_am",
        "phone_number",
        "job_title__title_en",
        "department__department_name_en",
    ]
    fieldsets = (
        (
            "User",
            {
                "fields": ("user",),
            },
        ),
        (
            "Personal Info (English)",
            {
                "fields": (
                    "first_name_en",
                    "middle_name_en",
                    "last_name_en",
                    "phone_number",
                ),
            },
        ),
        (
            "Personal Info (Amharic)",
            {
                "fields": (
                    "first_name_am",
                    "middle_name_am",
                    "last_name_am",
                ),
            },
        ),
        (
            "Job Details",
            {
                "fields": (
                    "job_title",
                    "department",
                ),
            },
        ),
    )


# Admin Configuration for the UserPermissions Model
@admin.register(UserPermissions)
class UserPermissionsAdmin(ModelAdmin):
    list_display = [
        "user",
        "is_admin",
        "is_staff",
        "is_superuser",
        "is_kioskuser",
    ]
    fieldsets = (
        (
            "User",
            {
                "fields": ("user",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                    "is_kioskuser",
                ),
            },
        ),
    )
    readonly_fields = []


# Admin Configuration for the UserSetting Model
@admin.register(UserSetting)
class UserSettingAdmin(ModelAdmin):
    list_display = ["user", "is_2fa_enabled", "is_verified"]
    fieldsets = (
        (
            "User",
            {
                "fields": ("user",),
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "is_2fa_enabled",
                    "is_verified",
                ),
            },
        ),
    )
    readonly_fields = ["is_2fa_enabled", "is_verified"]


# Admin Configuration for the UserPreference Model
@admin.register(UserPreference)
class UserPreferenceAdmin(ModelAdmin):
    list_display = ["user", "use_email", "use_sms"]
    fieldsets = (
        (
            "User",
            {
                "fields": ("user",),
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "use_email",
                    "use_sms",
                ),
            },
        ),
    )
    readonly_fields = []
