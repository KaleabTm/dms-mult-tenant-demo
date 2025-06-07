from django.contrib import admin
from easyaudit.admin import CRUDEventAdmin, LoginEventAdmin, RequestEventAdmin
from easyaudit.models import CRUDEvent, LoginEvent, RequestEvent
from unfold.admin import ModelAdmin

from core.departments.admin import DepartmentAdmin, JobTitleAdmin
from core.departments.models import Department, JobTitle
from core.users.admin import UserAdmin
from core.users.models import User

from .models import Address


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ("city_en", "city_am", "created_at", "updated_at")
    search_fields = ["city_en", "city_am"]
    ordering = ["city_en"]
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "city_en",
                    "city_am",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


class DMSAdminSite(admin.AdminSite):
    site_header = "Document Management System Admin Site"
    site_title = "DMS Admin"
    index_title = "Admin Dashboard"


dms_admin_site = DMSAdminSite(name="dms_admin")


dms_admin_site.register(User, UserAdmin)

dms_admin_site.register(JobTitle, JobTitleAdmin)
dms_admin_site.register(Department, DepartmentAdmin)

dms_admin_site.register(LoginEvent, LoginEventAdmin)
dms_admin_site.register(RequestEvent, RequestEventAdmin)
dms_admin_site.register(CRUDEvent, CRUDEventAdmin)
