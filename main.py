"""
Script pour générer des graphiques de pollution en France.
Crée des histogrammes et des scatter plots pour chaque polluant et année.
"""
import webbrowser
import os
import html
import pandas as pd
from plotly.io import write_html
from src.utils.common_functions import load_commune_mappings, load_data_for_year
from src.visualizations.scatter_plots import create_pollution_scatter
from src.visualizations.histograms import create_pollution_histogram


def generate_graphs():
    """
    Fonction pour générer tous les graphiques (histogrammes et scatter plots).
    """
    try:
        print("\nChargement des données pour toutes les années...")
        data = pd.DataFrame()
        
        commune_to_insee, insee_to_commune = load_commune_mappings()
        if commune_to_insee is None or insee_to_commune is None:
            print("Erreur : Impossible de charger les correspondances des communes.")
            return
        
        print(f"Correspondances des communes chargées : {len(commune_to_insee)} communes")
        
        for year in range(2000, 2016):
            if year == 2006:
                continue
            print(f"\nChargement des données pour l'année {year}...")
            year_data = load_data_for_year(year)
            if year_data is not None:
                communes_manquantes = [c for c in year_data['Commune'] if c not in commune_to_insee]
                if communes_manquantes:
                    print(f"Attention : {len(communes_manquantes)} communes non trouvées en {year}")
                data = pd.concat([data, year_data], ignore_index=True)
        
        if data.empty:
            print("Erreur : aucune donnée chargée.")
            return

        # Créer les dossiers de sortie
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_hist_dir = os.path.join(script_dir, 'assets', 'html_histograms')
        output_scatter_dir = os.path.join(script_dir, 'assets', 'scatter')
        os.makedirs(output_hist_dir, exist_ok=True)
        os.makedirs(output_scatter_dir, exist_ok=True)
        print(f"Dossiers créés :\n- Histogrammes : {output_hist_dir}\n- Scatter : {output_scatter_dir}")

        # Polluants et colonnes
        polluants_tous = ['NO2', 'PM10', 'O3', 'Somo 35', 'AOT 40']
        polluant_2009 = 'PM25'
        noms_colonnes = {
            'NO2': 'Moyenne annuelle de concentration de NO2 (ug/m3)',
            'PM10': 'Moyenne annuelle de concentration de PM10 (ug/m3)',
            'O3': 'Moyenne annuelle de concentration de O3 (ug/m3)',
            'Somo 35': 'Moyenne annuelle de somo 35 (ug/m3.jour)',
            'AOT 40': "Moyenne annuelle d'AOT 40 (ug/m3.heure)",
            'PM25': 'Moyenne annuelle de concentration de PM25 (ug/m3)'
        }

        années = sorted(data['Année'].unique())
        for année in années:
            print(f"\nTraitement de l'année {année}...")
            données_année = data[data['Année'] == année]
            
            polluants_à_traiter = polluants_tous.copy()
            if année >= 2009:
                polluants_à_traiter.append(polluant_2009)
            
            for polluant in polluants_à_traiter:
                colonne = noms_colonnes[polluant]
                if colonne not in données_année.columns:
                    print(f"  Données non disponibles pour {polluant} en {année}")
                    continue
                
                try:
                    # Scatter plot
                    fig_scatter = create_pollution_scatter(données_année, insee_to_commune, polluant)
                    scatter_file = os.path.join(output_scatter_dir, f'{polluant}_scatter_{année}.html')
                    write_html(fig_scatter, scatter_file, auto_open=False, include_plotlyjs='cdn')
                    
                    # Histogramme
                    fig_hist = create_pollution_histogram(données_année, polluant)
                    hist_file = os.path.join(output_hist_dir, f'{polluant}_histogram_{année}.html')
                    write_html(fig_hist, hist_file, auto_open=False, include_plotlyjs='cdn')
                    
                    print(f"  ✓ Graphiques générés pour {polluant}")
                except Exception as e:
                    print(f"  ✗ Erreur lors de la génération des graphiques pour {polluant} : {e}")

        print("\nToutes les visualisations ont été générées avec succès !")
        
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


def generate_dashboard():
    """
    Generates a static dashboard (3 tabs): README, Map, Graphs.
Writes the file to ../output_csv/superposed_graphs_map/FINAL_dashboard.html
and references the HTML files already generated in ../output/FINAL_superposed_graphs_map/.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, '..'))

    # Output locations and existing files
    output_dir = os.path.join(workspace_root, 'output_csv', 'superposed_graphs_map')
    os.makedirs(output_dir, exist_ok=True)
    dashboard_path = os.path.join(output_dir, 'FINAL_dashboard.html')

    # Possible locations of existing outputs
    candidates_base = [
      os.path.join(script_dir, 'assets', 'output_csv', 'FINAL_superposed_graphs_map'),
      os.path.join(script_dir, 'assets', 'maps'),
      os.path.join(script_dir, 'assets'),
      os.path.join(workspace_root, 'output', 'FINAL_superposed_graphs_map'),
    ]

    def find_existing_file(possible_dirs, filename):
      for d in possible_dirs:
        p = os.path.join(d, filename)
        if os.path.exists(p):
          return p
      return None

    map_file = find_existing_file(
      [
        os.path.join(script_dir, 'assets', 'output_csv', 'FINAL_superposed_graphs_map'),
        os.path.join(script_dir, 'assets', 'maps'),
        os.path.join(script_dir, 'assets'),
        os.path.join(workspace_root, 'output', 'FINAL_superposed_graphs_map'),
      ],
      'interactive_pollution_map.html'
    )
    hist_viewer = find_existing_file(candidates_base, 'FINAL_histogrammes_viewer.html')
    scatter_viewer = find_existing_file(candidates_base, 'FINAL_superposed_scatter_plots.html')

    # Relative paths from the dashboard to the targeted files
    def to_rel(src_abs):
      return os.path.relpath(os.path.dirname(src_abs), output_dir).replace('\\', '/') + '/' + os.path.basename(src_abs)

    map_src = to_rel(map_file) if map_file else None
    hist_src = to_rel(hist_viewer) if hist_viewer else None
    scatter_src = to_rel(scatter_viewer) if scatter_viewer else None

    # README content
    readme_path = os.path.join(script_dir, 'README.md')
    readme_md = ''
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_md = f.read()
        except Exception:
            readme_md = '# README\nImpossible de lire README.md.'
    else:
        readme_md = '# README\nAucun fichier README.md trouvé dans le projet.'

    readme_js = readme_md.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')

    def iframe_or_message(src, message):
        if src:
            return f'<iframe src="{src}" class="content-frame"></iframe>'
        return f'<div class="missing">{html.escape(message)}</div>'

    map_block = iframe_or_message(map_src, 'Carte introuvable: interactive_pollution_map.html')
    hist_block = iframe_or_message(hist_src, 'Viewer histogrammes introuvable: FINAL_histogrammes_viewer.html')
    scatter_block = iframe_or_message(scatter_src, 'Viewer scatter introuvable: FINAL_superposed_scatter_plots.html')

    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Dashboard Pollution - README | Carte | Graphiques</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root {{
      --bg: #f5f7fb; --surface: #ffffff; --text: #2c3e50; --muted: #6b7280;
      --primary: #2563eb; --primary-600: #1d4ed8; --primary-700: #1e40af;
      --border: #e5e7eb; --sidebar-width: 220px;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font-family: -apple-system, Segoe UI, Roboto, Arial, sans-serif; background: var(--bg); color: var(--text); display: flex; height: 100vh; overflow: hidden; }}
    .sidebar {{ width: var(--sidebar-width); background: var(--surface); border-right: 2px solid var(--border); display: flex; flex-direction: column; }}
    .header {{ background: linear-gradient(135deg, var(--primary), var(--primary-700)); color:#fff; padding: 20px 16px; border-bottom: 1px solid rgba(255,255,255,0.1); }}
    .header h1 {{ margin:0; font-size: 16px; font-weight: 600; line-height: 1.3; }}
    .tabs {{ display:flex; flex-direction: column; gap:6px; padding: 16px 12px; flex: 1; }}
    .tab-btn {{ padding:12px 14px; border:1px solid var(--border); background: #fff; color: var(--text); border-radius:8px; cursor:pointer; font-weight:600; font-size:14px; text-align: left; transition: all 0.2s; }}
    .tab-btn:hover {{ background: #f9fafb; border-color: var(--primary-600); }}
    .tab-btn.active {{ background: var(--primary); color:#fff; border-color: transparent; box-shadow: 0 2px 4px rgba(37,99,235,0.2); }}
    .main-content {{ flex: 1; display: flex; flex-direction: column; overflow: hidden; }}
    .container {{ flex: 1; padding: 0; overflow: hidden; }}
    .card {{ background: var(--surface); border:1px solid var(--border); border-radius: 10px; box-shadow: 0 2px 8px rgba(16,24,40,0.04); padding: 20px; height: 100%; overflow: auto; }}
    .card.map-card {{ padding: 0; overflow: hidden; }}
    .content-frame {{ width: 100%; height: 100%; border: none; border-radius: 8px; }}
    .missing {{ padding: 16px; color: #b91c1c; background: #fee2e2; border: 1px solid #fecaca; border-radius: 8px; }}
    .readme {{ line-height: 1.6; color: var(--text); }}
    .readme h1, .readme h2, .readme h3 {{ margin-top: 1.2em; }}
    .readme pre {{ background:#0b1020; color:#e5e7eb; padding:12px; border-radius:8px; overflow:auto; }}
    .subtabs {{ display:flex; gap:8px; margin-bottom: 12px; }}
    .page {{ display: none; height: 100%; }}
    .page.active {{ display: block; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {{
      // Tabs gestion
      const pages = ['readme','map','graphs'];
      function show(id) {{
        pages.forEach(p => {{
          document.getElementById('page-'+p).style.display = (p===id)?'block':'none';
          document.getElementById('tab-'+p).classList.toggle('active', p===id);
        }});
      }}
      window.switchTab = function(id) {{
        pages.forEach(p => {{
          const page = document.getElementById('page-'+p);
          const tab = document.getElementById('tab-'+p);
          if (p === id) {{
            page.classList.add('active');
            tab.classList.add('active');
          }} else {{
            page.classList.remove('active');
            tab.classList.remove('active');
          }}
        }});
      }};
      window.switchTab('readme');

      // Render README markdown
      const md = "{readme_js}";
      const target = document.getElementById('readme-content');
      try {{ target.innerHTML = marked.parse(md); }} catch(e) {{ target.textContent = md; }}

      // Graphs subtabs
      const histBtn = document.getElementById('subtab-hist');
      const scatBtn = document.getElementById('subtab-scat');
      const frame = document.getElementById('graphs-frame');
      histBtn?.addEventListener('click', function() {{
        histBtn.classList.add('active'); scatBtn.classList.remove('active');
        frame.src = '{hist_src if hist_src else ''}';
      }});
      scatBtn?.addEventListener('click', function() {{
        scatBtn.classList.add('active'); histBtn.classList.remove('active');
        frame.src = '{scatter_src if scatter_src else ''}';
      }});
      // Default subtab
      if (histBtn && scatBtn) {{ histBtn.click(); }}
    }});
  </script>
</head>
<body>
  <div class="sidebar">
    <div class="header">
      <h1>📊 Dashboard Pollution Atmosphérique France</h1>
    </div>
    <div class="tabs">
      <button id="tab-readme" class="tab-btn" onclick="switchTab('readme')">📄 README</button>
      <button id="tab-map" class="tab-btn" onclick="switchTab('map')">🗺️ Carte Interactive</button>
      <button id="tab-graphs" class="tab-btn" onclick="switchTab('graphs')">📊 Graphiques</button>
    </div>
  </div>
  <div class="main-content">
    <div class="container">
      <div id="page-readme" class="page card">
        <div id="readme-content" class="readme"></div>
      </div>
      <div id="page-map" class="page card map-card">
        {map_block}
      </div>
      <div id="page-graphs" class="page card">
        <div class="subtabs">
          <button id="subtab-hist" class="tab-btn">Histogrammes</button>
          <button id="subtab-scat" class="tab-btn">Scatter Plots</button>
        </div>
        {('<div class="missing">Aucun viewer trouvé.</div>' if (not hist_src and not scatter_src) else '<iframe id="graphs-frame" class="content-frame"></iframe>')}
    </div>
  </div>
</body>
</html>
"""

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Dashboard généré:")
    print(dashboard_path)
    return dashboard_path


if __name__ == '__main__':
    # Générer les graphiques (scatter plots et histogrammes)
    print("=== Génération des graphiques ===")
    generate_graphs()
    
    # Générer le dashboard
    print("\n=== Génération du dashboard ===")
    dashboard_file = generate_dashboard()
    webbrowser.open(f'file:///{dashboard_file.replace(os.sep, "/")}') 
    
