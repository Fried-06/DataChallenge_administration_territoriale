"""
pages/routes.py
Page Réseau Routier : Question civique, répartition de l'état 2020 par région, tableau AG Grid des tronçons dégradés.
"""

import dash
from dash import html, dcc
import dash_ag_grid as dag
import dash_mantine_components as dmc
from components.carte_graphique import CarteGraphique
from figures import fig_etat_routes_region
from data_access import get_etat_routes_region, get_etat_routes_troncons
from insights import format_fr, get_titre_routes

dash.register_page(__name__, path="/routes", name="Routes")

def layout():
    df_reg = get_etat_routes_region()
    df_tron = get_etat_routes_troncons()
    
    # Chiffres clés
    tot_km = df_reg['TOTAL'].sum()
    mauvais_km = df_reg['MAUVAIS'].sum()
    travaux_km = df_reg['TRAVAUX'].sum()
    pct_mauvais = (mauvais_km / tot_km) * 100.0
    pct_travaux = (travaux_km / tot_km) * 100.0
    
    a_retenir_etat = (
        f"Sur les {format_fr(tot_km)} km de réseau audités en 2020, {format_fr(pct_mauvais, 1)} % sont en mauvais état "
        f"({format_fr(mauvais_km)} km) et {format_fr(pct_travaux, 1)} % en travaux ({format_fr(travaux_km)} km). La région des Plateaux présente la plus forte dégradation."
    )
    
    aide_etat = {
        "axes": "Axe Y : Régions du Togo. Axe X : Proportion du réseau audité (%).",
        "exemple": "Le segment rouge indique les tronçons dégradés, le bleu les sections en travaux, le jaune l'état moyen et le vert le bon état.",
        "piege": "L'état 'Travaux' n'est pas un 'Bon état' : il engendre des ralentissements et des risques accrus pour les usagers."
    }
    
    # Séries pour légende HTML (4 séries)
    series_routes = [
        ("#43A842", "Bon état"),
        ("#F2B705", "État moyen"),
        ("#D64545", "Mauvais état"),
        ("#106E98", "En travaux")
    ]
    
    carte_etat = CarteGraphique(
        id_prefix="routes_etat",
        titre=get_titre_routes(),
        unite_text="Proportion du réseau audité par région (%)",
        series_legende=series_routes,
        graph_component=dcc.Graph(
            figure=fig_etat_routes_region(df_reg),
            responsive=True,
            style={"height": "380px", "width": "100%"},
            config={"displayModeBar": False}
        ),
        a_retenir_text=a_retenir_etat,
        aide_lecture_dict=aide_etat,
        source_text="Direction Générale des Travaux Publics (DGTP)",
        annee_text="2020 (Audit d'état)",
        limite_text="Audit réalisé sur les axes structurants en 2020"
    )
    
    # Tableau AG Grid des tronçons les plus dégradés
    df_top_degrades = df_tron.sort_values('pct_mauvais', ascending=False).head(15).copy()
    grid_data = df_top_degrades[['tronçon', 'region', 'indicateur', 'TOTAL', 'MAUVAIS', 'pct_mauvais', 'TRAVAUX']].to_dict('records')
    
    column_defs = [
        {"field": "tronçon", "headerName": "Tronçon / Axe", "flex": 2, "filter": True},
        {"field": "region", "headerName": "Région", "flex": 1, "filter": True},
        {"field": "indicateur", "headerName": "Revêtement", "flex": 1, "filter": True},
        {"field": "TOTAL", "headerName": "Longueur (km)", "flex": 1, "valueFormatter": {"function": "d3.format(',.1f')(params.value)"}},
        {"field": "MAUVAIS", "headerName": "Km Mauvais", "flex": 1, "valueFormatter": {"function": "d3.format(',.1f')(params.value)"}},
        {"field": "pct_mauvais", "headerName": "% Mauvais", "flex": 1, "valueFormatter": {"function": "d3.format(',.1f')(params.value) + ' %'"}}
    ]
    
    grid = dag.AgGrid(
        id="grid-troncons-degrades",
        rowData=grid_data,
        columnDefs=column_defs,
        defaultColDef={"resizable": True, "sortable": True},
        dashGridOptions={"pagination": True, "paginationPageSize": 8},
        className="ag-theme-alpine",
        style={"height": 380, "width": "100%"}
    )
    
    carte_grid = html.Div(
        className="card-standard mb-6",
        children=[
            html.H3("Priorités d'entretien : les 15 tronçons les plus dégradés du réseau", className="text-base font-semibold mb-2", style={"color": "var(--color-ink)"}),
            html.P(
                "Tableau dynamique des axes routiers répertoriant les plus forts taux de dégradation physique lors de l'audit technique.",
                className="text-xs mb-4",
                style={"color": "var(--color-ink-soft)"}
            ),
            grid
        ]
    )
    
    return html.Div(
        className="max-w-7xl mx-auto px-4 py-8",
        children=[
            html.Div(
                className="mb-8",
                children=[
                    html.H2("Dans quel état physique se trouve le réseau, et où ?", className="text-2xl font-bold mb-2", style={"color": "var(--color-ink)"}),
                    html.P(
                        "Diagnostic spatialisé de l'infrastructure routière nationale, identification des points noirs d'entretien et suivi des chantiers.",
                        className="text-sm",
                        style={"color": "var(--color-ink-soft)"}
                    )
                ]
            ),
            carte_etat,
            carte_grid
        ]
    )
