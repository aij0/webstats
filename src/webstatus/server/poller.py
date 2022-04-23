import urllib
import logging
import re
import threading


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

    try:
        page, code = get_page(uri_prefix + server["address"])
        logging.debug("Return code: %s", code)
        if server["regex"]:
            content_found = check_regex(page, server["regex"])
            logging.debug(content_found)
    except Exception as err:
        logging.error("Error: %s", err)


def poller(data):
    threads = list()
    for server in data['servers']:
        logging.debug("starting thread for %s.", server)
        x = threading.Thread(target=connect_to_server, args=(server,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()
        logging.debug("thread %d done", index)
