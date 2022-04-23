import json
import jsonschema
import logging

serverSchema = {
        "type": "object",
        "properties": {
            "server": {"type": "string"},
            "address": {"type": "string", "format": "ip-address"},
            "poll_period": {"type": "number"},
            "regex": {"type": "string"}
        }
    }


def validate_server_details(dict):
    try:
        jsonschema.validate(instance=dict, schema=serverSchema)
    except jsonschema.exceptions.ValidationError as err:
        logging.error("The server details are not correct %s", err)
        return False
    return True


def parse_servers(file):
    file = open(file)
    data = json.load(file)
    for i in data['servers']:
        if validate_server_details(i):
            logging.debug("Server details ok")
        else:
            logging.warning("Issue with server detail, please check")
    file.close()
    return data
