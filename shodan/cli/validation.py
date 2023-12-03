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

def check_file_format(ctx, param, value):
    """
    Click callback method used for output file format input validation.
    :param ctx: Python Click library Context object.
    :param param: Python Click Context object params attribute.
    :param value: Value passed in for a given command line parameter.
    """
    supported_file_types = ["kml", "csv", "geo.json", "images", "xlsx"]
    file_type_str = ', '.join(supported_file_types)

    if value not in supported_file_types:
        raise click.BadParameter(f"Output file type must be one of the supported file extensions:\n{file_type_str}")
    return value
