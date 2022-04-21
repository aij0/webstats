import urllib
from urllib.request import urlopen


def connect_to_servers(data):
    uri_prefix = "https://"
    for server in data['servers']:
        page = urllib.request.urlopen(uri_prefix + server["address"])
        print(page)
