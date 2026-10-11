"""
components/kpi.py
Cartes KPI avec valeur 40px/700, infobulle d'explication et comparaison de référence (Section 3 de DESIGN.md).
"""

from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

def render_kpi_card(valeur, label, comparaison, aide_texte):
    tooltip = dmc.Tooltip(
        label=aide_texte,
        position="top",
        withArrow=True,
        multiline=True,
        w=260,
        children=[
            dmc.ActionIcon(
                DashIconify(icon="lucide:help-circle", width=16),
                size="xs",
                variant="subtle",
                style={"color": "var(--color-ink-muted)"}
            )
        ]
    )
    
    return html.Div(
        className="card-standard flex-1 min-w-[220px]",
        children=[
            html.Div(
                className="flex items-center justify-between mb-2",
                children=[
                    html.Span(label, className="text-xs font-medium", style={"color": "var(--color-ink-soft)"}),
                    tooltip
                ]
            ),
            html.Div(
                valeur,
                className="text-3xl lg:text-4xl font-bold tracking-tight mb-2 tabular-nums",
                style={"color": "var(--color-ink)"}
            ),
            html.Div(
                comparaison,
                className="text-xs font-semibold px-2 py-0.5 rounded inline-block",
                style={"backgroundColor": "rgba(67, 168, 66, 0.12)", "color": "var(--color-brand-green-text)"}
            )
        ]
    )
