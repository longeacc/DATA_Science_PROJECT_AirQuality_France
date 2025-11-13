import os
import webbrowser

def create_scatter_plots_viewer():
    output_dir = "output/FINAL_superposed_graphs_map"
    pollutants = ["NO2", "PM10", "O3", "somo 35", "PM25", "AOT 40"]
    years = list(range(2000, 2016))
    years.remove(2006)
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Visualisation des Histogrammes - Polluants Atmosphériques</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        h1 { margin: 0; }
        .controls { 
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        .control-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        select { 
            padding: 10px 15px; 
            font-size: 16px; 
            border: 2px solid #3498db;
            border-radius: 5px;
            cursor: pointer;
            background-color: white;
            min-width: 150px;
        }
        select:hover {
            border-color: #2980b9;
        }
        label { 
            font-weight: bold; 
            color: #2c3e50;
        }
        .graph-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
            margin-bottom: 20px;
        }
        iframe { 
            width: 100%; 
            height: 600px; 
            border: none;
            display: block;
        }
        .info {
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #3498db;
        }
        .slider-container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .slider-container input[type="range"] {
            width: 100%;
            height: 8px;
            border-radius: 5px;
            background: #d3d3d3;
            outline: none;
        }
        .slider-container input[type="range"]::-webkit-slider-thumb {
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #3498db;
            cursor: pointer;
        }
        .slider-container input[type="range"]::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #3498db;
            cursor: pointer;
            border: none;
        }
        .year-display {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-top: 10px;
        }
        .view-type {
            display: flex;
            gap: 10px;
            margin-left: auto;
        }
        .view-btn {
            padding: 10px 20px;
            border: 2px solid #3498db;
            background-color: white;
            color: #3498db;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        .view-btn.active {
            background-color: #3498db;
            color: white;
        }
        .view-btn:hover {
            background-color: #2980b9;
            color: white;
            border-color: #2980b9;
        }
        .comparison-controls {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            display: none;
        }
        .comparison-group {
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }
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
        
        const years = ["""
    
    html_content += ', '.join([str(year) for year in years])
    
    html_content += """];
        
        // Fonction pour mettre à jour le graphique
        function updateGraph() {
            const pollutant = pollutantSelect.value;
            const yearIndex = parseInt(yearSlider.value);
            const year = years[yearIndex];
            yearDisplay.textContent = year;
            
            const filename = `${pollutant}_moyenne_annuelle_${year}.html`;
            graphFrame.src = `../${filename}`;
        }
        
        // Fonction pour changer la vue
        function setView(viewType) {
            currentView = viewType;
            
            // Mettre à jour les boutons
            btnSingle.classList.remove('active');
            btnComparison.classList.remove('active');
            btnEvolution.classList.remove('active');
            
            // Afficher/masquer les conteneurs
            singleYearContainer.style.display = 'none';
            comparisonContainer.style.display = 'none';
            
            if (viewType === 'single') {
                btnSingle.classList.add('active');
                singleYearContainer.style.display = 'block';
            } else if (viewType === 'comparison') {
                btnComparison.classList.add('active');
                comparisonContainer.style.display = 'block';
            } else if (viewType === 'evolution') {
                btnEvolution.classList.add('active');
            }
            
            updateGraph();
        }
        
        pollutantSelect.addEventListener('change', updateGraph);
        yearSlider.addEventListener('input', updateGraph);
        
        // Charger le premier graphique
        updateGraph();
    </script>
</body>
</html>
"""
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "FINAL_superposed_scatter_plots.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Fichier {output_path} créé avec succès")

if __name__ == "__main__":
    create_scatter_plots_viewer()