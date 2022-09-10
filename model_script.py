# Dependencies
import pandas as pd
import sqlite3
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# Creating machine learning model
def make_model():

    # Reading in data from sqlite
    con = sqlite3.connect('Resources/stroke_prediction_data.sqlite')
    data = pd.read_sql('SELECT * FROM stroke_prediction_data', con)
    data = data.drop('index', axis=1)
    #print(data.dtypes)

    # Separating target values from features
    y = data['stroke']
    X = data.drop('stroke', axis=1).values

    # Splitting data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    # Setting up StandardScaler
    scaler = StandardScaler()

    # Fitting training data
    X_scaler = scaler.fit(X_train)

    # Scale the data
    X_train_scaled = X_scaler.transform(X_train)
    #X_test_scaled = X_scaler.transform(X_test)

    # Creating decision tree model
    dtc_pipe = Pipeline(steps=[('scale',StandardScaler()),('DT',DecisionTreeClassifier(random_state=1))])
    dtc_pipe = dtc_pipe.fit(X_train_scaled, y_train)

    # (for testing) Returns string if running correctly within Flask
    #if dtc_pipe.score(X_test_scaled, y_test) > 0:
        #score = 'test'
    #return score

    # (for testing) Returns 0 or 1 depending on user input parameters
    # Predicted outcome with sample: 1
    #sample = [1,49.0,0,0,1,0,171.23,34.400000,0,0,1,0,0,0,0,0,1]
    #keys = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'Residence_type', 'avg_glucose_level', 'bmi', 'work_type_Govt_job', 'work_type_Never_worked', 'work_type_Private', 'work_type_Self-employed', 'work_type_children', 'smoking_status_Unknown', 'smoking_status_formerly smoked', 'smoking_status_never smoked', 'smoking_status_smokes']
    #nsample = pd.DataFrame(columns=keys)
    #nsample.loc[0] = sample
    #print(dtc_pipe.predict(nsample))

    # Return model
    return dtc_pipe


# Creating StandardScaler for user inputs
def scale_input(input):

    # Reading in data from sqlite
    con = sqlite3.connect('Resources/stroke_prediction_data.sqlite')
    data = pd.read_sql('SELECT * FROM stroke_prediction_data', con)
    data = data.drop('index', axis=1)
    #print(data.dtypes)

    # Separating feature values
    y = data['stroke']
    X = data.drop('stroke', axis=1).values

    # Splitting data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    # Setting up StandardScaler
    scaler = StandardScaler()

    # Fitting training data
    X_scaler = scaler.fit(X_train)

    # Scaling data
    input_scaled = X_scaler.transform(input)

    # Return 
    return input_scaled