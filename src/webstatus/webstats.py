#!/usr/bin/python
import getopt
import logging
import sys
from common.validators import validate_input_file_type
from database.local import setup_database
from server.servers import parse_servers
from server.poller import poller


def parse_args(argv):
    help = "-h [help], -i <inputfile> [web servers]"
    inputfile = ""

    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(help)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = validate_input_file_type(arg)
        else:
            print("unknown argument, exiting")
            sys.exit(1)

    if not opts:
        print(help)
        sys.exit()

    return inputfile


def main(argv):

    inputfile = parse_args(argv)

    try:
        servers = parse_servers(inputfile)
    except KeyError as err:
        logging.error("Please use 'servers' as array name %s", err)
        sys.exit(1)

    try:
        db_connection = setup_database("local.sqlite")
    except Exception as err:
        print("Can't create local database: ", err)
        sys.exit(3)

    poller(servers)


if __name__ == "__main__":
    main(sys.argv[1:])
