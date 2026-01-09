# Rapport de Projet : Skijo

## 1. Introduction

### 1.1 Présentation du projet
**Skijo** est une implémentation numérique du jeu de cartes Skyjo en Python. Le projet propose une interface graphique interactive permettant à plusieurs joueurs de s'affronter dans ce jeu de stratégie où l'objectif est d'obtenir le score le plus bas possible.

### 1.2 Objectifs du projet
- Créer une version jouable du jeu de cartes Skyjo
- Fournir une interface graphique conviviale avec Tkinter
- Implémenter la logique de jeu complète
- Permettre des parties multijoueurs
- Gérer un système de scores sur plusieurs manches

## 2. Architecture du Projet

### 2.1 Structure des répertoires

```
Skijo/
├── main.py              # Point d'entrée de l'application
├── core/                # Module principal du jeu
│   ├── deck.py         # Gestion du paquet de cartes
│   ├── player_base.py  # Classe de base des joueurs
│   └── skyjo_board.py  # Plateau de jeu et logique principale
├── gui/                 # Interface graphique
│   └── skyjoApp.py     # Application Tkinter
└── bots/                # Intelligence artificielle
    └── random_bot.py   # Bot aléatoire (en développement)
```

### 2.2 Technologies utilisées
- **Langage** : Python 3
- **Interface graphique** : Tkinter
- **Bibliothèques** : random (pour le mélange des cartes)

## 3. Modules et Composants

### 3.1 Module Core

#### 3.1.1 deck.py - Gestion du paquet de cartes
**Responsabilité** : Créer et gérer le paquet de cartes Skyjo

**Classe principale** : `Deck`

**Fonctionnalités** :
- Création d'un paquet de 150 cartes selon les règles officielles :
  - Cartes de valeur -2 : 5 exemplaires
  - Cartes de valeur -1 à 12 : 10 exemplaires chacune
  - Cartes de valeur 0 : 15 exemplaires
- Mélange aléatoire du paquet
- Pioche de cartes

**Méthodes clés** :
```python
creat_deck()      # Création du paquet
shuffle_deck()    # Mélange du paquet
pick_card()       # Pioche d'une carte
```

#### 3.1.2 player_base.py - Joueur de base
**Responsabilité** : Représenter un joueur et son état de jeu

**Classe principale** : `SkyjoPlayer`

**Caractéristiques** :
- Grille de 12 cartes (3 lignes × 4 colonnes)
- Chaque carte a deux états : valeur et visibilité
- Calcul du score total

**Attributs** :
- `name` : Nom du joueur
- `grid` : Dictionnaire contenant les 12 cartes
- `score` : Score actuel du joueur

**Méthodes clés** :
```python
init_player(deck)    # Initialisation avec 12 cartes
compute_score()      # Calcul du score total
```

#### 3.1.3 skyjo_board.py - Plateau de jeu
**Responsabilité** : Gérer la logique du jeu et l'état de la partie

**Classe principale** : `SkyjoBoard`

**Fonctionnalités** :
- Initialisation d'une partie avec plusieurs joueurs
- Gestion du tour des joueurs
- Gestion de la pioche et de la défausse
- Détection de fin de partie
- Calcul des gagnants

**Attributs principaux** :
- `players` : Dictionnaire des joueurs
- `deck` : Paquet de cartes
- `discard_pile` : Pile de défausse
- `current_player` : Joueur actuel
- `game_over` : État de la partie

**Méthodes clés** :
```python
init_game(players_name)      # Initialisation de la partie
pick_from_deck()             # Piocher du paquet
pick_from_pile()             # Piocher de la défausse
next_player()                # Passer au joueur suivant
is_player_all_visible()      # Vérifier si toutes les cartes sont visibles
finalize_if_needed()         # Finaliser la partie si nécessaire
```

### 3.2 Module GUI

#### 3.2.1 skyjoApp.py - Interface graphique
**Responsabilité** : Fournir l'interface utilisateur et gérer les interactions

**Classe principale** : `SkyjoApp`

**Fonctionnalités** :
- Affichage des grilles de tous les joueurs
- Boutons pour piocher du deck ou de la pile
- Gestion des clics sur les cartes
- Mise à jour visuelle de l'état du jeu
- Détection et gestion des colonnes identiques (règle spéciale)
- Affichage des scores

**Composants UI** :
- Grilles de cartes (3×4) pour chaque joueur
- Bouton "Piocher une carte"
- Bouton affichant la carte du dessus de la défausse
- Système de tours (un seul joueur actif à la fois)

**Mécanisme de jeu** :
1. Le joueur clique sur "Piocher" ou sur la pile de défausse
2. Si pioche du deck : la carte est affichée temporairement
3. Le joueur clique sur une de ses cartes pour la remplacer
4. L'ancienne carte va dans la défausse
5. Vérification des colonnes identiques (3 cartes = suppression)
6. Passage au joueur suivant

### 3.3 Module Bots

#### 3.3.1 random_bot.py - Intelligence artificielle
**Responsabilité** : Fournir un adversaire contrôlé par l'ordinateur

**État actuel** : Squelette de base créé mais non implémenté

**Classe principale** : `RandomBot` (hérite de `SkyjoPlayer`)

## 4. Règles du Jeu Implémentées

### 4.1 Règles de base
1. **Objectif** : Obtenir le score le plus bas possible
2. **Plateau** : Chaque joueur possède 12 cartes disposées en grille 3×4
3. **Début** : Les cartes sont face cachée au départ

### 4.2 Déroulement d'un tour
1. Le joueur peut :
   - Piocher une carte du deck (face cachée)
   - Prendre la carte visible de la défausse
2. Avec la carte piochée :
   - Remplacer une de ses cartes (qui va dans la défausse)

### 4.3 Règle spéciale : Colonnes identiques
Si 3 cartes d'une même colonne ont la même valeur, elles sont éliminées et comptent pour 0 point.

### 4.4 Fin de partie
La partie se termine quand un joueur a toutes ses cartes visibles. Le joueur avec le score le plus bas gagne la manche.

### 4.5 Système de manches
Le jeu continue jusqu'à ce qu'un joueur atteigne 3 victoires. Les scores sont cumulés sur 100 points.

## 5. Point d'Entrée : main.py

Le fichier `main.py` orchestre l'ensemble du jeu :

```python
# Configuration initiale
players = ["Maxime", "Antoine"]
scores = {name: {"win": 0, "score": 0} for name in players}

# Boucle de jeu (jusqu'à 3 victoires)
while scores["Maxime"]["win"] < 3 and scores["Antoine"]["win"] < 3:
    # Initialisation d'une nouvelle partie
    game = SkyjoBoard()
    game.init_game(players)
    
    # Lancement de l'interface
    app = SkyjoApp(root, game, scores)
    root.mainloop()
```

## 6. Analyse Technique

### 6.1 Points forts
1. **Architecture modulaire** : Séparation claire entre logique métier (core), interface (gui) et IA (bots)
2. **Extensibilité** : Structure permettant d'ajouter facilement de nouveaux types de joueurs (IA)
3. **Gestion d'état** : Bonne séparation entre l'état du jeu et l'affichage
4. **Règles du jeu** : Implémentation correcte des mécaniques de base

### 6.2 Points à améliorer

#### 6.2.1 Interface utilisateur
- **Limitation actuelle** : L'interface détruit et recrée la fenêtre à chaque manche (ligne 103 de skyjoApp.py)
- **Impact** : Expérience utilisateur interrompue
- **Recommandation** : Implémenter un système de réinitialisation sans destruction de fenêtre

#### 6.2.2 Gestion des tours
- **Limitation** : Pas de distinction visuelle claire du joueur actif
- **Recommandation** : Ajouter des indicateurs visuels (couleurs, bordures) pour le joueur actuel

#### 6.2.3 Affichage des cartes
- **Limitation** : Les cartes cachées affichent "?" (basique)
- **Recommandation** : Améliorer le design avec des couleurs, des images ou des symboles

#### 6.2.4 Intelligence artificielle
- **État** : RandomBot non implémenté
- **Impact** : Impossible de jouer contre l'ordinateur
- **Recommandation prioritaire** : Implémenter la logique du bot

#### 6.2.5 Gestion d'erreurs
- **Limitation** : Peu de validation et de gestion d'exceptions
- **Risques** : 
  - Que se passe-t-il si le deck est vide ?
  - Gestion des cas limites
- **Recommandation** : Ajouter des vérifications et des messages d'erreur

#### 6.2.6 Code quality
- **Observations** :
  - Noms de variables en français et anglais mélangés
  - Commentaires limités
  - Pas de docstrings pour certaines méthodes
- **Recommandation** : Standardiser le code (tout en français ou tout en anglais)

#### 6.2.7 Tests
- **État** : Aucun test unitaire présent
- **Risque** : Difficile de valider les modifications sans régression
- **Recommandation** : Ajouter des tests pour les modules core

## 7. Fonctionnalités Manquantes

### 7.1 Phase initiale du jeu
Dans Skyjo, les joueurs doivent initialement révéler 2 cartes de leur choix avant de commencer. Cette phase n'est pas implémentée.

### 7.2 Intelligence artificielle
Le bot RandomBot n'a pas de logique de jeu. Il devrait pouvoir :
- Décider de piocher du deck ou de la pile
- Choisir quelle carte remplacer
- Utiliser une stratégie (même simple)

### 7.3 Validation des règles
Certaines règles pourraient être mieux contrôlées :
- Empêcher les actions hors tour
- Valider les actions possibles
- Afficher les actions disponibles

### 7.4 Sauvegarde et statistiques
- Pas de sauvegarde de partie
- Pas d'historique des parties
- Pas de statistiques détaillées

### 7.5 Multijoueur réseau
Le jeu est actuellement limité à des joueurs sur le même ordinateur.

## 8. Recommandations de Développement

### 8.1 Court terme (Priorité haute)
1. **Implémenter RandomBot** : Permettre de jouer contre l'IA
2. **Ajouter la phase initiale** : Révéler 2 cartes au début
3. **Améliorer l'UI** : Indicateurs visuels du joueur actif
4. **Fixer le bug de destroy()** : Éviter la fermeture brutale de fenêtre

### 8.2 Moyen terme (Priorité moyenne)
1. **Tests unitaires** : Couvrir les modules core
2. **Gestion d'erreurs** : Ajouter validations et exceptions
3. **Documentation** : Ajouter docstrings et commentaires
4. **Standardisation** : Choisir une langue unique pour le code

### 8.3 Long terme (Amélioration)
1. **IA avancée** : Stratégies de jeu plus élaborées
2. **Mode multijoueur réseau** : Jouer en ligne
3. **Personnalisation** : Thèmes visuels, nombres de joueurs variables
4. **Statistiques** : Tracking des performances, historique
5. **Animations** : Mouvements de cartes fluides
6. **Son** : Effets sonores et musique de fond

## 9. Estimation de l'État du Projet

### 9.1 Complétude fonctionnelle
- **Logique de jeu** : 75% (règles de base OK, manque phase initiale)
- **Interface utilisateur** : 60% (fonctionnelle mais basique)
- **Intelligence artificielle** : 5% (structure seulement)
- **Qualité du code** : 65% (architecture OK, manque tests et doc)

### 9.2 État global
**Prototype fonctionnel** : Le jeu est jouable entre humains mais nécessite des améliorations pour être considéré comme "terminé".

## 10. Conclusion

Le projet Skijo représente une implémentation solide des bases du jeu de cartes Skyjo. L'architecture modulaire et la séparation des responsabilités constituent de bonnes fondations pour le développement futur.

### Points positifs :
- ✅ Structure de projet claire et logique
- ✅ Séparation des préoccupations (MVC-like)
- ✅ Règles de base du jeu implémentées
- ✅ Interface fonctionnelle avec Tkinter
- ✅ Système de scores et manches

### Axes d'amélioration :
- ⚠️ Finaliser l'intelligence artificielle
- ⚠️ Améliorer l'expérience utilisateur
- ⚠️ Ajouter des tests
- ⚠️ Enrichir la documentation
- ⚠️ Corriger les bugs mineurs

Le projet est dans un état satisfaisant pour un prototype et peut servir de base solide pour un développement plus poussé vers une version complète et polie du jeu Skyjo.

---

**Date du rapport** : Janvier 2026  
**Version analysée** : Commit 16157e0  
**Nombre de fichiers** : 7 fichiers Python principaux  
**Lignes de code** : ~300 lignes (estimation)
