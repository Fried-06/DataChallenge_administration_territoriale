import pandas as pd
import numpy as np
import unicodedata

def norm(s):
    if pd.isna(s): return ""
    s = unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore').decode('utf-8')
    return s.strip().upper()

# 1. Inspecter la structure exacte de la population
df_pop = pd.read_csv("data/observationdata-kwwolwb (2).csv")
print("Total rows:", len(df_pop))
# Identifier les régions et préfectures
# Savanes = 1143520
# Kara = 985512
# Centrale = 795529
# Plateaux = 1635946
# Maritime = 1346615
# DAGL = 2188376 (Golfe = 1305681, Agoe-Nyive = 882695)
# Somme des 5 régions + DAGL:
s = 1143520 + 985512 + 795529 + 1635946 + 1346615 + 2188376
print(f"Somme Savanes + Kara + Centrale + Plateaux + Maritime + DAGL = {s} (Attendu: 8095498, match={s==8095498})")
print(f"Maritime fusionné = {1346615 + 2188376} = 3534991")

# 2. Inspecter les préfectures dans la population
# Regardons comment les préfectures sont imbriquées
# Dans le fichier kwwolwb, comment distinguer région, préfecture, commune, canton ?
# Analysons les indices et lignes de df_pop
for idx, row in df_pop.iterrows():
    val = row['Value']
    nom = row['découpage-administratif']
    if nom in ['SAVANES', 'KARA', 'CENTRALE', 'PLATEAUX', 'MARITIME', 'DAGL']:
        print(f"\nREGION: {nom} ({val}) à l'index {idx}")
    elif val > 40000 and idx < 100:
        print(f"  Row {idx}: {nom} = {val}")

# 3. Comparer préfectures des routes et auto-écoles avec la population
df_routes = pd.read_csv("data/file-routes-routes-classees-18-12-2024-20-38-02.csv")
df_ae = pd.read_csv("data/file-entreprises-auto-ecoles-02-01-2025-16-28-05.csv")

pref_routes = set(norm(p) for p in df_routes['prefecture_nom_bdd'].unique() if pd.notna(p))
pref_ae = set(norm(p) for p in df_ae['prefecture_nom_bdd'].unique() if pd.notna(p))
all_entities_pop = set(norm(p) for p in df_pop['découpage-administratif'].unique())

print("\nPréfectures dans routes classées:", sorted(list(pref_routes)))
print("Préfectures dans auto-écoles:", sorted(list(pref_ae)))
print("Préfectures routes absentes de la population (noms bruts normalisés):", pref_routes - all_entities_pop)
print("Préfectures auto-écoles absentes de la population (noms bruts normalisés):", pref_ae - all_entities_pop)
