"""
pages/formation.py
Page Formation : Question civique, répartition des auto-écoles, agréments et indice de vulnérabilité paramétrable.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
from components.carte_graphique import CarteGraphique
from figures import fig_densite_auto_ecoles
from data_access import get_region_indicateurs, get_auto_ecoles
from insights import format_fr, get_titre_auto_ecoles

dash.register_page(__name__, path="/formation", name="Formation")

def layout():
    df_reg = get_region_indicateurs()
    df_ae = get_auto_ecoles()
    
    tot_ae = len(df_ae)
    tot_agreees = len(df_ae[df_ae['est_agreee'] == True])
    pct_agreees = (tot_agreees / tot_ae) * 100.0
    
    maritime_ae = len(df_ae[df_ae['region'] == 'MARITIME'])
    part_maritime_pct = (maritime_ae / tot_ae) * 100.0
    
    a_retenir_ae = (
        f"Le Togo compte {format_fr(tot_ae)} auto-écoles recensées, dont {format_fr(tot_agreees)} agréées ou antennes agréées ({format_fr(pct_agreees, 1)} %). "
        f"La région Maritime concentre {format_fr(part_maritime_pct, 1)} % des établissements ({maritime_ae} établissements)."
    )
    
    aide_ae = {
        "axes": "Axe Y : Régions du Togo. Axe X : Nombre d'auto-écoles pour 100 000 habitants.",
        "exemple": "La région Maritime présente le ratio le plus élevé avec plus de 6 auto-écoles pour 100k hab, contre moins de 2 dans les Savanes.",
        "piege": "La présence d'une structure ne garantit pas la détention d'un agrément ministériel valide."
    }
    
    carte_densite = CarteGraphique(
        id_prefix="form_densite",
        titre=get_titre_auto_ecoles(),
        unite_text="Nombre d'auto-écoles pour 100 000 habitants",
        graph_component=dcc.Graph(
            figure=fig_densite_auto_ecoles(df_reg),
            responsive=True,
            style={"height": "360px", "width": "100%"},
            config={"displayModeBar": False}
        ),
        a_retenir_text=a_retenir_ae,
        aide_lecture_dict=aide_ae,
        source_text="Répertoire des entreprises - Ministère des Transports",
        annee_text="2025 (Recensement des établissements)"
    )
    
    # Simulateur de l'Indice de Vulnérabilité Régionale
    simulateur = html.Div(
        className="card-standard mb-6",
        children=[
            html.H3("Indice de Vulnérabilité Territoriale (Simulateur interactif 0-100)", className="text-base font-semibold mb-2", style={"color": "var(--color-ink)"}),
            html.P(
                "Ajustez les pondérations politiques et techniques pour observer la sensibilité du score de vulnérabilité de chaque région.",
                className="text-xs mb-4",
                style={"color": "var(--color-ink-soft)"}
            ),
            html.Div(
                className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6",
                children=[
                    html.Div([
                        html.Label("Poids : Routes en mauvais état (%)", className="text-xs font-medium mb-1 block"),
                        dcc.Slider(id="slider-poids-routes", min=0, max=100, step=5, value=40, marks={0: '0%', 50: '50%', 100: '100%'})
                    ]),
                    html.Div([
                        html.Label("Poids : Déficit de réseau classé (%)", className="text-xs font-medium mb-1 block"),
                        dcc.Slider(id="slider-poids-km", min=0, max=100, step=5, value=30, marks={0: '0%', 50: '50%', 100: '100%'})
                    ]),
                    html.Div([
                        html.Label("Poids : Déficit d'auto-écoles agréées (%)", className="text-xs font-medium mb-1 block"),
                        dcc.Slider(id="slider-poids-ae", min=0, max=100, step=5, value=30, marks={0: '0%', 50: '50%', 100: '100%'})
                    ])
                ]
            ),
            html.Div(id="resultat-vulnerabilite", className="mt-4")
        ]
    )
    
    return html.Div(
        className="max-w-7xl mx-auto px-4 py-8",
        children=[
            html.Div(
                className="mb-8",
                children=[
                    html.H2("Y a-t-il assez d'auto-écoles, et sont-elles agréées ?", className="text-2xl font-bold mb-2", style={"color": "var(--color-ink)"}),
                    html.P(
                        "Analyse de l'accès à l'apprentissage de la conduite et calcul de la vulnérabilité globale des territoires.",
                        className="text-sm",
                        style={"color": "var(--color-ink-soft)"}
                    )
                ]
            ),
            carte_densite,
            simulateur
        ]
    )

@callback(
    Output("resultat-vulnerabilite", "children"),
    Input("slider-poids-routes", "value"),
    Input("slider-poids-km", "value"),
    Input("slider-poids-ae", "value")
)
def update_vulnerabilite(p_routes, p_km, p_ae):
    tot = p_routes + p_km + p_ae
    if tot == 0:
        w_r, w_k, w_a = 0.33, 0.33, 0.34
    else:
        w_r, w_k, w_a = p_routes / tot, p_km / tot, p_ae / tot
        
    df = get_region_indicateurs().copy()
    
    def min_max(s):
        diff = s.max() - s.min()
        return (s - s.min()) / diff if diff > 0 else s * 0
        
    norm_mauvais = min_max(df['pct_mauvais'])
    norm_km_inv = 1.0 - min_max(df['km_routes_pour_100k_hab'])
    norm_ae_inv = 1.0 - min_max(df['auto_ecoles_agreees_pour_100k_hab'])
    
    df['score'] = (w_r * norm_mauvais + w_k * norm_km_inv + w_a * norm_ae_inv) * 100.0
    df = df.sort_values('score', ascending=False)
    
    cards = []
    for idx, row in df.iterrows():
        cards.append(
            html.Div(
                className="flex items-center justify-between p-3 rounded-lg border mb-2",
                style={"borderColor": "var(--color-line)", "backgroundColor": "var(--color-surface)"},
                children=[
                    html.Span(row['region'], className="font-semibold text-sm", style={"color": "var(--color-ink)"}),
                    html.Div(className="flex items-center gap-3", children=[
                        html.Span(f"Score : {row['score']:.1f} / 100", className="text-sm font-bold", style={"color": "var(--color-brand-deep)"}),
                        html.Span(f"(Routes dégradées : {row['pct_mauvais']:.1f} %)", className="text-xs text-gray-500")
                    ])
                ]
            )
        )
        
    return html.Div(children=cards)
