import json
from datetime import datetime
from decimal import Decimal
from sqlalchemy import create_engine
from config import settings

def connect_to_db():
    """Connects to DB server using mssql and pymssql"""
    driver = 'SQL Server Native Client 11.0' # Can change to other drivers
    user = settings.database_username
    db = settings.database_name
    server = settings.database_host
    password = settings.database_password
    connection_string = f'mssql+pymssql://{user}:{password}@{server}/{db}'
    engine = create_engine(connection_string)
    connection = engine.connect()
    dbapi_connection = connection.connection
    cursor = dbapi_connection.cursor()
    return cursor


def get_data(query:str) -> list[dict]:
    """Executes a query agains the DB and return results in a list of dictionaries"""
    cursor = connect_to_db()
    cursor.execute(query)
    results = []
    """This loop will handle datetime stamps and decimal serialization.
        IMPORTANT: This is transforming Decimal to String. 
        You may change it to integers or floats if you need to.
    """
    for row in cursor.fetchall():
        result = {}
        for i, column in enumerate(cursor.description):
            if isinstance(row[i], datetime):
                result[column[0]] = row[i].strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(row[i], Decimal):
                result[column[0]] = str(row[i])
            else:
                result[column[0]] = row[i]
        results.append(result)
    return results # If JSON is needed change to json.dumps(result)




