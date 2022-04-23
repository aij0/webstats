import urllib
import logging
import re


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


def connect_to_servers(data):
    uri_prefix = "http://"
    for server in data['servers']:
        try:
            page, code = get_page(uri_prefix + server["address"])
            logging.debug("Return code: %s", code)
            if server["regex"]:
                content_found = check_regex(page, server["regex"])
                logging.debug(content_found)
        except Exception as err:
            logging.error("Error: %s", err)
