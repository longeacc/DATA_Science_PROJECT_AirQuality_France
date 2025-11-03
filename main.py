import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from src.utils.common_functions import read_data
# Imports optionnels avec gestion des erreurs
try:
    import plotly.graph_objects as go
    import plotly.io as pio
    from plotly.io import write_html
    PLOTLY_AVAILABLE = True
except ImportError:
    print("Note: plotly n'est pas installé. Pour l'installer, exécutez : pip install plotly")
    PLOTLY_AVAILABLE = False

# Définir le chemin du fichier
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2007_Ineris_v.Sep2020.csv')

# Charger les données
data = read_data.load_data(file_path)
data = read_data.process_data(data)

if __name__ == "__main__":
    if data is not None:
        print("\nDonnées chargées avec succès dans le script principal.")
        
        # Afficher les informations sur les colonnes
        print("\nListe des colonnes :")
        for i, col in enumerate(data.columns):
            print(f"{i + 1}. {col}")
            # Afficher quelques valeurs uniques pour chaque colonne
            unique_values = data[col].nunique()
            print(f"   Nombre de valeurs uniques : {unique_values}")
            print(f"   Exemple de valeurs : {data[col].head().tolist()}\n")
        
        print(f"\nDimensions des données : {data.shape}")
        
        # Vérifier les types de données
        print("\nTypes de données par colonne :")
        print(data.dtypes)
        
        # Afficher un résumé statistique pour les colonnes numériques
        print("\nRésumé statistique des colonnes numériques :")
        print(data.describe())
        
        # Vérifier les valeurs manquantes
        print("\nNombre de valeurs manquantes par colonne :")
        missing_values = data.isnull().sum()
        for col in data.columns:
            if missing_values[col] > 0:
                print(f"{col}: {missing_values[col]} valeurs manquantes")
    else:
        print("Échec du chargement des données dans le script principal.")
    
    # Visualization of N02
    data_sorted_commune_2020 = data.sort_values('COM Insee')
    trace = go.Scatter(x=data_sorted_commune_2020['COM Insee'], y=data['Moyenne annuelle de concentration de NO2 (ug/m3)'], mode='markers')
    layout = go.Layout( title='NO2 Moyenne Annuelle par COM Insee en 2020', xaxis_title='Commune', yaxis_title='NO2 Moyenne Annuelle',
    # Rotation des étiquettes de l'axe x
    xaxis=dict(
        tickangle=-45,  # Rotation à 45 degrés
        tickfont=dict(size=10)  # Réduction de la taille de police si nécessaire
    ),
    # Ajout d'une annotation pour indiquer que la liste n'est pas complète
    annotations=[
        dict(
            x=0.5,
            y=-0.2,  # Position en bas du graphique
            xref='paper',
            yref='paper',
            text="Liste non exhaustive : seules certaines communes sont affichées",
            showarrow=False,
            font=dict(size=12, style='italic'),
            align='center'
        )
    ],
    # Ajustement des marges pour accommoder l'annotation et les étiquettes inclinées
    margin=dict(b=100)  # Marge augmentée en bas
)
    fig = go.Figure(data=[trace], layout=layout)
    write_html(fig, file='NO2_moyenne_annuelle_2020.html', auto_open=True, include_plotlyjs='cdn')



    # Visualization of PM10
    trace = go.Scatter(x=data_sorted_commune_2020['COM Insee'], y=data['Moyenne annuelle de concentration de PM10 (ug/m3)'], mode='markers')
    layout = go.Layout(title='PM10 Moyenne Annuelle par Commune en 2020', xaxis_title='COM Insee', yaxis_title='PM10 Moyenne Annuelle')
    fig = go.Figure(data=[trace], layout=layout)
    write_html(fig, file='PM10_moyenne_annuelle_2020.html', auto_open=True, include_plotlyjs='cdn')

