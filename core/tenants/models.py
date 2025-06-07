from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from core.common.models import BaseModel

class Tenant(BaseModel, TenantMixin):
    tenant_name_am = models.CharField(max_length=100)
    tenant_name_en = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    paid_until =  models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(null=True, blank=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class Domain(BaseModel, DomainMixin):
    domain = models.CharField(max_length=255, unique=True)  # e.g. company1.example.com
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="domains")
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def __str__(self):
        return self.domain


class Membership(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="memberships")
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="memberships")
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_kioskuser = models.BooleanField(default=False)
    job_title = models.ForeignKey("departments.JobTitle", null=True, blank=True, on_delete=models.SET_NULL)
    department = models.ForeignKey("departments.Department", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("user", "tenant")

    def get_role(self):
        if self.is_admin:
            return "admin"
        elif self.is_staff:
            return "staff"
        elif self.is_kioskuser:
            return "kioskuser"
        return "none"
