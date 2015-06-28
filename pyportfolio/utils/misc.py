import inspect

def get_required_args(f, d):
    """
    :param f: function
    :param d: dictionary of arguments
    :return: dictionary of arguments, reduced to only the ones required by
    function
    """
    args = inspect.getargspec(f)[0]
    if args[0] == 'self':
        args = args[1:]
    return {k: d[k] for k in args}
