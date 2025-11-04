import plotly.graph_objects as go
import numpy as np
from plotly.io import write_html

def create_pollution_histogram(data, pollutant_type):
    """
    Crée un histogramme pour NO2 ou PM10
    
    Args:
        data (pd.DataFrame): Le DataFrame contenant les données
        pollutant_type (str): Type de polluant ("NO2" ou "PM10")
    
    Returns:
        plotly.graph_objects.Figure: La figure créée
    """
    column_name = f'Moyenne annuelle de concentration de {pollutant_type} (ug/m3)'
    pollutant_data = data[column_name]
    
    # Définir les intervalles
    start_value = 10 if pollutant_type == "NO2" else 10
    bins = list(range(start_value, 50, 5))
    bin_labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins)-1)]
    
    # Calculer l'histogramme
    hist_values = np.histogram(pollutant_data[pollutant_data.between(10, 70)], bins=bins)[0]
    
    # Calculer les valeurs hors intervalles
    below = np.sum(pollutant_data < 10)
    above = np.sum(pollutant_data > 75)

    trace = go.Bar(
        x=bin_labels,
        y=hist_values,
        name=pollutant_type,
        text=hist_values,
        textposition='auto',
        hovertemplate="Intervalle: %{x}<br>Nombre de communes: %{y}<br><extra></extra>"
    )

    layout = go.Layout(
        title=dict(
            text=f'Distribution des communes par concentration de {pollutant_type}',
            font=dict(size=24)
        ),
        xaxis=dict(title=f'Concentration {pollutant_type} (µg/m³)'),
        yaxis=dict(title='Nombre de communes'),
        annotations=[dict(
            x=0.5,
            y=-0.15,
            xref='paper',
            yref='paper',
            text=f"Communes avec concentrations < 15 µg/m³ : {below}<br>"
                 f"Communes avec concentrations > 45 µg/m³ : {above}",
            showarrow=False,
            font=dict(size=12),
            align='center'
        )],
        margin=dict(b=100)
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig