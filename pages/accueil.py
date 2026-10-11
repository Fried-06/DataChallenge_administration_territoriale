"""
pages/accueil.py
Page d'accueil : phrase d'ouverture, 4 KPI clés, 3 constats majeurs calculés, cartes des questions vers les 5 pages.
"""

import dash
from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from components.kpi import render_kpi_card
from insights import get_kpis_accueil, get_constats_accueil

dash.register_page(__name__, path="/", name="Accueil")

PAGES_LINKS = [
    {
        "titre": "Mobilité & Motorisation",
        "question": "Combien de véhicules et de conducteurs arrivent sur les routes, et quelle est la place des deux-roues ?",
        "href": "/mobilite",
        "icon": "lucide:car"
    },
    {
        "titre": "Sécurité Routière",
        "question": "La route est-elle plus dangereuse, pour qui, et le volume de trafic explique-t-il les décès ?",
        "href": "/securite",
        "icon": "lucide:shield-alert"
    },
    {
        "titre": "Réseau Routier",
        "question": "Dans quel état physique se trouve le réseau routier togolais, et quelles régions sont pénalisées ?",
        "href": "/routes",
        "icon": "lucide:git-commit"
    },
    {
        "titre": "Formation & Auto-écoles",
        "question": "Y a-t-il assez d'auto-écoles agréées pour former les conducteurs selon les régions ?",
        "href": "/formation",
        "icon": "lucide:graduation-cap"
    },
    {
        "titre": "Recommandations Ciblées",
        "question": "Quelles actions concrètes et mesurables engager pour l'administration territoriale ?",
        "href": "/recommandations",
        "icon": "lucide:check-circle-2"
    }
]

def layout():
    kpis = get_kpis_accueil()
    constats = get_constats_accueil()
    
    # 4 Cartes KPI
    kpi_cards = [
        render_kpi_card(kpis["morts"]["valeur"], kpis["morts"]["label"], kpis["morts"]["comparaison"], kpis["morts"]["aide"]),
        render_kpi_card(kpis["accidents"]["valeur"], kpis["accidents"]["label"], kpis["accidents"]["comparaison"], kpis["accidents"]["aide"]),
        render_kpi_card(kpis["immatriculations"]["valeur"], kpis["immatriculations"]["label"], kpis["immatriculations"]["comparaison"], kpis["immatriculations"]["aide"]),
        render_kpi_card(kpis["routes_degradees"]["valeur"], kpis["routes_degradees"]["label"], kpis["routes_degradees"]["comparaison"], kpis["routes_degradees"]["aide"])
    ]
    
    # Cartes vers les 5 pages
    nav_cards = []
    for p in PAGES_LINKS:
        nav_cards.append(
            dcc.Link(
                href=p["href"],
                className="card-standard hover:border-emerald-600 transition-colors flex flex-col justify-between text-decoration-none block",
                style={"textDecoration": "none"},
                children=[
                    html.Div([
                        html.Div(
                            className="w-10 h-10 rounded-lg flex items-center justify-center mb-3",
                            style={"backgroundColor": "rgba(0, 106, 80, 0.1)"},
                            children=[DashIconify(icon=p["icon"], width=22, style={"color": "var(--color-brand-deep)"})]
                        ),
                        html.H4(p["titre"], className="text-base font-semibold mb-2", style={"color": "var(--color-ink)"}),
                        html.P(p["question"], className="text-xs leading-relaxed mb-4", style={"color": "var(--color-ink-soft)"})
                    ]),
                    html.Div(
                        className="text-xs font-semibold flex items-center gap-1",
                        style={"color": "var(--color-brand-green-text)"},
                        children=[
                            html.Span("Explorer les données"),
                            DashIconify(icon="lucide:arrow-right", width=14)
                        ]
                    )
                ]
            )
        )
        
    return html.Div(
        className="max-w-7xl mx-auto px-4 py-8",
        children=[
            # Phrase d'ouverture
            html.Div(
                className="mb-8",
                children=[
                    html.H2(
                        "Comprendre la dynamique routière pour agir sur les territoires",
                        className="text-2xl lg:text-3xl font-bold tracking-tight mb-2",
                        style={"color": "var(--color-ink)"}
                    ),
                    html.P(
                        "Cet outil public rassemble et croise les données officielles de circulation, de sinistralité, "
                        "de voirie et d'accès à la formation pour éclairer les décisions d'aménagement et de sécurité au Togo.",
                        className="text-sm max-w-3xl leading-relaxed",
                        style={"color": "var(--color-ink-soft)"}
                    )
                ]
            ),
            
            # Bandeau dismissible d'aide à la lecture
            dmc.Alert(
                title="Comment lire ce tableau de bord ?",
                color="teal",
                className="mb-8",
                styles={"root": {"borderRadius": "12px"}},
                children=[
                    html.P(
                        "1. Chaque page répond à une question civique précise en fournissant des preuves chiffrées issues des bases officielles. "
                        "2. Aucun graphique n'est présenté sans son explication synthétique et son cartouche d'aide à la lecture. "
                        "3. Toutes les définitions et conventions de calcul sont consultables via le bouton Lexique en haut à droite.",
                        className="text-xs leading-relaxed m-0"
                    )
                ]
            ),
            
            # Rangée des 4 KPI
            html.Div(
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10",
                children=kpi_cards
            ),
            
            # Section Ce qu'il faut retenir (3 constats calculés)
            html.Div(
                className="card-standard mb-10",
                children=[
                    html.Div(
                        className="flex items-center gap-2 mb-4",
                        children=[
                            DashIconify(icon="lucide:sparkles", width=20, style={"color": "var(--color-brand-green)"}),
                            html.H3("Ce qu'il faut retenir (faits établis par les données)", className="text-lg font-semibold m-0", style={"color": "var(--color-ink)"})
                        ]
                    ),
                    html.Div(
                        className="grid grid-cols-1 md:grid-cols-3 gap-6",
                        children=[
                            html.Div(className="box-note text-xs leading-relaxed", children=[constats[0]]),
                            html.Div(className="box-note text-xs leading-relaxed", children=[constats[1]]),
                            html.Div(className="box-note text-xs leading-relaxed", children=[constats[2]])
                        ]
                    )
                ]
            ),
            
            # Grille des 5 pages avec questions
            html.Div(
                className="mb-6",
                children=[
                    html.H3("Axes d'exploration thématiques", className="text-xl font-bold mb-4", style={"color": "var(--color-ink)"}),
                    html.Div(
                        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6",
                        children=nav_cards
                    )
                ]
            )
        ]
    )
