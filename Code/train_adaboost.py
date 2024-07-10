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
     
    # Description: This code snippet is used to train an AdaBoost classifier with GridSearchCV for hyperparameter tuning.
        # Redis: Yes

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python 3.11.5
            # Scikit-learn 1.5.1
            # Pandas 2.2.2
            # Joblib 1.4.2
            # SHAP 0.46.0

import joblib                                       # For saving the model
# import shap                                       # For SHAP value interpretation
from sklearn.ensemble import AdaBoostClassifier     # For training the model
from sklearn.model_selection import GridSearchCV    # For hyperparameter tuning
from io import StringIO                             # For reading the data string
import pandas as pd                                 # For data manipulation and analysis

# Importing the necessary .py helper files and functions
from db_utils import connect_redis, retrieve_from_redis
from evaluate import evaluate_model

# Note: The dataset consists of 1000 samples, leading to potential overfitting with a high training accuracy.
# This would not occur in real-life scenarios with larger and more varied datasets, providing a more realistic accuracy.

def train_adaboost(data):
    # Drop the 'attrition' column to get the features
    X = data.drop(columns=['attrition'])
    # Get the target variable 'attrition'
    y = data['attrition']
    
    # Initialize the AdaBoost classifier with SAMME algorithm
    model = AdaBoostClassifier(algorithm='SAMME')
    
    # Define the parameter grid for GridSearchCV
    # Here, we tune the number of estimators and learning rate
    param_grid = {'n_estimators': [50, 100, 150], 'learning_rate': [0.01, 0.1, 1]}
    
    # Setup GridSearchCV with accuracy scoring and 5-fold cross-validation
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
    
    # Fit the model to the data
    grid_search.fit(X, y)
    
    # Get the best model from the grid search
    best_model = grid_search.best_estimator_

    # # Explain the model using SHAP for one random data point
    # import numpy as np
    # random_idx = np.random.choice(X.shape[0])  # Choose a random index
    # X_sample = X.iloc[[random_idx]]  # Extract the sample
    # explainer = shap.KernelExplainer(best_model.predict_proba, X_sample)
    # shap_values = explainer.shap_values(X_sample)

    # # Generate SHAP summary plot for the single data point
    # shap.initjs()
    # # Summary plot for the sample's SHAP values
    # shap.summary_plot(shap_values, X_sample, feature_names=X.columns)

    return best_model

def main():
    # Connect to Redis
    redis_conn = connect_redis('localhost', 6379)  # Port specified for Redis
    
    # Retrieve the training data from Redis
    training_data = retrieve_from_redis(redis_conn, 'train')
    
    # Convert the CSV data string to a DataFrame
    data_str = training_data
    data = pd.read_csv(StringIO(data_str))
    
    # Train the AdaBoost model
    model = train_adaboost(data)
    
    # Save the trained model to a file
    joblib.dump(model, 'adaboost_model.pkl')
    
    # Evaluate the model
    evaluate_model('adaboost_model.pkl', 'train')

if __name__ == "__main__":
    main()