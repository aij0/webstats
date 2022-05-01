import urllib
import logging
import re
import sys
from threading import Timer
from database.local import create_server_insert_query
from database.local import create_status_insert_query, execute_query
from database.local import setup_database


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
    content_found = 'NULL'
    retcode = None

    try:
        page, retcode = get_page(uri_prefix + address)
        logging.debug("Server [%s] return code: %s", name, retcode)
        if regex:
            content_found = check_regex(page, regex)
            logging.debug(content_found)
    except Exception as err:
        logging.error("Error: %s", err)

    return retcode, content_found


def poll_server(server, database, server_id):
    return_code, content_found = connect_to_server(server)

    try:
        execute_query(database,
                      "push",
                      create_status_insert_query(return_code,
                                                 content_found,
                                                 server_id))
    except Exception as err:
        logging.error("Can't execute query to the database [%s]: ",
                      database["name"], err)
        sys.exit(3)


class Repeater(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def poller(data, database):
    for server in data['servers']:
        name = server["server"]
        address = server["address"]
        server_id_query = f"SELECT id FROM servers WHERE name = '{name}'"

        setup_database(database)

        execute_query(database, "push",
                      create_server_insert_query(database["type"],
                                                 name, address))

        server_id = execute_query(database,
                                  "pull",
                                  server_id_query)
        server_id = server_id[0]
        logging.debug("Server %s id %s", name, server_id)
        timer = Repeater(server["poll_period"],
                         poll_server, [server, database, server_id])
        timer.start()
