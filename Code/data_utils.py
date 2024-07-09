# All the functions for connecting databases in one place

import pandas as pd # For data manipulation
import mysql.connector # For connecting to MariaDB
from elasticsearch import Elasticsearch # For connecting to Elasticsearch
import redis # For connecting to Redis

def connect_mariadb(host, user, password, database=None):
    if database:
        return mysql.connector.connect(host=host, user=user, password=password, database=database)
    else:
        return mysql.connector.connect(host=host, user=user, password=password)

def create_mariadb_database(conn, database):
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    conn.commit()

def create_mariadb_table(conn, table_name, table_schema):
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({table_schema})")
    conn.commit()

def connect_elasticsearch(host, port, user=None, password=None):
    es_url = f"http://{host}:{port}"
    if user and password:
        return Elasticsearch([es_url], http_auth=(user, password))
    return Elasticsearch([es_url])

def create_es_index(es, index_name, index_schema):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_schema)

def connect_redis(host, port):
    return redis.StrictRedis(host=host, port=port, decode_responses=True)

def store_to_mariadb(conn, table_name, df):
    cursor = conn.cursor()
    for i, row in df.iterrows():
        sql = f"REPLACE INTO {table_name} VALUES ({', '.join(['%s'] * len(row))})"
        cursor.execute(sql, tuple(row))
    conn.commit()

def store_to_elasticsearch(es, index_name, df):
    for i, row in df.iterrows():
        es.index(index=index_name, id=row['employee_id'], document=row.to_dict())

def store_to_redis(r, key, data):
    r.set(key, data)

def retrieve_from_redis(r, key):
    return r.get(key)

def remove_from_redis(r, key):
    r.delete(key)
    
def retrieve_from_mariadb(conn, query):
    return pd.read_sql(query, conn)

def retrieve_from_elasticsearch(es, index_name, query):
    return es.search(index=index_name, body=query)

if __name__ == "__main__":
    pass