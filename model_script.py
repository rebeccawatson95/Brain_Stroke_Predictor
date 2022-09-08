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
    y = data['Stroke']
    X = data.drop('Stroke', axis=1).values

    # Splitting data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    # Setting up StandardScaler
    scaler = StandardScaler()

    # Fitting training data
    X_scaler = scaler.fit(X_train)

    # Scale the data
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)

    # Creating decision tree model
    dtc_pipe = Pipeline(steps=[('scale',StandardScaler()),('DT',DecisionTreeClassifier(random_state=1))])
    dtc_pipe = dtc_pipe.fit(X_train_scaled, y_train)

    # Testing for functionality
    #if dtc_pipe.score(X_test_scaled, y_test) > 0:
        #score = 'test'
    #return score

    sample = [1,49.0,0,0,1,0,171.23,34.400000,0,0,1,0,0,0,0,0,1]
    keys = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married',
       'Residence_type', 'avg_glucose_level', 'bmi', 'work_type_Govt_job',
       'work_type_Never_worked', 'work_type_Private',
       'work_type_Self-employed', 'work_type_children',
       'smoking_status_Unknown', 'smoking_status_formerly smoked',
       'smoking_status_never smoked', 'smoking_status_smokes']
    nsample = pd.DataFrame(columns=keys)
    nsample.loc[0] = sample
    #print(dtc_pipe.predict(nsample))

    #dict = {'dtc_pipe': dtc_pipe, 'X_scaler': X_scaler}

    # Return model
    return dtc_pipe

    #pred = dtc_pipe.predict(input)
    #output = str(pred[0])
    #return output

def scale_input(input):

    # Reading in data from sqlite
    con = sqlite3.connect('Resources/stroke_prediction_data.sqlite')
    data = pd.read_sql('SELECT * FROM stroke_prediction_data', con)
    data = data.drop('index', axis=1)
    #print(data.dtypes)

    # Separating target values from features
    y = data['Stroke']
    X = data.drop('Stroke', axis=1).values

    # Splitting data into training and testing sets
    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    # Setting up StandardScaler
    scaler = StandardScaler()

    # Fitting training data
    X_scaler = scaler.fit(X)

    input_scaled = X_scaler.transform(input)

    return input_scaled