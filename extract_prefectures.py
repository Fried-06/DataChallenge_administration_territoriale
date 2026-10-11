import pandas as pd
import unicodedata
import re

def norm(s):
    if pd.isna(s): return ""
    s = unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore').decode('utf-8')
    return s.strip().upper()

df_pop = pd.read_csv("data/observationdata-kwwolwb (2).csv")

# Liste officielle des préfectures du Togo par région:
# Savanes (7): CINKASSE, KPENDJAL, KPENDJAL-OUEST, OTI, OTI-SUD, TANDJOARE, TONE
# Kara (7): ASSOLI, BASSAR, BINAH, DANKPEN, DOUFELGOU, KERAN, KOZAH
# Centrale (5): BLITTA, MO (PLAINE DU MO), SOTOUBOUA, TCHAMBA, TCHAOUDJO
# Plateaux (12): AGOU, AKEBOU, AMOU, ANIE, DANYI, EST-MONO, HAHO, KLOTO, KPELE, MOYEN-MONO, OGOU, WAWA
# Maritime hors DAGL (6): AVE, BAS-MONO, LACS, VO, YOTO, ZIO
# DAGL (2): AGOE-NYIVE, GOLFE
# Total = 7 + 7 + 5 + 12 + 6 + 2 = 39 entités préfectorales

regions_dict = {
    'SAVANES': ['CINKASSE', 'KPENDJAL', 'KPENDJAL-OUEST', 'OTI', 'OTI-SUD', 'TANDJOARE', 'TONE'],
    'KARA': ['ASSOLI', 'BASSAR', 'BINAH', 'DANKPEN', 'DOUFELGOU', 'KERAN', 'KOZAH'],
    'CENTRALE': ['BLITTA', 'MO', 'SOTOUBOUA', 'TCHAMBA', 'TCHAOUDJO'],
    'PLATEAUX': ['AGOU', 'AKEBOU', 'AMOU', 'ANIE', 'DANYI', 'EST-MONO', 'HAHO', 'KLOTO', 'KPELE', 'MOYEN-MONO', 'OGOU', 'WAWA'],
    'MARITIME': ['AVE', 'BAS-MONO', 'LACS', 'VO', 'YOTO', 'ZIO'],
    'DAGL': ['AGOE-NYIVE', 'GOLFE']
}

# Cherchons chacune dans df_pop
records = []
for reg, prefs in regions_dict.items():
    print(f"\nRecherche pour région {reg}:")
    for pref in prefs:
        # Cherchons les correspondances dans df_pop
        found = []
        for idx, row in df_pop.iterrows():
            n = norm(row['découpage-administratif'])
            val = row['Value']
            if n == pref or (pref == 'AVE' and n == 'TOTOAL AVE') or (pref == 'MO' and ('PLAINE DU MO' in n or n == 'MO')):
                found.append((idx, row['découpage-administratif'], val))
        print(f"  {pref}: {found}")
        if found:
            # On prend la ligne correspondante (si plusieurs, celle qui correspond au total de la préfecture)
            records.append({'region': reg, 'prefecture': pref, 'nom_original': found[0][1], 'population': found[0][2], 'idx': found[0][0]})

df_extracted = pd.DataFrame(records)
print("\nTotal préfectures extraites:", len(df_extracted))
for reg, group in df_extracted.groupby('region'):
    print(f"Somme extraite pour {reg}: {group['population'].sum()} (vs pop région)")
print("Somme totale extraite:", df_extracted['population'].sum())
