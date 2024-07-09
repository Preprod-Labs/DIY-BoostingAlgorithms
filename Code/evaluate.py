# Have not tested the corectness of this file yet

# To evaluate the model using any of the datasets

import pandas as pd # For data manipulation
from sklearn.metrics import accuracy_score, classification_report # For model evaluation

# Importing the necessary .py helper files and functions
from data_utils import connect_redis, retrieve_from_redis

def evaluate_model(model_path, data_key):
    # Connect to Redis
    r = connect_redis('localhost', 6379)  # Hardcoded for simplicity; can be passed as an argument
    
    # Retrieve data from Redis
    data_str = retrieve_from_redis(r, data_key)
    data = pd.read_json(data_str)
    
    # Extract features and labels
    X = data.drop(columns=['attrition'])
    y = data['attrition']
    
    # Load the model
    import joblib
    model = joblib.load(model_path)
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Print accuracy and classification report
    print(f"Evaluation on {data_key}:")
    print(f"Accuracy: {accuracy_score(y, y_pred)}")
    print("Classification Report:")
    print(classification_report(y, y_pred))

if __name__ == "__main__":
    pass