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
     
    # Description: This code snippet is used to ingest data from MariaDB, MongoDB, and Redis.
        # MariaDB: Yes
        # MongoDB: Yes

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python 3.11.5
            # Pandas 2.2.2

import pandas as pd # For data manipulation and analysis

# Importing the necessary .py helper files and functions
from db_utils import (
    connect_mariadb,
    connect_mongodb,
    store_to_mariadb, 
    store_to_mongodb,
    create_mariadb_database,
    create_mariadb_table,
    create_mongodb_collection
)

def ingest_data(csv_path, mariadb_config, mongodb_config):
    # Load the data from the CSV file
    data = pd.read_csv(csv_path)
    
    # Separate data for MariaDB and MongoDB
    mariadb_data = data[['employee_id', 'age', 'years_at_company', 'monthly_income', 
                         'job_satisfaction', 'performance_rating', 'work_life_balance', 
                         'training_hours_last_year', 'attrition']]
    
    mongodb_data = data[['employee_id', 'department']]
    
    # Connect to MariaDB and create database and table if they don't exist
    mariadb_conn = connect_mariadb(mariadb_config['host'], mariadb_config['user'], mariadb_config['password'])
    create_mariadb_database(mariadb_conn, mariadb_config['database'])
    
    # Connect to MariaDB and create table if it doesn't exist
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
    
    # Connect to MongoDB and create collection if it doesn't exist
    mongodb_db = connect_mongodb(mongodb_config['host'], mongodb_config['port'], mongodb_config['database'])
    mongodb_collection = create_mongodb_collection(mongodb_db, 'employees')
    store_to_mongodb(mongodb_collection, mongodb_data)
    
if __name__ == "__main__":
    # Configuration for MariaDB and MongoDB
    mariadb_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'preprod'
    }
    mongodb_config = {
        'host': 'localhost',
        'port': 27017,
        'database': 'preprod'
    }
    csv_path = 'Data/Master/mock_data.csv'
    ingest_data(csv_path, mariadb_config, mongodb_config)