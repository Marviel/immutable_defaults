import inspect

AVAILABLE_TYPES = [list, dict]

def construct_new_default(default_name, default_value):
    if type(default_value) == dict:
        return dict(default_value)
    elif type(default_value) == list:
        return default_value[:]
    else:
        raise ValueError("Default %s was not of supported type. Found type %s" %
                         (default_name, type(default_value)))

def immutable_defaults(*immutable_names, **argv):
    def wrapper(wrapped_function):
        def new_function(*args, **kwargs):
            # Get the wrapped_functioninal list of function defaults
            a = inspect.getargspec(wrapped_function)
            defaults = zip(a.args[-len(a.defaults):], a.defaults)

            for dk, dv in defaults:
                if len(immutable_names) > 0:
                    if dk in immutable_names:
                            kwargs[dk] = construct_new_default(dk, dv)  # Create a new list that will not be appended to a bunch.
                else:
                    kwargs[dk] = construct_new_default(dk, dv)  # Create new list.

            wrapped_function(*args, **kwargs)

        return new_function
    return wrapper
