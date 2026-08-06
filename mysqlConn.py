import mysql.connector


def connect_to_mysql():
    host = "localhost"
    port = 3306
    database = "mydb"
    user = "myuser"
    password = "mypass"
    return mysql.connector.connect(
        host=host, port=port, database=database, user=user, password=password
    )


cursor = connect_to_mysql().cursor()
