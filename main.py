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
#             output_dir = os.path.join(script_dir, 'output')
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
import os

def create_map_histogram_dashboard():
    output_dir = "output/FINAL_superposed_graphs_map"
    os.makedirs(output_dir, exist_ok=True)
    
    html_path = os.path.join(output_dir, "FINAL_dashboard_map_histograms.html")
    
    html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Dashboard Map & Histogrammes</title>
<style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
    .header { background: #2c3e50; color: white; padding: 20px; text-align: center; }
    .container { display: flex; height: calc(100vh - 80px); }
    .map-container { flex: 1; padding: 10px; }
    .map-container iframe { width: 100%; height: 100%; border: none; border-radius: 8px; }
    .histogram-container { flex: 1; display: flex; flex-direction: column; padding: 10px; }
    .tabs { display: flex; margin-bottom: 10px; }
    .tab { padding: 10px 15px; cursor: pointer; background: #34495e; color: white; margin-right: 5px; border-radius: 5px; transition: background 0.3s; }
    .tab.active { background: #3498db; font-weight: bold; }
    .tab:hover { background: #2980b9; }
    iframe.histogram-frame { flex: 1; width: 100%; border: none; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
</style>
</head>
<body>

<div class="header">
    <h1>📊 Dashboard Polluants Atmosphériques & Carte</h1>
</div>

<div class="container">
    <div class="map-container">
        <iframe src="interactive_pollution_map.html" id="map-frame"></iframe>
    </div>
    
    <div class="histogram-container">
        <div class="tabs">
            <div class="tab active" data-src="FINAL_histogrammes_viewer.html">Histogrammes</div>
            <div class="tab" data-src="AUTRE_FICHIER.html">Autre Visualisation</div>
        </div>
        <iframe src="FINAL_histogrammes_viewer.html" class="histogram-frame" id="histogram-frame"></iframe>
    </div>
</div>

<script>
    const tabs = document.querySelectorAll('.tab');
    const histFrame = document.getElementById('histogram-frame');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            histFrame.src = tab.getAttribute('data-src');
        });
    });
</script>

</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Dashboard Map & Histogrammes créé : {html_path}")

if __name__ == "__main__":
    create_map_histogram_dashboard()
