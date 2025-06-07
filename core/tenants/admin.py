from django.contrib import admin

# Register your models here.
from django_tenants.admin import TenantAdminMixin

from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("tenant_name_en", "tenant_name_am", "phone_number", "paid_until", "on_trial")
    search_fields = ("tenant_name_en", "tenant_name_am", "phone_number")
    list_filter = ("on_trial",)
    ordering = ("-created_at",)
