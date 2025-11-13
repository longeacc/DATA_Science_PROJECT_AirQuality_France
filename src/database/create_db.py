# create_database.py
import sqlite3
import pandas as pd
import os

def create_database():
    """
    Script de création et peuplement de la base de données SQLite
    """
    print("\n=== CRÉATION DE LA BASE DE DONNÉES ===")
    
    # Définir les chemins
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    data_path = os.path.join(base_dir, "data", "cleaned", "cleaned_air_quality_with_year.csv")
    db_path = os.path.join(base_dir, "data", "air_quality.db")

    # Charger le CSV nettoyé
    print(f"Chargement du fichier nettoyé : {data_path}")
    
    if not os.path.exists(data_path):
        print(f"❌ Fichier CSV introuvable : {data_path}")
        return False
        
    df = pd.read_csv(data_path)

    # Connexion à la base (elle est créée si elle n'existe pas)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Création de la table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS air_quality (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        com_insee TEXT,
        commune TEXT,
        population REAL,
        annee INTEGER,
        pm25 REAL,
        pm25_pop REAL,
        pm10 REAL,
        pm10_pop REAL,
        no2 REAL,
        no2_pop REAL,
        o3 REAL,
        o3_pop REAL,
        aot40 REAL,
        somo35 REAL,
        somo35_pop REAL
    )
    """)

    conn.commit()

    # Harmonisation des noms de colonnes avant insertion
    mapping = {
        'COM Insee': 'com_insee',
        'Commune': 'commune',
        'Population': 'population',
        'Année': 'annee',
        'Moyenne annuelle de concentration de PM25 (ug/m3)': 'pm25',
        'Moyenne annuelle de concentration de PM25 ponderee par la population (ug/m3)': 'pm25_pop',
        'Moyenne annuelle de concentration de PM10 (ug/m3)': 'pm10',
        'Moyenne annuelle de concentration de PM10 ponderee par la population (ug/m3)': 'pm10_pop',
        'Moyenne annuelle de concentration de NO2 (ug/m3)': 'no2',
        'Moyenne annuelle de concentration de NO2 ponderee par la population (ug/m3)': 'no2_pop',
        'Moyenne annuelle de concentration de O3 (ug/m3)': 'o3',
        'Moyenne annuelle de concentration de O3 ponderee par la population (ug/m3)': 'o3_pop',
        "Moyenne annuelle d'AOT 40 (ug/m3.heure)": 'aot40',
        'Moyenne annuelle de somo 35 (ug/m3.jour)': 'somo35',
        'Moyenne annuelle de somo 35 pondere par la population (ug/m3.jour)': 'somo35_pop',
    }

    df = df.rename(columns=mapping)

    # Garder uniquement les colonnes utiles
    cols = list(mapping.values())
    df = df[cols]

    # Vider la table avant insertion (optionnel)
    cursor.execute("DELETE FROM air_quality")
    conn.commit()

    # Insérer les données dans SQLite
    df.to_sql("air_quality", conn, if_exists="append", index=False)
    conn.commit()

    # Vérification
    count = cursor.execute("SELECT COUNT(*) FROM air_quality").fetchone()[0]
    
    print(f"✅ Base de données créée avec succès : {db_path}")
    print(f"Nombre de lignes insérées : {count}")

    # Test query
    query = "SELECT annee, COUNT(*) as nb_communes, AVG(no2) as moyenne_no2 FROM air_quality GROUP BY annee;"
    df_test = pd.read_sql_query(query, conn)
    print("\📊 Données par année :")
    print(df_test)

    conn.close()
    return True

if __name__ == "__main__":
    create_database()
