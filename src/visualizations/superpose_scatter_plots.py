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
                # Extraire x et y des données
                x_match = re.search(r'"x":\s*(\[.*?\])', data_str)
                y_match = re.search(r'"y":\s*(\[.*?\])', data_str)
                if x_match and y_match:
                    try:
                        # Nettoyer et évaluer les données de façon sûre
                        x_data = ast.literal_eval(x_match.group(1))
                        y_data = ast.literal_eval(y_match.group(1))
                        return x_data, y_data
                    except Exception as e:
                        print(f"Erreur lors de l'évaluation des données pour {file_path}: {e}")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
    return [], []

def create_superposed_plots():
    output_dir = "../../output"
    pollutants = ["NO2", "AOT 40","PM10","PM25","O3","somo 35"]
    years = list(range(2000, 2016))
    years.remove(2006)  # Année manquante

    # Créer une figure avec sous-graphiques (un pour chaque polluant)
    fig = make_subplots(rows=3, cols=2, subplot_titles=pollutants)

    # Créer un dictionnaire pour stocker toutes les traces
    all_traces = {pollutant: {} for pollutant in pollutants}

    # Charger toutes les données
    for pollutant in pollutants:
        for year in years:
            filename = f"{pollutant}_moyenne_annuelle_{year}.html"
            file_path = os.path.join(output_dir, filename)
            if os.path.exists(file_path):
                x_data, y_data = extract_data_from_html(file_path)
                if x_data and y_data:
                    trace = go.Scatter(
                        x=x_data,
                        y=y_data,
                        mode='markers',
                        name=f'{year}',
                        visible=True if year == years[0] else False
                    )
                    all_traces[pollutant][year] = trace

    # Ajouter les traces aux sous-graphiques
    for i, pollutant in enumerate(pollutants):
        # Calculer la position du sous-graphique
        row = (i // 2) + 1
        col = (i % 2) + 1
        for year in years:
            if year in all_traces[pollutant]:
                fig.add_trace(all_traces[pollutant][year], row=row, col=col)

    # Créer les steps pour le slider
    steps = []
    for i, year in enumerate(years):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                 {"title": f"Données pour l'année {year}"}],
            label=str(year)
        )
        # Rendre visible uniquement les traces correspondant à l'année sélectionnée
        for trace_idx in range(len(fig.data)):
            # Calculer l'année correspondante à cette trace
            pollutant_idx = trace_idx // len(years)
            year_idx = trace_idx % len(years)
            if pollutant_idx < len(pollutants):  # Vérifier si l'index est valide
                pollutant = pollutants[pollutant_idx]
                if year in all_traces[pollutant] and year == years[year_idx]:
                    step["args"][0]["visible"][trace_idx] = True
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
        title_text="Évolution des polluants par année",
        showlegend=False
    )

    # Mise à jour des axes
    for i, pollutant in enumerate(pollutants):
        row = (i // 2) + 1
        col = (i % 2) + 1
        fig.update_xaxes(title_text="Communes > 1500 habitants", row=row, col=col)
        fig.update_yaxes(title_text=f"Concentration en {pollutant}", row=row, col=col)

    # Sauvegarder la figure interactive
    fig.write_html(f"{'_'.join(pollutants)}_superposed_scatter_plots.html")

if __name__ == "__main__":
    create_superposed_plots()