from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import DepartmentListApi, JobTitleListApi

app_name = "enterprises"

urlpatterns: list[URLPattern] = [
    path("", DepartmentListApi.as_view(), name="department-list"),
    path("job_titles/", JobTitleListApi.as_view(), name="job_title-list"),
]
