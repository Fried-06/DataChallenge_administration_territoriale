"""
components/entete.py
Bandeau d'en-tête pleine largeur aux couleurs institutionnelles du portail service-public.gouv.tg.
Logo officiel posé sur une pastille blanche, titre, bascule thème clair/sombre, bouton Lexique.
"""

from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

def render_entete(theme="light"):
    theme_icon = "lucide:moon" if theme == "light" else "lucide:sun"
    theme_text = "Passer au thème sombre" if theme == "light" else "Passer au thème clair"
    
    return html.Header(
        className="header-banner w-full px-6 py-6 pb-12 shadow-sm",
        children=[
            html.Div(
                className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4",
                children=[
                    # Logo & Titre
                    html.Div(
                        className="flex items-center gap-4",
                        children=[
                            # Pastille blanche avec armoiries officielles
                            html.Div(
                                className="bg-white rounded-full p-2 w-14 h-14 flex items-center justify-center shadow-md",
                                children=[
                                    html.Img(
                                        src="/assets/images/republic-of-togo-government_08f238_opr.png",
                                        alt="République Togolaise",
                                        className="h-10 w-auto object-contain"
                                    )
                                ]
                            ),
                            html.Div([
                                html.H1(
                                    "Mobilité & Sécurité Routière au Togo",
                                    className="text-2xl font-bold tracking-tight text-white mb-0"
                                ),
                                html.P(
                                    "Tableau de bord de l'administration territoriale • Togo AI Labs",
                                    className="text-xs text-white text-opacity-85 m-0"
                                )
                            ])
                        ]
                    ),
                    
                    # Actions d'en-tête (Thème, Lexique, Méthodologie)
                    html.Div(
                        className="flex items-center gap-3",
                        children=[
                            # Bouton Lexique
                            dmc.Button(
                                "Lexique",
                                id="btn-open-lexique",
                                variant="outline",
                                leftSection=DashIconify(icon="lucide:book-open", width=18),
                                styles={"root": {
                                    "borderColor": "rgba(255,255,255,0.4)",
                                    "color": "#FFFFFF",
                                    "borderRadius": "10px",
                                    "&:hover": {"backgroundColor": "rgba(255,255,255,0.15)"}
                                }}
                            ),
                            # Bascule Thème Clair / Sombre
                            dmc.ActionIcon(
                                DashIconify(icon=theme_icon, width=20),
                                id="btn-theme-toggle",
                                size="lg",
                                variant="outline",
                                **{"aria-label": theme_text},
                                styles={"root": {
                                    "borderColor": "rgba(255,255,255,0.4)",
                                    "color": "#FFFFFF",
                                    "borderRadius": "10px",
                                    "&:hover": {"backgroundColor": "rgba(255,255,255,0.15)"}
                                }}
                            )
                        ]
                    )
                ]
            )
        ]
    )
