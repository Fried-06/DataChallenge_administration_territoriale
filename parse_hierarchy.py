import pandas as pd
import unicodedata

def norm(s):
    if pd.isna(s): return ""
    s = unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore').decode('utf-8')
    return s.strip().upper()

df_pop = pd.read_csv("data/observationdata-kwwolwb (2).csv")
# Affichons toutes les lignes entre les régions ou les niveaux préfectoraux
# Les 39 préfectures officielles du Togo (ou 35 préfectures + Golfe / Agoe-Nyive):
# Voyons comment les préfectures apparaissent sous chaque région.
# Par exemple dans Savanes: TONE, CINKASSE, KPENDJAL-OUEST, KPENDJAL, OTI-SUD, OTI, TANDJOARE
# Somme des 7 préfectures des Savanes:
pref_savanes = [388775, 128959, 123330, 88365, 150376, 124848, 138867]
print("Somme préfectures Savanes:", sum(pref_savanes), "vs Savanes:", 1143520)

# Trouvons toutes les lignes qui sont des préfectures
# Dans chaque région, une préfecture est suivie de Pref 1, Pref 2...
# Parcourons les régions
regions_idx = [
    ('SAVANES', 1, 94),
    ('KARA', 94, 200),
    ('CENTRALE', 200, 282),
    ('PLATEAUX', 282, 433),
    ('MARITIME', 433, 521),
    ('DAGL', 521, 759)
]

all_prefs = []
for reg, start, end in regions_idx:
    print(f"\n--- REGION {reg} (total={df_pop.loc[start, 'Value']}) ---")
    sub = df_pop.iloc[start+1:end].reset_index()
    # Cherchons les préfectures dans sub
    # On remarque que chaque préfecture a des communes <PREF> 1, <PREF> 2, etc.
    # Regardons les lignes de sub
    i = 0
    pref_sum = 0
    while i < len(sub):
        row = sub.iloc[i]
        nom = norm(row['découpage-administratif'])
        val = row['Value']
        orig_idx = row['index']
        # Si c'est TOTOAL AVE -> AVE
        if nom == 'TOTOAL AVE':
            nom = 'AVE'
        # Regardons si la ligne suivante contient nom + " 1" ou similiaire
        if i + 1 < len(sub):
            next_nom = norm(sub.iloc[i+1]['découpage-administratif'])
            # Si next_nom commence par nom ou est commune
            # Vérifions
        # Testons si cette ligne est une préfecture
        i += 1

