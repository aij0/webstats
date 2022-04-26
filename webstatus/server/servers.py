import json
import logging
import sys
from common.validators import validate_schema_details

serverSchema = {
        "type": "object",
        "properties": {
            "server": {"type": "string"},
            "address": {"type": "string", "format": "ip-address"},
            "poll_period": {"type": "number"},
            "regex": {"type": "string"}
        },
        "required": ["server", "address", "poll_period", "regex"]
    }


def parse_servers(file):
    data = ""
    try:
        file = open(file)
        data = json.load(file)
        for server in data['servers']:
            if validate_schema_details(server, serverSchema):
                logging.debug("Server details ok")
            else:
                logging.warning("Issue with server detail, please check")
        file.close()
    except FileNotFoundError:
        logging.error("File not found")
        sys.exit(2)

    return data
