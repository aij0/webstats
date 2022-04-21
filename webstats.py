#!/usr/bin/python
import getopt
import logging
import os
import sys
from servers import parse_servers


def validate_input_file_type(file):
    filename, file_extension = os.path.splitext(file)
    if file_extension == ".json":
        return file
    else:
        logging.error("input file not .json, please check file given")
        sys.exit(1)

def main(argv):
    help = "-h [help], -i <inputfile> [web servers]"

    try:
        opts, args = getopt.getopt(argv, "hi:",["ifile="])
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
            print("No arguments give, exiting")
            sys.exit(0)

    try:
        parse_servers(inputfile)
    except KeyError as err:
        logging.error("Please use 'servers' as array name %s", err)
        sys.exit(1)

    
if __name__ == "__main__":
    main(sys.argv[1:])

