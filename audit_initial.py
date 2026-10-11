import os
import glob
import unicodedata
import pandas as pd
import numpy as np

def norm_str(s):
    if pd.isna(s):
        return ""
    s = str(s)
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    return s.strip().upper()

print("="*60)
print("AUDIT COMPLET DES 8 FICHIERS CSV")
print("="*60)

# 1. observationdata-akkouh.csv
print("\n--- 1. akkouh (immatriculations 1990-2022) ---")
df_akk = pd.read_csv("data/observationdata-akkouh.csv")
print("Colonnes:", df_akk.columns.tolist())
print("Indicateurs / dimensions uniques:")
for col in df_akk.columns:
    if col not in ['Value', 'Date', 'Unit']:
        print(f"  {col}: {df_akk[col].unique()}")
print("Dates min/max:", df_akk['Date'].min(), df_akk['Date'].max(), "Nb lignes:", len(df_akk))
print("Aperçu valeurs pour Total:")
tot = df_akk[df_akk.iloc[:, 0].astype(str).str.contains("Total", case=False, na=False)]
print(tot.tail(5))

# 2. observationdata-wklhvw.csv
print("\n--- 2. wklhvw (détail 2013-2019) ---")
df_wkl = pd.read_csv("data/observationdata-wklhvw.csv")
print("Colonnes:", df_wkl.columns.tolist())
for col in df_wkl.columns:
    if col not in ['Value', 'Date', 'Unit']:
        print(f"  {col}: {df_wkl[col].unique()}")
print("Dates min/max:", df_wkl['Date'].min(), df_wkl['Date'].max(), "Nb lignes:", len(df_wkl))

# 3. observationdata-wvtolmb.csv
print("\n--- 3. wvtolmb (permis par catégorie 2007-2022) ---")
df_perm = pd.read_csv("data/observationdata-wvtolmb.csv")
print("Colonnes:", df_perm.columns.tolist())
for col in df_perm.columns:
    if col not in ['Value', 'Date', 'Unit']:
        print(f"  {col}: {df_perm[col].unique()}")
print("Dates min/max:", df_perm['Date'].min(), df_perm['Date'].max())
print("Vérification 2013:")
print(df_perm[df_perm['Date'] == 2013])
print("Permis par catégorie en 2016, 2019, 2022:")
print(df_perm[df_perm['Date'].isin([2016, 2019, 2022])].pivot_table(index='Date', columns=df_perm.columns[0], values='Value'))

# 4. observationdata-hxdpzbg.csv
print("\n--- 4. hxdpzbg (13 indicateurs) ---")
df_hxd = pd.read_csv("data/observationdata-hxdpzbg.csv")
print("Colonnes:", df_hxd.columns.tolist())
ind_col = df_hxd.columns[0]
print("Indicateurs uniques:")
for ind in df_hxd[ind_col].unique():
    sub = df_hxd[df_hxd[ind_col] == ind]
    print(f"  '{ind}': {sub['Date'].min()}-{sub['Date'].max()} (n={len(sub)}, non-null={sub['Value'].count()})")

# 5. observationdata-tmdtnad.csv
print("\n--- 5. tmdtnad (état des routes 2020) ---")
df_tmd = pd.read_csv("data/observationdata-tmdtnad.csv")
print("Colonnes:", df_tmd.columns.tolist())
print("Nb lignes:", len(df_tmd))
print("Premières lignes:")
print(df_tmd.head(10))

# 6. observationdata-kwwolwb (2).csv
print("\n--- 6. kwwolwb (population 2022) ---")
df_pop = pd.read_csv("data/observationdata-kwwolwb (2).csv")
print("Colonnes:", df_pop.columns.tolist())
print("Nb lignes:", len(df_pop))
print("Aperçu:")
print(df_pop.head(15))

# 7. file-routes-routes-classees-18-12-2024-20-38-02.csv
print("\n--- 7. routes classées ---")
df_routes = pd.read_csv("data/file-routes-routes-classees-18-12-2024-20-38-02.csv")
print("Colonnes:", df_routes.columns.tolist())
print("Nb lignes:", len(df_routes))
print(df_routes.head(2))

# 8. file-entreprises-auto-ecoles-02-01-2025-16-28-05.csv
print("\n--- 8. auto-écoles ---")
df_ae = pd.read_csv("data/file-entreprises-auto-ecoles-02-01-2025-16-28-05.csv")
print("Colonnes:", df_ae.columns.tolist())
print("Nb lignes:", len(df_ae))
print("Valeurs aggregation:")
print(df_ae['agregation'].value_counts(dropna=False))
print(df_ae.head(2))
