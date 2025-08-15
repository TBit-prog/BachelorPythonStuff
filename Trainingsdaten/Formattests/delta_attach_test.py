import numpy as np
import pandas as pd

def removeMidHeader(df):
    df = df[df["Temp"] != "Temp"] # Df ist alles, was nicht Temp in der Spalte Temp ist
    df = df.astype(float) # in float konvertieren
    return df

def removeTimestamp(df):
    if "Timestamp" in df.columns:
        df = df.drop(columns=["Timestamp"])
    return df

path = r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle\Trainingsdaten\Formattests"
data = r"\TestData.csv"

#kleines Testfile mit Header
df = pd.read_csv(path + data).iloc[:, [1,2,3,4,7]] # Daten laden und nur relevante Spalten aus der Datei nehmen
df = removeMidHeader(df)
df = removeMidHeader(df)

df_trend = pd.DataFrame(columns = ["trend_Temp", "trend_IAQ", "trend_Hum"])
df_lag = pd.DataFrame(columns = ["lag_Temp", "lag_IAQ", "lag_Hum"])
df_trend["trend_IAQ"] = df["IAQ"]
df_trend["trend_Temp"] = df["Temp"]
df_trend["trend_Hum"] = df["Hum"]
df_lag = df_trend.shift(-1).fillna(0)
df_trend = df_trend - df_lag
df_trend = df_trend
print(df_trend)
df = pd.concat([df, df_trend], axis=1).drop(df_trend.index[-1])
df["Fenster_offen"] = df["Fenster_offen"].astype(int)
print(df)


"""
df_trend["trend_IAQ"] = df["IAQ"]   - df["IAQ"].shift(1)
df_trend["trend_Hum"] = df["Hum"]   - df["Hum"].shift(1)
df_trend = df_trend.drop(index = 1)
#pd.concat([df, df_trend], axis = 1)
print(df_trend)
#delta_temp, delta_iaq, delta_hum = 0
"""
