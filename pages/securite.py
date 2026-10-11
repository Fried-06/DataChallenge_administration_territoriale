"""
pages/securite.py
Page Sécurité : accidents, morts, blessés, ratios de gravité — filtrables par plage d'années.
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
from components.carte_graphique import CarteGraphique
from figures import fig_accidents_morts_blesses, fig_ratios_securite
from data_access import get_accidents
from insights import format_fr, get_titre_accidents, get_titre_ratios_securite

dash.register_page(__name__, path="/securite", name="Sécurité")

# Bornes globales de la série accidents (2010-2022)
_ANNEE_MIN_SEC = 2010
_ANNEE_MAX_SEC = 2022

def _slider_marks(min_a, max_a):
    """Génère les marques du slider espacées de 2 ans."""
    return {str(y): str(y) for y in range(min_a, max_a + 1, 2)}


def layout():
    df_sec = get_accidents()

    # Chiffres 2022 pour les textes statiques
    sec_2022 = df_sec[df_sec['annee'] == 2022].iloc[0]
    acc_22 = sec_2022['accidents_total']
    morts_22 = sec_2022['morts_total']
    blesses_22 = sec_2022['blesses_total']
    gravite_22 = sec_2022['morts_pour_100_accidents']
    taux_100k_22 = sec_2022['morts_pour_100k_hab']

    a_retenir_bilan = (
        f"En 2022, le bilan humain s'établit à {format_fr(morts_22)} tués et {format_fr(blesses_22)} blessés "
        f"pour {format_fr(acc_22)} accidents corporels. La série 2010-2022 met en évidence une forte fluctuation, "
        f"avec un minimum en 2015 suivi d'une hausse jusqu'en 2022."
    )

    aide_bilan = {
        "axes": "Axe X : Année (2010 à 2022). Axe Y : Effectifs constatés (accidents, blessés, morts).",
        "exemple": "En 2022, la courbe verte des blessés atteint 9 918 personnes, tandis que celle des accidents s'établit à 7 507.",
        "piege": "Ces séries recensent les accidents constatés et déclarés par les services de sécurité (police et gendarmerie)."
    }

    a_retenir_ratios = (
        f"Le taux de gravité ressort à {format_fr(gravite_22, 1)} morts pour 100 accidents en 2022, "
        f"soit environ 1 décès pour 11 accidents corporels constatés. Le taux de mortalité atteint {format_fr(taux_100k_22, 1)} décès pour 100 000 habitants."
    )

    aide_ratios = {
        "axes": "Axe X : Année. Axe Y : Ratios calculés (taux de gravité en % et mortalité pour 100 000 hab).",
        "exemple": "En 2021 et 2022, la gravité oscille autour de 9,1 à 9,2 % des sinistres.",
        "piege": "Ne pas confondre 'taux d'accidents pour 100 000 hab' (92,7 en 2022) et 'taux de mortalité' (8,44 pour 100 000 hab)."
    }

    # ---------- Slider de filtre temporel ----------
    slider_section = html.Div(
        className="card-standard mb-6",
        style={"padding": "16px 24px"},
        children=[
            html.Div(
                className="flex items-center gap-3 mb-3",
                children=[
                    html.Span("🗓", style={"fontSize": "18px"}),
                    html.P(
                        "Filtrer la période d'analyse",
                        className="text-sm font-semibold",
                        style={"color": "var(--color-ink)", "margin": 0}
                    ),
                    html.Span(
                        id="sec-slider-label",
                        className="text-xs",
                        style={"color": "var(--color-ink-soft)", "marginLeft": "auto"},
                        children=f"{_ANNEE_MIN_SEC} – {_ANNEE_MAX_SEC}"
                    )
                ]
            ),
            dcc.RangeSlider(
                id="sec-year-slider",
                min=_ANNEE_MIN_SEC,
                max=_ANNEE_MAX_SEC,
                step=1,
                value=[_ANNEE_MIN_SEC, _ANNEE_MAX_SEC],
                marks=_slider_marks(_ANNEE_MIN_SEC, _ANNEE_MAX_SEC),
                allowCross=False,
                tooltip={"placement": "bottom", "always_visible": False},
                className="sec-slider"
            )
        ]
    )

    # ---------- Cartes graphiques (IDs pour callback) ----------
    carte_bilan = CarteGraphique(
        id_prefix="sec_bilan",
        titre=get_titre_accidents(),
        unite_text="Personnes / cas constatés au cours de l'année",
        graph_component=dcc.Graph(
            id="sec-graph-bilan",
            figure=fig_accidents_morts_blesses(df_sec),
            responsive=True,
            style={"height": "400px", "width": "100%"},
            config={"displayModeBar": False}
        ),
        a_retenir_text=a_retenir_bilan,
        aide_lecture_dict=aide_bilan,
        source_text="Direction de la Sécurité Routière / Ministère de la Sécurité",
        annee_text="2010-2022",
        limite_text="Aucune ventilation régionale disponible dans les archives nationales"
    )

    carte_ratios = CarteGraphique(
        id_prefix="sec_ratios",
        titre=get_titre_ratios_securite(),
        unite_text="Taux (mortalité pour 100 000 hab et gravité en %)",
        graph_component=dcc.Graph(
            id="sec-graph-ratios",
            figure=fig_ratios_securite(df_sec),
            responsive=True,
            style={"height": "380px", "width": "100%"},
            config={"displayModeBar": False}
        ),
        a_retenir_text=a_retenir_ratios,
        aide_lecture_dict=aide_ratios,
        source_text="Calculs d'après DSR et RGPH-5",
        annee_text="2010-2022"
    )

    # Encadré méthodologique sur les corrélations
    box_correl = html.Div(
        className="card-standard mb-6",
        children=[
            html.H3("Analyse statistique des corrélations et mise en garde méthodologique", className="text-base font-semibold mb-3", style={"color": "var(--color-ink)"}),
            html.P(
                "L'analyse croisée des séries temporelles (n = 13 années d'observation) met en évidence une corrélation forte entre le volume d'accidents et le nombre de morts (r ≈ 0,72, p < 0,01). "
                "En revanche, la liaison entre les accidents et les flux d'immatriculations annuelles est proche de zéro sur les variations annuelles.",
                className="text-xs leading-relaxed mb-3",
                style={"color": "var(--color-ink-soft)"}
            ),
            html.Div(
                className="box-note text-xs leading-relaxed",
                children=[
                    html.Strong("Rappel de rigueur scientifique : ", style={"color": "var(--color-note-edge)"}),
                    html.Span("Une corrélation statistique ne constitue jamais la démonstration d'un lien de cause à effet. La co-évolution de certains indicateurs de trafic et de sinistralité reflète avant tout la croissance démographique et économique globale du Togo.")
                ]
            )
        ]
    )

    return html.Div(
        className="max-w-7xl mx-auto px-4 py-8",
        children=[
            html.Div(
                className="mb-6",
                children=[
                    html.H2("La route est-elle plus dangereuse, et pour qui ?", className="text-2xl font-bold mb-2", style={"color": "var(--color-ink)"}),
                    html.P(
                        "Évaluation de la sinistralité routière, mesure de la gravité des accidents et vérification empirique des liens avec le trafic.",
                        className="text-sm",
                        style={"color": "var(--color-ink-soft)"}
                    )
                ]
            ),
            slider_section,
            carte_bilan,
            carte_ratios,
            box_correl
        ]
    )


# ── Callback : mise à jour des graphiques sécurité selon la plage choisie ──
@callback(
    Output("sec-graph-bilan", "figure"),
    Output("sec-graph-ratios", "figure"),
    Output("sec-slider-label", "children"),
    Input("sec-year-slider", "value"),
    Input("theme-store", "data"),
)
def update_securite_graphs(year_range, theme):
    theme = theme or "light"
    a_min, a_max = year_range if year_range else [_ANNEE_MIN_SEC, _ANNEE_MAX_SEC]
    df_sec = get_accidents()
    fig_bilan = fig_accidents_morts_blesses(df_sec, theme=theme, annee_min=a_min, annee_max=a_max)
    fig_ratios = fig_ratios_securite(df_sec, theme=theme, annee_min=a_min, annee_max=a_max)
    label = f"{a_min} – {a_max}"
    return fig_bilan, fig_ratios, label
