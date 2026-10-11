"""
app.py
Application Dash principale pour le tableau de bord Mobilité & Sécurité Routière du Togo.
Publication compatible Plotly Cloud (plan gratuit).
"""

import dash
from dash import html, dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from components.entete import render_entete
from components.navbar import render_navbar
from components.footer import render_footer
from components.lexique import render_lexique_drawer
from data_access import verify_all_assertions

# Contrôle strict d'intégrité au démarrage
verify_all_assertions()

# Initialisation de l'application Dash
app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Mobilité & Sécurité Routière • Togo",
    update_title=None
)

server = app.server

app.layout = html.Div([
    # Composants Dash utilitaires en dehors de MantineProvider (évite le crash DMC 0.14.7)
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="theme-store", storage_type="local", data="light"),
    
    # Enveloppe MantineProvider uniquement sur le contenu visuel
    dmc.MantineProvider(
        id="mantine-provider",
        theme={
            "primaryColor": "green",
            "fontFamily": "Poppins, system-ui, sans-serif",
            "defaultRadius": "md"
        },
        children=[
            # Enveloppe principale recevant l'attribut data-theme
            html.Div(
                id="app-root",
                children=[
                    # En-tête bandeau pleine largeur
                    html.Div(id="entete-container", children=render_entete("light")),
                    
                    # Navbar flottante à bosse
                    html.Div(id="navbar-container-wrapper", className="relative -mt-9 mb-6 z-40", children=render_navbar("/")),
                    
                    # Contenu dynamique de la page
                    html.Main(
                        id="page-content",
                        className="min-h-screen",
                        children=[dash.page_container]
                    ),
                    
                    # Pied de page
                    render_footer(),
                    
                    # Drawer du lexique
                    render_lexique_drawer()
                ]
            )
        ]
    )
])

# Callback de synchronisation de la navbar avec l'URL
@callback(
    Output("navbar-container-wrapper", "children"),
    Input("url", "pathname")
)
def update_navbar_active(pathname):
    return render_navbar(pathname or "/")

# Callback de bascule du thème
@callback(
    Output("theme-store", "data"),
    Input("btn-theme-toggle", "n_clicks"),
    State("theme-store", "data"),
    prevent_initial_call=True
)
def toggle_theme(n_clicks, current_theme):
    if not n_clicks:
        return current_theme
    return "dark" if current_theme == "light" else "light"

# Callback de mise à jour de l'attribut data-theme sur le conteneur principal et rafraîchissement de l'en-tête
@callback(
    Output("app-root", "data-theme"),
    Output("entete-container", "children"),
    Input("theme-store", "data")
)
def apply_theme(theme_data):
    theme = theme_data or "light"
    return theme, render_entete(theme)

# Callback d'ouverture du drawer Lexique
@callback(
    Output("drawer-lexique", "opened"),
    Input("btn-open-lexique", "n_clicks"),
    State("drawer-lexique", "opened"),
    prevent_initial_call=True
)
def toggle_lexique(n_clicks, is_opened):
    if not n_clicks:
        return False
    return not is_opened

if __name__ == "__main__":
    app.run(debug=True, port=8050)
