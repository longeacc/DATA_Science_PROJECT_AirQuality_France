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

# Créer les dictionnaires de correspondance commune-INSEE
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data)

if __name__ == "__main__":
    if data is not None and commune_to_insee is not None:
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
    
    # Visualization of NO2
    # Trier les données par code INSEE croissant
    data_sorted_no2 = data.sort_values('COM Insee', ascending=True)
    
    # Créer les listes pour le graphique
    communes = [insee_to_commune[code] for code in data_sorted_no2['COM Insee']]
    concentrations = data_sorted_no2['Moyenne annuelle de concentration de NO2 (ug/m3)']
    
    # Créer le scatter plot avec Plotly
    trace = go.Scatter(
        x=communes,
        y=concentrations,
        mode='markers',
        marker=dict(
            size=2,
            color=concentrations,  # Utiliser la concentration pour la couleur
            colorscale='Viridis',  # Échelle de couleur
            showscale=True  # Afficher la barre de couleur
        ),
        hovertemplate="<b>%{x}</b><br>" +
                     "NO2: %{y:.1f} µg/m³<br>" +
                     "Code INSEE: %{customdata}<extra></extra>",
        customdata=data_sorted_no2['COM Insee']  # Ajouter le code INSEE pour le hover
    )
    layout = go.Layout(
        title=dict(
            text='Concentration moyenne annuelle en 2007/2020 de NO2 par commune',
            font=dict(size=24)
        ),
        xaxis=dict(
            title='Commune',
            tickangle=-45,
            tickfont=dict(size=10),
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        yaxis=dict(
            title='NO2 (µg/m³)',
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='Gray'
        ),
        # Ajout d'une annotation pour indiquer que la liste n'est pas complète
        annotations=[
            dict(
                x=0.5,
                y=-0.3,  # Position en bas du graphique
                xref='paper',
                yref='paper',
                text="Liste des communes triées par code INSEE (ordre géographique)",
                showarrow=False,
                font=dict(size=12, style='italic'),
                align='center'
            )
        ],
    # Ajustement des marges pour accommoder l'annotation et les étiquettes inclinées
    margin=dict(b=100)  # Marge augmentée en bas
)
    # Créer et sauvegarder le graphique NO2
    fig_no2 = go.Figure(data=[trace], layout=layout)
    write_html(fig_no2, file='NO2_moyenne_annuelle_2007_2020.html', auto_open=True, include_plotlyjs='cdn')
    print("Graphique NO2 généré avec succès !")

    # Visualization of PM10
    data_sorted_pm10 = data.sort_values('COM Insee', ascending=True)
    communes_pm10 = [insee_to_commune[code] for code in data_sorted_pm10['COM Insee']]
    concentrations_pm10 = data_sorted_pm10['Moyenne annuelle de concentration de PM10 (ug/m3)']
    
    trace_pm10 = go.Scatter(
        x=communes_pm10,
        y=concentrations_pm10,
        mode='markers',
        marker=dict(
            size=2,
            color=concentrations_pm10,
            colorscale='Viridis',
            showscale=True
        ),
        hovertemplate="<b>%{x}</b><br>" +
                     "PM10: %{y:.1f} µg/m³<br>" +
                     "Code INSEE: %{customdata}<extra></extra>",
        customdata=data_sorted_pm10['COM Insee']
    )
    layout_pm10 = go.Layout(
        title=dict(
            text='Concentration moyenne annuelle en 2007/2020 de PM10 par commune',
            font=dict(size=24)
        ),
        xaxis=dict(
            title='Commune',
            tickangle=-45,
            tickfont=dict(size=10),
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        yaxis=dict(
            title='PM10 (µg/m³)',
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='Gray'
        ),
        annotations=[
            dict(
                x=0.5,
                y=-0.3,
                xref='paper',
                yref='paper',
                text="Liste des communes triées par code INSEE (ordre géographique)",
                showarrow=False,
                font=dict(size=12, style='italic'),
                align='center'
            )
        ],
        margin=dict(b=100)  # Marge augmentée en bas
    )
    # Créer et sauvegarder le graphique PM10
    fig_pm10 = go.Figure(data=[trace_pm10], layout=layout_pm10)
    write_html(fig_pm10, file='PM10_moyenne_annuelle_2007_2020.html', auto_open=True, include_plotlyjs='cdn')
    print("Graphique PM10 généré avec succès !")

