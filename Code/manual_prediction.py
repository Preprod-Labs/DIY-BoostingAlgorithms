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
     
    # Description: This code snippet is used to make a manual prediction using a pre-trained model.

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python 3.11.5
            # Pandas 2.2.2
            # Joblib 1.4.2

import pandas as pd # For data manipulation and analysis
import joblib       # For loading the pre-trained model

def prepare_input(age, years_at_company, monthly_income, job_satisfaction, performance_rating, work_life_balance, training_hours_last_year, department):
    # Prepare the input data for prediction by converting categorical features to numerical and creating a DataFrame
    
    # Convert the 'department' feature to numerical values
    departments = {
        'HR': 0,
        'Engineering': 1,
        'Sales': 2,
        'Accounting': 3,
        'Customer Service': 4
    }
    department_value = departments.get(department, -1)
    
    if department_value == -1:
        raise ValueError("Department must be one of the following: 'HR', 'Engineering', 'Sales', 'Marketing', 'Finance'")
    
    # Create a dictionary with user input data
    user_data = {
        'age': age,
        'years_at_company': years_at_company,
        'monthly_income': round(monthly_income, 2),
        'job_satisfaction': job_satisfaction,
        'performance_rating': performance_rating,
        'work_life_balance': work_life_balance,
        'training_hours_last_year': training_hours_last_year,
        'department': department_value
    }
    
    # Convert the dictionary to a DataFrame
    features = pd.DataFrame([user_data])
    return features

def predict(model, user_input):
    # Make a prediction using the model and user input data
    prediction = model.predict(user_input)[0]
    return 'Attrition' if prediction else 'No Attrition'

def manual_prediction(model_path, age, years_at_company, monthly_income, job_satisfaction, performance_rating, work_life_balance, training_hours_last_year, department):    
    # Load the model
    model = joblib.load(model_path)
    
    # Prepare user input data
    user_data = prepare_input(age, years_at_company, monthly_income, job_satisfaction, performance_rating, work_life_balance, training_hours_last_year, department)
    
    # Make a prediction using the model and user data
    prediction = predict(model, user_data)  
    
    # Print the prediction result
    print(f"Prediction: {prediction}")
    return prediction