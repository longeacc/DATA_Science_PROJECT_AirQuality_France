"""
Script principal pour l'analyse des données de qualité de l'air en France.
"""

import pandas as pd
import os
from plotly.io import write_html
from src.utils.common_functions import load_commune_mappings, load_data_for_year
from src.visualizations.scatter_plots import create_pollution_scatter
from src.visualizations.histograms import create_pollution_histogram
from src.visualizations.superpose_scatter_plots import create_pollution_scatter_animation
from src.visualizations.superpose_histograms import create_pollution_histogram_animation


def main():
    """
    Fonction principale du script.
    """
    try:
        # Charger les données pour toutes les années
        print("\nChargement des données pour toutes les années...")
        data = pd.DataFrame()
        
        # Charger les correspondances des communes (utilisation de l'année 2000 comme référence)
        commune_to_insee, insee_to_commune = load_commune_mappings()
        
        if commune_to_insee is None or insee_to_commune is None:
            print("Erreur : Impossible de charger les correspondances des communes.")
            return
        
        print(f"Correspondances des communes chargées avec succès :")
        print(f"- Nombre de communes : {len(commune_to_insee)}")
        print("Exemples de correspondances :")
        for commune, code_insee in list(commune_to_insee.items())[:3]:
            print(f"  {commune} -> {code_insee}")
        
        for year in range(2000, 2016):
            if year == 2006:
                continue  # Ignorer l'année 2006
            print(f"\nChargement des données pour l'année {year}...")
            year_data = load_data_for_year(year)
            if year_data is not None:
                # Vérifier que les communes correspondent
                communes_manquantes = [commune for commune in year_data['Commune'] 
                                     if commune not in commune_to_insee]
                if communes_manquantes:
                    print(f"Attention : {len(communes_manquantes)} communes non trouvées dans l'année {year}")
                    print("Exemples:", communes_manquantes[:3])
                
                data = pd.concat([data, year_data], ignore_index=True)
        
        if not data.empty:
            # Afficher un résumé des données
            print(f"\nDimensions totales des données : {data.shape}")
            print("\nRésumé statistique des colonnes numériques :")
            
            # Définir les colonnes pour le résumé statistique
            colonnes_stats = [
                'Moyenne annuelle de concentration de NO2 (ug/m3)',
                'Moyenne annuelle de concentration de PM10 (ug/m3)',
                'Moyenne annuelle de concentration de O3 (ug/m3)',
                'Moyenne annuelle de somo 35 (ug/m3.jour)',
                'Moyenne annuelle d\'AOT 40 (ug/m3.heure)',
                'Population'
            ]
            
            # Ajouter PM2.5 pour les années >= 2009
            données_récentes = data[data['Année'] >= 2009].copy()
            if 'Moyenne annuelle de concentration de PM25 (ug/m3)' in données_récentes.columns:
                print("\nRésumé statistique pour PM25 (2009-2015) :")
                print(données_récentes['Moyenne annuelle de concentration de PM25 (ug/m3)'].describe())
            
            # Résumé pour les autres polluants (toutes années)
            print("\nRésumé statistique pour les autres polluants (2000-2015) :")
            colonnes_disponibles = [col for col in colonnes_stats if col in data.columns]
            print(data[colonnes_disponibles].describe())
            
            # Créer le dossier de sortie s'il n'existe pas
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(script_dir, 'output')
            os.makedirs(output_dir, exist_ok=True)
            print(f"\nDossier de sortie créé : {output_dir}")
            
            # Définir les polluants et leurs périodes
            print("\nCréation des visualisations...")
            années = sorted(data['Année'].unique())
            polluants_tous = ['NO2', 'PM10', 'O3', 'Somo 35', 'AOT 40']  # Polluants pour 2000-2015
            polluant_2009 = 'PM25'  # Polluant uniquement pour 2009-2015
            
            # Mapping des noms de polluants vers les noms de colonnes exacts du CSV
            noms_colonnes = {
                'NO2': 'Moyenne annuelle de concentration de NO2 (ug/m3)',
                'PM10': 'Moyenne annuelle de concentration de PM10 (ug/m3)',
                'O3': 'Moyenne annuelle de concentration de O3 (ug/m3)',
                'Somo 35': 'Moyenne annuelle de somo 35 (ug/m3.jour)',
                'AOT 40': "Moyenne annuelle d'AOT 40 (ug/m3.heure)",
                'PM25': 'Moyenne annuelle de concentration de PM25 (ug/m3)'
            }
            
            for année in années:
                print(f"\nTraitement de l'année {année}...")
                # Filtrer les données pour l'année en cours
                données_année = data[data['Année'] == année]
                
                # Déterminer les polluants à traiter pour cette année
                polluants_à_traiter = polluants_tous.copy()  # NO2, PM10, O3, Somo35, AOT40 pour toutes les années
                if année >= 2009:
                    polluants_à_traiter.append(polluant_2009)  # Ajouter PM25 uniquement à partir de 2009
                
                for polluant in polluants_à_traiter:
                    # Obtenir le nom exact de la colonne depuis le mapping
                    colonne = noms_colonnes[polluant]
                    
                    # Vérifier si les données sont disponibles pour ce polluant
                    if colonne not in données_année.columns:
                        print(f"  Données non disponibles pour {polluant} en {année}")
                        continue
                        
                    print(f"  Génération des graphiques pour {polluant}...")
                    
                    try:
                        # Créer et sauvegarder le graphique de dispersion
                        fig_scatter = create_pollution_scatter(données_année, insee_to_commune, polluant)
                        scatter_file = os.path.join(output_dir, f'{polluant}_moyenne_annuelle_{année}.html')
                        write_html(fig_scatter, scatter_file, auto_open=False, include_plotlyjs='cdn')
                        
                        # Créer et sauvegarder l'histogramme
                        fig_hist = create_pollution_histogram(données_année, polluant)
                        hist_file = os.path.join(output_dir, f'{polluant}_histogram_{année}.html')
                        write_html(fig_hist, hist_file, auto_open=False, include_plotlyjs='cdn')
                        
                        print(f"  ✓ Graphiques générés avec succès pour {polluant}")
                    except Exception as e:
                        print(f"  ✗ Erreur lors de la génération des graphiques pour {polluant} : {str(e)}")
            
            # Générer les visualisations animées pour chaque polluant
            print("\nCréation des visualisations animées...")
            for polluant in polluants_tous:
                try:
                    print(f"  Génération des graphiques animés pour {polluant}...")
                    
                    # Créer et sauvegarder le graphique de dispersion animé
                    fig_scatter_anim = create_pollution_scatter_animation(data, insee_to_commune, polluant)
                    scatter_anim_file = os.path.join(output_dir, f'{polluant}_evolution_annuelle_scatter.html')
                    write_html(fig_scatter_anim, scatter_anim_file, auto_open=False, include_plotlyjs='cdn')
                    
                    # Créer et sauvegarder l'histogramme animé
                    fig_hist_anim = create_pollution_histogram_animation(data, polluant)
                    hist_anim_file = os.path.join(output_dir, f'{polluant}_evolution_annuelle_histogram.html')
                    write_html(fig_hist_anim, hist_anim_file, auto_open=False, include_plotlyjs='cdn')
                    
                    print(f"  ✓ Graphiques animés générés avec succès pour {polluant}")
                except Exception as e:
                    print(f"  ✗ Erreur lors de la génération des graphiques animés pour {polluant} : {str(e)}")
            
            # Générer les visualisations animées pour PM2.5 (2009-2015)
            if 'Moyenne annuelle de concentration de PM25 (ug/m3)' in données_récentes.columns:
                try:
                    print(f"  Génération des graphiques animés pour PM2.5 (2009-2015)...")
                    
                    # Créer et sauvegarder le graphique de dispersion animé
                    fig_scatter_anim = create_pollution_scatter_animation(données_récentes, insee_to_commune, 'PM25')
                    scatter_anim_file = os.path.join(output_dir, 'PM25_evolution_annuelle_scatter.html')
                    write_html(fig_scatter_anim, scatter_anim_file, auto_open=False, include_plotlyjs='cdn')
                    
                    # Créer et sauvegarder l'histogramme animé
                    fig_hist_anim = create_pollution_histogram_animation(données_récentes, 'PM25')
                    hist_anim_file = os.path.join(output_dir, 'PM25_evolution_annuelle_histogram.html')
                    write_html(fig_hist_anim, hist_anim_file, auto_open=False, include_plotlyjs='cdn')
                    
                    print(f"  ✓ Graphiques animés générés avec succès pour PM2.5")
                except Exception as e:
                    print(f"  ✗ Erreur lors de la génération des graphiques animés pour PM2.5 : {str(e)}")
            
            print("\nToutes les visualisations ont été générées avec succès !")
            print("Les fichiers HTML ont été créés dans le dossier 'output'.")
        else:
            print("Erreur : impossible de charger les données ou les correspondances de communes.")
            
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")


if __name__ == "__main__":
    main()