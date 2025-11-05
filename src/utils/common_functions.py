import pandas as pd 
import numpy as np
import os 
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from plotly.offline import plot as write_html
import sys

# Ajouter le chemin du répertoire parent pour pouvoir importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from visualizations.scatter_plots import create_pollution_scatter
from visualizations.histograms import create_pollution_histogram

# Functions to charge and load graph abou data

class read_data:
    def __init__(self):
        pass

    @staticmethod
    def load_data(file_path):
        """
        Charge les données depuis un fichier CSV avec gestion des erreurs et du formatage.
        
        Args:
            file_path (str): Chemin vers le fichier CSV à charger
            
        Returns:
            pandas.DataFrame: DataFrame contenant les données chargées, ou None en cas d'erreur
        """
        try:
            if file_path is None:
                raise ValueError("Le chemin du fichier ne peut pas être None")
            
            # Vérifier si le fichier existe
            if not os.path.exists(file_path):
                print(f"ERREUR : Le fichier '{file_path}' n'existe pas.")
                return None
                
            # Lire le fichier en ignorant la première ligne (description)
            data = pd.read_csv(
                file_path,
                encoding='cp1252',    # Encodage Windows par défaut
                skiprows=1,           # Ignorer la première ligne de description
                sep=',',              # Utiliser la virgule comme séparateur
                decimal='.',          # Le point comme séparateur décimal
                thousands=None,       # Pas de séparateur de milliers
                low_memory=False
            )
            
            # Vérifier si nous avons le bon nombre de colonnes
            if len(data.columns) not in [12, 14]:
                print(f"ATTENTION : Nombre incorrect de colonnes ({len(data.columns)}). Attendu : 12 ou 14")
                print("Colonnes trouvées :")
                print(data.columns.tolist())
                return None
                
            # Vérifier les colonnes requises
            required_columns = [
                'COM Insee',
                'Commune',
                'Population',
                'Moyenne annuelle de concentration de NO2 (ug/m3)',
                'Moyenne annuelle de concentration de PM10 (ug/m3)',
                'Moyenne annuelle de concentration de O3 (ug/m3)'
            ]
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                print("ERREUR : Colonnes manquantes :")
                print(missing_columns)
                return None
                
            print("Fichier chargé avec succès!")
            return data
            
        except pd.errors.EmptyDataError:
            print(f"ERREUR : Le fichier '{file_path}' est vide.")
            return None
        except pd.errors.ParserError as e:
            print(f"ERREUR : Problème de format dans le fichier '{file_path}' : {e}")
            return None
        except Exception as e:
            print(f"ERREUR : Problème lors du chargement du fichier '{file_path}' : {e}")
            return None
    
    # Fonction pour traiter les données après le chargement
    @staticmethod
    def process_data(df):
        """
        Traite les données pour s'assurer que les colonnes sont correctement séparées et typées.
        """
        if df is None:
            return None
        
        try:
            # Convertir les colonnes numériques
            numeric_columns = df.columns[2:]  # Toutes les colonnes après 'Commune' sont numériques
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Vérifier la cohérence des données
            print("\nVérification de la cohérence des données :")
            print(f"Nombre total de lignes : {len(df)}")
            print(f"Nombre de colonnes : {len(df.columns)}")
            
            return df
            
        except Exception as e:
            print(f"Erreur lors du traitement des données : {str(e)}")
            return None

    @staticmethod
    def create_commune_insee_dict(df):
        """
        Crée un dictionnaire complet des correspondances entre codes INSEE et noms des communes.
        
        Args:
            df (pandas.DataFrame): DataFrame contenant obligatoirement :
                - 'COM Insee' : colonne avec les codes INSEE (type: str ou int)
                - 'Commune' : colonne avec les noms des communes (type: str)
        
        Returns:
            tuple: (commune_to_insee, insee_to_commune)
                - commune_to_insee (dict): {nom_commune (str): code_insee (str)}
                - insee_to_commune (dict): {code_insee (str): nom_commune (str)}
        
        Exemple d'utilisation:
            >>> commune_to_insee, insee_to_commune = read_data.create_commune_insee_dict(data)
            >>> code_insee = commune_to_insee["Paris"]
            >>> nom_commune = insee_to_commune["75056"]
        """
        if df is None:
            print("Erreur : DataFrame non fourni")
            return None, None
            
        if 'COM Insee' not in df.columns or 'Commune' not in df.columns:
            print("Erreur : Les colonnes 'COM Insee' et 'Commune' sont requises")
            print(f"Colonnes disponibles : {df.columns.tolist()}")
            return None, None
            
        try:
            # Convertir les codes INSEE en string pour assurer la cohérence
            df['COM Insee'] = df['COM Insee'].astype(str)
            
            # Supprimer les doublons éventuels
            df_unique = df[['Commune', 'COM Insee']].drop_duplicates()
            
            # Créer les dictionnaires
            commune_to_insee = dict(zip(df_unique['Commune'], df_unique['COM Insee']))
            insee_to_commune = dict(zip(df_unique['COM Insee'], df_unique['Commune']))
            
            # Vérification et rapport
            print(f"\nDictionnaires créés avec succès:")
            print(f"- Nombre total de communes : {len(commune_to_insee)}")
            print(f"- Nombre de codes INSEE uniques : {len(insee_to_commune)}")
            
            if len(commune_to_insee) != len(insee_to_commune):
                print("\nATTENTION : Certaines communes ont le même code INSEE ou vice-versa")
            
            # Afficher quelques exemples
            print("\nExemples de correspondances :")
            for commune, insee in list(commune_to_insee.items())[:5]:
                print(f"Commune: {commune:30} -> Code INSEE: {insee}")
                
            print("\nUtilisation des dictionnaires:")
            print("commune_to_insee['nom_commune'] -> renvoie le code INSEE")
            print("insee_to_commune['code_insee'] -> renvoie le nom de la commune")
            
            return commune_to_insee, insee_to_commune
            
        except Exception as e:
            print(f"Erreur lors de la création des dictionnaires : {str(e)}")
            print("Détails des colonnes du DataFrame :")
            print(df.info())
            return None, None


def load_commune_mappings():
    """
    Charge les correspondances entre codes INSEE et noms de communes.
    
    Args:
        year (int): L'année pour laquelle charger les données (par défaut: 2000)
        
    Returns:
        tuple: (commune_to_insee, insee_to_commune) dictionnaires de correspondance
    """
    try:
        # Charger le fichier CSV
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_path = os.path.join(script_dir, "data", "raw", "Indicateurs_QualiteAir_France_Commune_2000_Ineris_v.Sep2020.csv")
        
        # Utiliser la méthode load_data de la classe read_data
        data = read_data.load_data(data_path)
        if data is None:
            raise ValueError("Impossible de charger les données pour les correspondances communes")
        
        # Créer les dictionnaires de correspondance
        commune_to_insee = dict(zip(data['Commune'], data['COM Insee']))
        insee_to_commune = dict(zip(data['COM Insee'], data['Commune']))
        
        return commune_to_insee, insee_to_commune
        
    except Exception as e:
        print(f"Erreur lors du chargement des correspondances communes")
        return None, None


def load_data_for_year(year):
    """
    Charge les données pour une année spécifique.
    
    Args:
        year (int): L'année pour laquelle charger les données
        
    Returns:
        pd.DataFrame: Les données pour l'année spécifiée, ou None en cas d'erreur
    """
    try:
        if year == 2006:
            return None
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_path = os.path.join(script_dir, "data", "raw", f"Indicateurs_QualiteAir_France_Commune_{year}_Ineris_v.Sep2020.csv")
        
        data = read_data.load_data(data_path)
        if data is not None:
            data['Année'] = year
            data = read_data.process_data(data)
            print(f"Données pour {year} chargées avec succès.")
            return data
        return None
        
    except Exception as e:
        print(f"Erreur lors du chargement des données pour {year}: {str(e)}")
        return None


def process_and_visualize_data(data, insee_to_commune):
    """
    Traite et visualise les données de pollution de l'air sur plusieurs années.
    
    Args:
        data (pd.DataFrame): Le DataFrame contenant les données
        insee_to_commune (dict): Dictionnaire de correspondance codes INSEE vers noms de communes
        
    Returns:
        dict: Dictionnaire contenant les figures générées
    """
    # Créer le dossier de sortie s'il n'existe pas
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nDossier de sortie créé : {output_dir}")
    
    # Dictionnaire pour stocker toutes les figures
    all_figures = {}
    
    # Traiter chaque année
    for year in sorted(data['Année'].unique()):
        print(f"\nCréation des visualisations pour l'année {year}...")
        year_data = data[data['Année'] == year]
        
        # Créer les visualisations pour chaque polluant
        for pollutant in ['NO2', 'PM10', 'O3']:
            # Graphique de dispersion
            fig_scatter = create_pollution_scatter(year_data, insee_to_commune, pollutant)
            
            # Histogramme
            fig_hist = create_pollution_histogram(year_data, pollutant)
            
            # Sauvegarder les visualisations
            scatter_file = os.path.join(output_dir, f'{pollutant}_moyenne_annuelle_{year}.html')
            hist_file = os.path.join(output_dir, f'{pollutant}_histogram_{year}.html')
            
            write_html(fig_scatter, scatter_file, auto_open=False, include_plotlyjs='cdn')
            write_html(fig_hist, hist_file, auto_open=False, include_plotlyjs='cdn')
            
            # Stocker les figures
            all_figures[f'{pollutant}_scatter_{year}'] = fig_scatter
            all_figures[f'{pollutant}_histogram_{year}'] = fig_hist
    
    print("\nToutes les visualisations ont été générées avec succès !")
    return all_figures