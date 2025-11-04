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
    # Trier les communes par population croissante
    data_sorted_no2 = data.sort_values('Population', ascending=True)
    
    # Créer les listes pour le graphique NO2
    communes = [insee_to_commune[code] for code in data_sorted_no2['COM Insee']]
    concentrations = data_sorted_no2['Moyenne annuelle de concentration de NO2 (ug/m3)']
    populations = data_sorted_no2['Population']  # Pour l'affichage dans les info-bulles
    
    # Créer le graphique de points pour NO2
    trace = go.Scatter(
        x=communes,
        y=concentrations,
        mode='markers',
        name='Mesures NO2',
        marker=dict(
            size=2,
            color=concentrations,
            colorscale='Viridis',
            showscale=True
        ),
        hovertemplate="<b>%{x}</b><br>" +
                     "NO2: %{y:.1f} µg/m³<br>" +
                     "Population: %{customdata:,.0f} hab.<extra></extra>",
        customdata=populations
    )
    
    # Trace des points
    trace_points = go.Scatter(
        x=communes,
        y=concentrations,
        mode='markers',
        name='Mesures',
        marker=dict(
            size=2,
            color=concentrations,
            colorscale='Viridis',
            showscale=True
        ),
        hovertemplate="<b>%{x}</b><br>" +
                     "NO2: %{y:.1f} µg/m³<br>" +
                     "Population: %{customdata:,.0f} hab.<extra></extra>",
        customdata=populations
    )
    
    # Trace de la ligne de tendance
    trace_line = go.Scatter(
        x=communes,
        y=concentrations,
        name='Tendance',
        hoverinfo='skip'
    )
    
    # Combiner les deux traces
    traces_no2 = [trace_points, trace_line]
    layout = go.Layout(
        title=dict(
            text='Concentration moyenne annuelle en 2007/2020 de NO2 par population de commune',
            font=dict(size=24)
        ),
        xaxis=dict(
            title='Population des communes',
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
            zeroline=False,
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
                text="Liste des communes triées par population croissante (ordre géographique)",
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
    data_sorted_pm10 = data.sort_values('Population', ascending=True)
    communes_pm10 = [insee_to_commune[code] for code in data_sorted_pm10['COM Insee']]
    concentrations_pm10 = data_sorted_pm10['Moyenne annuelle de concentration de PM10 (ug/m3)']
    populations_pm10 = data_sorted_pm10['Population']
    
    # Créer le graphique de points pour PM10
    trace_pm10 = go.Scatter(
        x=communes_pm10,
        y=concentrations_pm10,
        mode='markers',
        name='Mesures PM10',
        marker=dict(
            size=2,
            color=concentrations_pm10,
            colorscale='Viridis',
            showscale=True
        ),
        hovertemplate="<b>%{x}</b><br>" +
                     "PM10: %{y:.1f} µg/m³<br>" +
                     "Population: %{customdata:,.0f} hab.<extra></extra>",
        customdata=populations_pm10
    )  # Pour l'affichage dans les info-bulles
    
    # Trace des points uniquement pour PM10
    trace_pm10 = go.Scatter(
        x=communes_pm10,
        y=concentrations_pm10,
        mode='markers',
        name='Mesures PM10',
        marker=dict(
            size=2,
            color=concentrations_pm10,
            colorscale='Viridis',
            showscale=True
        ),
        hovertemplate="<b>%{x}</b><br>" +
                     "PM10: %{y:.1f} µg/m³<br>" +
                     "Population: %{customdata:,.0f} hab.<extra></extra>",
        customdata=populations_pm10
    )
    layout_pm10 = go.Layout(
        title=dict(
            text='Concentration moyenne annuelle en 2007/2020 de PM10 par commune',
            font=dict(size=24)
        ),
        xaxis=dict(
            title='Population des communes',
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
            zeroline=False,
            zerolinewidth=2,
            zerolinecolor='Gray'
        ),
        annotations=[
            dict(
                x=0.5,
                y=-0.3,
                xref='paper',
                yref='paper',
                text="Liste des communes triées par population croissante",
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




    #"""

    #       PASSAGE POUR LA CREATION DES HISTOGRAMMES NO2 ET PM10

    #"""


################### Création des histogrammes pour NO2
    no2_bins = [10, 15, 20, 25, 30, 35, 40, 45]  # Définition des intervalles
    no2_data = data['Moyenne annuelle de concentration de NO2 (ug/m3)']
    no2_hist_values = np.histogram(no2_data[no2_data.between(15, 45)], bins=no2_bins)[0]
    no2_bin_labels = ['10-20', '15-20', '20-25', '25-30', '30-35', '35-40', '40-45']
    
    # Calculer le nombre de valeurs hors intervalles
    no2_below = np.sum(no2_data < 10)
    no2_above = np.sum(no2_data > 45)

    trace_hist_no2 = go.Bar(
        x=no2_bin_labels,
        y=no2_hist_values,
        name='NO2',
        text=no2_hist_values,  # Ajouter le nombre exact sur chaque barre
        textposition='auto',
        hovertemplate="Intervalle: %{x}<br>" +
                     "Nombre de communes: %{y}<br>" +
                     "<extra></extra>"
    )

    layout_hist_no2 = go.Layout(
        title=dict(
            text='Distribution des communes par concentration de NO2',
            font=dict(size=24)
        ),
        xaxis=dict(
            title='Concentration NO2 (µg/m³)',
            tickangle=0
        ),
        yaxis=dict(
            title='Nombre de communes',
            gridcolor='LightGray'
        ),
        bargap=0.1,
        annotations=[
            dict(
                x=0.5,
                y=-0.15,
                xref='paper',
                yref='paper',
                text=f"Communes avec concentrations < 15 µg/m³ : {no2_below}<br>" +
                     f"Communes avec concentrations > 45 µg/m³ : {no2_above}",
                showarrow=False,
                font=dict(size=12),
                align='center'
            )
        ],
        margin=dict(b=100)
    )
    # Créer et sauvegarder l'histogramme NO2
    fig_hist_no2 = go.Figure(data=[trace_hist_no2], layout=layout_hist_no2)
    write_html(fig_hist_no2, file='NO2_histogram.html', auto_open=True, include_plotlyjs='cdn')
    print("Histogramme NO2 généré avec succès !")




###################"" Création des histogrammes pour PM10
    pm10_bins = [10, 15, 20, 25, 30, 35, 40, 45]  # Mêmes intervalles pour la cohérence
    pm10_data = data['Moyenne annuelle de concentration de PM10 (ug/m3)']
    pm10_hist_values = np.histogram(pm10_data[pm10_data.between(10, 45)], bins=pm10_bins)[0]
    pm10_bin_labels = ['10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40-45']
    
    # Calculer le nombre de valeurs hors intervalles
    pm10_below = np.sum(pm10_data < 10)
    pm10_above = np.sum(pm10_data > 45)

    trace_hist_pm10 = go.Bar(
        x=pm10_bin_labels,
        y=pm10_hist_values,
        name='PM10',
        text=pm10_hist_values,  # Ajouter le nombre exact sur chaque barre
        textposition='auto',
        marker_color='rgb(55, 83, 109)',  # Couleur différente pour distinguer de NO2
        hovertemplate="Intervalle: %{x}<br>" +
                     "Nombre de communes: %{y}<br>" +
                     "<extra></extra>"
    )

    layout_hist_pm10 = go.Layout(
        title=dict(
            text='Distribution des communes par concentration de PM10',
            font=dict(size=24)
        ),
        xaxis=dict(
            title='Concentration PM10 (µg/m³)',
            tickangle=0
        ),
        yaxis=dict(
            title='Nombre de communes',
            gridcolor='LightGray'
        ),
        bargap=0.1,
        annotations=[
            dict(
                x=0.5,
                y=-0.15,
                xref='paper',
                yref='paper',
                text=f"Communes avec concentrations < 15 µg/m³ : {pm10_below}<br>" +
                     f"Communes avec concentrations > 45 µg/m³ : {pm10_above}",
                showarrow=False,
                font=dict(size=12),
                align='center'
            )
        ],
        margin=dict(b=100)
    )

    # Créer et sauvegarder l'histogramme PM10
    fig_hist_pm10 = go.Figure(data=[trace_hist_pm10], layout=layout_hist_pm10)
    write_html(fig_hist_pm10, file='PM10_histogram.html', auto_open=True, include_plotlyjs='cdn')
    print("Histogramme PM10 généré avec succès !")

