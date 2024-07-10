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
     
    # Description: This code snippet is used to evaluate the model on testing, validation, and supervalidation datasets.
        # Redis: Yes

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python 3.11.5
            # Joblib 1.4.2
            # Pandas 2.2.2

import joblib # For loading the pre-trained model

# Importing the necessary .py helper files and functions
from db_utils import connect_redis, retrieve_from_redis
from evaluate import evaluate_model

def model_inference(model_path):
    # Connect to Redis
    redis_conn = connect_redis('localhost', 6379)  # Port specified for Redis
    
    # Retrieve the datasets from Redis
    test_data = retrieve_from_redis(redis_conn, 'test')
    val_data = retrieve_from_redis(redis_conn, 'validation')
    superval_data = retrieve_from_redis(redis_conn, 'supervalidation')
    
    # Here, 'io' and 'pandas' are imported within the function for better encapsulation
    # Convert the CSV data strings to DataFrames
    from io import StringIO # For reading the data string
    import pandas as pd # For data manipulation and analysis
    test_df = pd.read_csv(StringIO(test_data))
    val_df = pd.read_csv(StringIO(val_data))
    superval_df = pd.read_csv(StringIO(superval_data))
    
    # Evaluate the model on each dataset
    print("Evaluation on Testing Data:")
    evaluate_model(model_path, 'test')
    
    print("\nEvaluation on Validation Data:")
    evaluate_model(model_path, 'validation')
    
    print("\nEvaluation on Supervalidation Data:")
    evaluate_model(model_path, 'supervalidation')

if __name__ == "__main__":
    model_inference('adaboost_model.pkl')