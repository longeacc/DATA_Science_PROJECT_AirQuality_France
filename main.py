# """
# Script principal pour l'analyse des données de qualité de l'air en France.
# """

# import pandas as pd
# import os
# from plotly.io import write_html
# from src.utils.common_functions import load_commune_mappings, load_data_for_year
# from src.visualizations.scatter_plots import create_pollution_scatter
# from src.visualizations.histograms import create_pollution_histogram


# def main():
#     """
#     Fonction principale du script.
#     """
#     try:
#         # Charger les données pour toutes les années
#         print("\nChargement des données pour toutes les années...")
#         data = pd.DataFrame()
        
#         # Charger les correspondances des communes (utilisation de l'année 2000 comme référence)
#         commune_to_insee, insee_to_commune = load_commune_mappings()
        
#         if commune_to_insee is None or insee_to_commune is None:
#             print("Erreur : Impossible de charger les correspondances des communes.")
#             return
        
#         print(f"Correspondances des communes chargées avec succès :")
#         print(f"- Nombre de communes : {len(commune_to_insee)}")
#         print("Exemples de correspondances :")
#         for commune, code_insee in list(commune_to_insee.items())[:3]:
#             print(f"  {commune} -> {code_insee}")
        
#         for year in range(2000, 2016):
#             if year == 2006:
#                 continue  # Ignorer l'année 2006
#             print(f"\nChargement des données pour l'année {year}...")
#             year_data = load_data_for_year(year)
#             if year_data is not None:
#                 # Vérifier que les communes correspondent
#                 communes_manquantes = [commune for commune in year_data['Commune'] 
#                                      if commune not in commune_to_insee]
#                 if communes_manquantes:
#                     print(f"Attention : {len(communes_manquantes)} communes non trouvées dans l'année {year}")
#                     print("Exemples:", communes_manquantes[:3])
                
#                 data = pd.concat([data, year_data], ignore_index=True)
        
#         if not data.empty:
#             # Afficher un résumé des données
#             print(f"\nDimensions totales des données : {data.shape}")
#             print("\nRésumé statistique des colonnes numériques :")
            
#             # Définir les colonnes pour le résumé statistique
#             colonnes_stats = [
#                 'Moyenne annuelle de concentration de NO2 (ug/m3)',
#                 'Moyenne annuelle de concentration de PM10 (ug/m3)',
#                 'Moyenne annuelle de concentration de O3 (ug/m3)',
#                 'Moyenne annuelle de somo 35 (ug/m3.jour)',
#                 'Moyenne annuelle d\'AOT 40 (ug/m3.heure)',
#                 'Population'
#             ]
            
#             # Ajouter PM2.5 pour les années >= 2009
#             données_récentes = data[data['Année'] >= 2009].copy()
#             if 'Moyenne annuelle de concentration de PM25 (ug/m3)' in données_récentes.columns:
#                 print("\nRésumé statistique pour PM25 (2009-2015) :")
#                 print(données_récentes['Moyenne annuelle de concentration de PM25 (ug/m3)'].describe())
            
#             # Résumé pour les autres polluants (toutes années)
#             print("\nRésumé statistique pour les autres polluants (2000-2015) :")
#             colonnes_disponibles = [col for col in colonnes_stats if col in data.columns]
#             print(data[colonnes_disponibles].describe())
            
#             # Créer le dossier de sortie s'il n'existe pas
#             script_dir = os.path.dirname(os.path.abspath(__file__))
#             output_dir = os.path.join(script_dir, 'assets', 'html_histograms')
#             os.makedirs(output_dir, exist_ok=True)
#             print(f"\nDossier de sortie créé : {output_dir}")
            
#             # Définir les polluants et leurs périodes
#             print("\nCréation des visualisations...")
#             années = sorted(data['Année'].unique())
#             polluants_tous = ['NO2', 'PM10', 'O3', 'Somo 35', 'AOT 40']  # Polluants pour 2000-2015
#             polluant_2009 = 'PM25'  # Polluant uniquement pour 2009-2015
            
#             # Mapping des noms de polluants vers les noms de colonnes exacts du CSV
#             noms_colonnes = {
#                 'NO2': 'Moyenne annuelle de concentration de NO2 (ug/m3)',
#                 'PM10': 'Moyenne annuelle de concentration de PM10 (ug/m3)',
#                 'O3': 'Moyenne annuelle de concentration de O3 (ug/m3)',
#                 'Somo 35': 'Moyenne annuelle de somo 35 (ug/m3.jour)',
#                 'AOT 40': "Moyenne annuelle d'AOT 40 (ug/m3.heure)",
#                 'PM25': 'Moyenne annuelle de concentration de PM25 (ug/m3)'
#             }
            
#             for année in années:
#                 print(f"\nTraitement de l'année {année}...")
#                 # Filtrer les données pour l'année en cours
#                 données_année = data[data['Année'] == année]
                
#                 # Déterminer les polluants à traiter pour cette année
#                 polluants_à_traiter = polluants_tous.copy()  # NO2, PM10, O3, Somo35, AOT40 pour toutes les années
#                 if année >= 2009:
#                     polluants_à_traiter.append(polluant_2009)  # Ajouter PM25 uniquement à partir de 2009
                
#                 for polluant in polluants_à_traiter:
#                     # Obtenir le nom exact de la colonne depuis le mapping
#                     colonne = noms_colonnes[polluant]
                    
#                     # Vérifier si les données sont disponibles pour ce polluant
#                     if colonne not in données_année.columns:
#                         print(f"  Données non disponibles pour {polluant} en {année}")
#                         continue
                        
#                     print(f"  Génération des graphiques pour {polluant}...")
                    
#                     try:
#                         # Créer et sauvegarder le graphique de dispersion
#                         fig_scatter = create_pollution_scatter(données_année, insee_to_commune, polluant)
#                         scatter_file = os.path.join(output_dir, f'{polluant}_moyenne_annuelle_{année}.html')
#                         write_html(fig_scatter, scatter_file, auto_open=False, include_plotlyjs='cdn')
                        
#                         # Créer et sauvegarder l'histogramme
#                         fig_hist = create_pollution_histogram(données_année, polluant)
#                         hist_file = os.path.join(output_dir, f'{polluant}_histogram_{année}.html')
#                         write_html(fig_hist, hist_file, auto_open=False, include_plotlyjs='cdn')
                        
#                         print(f"  ✓ Graphiques générés avec succès pour {polluant}")
#                     except Exception as e:
#                         print(f"  ✗ Erreur lors de la génération des graphiques pour {polluant} : {str(e)}")
            
#             print("\nToutes les visualisations ont été générées avec succès !")
#             print("Les fichiers HTML ont été créés dans le dossier 'output'.")
#         else:
#             print("Erreur : impossible de charger les données ou les correspondances de communes.")
            
#     except Exception as e:
#         print(f"Une erreur s'est produite : {str(e)}")


# if __name__ == "__main__":
#     main() 
# --- À AJOUTER À LA FIN DE TON main.py EXISTANT ---
# create_sample_histograms.py
import dash
from dash import dcc, html, Input, Output
import os
import base64

# Configuration des chemins
output_dir = "output/FINAL_superposed_graphs_map"
html_source_dir = "output_csv"

print("🚀 Initialisation du dashboard...")

# Polluants disponibles
pollutants = ["NO2", "PM10", "O3", "somo 35", "PM25", "AOT 40"]
years = list(range(2000, 2016))
if 2006 in years:
    years.remove(2006)

app = dash.Dash(__name__, title="Dashboard Pollution")

# Layout SIMPLE avec carte intégrée
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
    
    # Section Histogrammes
    html.Div([
        html.H3("📊 Histogrammes des Polluants", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
        
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
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
            
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
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
        
        # Histogramme
        html.Iframe(
            id='graph-frame',
            style={'width': '100%', 'height': '600px', 'border': 'none', 'borderRadius': '8px', 'marginTop': '20px'}
        )
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px'})
])

# Callback pour l'année
@app.callback(
    Output('year-display', 'children'),
    [Input('year-slider', 'value')]
)
def update_year_display(year_index):
    return f"Année: {years[year_index]}"

# Callback pour l'histogramme
@app.callback(
    Output('graph-frame', 'src'),
    [Input('pollutant-select', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(pollutant, year_index):
    year = years[year_index]
    pollutant_clean = pollutant.replace(' ', '_')
    filename = f"{pollutant_clean}_histogram_{year}.html"
    filepath = os.path.join("assets", "html_histograms", filename)
    
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

if __name__ == '__main__':
    print("🌐 Démarrage du serveur...")
    print("📍 Accédez à: http://127.0.0.1:8050")
    app.run(debug=True, host='127.0.0.1', port=8050)