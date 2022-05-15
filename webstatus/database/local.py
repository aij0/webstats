import logging
import sys
from sqlite3 import Error, connect
from database.common import storing_query, fetching_query


class SqliteDatabase:

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

    def setup_database_in_sqlite(self, db_connection, database):
        try:
            storing_query(db_connection, self.create_sqlite_servers_table)
            logging.debug("Query %s succeeded",
                          self.create_sqlite_servers_table)
        except Exception as err:
            logging.error("Query failed with %s", err)

        try:
            db_connection = self.create_connection(database)
            storing_query(db_connection,
                          self.create_sqlite_stats_table)
            logging.debug("Query %s succeeded",
                          self.create_sqlite_stats_table)
        except Exception as err:
            logging.error("Query failed with %s", err)

    def create_connection(self, database):
        connection = None
        try:
            connection = connect(database["name"])
            logging.debug("Connection to %s ok", database["name"])
        except Error as err:
            logging.error("Database error: ", err)
        return connection

    def execute_query(self, database, direction, querystring):
        db_connection = self.create_connection(database)

        if direction == "push":
            storing_query(db_connection, querystring)
        else:
            return fetching_query(db_connection, querystring)

    def setup_database(self, database):
        try:
            db_connection = self.create_connection(database)
        except Exception as err:
            logging.error("Can't create database: %s", err)
            sys.exit(3)

        self.setup_database_in_sqlite(db_connection, database)

        return db_connection
