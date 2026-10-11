"""
components/carte_graphique.py
Composant réutilisable obligatoire pour chaque graphique, carte ou tableau :
1. Titre-question / Titre-conclusion calculé
2. Graphique ou carte
3. Ligne "À retenir" avec chiffres réels
4. Bouton Tooltip "Comment lire ce graphique" (dmc.Tooltip, compatible DMC 0.14.7)
5. Pied de carte : source, millésime, limites
6. Bloc d'aide à la lecture déplié sous le graphique
"""

from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def CarteGraphique(
    id_prefix,
    titre,
    graph_component,
    a_retenir_text,
    aide_lecture_dict,
    source_text="Ministère des Transports Routiers / DSR Togo",
    annee_text="2022",
    limite_text=None,
    df_table=None,
    unite_text=None,
    series_legende=None
):
    """
    Paramètres :
    - aide_lecture_dict : {'axes': str, 'exemple': str, 'piege': str}
    - unite_text : chaîne descriptive de l'unité (ex. "Véhicules immatriculés (flux annuel)")
    - series_legende : liste de tuples (couleur, libellé) pour légende HTML (>= 4 séries)
    
    Note d'implémentation (DMC 0.14.7) :
    dmc.HoverCard cause un crash JS ("Cannot read properties of undefined
    (reading 'type')") car HoverCardTarget tente de cloner l'enfant React pour
    injecter un ref, ce que DashIconify (composant fonctionnel pur) ne supporte
    pas. On utilise à la place un Tooltip textuel + un bloc d'aide statique.
    """

    # Texte unique de l'aide (pour dmc.Tooltip, label doit être une chaîne)
    axes_txt    = aide_lecture_dict.get('axes',    '')
    exemple_txt = aide_lecture_dict.get('exemple', '')
    piege_txt   = aide_lecture_dict.get('piege',   'Aucun piège majeur.')

    tooltip_label = (
        f"Axes : {axes_txt}  |  "
        f"Exemple : {exemple_txt}  |  "
        f"Piège : {piege_txt}"
    )

    # Bouton info avec Tooltip (uniquement texte — compatible DMC 0.14.7)
    info_btn = dmc.Tooltip(
        label=tooltip_label,
        position="bottom-end",
        withArrow=True,
        multiline=True,
        w=380,
        children=[
            html.Div(
                DashIconify(
                    icon="lucide:info",
                    width=18,
                    style={"color": "var(--color-ink-soft)"}
                ),
                style={
                    "cursor": "help",
                    "display": "flex",
                    "alignItems": "center",
                    "padding": "4px"
                }
            )
        ]
    )

    # Header de la carte avec Titre + Unité sous le titre (13px, texte secondaire)
    title_block = [
        html.H3(titre, className="text-base font-semibold m-0 leading-snug",
                style={"color": "var(--color-ink)"})
    ]
    if unite_text:
        title_block.append(
            html.Div(f"Unité : {unite_text}", className="mt-1 font-normal",
                     style={"color": "var(--color-ink-soft)", "fontSize": "13px"})
        )

    header = html.Div(
        className="flex items-start justify-between gap-4 mb-4",
        children=[
            html.Div(children=title_block, className="flex-1"),
            html.Div(className="flex items-center gap-2 flex-shrink-0",
                     children=[info_btn])
        ]
    )

    # Légende HTML responsive pour 4 séries ou plus (activée sur écran étroit via CSS)
    legende_html_block = None
    has_html_legende = False
    if series_legende and len(series_legende) >= 4:
        has_html_legende = True
        legende_html_block = html.Div(
            className="legende-html-narrow-only flex flex-wrap gap-x-4 gap-y-1.5 mb-3 text-xs items-center",
            children=[
                html.Div(
                    className="flex items-center gap-1.5",
                    children=[
                        html.Span(
                            style={
                                "display": "inline-block",
                                "width": "10px",
                                "height": "10px",
                                "borderRadius": "50%",
                                "backgroundColor": col,
                                "flexShrink": 0
                            }
                        ),
                        html.Span(lab, style={"color": "var(--color-ink-soft)"})
                    ]
                )
                for col, lab in series_legende
            ]
        )

    # Bloc d'aide à la lecture (toujours visible sous le graphique)
    aide_bloc = html.Div(
        className="mt-3 rounded-lg text-xs leading-relaxed",
        style={
            "backgroundColor": "rgba(16, 110, 152, 0.05)",
            "border": "1px solid rgba(16, 110, 152, 0.15)",
            "padding": "10px 14px"
        },
        children=[
            html.Div(
                className="flex items-center gap-1 mb-1 font-semibold",
                style={"color": "var(--color-brand-teal)"},
                children=[
                    DashIconify(icon="lucide:help-circle", width=14),
                    html.Span("Comment lire ce graphique")
                ]
            ),
            html.Div([
                html.Span("Repères et axes : ", className="font-medium"),
                html.Span(axes_txt, style={"color": "var(--color-ink-soft)"})
            ], className="mb-1"),
            html.Div([
                html.Span("Exemple : ", className="font-medium"),
                html.Span(exemple_txt, style={"color": "var(--color-ink-soft)"})
            ], className="mb-1"),
            html.Div([
                html.Span("⚠ Piège : ", className="font-medium",
                          style={"color": "var(--color-note-edge)"}),
                html.Span(piege_txt, style={"color": "var(--color-ink-soft)"})
            ])
        ]
    )

    # Ligne "À retenir"
    a_retenir_banner = html.Div(
        className="mt-3 py-2 px-3 rounded-lg text-sm flex items-start gap-2",
        style={
            "backgroundColor": "rgba(67, 168, 66, 0.08)",
            "border": "1px solid rgba(67, 168, 66, 0.2)"
        },
        children=[
            DashIconify(icon="lucide:check-circle-2", width=18,
                        className="mt-0.5 flex-shrink-0",
                        style={"color": "var(--color-brand-green-text)"}),
            html.Span([
                html.Strong("À retenir : ",
                            style={"color": "var(--color-brand-green-text)"}),
                html.Span(a_retenir_text, style={"color": "var(--color-ink)"})
            ])
        ]
    )

    # Footer avec source et limite
    footer_parts = [
        html.Span(
            f"Source : {source_text} • Données : {annee_text}",
            style={"color": "var(--color-ink-muted)", "fontSize": "12px"}
        )
    ]
    if limite_text:
        footer_parts.append(
            html.Span(
                f" • Limite : {limite_text}",
                style={"color": "var(--color-note-edge)", "fontSize": "12px"}
            )
        )

    footer = html.Div(
        className="mt-4 pt-3 border-t flex flex-wrap items-center justify-between gap-2",
        style={"borderColor": "var(--color-line)"},
        children=[html.Div(children=footer_parts)]
    )

    card_children = [header]
    if legende_html_block:
        card_children.append(legende_html_block)

    graph_wrapper_class = f"chart-container-wrapper w-full {'has-html-legend' if has_html_legende else ''}"
    card_children.append(html.Div(graph_component, className=graph_wrapper_class))
    card_children.extend([aide_bloc, a_retenir_banner, footer])

    return html.Div(
        className="card-standard w-full mb-6",
        children=card_children
    )

