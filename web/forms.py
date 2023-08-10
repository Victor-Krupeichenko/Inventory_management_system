def form_for_models(scheme):
    """Form for model"""
    temp_fields = list()
    fields = scheme.model_json_schema().get("properties")
    for field in fields:
        temp_fields.append({"title": field, "required": "required"})
    return temp_fields
