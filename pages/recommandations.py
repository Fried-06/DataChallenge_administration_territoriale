"""
pages/recommandations.py
Page Recommandations : 8 fiches d'actions ciblées, filtrables par domaine et région,
adossées à des chiffres exacts avec distinction stricte entre constats empiriques et hypothèses opérationnelles.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/recommandations", name="Recommandations")

RECOMMANDATIONS = [
    {
        "id": 1,
        "titre": "Généraliser la formation et le permis A obligatoire pour les deux-roues",
        "domaine": "Sécurité Routière",
        "region": "National",
        "chiffre": "67 639 motos immatriculées en 2022 (72,1 % du flux) pour seulement 4 837 permis moto A délivrés",
        "priorite": "Haute",
        "indicateur_suivi": "Taux de couverture permis A / immatriculations de deux-roues",
        "constat": "Le flux de deux-roues progresse de façon exponentielle tandis que la grande majorité des usagers circule sans permis moto A dédié.",
        "hypothese": "La généralisation des modules de formation moto et du port du casque homologué réduira significativement la gravité des traumatismes."
    },
    {
        "id": 2,
        "titre": "Plan d'urgence de réhabilitation des axes dégradés dans la région des Plateaux",
        "domaine": "Entretien du Réseau",
        "region": "Plateaux",
        "chiffre": "33,2 % du réseau revêtu audité en mauvais état lors du diagnostic 2020",
        "priorite": "Haute",
        "indicateur_suivi": "Kilomètres de voirie réhabilités et passés de l'état mauvais à bon",
        "constat": "La région des Plateaux concentre la proportion la plus critique de routes dégradées parmi l'ensemble des territoires audités.",
        "hypothese": "La remise à niveau prioritaire des tronçons critiques limitera les pertes de contrôle et favorisera l'écoulement des flux agricoles."
    },
    {
        "id": 3,
        "titre": "Déploiement d'antennes d'auto-écoles agréées dans les Savanes et la Centrale",
        "domaine": "Formation des Conducteurs",
        "region": "Savanes",
        "chiffre": "Seulement 10 auto-écoles pour 1,14 million d'habitants (0,87 structure pour 100 000 hab)",
        "priorite": "Haute",
        "indicateur_suivi": "Nombre de préfectures dotées d'au moins un centre d'examen agréé",
        "constat": "Un déséquilibre géographique extrême existe : 82,4 % des auto-écoles sont regroupées dans la seule région Maritime.",
        "hypothese": "Inciter les réseaux agréés à ouvrir des antennes en région par allègement fiscal améliorera le taux de réussite aux examens officiels."
    },
    {
        "id": 4,
        "titre": "Mise en place d'un registre territorialisé des accidents et des contrôles",
        "domaine": "Sécurité Routière",
        "region": "National",
        "chiffre": "0 ventilation régionale des accidents dans les statistiques nationales actuelles",
        "priorite": "Moyenne",
        "indicateur_suivi": "Taux de complétude du fichier numérique géolocalisé des constats d'accidents",
        "constat": "Les données de sinistralité sont agrégées au niveau national, empêchant l'identification fine des carrefours et tronçons accidentogènes.",
        "hypothese": "La géolocalisation des procès-verbaux d'accidents permettra d'orienter les patrouilles de gendarmerie sur les zones à fort risque."
    },
    {
        "id": 5,
        "titre": "Accélération et sécurisation des chantiers routiers dans les Savanes",
        "domaine": "Entretien du Réseau",
        "region": "Savanes",
        "chiffre": "28,5 % du réseau audité classé 'En travaux' en 2020",
        "priorite": "Moyenne",
        "indicateur_suivi": "Délai moyen de livraison des chantiers et signalisation temporaire conforme",
        "constat": "La région des Savanes affiche la part la plus élevée de voiries sous statut de chantier actif.",
        "hypothese": "Un renforcement des exigences de signalisation temporaire nocturne préviendra les collisions sur les zones de travaux."
    },
    {
        "id": 6,
        "titre": "Programme de mise en conformité et d'agrément des auto-écoles",
        "domaine": "Formation des Conducteurs",
        "region": "Maritime",
        "chiffre": "50,7 % des auto-écoles recensées sont non agréées (138 sur 272)",
        "priorite": "Haute",
        "indicateur_suivi": "Proportion des structures d'apprentissage régularisées avec label ministériel",
        "constat": "Plus de la moitié des établissements d'enseignement de la conduite fonctionnent actuellement sans statut agréé formel.",
        "hypothese": "Un audit systématique assorti d'une période de régularisation rehaussera la qualité pédagogique de l'apprentissage."
    },
    {
        "id": 7,
        "titre": "Aménagement des traversées urbaines sur la RN1 (Axe corridor Nord-Sud)",
        "domaine": "Sécurité Routière",
        "region": "Centrale",
        "chiffre": "2,19 millions de passages de poids lourds enregistrés sur le réseau national en 2022",
        "priorite": "Moyenne",
        "indicateur_suivi": "Nombre de passerelles piétonnes et ralentisseurs normalisés installés",
        "constat": "L'intensification du fret de transit accroît la cohabitation dangereuse entre trafic lourd international et usagers vulnérables locaux.",
        "hypothese": "Séparer physiquement les flux de passage et les modes doux dans les traversées d'agglomération diminuera la mortalité piétonne."
    },
    {
        "id": 8,
        "titre": "Institution d'un observatoire annuel du parc roulant et des radiations",
        "domaine": "Administration Territoriale",
        "region": "National",
        "chiffre": "93 770 immatriculations annuelles enregistrées en 2022 sans comptabilisation des radiations",
        "priorite": "Moyenne",
        "indicateur_suivi": "Publication annuelle d'un bilan officiel distinguant flux et stock de véhicules",
        "constat": "L'absence de suivi des sorties de parc empêche le calcul rigoureux de ratios d'exposition aux risques par véhicule en circulation.",
        "hypothese": "Mettre en place une procédure de radiation lors du contrôle technique ou du recyclage fiabilisera le pilotage des politiques publiques."
    }
]

def layout():
    cards = []
    for r in RECOMMANDATIONS:
        color_badge = "red" if r["priorite"] == "Haute" else "blue"
        cards.append(
            html.Div(
                className="card-standard mb-6",
                children=[
                    html.Div(
                        className="flex flex-wrap items-center justify-between gap-2 mb-3",
                        children=[
                            html.Span(
                                f"Fiche action #{r['id']} • {r['domaine']} ({r['region']})",
                                className="text-xs font-semibold uppercase tracking-wider",
                                style={"color": "var(--color-brand-deep)"}
                            ),
                            dmc.Badge(r["priorite"], color=color_badge, variant="light", size="sm")
                        ]
                    ),
                    html.H3(r["titre"], className="text-base font-bold mb-3", style={"color": "var(--color-ink)"}),
                    
                    # Preuve chiffrée
                    html.Div(
                        className="p-3 rounded-lg mb-4 text-xs font-medium flex items-start gap-2",
                        style={"backgroundColor": "rgba(16, 110, 152, 0.08)", "border": "1px solid rgba(16, 110, 152, 0.2)"},
                        children=[
                            DashIconify(icon="lucide:bar-chart-2", width=18, className="mt-0.5 flex-shrink-0", style={"color": "var(--color-brand-teal)"}),
                            html.Span([
                                html.Strong("Preuve empirique issue des données : ", style={"color": "var(--color-brand-teal)"}),
                                html.Span(r["chiffre"])
                            ])
                        ]
                    ),
                    
                    # Constat vs Hypothèse
                    html.Div(
                        className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs mb-3",
                        children=[
                            html.Div([
                                html.Strong("Constat observé dans les données : ", className="block mb-1", style={"color": "var(--color-ink)"}),
                                html.Span(r["constat"], style={"color": "var(--color-ink-soft)"})
                            ]),
                            html.Div([
                                html.Strong("Hypothèse d'impact opérationnelle : ", className="block mb-1", style={"color": "var(--color-note-edge)"}),
                                html.Span(r["hypothese"], style={"color": "var(--color-ink-soft)"})
                            ])
                        ]
                    ),
                    
                    html.Div(
                        className="pt-2 border-t text-xs flex items-center justify-between",
                        style={"borderColor": "var(--color-line)", "color": "var(--color-ink-muted)"},
                        children=[
                            html.Span(f"Indicateur de suivi proposé : {r['indicateur_suivi']}")
                        ]
                    )
                ]
            )
        )
        
    return html.Div(
        className="max-w-7xl mx-auto px-4 py-8",
        children=[
            html.Div(
                className="mb-8",
                children=[
                    html.H2("Recommandations d'action pour l'administration territoriale", className="text-2xl font-bold mb-2", style={"color": "var(--color-ink)"}),
                    html.P(
                        "8 fiches d'orientations publiques fondées sur les résultats empiriques, sans estimation de coûts non sourcée.",
                        className="text-sm",
                        style={"color": "var(--color-ink-soft)"}
                    )
                ]
            ),
            html.Div(children=cards)
        ]
    )
