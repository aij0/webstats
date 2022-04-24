import jsonschema
import logging
import os
import sys


def validate_schema_details(dict, schema):
    try:
        jsonschema.validate(dict, schema)
    except jsonschema.exceptions.ValidationError as err:
        logging.error("The database-server details are not correct %s", err)
        return False
    return True


def validate_input_file_type(file):
    filename, file_extension = os.path.splitext(file)
    if file_extension == ".json":
        return file
    else:
        logging.error("input file not .json, please check file given")
        sys.exit(1)
