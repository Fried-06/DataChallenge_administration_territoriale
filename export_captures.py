"""
export_captures.py
Capture automatique de chaque graphique et carte à 1440, 1024 et 390px, en thème clair et sombre.
Génération d'une galerie HTML d'inspection complète.
"""

import os
import time
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.abspath("outputs/captures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

VIEWPORTS = [
    ("1440px", 1440, 900),
    ("1024px", 1024, 768),
    ("390px", 390, 844)
]

THEMES = ["light", "dark"]

PAGES_CARDS = [
    ("/mobilite", [
        ("carte_immatriculations", 0),
        ("carte_permis", 1)
    ]),
    ("/securite", [
        ("carte_accidents_bilan", 0),
        ("carte_ratios_securite", 1)
    ]),
    ("/routes", [
        ("carte_etat_routes", 0)
    ]),
    ("/formation", [
        ("carte_densite_auto_ecoles", 0)
    ])
]

def main():
    print("[Captures] Démarrage de Playwright...")
    generated_images = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for vp_label, width, height in VIEWPORTS:
            for theme in THEMES:
                print(f"\n--- Viewport {vp_label} | Thème {theme} ---")
                context = browser.new_context(
                    viewport={"width": width, "height": height},
                    color_scheme=theme
                )
                
                # Injection de l'état du thème dans localStorage avant le chargement des scripts Dash
                context.add_init_script(f"""
                    try {{
                        localStorage.setItem('theme-store', JSON.stringify('{theme}'));
                    }} catch (e) {{}}
                """)
                
                page = context.new_page()
                
                for path, cards in PAGES_CARDS:
                    url = f"http://127.0.0.1:8050{path}"
                    try:
                        page.goto(url, wait_until="networkidle", timeout=15000)
                    except Exception:
                        page.goto(url, timeout=15000)
                    
                    # Forcer data-theme sur html et app-root pour correspondre exactement au thème demandé
                    page.evaluate(f"""() => {{
                        document.documentElement.setAttribute('data-theme', '{theme}');
                        document.documentElement.setAttribute('data-mantine-color-scheme', '{theme}');
                        const appRoot = document.getElementById('app-root');
                        if (appRoot) {{
                            appRoot.setAttribute('data-theme', '{theme}');
                        }}
                        // Masquer la barre de debug Dash et la navbar flottante pour une capture isolée
                        const debugEl = document.querySelectorAll('._dash-debug-menu, [class*="_dash-debug"]');
                        debugEl.forEach(el => el.style.display = 'none');
                        const navEl = document.querySelector('.navbar-container');
                        if (navEl) navEl.style.display = 'none';
                    }}""")
                    
                    # Attendre que les graphiques Plotly soient prêts
                    page.wait_for_selector(".js-plotly-plot", timeout=10000)
                    time.sleep(0.9) # Stabilisation du rendu
                    
                    # Sélectionner les cartes
                    card_elements = page.query_selector_all(".card-standard")
                    
                    for card_name, card_idx in cards:
                        if card_idx < len(card_elements):
                            elem = card_elements[card_idx]
                            out_filename = f"{card_name}_{vp_label}_{theme}.png"
                            out_path = os.path.join(OUTPUT_DIR, out_filename)
                            elem.screenshot(path=out_path)
                            generated_images.append((card_name, vp_label, theme, out_filename))
                            print(f"  -> Capture enregistrée : {out_filename}")
                        else:
                            print(f"  [!] Index non trouvé : {card_name} (#{card_idx})")
                            
                context.close()
                
        browser.close()
        
    # Génération d'une galerie d'inspection HTML
    gallery_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Grille de Contrôle Visuel des Graphiques et Cartes</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0F172A; color: #F8FAFC; margin: 0; padding: 24px; }
        h1 { font-size: 24px; margin-bottom: 8px; }
        p.subtitle { color: #94A3B8; margin-top: 0; margin-bottom: 32px; font-size: 14px; }
        .section-title { font-size: 18px; color: #38BDF8; margin: 32px 0 16px; border-bottom: 1px solid #334155; padding-bottom: 8px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 20px; }
        .card { background: #1E293B; border-radius: 12px; border: 1px solid #334155; overflow: hidden; }
        .card-header { padding: 12px 16px; font-size: 13px; font-weight: 600; background: #0F172A; display: flex; justify-content: space-between; border-bottom: 1px solid #334155; }
        .card-body { padding: 12px; display: flex; justify-content: center; background: #0B1120; }
        .card-body img { max-width: 100%; height: auto; border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .badge { padding: 2px 8px; border-radius: 999px; font-size: 11px; }
        .badge-light { background: #E2E8F0; color: #0F172A; }
        .badge-dark { background: #334155; color: #38BDF8; }
    </style>
</head>
<body>
    <h1>Grille de Contrôle Visuel des Graphiques et Cartes</h1>
    <p class="subtitle">Contrôle de superposition des titres/légendes, lisibilité des axes et comportement responsive à 1440px, 1024px et 390px.</p>
"""
    unique_cards = sorted(list(set(x[0] for x in generated_images)))
    for cname in unique_cards:
        gallery_html += f'<div class="section-title">{cname.replace("_", " ").title()}</div><div class="grid">'
        for card_name, vp_label, theme, fname in generated_images:
            if card_name == cname:
                badge_class = "badge-light" if theme == "light" else "badge-dark"
                gallery_html += f"""
                <div class="card">
                    <div class="card-header">
                        <span>{vp_label}</span>
                        <span class="badge {badge_class}">{theme}</span>
                    </div>
                    <div class="card-body">
                        <img src="{fname}" alt="{fname}">
                    </div>
                </div>
                """
        gallery_html += "</div>"
        
    gallery_html += """
</body>
</html>
"""
    gallery_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(gallery_path, "w", encoding="utf-8") as f:
        f.write(gallery_html)
        
    print(f"\n[Captures] Galerie HTML générée avec succès : {gallery_path}")

if __name__ == "__main__":
    main()
