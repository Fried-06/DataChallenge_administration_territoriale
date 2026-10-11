"""
data_cleaning.py
Nettoyage rigoureux des 8 fichiers CSV sources de la mobilité et sécurité routière au Togo.
Génère les 9 tables propres dans outputs/clean/.
"""

import os
import math
import unicodedata
import pandas as pd
import numpy as np
from shapely import wkt

def norm_str(s):
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    return s.strip().upper()

def haversine_dist(lon1, lat1, lon2, lat2):
    R = 6371.0 # Rayon de la Terre en km
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
    except Exception:
        return 0.0

def run_cleaning(output_dir="outputs/clean"):
    os.makedirs(output_dir, exist_ok=True)
    print("=== Début du nettoyage des données ===")

    # 1. Immatriculations annuelles (akkouh + wklhvw)
    # akkouh: 1990-2022
    df_akk = pd.read_csv("data/observationdata-akkouh.csv")
    type_col = df_akk.columns[1] # types-de-vehicule
    df_akk['type_vehicule'] = df_akk[type_col].replace({
        'Voitues': 'Voitures',
        '2 roues et assimiles': 'Motos et 2 roues',
        '2 roues et assimilées': 'Motos et 2 roues'
    })
    
    # Pivot pour table large
    piv_akk = df_akk.pivot_table(index='Date', columns='type_vehicule', values='Value', aggfunc='first').reset_index()
    piv_akk = piv_akk.sort_values('Date').reset_index(drop=True)
    piv_akk.rename(columns={'Date': 'annee'}, inplace=True)
    
    # Calcul du cumul indicatif depuis 1990 (en signalant l'absence de radiations)
    piv_akk['cumul_immatriculations_depuis_1990'] = piv_akk['Total'].cumsum()
    piv_akk['part_motos_pct'] = (piv_akk['Motos et 2 roues'] / piv_akk['Total']) * 100.0
    piv_akk.to_csv(os.path.join(output_dir, "immatriculations_annuelles.csv"), index=False, encoding="utf-8")
    print("[OK] immatriculations_annuelles.csv cree")

    # 2. Permis annuels (wvtolmb)
    # 2007-2022, 2013 = NaN
    df_perm = pd.read_csv("data/observationdata-wvtolmb.csv")
    cat_col = df_perm.columns[1]
    
    # Remplacement des libellés
    cat_map = {
        'Moto (A)': 'Permis_A_Moto',
        'Voiture lgr (B)': 'Permis_B_Voiture',
        'Voiture légèr (B)': 'Permis_B_Voiture',
        'Poids lourd (C)': 'Permis_C_Poids_Lourd',
        'Transport en commun (D)': 'Permis_D_Transport_Commun',
        'Semi-remorque (E)': 'Permis_E_Semi_Remorque',
        'Voiture spciale (F)': 'Permis_F_Special',
        'Voiture spéciale (F)': 'Permis_F_Special',
        'Total': 'Total_Permis'
    }
    df_perm['categorie'] = df_perm[cat_col].map(lambda x: cat_map.get(x, x))
    
    piv_perm = df_perm.pivot_table(index='Date', columns='categorie', values='Value', aggfunc='first').reset_index()
    piv_perm.rename(columns={'Date': 'annee'}, inplace=True)
    
    # 2013 est une donnée manquante : convertir 0 en NaN
    mask_2013 = (piv_perm['annee'] == 2013)
    for col in piv_perm.columns:
        if col != 'annee':
            piv_perm.loc[mask_2013, col] = np.nan
            
    piv_perm.to_csv(os.path.join(output_dir, "permis_annuels.csv"), index=False, encoding="utf-8")
    print("[OK] permis_annuels.csv cree")

    # 3. Sécurité routière et indicateurs annuels (hxdpzbg)
    df_hxd = pd.read_csv("data/observationdata-hxdpzbg.csv")
    ind_col = df_hxd.columns[0]
    
    # Mapping des indicateurs pour nommage standard
    ind_clean_map = {
        "Nombre de cas d'accidents de la circulation": "accidents_total",
        "Nombre de morts": "morts_total",
        "Nombre de blesss": "blesses_total",
        "Nombre de blessés": "blesses_total",
        "Accidents mortels /100.000 hab": "accidents_pour_100k_hab_brut",
        "Trafic de vhicules de transports de marchandises sur le rseau routier": "trafic_marchandises",
        "Trafic de véhicules de transports de marchandises sur le réseau routier": "trafic_marchandises",
        "Trafic de vhicules de transports de passagers sur le rseau routier": "trafic_passagers",
        "Trafic de véhicules de transports de passagers sur le réseau routier": "trafic_passagers",
        "Evolution du volume de fret routier": "fret_routier_tonnes",
        "Evolution des deux roues et assimiles immatricules": "deux_roues_flux",
        "Evolution des deux roues et assimilées immatriculées": "deux_roues_flux",
        "Nombre de permis de conduire dlivrs aux examens de permis de conduire": "permis_total_hxd",
        "Nombre de permis de conduire délivrés aux examens de permis de conduire": "permis_total_hxd"
    }
    
    df_hxd['ind_clean'] = df_hxd[ind_col].map(ind_clean_map)
    df_hxd_sub = df_hxd.dropna(subset=['ind_clean'])
    piv_hxd = df_hxd_sub.pivot_table(index='Date', columns='ind_clean', values='Value', aggfunc='first').reset_index()
    piv_hxd.rename(columns={'Date': 'annee'}, inplace=True)
    
    # Fusion avec les immatriculations pour ratios
    df_sec = pd.merge(piv_hxd, piv_akk[['annee', 'Total', 'Motos et 2 roues', 'Voitures', 'cumul_immatriculations_depuis_1990']], on='annee', how='left')
    df_sec.rename(columns={'Total': 'immatriculations_total', 'Motos et 2 roues': 'immatriculations_motos', 'Voitures': 'immatriculations_voitures'}, inplace=True)
    
    # Fusion avec permis
    df_sec = pd.merge(df_sec, piv_perm[['annee', 'Total_Permis', 'Permis_A_Moto', 'Permis_B_Voiture']], on='annee', how='left')
    
    # Recalcul de la population implicite de la source et des taux exacts
    df_sec['population_nationale_estimee'] = df_sec['accidents_total'] / (df_sec['accidents_pour_100k_hab_brut'] * 1e-5)
    
    # Taux de mortalité routière pour 100 000 habitants
    df_sec['morts_pour_100k_hab'] = (df_sec['morts_total'] / df_sec['population_nationale_estimee']) * 100000.0
    
    # Taux d'accidents pour 100 000 hab (le renommé de la source)
    df_sec['accidents_pour_100k_hab'] = df_sec['accidents_pour_100k_hab_brut']
    
    # Gravité : morts pour 100 accidents & blessés par accident
    df_sec['morts_pour_100_accidents'] = (df_sec['morts_total'] / df_sec['accidents_total']) * 100.0
    df_sec['blesses_par_accident'] = df_sec['blesses_total'] / df_sec['accidents_total']
    
    # Ratio de mortalité par rapport au cumul de véhicules (morts pour 10 000 véhicules cumulés)
    df_sec['morts_pour_10k_vehicules_cumul'] = (df_sec['morts_total'] / df_sec['cumul_immatriculations_depuis_1990']) * 10000.0
    
    # Ratio permis délivrés / immatriculations de l'année
    df_sec['ratio_permis_sur_immatriculations'] = df_sec['Total_Permis'] / df_sec['immatriculations_total']
    
    df_sec.to_csv(os.path.join(output_dir, "accidents_annuels.csv"), index=False, encoding="utf-8")
    print("[OK] accidents_annuels.csv cree")

    # 4. Population 2022 par région et préfecture (kwwolwb)
    df_pop = pd.read_csv("data/observationdata-kwwolwb (2).csv")
    
    regions_dict = {
        'SAVANES': ['CINKASSE', 'KPENDJAL', 'KPENDJAL-OUEST', 'OTI', 'OTI-SUD', 'TANDJOARE', 'TONE'],
        'KARA': ['ASSOLI', 'BASSAR', 'BINAH', 'DANKPEN', 'DOUFELGOU', 'KERAN', 'KOZAH'],
        'CENTRALE': ['BLITTA', 'MO', 'SOTOUBOUA', 'TCHAMBA', 'TCHAOUDJO'],
        'PLATEAUX': ['AGOU', 'AKEBOU', 'AMOU', 'ANIE', 'DANYI', 'EST-MONO', 'HAHO', 'KLOTO', 'KPELE', 'MOYEN-MONO', 'OGOU', 'WAWA'],
        'MARITIME': ['AVE', 'BAS-MONO', 'LACS', 'VO', 'YOTO', 'ZIO'],
        'DAGL': ['AGOE-NYIVE', 'GOLFE']
    }
    
    pref_rows = []
    ranges = [
        ('SAVANES', 1, 94),
        ('KARA', 94, 200),
        ('CENTRALE', 200, 282),
        ('PLATEAUX', 282, 433),
        ('MARITIME', 433, 521),
        ('DAGL', 521, 759)
    ]
    
    for reg, start, end in ranges:
        sub = df_pop.iloc[start+1:end].reset_index()
        targets = regions_dict[reg]
        for pref in targets:
            matched = False
            for idx_s, row_s in sub.iterrows():
                n = norm_str(row_s['découpage-administratif'])
                if pref == 'AVE' and n == 'TOTOAL AVE':
                    pref_rows.append({
                        'region': 'MARITIME',
                        'prefecture': 'AVE',
                        'population': int(row_s['Value']),
                        'sous_region': reg
                    })
                    matched = True
                    break
                elif n == pref:
                    pref_rows.append({
                        'region': 'MARITIME' if reg in ['MARITIME', 'DAGL'] else reg,
                        'prefecture': pref,
                        'population': int(row_s['Value']),
                        'sous_region': reg
                    })
                    matched = True
                    break
            if not matched:
                raise ValueError(f"Prefecture {pref} non trouvee dans la region {reg}")
                
    df_pref = pd.DataFrame(pref_rows)
    pop_tot = df_pref['population'].sum()
    assert pop_tot == 8095498, f"Erreur population : {pop_tot} != 8095498 attendu"
    df_pref.to_csv(os.path.join(output_dir, "population_region_prefecture.csv"), index=False, encoding="utf-8")
    print(f"[OK] population_region_prefecture.csv cree (Somme = {pop_tot} habitants)")

    # 5. État du réseau routier 2020 (tmdtnad)
    df_tmd = pd.read_csv("data/observationdata-tmdtnad.csv")
    lignes_agregees = ['TOTAL', 'VOIRIES  REVETUES', 'TOTAL RT', 'VOIRIES EN TERRE']
    
    df_troncons = df_tmd[~df_tmd['tronçon'].isin(lignes_agregees)].copy()
    
    piv_troncons = df_troncons.pivot_table(index=['indicateur', 'tronçon'], columns='etat', values='Value', fill_value=0.0).reset_index()
    
    if 'TRAVAUX' not in piv_troncons.columns:
        piv_troncons['TRAVAUX'] = 0.0
    for col in ['BON', 'MOYEN', 'MAUVAIS', 'TRAVAUX', 'TOTAL']:
        if col in piv_troncons.columns:
            piv_troncons[col] = piv_troncons[col].fillna(0.0)
            
    def infer_reg(troncon_nom):
        t = str(troncon_nom).upper()
        if 'TGRP' in t: return 'PLATEAUX'
        elif 'TGRC' in t: return 'CENTRALE'
        elif 'TGRK' in t: return 'KARA'
        elif 'TGRS' in t: return 'SAVANES'
        elif 'TGRM' in t: return 'MARITIME'
        else: return 'MARITIME'
        
    piv_troncons['region'] = piv_troncons['tronçon'].apply(infer_reg)
    
    piv_troncons['pct_mauvais'] = np.where(piv_troncons['TOTAL'] > 0, (piv_troncons['MAUVAIS'] / piv_troncons['TOTAL']) * 100.0, 0.0)
    piv_troncons['pct_bon'] = np.where(piv_troncons['TOTAL'] > 0, (piv_troncons['BON'] / piv_troncons['TOTAL']) * 100.0, 0.0)
    piv_troncons['pct_moyen'] = np.where(piv_troncons['TOTAL'] > 0, (piv_troncons['MOYEN'] / piv_troncons['TOTAL']) * 100.0, 0.0)
    piv_troncons['pct_travaux'] = np.where(piv_troncons['TOTAL'] > 0, (piv_troncons['TRAVAUX'] / piv_troncons['TOTAL']) * 100.0, 0.0)
    
    piv_troncons.to_csv(os.path.join(output_dir, "etat_routes_troncons.csv"), index=False, encoding="utf-8")
    print("[OK] etat_routes_troncons.csv cree")

    # Agrégation par région
    agg_reg = piv_troncons.groupby('region')[['TOTAL', 'BON', 'MOYEN', 'MAUVAIS', 'TRAVAUX']].sum().reset_index()
    agg_reg['pct_bon'] = (agg_reg['BON'] / agg_reg['TOTAL']) * 100.0
    agg_reg['pct_moyen'] = (agg_reg['MOYEN'] / agg_reg['TOTAL']) * 100.0
    agg_reg['pct_mauvais'] = (agg_reg['MAUVAIS'] / agg_reg['TOTAL']) * 100.0
    agg_reg['pct_travaux'] = (agg_reg['TRAVAUX'] / agg_reg['TOTAL']) * 100.0
    agg_reg.to_csv(os.path.join(output_dir, "etat_routes_region.csv"), index=False, encoding="utf-8")
    print("[OK] etat_routes_region.csv cree")

    # 6. Routes classées avec km calculé
    df_routes = pd.read_csv("data/file-routes-routes-classees-18-12-2024-20-38-02.csv")
    df_routes['longueur_km'] = df_routes['geometry'].apply(geom_length_km)
    
    df_routes['region'] = df_routes['region_nom_bdd'].apply(norm_str)
    df_routes['prefecture'] = df_routes['prefecture_nom_bdd'].apply(norm_str)
    
    df_routes_clean = df_routes[['FID', 'region', 'prefecture', 'commune_nom_bdd', 'route_type', 'route_recouvrement', 'route_nom', 'longueur_km', 'geometry']].copy()
    df_routes_clean.to_csv(os.path.join(output_dir, "routes_classees.csv"), index=False, encoding="utf-8")
    tot_km_calc = df_routes_clean['longueur_km'].sum()
    print(f"[OK] routes_classees.csv cree (Longueur totale = {tot_km_calc:.2f} km)")

    # 7. Auto-écoles
    df_ae = pd.read_csv("data/file-entreprises-auto-ecoles-02-01-2025-16-28-05.csv")
    df_ae['region'] = df_ae['region_nom_bdd'].apply(norm_str)
    df_ae['prefecture'] = df_ae['prefecture_nom_bdd'].apply(norm_str)
    
    def clean_agregation(val):
        v = norm_str(val)
        if 'ANTENNE' in v: return 'Antenne agre_e'
        elif 'NON' in v: return 'Non agre_e'
        elif 'AGRE' in v: return 'Agre_e'
        else: return 'Non agre_e'
            
    df_ae['statut_agrement'] = df_ae['agregation'].apply(clean_agregation)
    df_ae['est_agreee'] = df_ae['statut_agrement'].isin(['Agre_e', 'Antenne agre_e'])
    
    df_ae_clean = df_ae[['FID', 'region', 'prefecture', 'commune_nom_bdd', 'nom_etablissement', 'adresse_etablissement', 'statut_agrement', 'est_agreee', 'geometry']].copy()
    df_ae_clean.to_csv(os.path.join(output_dir, "auto_ecoles.csv"), index=False, encoding="utf-8")
    print(f"[OK] auto_ecoles.csv cree ({len(df_ae_clean)} etablissements)")

    # 8. Table maître : region_indicateurs
    pop_by_reg = df_pref.groupby('region')['population'].sum().reset_index()
    
    routes_by_reg = df_routes_clean.groupby('region').agg(
        km_routes_classees_total=('longueur_km', 'sum'),
        km_routes_revetues=('longueur_km', lambda s: df_routes_clean.loc[s.index][df_routes_clean.loc[s.index]['route_type'] == 'Route nationale rev\u00eatue']['longueur_km'].sum() if 'Route nationale rev\u00eatue' in df_routes_clean['route_type'].values else 0.0)
    ).reset_index()
    
    ae_by_reg = df_ae_clean.groupby('region').agg(
        auto_ecoles_total=('FID', 'count'),
        auto_ecoles_agreees=('est_agreee', lambda s: (s == True).sum())
    ).reset_index()
    
    df_master = pd.merge(pop_by_reg, routes_by_reg, on='region', how='left')
    df_master = pd.merge(df_master, agg_reg, on='region', how='left')
    df_master = pd.merge(df_master, ae_by_reg, on='region', how='left')
    
    df_master['km_routes_pour_100k_hab'] = (df_master['km_routes_classees_total'] / df_master['population']) * 100000.0
    df_master['auto_ecoles_pour_100k_hab'] = (df_master['auto_ecoles_total'] / df_master['population']) * 100000.0
    df_master['auto_ecoles_agreees_pour_100k_hab'] = (df_master['auto_ecoles_agreees'] / df_master['population']) * 100000.0
    df_master['habitants_par_auto_ecole'] = df_master['population'] / df_master['auto_ecoles_total']
    df_master['part_auto_ecoles_agreees_pct'] = (df_master['auto_ecoles_agreees'] / df_master['auto_ecoles_total']) * 100.0
    
    def min_max(s):
        diff = s.max() - s.min()
        return (s - s.min()) / diff if diff > 0 else s * 0
        
    norm_mauvais = min_max(df_master['pct_mauvais'])
    norm_km_inv = 1.0 - min_max(df_master['km_routes_pour_100k_hab'])
    norm_ae_inv = 1.0 - min_max(df_master['auto_ecoles_agreees_pour_100k_hab'])
    
    df_master['indice_vulnerabilite_defaut'] = (0.40 * norm_mauvais + 0.30 * norm_km_inv + 0.30 * norm_ae_inv) * 100.0
    
    df_master.to_csv(os.path.join(output_dir, "region_indicateurs.csv"), index=False, encoding="utf-8")
    print("[OK] region_indicateurs.csv cree")
    print("=== Toutes les tables propres generees avec succes ! ===")

if __name__ == "__main__":
    run_cleaning()

