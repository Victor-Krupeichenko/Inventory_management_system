from fastapi import status


async def error_checking(data, key):
    """Check fields errors"""
    list_errors = list()
    for value in data.values():
        if isinstance(value, dict):
            list_errors.append(value.get(key))
    if list_errors:
        return {"message": f"#{' #'.join(list_errors)}", "status": status.HTTP_400_BAD_REQUEST}
    return None
