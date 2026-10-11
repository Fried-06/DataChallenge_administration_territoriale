import pandas as pd
import unicodedata

def norm(s):
    if pd.isna(s): return ""
    s = unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore').decode('utf-8')
    return s.strip().upper()

df_pop = pd.read_csv("data/observationdata-kwwolwb (2).csv")
# Chercher où se trouve Ave ou Avé ou préfectures maritimes
for idx, row in df_pop.iterrows():
    val = row['découpage-administratif']
    n = norm(val)
    if 'AVE' in n or 'KEVE' in n or 'ASSAHOUN' in n:
        print(f"Row {idx}: {val} (norm={n}) = {row['Value']}")

# Listons toutes les préfectures de chaque région dans kwwolwb
