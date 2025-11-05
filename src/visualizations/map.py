# import pandas as pd
# from geopy.geocoders import Nominatim  
# import folium
# from folium.plugins import HeatMap
# import time
# df = pd.read_csv("data/cleaned/cleaned_air_quality_with_year.csv")
# # Vérifier les premières lignes
# print(df.head())
# # Exemple : les 5 premières communes
# df_test = df.head(5)
# # --- 2️⃣ Sélectionner les 5 premières communes pour le test ---
# df_test = df.head(5).copy()

# # --- 3️⃣ Géocoder les communes ---
# geolocator = Nominatim(user_agent="pollution_mapper")

# def get_coords(commune):
#     try:
#         location = geolocator.geocode(f"{commune}, France")
#         if location:
#             return location.latitude, location.longitude
#         else:
#             return None, None
#     except:
#         return None, None

# # Appliquer la géolocalisation
# df_test[['latitude', 'longitude']] = df_test['Commune'].apply(lambda x: pd.Series(get_coords(x)))
# time.sleep(1)  # éviter de surcharger l'API

# print(df_test[['Commune', 'latitude', 'longitude']])

# # --- 4️⃣ Créer une carte avec HeatMap ---
# # Filtrer les lignes avec des coordonnées valides
# df_map = df_test.dropna(subset=['latitude', 'longitude'])

# # Préparer les données pour la heatmap : [lat, lon, poids] (PM10)
# heat_data = [[row['latitude'], row['longitude'], row['Moyenne annuelle de concentration de PM10 (ug/m3)']] for _, row in df_map.iterrows()]

# # Créer la carte centrée sur la France
# map_test = folium.Map(location=[46.5, 2.5], zoom_start=6)

# # Ajouter la heatmap
# HeatMap(heat_data, radius=15, max_zoom=13).add_to(map_test)

# # --- 5️⃣ Sauvegarder la carte ---
# map_test.save("map_test_communes.html")
# print("Carte sauvegardée sous map_test_communes.html") 

# if 'latitude' in df.columns and 'longitude' in df.columns:
#     missing_coords = df[df['latitude'].isna() | df['longitude'].isna()]
#     print("Communes sans coordonnées :")
#     print(missing_coords[['Commune', 'COM Insee', 'latitude', 'longitude']])
# else:
#     print("Les colonnes latitude et longitude n'existent pas encore.") 

import pandas as pd
import folium
from folium.plugins import HeatMap

# --- 1️⃣ Charger les datasets ---
# Dataset pollution
df_pollution = pd.read_csv("data/cleaned/cleaned_air_quality_with_year.csv")

# Dataset communes avec lat/lon
df_communes = pd.read_csv("data/cleaned/base-officielle-codes-postaux.csv", dtype={"code_commune_insee": str})

# --- 2️⃣ Préparer les colonnes pour le merge ---
df_pollution['COM Insee'] = df_pollution['COM Insee'].astype(str)
df_communes['code_commune_insee'] = df_communes['code_commune_insee'].astype(str)

# --- 3️⃣ Merge pour ajouter latitude et longitude ---
df_merged = df_pollution.merge(
    df_communes[['code_commune_insee', 'latitude', 'longitude']],
    left_on='COM Insee',
    right_on='code_commune_insee',
    how='left'
)

# --- 4️⃣ Vérifier les communes sans coordonnées ---
missing_coords = df_merged[df_merged['latitude'].isna() | df_merged['longitude'].isna()]
print(f"Communes sans coordonnées : {missing_coords.shape[0]}")
print(missing_coords[['Commune', 'COM Insee']])

# --- 5️⃣ Créer une carte Folium avec HeatMap (PM10) ---
# Filtrer seulement les lignes avec coordonnées valides
df_map = df_merged.dropna(subset=['latitude', 'longitude'])

# Préparer les données pour HeatMap : [lat, lon, poids]
heat_data = [[row['latitude'], row['longitude'], row['Moyenne annuelle de concentration de PM10 (ug/m3)']]
             for _, row in df_map.iterrows()]

# Créer la carte centrée sur la France
map_pm10 = folium.Map(location=[46.5, 2.5], zoom_start=6)

# Ajouter la HeatMap
HeatMap(heat_data, radius=15, max_zoom=13).add_to(map_pm10)

# --- 6️⃣ Sauvegarder la carte ---
map_pm10.save("map_pm10_communes.html")
print("Carte sauvegardée sous map_pm10_communes.html")
