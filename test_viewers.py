import http.server
import socketserver
import webbrowser
import os

PORT = 8000

# Change to the project directory
os.chdir(r"DATA_Science_PROJECT_AirQuality_France")

Handler = http.server.SimpleHTTPRequestHandler

print(f" Server started on http://localhost:{PORT}/")
print(f" Directory: {os.getcwd()}")
print("\n Open the following links in your browser:")
print(f"   - Scatter Plots: http://localhost:{PORT}/output/FINAL_superposed_graphs_map/FINAL_superposed_scatter_plots.html")
print(f"   - Histograms: http://localhost:{PORT}/output/FINAL_superposed_graphs_map/FINAL_histogrammes_viewer.html")
print(f"   - Interactive Map: http://localhost:{PORT}/output/FINAL_superposed_graphs_map/interactive_pollution_map.html")
print("\n Press Ctrl+C to stop the server\n")
# Automatically open in the browser
webbrowser.open(f"http://localhost:{PORT}/output/FINAL_superposed_graphs_map/FINAL_superposed_scatter_plots.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n Server stopped")
