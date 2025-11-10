import plotly.graph_objects as go
import re
import json
import os

def get_data_from_html(file_path):
    """
    Extrait les données du fichier HTML.
    
    Args:
        file_path (str): Chemin vers le fichier HTML
        
    Returns:
        list: Liste des traces de données ou None en cas d'erreur
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Rechercher les données avec une expression régulière
            match = re.search(r'var data=(\[.*?\]);', content, re.DOTALL)
            if not match:
                match = re.search(r'data: (\[.*?\])};}', content, re.DOTALL)
            if match:
                data_str = match.group(1)
                try:
                    return json.loads(data_str)
                except json.JSONDecodeError as e:
                    print(f"  ! Impossible de décoder les données JSON de {file_path}: {str(e)}")
                    print(f"  Data string: {data_str[:100]}...")  # Afficher le début des données pour debug
                    return None
    except Exception as e:
        print(f"  ! Erreur lors de la lecture de {file_path}: {str(e)}")
        return None
    return None

def superpose_histograms_for_pollutant(output_dir, pollutant_type):
    """
    Crée un histogramme superposé pour un polluant donné.
    
    Args:
        output_dir (str): Le dossier contenant les fichiers HTML
        pollutant_type (str): Type de polluant
    """
    # Créer la figure
    fig = go.Figure()
    
    # Liste des années disponibles (en excluant 2006)
    years = list(range(2000, 2016))
    if 2006 in years:
        years.remove(2006)
    
    # Couleurs pour chaque année
    colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)',
             'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
             'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)',
             'rgb(23, 190, 207)', 'rgb(174, 199, 232)', 'rgb(255, 187, 120)',
             'rgb(152, 223, 138)', 'rgb(255, 152, 150)', 'rgb(197, 176, 213)']
    
    # Pour chaque année, récupérer et ajouter les données
    for i, year in enumerate(years):
        file_path = os.path.join(output_dir, f'{pollutant_type}_histogram_{year}.html')
        if os.path.exists(file_path):
            traces = get_data_from_html(file_path)
            if traces and len(traces) > 0:
                for trace in traces:
                    if isinstance(trace, dict) and 'x' in trace:
                        # Convertir les valeurs en nombres si ce ne sont pas déjà des nombres
                        x_values = []
                        for x in trace['x']:
                            try:
                                x_values.append(float(x) if isinstance(x, str) else x)
                            except (ValueError, TypeError):
                                continue
                        
                        if x_values:  # Ne créer la trace que si nous avons des données valides
                            new_trace = go.Histogram(
                                x=x_values,
                                nbinsx=30,
                                name=str(year),
                                marker_color=colors[i % len(colors)],
                                opacity=0.6,
                                hovertemplate="<b>Concentration</b>: %{x:.1f} µg/m³<br>" +
                                            "Nombre de communes: %{y}<br>" +
                                            f"Année: {year}<extra></extra>"
                            )
                            fig.add_trace(new_trace)
                            print(f"    → {len(x_values)} valeurs ajoutées pour {year}")
                        break  # Ne prendre que la première trace valide
    
    # Préparation du titre et des unités selon le type de polluant
    if pollutant_type == 'somo 35':
        titre_global = 'Superposition des distributions SOMO35 en France (2000-2015)'
        unite = 'µg/m³·jour'
    elif pollutant_type == 'AOT 40':
        titre_global = 'Superposition des distributions AOT40 en France (2000-2015)'
        unite = 'µg/m³·heure'
    elif pollutant_type == 'PM25':
        titre_global = 'Superposition des distributions PM2.5 en France (2000-2015)'
        unite = 'µg/m³'
    else:
        titre_global = f'Superposition des distributions {pollutant_type} en France (2000-2015)'
        unite = 'µg/m³'
    
    # Créer les steps pour le slider
    # Step pour "Toutes les années"
    steps = [dict(
        method="update",
        args=[{"visible": [True] * len(fig.data)}],
        label="Toutes les années"
    )]
    
    # Steps pour chaque année individuelle
    for year in years:
        visible = [str(year) == trace.name for trace in fig.data]
        if any(visible):  # Ne créer le step que si l'année existe dans les données
            step = dict(
                method="update",
                args=[{"visible": visible}],
                label=str(year)
            )
            steps.append(step)
    
    # Mise à jour du layout
    fig.update_layout(
        title=dict(
            text=titre_global,
            font=dict(size=24),
            y=0.95
        ),
        margin=dict(t=150),
        xaxis=dict(
            title=dict(
                text=f'Valeur ({unite})',
                font=dict(size=18)
            )
        ),
        yaxis=dict(
            title=dict(
                text='Fréquence',
                font=dict(size=18)
            )
        ),
        barmode='overlay',
        bargap=0.1,
        showlegend=False,
        sliders=[dict(
            active=0,
            currentvalue=dict(
                prefix="Année: ",
                xanchor="center",
                font=dict(size=16)
            ),
            pad=dict(t=50, b=10),
            yanchor="top",
            y=1.1,
            x=0.05,
            len=0.9,
            steps=steps
        )]
    )
    
    # Sauvegarder la figure
    output_file = os.path.join(output_dir, f'{pollutant_type}_histogrammes_superposes.html')
    fig.write_html(output_file)
    print(f"✓ Histogramme superposé créé pour {pollutant_type}")

def main():
    # Chemin vers le répertoire de sortie
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    output_dir = os.path.join(project_root, 'output')
    
    # Liste des polluants
    polluants = ['NO2', 'O3', 'PM10', 'PM25', 'AOT 40', 'somo 35']
    
    print("Création des histogrammes superposés...")
    # Créer les histogrammes superposés pour chaque polluant
    for polluant in polluants:
        print(f"\nTraitement de {polluant}...")
        superpose_histograms_for_pollutant(output_dir, polluant)
    
    print("\nTerminé ! Les fichiers ont été créés dans le dossier 'output'.")

if __name__ == "__main__":
    main()