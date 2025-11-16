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
# Chemins des fichiers
# ---------------------------
histogram_dir = os.path.join("assets", "html_histograms")
scatter_dir = os.path.join("assets", "scatter")

# Polluants et années
pollutants = ["NO2", "PM10", "O3", "somo 35", "PM25", "AOT 40"]
years = list(range(2000, 2016))
if 2006 in years:
    years.remove(2006)

pollutant_file_map = {p: p if " " not in p else p.title() for p in pollutants}

# ---------------------------
# Dash
# ---------------------------
app = dash.Dash(__name__, title="Dashboard Pollution")

def create_error_page(message):
    html_content = f"""
    <html><body style="display:flex;justify-content:center;align-items:center;height:100vh;">
    <div style="text-align:center;">
    <h2 style="color:red;">Erreur</h2>
    <p>{message}</p>
    </div></body></html>
    """
    encoded = base64.b64encode(html_content.encode()).decode()
    return f"data:text/html;base64,{encoded}"

# ---------------------------
# Layout CORRIGÉ
# ---------------------------
app.layout = html.Div([
    # Header général
    html.Div([
        html.H1("📊 Dashboard Pollution Atmosphérique - France",
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '5px'}),
        html.P("Visualisation interactive des données de qualité de l'air (2000-2015)",
               style={'textAlign': 'center', 'color': '#34495e', 'fontSize': '14px'})
    ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '15px', 'marginBottom': '30px'}),

    # Conteneur principal avec espacement FORCÉ
    html.Div([
        # Section Carte (gauche)
        html.Div([
            html.H3("🗺️ Carte Interactive de la Pollution Atmosphérique en France",
                    style={'marginBottom': '20px', 'color': '#2c3e50', 'textAlign': 'left'}),
            html.Iframe(
                src="/assets/interactive_pollution_map.html",
                style={
                    'width': '95%', 
                    'height': '600px', 
                    'border': 'none', 
                    'borderRadius': '12px',
                    'marginLeft': '20px'  # Espacement à gauche
                }
            )
        ], style={
            'width': '55%', 
            'display': 'inline-block', 
            'verticalAlign': 'top',
            'marginRight': '50px',  # ESPACEMENT IMPORTANT ICI
            'padding': '15px',
            'backgroundColor': 'white',
            'borderRadius': '12px',
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
        }),

        # Section Graphiques et Contrôles (droite)
        html.Div([
            html.H3("📊 Graphiques des Polluants",
                    style={'marginBottom': '25px', 'color': '#2c3e50', 'textAlign': 'left'}),
            
            # Contrôle Polluant avec ESPACEMENT
            html.Div([
                html.Label("🧪 Polluant:", style={
                    'fontWeight': 'bold', 
                    'marginBottom': '10px', 
                    'display': 'block',
                    'fontSize': '16px'
                }),
                dcc.Dropdown(
                    id='pollutant-select',
                    options=[{'label': p, 'value': p} for p in pollutants],
                    value='NO2',
                    clearable=False,
                    style={'width': '100%', 'marginBottom': '30px'}
                ),
            ], style={'marginBottom': '25px'}),
            
            # Contrôle Année avec ESPACEMENT
            html.Div([
                html.Label("📅 Année", style={
                    'fontWeight': 'bold', 
                    'marginBottom': '12px', 
                    'display': 'block',
                    'fontSize': '16px'
                }),
                dcc.Slider(
                    id='year-slider',
                    min=0,
                    max=len(years)-1,
                    value=0,
                    marks={i: str(year) for i, year in enumerate(years)},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode='drag'
                ),
                html.Div(id='year-display',
                         style={
                             'textAlign': 'center', 
                             'fontSize': '16px', 
                             'fontWeight': 'bold', 
                             'marginTop': '15px', 
                             'marginBottom': '30px',
                             'color': '#2c3e50'
                         }),
            ], style={'marginBottom': '25px'}),
            
            # Contrôle Type de graphique avec ESPACEMENT
            html.Div([
                html.Label("📊 Type de graphique", style={
                    'fontWeight': 'bold', 
                    'marginBottom': '12px', 
                    'display': 'block',
                    'fontSize': '16px'
                }),
                dcc.RadioItems(
                    id='graph-type',
                    options=[{'label': 'Histogramme', 'value': 'histogram'},
                             {'label': 'Scatter Plot', 'value': 'scatter'}],
                    value='histogram',
                    labelStyle={
                        'display': 'inline-block', 
                        'marginRight': '20px',
                        'fontSize': '14px'
                    },
                    style={'marginBottom': '25px'}
                ),
            ], style={'marginBottom': '25px'}),
            
            # Graphique
            html.Iframe(
                id='graph-frame',
                style={
                    'width': '100%', 
                    'height': '400px', 
                    'border': 'none', 
                    'borderRadius': '12px', 
                    'marginTop': '10px'
                }
            )
        ], style={
            'width': '40%', 
            'display': 'inline-block', 
            'verticalAlign': 'top',
            'padding': '25px',
            'backgroundColor': 'white',
            'borderRadius': '12px',
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
        }),

    ], style={
        'display': 'flex',
        'justifyContent': 'space-between', 
        'alignItems': 'flex-start',
        'gap': '60px',  # ESPACEMENT GLOBAL
        'padding': '20px 0'
    }),

], style={
    'padding': '20px', 
    'backgroundColor': '#f4f7f9', 
    'minHeight': '100vh'
})

# ---------------------------
# Callbacks
# ---------------------------
@app.callback(Output('year-display', 'children'), Input('year-slider', 'value'))
def update_year_display(year_index):
    return f"Année: {years[year_index]}"

@app.callback(Output('graph-frame', 'src'),
              [Input('pollutant-select', 'value'), Input('year-slider', 'value'), Input('graph-type', 'value')])
def update_graph(pollutant, year_index, graph_type):
    year = years[year_index]
    pollutant_clean = pollutant_file_map.get(pollutant, pollutant)
    filename = f"{pollutant_clean}_{'histogram' if graph_type=='histogram' else 'scatter'}_{year}.html"
    filepath = os.path.join(histogram_dir if graph_type=='histogram' else scatter_dir, filename)

    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        encoded = base64.b64encode(html_content.encode()).decode()
        return f"data:text/html;base64,{encoded}"
    else:
        return create_error_page(f"Fichier non trouvé: {filename}")

# ---------------------------
# Run server
# ---------------------------
if __name__ == '__main__':
    url = "http://127.0.0.1:8050"
    webbrowser.open(url)
    app.run(debug=True, host='127.0.0.1', port=8050, use_reloader=False)