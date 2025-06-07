from import_export import resources

from .models import Department, JobTitle


class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        fields = (
            "department_name_en",
            "department_name_am",
            "abbreviation_en",
            "abbreviation_am",
            "description",
            "contact_phone",
            "contact_email",
        )
        export_order = fields
        import_id_fields = (
            "department_name_en",
            "department_name_am",
            "abbreviation_en",
            "abbreviation_am",
        )


class JobTitleResource(resources.ModelResource):
    class Meta:
        model = JobTitle
        fields = (
            "title_en",
            "title_am",
            "titer_en",
            "titer_am",
        )
        export_order = fields
        import_id_fields = (
            "title_en",
            "title_am",
            "titer_en",
            "titer_am",
        )
