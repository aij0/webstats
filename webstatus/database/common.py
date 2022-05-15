import logging


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


def query_cursor(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logging.debug("Query %s executed", query)
    except Exception as err:
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
