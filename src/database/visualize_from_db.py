import os
import sqlite3
import pandas as pd
from plotly.io import write_html
from src.utils.common_functions import load_commune_mappings
from src.visualizations.scatter_plots import create_pollution_scatter
from src.visualizations.histograms import create_pollution_histogram


def main():
    """
    Script de visualisation des données de pollution à partir de la base SQLite.
    Génère des graphiques (scatter + histogrammes) pour chaque polluant et chaque année.
    """

    print("\n=== VISUALISATION À PARTIR DE LA BASE DE DONNÉES ===")

    try:
        # --- Définir le chemin vers la base de données ---
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        db_path = os.path.join(base_dir, "data", "air_quality.db")

        if not os.path.exists(db_path):
            print(f"❌ Base de données introuvable : {db_path}")
            return

        # --- Connexion à la base ---
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM air_quality"
        df = pd.read_sql_query(query, conn)
        conn.close()

        print(f"✅ {len(df)} lignes chargées depuis la base de données\n")

        # --- Harmonisation des noms pour compatibilité avec le code existant ---
        rename_mapping = {
            "com_insee": "COM Insee",
            "commune": "Commune",
            "population": "Population",
            "annee": "Année",
            "no2": "Moyenne annuelle de concentration de NO2 (ug/m3)",
            "pm10": "Moyenne annuelle de concentration de PM10 (ug/m3)",
            "pm25": "Moyenne annuelle de concentration de PM25 (ug/m3)",
            "o3": "Moyenne annuelle de concentration de O3 (ug/m3)",
            "aot40": "Moyenne annuelle de concentration de AOT40 (ug/m3)",
            "somo35": "Moyenne annuelle de concentration de SOMO35 (ug/m3)"
        }

        df.rename(columns=rename_mapping, inplace=True)

        # Charger les correspondances des communes
        commune_to_insee, insee_to_commune = load_commune_mappings()
        if commune_to_insee is None or insee_to_commune is None:
            print("❌ Impossible de charger les correspondances des communes.")
            return

        # Vérification des années disponibles
        années = sorted(df["Année"].unique())
        print(f"Années trouvées dans la base : {années}\n")

        # --- Créer le dossier de sortie ---
        output_dir = os.path.join(base_dir, "src", "database", "output")
        os.makedirs(output_dir, exist_ok=True)

        # --- Définir les polluants et leurs colonnes ---
        noms_colonnes = {
            'NO2': "Moyenne annuelle de concentration de NO2 (ug/m3)",
            'PM10': "Moyenne annuelle de concentration de PM10 (ug/m3)",
            'O3': "Moyenne annuelle de concentration de O3 (ug/m3)",
            'SOMO35': "Moyenne annuelle de concentration de SOMO35 (ug/m3)",
            'AOT40': "Moyenne annuelle de concentration de AOT40 (ug/m3)",
            'PM25': "Moyenne annuelle de concentration de PM25 (ug/m3)"
        }

        polluants_tous = ['NO2', 'PM10', 'O3', 'SOMO35', 'AOT40']
        polluant_2009 = 'PM25'  # ajouté à partir de 2009

        # --- Génération des graphiques ---
        for année in années:
            print(f"📅 Traitement de l'année {année}...")
            data_année = df[df["Année"] == année]

            polluants_à_traiter = polluants_tous.copy()
            if année >= 2009:
                polluants_à_traiter.append(polluant_2009)

            for polluant in polluants_à_traiter:
                colonne = noms_colonnes[polluant]

                if colonne not in data_année.columns:
                    print(f"  ⚠️ Données non disponibles pour {polluant} en {année}")
                    continue

                print(f"  → Génération des graphiques pour {polluant}...")

                try:
                    # Créer et sauvegarder le graphique de dispersion
                    fig_scatter = create_pollution_scatter(data_année, insee_to_commune, polluant)
                    scatter_file = os.path.join(output_dir, f"{polluant}_moyenne_annuelle_{année}.html")
                    write_html(fig_scatter, scatter_file, auto_open=False, include_plotlyjs='cdn')

                    # Créer et sauvegarder l'histogramme
                    fig_hist = create_pollution_histogram(data_année, polluant)
                    hist_file = os.path.join(output_dir, f"{polluant}_histogram_{année}.html")
                    write_html(fig_hist, hist_file, auto_open=False, include_plotlyjs='cdn')

                    print(f"    ✓ Graphiques générés avec succès pour {polluant}")
                except Exception as e:
                    print(f"    ✗ Erreur sur {polluant} ({année}) : {str(e)}")

        print("\n✅ Toutes les visualisations ont été générées dans le dossier 'output'.")

    except Exception as e:
        print(f"\n❌ Une erreur s'est produite : {str(e)}")


if __name__ == "__main__":
    main()

