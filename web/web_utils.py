def processing_data_from_a_form(data, key):
    """Processing data from a form"""
    product_list = data.get(key).split(",")
    product = dict(product=[word.rstrip(",") for word in product_list])
    return product


def check_error(form, key):
    """Getting fields in which there were errors"""
    list_error = list()
    for _, value in form:
        if key in value:
            list_error.append(value)
    return list_error


def form_valid_data(data, key, scheme):
    """Form data validation"""
    data = dict(data)
    product = processing_data_from_a_form(data, key)
    data.update(product)
    return scheme(**data)


def object_instance(form, model):
    """Creates an instance of the model"""
    data = dict(form)
    return model(**data)
