import logging
import psycopg2
from sqlite3 import Error, connect
import sys

create_sqlite_servers_table = """
CREATE TABLE IF NOT EXISTS servers (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    UNIQUE(name)
);
"""

create_sqlite_stats_table = """
CREATE TABLE IF NOT EXISTS stats (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    return_code INTEGER,
    content_found INTEGER(1),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    server_id INTEGER NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers (id)
)
"""

create_postgres_servers_table = """
CREATE TABLE IF NOT EXISTS servers (
    ID SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    UNIQUE(name)
);
"""

create_postgres_stats_table = """
CREATE TABLE IF NOT EXISTS stats (
    ID SERIAL PRIMARY KEY,
    return_code INTEGER,
    content_found BOOLEAN,
    timestamp TIMESTAMP,
    server_id INTEGER NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers (id)
)
"""


def create_server_insert_query(type, server, address):
    if type == "postgres":
        fullquery = f"""INSERT INTO servers (name, address)
        VALUES ('{server}', '{address}') ON CONFLICT (name) DO NOTHING;"""
    else:
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


def create_connection(database):
    connection = None
    if database["type"] == "postgres":
        try:
            connection = psycopg2.connect(user=database["user"],
                                          password=database["password"],
                                          host=database["host"],
                                          port=database["port"],
                                          database=database["name"])
            logging.debug("Connection to %s[%s] ok", database["host"],
                          database["name"])
        except Error as err:
            logging.error("Database error: ", err)
    else:
        try:
            connection = connect(database["name"])
            logging.debug("Connection to %s ok", database["name"])
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


def setup_database_in_sqlite(db_connection, database):
    try:
        storing_query(db_connection, create_sqlite_servers_table)
        logging.debug("Query %s succeeded", create_sqlite_servers_table)
    except Exception as err:
        logging.error("Query failed with %s", err)

    try:
        db_connection = create_connection(database)
        storing_query(db_connection, create_sqlite_stats_table)
        logging.debug("Query %s succeeded", create_sqlite_stats_table)
    except Exception as err:
        logging.error("Query failed with %s", err)


def setup_database_in_postgres(db_connection, database):
    try:
        storing_query(db_connection, create_postgres_servers_table)
        logging.debug("Query %s succeeded", create_postgres_servers_table)
    except Exception as err:
        logging.error("Query failed with %s", err)

    try:
        db_connection = create_connection(database)
        storing_query(db_connection, create_postgres_stats_table)
        logging.debug("Query %s succeeded", create_postgres_stats_table)
    except Exception as err:
        logging.error("Query failed with %s", err)


def setup_database(database):
    try:
        db_connection = create_connection(database)
    except Exception as err:
        logging.error("Can't create database: %s", err)
        sys.exit(3)

    if database["type"] == "postgres":
        setup_database_in_postgres(db_connection, database)
    else:
        setup_database_in_sqlite(db_connection, database)

    return db_connection
