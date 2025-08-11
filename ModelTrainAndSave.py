import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import plot_model
from sklearn.preprocessing import StandardScaler

from utils import removeMidHeader
from utils import removeTimestamp

class createNeuralNet:
    def __init__(self, input_shape):
        self.model = models.Sequential([
            layers.Dense(16, activation='relu', input_shape=(input_shape,)),
            layers.Dense(8, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        #Was ist adam, mse und mae? 
        # Adam ist ein Optimierungsalgorithmus
        # binary_crossentropy ist eine Verlustfunktion, die für binäre Klassifikation genutzt wird

    def train(self, X_train, y_train, epochs, validation_data):
        return self.model.fit(X_train, y_train, epochs=epochs, validation_data=validation_data)

    def predict(self, X):
        return self.model.predict(X)

    def save(self, filepath):
        self.model.save(filepath)

    def summary(self):
        self.model.summary()

    def evaluate(self, X_test, y_test):
        return self.model.evaluate(X_test, y_test)


# Pfad, in dem Modell gespeichert werden soll
savepath =   r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle\Modelle\NN"
model_name = r"\TestModel.keras"
savedModel = savepath + model_name

# Pfad zu Trainingsdaten
path = r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle\Trainingsdaten"
trainingsdata = r"\TestData.csv"

#Trainingsdaten einlesen und Header zwischendrin entfernen
df = pd.read_csv(path + trainingsdata)
df = removeTimestamp(df)
df = removeMidHeader(df)


#Input und OUtput Daten definieren
#X = df[["Temp", "IAQ", "Volume", "Hum", "VOC"]]
X = df[["Temp", "IAQ", "Hum", "VOC"]]
Y = df[["Fenster_offen"]]

# Daten aufteilen in Trainings- und Testdaten und skalieren
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, Y, test_size=0.1, random_state=42)
#random_state ist praktisch ein Seed, der die Zufälligkeit der Aufteilung kontrolliert

# Modell erstellen und trainieren
input_shape = X_train.shape[1]
nn = createNeuralNet(input_shape)
history = nn.train(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Modell speichern und Zusammenfassung anzeigen
nn.save(savedModel)
nn.summary()

# Modell für Vorhersagen nutzen (Beispiel mit Testdaten)
predictions = nn.predict(X_test)
print("Vorhersagen für Testdaten:", predictions[:5])

#Auswertung der Genauigkeit und der Verlusts während des Trainings
loss, acc = nn.evaluate(X_test, y_test)
print("Genauigkeit des Test:", acc)
print("Loss des Tests: ", loss)