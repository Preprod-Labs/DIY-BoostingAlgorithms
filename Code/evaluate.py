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
     
    # Description: This code snippet is used to evaluate the model using the data stored in Redis and print
    # the classification report.
        # Redis: Yes

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python 3.11.5
            # Scikit-learn 1.5.1
            # Pandas 2.2.2

from sklearn.metrics import accuracy_score, classification_report   # For model evaluation

# Importing the necessary .py helper files and functions
from db_utils import connect_redis, retrieve_from_redis

def evaluate_model(model_path, data_key):
    # Connect to Redis
    r = connect_redis('localhost', 6379)  # Hardcoded for simplicity; can be passed as an argument
    
    # Retrieve data from Redis
    data_str = retrieve_from_redis(r, data_key)
    
    # Convert the string data to a DataFrame
    from io import StringIO
    import pandas as pd
    data = pd.read_csv(StringIO(data_str))
    
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