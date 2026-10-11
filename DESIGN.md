# DESIGN.md : Tableau de bord Mobilité et Sécurité routière du Togo

Ce fichier est la source unique du style. Toute valeur visuelle (couleur, taille, rayon, ombre, durée) vient des tokens ci-dessous. Si une valeur n'y figure pas, demande-la au lieu de l'inventer.

## 1. Direction visuelle

Un outil public togolais, sobre et crédible, qui doit se lire comme un cousin du portail de l'administration (service-public.gouv.tg) sans en être une copie. Fond clair, cartes blanches, texte noir franc, vert et bleu-vert institutionnels. Les chiffres et les cartes sont le contenu, l'interface reste en retrait.

Le seul élément mémorable : la navbar flottante à bosse (section 5). Tout le reste est calme et discipliné. Pas de dégradé décoratif, sauf le bandeau d'en-tête qui reprend celui du portail.

## 2. Couleurs (tokens)

Couleurs de marque, échantillonnées sur le portail :

| Token | Valeur | Usage |
|---|---|---|
| `brand-deep` | #006A50 | début du dégradé d'en-tête, icône et libellé actifs de la navbar |
| `brand-teal` | #106E98 | fin du dégradé d'en-tête, liens secondaires, série 2 des graphiques |
| `brand-green` | #43A842 | boutons principaux, accents, série 1 des graphiques |
| `brand-green-text` | #2B8530 | texte vert sur fond blanc (contraste 4,6:1, le #43A842 n'atteint que 3:1) |
| `signal-yellow` | #FECE11 | bouton d'assistant uniquement, jamais ailleurs |

Neutres :

| Token | Valeur | Usage |
|---|---|---|
| `page` | #FAFAFA | fond de page |
| `surface` | #FFFFFF | cartes, navbar, champs |
| `line` | #E5E7EB | bordures de 1px |
| `ink` | #1B1B1B | titres et texte principal |
| `ink-soft` | #5F6B7A | texte secondaire, légendes, sources |
| `ink-muted` | #6B7686 | éléments inactifs de la navbar |
| `note-bg` | #FBF5DF | encadrés d'information |
| `note-edge` | #9A8B3C | barre gauche de 4px des encadrés |

Couleurs sémantiques de l'état des routes. Elles ne servent qu'à cela :

| État | Valeur |
|---|---|
| Bon | #43A842 |
| Moyen | #F2B705 |
| Mauvais | #D64545 |
| Travaux | #106E98 |

Séries de graphiques, dans cet ordre : #43A842, #106E98, #F2B705, #7A5C99, #8A94A3. Jamais plus de 5 couleurs par graphique.

## 3. Typographie

Famille unique : **Poppins** (Google Fonts, graisses 400, 500, 600, 700). Repli : `system-ui, sans-serif`. Chiffres : `font-variant-numeric: tabular-nums` pour aligner les colonnes.

| Rôle | Taille / graisse | Interligne |
|---|---|---|
| Titre de page | 28px / 700 | 1.2 |
| Titre de section | 20px / 600 | 1.3 |
| Titre de carte | 16px / 600 | 1.3 |
| Valeur de KPI | 40px / 700 | 1.1 |
| Corps | 15px / 400 | 1.55 |
| Libellé, légende, source | 13px / 400 | 1.4 |

Casse normale partout (pas de majuscules espacées pour les libellés). Longueur de ligne maximale : 70 caractères. Titres de page rédigés comme une conclusion chiffrée, par exemple « La Centrale concentre 52 % des routes en mauvais état ».

## 4. Forme, espacement, profondeur

- Rayons : cartes 16px, champs et boutons 10px, pastilles et navbar 999px. Pas de rayon unique pour tout.
- Espacement sur une grille de 8px : 8, 16, 24, 32, 48.
- Cartes : fond `surface`, bordure 1px `line`, padding 24px, **sans ombre**.
- Seule la navbar porte une ombre : `0 10px 30px rgba(0, 106, 80, 0.18)`.
- Boutons principaux : fond `brand-green`, texte blanc 15px / 600, hauteur 44px. Bouton secondaire : contour 1.5px `brand-green`, texte `brand-green-text`.
- Encadré d'information : fond `note-bg`, barre gauche 4px `note-edge`, texte `ink`.

## 5. Navigation : navbar flottante à bosse

Référence : la barre blanche à 3 éléments dont l'élément actif remonte dans un cercle, avec une encoche arrondie dans la barre. Pas de barre latérale.

**Structure**
- 5 entrées, dans l'ordre : Vue d'ensemble, Mobilité, Sécurité, Réseau routier, Formation. Chacune : une icône (Lucide, trait 1.75px, 24px) au-dessus d'un libellé de 12px / 500.
- Barre : fond `surface`, hauteur 72px, rayon 999px, largeur `5 × 96px` (480px), ombre de la section 4.
- Largeur par entrée : 96px fixes, pour que la bosse se calcule sans JavaScript.

**Élément actif**
- Un cercle de 64px, fond `surface`, remonte de 28px au-dessus de la barre. Il contient l'icône en `brand-deep`.
- Autour du cercle, la barre est découpée par une encoche concave de rayon 40px, ce qui donne la « bosse » de la référence.
- Un halo doux `rgba(67, 168, 66, 0.25)`, flou 24px, entoure le cercle.
- Le libellé actif passe en `brand-deep`, graisse 600.

**Éléments inactifs** : icône et libellé en `ink-muted`. Au survol : `ink`.

**Position**
- Écran large : centrée horizontalement, à cheval sur le bas du bandeau d'en-tête, de sorte que la bosse monte dans le dégradé vert.
- Écran étroit (moins de 768px) : fixée en bas de l'écran, à 16px des bords, largeur 100 % moins 32px, entrées de largeur égale.

**Mouvement** : le cercle glisse vers l'entrée choisie en 320ms, `cubic-bezier(0.4, 0, 0.2, 1)`. C'est la seule animation de l'interface. Avec `prefers-reduced-motion`, le déplacement est instantané.

**Réalisation dans Dash (sans JavaScript)**
- `html.Nav` avec 5 `dcc.Link`, et un attribut `data-active="0..4"` mis à jour par un callback sur `dcc.Location`.
- Position du cercle et de l'encoche pilotée par une variable CSS : `--x: calc(var(--item) * 96px + 48px)`.
- Encoche par masque : `mask: radial-gradient(circle 40px at var(--x) 0, transparent 98%, #000)`.
- Cercle : `left: var(--x)`, `transform: translateX(-50%)`, `transition: left 320ms`.
- Accessibilité : `aria-current="page"` sur l'entrée active, focus visible (anneau 2px `brand-teal`, décalage 2px), cibles de 48px minimum.

## 6. En-tête

Bandeau pleine largeur, hauteur 160px, dégradé linéaire à 90° de `brand-deep` vers `brand-teal`. Contient le titre de la page en blanc (28px / 700), une ligne de contexte en blanc à 85 % d'opacité, et le sélecteur d'année à droite. En fond, un motif discret blanc à 6 % d'opacité est permis (silhouette ou tracé de route), jamais de photo.

## 7. Mise en page

- Contenu centré, largeur maximale 1200px, marges de 24px. Grille de 12 colonnes, gouttière 24px.
- La carte principale de chaque page (carte ou graphique clé) occupe au moins 8 colonnes. Les KPI sont en rangée de 3 ou 4, au-dessus.
- Les pages : Vue d'ensemble, Mobilité, Sécurité, Réseau routier, Formation (auto-écoles et indice de vulnérabilité).
- Chaque page se termine par une carte « À savoir » (encadré `note-bg`) qui donne l'année des données et leurs limites, par exemple l'absence de ventilation régionale des accidents.

## 8. Graphiques Plotly

Un seul template appliqué partout : fond transparent, police Poppins 13px `ink-soft`, grille horizontale seule en `line`, pas de bordure d'axe, légende en haut à gauche, infobulle fond `surface` avec bordure `line`. Chaque graphique porte un titre de carte, la source et l'année. Barres plutôt que camemberts ; un camembert n'est permis que jusqu'à 4 parts. Pour l'état des routes, barres empilées à 100 % avec les 4 couleurs sémantiques.

## 9. Cartes

Fond de carte clair, sans étiquettes superflues. Routes classées colorées selon l'état (section 2) ou, sans état, par type : nationale revêtue `brand-deep`, non revêtue `brand-green`, voirie urbaine `brand-teal`, piste `ink-muted`. Auto-écoles : agréée `brand-green`, antenne agréée `brand-teal`, non agréée `ink-muted`. Légende dans une carte flottante en haut à droite.

## 10. Formulaires et composants Mantine

Champs : fond `surface`, bordure 1px `line`, rayon 10px, hauteur 44px, bordure `brand-teal` au focus. Libellé au-dessus, 13px / 500. Tableaux AG Grid en thème clair : en-tête fond `page`, lignes de 44px, séparateurs `line`.

## 11. Intégration technique

Une seule définition de ces couleurs dans trois endroits, sinon les graphiques détonnent :

```js
// tailwind.config.js
theme: { extend: { colors: {
  brand: { deep: '#006A50', teal: '#106E98', green: '#43A842', 'green-text': '#2B8530' },
  ink: { DEFAULT: '#1B1B1B', soft: '#5F6B7A', muted: '#6B7686' },
  page: '#FAFAFA', line: '#E5E7EB', note: '#FBF5DF'
}}, fontFamily: { sans: ['Poppins', 'system-ui', 'sans-serif'] } }
// corePlugins: { preflight: false }  (évite les conflits avec Mantine et dcc)
```

- Thème Mantine : `primaryColor` personnalisée construite sur `#43A842`, `fontFamily: "Poppins"`, `defaultRadius: "md"`.
- Template Plotly : `pio.templates["togo"]` avec `colorway` = séries de la section 2.

## 12. Interdits

Dégradés violet ou bleu décoratifs, effet verre dépoli, ombres sur les cartes, emojis en guise d'icônes, majuscules espacées au-dessus des titres, marqueurs numérotés (01, 02, 03) hors séquence réelle, flèche « → » ajoutée aux boutons, animations d'entrée sur chaque section, survol animé de chaque carte, couleurs d'état utilisées hors état des routes, jaune `signal-yellow` hors bouton d'assistant, plus de 5 couleurs par graphique, texte blanc sur `brand-green` en dessous de 15px.

## 13. Accessibilité

Contraste de 4,5:1 minimum pour le texte. Focus clavier visible partout. Information jamais portée par la couleur seule : les états des routes ont aussi un libellé ou un motif. Interface lisible jusqu'à 360px de large.

## 14. Consigne pour l'agent

Respecte strictement ce fichier. Avant de coder, liste les tokens que tu vas utiliser. Si une demande contredit ce fichier, signale-le au lieu de choisir en silence. Après construction, vérifie la navbar à 3 largeurs (1440, 1024, 390px) et le contraste des textes sur fond vert.
