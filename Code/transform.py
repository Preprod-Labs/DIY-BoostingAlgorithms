# Note: This code contains lots of measures to check where the the data went wrong

# To transform and merge data from MariaDB and Elasticsearch to Redis

import pandas as pd # For data manipulation
from sklearn.preprocessing import LabelEncoder # For encoding categorical data

# Importing the necessary .py helper files and functions
from data_utils import (
    connect_mariadb,
    connect_elasticsearch,
    connect_redis,
    store_to_redis,
    retrieve_from_mariadb,
    retrieve_from_elasticsearch,
    store_to_elasticsearch
)

def transform_data(mariadb_data, es_data):
    # Check for any missing values in the 'department' column
    if es_data['department'].isnull().any():
        raise ValueError("Missing values detected in 'department' column of Elasticsearch data.")

    # Encode 'department' feature from Elasticsearch to numerical values using LabelEncoder
    le = LabelEncoder()
    es_data['department'] = le.fit_transform(es_data['department'])

    # Show the department encoding
    department_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    print("Department Encoding Map:")
    for dept, code in department_mapping.items():
        print(f"{dept}: {int(code)}")  # Convert np.int64 to int for clarity

    # Normalize 'monthly_income' in MariaDB data
    mariadb_data['monthly_income'] = (mariadb_data['monthly_income'] - mariadb_data['monthly_income'].mean()) / mariadb_data['monthly_income'].std()

    return mariadb_data, es_data, le

def merge_data(mariadb_data, es_data):
    return pd.merge(mariadb_data, es_data, on='employee_id', how='outer')

def main(mariadb_config, es_config, redis_config):
    # Connect to MariaDB
    mariadb_conn = connect_mariadb(mariadb_config['host'], mariadb_config['user'], mariadb_config['password'], mariadb_config['database'])

    # Connect to Elasticsearch
    es = connect_elasticsearch(es_config['host'], es_config['port'], es_config['user'], es_config['password'])

    # Connect to Redis
    r = connect_redis(redis_config['host'], redis_config['port'])

    # Retrieve data from MariaDB
    mariadb_data = retrieve_from_mariadb(mariadb_conn, "SELECT * FROM employees")

    # Retrieve data from Elasticsearch
    es_query = {"query": {"match_all": {}}}
    es_response = retrieve_from_elasticsearch(es, 'employees', es_query)
    es_data = pd.DataFrame([doc['_source'] for doc in es_response['hits']['hits']])

    # Perform data transformation
    transformed_mariadb_data, transformed_es_data, le = transform_data(mariadb_data, es_data)

    # Store the transformed Elasticsearch data back to Elasticsearch
    store_to_elasticsearch(es, 'employees', transformed_es_data)

    # Retrieve the data again from Elasticsearch to ensure consistency
    es_response = retrieve_from_elasticsearch(es, 'employees', es_query)
    transformed_es_data = pd.DataFrame([doc['_source'] for doc in es_response['hits']['hits']])

    # Merge the transformed data from MariaDB and Elasticsearch
    merged_data = merge_data(transformed_mariadb_data, transformed_es_data)

    # Check the merged data size
    print(f"Merged Data Size: {merged_data.shape[0]} rows")

    # Check for any missing values
    print(f"Missing values in merged data:\n{merged_data.isnull().sum()}")

    # Store the merged data into Redis
    # Convert DataFrame to JSON string before storing in Redis
    store_to_redis(r, 'merged_data', merged_data.to_json(orient='records'))  # Ensure correct JSON format

if __name__ == "__main__":
    # Define configurations for MariaDB, Elasticsearch, and Redis
    mariadb_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'preprod'
    }
    es_config = {
        'host': 'localhost',
        'port': 9200,
        'user': 'elastic',      # Add your own Elasticsearch username
        'password': 'password'  # Add your own Elasticsearch password
    }
    redis_config = {
        'host': 'localhost',
        'port': 6379
    }
    main(mariadb_config, es_config, redis_config)