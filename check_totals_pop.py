import pandas as pd
import unicodedata

def norm(s):
    if pd.isna(s): return ""
    s = unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore').decode('utf-8')
    return s.strip().upper()

df_pop = pd.read_csv("data/observationdata-kwwolwb (2).csv")
# Regardons toutes les préfectures de chaque région
# Une préfecture a ses communes x 1, x 2...
# Parcourons les lignes et repérons le découpage
for idx in range(len(df_pop)):
    val = df_pop.loc[idx, 'découpage-administratif']
    pop = df_pop.loc[idx, 'Value']
    n = norm(val)
    if 'TOTAL' in n or 'TOTOAL' in n:
        print(f"Row {idx}: {val} -> {pop}")
