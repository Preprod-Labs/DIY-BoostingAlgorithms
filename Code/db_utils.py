# META DATA - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Developer details: 
        # Name: Mohini T and Vansh R
        # Role: Architects
        # Code ownership rights: Mohini T and Vansh R
    # Version:
        # Version: V 1.0 (11 July 2024)
            # Developers: Mohini T and Vansh R
            # Unit test: Pass
            # Integration test: Pass
     
    # Description: This code snippet is used to create utility functions for connecting to MariaDB, MongoDB, and Redis.
        # MariaDB: Yes
        # MongoDB: Yes
        # Redis: Yes

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python 3.11.5
            # Scikit-learn 1.5.1
            # Pandas 2.2.2

import pandas as pd     # For data manipulation and analysis
import mysql.connector  # For connecting to MariaDB
import pymongo          # For connecting to MongoDB
import redis            # For connecting to Redis

def connect_mariadb(host, user, password, database=None): # For connecting to MariaDB
    if database:
        return mysql.connector.connect(host=host, user=user, password=password, database=database)
    else:
        return mysql.connector.connect(host=host, user=user, password=password)

def create_mariadb_database(conn, database): # For creating a MariaDB database
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    conn.commit()

def create_mariadb_table(conn, table_name, table_schema): # For creating a MariaDB table
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({table_schema})")
    conn.commit()

def connect_mongodb(host, port, database, user=None, password=None): # For connecting to MongoDB
    if user and password:
        mongo_uri = f"mongodb://{user}:{password}@{host}:{port}/"
    else:
        mongo_uri = f"mongodb://{host}:{port}/"
    client = pymongo.MongoClient(mongo_uri)
    return client[database]

def create_mongodb_collection(db, collection_name): # For creating a MongoDB collection
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
    return db[collection_name]

def connect_redis(host, port): # For connecting to Redis
    return redis.StrictRedis(host=host, port=port, decode_responses=True)

def create_redis_keyspace(r, key): # For creating a Redis keyspace
    if not r.exists(key):
        r.set(key, "")

def store_to_mariadb(conn, table_name, df): # For storing data to MariaDB
    cursor = conn.cursor()
    for i, row in df.iterrows():
        sql = f"REPLACE INTO {table_name} VALUES ({', '.join(['%s'] * len(row))})"
        cursor.execute(sql, tuple(row))
    conn.commit()

def store_to_mongodb(collection, df): # For storing data to MongoDB
    records = df.to_dict(orient='records')
    collection.insert_many(records)

def store_to_redis(r, key, data): # For storing data to Redis
    r.set(key, data)

def retrieve_from_redis(r, key): # For retrieving data from Redis
    return r.get(key)

def remove_from_redis(r, key): # For removing data from Redis
    r.delete(key)

def retrieve_from_mariadb(conn, query): # For retrieving data from MariaDB
    return pd.read_sql(query, conn)

def retrieve_from_mongodb(collection, query): # For retrieving data from MongoDB
    cursor = collection.find(query)
    return pd.DataFrame(list(cursor))

if __name__ == "__main__":
    pass
