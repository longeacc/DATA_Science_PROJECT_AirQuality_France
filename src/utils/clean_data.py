import pandas as pd
import os
import glob
import warnings
import re

# Ignorer le warning FutureWarning sur concat
warnings.simplefilter(action='ignore', category=FutureWarning)

# Dossier contenant tes fichiers CSV
data_folder = r"C:\Users\willi\Downloads\Indicateurs_QualiteAir_France_Commune_2000-2015_Ineris_v.Sep2020"

# Lister tous les fichiers CSV
all_files = glob.glob(os.path.join(data_folder, "*.csv"))

list_of_dfs = []

# Lecture et ajout de l'année
for filepath in all_files:
    match = re.search(r'(\d{4})', os.path.basename(filepath))
    year = int(match.group(1)) if match else None

    df = pd.read_csv(filepath, encoding="latin1", skiprows=1)
    df['Année'] = year
    list_of_dfs.append(df)

# Harmonisation des colonnes
all_columns = set()
for df in list_of_dfs:
    all_columns.update(df.columns)
all_columns = list(all_columns)

for i, df in enumerate(list_of_dfs):
    for col in all_columns:
        if col not in df.columns:
            df[col] = pd.NA
    list_of_dfs[i] = df[all_columns]

# Fusionner tous les fichiers
final_df = pd.concat(list_of_dfs, ignore_index=True)

# Colonnes pour lesquelles on remplace les NA par la médiane
pollutants_cols = [
    'Moyenne annuelle de concentration de PM25 (ug/m3)',
    'Moyenne annuelle de concentration de PM25 ponderee par la population (ug/m3)',
    'Moyenne annuelle de concentration de PM10 (ug/m3)',
    'Moyenne annuelle de concentration de PM10 ponderee par la population (ug/m3)',
    'Moyenne annuelle de concentration de NO2 (ug/m3)',
    'Moyenne annuelle de concentration de NO2 ponderee par la population (ug/m3)',
    'Moyenne annuelle de concentration de O3 (ug/m3)',
    'Moyenne annuelle de concentration de O3 ponderee par la population (ug/m3)',
    "Moyenne annuelle d'AOT 40 (ug/m3.heure)",
    'Moyenne annuelle de somo 35 (ug/m3.jour)',
    'Moyenne annuelle de somo 35 pondere par la population (ug/m3.jour)'
]

# Remplir les NA par la médiane si la colonne existe
for col in pollutants_cols:
    if col in final_df.columns:
        final_df[col].fillna(final_df[col].median(skipna=True), inplace=True)

# COM Insee : remplacer NA par "Unknown"
if 'COM Insee' in final_df.columns:
    final_df['COM Insee'].fillna('Unknown', inplace=True)

# Population : remplacer NA par 0
if 'Population' in final_df.columns:
    final_df['Population'].fillna(0, inplace=True)

# Créer le dossier de sortie si nécessaire
output_folder = r"C:\Users\willi\Downloads\projetdata\DATA_Science_PROJECT_AirQuality_France\data\cleaned"
os.makedirs(output_folder, exist_ok=True)

# Sauvegarder uniquement le fichier 
output_path = os.path.join(output_folder, "cleaned_air_quality_with_year.csv")
final_df.to_csv(output_path, index=False)


print(" Fusion terminée avec l'année ! Dimension :", final_df.shape)
print(" Fichier  sauvegardé dans :", output_path) 

import pandas as pd

# Lire ton dataset (ici, on suppose qu'il s'appelle cleaned_air_quality_with_year.csv)
df = pd.read_csv(r"C:\Users\willi\Downloads\projetdata\DATA_Science_PROJECT_AirQuality_France\data\cleaned\cleaned_air_quality_with_year.csv")

# Afficher les 5 premières lignes
print(df.head())

# 1️⃣ Vérifier les valeurs manquantes
print(" Valeurs manquantes par colonne :")
print(final_df.isna().sum())

# Optionnel : supprimer les lignes avec NA encore présentes (à utiliser seulement si nécessaire)
# final_df.dropna(inplace=True)

# 2️⃣ Vérifier les doublons par commune et année
duplicated_count = final_df.duplicated(subset=['COM Insee', 'Année']).sum()
print(f"\n Nombre de doublons par 'COM Insee' et 'Année' : {duplicated_count}")

# Optionnel : supprimer les doublons exacts
# final_df = final_df.drop_duplicates(subset=['COM Insee', 'Année'])

# 3️⃣ Aperçu des statistiques pour les colonnes numériques
print("\n Statistiques descriptives des colonnes numériques :")
print(final_df.describe())
