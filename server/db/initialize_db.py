# Initalizes the database tables and seeds
from db.credentials import db_name, user, pw, db_url
from db.sql.tables import tables
import psycopg2 as pg
import sys
from faker import Faker
fake = Faker()

# Send in connection, table, and a list of column names and values to set
def insertIntoTable(conn, table_name, insertList):
    columns, values = zip(*insertList)

    columns=",".join(str(col) for col in columns)
    values=",".join(f"""'{val}'""" for val in values)

    command = f"""
        INSERT INTO {table_name}({columns})
        VALUES
        ({values})
    """

    try:
        cur = conn.cursor()
        print(command)
        cur.execute(command)
        cur.close()

        conn.commit()
    except:   
        e = sys.exc_info()[0]
        print(f"Error adding table{table_name}: {e}")

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

def seed(conn, tables):
    licensePlates = ['A1B2C3','D4E7H0','Z6P9Y8']
    phoneNumbers = ['+15147425793', '+14389376453', '+15148021867']

    try:
        # seed parking spots
        for i in range(3):
            insertIntoTable(conn,'parking_spots', [('address',fake.address())])
            insertIntoTable(conn, 'person',[('name', fake.name()),('vehicle',licensePlates[i]),('gender','male'),('dob','1997-03-22'),('phone_num',phoneNumbers[i])])
            insertIntoTable(conn, 'vehicles',[('license',licensePlates[i]),('owner',i+1),('type','sedan'),('model','AE3'),('model_year','2008')])   

    except:
        e = sys.exc_info()[0]
        print(f"Error adding table{tables}: {e}")

if __name__ == "__main__":
    conn = pg.connect(host=db_url, database=db_name, user=user, password=pw)

    resetDB(conn, tables)
    seed(conn,tables)
    #insertIntoTable(conn, 'person', [('insurance_num', '2')])

    conn.close()
    pass