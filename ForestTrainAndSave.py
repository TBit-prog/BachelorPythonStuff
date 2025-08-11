## Vorlage: https://www.datacamp.com/tutorial/random-forests-classifier-python?dc_referrer=https%3A%2F%2Fwww.google.com%2F
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

from sklearn.tree import export_graphviz
from IPython.display import Image
import graphviz

import joblib


path = r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle\Trainingsdaten"
trainingsdata = r"\TestData.csv"

modelpath = r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle\Modelle\Random Forest"
modelname = r"\MyFirstForest.joblib"

def removeMidHeader(df):
    df = df[df['Temp'] != 'Temp'] # Df ist alles, was nicht Temp in der Spalte Temp ist
    df = df.astype(float) # in float konvertieren
    return df

def removeTimestamp(df):
    if "Timestamp" in df.columns:
        df = df.drop(columns=["Timestamp"])
    return df

##Read and Format Data
df = pd.read_csv(path + trainingsdata)
df = removeTimestamp(df)
df = removeMidHeader(df)

#Input X Output Y
X = df[["Temp", "IAQ", "Hum", "VOC"]]
Y = df[["Fenster_offen"]]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

#Create Random Forest Model
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

#Test Prediction
prediction = rf.predict(X_test)
accuracy = accuracy_score(y_test, prediction)
print("Accuracy", accuracy)

#Save Model
joblib.dump(rf, modelpath + modelname)