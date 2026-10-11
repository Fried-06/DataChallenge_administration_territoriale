# QUALITE.md : Audit des sources et journal des anomalies traitées

Ce document consigne les contrôles d'intégrité, les limites méthodologiques et la résolution des 10 pièges connus sur les 8 fichiers CSV du concours Togo AI Labs (Mobilité et sécurité routière).

---

## 1. Dictionnaire des fichiers sources

1. `observationdata-akkouh.csv` : Immatriculations annuelles par catégorie (1990–2022).
2. `observationdata-wklhvw.csv` : Détail des cylindrées et catégories automobiles (2013–2019).
3. `observationdata-wvtolmb.csv` : Permis délivrés aux examens par catégorie (2007–2022).
4. `observationdata-hxdpzbg.csv` : 13 indicateurs macroéconomiques, de trafic et de sécurité routière (1990–2022).
5. `observationdata-tmdtnad.csv` : Audit technique de l'état du réseau routier par tronçon (2020 uniquement).
6. `observationdata-kwwolwb (2).csv` : Recensement général de la population (RGPH-5, INSEED, 2022).
7. `file-routes-routes-classees-18-12-2024-20-38-02.csv` : Répertoire géographique des 799 segments classés (2024).
8. `file-entreprises-auto-ecoles-02-01-2025-16-28-05.csv` : Répertoire géoréférencé des 272 établissements d'auto-écoles (2025).

---

## 2. Traitement des 10 pièges connus

### Piège 1 : Dénomination erronée de l'accidentologie (`hxdpzbg`)
- **Problème :** L'indicateur intitulé *"Accidents mortels /100.000 hab"* mesurait en réalité l'ensemble des accidents de la circulation rapporté à la population ($7\,507 / 8{,}1\text{ M} = 92{,}73$ en 2022) et non les décès.
- **Résolution :** L'indicateur brut a été renommé `accidents_pour_100k_hab`. Le véritable taux de mortalité routière `morts_pour_100k_hab` a été recalculé séparément ($683 / 80{,}95 = 8{,}44$ pour 100 000 habitants en 2022).

### Piège 2 : Flux annuels vs Stock de véhicules (`akkouh`, `wklhvw`)
- **Problème :** Les immatriculations annuelles constituent des **flux** (nouvelles immatriculations de l'année) et non un stock de parc en circulation (ex. 65 599 motos en 2015 $\to$ 45 341 en 2016).
- **Résolution :** Bannissement total du terme "parc" dans l'application au profit de *"Immatriculations de l'année"*. Tout calcul de ratio "par véhicule" s'appuie sur un cumul indicatif depuis 1990 en mentionnant explicitement l'absence de données sur les radiations et mises au rebut.

### Piège 3 : Données manquantes et valeurs atypiques des permis (`wvtolmb`)
- **Problème :** L'année 2013 affichait la valeur "0", masquant une absence de collecte. Des valeurs atypiques apparaissent en 2016 (Total = 28 451) et pour les permis moto A en 2019 (2 425) et 2022 (4 837).
- **Résolution :** L'année 2013 est convertie en `NaN` (valeur manquante non interpolée). Les valeurs atypiques sont conservées et explicitées comme campagnes exceptionnelles d'examens dans les infobulles.

### Piège 4 : Hiérarchie démographique et statut du Grand Lomé (`kwwolwb`)
- **Problème :** La ligne *"MARITIME"* (1 346 615 hab) exclut le Grand Lomé (DAGL = Golfe + Agoè-Nyivé = 2 188 376 hab).
- **Résolution :** Réconciliation stricte : Région Maritime unifiée = $1\,346\,615 + 2\,188\,376 = 3\,534\,991$ habitants. La somme des 5 régions équivaut exactement aux 8 095 498 habitants du Togo.

### Piège 5 : Normalisation toponymique et préfectures
- **Problème :** Toponymes avec accents ou casse hétérogène (Tône vs TONE, Cinkassé vs CINKASSE). L'Avé est étiqueté `"TOTOAL AVE"` (111 214 hab).
- **Résolution :** Normalisation standard Unicode ASCII majuscule sans accent. Les 39 préfectures officielles ont été extraites avec exactitude arithmétique ($8\,095\,498$ hab).

### Piège 6 : Découpage et intégrité de l'état des routes (`tmdtnad`)
- **Problème :** Présence de 4 lignes de totaux partiels (`TOTAL`, `TOTAL RT`, `VOIRIES  REVETUES`, `VOIRIES EN TERRE`) doublant les linéaires réels.
- **Résolution :** Séparation des lignes agrégées et validation de l'égalité stricte :
  $$\text{BON} + \text{MOYEN} + \text{MAUVAIS} + \text{TRAVAUX} = \text{TOTAL}$$
  Écart maximal mesuré : $0{,}00\text{ km}$ (tolérance de $0{,}02\text{ km}$ respectée). Remplacement des NaN de `TRAVAUX` par 0,0. Inférence régionale par préfixe (`TGRP` $\to$ Plateaux, `TGRK` $\to$ Kara, etc.).

### Piège 7 : Absence de longueur sur les routes classées
- **Problème :** Le fichier géographique WKT ne comportait aucun attribut métrique de longueur.
- **Résolution :** Calcul géodésique Haversine (WGS84). Longueur totale mesurée : **3 373,02 km** (écart $< 0{,}01\%$ par rapport aux 3 373 km théoriques).

### Piège 8 : Décalage temporel des millésimes
- **Constat :** Réseau audité en 2020, Population en 2022, Répertoire d'entreprises en 2024-2025.
- **Résolution :** Affichage systématique du millésime exact sur chaque graphique et cartouche.

### Piège 9 : Absence de ventilation régionale des accidents
- **Constat :** Aucune donnée d'accident ou de permis n'est ventilée par région dans les statistiques nationales.
- **Résolution :** Les ratios d'accidents sont exclusivement nationaux. L'absence de régionalisation est clairement notifiée.

### Piège 10 : Auto-écoles et qualité des adresses
- **Constat :** Adresses souvent non renseignées ("Nsp", "Néant").
- **Résolution :** Traitement en valeurs manquantes sans altération du positionnement géographique. Nettoyage du statut en {Agréée, Antenne agréée, Non agréée}.
