import logging
from sqlite3 import Error, connect

create_servers_table = """
CREATE TABLE IF NOT EXISTS servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL
);
"""

create_stats_table = """
CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    return_code INTEGER,
    content_found INTEGER(1),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    server_id INTEGER NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers (id)
)
"""


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
