import click
from os import path


def check_not_null(ctx, param, value):
    """
    Click callback method used to verify command line parameter is not an empty string.
    :param ctx: Python Click library Context object.
    :param param: Python Click Context object params attribute.
    :param value: Value passed in for a given command line parameter.
    """
    if not value:
        raise click.BadParameter("Value cannot be empty / null")
    return value


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


def check_filename_filepath(ctx, param, value):
    """
    Click callback method used for file path input validation.
    :param ctx: Python Click library Context object.
    :param param: Python Click Context object params attribute.
    :param value: Value passed in for a given command line parameter.
    """
    filename = value.strip()
    folder_idx = filename.rfind('/')

    if filename == '':
        raise click.click.BadParameter('Empty filename')

    if folder_idx != -1:
        parent_folder = filename[0: folder_idx + 1]
        if not path.exists(parent_folder):
            raise click.BadParameter('File path does not exist.')

    return value
