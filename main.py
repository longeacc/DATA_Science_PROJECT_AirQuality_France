# """
# Script pour générer des graphiques de pollution en France.
# Crée des histogrammes et des scatter plots pour chaque polluant et année.
# """

# import pandas as pd
# import os
# from plotly.io import write_html
# from src.utils.common_functions import load_commune_mappings, load_data_for_year
# from src.visualizations.scatter_plots import create_pollution_scatter
# from src.visualizations.histograms import create_pollution_histogram

# def main():
#     """
#     Fonction principale du script pour générer des graphiques.
#     """
#     try:
#         print("\nChargement des données pour toutes les années...")
#         data = pd.DataFrame()
        
#         commune_to_insee, insee_to_commune = load_commune_mappings()
#         if commune_to_insee is None or insee_to_commune is None:
#             print("Erreur : Impossible de charger les correspondances des communes.")
#             return
        
#         print(f"Correspondances des communes chargées : {len(commune_to_insee)} communes")
        
#         for year in range(2000, 2016):
#             if year == 2006:
#                 continue
#             print(f"\nChargement des données pour l'année {year}...")
#             year_data = load_data_for_year(year)
#             if year_data is not None:
#                 communes_manquantes = [c for c in year_data['Commune'] if c not in commune_to_insee]
#                 if communes_manquantes:
#                     print(f"Attention : {len(communes_manquantes)} communes non trouvées en {year}")
#                 data = pd.concat([data, year_data], ignore_index=True)
        
#         if data.empty:
#             print("Erreur : aucune donnée chargée.")
#             return

#         # Créer les dossiers de sortie
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         output_hist_dir = os.path.join(script_dir, 'assets', 'html_histograms')
#         output_scatter_dir = os.path.join(script_dir, 'assets', 'scatter')
#         os.makedirs(output_hist_dir, exist_ok=True)
#         os.makedirs(output_scatter_dir, exist_ok=True)
#         print(f"Dossiers créés :\n- Histogrammes : {output_hist_dir}\n- Scatter : {output_scatter_dir}")

#         # Polluants et colonnes
#         polluants_tous = ['NO2', 'PM10', 'O3', 'Somo 35', 'AOT 40']
#         polluant_2009 = 'PM25'
#         noms_colonnes = {
#             'NO2': 'Moyenne annuelle de concentration de NO2 (ug/m3)',
#             'PM10': 'Moyenne annuelle de concentration de PM10 (ug/m3)',
#             'O3': 'Moyenne annuelle de concentration de O3 (ug/m3)',
#             'Somo 35': 'Moyenne annuelle de somo 35 (ug/m3.jour)',
#             'AOT 40': "Moyenne annuelle d'AOT 40 (ug/m3.heure)",
#             'PM25': 'Moyenne annuelle de concentration de PM25 (ug/m3)'
#         }

#         années = sorted(data['Année'].unique())
#         for année in années:
#             print(f"\nTraitement de l'année {année}...")
#             données_année = data[data['Année'] == année]
            
#             polluants_à_traiter = polluants_tous.copy()
#             if année >= 2009:
#                 polluants_à_traiter.append(polluant_2009)
            
#             for polluant in polluants_à_traiter:
#                 colonne = noms_colonnes[polluant]
#                 if colonne not in données_année.columns:
#                     print(f"  Données non disponibles pour {polluant} en {année}")
#                     continue
                
#                 try:
#                     # Scatter plot
#                     fig_scatter = create_pollution_scatter(données_année, insee_to_commune, polluant)
#                     scatter_file = os.path.join(output_scatter_dir, f'{polluant}_scatter_{année}.html')
#                     write_html(fig_scatter, scatter_file, auto_open=False, include_plotlyjs='cdn')
                    
#                     # Histogramme
#                     fig_hist = create_pollution_histogram(données_année, polluant)
#                     hist_file = os.path.join(output_hist_dir, f'{polluant}_histogram_{année}.html')
#                     write_html(fig_hist, hist_file, auto_open=False, include_plotlyjs='cdn')
                    
#                     print(f"  ✓ Graphiques générés pour {polluant}")
#                 except Exception as e:
#                     print(f"  ✗ Erreur lors de la génération des graphiques pour {polluant} : {e}")

#         print("\nToutes les visualisations ont été générées avec succès !")
        
#     except Exception as e:
#         print(f"Une erreur s'est produite : {e}")


# if __name__ == "__main__":
#     main()

# --- À AJOUTER À LA FIN DE TON main.py EXISTANT ---
# create_sample_histograms.py
import dash
from dash import dcc, html, Input, Output
import os
import base64
import webbrowser

# ---------------------------
# Configuration des chemins
# ---------------------------
output_dir = "output/FINAL_superposed_graphs_map"
html_source_dir = "output_csv"
histogram_dir = os.path.join("assets", "html_histograms")
scatter_dir = os.path.join("assets", "scatter")

# ---------------------------
# Polluants et années
# ---------------------------
pollutants = ["NO2", "PM10", "O3", "somo 35", "PM25", "AOT 40"]
years = list(range(2000, 2016))
if 2006 in years:
    years.remove(2006)




# ---------------------------
# Polluants et années
# ---------------------------
pollutants = ["NO2", "PM10", "O3", "somo 35", "PM25", "AOT 40"]
years = list(range(2000, 2016))
if 2006 in years:
    years.remove(2006)

# ---------------------------
# Mapping pour correspondre au nom exact du fichier
# ---------------------------
pollutant_file_map = {
    "NO2": "NO2",
    "PM10": "PM10",
    "O3": "O3",
    "somo 35": "Somo 35",
    "PM25": "PM25",
    "AOT 40": "AOT 40"
}


# ---------------------------
# Initialisation Dash
# ---------------------------
app = dash.Dash(__name__, title="Dashboard Pollution")

# ---------------------------
# Fonction page d'erreur
# ---------------------------
def create_error_page(message):
    error_html = f"""
    <html>
    <body style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column; font-family: Arial;">
        <div style="text-align: center; padding: 40px;">
            <h2 style="color: #e74c3c;">📊 Erreur</h2>
            <p>{message}</p>
        </div>
    </body>
    </html>
    """
    error_encoded = base64.b64encode(error_html.encode()).decode()
    return f"data:text/html;base64,{error_encoded}"

# ---------------------------
# Layout
# ---------------------------
app.layout = html.Div([
    # En-tête
    html.Div([
        html.H1("📊 Dashboard Pollution Atmosphérique - France", 
                style={'textAlign': 'center', 'color': 'white', 'marginBottom': '10px'}),
        html.P("Visualisation interactive des données de qualité de l'air (2000-2015)",
               style={'textAlign': 'center', 'color': 'white', 'fontSize': '16px'})
    ], style={'backgroundColor': '#2c3e50', 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px'}),
    
    # Section Carte
    html.Div([
        html.H3("🗺️ Carte Interactive de la Pollution", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px'}),
        html.Iframe(
            src="/assets/interactive_pollution_map.html",
            style={'width': '100%', 'height': '700px', 'border': 'none', 'borderRadius': '8px'}
        )
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),
    
    # Section Graphiques (Histogrammes et Scatter)
    html.Div([
        html.H3("📊 Graphiques des Polluants", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
        
        # Contrôles
        html.Div([
            html.Div([
                html.Label("🧪 Polluant:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='pollutant-select',
                    options=[{'label': p, 'value': p} for p in pollutants],
                    value='NO2',
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px'}),
            
            html.Div([
                html.Label("📅 Année:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Slider(
                    id='year-slider',
                    min=0,
                    max=len(years)-1,
                    value=0,
                    marks={i: str(year) for i, year in enumerate(years)},
                    step=1
                ),
                html.Div(id='year-display', style={'textAlign': 'center', 'fontSize': '16px', 'fontWeight': 'bold', 'marginTop': '10px'})
            ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px'}),
            
            html.Div([
                html.Label("📊 Type de graphique:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.RadioItems(
                    id='graph-type',
                    options=[{'label': 'Histogramme', 'value': 'histogram'},
                             {'label': 'Scatter Plot', 'value': 'scatter'}],
                    value='histogram',
                    labelStyle={'display': 'inline-block', 'marginRight': '10px'}
                )
            ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px'})
        ]),
        
        # IFrame Graphique
        html.Iframe(
            id='graph-frame',
            style={'width': '100%', 'height': '600px', 'border': 'none', 'borderRadius': '8px', 'marginTop': '20px'}
        )
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px'})
])

# ---------------------------
# Callbacks
# ---------------------------
@app.callback(
    Output('year-display', 'children'),
    Input('year-slider', 'value')
)
def update_year_display(year_index):
    return f"Année: {years[year_index]}"

@app.callback(
    Output('graph-frame', 'src'),
    [Input('pollutant-select', 'value'),
     Input('year-slider', 'value'),
     Input('graph-type', 'value')]
)
def update_graph(pollutant, year_index, graph_type):
    year = years[year_index]
    pollutant_clean = pollutant_file_map.get(pollutant, pollutant)
    
    if graph_type == 'histogram':
        filename = f"{pollutant_clean}_histogram_{year}.html"
        filepath = os.path.join(histogram_dir, filename)
    else:
        filename = f"{pollutant_clean}_scatter_{year}.html"
        filepath = os.path.join(scatter_dir, filename)
    
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            html_encoded = base64.b64encode(html_content.encode()).decode()
            return f"data:text/html;base64,{html_encoded}"
        except Exception as e:
            return create_error_page(f"Erreur: {str(e)}")
    else:
        return create_error_page(f"Fichier non trouvé: {filename}")

# ---------------------------
# Lancer le serveur et ouvrir automatiquement le navigateur
# ---------------------------
if __name__ == '__main__':
    url = "http://127.0.0.1:8050"
    print("🌐 Démarrage du serveur Dash...")
    print(f"📍 Accédez à: {url}")
    
    # Ouvre le navigateur automatiquement
    webbrowser.open(url)
    
    # Lancer le serveur Dash
    app.run(debug=True, host='127.0.0.1', port=8050, use_reloader=False)
