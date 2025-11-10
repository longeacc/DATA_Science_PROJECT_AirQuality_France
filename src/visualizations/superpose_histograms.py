import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from bs4 import BeautifulSoup
import re
import ast

def extract_data_from_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Rechercher le pattern des données dans le script Plotly
            data_match = re.search(r'var data = \[(.*?)\];', content, re.DOTALL)
            if data_match:
                data_str = data_match.group(1)
                # Extraire x des données
                x_match = re.search(r'"x":\s*(\[.*?\])', data_str)
                if x_match:
                    try:
                        # Nettoyer et évaluer les données de façon sûre
                        x_data = ast.literal_eval(x_match.group(1))
                        return x_data
                    except Exception as e:
                        print(f"Erreur lors de l'évaluation des données pour {file_path}: {e}")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
    return []

def create_superposed_histograms():
    output_dir = "../../output"
    pollutants = ["NO2", "AOT 40"]
    years = list(range(2000, 2016))
    years.remove(2006)  # Année manquante

    # Créer une figure avec deux sous-graphiques (un pour chaque polluant)
    fig = make_subplots(rows=2, cols=1, subplot_titles=pollutants)

    # Créer un dictionnaire pour stocker toutes les traces
    all_traces = {pollutant: {} for pollutant in pollutants}

    # Charger toutes les données
    for pollutant in pollutants:
        for year in years:
            filename = f"{pollutant}_histogram_{year}.html"
            file_path = os.path.join(output_dir, filename)
            if os.path.exists(file_path):
                x_data = extract_data_from_html(file_path)
                if x_data:
                    trace = go.Histogram(
                        x=x_data,
                        name=f'{year}',
                        opacity=0.7,
                        nbinsx=30,
                        visible=True if year == years[0] else False
                    )
                    all_traces[pollutant][year] = trace

    # Ajouter les traces aux sous-graphiques
    for i, pollutant in enumerate(pollutants, 1):
        for year in years:
            if year in all_traces[pollutant]:
                fig.add_trace(all_traces[pollutant][year], row=i, col=1)

    # Créer les steps pour le slider
    steps = []
    for i, year in enumerate(years):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                 {"title": f"Concentration de {', '.join(pollutants)} pour l'année {year}"}],
            label=str(year)
        )
        # Rendre visible uniquement les traces correspondant à l'année sélectionnée
        for j, pollutant in enumerate(pollutants):
            if year in all_traces[pollutant]:
                trace_index = years.index(year) + j * len(years)
                if trace_index < len(fig.data):
                    step["args"][0]["visible"][trace_index] = True
        steps.append(step)

    # Ajouter le slider
    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Année: "},
        pad={"t": 50},
        steps=steps
    )]

    # Mise à jour de la mise en page
    fig.update_layout(
        height=800,
        sliders=sliders,
        title_text="Distribution des polluants par année",
        showlegend=False,
        barmode='overlay'
    )

    # Mise à jour des axes
    for i, pollutant in enumerate(pollutants, 1):
        fig.update_xaxes(title_text=f"Concentration en {pollutant}", row=i, col=1)
        fig.update_yaxes(title_text="Nombre de communes", row=i, col=1)

    # Sauvegarder la figure interactive
    fig.write_html("superposed_histograms.html")

if __name__ == "__main__":
    create_superposed_histograms()