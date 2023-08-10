def processing_data_from_a_form(data, key):
    """Processing data from a form"""
    if key:
        product_list = data.get(key).split(",")
        product = dict(product=[word.rstrip(",").strip() for word in product_list])
        return product
    return data


def check_error(form, key):
    """Getting fields in which there were errors"""
    list_error = list()
    for _, value in form:
        if not isinstance(value, int):
            if key in value:
                list_error.append(value)
    return list_error


def form_valid_data(data, scheme, key=None):
    """Form data validation"""
    data = dict(data)
    product = processing_data_from_a_form(data, key)
    data.update(product)
    return scheme(**data)


def object_instance(form, model):
    """Creates an instance of the model"""
    data = dict(form)
    return model(**data)


def templates_error(request, templates, name_template, errors_list, status_code, form_fields=None):
    """Returns a template with a list of errors"""
    return templates.TemplateResponse(
        name=name_template, status_code=status_code, context={
            "request": request,
            "errors_list": errors_list,
            "form_fields": form_fields
        }
    )


async def form_processing(request, scheme):
    """form processing"""
    form_data = await request.form()
    form_valid = form_valid_data(form_data, scheme)
    errors_list = check_error(form_valid, "error")
    return form_data, errors_list
