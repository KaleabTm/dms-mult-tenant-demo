from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm

from .models import Department, JobTitle
from .resources import DepartmentResource, JobTitleResource


@admin.register(Department)
class DepartmentAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = DepartmentResource
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

    list_display = (
        "department_name_en",
        "department_name_am",
        "abbreviation_en",
        "abbreviation_am",
        "created_at",
        "updated_at",
    )
    ordering = ["department_name_en"]


@admin.register(JobTitle)
class JobTitleAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = JobTitleResource
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

    list_display = ("title_en", "title_am", "titer_am", "titer_en", "created_at", "updated_at")
    ordering = ["title_en"]
