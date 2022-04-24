import urllib
import logging
import re
from threading import Timer
from database.local import create_server_insert_query, query


def get_page(address):
    response = urllib.request.urlopen(address)
    return_code = response.getcode()
    html_bytes = response.read()
    html = html_bytes.decode('utf-8')
    return html, return_code


def check_regex(page, regex):
    pattern = re.compile(regex)
    res = pattern.findall(page)
    logging.debug(res)
    if res:
        return True
    else:
        return False


def connect_to_server(server):
    uri_prefix = "http://"
    name = server["server"]
    address = server["address"]
    regex = server["regex"]

    try:
        page, retcode = get_page(uri_prefix + address)
        logging.debug("Server [%s] return code: %s", name, retcode)
        if regex:
            content_found = check_regex(page, regex)
            logging.debug(content_found)
    except Exception as err:
        logging.error("Error: %s", err)


class Repeater(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def poller(data, db_connection):
    for server in data['servers']:
        name = server["server"]
        address = server["address"]
        query(db_connection, create_server_insert_query(name, address))
        timer = Repeater(server["poll_period"], connect_to_server, [server])
        timer.start()
