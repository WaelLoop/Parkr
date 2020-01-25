# Initalizes the database tables and seeds
from credentials import db_name, user, pw, db_url
from sql.tables import tables
import psycopg2 as pg

def initTableIfDoesntExist(conn, table_name, attributes):
    # Create
    command = f"""
    CREATE TABLE IF NOT EXISTS {table_name}(
    """
    command += attributes
    
    command += """)"""

    print(command)
    try:
        # Create cursor to db
        cur = conn.cursor()

        cur.execute(command)

        cur.close()

        conn.commit()
        
    except:
        print(f"Error added table{table_name}")

def dropTableIfExists(conn, table_name):
    command = f"""
    DROP TABLE IF EXISTS {table_name} CASCADE
    """

    try:
        cur = conn.cursor()

        cur.execute(command)

        cur.close()

        conn.commit()
    except:
        print(f"Error deleting table {table_name}")


if __name__ == "__main__":
    conn = pg.connect(host=db_url, database=db_name, user=user, password=pw)

    initTableIfDoesntExist(conn, 'parking_spots', tables['parking_spots'])
    #dropTableIfExists(conn, 'parking_spots')

    conn.close()
    pass