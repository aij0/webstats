#!/usr/bin/python
import getopt
import logging
import sys
from common.validators import validate_input_file_type
from server.servers import parse_servers
from server.poller import poller
from database.config import parse_config


def parse_args(argv):
    help = '''\nArgument(s):
-h [help],
-s <JSON inputfile> [web servers],
-d <JSON inputfile> [database]'''
    server_inputfile = ""
    database_inputfile = ""

    try:
        opts, args = getopt.getopt(argv, "hs:d:", ["sfile=", "dfile="])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(help)
            sys.exit()
        elif opt in ("-s", "--sfile"):
            server_inputfile = validate_input_file_type(arg)
        elif opt in ("-d", "--dfile"):
            database_inputfile = validate_input_file_type(arg)
        else:
            print("unknown argument, exiting")
            sys.exit(1)

    if not opts:
        print(help)
        sys.exit()

    if not server_inputfile:
        print("Server config missing!")
        print(help)
        sys.exit(1)
    if not database_inputfile:
        print("Database config missing!")
        print(help)
        sys.exit(1)

    return server_inputfile, database_inputfile


def main(argv):

    server_inputfile, database_inputfile = parse_args(argv)

    try:
        servers = parse_servers(server_inputfile)
    except KeyError as err:
        logging.error("Please use 'servers' as array name %s", err)
        sys.exit(1)
    try:
        database = parse_config(database_inputfile)
    except Exception as err:
        logging.error("Error while parsing database config %s", err)
        sys.exit(1)

    poller(servers, database)


if __name__ == "__main__":
    main(sys.argv[1:])
