# To split and ingest mock data into MariaDB and Elasticsearch

import pandas as pd # For data manipulation

# Importing the necessary .py helper files and functions
from data_utils import (
    connect_mariadb,
    connect_elasticsearch,
    store_to_mariadb, store_to_elasticsearch,
    create_mariadb_database,
    create_mariadb_table,
    create_es_index
)

def ingest_data(csv_path, mariadb_config, es_config):
    data = pd.read_csv(csv_path)
    
    # Separate data for MariaDB and Elasticsearch
    mariadb_data = data[['employee_id', 'age', 'years_at_company', 'monthly_income', 
                         'job_satisfaction', 'performance_rating', 'work_life_balance', 
                         'training_hours_last_year', 'attrition']]
    
    es_data = data[['employee_id', 'department']]
    
    # Connect to MariaDB and create database and table if they don't exist
    mariadb_conn = connect_mariadb(mariadb_config['host'], mariadb_config['user'], mariadb_config['password'])
    create_mariadb_database(mariadb_conn, mariadb_config['database'])
    
    mariadb_conn = connect_mariadb(mariadb_config['host'], mariadb_config['user'], mariadb_config['password'], mariadb_config['database'])
    table_schema = """
        employee_id INT PRIMARY KEY,
        age INT,
        years_at_company INT,
        monthly_income FLOAT,
        job_satisfaction INT,
        performance_rating INT,
        work_life_balance INT,
        training_hours_last_year INT,
        attrition BOOLEAN
    """
    create_mariadb_table(mariadb_conn, 'employees', table_schema)
    store_to_mariadb(mariadb_conn, 'employees', mariadb_data)
    
    # Store data in Elasticsearch
    es = connect_elasticsearch(es_config['host'], es_config['port'], es_config['user'], es_config['password'])
    index_schema = {
        "mappings": {
            "properties": {
                "employee_id": {"type": "integer"},
                "department": {"type": "text"}
            }
        }
    }
    create_es_index(es, 'employees', index_schema)
    store_to_elasticsearch(es, 'employees', es_data)
    
if __name__ == "__main__":
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
    csv_path = 'Data/Master/mock_data.csv'
    ingest_data(csv_path, mariadb_config, es_config)