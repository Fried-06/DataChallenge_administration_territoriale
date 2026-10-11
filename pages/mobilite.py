"""
pages/mobilite.py
Page Mobilité : immatriculations (1990-2022) et permis (2007-2022) — filtrables par plage d'années.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
from components.carte_graphique import CarteGraphique
from figures import fig_immatriculations_types, fig_permis_categories, SERIES_CLAIR
from data_access import get_immatriculations, get_permis
from insights import format_fr, get_titre_immatriculations, get_titre_permis

dash.register_page(__name__, path="/mobilite", name="Mobilité")

# Bornes globales
_IMM_MIN, _IMM_MAX = 1990, 2022
_PERM_MIN, _PERM_MAX = 2007, 2022


def _slider_marks(min_a, max_a, step=5):
    return {str(y): str(y) for y in range(min_a, max_a + 1, step)}


# Légendes couleur
series_imm = [
    (SERIES_CLAIR[0], 'Motos et deux-roues'),
    (SERIES_CLAIR[1], 'Voitures particulières'),
    (SERIES_CLAIR[2], 'Camionnettes'),
    (SERIES_CLAIR[3], 'Camions et semi-remorques'),
    (SERIES_CLAIR[4], 'Autocars et autobus')
]

series_perm = [
    (SERIES_CLAIR[0], 'Permis B (Voiture)'),
    (SERIES_CLAIR[1], 'Permis A (Moto)'),
    (SERIES_CLAIR[2], 'Permis C (Poids lourd)'),
    (SERIES_CLAIR[3], 'Permis D (Transport en commun)'),
    (SERIES_CLAIR[4], 'Permis E (Semi-remorque)')
]


def layout():
    df_imm = get_immatriculations()
    df_perm = get_permis()

    # ── Chiffres clés immatriculations ──
    imm_2022 = df_imm[df_imm['annee'] == 2022].iloc[0]
    motos_2022 = imm_2022['Motos et 2 roues']
    tot_2022 = imm_2022['Total']
    part_motos_pct = (motos_2022 / tot_2022) * 100.0
    imm_1990 = df_imm[df_imm['annee'] == 1990].iloc[0]
    mult_tot = tot_2022 / imm_1990['Total']

    a_retenir_imm = (
        f"En 2022, les deux-roues représentent {format_fr(part_motos_pct, 1)} % des flux annuels d'immatriculations "
        f"({format_fr(motos_2022)} sur {format_fr(tot_2022)} véhicules enregistrés). Le volume total a été multiplié par {format_fr(mult_tot, 1)} depuis 1990."
    )

    aide_imm = {
        "axes": "Axe X : Année (1990 à 2022). Axe Y : Nombre de véhicules immatriculés au cours de l'année (flux).",
        "exemple": "En 2022, la zone la plus large correspond aux deux-roues motorisés avec 67 639 unités.",
        "piege": "Ces valeurs mesurent les arrivées annuelles (flux) et non le parc en circulation (qui déduirait les pannes et destructions)."
    }

    # ── Chiffres clés permis ──
    perm_2022 = df_perm[df_perm['annee'] == 2022].iloc[0]
    tot_perm_2022 = perm_2022['Total_Permis']
    perm_b_2022 = perm_2022['Permis_B_Voiture']
    perm_a_2022 = perm_2022['Permis_A_Moto']

    a_retenir_perm = (
        f"En 2022, {format_fr(tot_perm_2022)} permis ont été délivrés, dont {format_fr(perm_b_2022)} permis B (voiture) "
        f"et un pic de {format_fr(perm_a_2022)} permis A (moto). L'année 2013 est absente de la série officielle."
    )

    aide_perm = {
        "axes": "Axe X : Années disponibles (2007-2022). Axe Y : Permis délivrés par catégorie d'examen.",
        "exemple": "En 2016, une campagne d'examens exceptionnelle porte le total délivré à 28 451 permis.",
        "piege": "L'année 2013 est une donnée non enregistrée dans la source originale et non une absence totale de conducteurs."
    }

    # ── Slider immatriculations ──
    slider_imm = html.Div(
        className="card-standard mb-4",
        style={"padding": "14px 24px"},
        children=[
            html.Div(
                className="flex items-center gap-3 mb-3",
                children=[
                    html.Span("🗓", style={"fontSize": "16px"}),
                    html.P("Période — immatriculations", className="text-sm font-semibold",
                           style={"color": "var(--color-ink)", "margin": 0}),
                    html.Span(id="mob-imm-label", className="text-xs",
                              style={"color": "var(--color-ink-soft)", "marginLeft": "auto"},
                              children=f"{_IMM_MIN} – {_IMM_MAX}")
                ]
            ),
            dcc.RangeSlider(
                id="mob-imm-slider",
                min=_IMM_MIN, max=_IMM_MAX, step=1,
                value=[_IMM_MIN, _IMM_MAX],
                marks=_slider_marks(_IMM_MIN, _IMM_MAX, step=5),
                allowCross=False,
                tooltip={"placement": "bottom", "always_visible": False},
                className="mob-slider"
            )
        ]
    )

    # ── Slider permis ──
    slider_perm = html.Div(
        className="card-standard mb-4",
        style={"padding": "14px 24px"},
        children=[
            html.Div(
                className="flex items-center gap-3 mb-3",
                children=[
                    html.Span("🗓", style={"fontSize": "16px"}),
                    html.P("Période — permis de conduire", className="text-sm font-semibold",
                           style={"color": "var(--color-ink)", "margin": 0}),
                    html.Span(id="mob-perm-label", className="text-xs",
                              style={"color": "var(--color-ink-soft)", "marginLeft": "auto"},
                              children=f"{_PERM_MIN} – {_PERM_MAX}")
                ]
            ),
            dcc.RangeSlider(
                id="mob-perm-slider",
                min=_PERM_MIN, max=_PERM_MAX, step=1,
                value=[_PERM_MIN, _PERM_MAX],
                marks=_slider_marks(_PERM_MIN, _PERM_MAX, step=3),
                allowCross=False,
                tooltip={"placement": "bottom", "always_visible": False},
                className="mob-slider"
            )
        ]
    )

    # ── Cartes graphiques ──
    carte_imm = CarteGraphique(
        id_prefix="mob_imm",
        titre=get_titre_immatriculations(),
        unite_text="Véhicules immatriculés au cours de l'année (flux annuel)",
        series_legende=series_imm,
        graph_component=dcc.Graph(
            id="mob-graph-imm",
            figure=fig_immatriculations_types(df_imm),
            responsive=True,
            style={"height": "400px", "width": "100%"},
            config={"displayModeBar": False}
        ),
        a_retenir_text=a_retenir_imm,
        aide_lecture_dict=aide_imm,
        source_text="Direction des Transports Routiers et Ferroviaires (DTRF)",
        annee_text="1990-2022",
        limite_text="Radiations et mises au rebut non comptabilisées"
    )

    carte_perm = CarteGraphique(
        id_prefix="mob_perm",
        titre=get_titre_permis(),
        unite_text="Nombre de permis délivrés",
        series_legende=series_perm,
        graph_component=dcc.Graph(
            id="mob-graph-perm",
            figure=fig_permis_categories(df_perm),
            responsive=True,
            style={"height": "400px", "width": "100%"},
            config={"displayModeBar": False}
        ),
        a_retenir_text=a_retenir_perm,
        aide_lecture_dict=aide_perm,
        source_text="Examens de permis de conduire - DTRF",
        annee_text="2007-2022",
        limite_text="Données 2013 non renseignées dans les archives officielles"
    )

    return html.Div(
        className="max-w-7xl mx-auto px-4 py-8",
        children=[
            html.Div(
                className="mb-6",
                children=[
                    html.H2("Combien de véhicules et de conducteurs arrivent sur les routes ?",
                            className="text-2xl font-bold mb-2", style={"color": "var(--color-ink)"}),
                    html.P(
                        "Analyse des flux annuels d'immatriculations et de la délivrance des permis de conduire pour mesurer l'expansion du parc roulant.",
                        className="text-sm", style={"color": "var(--color-ink-soft)"}
                    )
                ]
            ),
            slider_imm,
            carte_imm,
            slider_perm,
            carte_perm,
        ]
    )


# ── Callback immatriculations ──
@callback(
    Output("mob-graph-imm", "figure"),
    Output("mob-imm-label", "children"),
    Input("mob-imm-slider", "value"),
    Input("theme-store", "data"),
)
def update_imm_graph(year_range, theme):
    theme = theme or "light"
    a_min, a_max = year_range if year_range else [_IMM_MIN, _IMM_MAX]
    df_imm = get_immatriculations()
    fig = fig_immatriculations_types(df_imm, theme=theme, annee_min=a_min, annee_max=a_max)
    return fig, f"{a_min} – {a_max}"


# ── Callback permis ──
@callback(
    Output("mob-graph-perm", "figure"),
    Output("mob-perm-label", "children"),
    Input("mob-perm-slider", "value"),
    Input("theme-store", "data"),
)
def update_perm_graph(year_range, theme):
    theme = theme or "light"
    a_min, a_max = year_range if year_range else [_PERM_MIN, _PERM_MAX]
    df_perm = get_permis()
    fig = fig_permis_categories(df_perm, theme=theme, annee_min=a_min, annee_max=a_max)
    return fig, f"{a_min} – {a_max}"
