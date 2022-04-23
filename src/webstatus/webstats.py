#!/usr/bin/python
import getopt
import logging
import os
import sys
from server.servers import parse_servers
from server.poller import poller


def validate_input_file_type(file):
    filename, file_extension = os.path.splitext(file)
    if file_extension == ".json":
        return file
    else:
        logging.error("input file not .json, please check file given")
        sys.exit(1)


def main(argv):
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
            sys.exit(0)

    if not opts:
        print(help)
        sys.exit()

    try:
        servers = parse_servers(inputfile)
    except KeyError as err:
        logging.error("Please use 'servers' as array name %s", err)
        sys.exit(1)

    poller(servers)


if __name__ == "__main__":
    main(sys.argv[1:])
