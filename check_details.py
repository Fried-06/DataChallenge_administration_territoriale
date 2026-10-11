import pandas as pd
import numpy as np
from shapely import wkt
import math

# 1. Verification population Togo & hierarchie
df_pop = pd.read_csv("data/observationdata-kwwolwb (2).csv")
# Explorons la hierarchie
print("=== VERIFICATION POPULATION ===")
# Les 5 regions traditionnelles + grand lome ?
regions_check = ['SAVANES', 'KARA', 'CENTRALE', 'PLATEAUX', 'MARITIME', 'GRAND LOME']
# Regardons toutes les lignes au niveau 1
print(df_pop[df_pop['Value'] > 200000][['découpage-administratif', 'Value']])

# 2. Verification routes classee km avec Shapely et projection UTM 31N
print("\n=== VERIFICATION ROUTES CLASSEES KM ===")
df_routes = pd.read_csv("data/file-routes-routes-classees-18-12-2024-20-38-02.csv")

def haversine_dist(lon1, lat1, lon2, lat2):
    R = 6371.0 # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def geom_length_km(geom_wkt):
    try:
        g = wkt.loads(geom_wkt)
        length_km = 0.0
        if g.geom_type == 'LineString':
            coords = list(g.coords)
            for i in range(len(coords)-1):
                length_km += haversine_dist(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
        elif g.geom_type == 'MultiLineString':
            for line in g.geoms:
                coords = list(line.coords)
                for i in range(len(coords)-1):
                    length_km += haversine_dist(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
        return length_km
    except Exception as e:
        return 0.0

df_routes['km_calc'] = df_routes['geometry'].apply(geom_length_km)
print("Total km calculé (Haversine WGS84):", df_routes['km_calc'].sum())
print("Par type de route:")
print(df_routes.groupby('route_type')['km_calc'].agg(['count', 'sum']))
print("Par recouvrement:")
print(df_routes.groupby('route_recouvrement')['km_calc'].agg(['count', 'sum']))

# 3. Verification tmdtnad
print("\n=== VERIFICATION TMDTNAD ===")
df_tmd = pd.read_csv("data/observationdata-tmdtnad.csv")
# Regardons comment les troncons sont structures
# Est-ce qu'il y a des troncons avec plusieurs etats ?
piv_tmd = df_tmd.pivot_table(index=['indicateur', 'tronçon'], columns='etat', values='Value', fill_value=0).reset_index()
print(f"Nombre total de (indicateur, troncon) uniques: {len(piv_tmd)}")
print("Aperçu pivot tmdtnad:")
print(piv_tmd.head(10))

# Vérif TOTAL vs somme
piv_tmd['SOMME_COMPOSANTES'] = piv_tmd.get('BON', 0) + piv_tmd.get('MOYEN', 0) + piv_tmd.get('MAUVAIS', 0) + piv_tmd.get('TRAVAUX', 0)
piv_tmd['DIFF'] = piv_tmd['SOMME_COMPOSANTES'] - piv_tmd['TOTAL']
print("Tronçons avec écart > 0.05 km entre TOTAL et somme:")
print(piv_tmd[piv_tmd['DIFF'].abs() > 0.05][['indicateur', 'tronçon', 'TOTAL', 'SOMME_COMPOSANTES', 'DIFF']])
