# Initalizes the database tables and seeds
from credentials import db_name, user, pw, db_url
import psycopg2 as pg

def initTableIfDoesntExist(conn, table_name):

    # Create cursor to db
    cur = conn.cursor()

    # Create
    command = f"""
    CREATE TABLE IF NOT EXISTS {table_name}(
    ID SERIAL PRIMARY KEY,
    ADDRESS VARCHAR(255),
    OCCUPIED BOOLEAN
    )
    """

    print(command)


if __name__ == "__main__":
    conn = pg.connect(host=db_url, database=db_name, user=user, password=pw)
    initTableIfDoesntExist(conn, 'parking_spots')
    pass