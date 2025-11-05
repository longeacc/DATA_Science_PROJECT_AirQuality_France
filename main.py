"""
Script principal pour l'analyse des données de qualité de l'air en France.
"""

import pandas as pd
import os
from plotly.io import write_html
from src.utils.common_functions import load_commune_mappings, load_data_for_year
from src.visualizations.scatter_plots import create_pollution_scatter
from src.visualizations.histograms import create_pollution_histogram


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
            columns_to_describe = [
                'Moyenne annuelle de concentration de NO2 (ug/m3)',
                'Moyenne annuelle de concentration de PM10 (ug/m3)',
                'Moyenne annuelle de concentration de O3 (ug/m3)',
                'Population'
            ]
            print(data[columns_to_describe].describe())
            
            # Créer le dossier de sortie s'il n'existe pas
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(script_dir, 'output')
            os.makedirs(output_dir, exist_ok=True)
            print(f"\nDossier de sortie créé : {output_dir}")
            
            # Créer les visualisations pour chaque année
            print("\nCréation des visualisations...")
            années = sorted(data['Année'].unique())
            polluants = ['NO2', 'PM10', 'O3']
            
            for année in années:
                print(f"\nTraitement de l'année {année}...")
                # Filtrer les données pour l'année en cours
                données_année = data[data['Année'] == année]
                
                for polluant in polluants:
                    print(f"  Génération des graphiques pour {polluant}...")
                    
                    # Créer et sauvegarder le graphique de dispersion
                    fig_scatter = create_pollution_scatter(données_année, insee_to_commune, polluant)
                    scatter_file = os.path.join(output_dir, f'{polluant}_moyenne_annuelle_{année}.html')
                    write_html(fig_scatter, scatter_file, auto_open=False, include_plotlyjs='cdn')
                    
                    # Créer et sauvegarder l'histogramme
                    fig_hist = create_pollution_histogram(données_année, polluant)
                    hist_file = os.path.join(output_dir, f'{polluant}_histogram_{année}.html')
                    write_html(fig_hist, hist_file, auto_open=False, include_plotlyjs='cdn')
            
            print("\nToutes les visualisations ont été générées avec succès !")
            print("Les fichiers HTML ont été créés dans le dossier 'output'.")
        else:
            print("Erreur : impossible de charger les données ou les correspondances de communes.")
            
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")


if __name__ == "__main__":
    main()