from .credentials import db_name, user, pw, db_url
from .sql.tables import tables
from .initialize_db import insertIntoTable
import psycopg2 as pg
import sys

def getTableByRow(conn, table, pk):
    command = f"""
        SELECT *
        FROM {table}
        WHERE {pk[0]}={pk[1]}
    """
    try:
        cur = conn.cursor()
        cur.execute(command)
        res = cur.fetchone()
        cur.close()
        conn.commit()

        return res
    except:
        e = sys.exc_info()[0]
        print(f"{e}")

def getTableValueByName(conn, table, attr, pk):
    command = f"""
        SELECT {attr}
        FROM {table}
        WHERE {pk[0]}='{pk[1]}'
    """
    try:
        cur = conn.cursor()
        cur.execute(command)
        res = cur.fetchone()
        cur.close()
        conn.commit()

        return res[0]
    except:
        e = sys.exc_info()[0]
        print(f"{e}")

def updateTable(conn, table, updateList, whereId):
    command = f"""
        UPDATE {table}
    """

    for col, val in updateList:

        command += f"""
        SET {col}={val}"""
    command+=f"""
        WHERE {whereId[0]} = {whereId[1]}"""

    try:
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
    except:
        e = sys.exc_info()[0]
        print(f"{e}")

def newParkingSession(conn, license, parkingId):
    insertIntoTable(conn, 'parking_sessions', [('license', license),('parking_id',parkingId)])

    sessionId = getLatestPk(conn, 'parking_sessions')

    updateTable(conn, 'parking_spots',[('session_id',sessionId)],('id',parkingId))

    conn.commit()

def updateParkingSpot(conn, license, parkingId):
    try:
        getCurrentOccupancy = f"""
            SELECT license, end_time
            FROM parking_sessions
            WHERE id IN (
                SELECT session_id
                FROM parking_spots
                WHERE id = {parkingId}
            )
        """

        cur = conn.cursor()
        cur.execute(getCurrentOccupancy)

        res = cur.fetchone()
        print('res', res)
        cur.close()

        # If there was no car at that position
        if res is None:
            # This means there is a new car at the position
            if license is not None:
                # start new parking session
                newParkingSession(conn, license, parkingId)
                
        # Means there was a car there
        else:
            if license is not None:
                licenseInDB = res[0]
                end_time = res[1]

                # This means that there's been a new car that's come since last time
                if not license == licenseInDB:
                    currentSessionId = getTableValueByName(conn, 'parking_spots','session_id',('id', parkingId))
                    # end the current session
                    updateTable(conn, 'parking_sessions', [('end_time','CURRENT_TIMESTAMP')],('id',parkingId))
                    # Start new session for this new license
                    newParkingSession(conn, license, parkingId)

                    # Now we return the user info of the person that just left
                    return (getTableValueByName(conn, 'vehicles', 'owner',('license', licenseInDB)), currentSessionId)

                # If not then we have the same car there so don't do anything]
            # Here it means no license plate so the car just left
            else:
                currentSessionId = getTableValueByName(conn, 'parking_spots','session_id',('id', parkingId))
                print('yello',currentSessionId)
                updateTable(conn, 'parking_spots', [('session_id','NULL')],('id',parkingId))
                print('hello')
                # end the session
                updateTable(conn, 'parking_sessions',[('end_time','CURRENT_TIMESTAMP')],('id',currentSessionId))
                print('allo')
                print(getTableValueByName(conn, 'vehicles', 'owner',('license', res[0])))
                # Now we return the user info of the person that just left
                return (getTableValueByName(conn, 'vehicles', 'owner',('license', res[0])), currentSessionId)

        conn.commit()
    except:
        e = sys.exc_info()[0]
        print(f"{e}")

def getLatestPk(conn, table, pk='id'):
    command = f"""
        SELECT MAX({pk})
        FROM {table}
    """

    cur = conn.cursor()
    cur.execute(command)
    res = cur.fetchone()
    cur.close()

    return res[0]

if __name__ == "__main__":
    conn = pg.connect(host=db_url, database=db_name, user=user, password=pw)

    updateParkingSpot(conn, None, 1)

    conn.close()