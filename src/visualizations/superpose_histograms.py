import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

def create_pollution_histogram_animation(data, pollutant_type):
    """
    Crée un histogramme animé pour visualiser la distribution d'un polluant de 2000 à 2015.
    
    Args:
        data (pd.DataFrame): Le DataFrame contenant les données de toutes les années
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
        year_data = data[data['Année'] == year]
        values = year_data[column_name]
        
        fig.add_trace(
            go.Histogram(
                x=values,
                name=f'Distribution {pollutant_type} - {year}',
                nbinsx=30,
                marker_color='rgb(70, 130, 180)',
                hovertemplate="<b>Concentration</b>: %{x:.1f} µg/m³<br>" +
                             "Nombre de communes: %{y}<br>" +
                             f"Année: {year}<extra></extra>",
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
                  {"title": f"Distribution des concentrations de {pollutant_type} - {year}"}],
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
    
    # Mise à jour du layout
    fig.update_layout(
        title=dict(
            text=f'Distribution des concentrations de {pollutant_type} - {years[0]}',
            font=dict(size=24)
        ),
        xaxis=dict(
            title=f'Concentration de {pollutant_type} (µg/m³)',
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        yaxis=dict(
            title='Nombre de communes',
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        showlegend=False,
        sliders=sliders
    )
    
    # Ajouter une ligne verticale pour la moyenne (qui se déplacera avec l'animation)
    for year in years:
        year_data = data[data['Année'] == year]
        mean_value = year_data[column_name].mean()
        
        fig.add_vline(
            x=mean_value,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Moyenne: {mean_value:.1f}",
            annotation_position="top right",
            visible=False
        )
    
    # Rendre visible la ligne de la première année
    fig.data[len(years)].visible = True
    
    return fig

if __name__ == "__main__":
    # Liste des polluants à traiter
    polluants = ['NO2', 'PM10', 'O3',]
    
    # Dossier de sortie des graphiques
    output_dir = '../output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Charger les données
    data_file = '../data/processed/pollution_data_all_years.csv'
    data = pd.read_csv(data_file)
    
    # Générer les histogrammes superposés pour chaque polluant
    for polluant in polluants:
        print(f"Génération de l'histogramme superposé pour {polluant}...")
        try:
            fig = create_pollution_histogram_animation(data, polluant)
            fig.write_html(os.path.join(output_dir, f'{polluant}_histogrammes_superposes.html'))
            print(f"  ✓ Histogramme superposé généré pour {polluant}")
        except Exception as e:
            print(f"  ✗ Erreur lors de la génération de l'histogramme superposé pour {polluant}: {str(e)}")
    
    print("\nTerminé ! Les histogrammes superposés ont été générés dans le dossier 'output'.")