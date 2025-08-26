import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import groupby

#Daten abpacken
df     = pd.read_csv("Result.csv")
points = df.shape[0]
print(df.columns)

###Analyse
##Genauigkeit
inf      = df["Fenster_real"] == df["Fenster_mess"] ##Ergebnis: Spalte mit Bol
inf_sum  = inf.sum()
accuracy = (inf_sum/points)*100
print(f"Die Genauigkeit der Inferenz beträgt {accuracy.round(2)}%")
print(inf)

##Zeit vergangen zwischen Ausgleich
"""
ANNAHME 1: Beide Messreihen haben denselben Anfangswert
ANNAHME 2: Nicht erkannte Änderungen des Fensters sind alle zum Schluss
ANNAHME 3: Kein Rauschen, nur Verzögerungen der Inferenz in Bezug zu realem Wert
"""
#tuples mit Länge der konstanten Abschnitte
real     = df["Fenster_real"]
inferenz = df["Fenster_mess"]

liste_r = []
liste_i = []
for wert_real, gruppe_real in groupby(real):
    liste_real = list(gruppe_real)
    abschnitt_real = len(liste_real)
    liste_r.append(abschnitt_real)

for wert_inferenz, gruppe_inferenz in groupby(inferenz):
    liste_inferenz = list(gruppe_inferenz)
    abschnitt_inferenz = len(liste_inferenz)
    liste_i.append(abschnitt_inferenz)

print(f"Reale Werte:{liste_r}")
print(f"Inferenzwerte: {liste_i}")

delta = [0] * len(liste_i)

for i in range(0, len(liste_i)):
    if i > 0 and i < len(liste_i) - 1:
        liste_i[i] = liste_i[i] + delta[i-1]
    delta[i] = liste_i[i] - liste_r[i]
    print(delta)
    print(i)
    print(len(liste_i))

print(f"Die Deltas sind: {delta}")

messintervall = 4 # in Sekunden
#Wie oft Ändert sich Fensterzustand in der Inferenz
if len(liste_i) < len(liste_r):
    lag = [0]* (len(delta) - 1)
    print("Nicht alle Öffnungen/Schließungen des Fensters erkannt")
else:
    lag = [0]*len(delta)

#Umrechnung Messpunkte in Sekunden
for i in range(0, len(lag)):
    lag[i] = delta[i] * messintervall

print(lag)



###Plot
fig = plt.figure(1)
plt.plot(df, linewidth=2.0)
plt.legend(["Real", "Inferenz"])
plt.xlabel("Messindex")
plt.ylabel(" Fensterzustand")
plt.suptitle("Vergleich der Inferenz mit realem Zustand")
plt.axis([0, points, 0, 1.1])
plt.yticks([0, 1], ["Geschlossen", "Offen"])
fig.text(0.6, 0.03, f"Genauigkeit der Inferenz: {accuracy.round(2)}%")
plt.show()
#Print