parking_spot_attrs = """
    ID SERIAL PRIMARY KEY,
    LICENCE CHAR(7) DEFAULT NULL,
    ADDRESS VARCHAR(255),
    URBAN BOOLEAN DEFAULT TRUE
"""

person_attrs = """
    ID SERIAL PRIMARY KEY,
    VEHICLE CHAR(7),
    GENDER VARCHAR(31) DEFAULT 'male',
    DOB DATE,
    INSURANCE_PROVIDER INTEGER,
    INSURANCE_NUM INTEGER
"""

vehicle_attrs = """
    LICENSE CHAR(7) PRIMARY KEY,
    OWNER INTEGER,
    TYPE VARCHAR(127) DEFAULT 'sedan',
    RENTAL BOOLEAN DEFAULT FALSE,
    MODEL VARCHAR(127),
    MODEL_YEAR INTEGER,
    PRIVATE BOOLEAN DEFAULT TRUE
"""
parking_session_attrs = """
    ID SERIAL PRIMARY KEY,
    LICENSE CHAR(7),
    PARKING_ID INTEGER,
    START_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    END_TIME TIMESTAMP
"""
insurance_attrs = """
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(255)
"""

tables = {
    "parking_spots": parking_spot_attrs,
    "person": person_attrs,
    "vehicles": vehicle_attrs,
    "parking_sessions": parking_session_attrs,
    "insurance": insurance_attrs
}