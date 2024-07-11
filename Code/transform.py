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
     
    # Description: This code snippet is used to transform and merge data from MariaDB and Elasticsearch to Redis.
        # MariaDB: Yes
        # MongoDB: Yes
        # Redis: Yes

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python 3.11.5
            # Pandas 2.2.2
            # Scikit-learn 1.5.1

import pandas as pd                             # For data manipulation and analysis
from sklearn.preprocessing import LabelEncoder  # For encoding categorical features, here, 'department'

# Importing the necessary .py helper files and functions
from db_utils import (
    connect_mariadb, 
    connect_mongodb, 
    retrieve_from_mariadb, 
    retrieve_from_mongodb, 
    store_to_redis, 
    create_mariadb_database,
    create_mariadb_table,
    create_mongodb_collection,
    connect_redis,
    create_redis_keyspace
)

def transform_department_feature(df):
    # Encode the 'department' feature into numerical values
    le = LabelEncoder()
    df['department'] = le.fit_transform(df['department'])
    return df

def merge_data(mariadb_df, mongodb_df):
    # Merge the MariaDB and MongoDB dataframes on 'employee_id'
    return pd.merge(mariadb_df, mongodb_df, on='employee_id')

def split_data(df, train_size=600, test_size=150, validation_size=150, supervalidation_size=100):
    # Split the data into training, testing, validation, and supervalidation datasets
    train = df.iloc[:train_size]
    test = df.iloc[train_size:train_size+test_size]
    validation = df.iloc[train_size+test_size:train_size+test_size+validation_size]
    supervalidation = df.iloc[train_size+test_size+validation_size:train_size+test_size+validation_size+supervalidation_size]
    return train, test, validation, supervalidation

def store_datasets_to_redis(redis_conn, datasets, dataset_names):
    # Stores datasets in Redis
    for dataset, name in zip(datasets, dataset_names):
        # Drop 'employee_id' before saving
        dataset = dataset.drop(columns=['employee_id'])
        # Store dataset as a CSV string in Redis
        store_to_redis(redis_conn, name, dataset.to_csv(index=False))
        print(f"Dataset '{name}' saved to Redis.")

def transform(mariadb_config, mongodb_config, redis_config):
    # Connect to databases
    mariadb_conn = connect_mariadb(mariadb_config['host'], mariadb_config['user'], mariadb_config['password'])
    create_mariadb_database(mariadb_conn, mariadb_config['database'])
    mariadb_conn = connect_mariadb(mariadb_config['host'], mariadb_config['user'], mariadb_config['password'], mariadb_config['database'])
    
    # Ensure MariaDB table exists
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
    
    mongodb_db = connect_mongodb(mongodb_config['host'], mongodb_config['port'], mongodb_config['database'])
    mongodb_collection = create_mongodb_collection(mongodb_db, 'employees')
    
    redis_conn = connect_redis(redis_config['host'], redis_config['port'])
    
    # Retrieve data from databases
    mariadb_df = retrieve_from_mariadb(mariadb_conn, 'SELECT * FROM employees')
    mongodb_df = retrieve_from_mongodb(mongodb_collection, {})
    
    # Drop the '_id' column from MongoDB data
    if '_id' in mongodb_df.columns:
        mongodb_df.drop(columns=['_id'], inplace=True)

    # Transform MongoDB data
    mongodb_df = transform_department_feature(mongodb_df)
    
    # Merge data
    merged_df = merge_data(mariadb_df, mongodb_df)

    # Split data
    train, test, validation, supervalidation = split_data(merged_df)
    
    # Ensure Redis keyspace exists
    dataset_names = ['train', 'test', 'validation', 'supervalidation']
    for name in dataset_names:
        create_redis_keyspace(redis_conn, name)
    
    # Store datasets to Redis
    datasets = [train, test, validation, supervalidation]
    store_datasets_to_redis(redis_conn, datasets, dataset_names)