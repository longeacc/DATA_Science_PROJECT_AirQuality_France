import sqlite3
import pandas as pd

db_path = "data/air_quality.db"
conn = sqlite3.connect(db_path)

# Vérifier le nombre de lignes par commune et année
query = """
SELECT com_insee, annee, COUNT(*) as count
FROM air_quality
GROUP BY com_insee, annee
HAVING COUNT(*) > 1
LIMIT 10
"""
df_dup = pd.read_sql_query(query, conn)
print("Communes avec duplications:")
print(df_dup)

# Compter le total de lignes avec duplications
query2 = """
SELECT COUNT(*) as total_groups, SUM(count) as total_rows
FROM (
    SELECT com_insee, annee, COUNT(*) as count
    FROM air_quality
    GROUP BY com_insee, annee
    HAVING COUNT(*) > 1
)
"""
df_count = pd.read_sql_query(query2, conn)
print("\nStatistiques des duplications:")
print(df_count)

# Vérifier une commune spécifique
query3 = """
SELECT *
FROM air_quality
WHERE com_insee = (
    SELECT com_insee
    FROM air_quality
    GROUP BY com_insee, annee
    HAVING COUNT(*) > 1
    LIMIT 1
)
AND annee = 2000
LIMIT 5
"""
df_sample = pd.read_sql_query(query3, conn)
print("\nExemple de lignes dupliquées:")
print(df_sample)

conn.close()
