import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import re
import ast

def extract_data_simple(file_path):
    """
    Extraction simple qui fonctionnait
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Pattern simple qui fonctionnait
        x_match = re.search(r'x\s*:\s*(\[.*?\])', content)
        y_match = re.search(r'y\s*:\s*(\[.*?\])', content)
        
        if x_match and y_match:
            x_data = ast.literal_eval(x_match.group(1))
            y_data = ast.literal_eval(y_match.group(1))
            return x_data, y_data
    except:
        pass
    return [], []

def create_all_pollutants_plot():
    """
    Crée un graphique avec TOUS les polluants visibles
    """
    print("=== CRÉATION DU GRAPHIQUE AVEC TOUS LES POLLUANTS ===")
    
    output_dir = "./output"
    pollutants = ["NO2", "AOT 40", "PM10", "PM25", "O3", "somo 35"]
    years = list(range(2000, 2016))
    years.remove(2006)
    
    # Créer une figure avec 6 sous-graphiques
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=pollutants,
        vertical_spacing=0.1,
        horizontal_spacing=0.1
    )
    
    # Pour stocker toutes les traces
    all_traces = []
    trace_count = 0
    
    # Couleurs différentes pour chaque année
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
              '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78',
              '#98df8a', '#ff9896', '#c5b0d5', '#c49c94']
    
    # Pour chaque polluant
    for i, pollutant in enumerate(pollutants):
        row = (i // 2) + 1
        col = (i % 2) + 1
        
        print(f"📊 Ajout de {pollutant}...")
        
        # Pour chaque année
        for j, year in enumerate(years):
            filename = f"{pollutant}_moyenne_annuelle_{year}.html"
            file_path = os.path.join(output_dir, filename)
            
            if os.path.exists(file_path):
                x_data, y_data = extract_data_simple(file_path)
                
                if x_data and y_data:
                    # Créer la trace
                    trace = go.Scatter(
                        x=x_data,
                        y=y_data,
                        mode='markers',
                        name=f'{pollutant} {year}',
                        marker=dict(
                            size=4,
                            color=colors[j % len(colors)],
                            opacity=0.6
                        ),
                        visible=(year == 2000),  # Seulement 2000 visible au début
                        legendgroup=f'group{year}',
                        showlegend=False
                    )
                    
                    # Ajouter au bon sous-graphique
                    fig.add_trace(trace, row=row, col=col)
                    all_traces.append((pollutant, year, trace_count))
                    trace_count += 1
                    print(f"  ✅ {year}: {len(y_data)} points")
    
    print(f"\n📈 Total: {trace_count} traces créées")
    
    # Créer les steps pour le slider
    steps = []
    for i, year in enumerate(years):
        step = dict(
            method="update",
            args=[{"visible": [False] * trace_count}],
            label=str(year)
        )
        
        # Rendre visibles seulement les traces de cette année
        for trace_info in all_traces:
            pollutant, trace_year, trace_idx = trace_info
            if trace_year == year:
                step["args"][0]["visible"][trace_idx] = True
        
        steps.append(step)
    
    # Ajouter le slider
    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Année: "},
        pad={"t": 50},
        steps=steps
    )]
    
    # Mise en page
    fig.update_layout(
        height=1200,
        width=1400,
        title_text="Évolution de tous les polluants (2000-2015) - Utilisez le slider pour changer d'année",
        title_x=0.5,
        sliders=sliders,
        showlegend=False
    )
    
    # Configurer les axes
    for i, pollutant in enumerate(pollutants):
        row = (i // 2) + 1
        col = (i % 2) + 1
        fig.update_xaxes(title_text="Communes", row=row, col=col)
        fig.update_yaxes(title_text=f"Concentration {pollutant}", row=row, col=col)
    
    # Sauvegarder
    output_filename = "ALL_pollutants_superposed.html"
    fig.write_html(output_filename)
    print(f"\n✅ GRAPHIQUE COMPLET sauvegardé: {output_filename}")
    print("📁 Ouvrez ce fichier dans votre navigateur pour voir TOUS les polluants")
    
    return fig

def create_simple_comparison():
    """
    Version simple avec moyenne par année pour tous les polluants
    """
    print("\n=== CRÉATION VERSION SIMPLIFIÉE ===")
    
    output_dir = "./output"
    pollutants = ["NO2", "AOT 40", "PM10", "PM25", "O3", "somo 35"]
    years = list(range(2000, 2016))
    years.remove(2006)
    
    # Stocker les moyennes
    data_by_pollutant = {}
    
    for pollutant in pollutants:
        print(f"📊 Calcul des moyennes pour {pollutant}...")
        yearly_means = []
        
        for year in years:
            filename = f"{pollutant}_moyenne_annuelle_{year}.html"
            file_path = os.path.join(output_dir, filename)
            
            if os.path.exists(file_path):
                x_data, y_data = extract_data_simple(file_path)
                if y_data:
                    mean_val = sum(y_data) / len(y_data)
                    yearly_means.append(mean_val)
                    print(f"  {year}: {mean_val:.2f}")
                else:
                    yearly_means.append(None)
            else:
                yearly_means.append(None)
        
        data_by_pollutant[pollutant] = yearly_means
    
    # Créer le graphique de comparaison
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, pollutant in enumerate(pollutants):
        means = data_by_pollutant[pollutant]
        valid_data = [(year, mean) for year, mean in zip(years, means) if mean is not None]
        
        if valid_data:
            years_valid, means_valid = zip(*valid_data)
            fig.add_trace(go.Scatter(
                x=years_valid,
                y=means_valid,
                mode='lines+markers',
                name=pollutant,
                line=dict(color=colors[i], width=3),
                marker=dict(size=6)
            ))
    
    fig.update_layout(
        title="Évolution des concentrations moyennes de tous les polluants",
        xaxis_title="Année",
        yaxis_title="Concentration moyenne",
        template="plotly_white",
        height=600,
        width=1000
    )
    
    output_filename = "ALL_pollutants_comparison.html"
    fig.write_html(output_filename)
    print(f"✅ COMPARAISON sauvegardée: {output_filename}")
    
    return fig

if __name__ == "__main__":
    print("🚀 CRÉATION DES GRAPHIQUES AVEC TOUS LES POLLUANTS")
    print("=" * 50)
    
    # Version 1: Graphique complet avec slider
    fig1 = create_all_pollutants_plot()
    
    # Version 2: Comparaison simplifiée
    fig2 = create_simple_comparison()
    
    print("\n" + "=" * 50)
    print("🎉 CRÉATION TERMINÉE !")
    print("\n📁 FICHIERS GÉNÉRÉS:")
    print("1. ALL_pollutants_superposed.html - Version complète avec slider")
    print("2. ALL_pollutants_comparison.html - Version simplifiée avec courbes")
    print("\n💡 CONSEILS:")
    print("   - Ouvrez ALL_pollutants_superposed.html pour voir TOUS les polluants")
    print("   - Utilisez le slider en bas pour changer d'année")
    print("   - Chaque sous-graphique montre un polluant différent")