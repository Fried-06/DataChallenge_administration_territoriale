import pandas as pd
import numpy as np
import unicodedata
import re

def norm(s):
    if pd.isna(s): return ""
    s = unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore').decode('utf-8')
    return s.strip().upper()

# 1. akkouh
print("=== 1. AKKOUH ===")
df_akk = pd.read_csv("data/observationdata-akkouh.csv")
col_type = df_akk.columns[1]
print("Types de vehicules distincts:", df_akk[col_type].unique())
piv_akk = df_akk.pivot_table(index='Date', columns=col_type, values='Value')
print("Extrait pivot akkouh (1990, 2002, 2015, 2016, 2022):")
print(piv_akk.loc[[1990, 2002, 2015, 2016, 2022]])

# 2. wvtolmb (permis)
print("\n=== 2. WVTOLMB ===")
df_perm = pd.read_csv("data/observationdata-wvtolmb.csv")
col_cat = df_perm.columns[1]
print("Categories:", df_perm[col_cat].unique())
piv_perm = df_perm.pivot_table(index='Date', columns=col_cat, values='Value')
print(piv_perm)

# 3. hxdpzbg (indicateurs)
print("\n=== 3. HXDPZBG ===")
df_hxd = pd.read_csv("data/observationdata-hxdpzbg.csv")
ind_col = df_hxd.columns[0]
for ind in df_hxd[ind_col].unique():
    sub = df_hxd[df_hxd[ind_col] == ind].sort_values('Date')
    print(f"Indicateur: {ind} | Annees: {sub['Date'].min()}-{sub['Date'].max()} | Dernieres val: {sub[['Date', 'Value']].tail(3).to_dict('records')}")

# 4. tmdtnad (etat routes)
print("\n=== 4. TMDTNAD ===")
df_tmd = pd.read_csv("data/observationdata-tmdtnad.csv")
print("Indicateurs dans tmdtnad:", df_tmd['indicateur'].unique())
print("Etats dans tmdtnad:", df_tmd['etat'].unique())
print("Troncons contenant TOTAL ou VOIRIE:")
print(df_tmd[df_tmd['tronçon'].astype(str).str.contains("TOTAL|VOIRIE|RT", case=False, na=False)][['indicateur', 'tronçon', 'etat', 'Value']])

# 5. kwwolwb (population)
print("\n=== 5. KWWOLWB ===")
df_pop = pd.read_csv("data/observationdata-kwwolwb (2).csv")
print("Sexe unique:", df_pop['sexe'].unique())
# Filtre sur Total ou ensemble ?
print(df_pop.head(25)[['découpage-administratif', 'sexe', 'Value']])

# 6. file-routes
print("\n=== 6. ROUTES CLASSEES ===")
df_routes = pd.read_csv("data/file-routes-routes-classees-18-12-2024-20-38-02.csv")
print("Route types:", df_routes['route_type'].value_counts(dropna=False))
print("Route recouvrement:", df_routes['route_recouvrement'].value_counts(dropna=False))
print("Route classee:", df_routes['route_classee'].value_counts(dropna=False))

# 7. auto-ecoles
print("\n=== 7. AUTO-ECOLES ===")
df_ae = pd.read_csv("data/file-entreprises-auto-ecoles-02-01-2025-16-28-05.csv")
print("Regions auto-ecoles:", df_ae['region_nom_bdd'].value_counts(dropna=False))
print("Prefectures Maritime auto-ecoles:", df_ae[df_ae['region_nom_bdd'].astype(str).str.contains("Maritime", case=False)]['prefecture_nom_bdd'].value_counts())
