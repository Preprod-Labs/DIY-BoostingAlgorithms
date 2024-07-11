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

# Importing the necessary .py helper files and functions
from evaluate import evaluate_model

def model_inference(model_path):
    # Evaluatiing the model on the test, validation, and supervalidation datasets
    
    testAccuracy, testClassificationReport  = evaluate_model(model_path, 'test')
    validationAccuracy, validationClassificationReport = evaluate_model(model_path, 'validation')
    supervalidationAccuracy, supervalidationClassificationReport = evaluate_model(model_path, 'supervalidation')

    return testAccuracy, testClassificationReport, validationAccuracy, validationClassificationReport, supervalidationAccuracy, supervalidationClassificationReport

if __name__ == "__main__":
    model_inference('adaboost_model.pkl')