"""
components/footer.py
Pied de page officiel sobre et rigoureux (Section 7 de DESIGN.md).
"""

from dash import html, dcc

def render_footer():
    return html.Footer(
        className="w-full border-t mt-16 py-8 px-6 text-sm",
        style={"borderColor": "var(--color-line)", "backgroundColor": "var(--color-surface)"},
        children=[
            html.Div(
                className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4",
                children=[
                    html.Div(
                        className="flex items-center gap-3",
                        children=[
                            html.Img(
                                src="/assets/images/republic-of-togo-government_08f238_opr.png",
                                alt="Gouvernement Togolais",
                                className="h-8 w-auto object-contain"
                            ),
                            html.Span(
                                "Données ouvertes du Togo • Concours Togo AI Labs (Administration Territoriale)",
                                style={"color": "var(--color-ink-soft)"}
                            )
                        ]
                    ),
                    html.Div(
                        className="flex items-center gap-6",
                        children=[
                            html.Span(
                                "Sources : 2020 (Routes), 2022 (Population & Accidents), 2024-2025 (Établissements)",
                                style={"color": "var(--color-ink-muted)", "fontSize": "12px"}
                            ),
                            dcc.Link(
                                "Méthodologie & Qualité",
                                href="/methodologie",
                                style={"color": "var(--color-brand-teal)", "fontWeight": "500", "textDecoration": "none"}
                            )
                        ]
                    )
                ]
            )
        ]
    )
