import logging
from sqlite3 import Error, connect
import sys

create_servers_table = """
CREATE TABLE IF NOT EXISTS servers (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    UNIQUE(name)
);
"""

create_stats_table = """
CREATE TABLE IF NOT EXISTS stats (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    return_code INTEGER,
    content_found INTEGER(1),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    server_id INTEGER NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers (id)
)
"""


def create_server_insert_query(server, address):
    fullquery = f"""INSERT OR IGNORE INTO servers (name, address)
     VALUES ('{server}', '{address}');"""
    logging.debug("server insert query: %s", fullquery)
    return fullquery


def create_connection(path):
    connection = None
    try:
        connection = connect(path)
        logging.debug("Connection to %s ok", path)
    except Error as err:
        logging.error("Database error: ", err)

    return connection


def query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logging.debug("Query %s executed", query)
    except Error as err:
        logging.error("Query error: %s", err)
        return False
    return True


def setup_database(config):
    try:
        db_connection = create_connection("local.sqlite")
    except Exception as err:
        logging.error("Can't create local database: %s", err)
        sys.exit(3)

    try:
        query(db_connection, create_servers_table)
        logging.debug("Query %s succeeded", create_servers_table)
    except Exception as err:
        logging.error("Query failed with %s", err)

    try:
        query(db_connection, create_stats_table)
        logging.debug("Query %s succeeded", create_stats_table)
    except Exception as err:
        logging.error("Query failed with %s", err)

    return db_connection
