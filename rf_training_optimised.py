# Vorlage: https://www.datacamp.com/tutorial/random-forests-classifier-python?dc_referrer=https%3A%2F%2Fwww.google.com%2F
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split, cross_val_score
from dataclasses import dataclass

import joblib

def removeMidHeader(df):
    df = df[df['Temp'] != 'Temp'] # Df ist alles, was nicht Temp in der Spalte Temp ist
    df = df.astype(float) # in float konvertieren
    return df


#Pfade
root_loc         = r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle"
data_loc         = r"\Trainingsdaten\TestData.csv"   
model_loc        = r"\Modelle\Random Forest\MyFirstForest.joblib" 
feature_loc      = r"\Modelle\Random Forest\MyFeatureNames.joblib"

#Daten vorbereiten
df = pd.read_csv(root_loc + data_loc).iloc[:, [1,2,4,6]] # Daten laden und nur relevante Spalten aus der Datei nehmen
df = removeMidHeader(df)

#Trenddaten erzeugen
df_trend = pd.DataFrame(columns = ["trend_Temp", "trend_IAQ", "trend_Hum"])
df_lag = pd.DataFrame(columns = ["lag_Temp", "lag_IAQ", "lag_Hum"])
df_trend["trend_IAQ"] = df["IAQ"]
df_trend["trend_Temp"] = df["Temp"]
df_trend["trend_Hum"] = df["Hum"]
df_lag = df_trend.shift(-1).fillna(0)
df_trend = df_trend - df_lag

print(df_trend)
#Split Input Output
X = df[["Temp", "IAQ", "Hum"]]#"Volume"
y = df["Fenster_offen"]
features = list(df.columns[:-1])
#Part für Trenddaten nochmal aufräumen

print(df_trend)
X = pd.concat([X, df_trend], axis=1)
X = X.drop(X.index[-1])
y = y.drop(y.index[-1])
#df["Fenster_offen"] = df["Fenster_offen"].astype(int)
print(X)

#Modell erstellen
rf = RandomForestClassifier()
rf.fit(X, y)

scores = cross_val_score(rf, X, y, cv = 5)
print("Mittlere Genauigkeit:", scores.mean())

importances = rf.feature_importances_
for name, val in zip(X.columns, importances):
    print(f"{name}: {val:.3f}")

#Save Model
joblib.dump(rf, root_loc + model_loc)
joblib.dump(features, root_loc + feature_loc)

