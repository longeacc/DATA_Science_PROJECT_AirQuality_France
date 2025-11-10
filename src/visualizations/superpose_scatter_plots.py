import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
import os

def create_pollution_scatter_animation(data, insee_to_commune, pollutant_type):
    """
    Crée un graphique de dispersion animé pour visualiser l'évolution d'un polluant de 2000 à 2015.
    
    Args:
        data (pd.DataFrame): Le DataFrame contenant les données de toutes les années
        insee_to_commune (dict): Dictionnaire de correspondance codes INSEE vers noms de communes
        pollutant_type (str): Type de polluant
    
    Returns:
        plotly.graph_objects.Figure: La figure créée avec animation
    """
    # Filtrer les communes avec plus de 1500 habitants
    data = data[data['Population'] > 1500]
    
    # Déterminer le nom de la colonne selon le type de polluant
    if pollutant_type == 'Somo 35':
        column_name = 'Moyenne annuelle de somo 35 (ug/m3.jour)'
    elif pollutant_type == 'AOT 40':
        column_name = "Moyenne annuelle d'AOT 40 (ug/m3.heure)"
    else:
        column_name = f'Moyenne annuelle de concentration de {pollutant_type} (ug/m3)'
    
    # Créer la figure
    fig = go.Figure()
    
    # Liste des années disponibles (en excluant 2006)
    years = sorted(list(set(data['Année'].unique()) - {2006}))
    
    # Pour chaque année, ajouter une trace (initialement invisible)
    for year in years:
        year_data = data[data['Année'] == year].sort_values('Population', ascending=True)
        communes = [insee_to_commune[code] for code in year_data['COM Insee']]
        concentrations = year_data[column_name]
        populations = year_data['Population']
        
        fig.add_trace(
            go.Scatter(
                x=communes,
                y=concentrations,
                mode='markers',
                name=f'Mesures {pollutant_type} - {year}',
                marker=dict(
                    size=2,
                    color=concentrations,
                    colorscale=[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']],
                    showscale=True if year == years[-1] else False
                ),
                hovertemplate="<b>%{x}</b><br>" +
                             f"{pollutant_type}: %{{y:.1f}} µg/m³<br>" +
                             "Population: %{customdata:,.0f} hab.<br>" +
                             f"Année: {year}<extra></extra>",
                customdata=populations,
                visible=False
            )
        )
    
    # Rendre la première trace visible
    fig.data[0].visible = True
    
    # Créer les steps pour le slider
    steps = []
    for i, year in enumerate(years):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"title": f"Concentration moyenne annuelle de {pollutant_type} par commune - {year}"}],
            label=str(year)
        )
        step["args"][0]["visible"][i] = True
        steps.append(step)
    
    # Créer le slider
    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Année: "},
        pad={"t": 50},
        steps=steps
    )]
    
    # Préparation du titre et des unités selon le type de polluant
    if pollutant_type == 'Somo 35':
        titre_global = 'Valeurs de SOMO35 en fonction de la population (2000-2015)'
        unite = 'µg/m³·jour'
        hover_text = "SOMO35"
    elif pollutant_type == 'AOT 40':
        titre_global = 'Valeurs d\'AOT40 en fonction de la population (2000-2015)'
        unite = 'µg/m³·heure'
        hover_text = "AOT40"
    elif pollutant_type == 'PM25':
        titre_global = 'Concentration de PM2.5 en fonction de la population (2000-2015)'
        unite = 'µg/m³'
        hover_text = "PM2.5"
    else:
        titre_global = f'Concentration de {pollutant_type} en fonction de la population (2000-2015)'
        unite = 'µg/m³'
        hover_text = pollutant_type

    # Mise à jour des textes de survol pour tous les points
    for trace in fig.data:
        trace.hovertemplate = (
            "<b>%{text}</b><br>" +
            f"{hover_text}: %{{y:.1f}} {unite}<br>" +
            "Population: %{x:,.0f} hab.<br>" +
            f"Année: {trace.name.split(' - ')[1]}<extra></extra>"
        )

    # Créer les steps pour le slider
    steps = []
    for year in years:
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}],
            label=str(year)
        )
        step["args"][0]["visible"][years.index(year)] = True
        steps.append(step)

    # Mise à jour du layout
    fig.update_layout(
        title=dict(
            text=titre_global,
            font=dict(size=24),
            y=0.95  # Position du titre principal en haut
        ),
        margin=dict(t=150),  # Marge supérieure pour le titre et le slider
        xaxis=dict(
            title='Population (habitants)',
            type='log',  # Échelle logarithmique pour la population
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        yaxis=dict(
            title=f'Valeur ({unite})',
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        showlegend=False,
        sliders=[dict(
            active=0,
            currentvalue={"prefix": "Année: ", "xanchor": "right"},
            pad={"t": 0, "b": 10},
            yanchor="top",
            y=0.85,  # Position du slider sous le titre principal
            x=0.05,
            len=0.9,  # Longueur du slider
            steps=steps
        )]
    )
    
    
    return fig

if __name__ == "__main__":
    # Liste des polluants à traiter
    polluants = ['NO2', 'PM10', 'O3']
    
    # Dossier de sortie des graphiques
    output_dir = '../output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Charger les données
    data_file = '../data/processed/pollution_data_all_years.csv'
    insee_file = '../data/processed/insee_to_commune.json'
    
    data = pd.read_csv(data_file)
    with open(insee_file, 'r', encoding='utf-8') as f:
        insee_to_commune = json.load(f)
    
    # Générer les scatter plots superposés pour chaque polluant
    for polluant in polluants:
        print(f"Génération du scatter plot superposé pour {polluant}...")
        try:
            fig = create_pollution_scatter_animation(data, insee_to_commune, polluant)
            fig.write_html(os.path.join(output_dir, f'{polluant}_scatter_superposes.html'))
            print(f"  ✓ Scatter plot superposé généré pour {polluant}")
        except Exception as e:
            print(f"  ✗ Erreur lors de la génération du scatter plot superposé pour {polluant}: {str(e)}")
    
    print("\nTerminé ! Les graphiques de moyennes annuelles superposés ont été générés dans le dossier 'output'.")