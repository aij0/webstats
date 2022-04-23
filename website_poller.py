import urllib
import logging
import re


def get_page(address):
    page_raw = urllib.request.urlopen(address)
    html_bytes = page_raw.read()
    html = html_bytes.decode('utf-8')
    return html


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
            page = get_page(uri_prefix + server["address"])
            if server["regex"]:
                content_found = check_regex(page, server["regex"])
                logging.debug(content_found)
        except Exception as err:
            logging.error("Error: %s", err)
