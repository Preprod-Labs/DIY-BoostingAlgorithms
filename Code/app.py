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
     
    # Description: This code snippet is used to create a web app using Streamlit for visualizing the data
    # and model predictions.

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python 3.11.5
            # Streamlit 1.36.0

import streamlit as st # For creating the web app

# Importing the necessary .py helper files and functions
from ingest import ingest_data # For ingesting data from MariaDB and MongoDB
from transform import transform # For transforming and preprocessing the data
from train_adaboost import train_model as train_adaboost_model # For training the AdaBoost model
from train_gbm import train_model as train_gbm_model # For training the GBM model
from model_inference import model_inference # For getting the model metrics
from manual_prediction import manual_prediction # For manual user inputs

# Setting the page configuration for the web app
st.set_page_config(page_title="Boosting Algorithms", page_icon=":chart_with_upwards_trend:", layout="centered")

# Adding a heading to the web app
st.markdown("<h1 style='text-align: center; color: white;'>Boosting Algorithms</h1>", unsafe_allow_html=True)
st.divider()

# Declaring session states(streamlit variables) for saving the path throught page reloads
# This is how we declare session state variables in streamlit.

# MariaDB configuration 
if "mariadb_host" not in st.session_state:
    st.session_state.mariadb_host= "localhost"
    
if "mariadb_user" not in st.session_state:
    st.session_state.mariadb_user= "root"
    
if "mariadb_password" not in st.session_state:
    st.session_state.mariadb_password= "password"
    
if "mariadb_database" not in st.session_state:
    st.session_state.mariadb_database= "preprod"
    
# MongoDB configuration
if "mongodb_host" not in st.session_state:
    st.session_state.mongodb_host= "localhost"
    
if "mongodb_port" not in st.session_state:
    st.session_state.mongodb_port= 27017
    
if "mongodb_database" not in st.session_state:
    st.session_state.mongodb_database= "preprod"
    
# Redis configuration
if "redis_host" not in st.session_state:
    st.session_state.redis_host= "localhost"
    
if "redis_port" not in st.session_state:
    st.session_state.redis_port= 6379

# Paths configuration
if "master_data_path" not in st.session_state:
    st.session_state.master_data_path= "Data/Master/mock_data.csv"
    
if "adaboost_model_path" not in st.session_state:
    st.session_state.adaboost_model_path= "adaboost_model.pkl"
    
if "gbm_model_path" not in st.session_state:
    st.session_state.gbm_model_path= "gbm_model.pkl"

# Creating two tabs for the web app: "Model Training" and "Model Prediction"
tab1, tab2, tab3, tab4 = st.tabs(["Model Config","Model Training","Model Evaluation", "Model Prediction"])

with tab1:
    # Model Configuration tab
    st.subheader("Model Configuration")
    st.write("This is where you can configure the model.")
    st.divider()
    
    with st.form(key="Config Form"):
        tab_maria_db, tab_mongo_db, tab_redis, tab_paths = st.tabs(["MariaDB","MongoDB","Redis","Paths"])
        
        # Tab for MariaDB configuration
        with tab_maria_db:
            st.markdown("<h2 style='text-align: center; color: white;'>MariaDB Configuration</h2>", unsafe_allow_html=True)
            st.write(" ")
            
            # MariaDB Host
            mariadb_host = st.text_input("MariaDB Host", st.session_state.mariadb_host)
            st.session_state.mariadb_host = mariadb_host
            
            # MariaDB User
            mariadb_user = st.text_input("MariaDB User", st.session_state.mariadb_user)
            st.session_state.mariadb_user = mariadb_user
            
            # MariaDB Password
            mariadb_password = st.text_input("MariaDB Password", st.session_state.mariadb_password, type="password")
            st.session_state.mariadb_password = mariadb_password
            
            # MariaDB Database
            mariadb_database = st.text_input("MariaDB Database", st.session_state.mariadb_database)
            st.session_state.mariadb_database = mariadb_database
            
            # MariaDB configuration dictionary
            maridb_config = {
                "host": st.session_state.mariadb_host,
                "user": st.session_state.mariadb_user,
                "password": st.session_state.mariadb_password,
                "database": st.session_state.mariadb_database
            }
            
        # Tab for MongoDB configuration
        with tab_mongo_db:
            st.markdown("<h2 style='text-align: center; color: white;'>MongoDB Configuration</h2>", unsafe_allow_html=True)
            st.write(" ")
            
            # MongoDB Host
            mongodb_host = st.text_input("MongoDB Host", st.session_state.mongodb_host)
            st.session_state.mongodb_host = mongodb_host
            
            # MongoDB Port
            mongodb_port = st.number_input("MongoDB Port", st.session_state.mongodb_port)
            st.session_state.mongodb_port = mongodb_port
            
            # MongoDB Database
            mongodb_database = st.text_input("MongoDB Database", st.session_state.mongodb_database)
            st.session_state.mongodb_database = mongodb_database
            
            # MongoDB configuration dictionary
            mongodb_config = {
                "host": st.session_state.mongodb_host,
                "port": st.session_state.mongodb_port,
                "database": st.session_state.mongodb_database
            }
            
        # Tab for Redis configuration
        with tab_redis:
            st.markdown("<h2 style='text-align: center; color: white;'>Redis Configuration</h2>", unsafe_allow_html=True)
            st.write(" ")
            
            # Redis Host
            redis_host = st.text_input("Redis Host", st.session_state.redis_host)
            st.session_state.redis_host = redis_host
            
            # Redis Port
            redis_port = st.number_input("Redis Port", st.session_state.redis_port)
            st.session_state.redis_port = redis_port
            
            # Redis configuration dictionary
            redis_config = {
                "host": st.session_state.redis_host,
                "port": st.session_state.redis_port
            }
            
        # Tab for Paths configuration
        with tab_paths:
            st.markdown("<h2 style='text-align: center; color: white;'>Paths Configuration</h2>", unsafe_allow_html=True)
            st.write(" ")
            
            # Master Data Path
            master_data_path = st.text_input("Master Data Path", st.session_state.master_data_path)
            st.session_state.master_data_path = master_data_path
            
            # AdaBoost Model Path
            adaboost_model_path = st.text_input("AdaBoost Model Path", st.session_state.adaboost_model_path)
            st.session_state.adaboost_model_path = adaboost_model_path
            
            # GBM Model Path
            gbm_model_path = st.text_input("GBM Model Path", st.session_state.gbm_model_path)
            st.session_state.gbm_model_path = gbm_model_path
    
        if st.form_submit_button("Save Configuration"):
            st.success("Configuration saved successfully! ✅")
    
with tab2:
    # Model Training tab
    st.subheader("Model Training")
    st.write("This is where you can train the model.")
    st.divider()
    
    # Training the model
    selected_model = st.selectbox("Select the model to train", ["AdaBoost", "GBM"])
    if st.button("Train Model"):
        with st.status("Training the model..."):

            st.write("Ingesting data...")
            ingest_data(st.session_state.master_data_path, maridb_config, mongodb_config)
            st.write("Data ingested successfully! ✅")
            
            st.write("PreProcessing data...")
            transform(maridb_config, mongodb_config, redis_config)
            st.write("Data PreProcessed, split and stored in Redis successfully! ✅")
            
            st.write("Training the model...")
            if selected_model == "AdaBoost":
                st.write("Training AdaBoost model...")
                accuracy_score, classification_report = train_adaboost_model(st.session_state.redis_host, st.session_state.redis_port, st.session_state.adaboost_model_path)
            else:
                st.write("Training GBM model...")
                accuracy_score, classification_report = train_gbm_model(st.session_state.redis_host, st.session_state.redis_port, st.session_state.gbm_model_path)
                
        st.success(f"{selected_model} trained successfully with an accuracy score of {accuracy_score}! ✅")
        st.text("Classification Report:")
        st.text(classification_report)
            
with tab3:
    # Model Evaluation tab
    st.subheader("Model Evaluation")
    st.write("This is where you can see the current metrics of the most recently saved models")
    st.divider()
    
    # Displaying the metrics for the AdaBoost Model
    st.markdown("<h3 style='text-align: center; color: white;'>AdaBoost</h3>", unsafe_allow_html=True)
    st.divider()
    
    # Getting the model test, validation ad supervalidation metrics
    testAccuracy, testClassificationReport, validationAccuracy, validationClassificationReport, supervalidationAccuracy, supervalidationClassificationReport = model_inference(st.session_state.adaboost_model_path)
    
    # Test Metrics
    st.markdown("<h4 style='text-align: center; color: white;'>Test Metrics</h4>", unsafe_allow_html=True)
    st.text(f"Test Accuracy: {testAccuracy}")
    st.text("Test Classification Report:")
    st.text(testClassificationReport)
    
    # Validation Metrics
    st.markdown("<h4 style='text-align: center; color: white;'>Validation Metrics</h4>", unsafe_allow_html=True)
    st.text(f"Validation Accuracy: {validationAccuracy}")
    st.text("Validation Classification Report:")
    st.text(validationClassificationReport)
    
    # Supervalidation Metrics
    st.markdown("<h4 style='text-align: center; color: white;'>Supervalidation Metrics</h4>", unsafe_allow_html=True)
    st.text(f"Supervalidation Accuracy: {supervalidationAccuracy}")
    st.text("Supervalidation Classification Report:")
    st.text(supervalidationClassificationReport)
    
    st.divider()
    
    # Displaying the metrics for the GBM Model
    st.markdown("<h3 style='text-align: center; color: white;'>GBM</h3>", unsafe_allow_html=True)
    st.divider()
    
    # Getting the model test, validation ad supervalidation metrics
    testAccuracy, testClassificationReport, validationAccuracy, validationClassificationReport, supervalidationAccuracy, supervalidationClassificationReport = model_inference(st.session_state.gbm_model_path)
    
    # Test Metrics
    st.markdown("<h4 style='text-align: center; color: white;'>Test Metrics</h4>", unsafe_allow_html=True)
    st.text(f"Test Accuracy: {testAccuracy}")
    st.text("Test Classification Report:")
    st.text(testClassificationReport)
    
    # Validation Metrics
    st.markdown("<h4 style='text-align: center; color: white;'>Validation Metrics</h4>", unsafe_allow_html=True)
    st.text(f"Validation Accuracy: {validationAccuracy}")
    st.text("Validation Classification Report:")
    st.text(validationClassificationReport)
    
    # Supervalidation Metrics
    st.markdown("<h4 style='text-align: center; color: white;'>Supervalidation Metrics</h4>", unsafe_allow_html=True)
    st.text(f"Supervalidation Accuracy: {supervalidationAccuracy}")
    st.text("Supervalidation Classification Report:")
    st.text(supervalidationClassificationReport)
    
with tab4:
    # Model Prediction tab
    st.subheader("Model Prediction")
    st.write("This is where you can predict employee attrition.")
    
    with st.form(key="Prediction Form"):
        
        selected_model = st.selectbox("Select the model to predict", ["AdaBoost", "GBM"])
        selected_model_path = st.session_state.adaboost_model_path if selected_model == "AdaBoost" else st.session_state.gbm_model_path
        
        # Input fields for prediction
        age = st.number_input("Age", min_value=21, max_value=55)
        years_at_company = st.number_input("Years at Company", min_value=2, max_value=34, value=17)
        monthly_income = st.number_input("Monthly Income", min_value=50000, max_value=600000, value=300000)
        job_satisfaction = st.number_input("Job Satisfaction", min_value=1, max_value=10, value=5)
        performance_rating = st.number_input("Performance Rating", min_value=1, max_value=5, value=3)
        work_life_balance = st.number_input("Work Life Balance", min_value=1, max_value=5, value=3)
        training_hours_last_year = st.number_input("Training Hours Last Year", min_value=1, max_value=200, value=50)
        department = st.selectbox("Department", ["HR", "Accounting", "Engineering", "Sales", "Customer Service"])
        
        if st.form_submit_button("Predict"):
            prediction = manual_prediction(selected_model_path, age, years_at_company, monthly_income, job_satisfaction, performance_rating, work_life_balance, training_hours_last_year, department)
            st.success(f"Prediction: {prediction} ✅")