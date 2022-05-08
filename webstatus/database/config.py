import json
import logging
import sys
from common.validators import validate_schema_details

databaseSchema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "address": {"type": "string", "format": "ip-address"},
            "port": {"type": "number"},
            "user": {"type": "string"},
            "password": {"type": "string"}
        },
        "required": ["name", "address", "port", "user", "password"]
    }


def parse_config(file):
    data = ""
    try:
        file = open(file)
        data = json.load(file)
        if validate_schema_details(data, databaseSchema):
            logging.debug("database-server details ok")
            file.close()
        else:
            logging.error("Issue with database-server detail, \
                            ´please check")
            file.close()
            sys.exit(2)
    except FileNotFoundError:
        logging.error("File [%s] not found", file)
        sys.exit(2)

    return data
