"""
components/navbar.py
Navbar flottante à bosse (Section 5 de DESIGN.md), 6 entrées :
1. Accueil
2. Mobilité
3. Sécurité
4. Routes
5. Formation
6. Recommandations
"""

from dash import html, dcc
from dash_iconify import DashIconify

NAV_ITEMS = [
    {"href": "/", "label": "Accueil", "icon": "lucide:home", "idx": 0},
    {"href": "/mobilite", "label": "Mobilité", "icon": "lucide:car", "idx": 1},
    {"href": "/securite", "label": "Sécurité", "icon": "lucide:shield-alert", "idx": 2},
    {"href": "/routes", "label": "Routes", "icon": "lucide:git-commit", "idx": 3},
    {"href": "/formation", "label": "Formation", "icon": "lucide:graduation-cap", "idx": 4},
    {"href": "/recommandations", "label": "Actions", "icon": "lucide:check-circle-2", "idx": 5},
]

def render_navbar(active_path="/"):
    # Déterminer l'index actif
    active_idx = 0
    for item in NAV_ITEMS:
        if item["href"] == active_path:
            active_idx = item["idx"]
            break
            
    # Calcul de la position du cercle actif : var(--item) * 104px + (104/2 - 32)
    left_pos = active_idx * 104 + 20
    active_icon = NAV_ITEMS[active_idx]["icon"]
    
    links = []
    for item in NAV_ITEMS:
        is_active = (item["idx"] == active_idx)
        cls = "navbar-item active" if is_active else "navbar-item"
        links.append(
            dcc.Link(
                href=item["href"],
                className=cls,
                children=[
                    DashIconify(icon=item["icon"], width=22, height=22, className="mb-1"),
                    html.Span(item["label"], className="navbar-label")
                ]
            )
        )
        
    indicator = html.Div(
        className="navbar-active-indicator",
        style={"left": f"{left_pos}px"},
        children=[
            DashIconify(icon=active_icon, width=28, height=28, style={"color": "var(--navbar-active-icon)"})
        ]
    )
    
    return html.Nav(
        className="navbar-container",
        children=[indicator] + links
    )
