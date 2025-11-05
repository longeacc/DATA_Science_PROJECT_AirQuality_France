import pandas as pd
from histograms import create_pollution_histogram  # ton fichier histograms.py
from plotly.io import show

# 1. Charger le CSV
data = pd.read_csv("data/cleaned/cleaned_air_quality_with_year.csv")

# 2. Créer l'histogramme pour un polluant
fig = create_pollution_histogram(data, "NO2")  # tu peux mettre PM10 ou O3

# 3. Afficher la figure dans une fenêtre du navigateur
show(fig)