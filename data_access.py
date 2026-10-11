"""
data_access.py
Module centralisé de chargement, de mise en cache et d'assertions de contrôle.
"""

import os
import pandas as pd
import numpy as np

CLEAN_DIR = os.path.join(os.path.dirname(__file__), "outputs", "clean")

# Variables de cache
_DATA_CACHE = {}

def get_immatriculations():
    if "immatriculations" not in _DATA_CACHE:
        df = pd.read_csv(os.path.join(CLEAN_DIR, "immatriculations_annuelles.csv"))
        _DATA_CACHE["immatriculations"] = df
    return _DATA_CACHE["immatriculations"]

def get_permis():
    if "permis" not in _DATA_CACHE:
        df = pd.read_csv(os.path.join(CLEAN_DIR, "permis_annuels.csv"))
        _DATA_CACHE["permis"] = df
    return _DATA_CACHE["permis"]

def get_accidents():
    if "accidents" not in _DATA_CACHE:
        df = pd.read_csv(os.path.join(CLEAN_DIR, "accidents_annuels.csv"))
        _DATA_CACHE["accidents"] = df
    return _DATA_CACHE["accidents"]

def get_population():
    if "population" not in _DATA_CACHE:
        df = pd.read_csv(os.path.join(CLEAN_DIR, "population_region_prefecture.csv"))
        assert df["population"].sum() == 8095498, "Échec assertion population totale = 8 095 498"
        _DATA_CACHE["population"] = df
    return _DATA_CACHE["population"]

def get_etat_routes_troncons():
    if "etat_routes_troncons" not in _DATA_CACHE:
        df = pd.read_csv(os.path.join(CLEAN_DIR, "etat_routes_troncons.csv"))
        _DATA_CACHE["etat_routes_troncons"] = df
    return _DATA_CACHE["etat_routes_troncons"]

def get_etat_routes_region():
    if "etat_routes_region" not in _DATA_CACHE:
        df = pd.read_csv(os.path.join(CLEAN_DIR, "etat_routes_region.csv"))
        _DATA_CACHE["etat_routes_region"] = df
    return _DATA_CACHE["etat_routes_region"]

def get_routes_classees():
    if "routes_classees" not in _DATA_CACHE:
        df = pd.read_csv(os.path.join(CLEAN_DIR, "routes_classees.csv"))
        _DATA_CACHE["routes_classees"] = df
    return _DATA_CACHE["routes_classees"]

def get_auto_ecoles():
    if "auto_ecoles" not in _DATA_CACHE:
        df = pd.read_csv(os.path.join(CLEAN_DIR, "auto_ecoles.csv"))
        _DATA_CACHE["auto_ecoles"] = df
    return _DATA_CACHE["auto_ecoles"]

def get_region_indicateurs():
    if "region_indicateurs" not in _DATA_CACHE:
        df = pd.read_csv(os.path.join(CLEAN_DIR, "region_indicateurs.csv"))
        _DATA_CACHE["region_indicateurs"] = df
    return _DATA_CACHE["region_indicateurs"]

def verify_all_assertions():
    """Valide au démarrage l'intégrité de toutes les données."""
    pop = get_population()
    assert pop["population"].sum() == 8095498, "Population totale invalide !"
    
    tmd = get_etat_routes_troncons()
    diff = (tmd["BON"] + tmd["MOYEN"] + tmd["MAUVAIS"] + tmd["TRAVAUX"]) - tmd["TOTAL"]
    assert diff.abs().max() < 0.05, "Incohérence sur la somme des tronçons !"
    
    routes = get_routes_classees()
    assert abs(routes["longueur_km"].sum() - 3373.0) < 5.0, "Longueur totale des routes classées hors tolérance !"
    print("[Data Access] Assertions d'intégrité validées avec succès.")

if __name__ == "__main__":
    verify_all_assertions()
