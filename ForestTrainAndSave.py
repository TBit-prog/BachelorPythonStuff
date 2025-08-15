## Vorlage: https://www.datacamp.com/tutorial/random-forests-classifier-python?dc_referrer=https%3A%2F%2Fwww.google.com%2F
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split, cross_val_score

import joblib

def removeMidHeader(df):
    df = df[df['Temp'] != 'Temp'] # Df ist alles, was nicht Temp in der Spalte Temp ist
    df = df.astype(float) # in float konvertieren
    return df

def removeTimestamp(df):
    if "Timestamp" in df.columns:
        df = df.drop(columns=["Timestamp"])
    return df

path = r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle\Trainingsdaten"
trainingsdata = r"\TestData.csv"

modelpath   = r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle\Modelle\Random Forest"
modelname   = r"\MyFirstForest.joblib"
featurename = r"\MyFeatureNames.joblib"
 
##Read and Format Data
df = pd.read_csv(path + trainingsdata).iloc[:, [1,2,4,6]] # Daten laden und nur relevante Spalten aus der Datei nehmen, noch 4 für Volume
df = removeMidHeader(df)

#Input X Output Y
X = df[["Temp", "IAQ", "Hum"]] #"Volume",
Y = df["Fenster_offen"]
features = list(df.columns[:-1])
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

#Create Random Forest Model
rf = RandomForestClassifier()
rf.fit(X, Y)
scores = cross_val_score(rf, X, Y, cv = 5)
print("Mittlere Genauigkeit:", scores.mean())

#Prediction
prediction = rf.predict(X_test)

importances = rf.feature_importances_
for name, val in zip(X.columns, importances):
    print(f"{name}: {val:.3f}")

#Save Model
joblib.dump(rf, modelpath + modelname)
joblib.dump(features, modelpath + featurename)


"""

WORKFLOW

Data Collection
Data cleaning
Feature engineering
Split the data

Hyperparameter Tuning
Train your models
Make predictions
Asses Model Performance

Deployment and iteration of the process
"""