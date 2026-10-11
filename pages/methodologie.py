"""
pages/methodologie.py
Page Méthodologie : Sources, années, définitions, limites et corrections des anomalies (reprend QUALITE.md).
"""

import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(__name__, path="/methodologie", name="Méthodologie")

def layout():
    return html.Div(
        className="max-w-7xl mx-auto px-4 py-8",
        children=[
            html.Div(
                className="mb-8",
                children=[
                    html.H2("Méthodologie, Sources & Rigueur des Données", className="text-2xl font-bold mb-2", style={"color": "var(--color-ink)"}),
                    html.P(
                        "Documentation complète du processus de traitement, des limites scientifiques et des corrections appliquées aux données du Togo AI Labs.",
                        className="text-sm",
                        style={"color": "var(--color-ink-soft)"}
                    )
                ]
            ),
            
            # Section 1 : Sources et millésimes
            html.Div(
                className="card-standard mb-6",
                children=[
                    html.H3("1. Inventaire des sources et millésimes des données", className="text-base font-semibold mb-3", style={"color": "var(--color-ink)"}),
                    html.P(
                        "Les analyses reposent sur 8 fichiers administratifs ouverts mis à disposition pour le concours. "
                        "Les séries présentent des décalages temporels à prendre impérativement en compte lors des interprétations :",
                        className="text-xs leading-relaxed mb-3",
                        style={"color": "var(--color-ink-soft)"}
                    ),
                    html.Ul(
                        className="text-xs leading-relaxed space-y-1 list-disc pl-5",
                        style={"color": "var(--color-ink-soft)"},
                        children=[
                            html.Li("Flux d'immatriculations : 1990 à 2022 (série annuelle nationale complète)."),
                            html.Li("Examens de permis de conduire : 2007 à 2022 (données 2013 manquantes dans la source)."),
                            html.Li("Accidentologie et sécurité routière : 2010 à 2022 (agrégats nationaux uniquement)."),
                            html.Li("Trafic routier marchandises et passagers : 2014 à 2022."),
                            html.Li("État physique du réseau routier : audit de l'année 2020 uniquement (DGTP)."),
                            html.Li("Recensement de la population : RGPH-5 de l'INSEED, année 2022 (8 095 498 habitants)."),
                            html.Li("Réseau routier classé et auto-écoles : bases géographiques 2024-2025.")
                        ]
                    )
                ]
            ),
            
            # Section 2 : Traitement des pièges
            html.Div(
                className="card-standard mb-6",
                children=[
                    html.H3("2. Traitement explicite des anomalies identifiées", className="text-base font-semibold mb-3", style={"color": "var(--color-ink)"}),
                    html.Div(
                        className="space-y-4 text-xs leading-relaxed",
                        style={"color": "var(--color-ink-soft)"},
                        children=[
                            html.Div([
                                html.Strong("• Rectification de l'indicateur d'accidents : ", style={"color": "var(--color-ink)"}),
                                html.Span("L'intitulé 'Accidents mortels /100.000 hab' dans la source mesurait en réalité l'ensemble des accidents rapporté à la population. Nous l'avons renommé 'accidents_pour_100k_hab' et avons recalculé séparément le vrai taux de mortalité 'morts_pour_100k_hab'.")
                            ]),
                            html.Div([
                                html.Strong("• Flux vs Stock de véhicules : ", style={"color": "var(--color-ink)"}),
                                html.Span("Les séries d'immatriculations ne constituent pas un parc en circulation. Aucun décompte officiel des véhicules mis à la casse ou exportés n'existant, tout ratio par véhicule est fondé sur un cumul indicatif depuis 1990.")
                            ]),
                            html.Div([
                                html.Strong("• Réconciliation démographique : ", style={"color": "var(--color-ink)"}),
                                html.Span("La ligne 'MARITIME' de l'INSEED (1 346 615 hab) exclut la capitale. Le total administratif de la région Maritime unifiée (avec Grand Lomé) s'établit à 3 534 991 hab. La somme des 5 régions équivaut exactement à 8 095 498 habitants.")
                            ]),
                            html.Div([
                                html.Strong("• Calcul géodésique du réseau routier classé : ", style={"color": "var(--color-ink)"}),
                                html.Span("En l'absence de colonnes kilométriques dans le fichier géographique, la longueur a été calculée sur les géométries WKT par la formule Haversine, aboutissant à un linéaire exact de 3 373,02 km.")
                            ])
                        ]
                    )
                ]
            )
        ]
    )
