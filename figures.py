"""
figures.py
Génération de toutes les visualisations Plotly avec les deux templates stricts togo_clair et togo_sombre.
Format français obligatoire (virgule décimale, séparateur milliers espace fine).
"""

import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np

# 1. Définition des templates togo_clair et togo_sombre selon DESIGN.md
SERIES_CLAIR = ['#43A842', '#106E98', '#F2B705', '#7A5C99', '#8A94A3']
SERIES_SOMBRE = ['#5FCB5E', '#4AA8D8', '#F5C02A', '#A98BD0', '#9AA8B3']

def mise_en_page_base(fig, legende=True):
    """
    Mise en page standardisée appliquée à TOUTES les figures Plotly :
    - Titre None (géré par CarteGraphique)
    - Marges optimisées (t=72 si légende, 16 sinon)
    - Légende horizontale au-dessus du graphique
    - hovermode x unified, séparateurs français
    - automargin sur axes X et Y, aucun titre d'axe par défaut
    """
    fig.update_layout(
        title=None,
        margin=dict(l=8, r=16, t=72 if legende else 16, b=8),
        legend=dict(
            orientation="h",
            x=0,
            xanchor="left",
            y=1.02,
            yanchor="bottom",
            font=dict(size=12)
        ),
        hovermode="x unified",
        separators=",\u00a0",
        autosize=True
    )
    fig.update_xaxes(automargin=True, title=None, ticklabelstandoff=4)
    fig.update_yaxes(automargin=True, title=None)
    return fig

togo_clair = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Poppins, system-ui, sans-serif", size=13, color="#5F6B7A"),
        separators=",\u00a0",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=SERIES_CLAIR,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor="#E5E7EB",
            tickcolor="#E5E7EB"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E5E7EB",
            zeroline=False,
            linecolor="rgba(0,0,0,0)"
        )
    )
)

togo_sombre = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Poppins, system-ui, sans-serif", size=13, color="#A3B3AD"),
        separators=",\u00a0",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=SERIES_SOMBRE,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor="#243630",
            tickcolor="#243630"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#243630",
            zeroline=False,
            linecolor="rgba(0,0,0,0)"
        )
    )
)

pio.templates["togo_clair"] = togo_clair
pio.templates["togo_sombre"] = togo_sombre

def get_template(theme="light"):
    return "togo_sombre" if theme == "dark" else "togo_clair"

# --- Figures Mobilité ---

def fig_immatriculations_types(df, theme="light", annee_min=None, annee_max=None):
    tpl = get_template(theme)
    fig = go.Figure()
    
    # Filtrage par plage d'années si précisé
    df_plot = df.copy()
    if annee_min is not None:
        df_plot = df_plot[df_plot['annee'] >= annee_min]
    if annee_max is not None:
        df_plot = df_plot[df_plot['annee'] <= annee_max]
    
    colonnes_flux = [
        ('Motos et 2 roues', 'Motos et deux-roues'),
        ('Voitures', 'Voitures particulières'),
        ('Camionnettes', 'Camionnettes'),
        ('Camions', 'Camions et semi-remorques'),
        ('Autocars/Autobus', 'Autocars et autobus')
    ]
    
    for col, label in colonnes_flux:
        if col in df_plot.columns:
            fig.add_trace(go.Scatter(
                x=df_plot['annee'],
                y=df_plot[col],
                mode='lines',
                stackgroup='one',
                name=label,
                hovertemplate="<b>%{x}</b><br>" + label + " : %{y:,\u00a0.0f} véhicules<extra></extra>"
            ))
            
    fig.update_layout(template=tpl, height=400)
    
    # Plage réelle des données sans marge vide
    df_valid = df_plot.dropna(subset=['annee', 'Total'])
    x_min = int(df_valid['annee'].min()) if not df_valid.empty else 1990
    x_max = int(df_valid['annee'].max()) if not df_valid.empty else 2022
    fig.update_xaxes(range=[x_min, x_max], dtick=5)
    
    return mise_en_page_base(fig, legende=True)

def fig_permis_categories(df, theme="light", annee_min=None, annee_max=None):
    tpl = get_template(theme)
    fig = go.Figure()
    
    # Filtrage par plage d'années si précisé
    df_plot = df.copy()
    if annee_min is not None:
        df_plot = df_plot[df_plot['annee'] >= annee_min]
    if annee_max is not None:
        df_plot = df_plot[df_plot['annee'] <= annee_max]
    
    categories = [
        ('Permis_B_Voiture', 'Permis B (Voiture)'),
        ('Permis_A_Moto', 'Permis A (Moto)'),
        ('Permis_C_Poids_Lourd', 'Permis C (Poids lourd)'),
        ('Permis_D_Transport_Commun', 'Permis D (Transport en commun)'),
        ('Permis_E_Semi_Remorque', 'Permis E (Semi-remorque)')
    ]
    
    for col, label in categories:
        if col in df_plot.columns:
            fig.add_trace(go.Bar(
                x=df_plot['annee'],
                y=df_plot[col],
                name=label,
                hovertemplate="<b>%{x}</b><br>" + label + " : %{y:,\u00a0.0f}<extra></extra>"
            ))
            
    fig.update_layout(template=tpl, barmode='stack', height=400)
    
    # Plage réelle des données
    df_valid = df_plot.dropna(subset=['annee'])
    x_min = int(df_valid['annee'].min()) if not df_valid.empty else 2007
    x_max = int(df_valid['annee'].max()) if not df_valid.empty else 2022
    fig.update_xaxes(range=[x_min - 0.5, x_max + 0.5], dtick=2)
    
    return mise_en_page_base(fig, legende=True)

# --- Figures Sécurité ---

def fig_accidents_morts_blesses(df, theme="light", annee_min=None, annee_max=None):
    tpl = get_template(theme)
    colors = SERIES_SOMBRE if theme == "dark" else SERIES_CLAIR
    fig = go.Figure()
    
    # Filtrage par plage d'années si précisé
    df_plot = df.copy()
    if annee_min is not None:
        df_plot = df_plot[df_plot['annee'] >= annee_min]
    if annee_max is not None:
        df_plot = df_plot[df_plot['annee'] <= annee_max]
    
    fig.add_trace(go.Scatter(
        x=df_plot['annee'],
        y=df_plot['accidents_total'],
        mode='lines+markers',
        name='Accidents corporels',
        line=dict(color=colors[0], width=3),
        hovertemplate="<b>%{x}</b><br>Accidents : %{y:,\u00a0.0f}<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=df_plot['annee'],
        y=df_plot['blesses_total'],
        mode='lines+markers',
        name='Blessés',
        line=dict(color=colors[1], width=2.5),
        hovertemplate="<b>%{x}</b><br>Blessés : %{y:,\u00a0.0f}<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=df_plot['annee'],
        y=df_plot['morts_total'],
        mode='lines+markers',
        name='Morts',
        line=dict(color=colors[2], width=2.5),
        hovertemplate="<b>%{x}</b><br>Morts : %{y:,\u00a0.0f}<extra></extra>"
    ))
    
    fig.update_layout(template=tpl, height=400)
    
    # Plage réelle des données sans marge vide
    df_valid = df_plot.dropna(subset=['accidents_total'])
    x_min = int(df_valid['annee'].min()) if not df_valid.empty else 2010
    x_max = int(df_valid['annee'].max()) if not df_valid.empty else 2022
    fig.update_xaxes(range=[x_min, x_max], dtick=2)
    
    return mise_en_page_base(fig, legende=True)

def fig_ratios_securite(df, theme="light", annee_min=None, annee_max=None):
    tpl = get_template(theme)
    colors = SERIES_SOMBRE if theme == "dark" else SERIES_CLAIR
    fig = go.Figure()
    
    # Filtrage par plage d'années si précisé
    df_plot = df.copy()
    if annee_min is not None:
        df_plot = df_plot[df_plot['annee'] >= annee_min]
    if annee_max is not None:
        df_plot = df_plot[df_plot['annee'] <= annee_max]
    
    fig.add_trace(go.Scatter(
        x=df_plot['annee'],
        y=df_plot['morts_pour_100k_hab'],
        mode='lines+markers',
        name='Morts pour 100 000 hab',
        line=dict(color=colors[0], width=3),
        hovertemplate="<b>%{x}</b><br>Mortalité : %{y:.2f} pour 100 000 hab<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=df_plot['annee'],
        y=df_plot['morts_pour_100_accidents'],
        mode='lines+markers',
        name='Gravité (morts / 100 accidents)',
        line=dict(color=colors[1], width=2.5, dash='dash'),
        hovertemplate="<b>%{x}</b><br>Gravité : %{y:.2f} %<extra></extra>"
    ))
    
    fig.update_layout(template=tpl, height=380)
    
    df_valid = df_plot.dropna(subset=['morts_pour_100k_hab'])
    x_min = int(df_valid['annee'].min()) if not df_valid.empty else 2010
    x_max = int(df_valid['annee'].max()) if not df_valid.empty else 2022
    fig.update_xaxes(range=[x_min, x_max], dtick=2)
    
    return mise_en_page_base(fig, legende=True)

# --- Figures Réseau Routier ---

def fig_etat_routes_region(df, theme="light"):
    tpl = get_template(theme)
    c_bon = "#4CC24B" if theme == "dark" else "#43A842"
    c_moyen = "#F5C02A" if theme == "dark" else "#F2B705"
    c_mauvais = "#EF6B6B" if theme == "dark" else "#D64545"
    c_travaux = "#4AA8D8" if theme == "dark" else "#106E98"
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['region'],
        x=df['pct_bon'],
        name='Bon état',
        orientation='h',
        marker_color=c_bon,
        hovertemplate="<b>%{y}</b><br>Bon état : %{x:.1f} %<extra></extra>"
    ))
    
    fig.add_trace(go.Bar(
        y=df['region'],
        x=df['pct_moyen'],
        name='État moyen',
        orientation='h',
        marker_color=c_moyen,
        hovertemplate="<b>%{y}</b><br>État moyen : %{x:.1f} %<extra></extra>"
    ))
    
    fig.add_trace(go.Bar(
        y=df['region'],
        x=df['pct_mauvais'],
        name='Mauvais état',
        orientation='h',
        marker_color=c_mauvais,
        hovertemplate="<b>%{y}</b><br>Mauvais état : %{x:.1f} %<extra></extra>"
    ))
    
    fig.add_trace(go.Bar(
        y=df['region'],
        x=df['pct_travaux'],
        name='En travaux',
        orientation='h',
        marker_color=c_travaux,
        hovertemplate="<b>%{y}</b><br>En travaux : %{x:.1f} %<extra></extra>"
    ))
    
    fig.update_layout(template=tpl, barmode='stack', height=380)
    fig.update_xaxes(range=[0, 100], dtick=20)
    
    return mise_en_page_base(fig, legende=True)

# --- Figures Formation ---

def fig_densite_auto_ecoles(df, theme="light"):
    tpl = get_template(theme)
    colors = SERIES_SOMBRE if theme == "dark" else SERIES_CLAIR
    
    df_sorted = df.sort_values('auto_ecoles_pour_100k_hab', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_sorted['region'],
        x=df_sorted['auto_ecoles_pour_100k_hab'],
        orientation='h',
        name='Auto-écoles pour 100 000 hab',
        marker_color=colors[0],
        hovertemplate="<b>%{y}</b><br>%{x:.2f} auto-écoles pour 100 000 hab<extra></extra>"
    ))
    
    fig.update_layout(template=tpl, showlegend=False, height=360)
    max_val = float(df_sorted['auto_ecoles_pour_100k_hab'].max())
    fig.update_xaxes(range=[0, max_val * 1.05])
    
    return mise_en_page_base(fig, legende=False)
