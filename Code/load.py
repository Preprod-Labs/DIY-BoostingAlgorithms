# To fetch merged data from Redis, split it in the given ratio, and store the split data back into Redis

import pandas as pd # For data manipulation
from sklearn.model_selection import train_test_split # For splitting the data

# Importing the necessary .py helper files and functions
from data_utils import connect_redis, store_to_redis, retrieve_from_redis

def split_data(data):
    # Split the data into training (600) and remaining data
    train_data, temp_data = train_test_split(data, train_size=600, random_state=42)
    
    # Split the remaining data into testing (150) and remaining data
    test_data, temp_data = train_test_split(temp_data, test_size=150, random_state=42)
    
    # Split the remaining data into validation (150) and supervalidation (100)
    validation_data, supervalidation_data = train_test_split(temp_data, test_size=100, random_state=42)
    
    return train_data, test_data, validation_data, supervalidation_data

def main(redis_config):
    # Connect to Redis
    r = connect_redis(redis_config['host'], redis_config['port'])
    
    # Retrieve the merged data from Redis
    merged_data = pd.read_json(retrieve_from_redis(r, 'merged_data'))
    
    # Split the data
    train_data, test_data, validation_data, supervalidation_data = split_data(merged_data)
    
    # Store the split data into Redis
    store_to_redis(r, 'train_data', train_data.to_json())
    store_to_redis(r, 'test_data', test_data.to_json())
    store_to_redis(r, 'validation_data', validation_data.to_json())
    store_to_redis(r, 'supervalidation_data', supervalidation_data.to_json())

if __name__ == "__main__":
    # Define configurations for Redis
    redis_config = {
        'host': 'localhost',
        'port': 6379
    }
    main(redis_config)
