import pandas as pd
import numpy as np
import re

df_tmd = pd.read_csv("data/observationdata-tmdtnad.csv")

# Troncons uniques (hors TOTAL, TOTAL RT, VOIRIES REVETUES, VOIRIES EN TERRE)
# Regardons toutes les valeurs de la colonne 'tronçon'
troncons = df_tmd['tronçon'].unique()
print(f"Nombre de valeurs uniques dans 'tronçon': {len(troncons)}")

lignes_agregees = [t for t in troncons if any(k in str(t).upper() for k in ['TOTAL', 'VOIRIE'])]
print("Lignes agrégées détectées:", lignes_agregees)

vrais_troncons = [t for t in troncons if t not in lignes_agregees]
print(f"Nombre de vrais tronçons: {len(vrais_troncons)}")

def infer_region(troncon_nom):
    t = str(troncon_nom).upper()
    if 'TGRP' in t:
        return 'PLATEAUX'
    elif 'TGRC' in t:
        return 'CENTRALE'
    elif 'TGRK' in t:
        return 'KARA'
    elif 'TGRS' in t:
        return 'SAVANES'
    elif 'TGRM' in t:
        return 'MARITIME'
    else:
        return 'MARITIME/LOME' # Provisoire pour RN1 Amakpape... ou Lomé

repartition = {}
for t in vrais_troncons:
    reg = infer_region(t)
    repartition[reg] = repartition.get(reg, 0) + 1
print("Répartition des tronçons par région:", repartition)

# Regardons ceux classés en MARITIME/LOME
print("Tronçons classés en MARITIME/LOME:")
for t in vrais_troncons:
    if infer_region(t) == 'MARITIME/LOME':
        print(f"  - {t}")
