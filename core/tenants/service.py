import re

from .models import Domain, Tenant  # Adjust import path as needed


def extract_subdomain(domain_url: str) -> str:
    """
    Extract a schema-safe subdomain from a full domain.
    Example: 'tenant1.example.com' -> 'tenant1'
    """
    subdomain = domain_url.split(".")[0].lower()
    # clean to match schema rules: lowercase, no dashes/spaces

    return re.sub(r"[^a-z0-9_]", "_", subdomain)


def tenant_create(
    tenant_name_am: str,
    tenant_name_en: str,
    phone_number: str,
    domain_url: str,
    paid_until=None,
    on_trial=None,
) -> Tenant:
    slug = extract_subdomain(domain_url)

    tenant = Tenant.objects.create(
        tenant_name_am=tenant_name_am,
        tenant_name_en=tenant_name_en,
        phone_number=phone_number,
        slug=slug,
        schema_name=slug,  # important for django-tenants
        paid_until=paid_until,
        on_trial=on_trial,
    )

    Domain.objects.create(
        domain=domain_url,
        tenant=tenant,
        is_primary=True,
    )

    return tenant
