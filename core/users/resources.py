from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from core.departments.models import Department, JobTitle

from .models import User, UserPermissions, UserPreference, UserProfile, UserSetting
from .services import process_imported_user_data


class UserResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        process_imported_user_data(row)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )
        export_order = fields
        import_id_fields = ("email",)


class UserProfileResource(resources.ModelResource):
    user = Field(attribute="user", column_name="email", widget=ForeignKeyWidget(User, "email"))
    department = Field(
        attribute="department",
        column_name="department",
        widget=ForeignKeyWidget(Department, "abbreviation_en"),
    )
    job_title = Field(attribute="job_title", column_name="job_title", widget=ForeignKeyWidget(JobTitle, "title_en"))

    class Meta:
        model = UserProfile
        fields = (
            "user",
            "first_name_en",
            "middle_name_en",
            "last_name_en",
            "first_name_am",
            "middle_name_am",
            "last_name_am",
            "job_title",
            "department",
            "phone_number",
        )
        export_order = fields
        import_id_fields = ("user",)


class UserSettingResource(resources.ModelResource):
    user = Field(attribute="user", column_name="email", widget=ForeignKeyWidget(User, "email"))

    class Meta:
        model = UserSetting
        fields = (
            "user",
            "is_2fa_enabled",
            "is_verified",
        )
        export_order = fields
        import_id_fields = ("user",)


class UserPreferenceResource(resources.ModelResource):
    user = Field(attribute="user", column_name="email", widget=ForeignKeyWidget(User, "email"))

    class Meta:
        models = UserPreference
        fields = (
            "user",
            "use_email",
            "use_sms",
        )
        export_order = fields
        import_id_fields = ("user",)


class UserPermissionsResource(resources.ModelResource):
    user = Field(attribute="user", column_name="email", widget=ForeignKeyWidget(User, "email"))

    class Meta:
        model = UserPermissions
        fields = (
            "user",
            "is_admin",
            "is_staff",
            "is_superuser",
            "is_kioskuser",
        )
        export_order = fields
        import_id_fields = ("user",)
