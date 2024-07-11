# DIY-BoostingAlgorithms

This is the Boosting Algorithms branch.

> **IMP:** This project utilizes the default configurations for MariaDB, MongoDB, and Redis databases.

# Boosting Algorithms

|AdaBoost                          |GBM                         |
|-------------------------------|-----------------------------|
AdaBoost (Adaptive Boosting) enhances weak classifiers by iteratively focusing on misclassified examples and combining them through weighted majority voting. It adjusts sample weights to improve overall accuracy, commonly using algorithms like SAMME or SAMME.R.         |Gradient Boosting Machine (GBM) builds models sequentially, where each new model corrects previous errors by fitting decision trees to the residuals using gradient descent. It optimizes a loss function to improve predictive performance.            |

## Problem Definition

A company aims to enhance its employee retention strategy by predicting employee attrition. By using AdaBoost on the dataset, the HR team can identify patterns and factors contributing to employee turnover. This analysis will help the company proactively address the issues leading to attrition, improve job satisfaction, and implement targeted retention programs. The goal is to maintain a motivated and stable workforce, reducing the costs and disruptions associated with high employee turnover.

## Data Definition

Mock data for learning purposes with features: Employee ID, Age, Years at Company, Monthly Income, Job Satisfaction, Performance Rating,Work Life Balance, Training Hours Last Year, Department, Attrition 

> **Note:** The dataset consists of 1000 samples, leading to potential overfitting with a high training accuracy. This would not occur in real-life scenarios with larger and more varied datasets, providing a more realistic accuracy.

## Directory Structure

- **Code/**: Contains all the scripts for data ingestion, transformation, loading, evaluation, model training, inference, manual prediction, and web application.
- **Data/**: Contains the raw mock data.

### Data Splitting

- **Training Samples**: 600
- **Testing Samples**: 150
- **Validation Samples**: 150
- **Supervalidation Samples**: 100

## Program Flow

1. **`db_utils.py`:** Contains utility functions for database connections and operations.
1. **Data Ingestion:**: Extract data from Data/Master, split it into SQL and NoSQL databases as required. Here, 'department' was categorical and hence stored in MongoDB (NoSQL). 'employee_id' was retained in both the databases as **key** to merge the databases on. [`ingest.py`]
2. **Data Transformation:** The data from MariaDB and MongoDB is transformed (as required), merged on 'employee_id', split into the given ratio, and stored separately in Redis. [`transform.py`]
3. **Model Training** Train models using the training data, perform hyperparameter tuning, and save the best-performing models. [`train_adaboost.py`, `train_gbm.py`]
4. **Model Evaluation:** Evaluate the trained models on the test, validation, and supervalidation datasets. ['model_inference.py`]
5. **Manual Prediction:** Provide a mechanism for users to input data and get predictions from the trained models. [`manual_prediction.py`]
6. **Web Application:** Streamlit app to provide a user-friendly GUI for predictions. [`app.py`]

## Steps to Run

1. Install the necessary packages: `pip install -r requirements.txt`
2. Run the Streamlit web application: `streamlit run Code/app.py`