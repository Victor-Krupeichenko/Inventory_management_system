from api.company.schemes import CompanyCreateScheme


def form_company():
    """Form for model Company"""
    temp_fields = list()
    fields = CompanyCreateScheme.model_json_schema().get("properties")
    for field in fields:
        temp_fields.append({"title": field, "required": "required"})
    return temp_fields
