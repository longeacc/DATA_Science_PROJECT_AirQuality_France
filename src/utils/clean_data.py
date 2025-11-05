# src/utils/clean_data.py

import pandas as pd
import os
import glob
import warnings
import re

# Ignorer le warning FutureWarning sur concat
warnings.simplefilter(action='ignore', category=FutureWarning)

# 🔹 Chemins relatifs depuis src/utils/ jusqu'à la racine du projet
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Dossier contenant les CSV bruts (data/raw/)
data_folder = os.path.join(base_dir, "data", "raw")

# Dossier pour sauvegarder le CSV nettoyé (data/cleaned/)
output_folder = os.path.join(base_dir, "data", "cleaned")
os.makedirs(output_folder, exist_ok=True)

print("📁 Dossier source :", data_folder)
print("💾 Dossier de sortie :", output_folder)

# 🔹 Lister tous les fichiers CSV
all_files = glob.glob(os.path.join(data_folder, "*.csv"))

if not all_files:
    print("⚠️ Aucun fichier CSV trouvé dans le dossier raw !")
    exit()

list_of_dfs = []

# 🔹 Lecture des fichiers et ajout de l'année
for filepath in all_files:
    match = re.search(r'(\d{4})', os.path.basename(filepath))
    year = int(match.group(1)) if match else None

    df = pd.read_csv(filepath, encoding="latin1", skiprows=1)
    df['Année'] = year
    list_of_dfs.append(df)

# 🔹 Harmonisation des colonnes
all_columns = set()
for df in list_of_dfs:
    all_columns.update(df.columns)
all_columns = list(all_columns)

for i, df in enumerate(list_of_dfs):
    for col in all_columns:
        if col not in df.columns:
            df[col] = pd.NA
    list_of_dfs[i] = df[all_columns]

# 🔹 Fusionner tous les fichiers
final_df = pd.concat(list_of_dfs, ignore_index=True)

# 🔹 Colonnes polluants pour lesquelles on remplace les NA par la médiane
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

# 🔹 Vérifier les doublons par commune et année
duplicated_count = final_df.duplicated(subset=['COM Insee', 'Année']).sum()
print(f"🔹 Nombre de doublons par 'COM Insee' et 'Année' : {duplicated_count}")

# 🔹 Sauvegarder le fichier nettoyé
output_path = os.path.join(output_folder, "cleaned_air_quality_with_year.csv")
final_df.to_csv(output_path, index=False)

print("✅ Fusion et nettoyage terminés ! Dimension du DataFrame :", final_df.shape)
print("💾 Fichier sauvegardé dans :", output_path)
