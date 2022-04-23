import jsonschema
import logging


def validate_schema_details(dict, schema):
    try:
        jsonschema.validate(dict, schema)
    except jsonschema.exceptions.ValidationError as err:
        logging.error("The database-server details are not correct %s", err)
        return False
    return True
