import json
import logging
import sys
from common.validators import validate_schema_details

databaseSchema = {
        "type": "object",
        "properties": {
            "server": {"type": "string"},
            "address": {"type": "string", "format": "ip-address"},
            "port": {"type": "number"},
            "user": {"type": "string"},
            "password": {"type": "string"}
        },
        "required": ["server", "address", "port", "user", "password"]
    }


def parse_config(file):
    data = ""
    try:
        file = open(file)
        data = json.load(file)
        if validate_schema_details(data, databaseSchema):
            logging.debug("database-server details ok")
        else:
            logging.warning("Issue with database-server detail, \
                            ´please check")
        file.close()
    except FileNotFoundError:
        logging.error("File not found")
        sys.exit(2)

    return data
