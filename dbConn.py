def connect_to_db(driver, conn_params):
    if driver == "mysql":
        import mysql.connector

        return mysql.connector.connect(**conn_params)
    elif driver == "postgresql":
        import psycopg

        return psycopg.connect(**conn_params)
    else:
        raise ValueError("Unsupported database driver: {}".format(driver))
