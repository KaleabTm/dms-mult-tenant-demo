from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import UserCreateApi, UserDetailApi, UserListApi, UserUpdateApi

app_name = "users"

urlpatterns: list[URLPattern] = [
    path("", UserListApi.as_view(), name="user-list"),
    path("create/", UserCreateApi.as_view(), name="user-create"),
    path("<uuid:id>/", UserDetailApi.as_view(), name="user-detail"),
    path("update/", UserUpdateApi.as_view(), name="user-update"),
]
