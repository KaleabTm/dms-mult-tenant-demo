from django.urls import include, path
from django.urls.resolvers import URLResolver

urlpatterns: list[URLResolver] = [
    path("auth/", include(("core.authentication.urls", "authentication"), namespace="authentication")),
    path("contacts/", include(("core.contacts.urls", "contacts"), namespace="contacts")),
    path("departments/", include(("core.departments.urls", "departmetns"), namespace="departments")),
    path("users/", include(("core.users.urls", "users"), namespace="users")),
    path("posts/", include(("core.posts.urls", "posts"), namespace="posts")),
    path("tenants/", include(("core.tenants.urls", "tenants"), namespace="tenants")),
]
