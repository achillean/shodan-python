import click


def check_input_file_type(ctx, param, value):
    """
    Click callback method used for file type input validation.
    :param ctx: Python Click library Context object.
    :param param: Python Click Context object params attribute.
    :param value: Value passed in for a given command line parameter.
    """
    idx = value.find(".")

    if idx == -1 or value[idx:] != ".json.gz":
        raise click.BadParameter("Input file type must be '.json.gz'")
    return value
