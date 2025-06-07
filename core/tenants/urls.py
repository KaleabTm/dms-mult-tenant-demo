from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import TenantCreateApi

app_name = "tenants"

urlpatterns: list[URLPattern] = [
    path("create/", TenantCreateApi.as_view(), name="tenant-create"),
]
