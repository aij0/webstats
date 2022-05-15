import logging
import sys
from psycopg2 import connect, Error
from database.common import storing_query, fetching_query

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


def create_connection(database):
    connection = None

    try:
        connection = connect(user=database["user"],
                             password=database["password"],
                             address=database["address"],
                             port=database["port"],
                             database=database["name"])
        logging.debug("Connection to %s[%s] ok", database["address"],
                      database["name"])
    except Error as err:
        logging.error("Database error: ", err)

    return connection


def execute_query(database, direction, querystring):
    db_connection = create_connection(database)

    if direction == "push":
        storing_query(db_connection, querystring)
    else:
        return fetching_query(db_connection, querystring)


def setup_database(database):
    try:
        db_connection = create_connection(database)
    except Exception as err:
        logging.error("Can't create database: %s", err)
        sys.exit(3)

    setup_database_in_postgres(db_connection, database)

    return db_connection
