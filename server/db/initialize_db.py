# Initalizes the database tables and seeds
from credentials import db_name, user, pw, db_url
from sql.tables import tables
import psycopg2 as pg
import sys

def initTableIfDoesntExist(conn, table_name, attributes):
    # Create
    command = f"""
    CREATE TABLE IF NOT EXISTS {table_name}(
    """
    command += attributes
    
    command += """)"""

    try:
        # Create cursor to db
        cur = conn.cursor()

        cur.execute(command)

        cur.close()

        conn.commit()
        
    except:
        e = sys.exc_info()[0]
        print(f"Error adding table{table_name}: {e}")

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

def resetDB(conn, tables):
    table_names = tables.keys()

    # First we remove any table that was already there
    for table in table_names:
        dropTableIfExists(conn, table)
    
    # Now we create the tables again
    for table in table_names:
        print("attrs", table, tables.get(table))
        initTableIfDoesntExist(conn, table, tables.get(table))
    


if __name__ == "__main__":
    conn = pg.connect(host=db_url, database=db_name, user=user, password=pw)

    #initTableIfDoesntExist(conn, 'parking_spots', tables['parking_spots'])
    #dropTableIfExists(conn, 'parking_spots')
    resetDB(conn, tables)

    conn.close()
    pass