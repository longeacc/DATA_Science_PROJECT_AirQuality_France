import http.server
import socketserver
import webbrowser
import os

PORT = 8000

# Changer vers le répertoire du projet
os.chdir(r"C:\Users\Clement LONGEAC\Desktop\ESIEE SCHOOL\ESIEE E4\Python\Projet\DATA_Science_PROJECT_AirQuality_France")

Handler = http.server.SimpleHTTPRequestHandler

print(f"🌐 Serveur démarré sur http://localhost:{PORT}/")
print(f"📁 Répertoire: {os.getcwd()}")
print("\n📊 Ouvrez les liens suivants dans votre navigateur:")
print(f"   - Scatter Plots: http://localhost:{PORT}/output/FINAL_superposed_graphs_map/FINAL_superposed_scatter_plots.html")
print(f"   - Histogrammes: http://localhost:{PORT}/output/FINAL_superposed_graphs_map/FINAL_histogrammes_viewer.html")
print(f"   - Carte Interactive: http://localhost:{PORT}/output/FINAL_superposed_graphs_map/interactive_pollution_map.html")
print("\n🛑 Appuyez sur Ctrl+C pour arrêter le serveur\n")

# Ouvrir automatiquement dans le navigateur
webbrowser.open(f"http://localhost:{PORT}/output/FINAL_superposed_graphs_map/FINAL_superposed_scatter_plots.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Serveur arrêté")
