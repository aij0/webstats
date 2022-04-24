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


def create_status_insert_query(return_code, content_found, server_id):
    fullquery = f"""INSERT INTO stats
     (return_code, content_found, server_id)
      VALUES ('{return_code}', '{content_found}', '{server_id}');"""
    logging.debug("status insert query: %s", fullquery)
    return fullquery


def create_connection(path):
    connection = None
    try:
        connection = connect(path)
        logging.debug("Connection to %s ok", path)
    except Error as err:
        logging.error("Database error: ", err)

    return connection


def query_cursor(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logging.debug("Query %s executed", query)
    except Error as err:
        logging.error("Query error: %s", err)
        connection.close()
        return False

    return cursor, connection


def storing_query(connection, query):
    cursor, connection = query_cursor(connection, query)
    connection.close()
    return True


def fetching_query(connection, query):
    cursor, connection = query_cursor(connection, query)
    response = cursor.fetchone()
    connection.close()
    return response


def execute_query(database, direction, querystring):
    db_connection = create_connection(database)
    if direction == "push":
        storing_query(db_connection, querystring)
    else:
        return fetching_query(db_connection, querystring)


def setup_database(config):
    db = "local.sqlite"
    try:
        db_connection = create_connection(db)
    except Exception as err:
        logging.error("Can't create local database: %s", err)
        sys.exit(3)

    try:
        storing_query(db_connection, create_servers_table)
        logging.debug("Query %s succeeded", create_servers_table)
    except Exception as err:
        logging.error("Query failed with %s", err)

    try:
        db_connection = create_connection(db)
        storing_query(db_connection, create_stats_table)
        logging.debug("Query %s succeeded", create_stats_table)
    except Exception as err:
        logging.error("Query failed with %s", err)

    return db_connection
