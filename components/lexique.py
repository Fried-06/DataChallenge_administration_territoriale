"""
components/lexique.py
Drawer interactif contenant les définitions rigoureuses de tous les termes techniques employés.
"""

from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

LEXIQUE_TERMES = [
    {
        "terme": "Flux annuel d'immatriculations",
        "definition": "Volume brut des nouveaux véhicules enregistrés ou mis en circulation au cours d'une année civile. Il ne prend pas en compte les radiations, destructions ou départs, et ne doit jamais être confondu avec un parc de véhicules en circulation."
    },
    {
        "terme": "Taux d'accidents pour 100 000 habitants",
        "definition": "Nombre d'accidents corporels rapporté à la population résidente nationale, multiplié par 100 000. Dans certains rapports initiaux, cet indicateur a été incorrectement libellé 'Accidents mortels /100k hab' alors qu'il inclut l'ensemble des sinistres."
    },
    {
        "terme": "Taux de mortalité routière (morts / 100k hab)",
        "definition": "Nombre de personnes décédées des suites d'un accident de la circulation pour 100 000 habitants au cours d'une année."
    },
    {
        "terme": "Taux de gravité",
        "definition": "Nombre de personnes tuées pour 100 accidents corporels constatés. Il mesure la létalité relative des sinistres survenus sur le réseau."
    },
    {
        "terme": "État 'Travaux' d'un tronçon",
        "definition": "Tronçon routier faisant l'objet d'un chantier d'aménagement, d'élargissement ou de réhabilitation. Il n'est pas classé en 'Bon état' car la circulation y subit des restrictions ou des perturbations."
    },
    {
        "terme": "Corrélation statistique (r)",
        "definition": "Mesure du degré de liaison linéaire (Pearson) ou de rang (Spearman) entre deux séries. Une corrélation élevée n'implique aucune relation de cause à effet : deux indicateurs peuvent évoluer conjointement sous l'effet d'une croissance démographique ou d'une tendance commune sans que l'un ne cause l'autre."
    },
    {
        "terme": "Auto-école agréée / Antenne",
        "definition": "Établissement d'enseignement de la conduite ayant reçu l'agrément ministériel formel certifiant la conformité de ses équipements, véhicules et formateurs. Les antennes sont des succursales rattachées à un siège agréé."
    }
]

def render_lexique_drawer():
    accordions = []
    for item in LEXIQUE_TERMES:
        accordions.append(
            dmc.AccordionItem(
                value=item["terme"],
                children=[
                    dmc.AccordionControl(item["terme"], style={"fontWeight": "600", "color": "var(--color-ink)"}),
                    dmc.AccordionPanel(item["definition"], style={"fontSize": "13px", "color": "var(--color-ink-soft)", "lineHeight": "1.6"})
                ]
            )
        )
        
    return dmc.Drawer(
        id="drawer-lexique",
        title=html.Div([
            DashIconify(icon="lucide:book-open", width=22, className="inline mr-2", style={"color": "var(--color-brand-green)"}),
            html.Span("Lexique & Définitions officielles", className="font-semibold text-lg")
        ]),
        padding="md",
        size="md",
        position="right",
        opened=False,
        children=[
            html.P(
                "Toutes les notions techniques employées dans le tableau de bord sont définies ci-dessous en langage clair et vérifié.",
                className="text-xs mb-4",
                style={"color": "var(--color-ink-soft)"}
            ),
            dmc.Accordion(children=accordions, value=LEXIQUE_TERMES[0]["terme"])
        ]
    )
