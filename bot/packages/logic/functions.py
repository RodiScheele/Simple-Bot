# Checks if a given parameter is an integer.
async def is_int(parameter):
    value = True
    try:
        int(parameter)
    except ValueError:
        value = False

    return value
