import os
import html
import dash

def generate_dashboard():
    """
    Génère un tableau de bord statique (3 onglets): README, Carte, Graphiques.
    Écrit le fichier dans ../output_csv/superposed_graphs_map/FINAL_dashboard.html
    et référence les fichiers HTML déjà générés sous ../output/FINAL_superposed_graphs_map/.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, '..'))

    # Emplacements de sortie et des fichiers existants
    output_dir = os.path.join(workspace_root, 'output_csv', 'superposed_graphs_map')
    os.makedirs(output_dir, exist_ok=True)
    dashboard_path = os.path.join(output_dir, 'FINAL_dashboard.html')

    # Emplacements possibles des sorties existantes
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

    # Chemins relatifs depuis le tableau de bord vers les fichiers ciblés
    def to_rel(src_abs):
      return os.path.relpath(os.path.dirname(src_abs), output_dir).replace('\\', '/') + '/' + os.path.basename(src_abs)

    map_src = to_rel(map_file) if map_file else None
    hist_src = to_rel(hist_viewer) if hist_viewer else None
    scatter_src = to_rel(scatter_viewer) if scatter_viewer else None

    # Contenu README
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

    # Échapper pour JS string
    readme_js = readme_md.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')

    # Messages d'erreur intégrés
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
    import webbrowser
    dashboard_file = generate_dashboard()
    webbrowser.open(f'file:///{dashboard_file.replace(os.sep, "/")}') 
