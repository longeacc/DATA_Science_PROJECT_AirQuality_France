import os
import webbrowser

def create_html_viewer():
    # Dossier de sortie correspondant au script de génération
    output_dir = "src/database/output"

    # Polluants : doivent correspondre aux noms utilisés dans ton script Python
    pollutants = ["NO2", "PM10", "O3", "SOMO35", "PM25", "AOT40"]
    
    # Années disponibles (correspondent à celles générées)
    years = list(range(2000, 2016))
    years.remove(2006)
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Visualisation des Scatter Plots - Polluants Atmosphériques</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        h1 {{ margin: 0; }}
        .controls {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; display: flex; align-items: center; gap: 20px; }}
        .control-group {{ display: flex; align-items: center; gap: 10px; }}
        select {{ padding: 10px 15px; font-size: 16px; border: 2px solid #3498db; border-radius: 5px; cursor: pointer; background-color: white; min-width: 150px; }}
        select:hover {{ border-color: #2980b9; }}
        label {{ font-weight: bold; color: #2c3e50; }}
        .graph-container {{ background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow: hidden; }}
        iframe {{ width: 100%; height: 800px; border: none; display: block; }}
        .info {{ background-color: #e8f4f8; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #3498db; }}
        .slider-container {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .slider-container input[type="range"] {{ width: 100%; height: 8px; border-radius: 5px; background: #d3d3d3; outline: none; }}
        .slider-container input[type="range"]::-webkit-slider-thumb {{ appearance: none; width: 20px; height: 20px; border-radius: 50%; background: #3498db; cursor: pointer; }}
        .slider-container input[type="range"]::-moz-range-thumb {{ width: 20px; height: 20px; border-radius: 50%; background: #3498db; cursor: pointer; border: none; }}
        .year-display {{ text-align: center; font-size: 24px; font-weight: bold; color: #2c3e50; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Évolution des Polluants Atmosphériques - Scatter Plots</h1>
    </div>
    
    <div class="info">
        <strong>ℹ️ Information :</strong> Utilisez les contrôles ci-dessous pour naviguer entre les différents polluants et années.
    </div>
    
    <div class="controls">
        <div class="control-group">
            <label>🧪 Polluant:</label>
            <select id="pollutant-select">
"""

    for pollutant in pollutants:
        html_content += f'                <option value="{pollutant}">{pollutant}</option>\n'

    html_content += """            </select>
        </div>
    </div>
    
    <div class="slider-container">
        <label>📅 Année:</label>
        <input type="range" id="year-slider" min="0" max="14" value="0" step="1">
        <div class="year-display" id="year-display">2000</div>
    </div>
    
    <div class="graph-container">
        <iframe id="graph-frame" src=""></iframe>
    </div>
    
    <script>
        const pollutantSelect = document.getElementById('pollutant-select');
        const yearSlider = document.getElementById('year-slider');
        const yearDisplay = document.getElementById('year-display');
        const graphFrame = document.getElementById('graph-frame');
        
        const years = [""" + ', '.join([str(y) for y in years]) + """];
        
        function updateGraph() {
            const pollutant = pollutantSelect.value;
            const yearIndex = parseInt(yearSlider.value);
            const year = years[yearIndex];
            yearDisplay.textContent = year;

            // Correspond exactement aux fichiers générés par Python
            const filename = pollutant.replace(/ /g, '_') + "_" + year + "_scatter.html";
            graphFrame.src = "src/database/output/" + filename;
        }
        
        pollutantSelect.addEventListener('change', updateGraph);
        yearSlider.addEventListener('input', updateGraph);
        
        // Charger le premier graphique
        updateGraph();
    </script>
</body>
</html>
"""

    output_path = "superposed_scatter_plots.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Fichier {output_path} créé avec succès")
    
    # Ouvrir automatiquement dans le navigateur
    abs_path = os.path.abspath(output_path)
    webbrowser.open('file://' + abs_path)

if __name__ == "__main__":
    create_html_viewer()
