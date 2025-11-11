import os
import webbrowser

def create_histograms_viewer():
    output_dir = "output"
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
        <h1>📊 Histogrammes des Polluants Atmosphériques</h1>
        <p>Distribution des concentrations par commune</p>
    </div>
    
    <div class="info">
        <strong>ℹ️ Information :</strong> Visualisez la distribution des concentrations de polluants à travers les communes françaises. Les histogrammes montrent la fréquence des différentes concentrations.
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
        
        <div class="view-type">
            <button class="view-btn active" id="btn-single">Année unique</button>
            <button class="view-btn" id="btn-comparison">Comparaison</button>
            <button class="view-btn" id="btn-evolution">Évolution</button>
        </div>
    </div>
    
    <div class="slider-container" id="single-year-container">
        <label>📅 Année:</label>
        <input type="range" id="year-slider" min="0" max="14" value="0" step="1">
        <div class="year-display" id="year-display">2000</div>
    </div>
    
    <div class="comparison-controls" id="comparison-container">
        <div class="comparison-group">
            <div class="control-group">
                <label>📅 Année 1:</label>
                <select id="year1-select">
"""
    
    for year in years:
        html_content += f'                    <option value="{year}">{year}</option>\n'
    
    html_content += """                </select>
            </div>
            <div class="control-group">
                <label>📅 Année 2:</label>
                <select id="year2-select">
"""
    
    for year in years:
        if year != 2000:  # Éviter la même année par défaut
            html_content += f'                    <option value="{year}">{year}</option>\n'
        else:
            html_content += f'                    <option value="{year}" selected>{year}</option>\n'
    
    html_content += """                </select>
            </div>
        </div>
    </div>
    
    <div class="graph-container">
        <iframe id="graph-frame" src=""></iframe>
    </div>
    
    <script>
        // Éléments DOM
        const pollutantSelect = document.getElementById('pollutant-select');
        const yearSlider = document.getElementById('year-slider');
        const yearDisplay = document.getElementById('year-display');
        const graphFrame = document.getElementById('graph-frame');
        const btnSingle = document.getElementById('btn-single');
        const btnComparison = document.getElementById('btn-comparison');
        const btnEvolution = document.getElementById('btn-evolution');
        const singleYearContainer = document.getElementById('single-year-container');
        const comparisonContainer = document.getElementById('comparison-container');
        const year1Select = document.getElementById('year1-select');
        const year2Select = document.getElementById('year2-select');
        
        const years = ["""
    
    html_content += ', '.join([str(year) for year in years])
    
    html_content += """];
        
        let currentView = 'single';
        
        // Fonction pour mettre à jour le graphique
        function updateGraph() {
            const pollutant = pollutantSelect.value;
            
            if (currentView === 'single') {
                const yearIndex = parseInt(yearSlider.value);
                const year = years[yearIndex];
                yearDisplay.textContent = year;
                
                const filename = `${pollutant}_histogram_${year}.html`;
                graphFrame.src = `output/${filename}`;
                
            } else if (currentView === 'comparison') {
                const year1 = year1Select.value;
                const year2 = year2Select.value;
                
                const filename = `${pollutant}_histogram_comparison_${year1}_${year2}.html`;
                graphFrame.src = `output/${filename}`;
                
            } else if (currentView === 'evolution') {
                const filename = `${pollutant}_histogram_evolution.html`;
                graphFrame.src = `output/${filename}`;
            }
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
        
        // Événements
        pollutantSelect.addEventListener('change', updateGraph);
        yearSlider.addEventListener('input', updateGraph);
        year1Select.addEventListener('change', updateGraph);
        year2Select.addEventListener('change', updateGraph);
        
        btnSingle.addEventListener('click', () => setView('single'));
        btnComparison.addEventListener('click', () => setView('comparison'));
        btnEvolution.addEventListener('click', () => setView('evolution'));
        
        // Charger le premier graphique
        setView('single');
        
        // Gestion des erreurs de charnement
        graphFrame.addEventListener('load', function() {
            if (graphFrame.contentDocument.body.innerHTML.includes('404') || 
                graphFrame.contentDocument.body.innerHTML.includes('Not Found')) {
                graphFrame.contentDocument.body.innerHTML = `
                    <div style="display: flex; justify-content: center; align-items: center; height: 100%; flex-direction: column; color: #666;">
                        <h2>📊 Histogramme non disponible</h2>
                        <p>Le fichier histogramme pour cette sélection n'a pas encore été généré.</p>
                        <p>Utilisez le script Python pour créer les histogrammes d'abord.</p>
                    </div>
                `;
            }
        });
    </script>
</body>
</html>
"""
    
    output_path = "histogrammes_viewer.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Fichier {output_path} créé avec succès")
    
    # Créer aussi les fichiers histogrammes de base
    create_basic_histograms()
    
    # Ouvrir automatiquement dans le navigateur
    abs_path = os.path.abspath(output_path)
    webbrowser.open('file://' + abs_path)

def create_basic_histograms():
    """
    Crée quelques histogrammes de base pour tester l'interface
    """
    print("🔄 Création des histogrammes de base...")
    
    # Cette fonction créerait les fichiers HTML d'histogrammes
    # Pour l'instant, on va créer des fichiers de démonstration
    import plotly.graph_objects as go
    import numpy as np
    
    pollutants = ["NO2", "PM10", "O3"]
    years = [2000, 2010, 2015]
    
    for pollutant in pollutants:
        for year in years:
            # Données factices réalistes
            if pollutant == "NO2":
                data = np.random.normal(25 - (year-2000)*0.5, 8, 1000)
            elif pollutant == "PM10":
                data = np.random.normal(18 - (year-2000)*0.3, 5, 1000)
            elif pollutant == "O3":
                data = np.random.normal(35 + (year-2000)*0.2, 10, 1000)
            else:
                data = np.random.normal(20, 6, 1000)
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=data,
                nbinsx=20,
                name=f'{pollutant} {year}',
                marker_color='#1f77b4',
                opacity=0.7
            ))
            
            # Ajouter la moyenne
            mean_val = np.mean(data)
            fig.add_vline(x=mean_val, line_dash="dash", line_color="red", 
                         annotation_text=f"Moyenne: {mean_val:.2f}")
            
            fig.update_layout(
                title=f"Distribution {pollutant} - {year}",
                xaxis_title=f"Concentration {pollutant}",
                yaxis_title="Nombre de communes",
                template="plotly_white",
                height=500
            )
            
            # Sauvegarder
            filename = f"output/{pollutant}_histogram_{year}.html"
            fig.write_html(filename)
            print(f"  ✅ {filename} créé")

if __name__ == "__main__":
    create_histograms_viewer()