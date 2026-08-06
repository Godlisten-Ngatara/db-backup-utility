import psycopg

host = "localhost"
port = 5432
database = "mydb"
user = "myuser"
password = "mypass"

conn = psycopg.connect(
    host=host, port=port, database=database, user=user, password=password
)
cursor = conn.cursor()
