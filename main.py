import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.utils.common_functions import read_data
from src.visualization.scatter_plots import create_pollution_scatter
from src.visualization.histograms import create_pollution_histogram
from plotly.io import write_html

# Définir le chemin du fichier de 2000 - 2015
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path_2000 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2000_Ineris_v.Sep2020.csv')
file_path_2001 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2001_Ineris_v.Sep2020.csv')
file_path_2002 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2002_Ineris_v.Sep2020.csv')
file_path_2003 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2003_Ineris_v.Sep2020.csv')
file_path_2004 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2004_Ineris_v.Sep2020.csv')
file_path_2005 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2005_Ineris_v.Sep2020.csv')
file_path_2006 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2006_Ineris_v.Sep2020.csv')
file_path_2007 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2007_Ineris_v.Sep2020.csv')
file_path_2008 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2008_Ineris_v.Sep2020.csv')
file_path_2009 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2009_Ineris_v.Sep2020.csv')
file_path_2010 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2010_Ineris_v.Sep2020.csv')
file_path_2011 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2011_Ineris_v.Sep2020.csv')
file_path_2012 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2012_Ineris_v.Sep2020.csv')
file_path_2013 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2013_Ineris_v.Sep2020.csv')
file_path_2014 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2014_Ineris_v.Sep2020.csv')
file_path_2015 = os.path.join(script_dir, 'data', 'raw', 'Indicateurs_QualiteAir_France_Commune_2015_Ineris_v.Sep2020.csv')

# Charger les données
data = read_data.load_data(file_path_2000)
data = read_data.process_data(data)

data_2001 = read_data.load_data(file_path_2001)
data_2001 = read_data.process_data(data_2001)

data_2002 = read_data.load_data(file_path_2002)
data_2002 = read_data.process_data(data_2002)

data_2003 = read_data.load_data(file_path_2003)
data_2003 = read_data.process_data(data_2003)

data_2004 = read_data.load_data(file_path_2004)
data_2004 = read_data.process_data(data_2004)

data_2005 = read_data.load_data(file_path_2005)
data_2005 = read_data.process_data(data_2005)

data_2006 = read_data.load_data(file_path_2006)
data_2006 = read_data.process_data(data_2006)

data_2007 = read_data.load_data(file_path_2007)
data_2007 = read_data.process_data(data_2007)

data_2008 = read_data.load_data(file_path_2008)
data_2008 = read_data.process_data(data_2008)

data_2009 = read_data.load_data(file_path_2009)
data_2009 = read_data.process_data(data_2009)

data_2010 = read_data.load_data(file_path_2010)
data_2010 = read_data.process_data(data_2010)

data_2011 = read_data.load_data(file_path_2011)
data_2011 = read_data.process_data(data_2011)

data_2012 = read_data.load_data(file_path_2012)
data_2012 = read_data.process_data(data_2012)

data_2013 = read_data.load_data(file_path_2013)
data_2013 = read_data.process_data(data_2013)

data_2014 = read_data.load_data(file_path_2014)
data_2014 = read_data.process_data(data_2014)

data_2015 = read_data.load_data(file_path_2015)
data_2015 = read_data.process_data(data_2015)


# Créer les dictionnaires de correspondance commune-INSEE de 2000 à 2015
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2001)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2002)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2003)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2004)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2005)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2006)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2007)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2008)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2009)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2010)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2011)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2012)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2013)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2014)
commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data_2015)

def process_and_visualize_data(data, insee_to_commune):
    """
    Traite et visualise les données de pollution de l'air.
    
    Args:
        data (pd.DataFrame): Le DataFrame contenant les données
        insee_to_commune (dict): Dictionnaire de correspondance codes INSEE vers noms de communes
        
    Returns:
        dict: Dictionnaire contenant les figures générées
    """
    ###################################2000###############################
    # Créer les visualisations
    fig_no2 = create_pollution_scatter(data, insee_to_commune, "NO2")
    fig_pm10 = create_pollution_scatter(data, insee_to_commune, "PM10")
    fig_o3 = create_pollution_scatter(data, insee_to_commune, "O3")
    
    # Créer les histogrammes
    fig_hist_no2 = create_pollution_histogram(data, "NO2")
    fig_hist_pm10 = create_pollution_histogram(data, "PM10")
    fig_hist_o3 = create_pollution_histogram(data, "O3")

    # Créer le dossier de sortie s'il n'existe pas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nDossier de sortie créé : {output_dir}")
    
    # Sauvegarder les visualisations
    write_html(fig_no2, os.path.join(output_dir, 'NO2_moyenne_annuelle_2007_2020.html'), auto_open=True, include_plotlyjs='cdn')
    write_html(fig_pm10, os.path.join(output_dir, 'PM10_moyenne_annuelle_2007_2020.html'), auto_open=True, include_plotlyjs='cdn')
    write_html(fig_hist_no2, os.path.join(output_dir, 'NO2_histogram.html'), auto_open=True, include_plotlyjs='cdn')
    write_html(fig_hist_pm10, os.path.join(output_dir, 'PM10_histogram.html'), auto_open=True, include_plotlyjs='cdn')
    write_html(fig_hist_o3, os.path.join(output_dir, 'O3_histogram.html'), auto_open=True, include_plotlyjs='cdn')
    write_html(fig_o3, os.path.join(output_dir, 'O3_moyenne_annuelle_2007_2020.html'), auto_open=True, include_plotlyjs='cdn')
    return {
        'no2_scatter': fig_no2,
        'pm10_scatter': fig_pm10,
        'no2_histogram': fig_hist_no2,
        'pm10_histogram': fig_hist_pm10,
        'o3_scatter': fig_o3,
        'o3_histogram': fig_hist_o3
    }


####################################2001###################################


if __name__ == "__main__":
    if data is not None and commune_to_insee is not None:
        print("\nDonnées chargées avec succès dans le script principal.")
        
        # Afficher un résumé des données
        print(f"\nDimensions des données : {data.shape}")
        print("\nRésumé statistique des colonnes numériques :")
        print(data[['Moyenne annuelle de concentration de NO2 (ug/m3)', 
                   'Moyenne annuelle de concentration de PM10 (ug/m3)',
                   'Moyenne annuelle de concentration de O3 (ug/m3)',
                   'Population']].describe())
        
        # Créer les visualisations
        print("\nCréation des visualisations...")
        figures = process_and_visualize_data(data, insee_to_commune)
        
        print("\nVisualisations générées avec succès !")
        print("Les fichiers HTML ont été créés dans le dossier 'output'.")
        
        # Afficher les informations sur les données
        print(f"\nDimensions des données : {data.shape}")
        print("\nRésumé statistique des colonnes numériques :")
        print(data.describe())
        
        # Créer les visualisations
        figures = process_and_visualize_data(data, insee_to_commune)
        print("\nVisualisations générées avec succès !")
        print("Les fichiers HTML ont été créés dans le dossier 'output'.")
    else:
        print("Échec du chargement des données dans le script principal.")

