import pandas as pd 
import numpy as np
import os 
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

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
            if len(data.columns) != 12:
                print(f"ATTENTION : Nombre incorrect de colonnes ({len(data.columns)}). Attendu : 12")
                print("Colonnes trouvées :")
                print(data.columns.tolist())
                return KeyError
                
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