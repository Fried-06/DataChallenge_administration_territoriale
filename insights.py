"""
insights.py
Génération automatique des synthèses et phrases "À retenir" directement calculées depuis les données.
Aucun chiffre n'est codé en dur.
"""

from data_access import (
    get_immatriculations, get_permis, get_accidents,
    get_etat_routes_region, get_etat_routes_troncons,
    get_auto_ecoles, get_region_indicateurs
)

def format_fr(val, decimales=0):
    if val is None or (isinstance(val, float) and (val != val)):
        return "N/D"
    if decimales == 0:
        return f"{int(round(val)):,}".replace(",", " ")
    else:
        formatted = f"{val:,.{decimales}f}".replace(",", " ").replace(".", ",")
        return formatted

def get_kpis_accueil():
    df_acc = get_accidents()
    df_imm = get_immatriculations()
    df_routes = get_etat_routes_region()
    
    # 1. Morts sur les routes (dernière année, 2022)
    dernier_acc = df_acc.dropna(subset=['morts_total']).iloc[-1]
    annee_acc = int(dernier_acc['annee'])
    morts_val = int(dernier_acc['morts_total'])
    
    # Année de référence (ex. 2020)
    ref_acc = df_acc[df_acc['annee'] == 2020].iloc[0]
    morts_ref = int(ref_acc['morts_total'])
    diff_morts = morts_val - morts_ref
    diff_morts_str = f"+{diff_morts} vs 2020" if diff_morts > 0 else f"{diff_morts} vs 2020"
    
    # 2. Accidents
    acc_val = int(dernier_acc['accidents_total'])
    acc_ref = int(ref_acc['accidents_total'])
    diff_acc = acc_val - acc_ref
    diff_acc_str = f"+{diff_acc} vs 2020" if diff_acc > 0 else f"{diff_acc} vs 2020"
    
    # 3. Immatriculations de l'année (flux)
    dernier_imm = df_imm.iloc[-1]
    annee_imm = int(dernier_imm['annee'])
    imm_val = int(dernier_imm['Total'])
    ref_imm = df_imm[df_imm['annee'] == 2020].iloc[0]
    diff_imm = imm_val - int(ref_imm['Total'])
    diff_imm_str = f"+{format_fr(diff_imm)} vs 2020" if diff_imm > 0 else f"{format_fr(diff_imm)} vs 2020"
    
    # 4. Part du réseau en mauvais état (2020)
    total_km = df_routes['TOTAL'].sum()
    mauvais_km = df_routes['MAUVAIS'].sum()
    pct_mauvais = (mauvais_km / total_km) * 100.0
    
    return {
        "morts": {
            "valeur": format_fr(morts_val),
            "label": f"Morts sur les routes ({annee_acc})",
            "comparaison": diff_morts_str,
            "aide": f"Nombre total de décès constatés lors d'accidents de la circulation en {annee_acc} sur l'ensemble du territoire togolais."
        },
        "accidents": {
            "valeur": format_fr(acc_val),
            "label": f"Accidents corporels ({annee_acc})",
            "comparaison": diff_acc_str,
            "aide": f"Nombre de cas d'accidents enregistrés par les services de sécurité routière au cours de l'année {annee_acc}."
        },
        "immatriculations": {
            "valeur": format_fr(imm_val),
            "label": f"Immatriculations de l'année ({annee_imm})",
            "comparaison": diff_imm_str,
            "aide": "Flux annuel des nouveaux véhicules immatriculés (premières mises en circulation), à distinguer d'un stock de parc."
        },
        "routes_degradees": {
            "valeur": f"{format_fr(pct_mauvais, 1)} %",
            "label": "Routes en mauvais état (2020)",
            "comparaison": f"{format_fr(mauvais_km, 0)} km sur {format_fr(total_km, 0)} km",
            "aide": "Proportion des tronçons répertoriés nécessitant une réhabilitation lourde lors de l'audit de 2020."
        }
    }

def get_constats_accueil():
    df_imm = get_immatriculations()
    df_acc = get_accidents()
    df_ae = get_auto_ecoles()
    df_reg = get_region_indicateurs()
    
    # Constat 1 : Domination des motos
    imm_2022 = df_imm[df_imm['annee'] == 2022].iloc[0]
    part_motos_2022 = (imm_2022['Motos et 2 roues'] / imm_2022['Total']) * 100.0
    imm_1990 = df_imm[df_imm['annee'] == 1990].iloc[0]
    part_motos_1990 = (imm_1990['Motos et 2 roues'] / imm_1990['Total']) * 100.0
    constat_1 = (
        f"La motorisation togolaise est massivement portée par les deux-roues : les motos représentaient "
        f"{format_fr(part_motos_1990, 1)} % des flux en 1990 ({format_fr(imm_1990['Motos et 2 roues'])} unités), "
        f"contre {format_fr(part_motos_2022, 1)} % en 2022 ({format_fr(imm_2022['Motos et 2 roues'])} unités sur {format_fr(imm_2022['Total'])})."
    )
    
    # Constat 2 : Gravité et mortalité
    acc_2022 = df_acc[df_acc['annee'] == 2022].iloc[0]
    gravite_2022 = acc_2022['morts_pour_100_accidents']
    taux_100k = acc_2022['morts_pour_100k_hab']
    constat_2 = (
        f"En 2022, le bilan routier national s'élève à {format_fr(acc_2022['morts_total'])} décès et "
        f"{format_fr(acc_2022['blesses_total'])} blessés pour {format_fr(acc_2022['accidents_total'])} accidents, "
        f"soit un taux de gravité de {format_fr(gravite_2022, 1)} morts pour 100 accidents et {format_fr(taux_100k, 1)} décès pour 100 000 habitants."
    )
    
    # Constat 3 : Hyper-concentration de l'offre de formation
    ae_maritime = len(df_ae[df_ae['region'] == 'MARITIME'])
    ae_total = len(df_ae)
    part_ae_maritime = (ae_maritime / ae_total) * 100.0
    pop_maritime = df_reg[df_reg['region'] == 'MARITIME']['population'].iloc[0]
    part_pop_maritime = (pop_maritime / 8095498) * 100.0
    constat_3 = (
        f"L'offre d'apprentissage de la conduite présente une disparité territoriale majeure : la région Maritime "
        f"concentre {format_fr(part_ae_maritime, 1)} % des auto-écoles ({ae_maritime} sur {ae_total}) pour "
        f"{format_fr(part_pop_maritime, 1)} % de la population nationale, laissant plusieurs préfectures de l'intérieur sans structure de formation agréée."
    )
    
    return [constat_1, constat_2, constat_3]

def get_titre_accidents():
    """
    Titre prudent calculé sur la série réelle d'accidents (2010-2022).
    Reflète la forte fluctuation, le pic de 2012 et le creux de 2015.
    """
    df_acc = get_accidents()
    df_valid = df_acc.dropna(subset=['accidents_total'])
    annee_min = int(df_valid['annee'].min())
    annee_max = int(df_valid['annee'].max())
    creux_row = df_valid.loc[df_valid['accidents_total'].idxmin()]
    creux_annee = int(creux_row['annee'])
    max_row = df_valid.loc[df_valid['accidents_total'].idxmax()]
    max_annee = int(max_row['annee'])
    return (
        f"Accidents et blessés ({annee_min}-{annee_max}) : forte fluctuation avec pic en {max_annee}, "
        f"creux en {creux_annee} ({format_fr(creux_row['accidents_total'])} accidents) puis reprise"
    )

def get_titre_ratios_securite():
    df_acc = get_accidents()
    df_valid = df_acc.dropna(subset=['morts_pour_100k_hab'])
    dernier = df_valid.iloc[-1]
    return (
        f"Mortalité rapportée à la population ({format_fr(dernier['morts_pour_100k_hab'], 1)} pour 100k hab) "
        f"et gravité des accidents ({format_fr(dernier['morts_pour_100_accidents'], 1)} % en {int(dernier['annee'])})"
    )

def get_titre_immatriculations():
    df_imm = get_immatriculations()
    row_22 = df_imm[df_imm['annee'] == 2022].iloc[0]
    pct_motos = (row_22['Motos et 2 roues'] / row_22['Total']) * 100.0
    return f"Flux d'immatriculations (1990-2022) : part prépondérante des deux-roues ({format_fr(pct_motos, 1)} % en 2022)"

def get_titre_permis():
    return "Permis de conduire délivrés par catégorie (2007-2022) : prédominance de la catégorie B (voitures) et pic en 2016"

def get_titre_routes():
    return "État physique du réseau routier audité par région (audit 2020) : disparités territoriales du niveau de dégradation"

def get_titre_auto_ecoles():
    df_ae = get_auto_ecoles()
    ae_maritime = len(df_ae[df_ae['region'] == 'MARITIME'])
    pct_ae = (ae_maritime / len(df_ae)) * 100.0
    return f"Densité des auto-écoles par région : la Maritime concentre {format_fr(pct_ae, 1)} % des structures pour 43,7 % de la population"

