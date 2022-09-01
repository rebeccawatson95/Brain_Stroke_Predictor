# Dependencies
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from imblearn.over_sampling import RandomOverSampler

# Reading in data
df = pd.read_csv('Resources/healthcare-dataset-stroke-data.csv')
df.head()

# Removing outlier values in 'gender' column, converting to numerical values
df = df[df['gender'] != 'Other']
df.gender = df.gender.replace({'Male':0, 'Female':1})

# Removing the 'id' column
df = df.drop('id', axis=1)

# Converting other binary data points into numerical values
df.ever_married = df.ever_married.replace({'No':0, 'Yes':1})
df.Residence_type = df.Residence_type.replace({'Urban':0, 'Rural':1})

# Filling in missing values from 'bmi' column, using a decision tree model that predicts the missing values
# Code originally written by Thomas Konstantin
DT_bmi_pipe = Pipeline(steps=[ 
                               ('scale',StandardScaler()),
                               ('lr',DecisionTreeRegressor(random_state=1))
                              ])
X_bmi = df[['age','gender','bmi']].copy()

Missing = X_bmi[X_bmi.bmi.isna()]
X_bmi = X_bmi[~X_bmi.bmi.isna()]
y_bmi = X_bmi.pop('bmi')
DT_bmi_pipe.fit(X_bmi,y_bmi)
predicted_bmi = pd.Series(DT_bmi_pipe.predict(Missing[['age','gender']]),index=Missing.index)
df.loc[Missing.index,'bmi'] = predicted_bmi

# Converting dataset into numerical values
df_num = pd.get_dummies(df)
df_num.shape

# Upsampling data so the dataset is not skewed towards 'no stroke' values
y = df_num['stroke']
X = df_num.drop('stroke', axis=1)

ros = RandomOverSampler(random_state=1)
X_resampled, y_resampled = ros.fit_resample(X, y)
ros_df = X_resampled.assign(Stroke = y_resampled)

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, random_state=1)

# Setting up StandardScaler
scaler = StandardScaler()

# Fitting training data
X_scaler = scaler.fit(X_train)

# Scale the data
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

# Creating decision tree model
dtc_pipe = Pipeline(steps=[('scale',StandardScaler()),('DT',DecisionTreeClassifier(random_state=1))])
dtc_pipe.fit(X_train_scaled, y_train)
print('Test Acc: %.3f' % dtc_pipe.score(X_test_scaled, y_test))

# Classification report for Decision Tree Classifier model
dtcpred = dtc_pipe.predict(X_test_scaled)
print(classification_report(y_test, dtcpred, target_names=['no_stroke','stroke']))
