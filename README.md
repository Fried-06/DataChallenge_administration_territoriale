# Tableau de Bord Mobilité et Sécurité Routière au Togo
**Concours Togo AI Labs • Thème : Administration Territoriale**

Application Dash conçue pour permettre à tout citoyen, journaliste ou décideur public d'explorer et de comprendre la dynamique de la circulation, l'état physique du réseau et la sinistralité routière au Togo.

---

## 1. Lancement local rapide

Dans votre terminal PowerShell :

```powershell
# 1. (Optionnel) Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application Dash
python app.py
```

Ouvrez ensuite votre navigateur à l'adresse suivante :
👉 **`http://127.0.0.1:8050/`** (ou `http://localhost:8050/`)

---

## 2. Déploiement Plotly Cloud (Plan Gratuit)

L'application est 100 % prête pour être déployée sur Plotly Cloud / Render / Heroku :
- **Point d'entrée :** `app.py`
- **Serveur WSGI :** `server = app.server`
- **Dépendances :** épinglées dans `requirements.txt`
- **Fichiers CSS :** entièrement précompilés dans `assets/tailwind.css` et `assets/custom.css` (aucun build Node.js requis en production).

> **Note relative au plan gratuit Plotly Cloud :**
> Le plan gratuit n'héberge qu'une application à la fois et peut mettre le conteneur en veille après une période d'inactivité. Le redémarrage peut alors prendre quelques dizaines de secondes lors de la première requête.

---

## 3. Structure du projet

- `app.py` : Point d'entrée Dash avec architecture multipage (`use_pages=True`).
- `pages/` : Les 6 pages principales et la page méthodologie :
  - `accueil.py` : Synthèse globale, 4 KPI clés, 3 constats majeurs et accès thématiques.
  - `mobilite.py` : Flux d'immatriculations, part des deux-roues et examens de permis.
  - `securite.py` : Accidents, blessés, mortalité et analyse des corrélations.
  - `routes.py` : Répartition de l'état physique 2020 et tableau des tronçons dégradés.
  - `formation.py` : Répartition géographique des auto-écoles et simulateur de vulnérabilité.
  - `recommandations.py` : 8 fiches d'action ciblées pour les territoires.
  - `methodologie.py` : Documentation des données, sources et limites.
- `components/` :
  - `navbar.py` : Navbar flottante à bosse (6 entrées, encoche concave et glissement 320ms).
  - `entete.py` : Bandeau dégradé aux couleurs institutionnelles, bascule thème et Lexique.
  - `carte_graphique.py` : Conteneur réutilisable pour chaque visuel avec aide à la lecture et données.
  - `lexique.py` : Drawer interactif des termes techniques.
- `figures.py` : Templates stricts `togo_clair` et `togo_sombre` et visualisations Plotly.
- `data_access.py` : Couche d'accès, cache et assertions d'intégrité (population = 8 095 498).
- `outputs/clean/` : Les 9 tables nettoyées et documentées.
- `QUALITE.md` : Journal d'audit et traitement détaillé des 10 pièges connus.
- `RAPPORT.md` : Synthèse analytique et orientations stratégiques.
