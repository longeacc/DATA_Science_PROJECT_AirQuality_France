# visualize_from_database.py
import os
import sqlite3
import pandas as pd
from plotly.io import write_html
from src.utils.common_functions import load_commune_mappings
from src.visualizations.scatter_plots import create_pollution_scatter
from src.visualizations.histograms import create_pollution_histogram


def load_data_from_database():
    """
    Charge les données depuis la base SQLite
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    db_path = os.path.join(base_dir, "data", "air_quality.db")

    if not os.path.exists(db_path):
        print(f"❌ Base de données introuvable : {db_path}")
        return None

    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM air_quality"
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df, base_dir


def prepare_data(df):
    """
    Prépare les données en harmonisant les noms de colonnes
    pour la compatibilité avec les fonctions de visualisation
    """
    # CORRECTION : Mapping vers les noms attendus par les fonctions de visualisation
    rename_mapping = {
        "com_insee": "COM Insee",
        "commune": "Commune", 
        "population": "Population",
        "annee": "Année",
        "pm25": "Moyenne annuelle de concentration de PM25 (ug/m3)",
        "pm25_pop": "Moyenne annuelle de concentration de PM25 ponderee (ug/m3)",  # SUPPRIMÉ "par la population"
        "pm10": "Moyenne annuelle de concentration de PM10 (ug/m3)", 
        "pm10_pop": "Moyenne annuelle de concentration de PM10 ponderee (ug/m3)",  # SUPPRIMÉ "par la population"
        "no2": "Moyenne annuelle de concentration de NO2 (ug/m3)",
        "no2_pop": "Moyenne annuelle de concentration de NO2 ponderee (ug/m3)",    # SUPPRIMÉ "par la population"
        "o3": "Moyenne annuelle de concentration de O3 (ug/m3)",
        "o3_pop": "Moyenne annuelle de concentration de O3 ponderee (ug/m3)",      # SUPPRIMÉ "par la population"
        "aot40": "Moyenne annuelle de concentration de AOT40 (ug/m3)",             # CORRIGÉ
        "somo35": "Moyenne annuelle de concentration de SOMO35 (ug/m3)",           # CORRIGÉ
        "somo35_pop": "Moyenne annuelle de concentration de SOMO35 ponderee (ug/m3)" # SUPPRIMÉ "par la population"
    }

    df.rename(columns=rename_mapping, inplace=True)
    return df


def generate_visualizations():
    """
    Script de visualisation des données de pollution à partir de la base SQLite.
    Génère des graphiques (scatter + histogrammes) pour chaque polluant et chaque année.
    """
    print("\n=== VISUALISATION À PARTIR DE LA BASE DE DONNÉES ===")

    try:
        # Charger les données
        result = load_data_from_database()
        if result is None:
            return
        df, base_dir = result

        print(f"✅ {len(df)} lignes chargées depuis la base de données\n")

        # Préparer les données
        df = prepare_data(df)

        # Debug : afficher les colonnes disponibles
        print("Colonnes disponibles après renommage :")
        for col in df.columns:
            print(f"  - {col}")
        print()

        # Charger les correspondances des communes
        commune_to_insee, insee_to_commune = load_commune_mappings()
        if commune_to_insee is None or insee_to_commune is None:
            print("❌ Impossible de charger les correspondances des communes.")
            return

        # Vérification des années disponibles
        années = sorted(df["Année"].unique())
        print(f"Années trouvées dans la base : {années}\n")

        # Créer le dossier de sortie
        output_dir = os.path.join(base_dir, "src", "database", "output")
        os.makedirs(output_dir, exist_ok=True)

        # CORRECTION : Définir les polluants avec les noms exacts attendus par les fonctions
        noms_colonnes = {
            'NO2': "Moyenne annuelle de concentration de NO2 (ug/m3)",
            'NO2 ponderee': "Moyenne annuelle de concentration de NO2 ponderee (ug/m3)",
            'PM10': "Moyenne annuelle de concentration de PM10 (ug/m3)",
            'PM10 ponderee': "Moyenne annuelle de concentration de PM10 ponderee (ug/m3)",
            'PM25': "Moyenne annuelle de concentration de PM25 (ug/m3)",
            'PM25 ponderee': "Moyenne annuelle de concentration de PM25 ponderee (ug/m3)",
            'O3': "Moyenne annuelle de concentration de O3 (ug/m3)",
            'O3 ponderee': "Moyenne annuelle de concentration de O3 ponderee (ug/m3)",
            'AOT40': "Moyenne annuelle de concentration de AOT40 (ug/m3)",
            'SOMO35': "Moyenne annuelle de concentration de SOMO35 (ug/m3)",
            'SOMO35 ponderee': "Moyenne annuelle de concentration de SOMO35 ponderee (ug/m3)"
        }

        # Génération des graphiques
        for année in années:
            print(f"📅 Traitement de l'année {année}...")
            data_année = df[df["Année"] == année]

            for polluant, colonne in noms_colonnes.items():
                # Vérification plus détaillée
                if colonne not in data_année.columns:
                    print(f"  ⚠️ Colonne '{colonne}' non trouvée pour {polluant} en {année}")
                    continue
                
                # Vérifier s'il y a des données non nulles
                if data_année[colonne].isna().all():
                    print(f"  ⚠️ Données manquantes pour {polluant} en {année}")
                    continue

                print(f"  → Génération des graphiques pour {polluant}...")

                try:
                    # Créer et sauvegarder le graphique de dispersion
                    fig_scatter = create_pollution_scatter(data_année, insee_to_commune, polluant)
                    scatter_file = os.path.join(output_dir, f"{polluant.replace(' ', '_')}_{année}_scatter.html")
                    write_html(fig_scatter, scatter_file, auto_open=False, include_plotlyjs='cdn')

                    # Créer et sauvegarder l'histogramme
                    fig_hist = create_pollution_histogram(data_année, polluant)
                    hist_file = os.path.join(output_dir, f"{polluant.replace(' ', '_')}_{année}_histogram.html")
                    write_html(fig_hist, hist_file, auto_open=False, include_plotlyjs='cdn')

                    print(f"    ✓ Graphiques générés avec succès pour {polluant}")
                except Exception as e:
                    print(f"    ✗ Erreur sur {polluant} ({année}) : {str(e)}")

        print("\n✅ Toutes les visualisations ont été générées dans le dossier 'output'.")

    except Exception as e:
        print(f"\n❌ Une erreur s'est produite : {str(e)}")


if __name__ == "__main__":
    generate_visualizations()