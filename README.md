# 🎮 Éditeur de Cartes Love2D

Éditeur moderne d'interface française pour créer et gérer des cartes de jeu Love2D avec support des thèmes Windows 11.

## 🚀 Dernières Améliorations (v2.5.0)

### 🎯 **NOUVEAU : Système d'Export Template vs Complet**
- **Deux types d'export package** : Template (images seules) et Complet (avec texte fusionné)
- **Export Template** : Images pures pour positionnement dynamique, animations et traductions
- **Export Complet** : Images prêtes à utiliser avec texte intégré définitivement
- **Tests unitaires complets** : 8/8 tests validant le filtrage de cartes et génération ZIP
- **Documentation intégrée** : README automatique dans chaque package expliquant l'utilisation

### ⭐ **NOUVEAU : Système de Favoris de Formatage**
- **4 boutons favoris** dans l'éditeur de formatage de texte
- **Sauvegarde instantanée** : Bouton "★ Ajouter aux Favoris"
- **Chargement rapide** : 3 boutons "⭐ Favori 1/2/3" pour accès immédiat
- **Feedback visuel** : États colorés (vert=disponible, rouge=vide, normal=défaut)
- **Persistance** : Favoris sauvegardés en base de données
- **Validation robuste** : Gestion d'erreurs et corruption automatique

### ✨ **Correction Majeure : Superposition de Templates (v2.1)**
- **Problème résolu** : Plus de superposition lors des changements de rareté multiples
- **Système perfectionné** : Séparation complète entre image source et image d'affichage
- **Migration automatique** : Cartes existantes mises à jour transparente

### 🔄 **Système de Migration Automatique**
- **Migration progressive** : Mise à jour par étapes de v1 à v5
- **Sauvegarde automatique** : Protection avant chaque migration
- **Compatibilité GitHub** : Utilisateurs existants préservés lors des mises à jour
- **Support chemins absolus** : Gestion complète des chemins personnalisés

### 🛡️ **Robustesse Améliorée**
- **Base de données protégée** : Exclusion automatique du versioning Git
- **Intégrité garantie** : Vérification automatique de la base
- **Tests complets** : Validation du scénario utilisateur GitHub

---

## 🎯 Liens de Documentation

### 📚 Documentation Complète
- **[📖 Documentation Technique](docs/DOCUMENTATION_TECHNIQUE.md)** - Architecture et intégration pour développeurs
- **[⭐ Guide Favoris Utilisateur](docs/GUIDE_FAVORIS_UTILISATEUR.md)** - Guide complet d'utilisation des favoris
- **[📋 Changelog Détaillé](docs/CHANGELOG.md)** - Historique complet des versions
- **[🚀 Guide d'Implémentation](docs/FAVORIS_FORMATAGE_IMPLEMENTATION.md)** - Détails techniques de l'implémentation

### 🎯 Démarrage Rapide v2.4.0
1. **Téléchargez** la dernière version (v2.4.0-favoris)
2. **Lancez** avec `run.bat` (installation automatique)
3. **Explorez** les favoris de formatage dans l'éditeur de texte
4. **Consultez** le guide utilisateur pour maximiser votre productivité

---

## ✨ Fonctionnalités

### � **Système d'Acteurs (Nouveau !)**
- **Acteurs personnalisables** : Créez des personnages, factions, classes
- **Interface visuelle** : Icônes et couleurs pour chaque acteur
- **Liaison carte-acteur** : Associez des cartes à un ou plusieurs acteurs
- **Export par acteur** : Génération de fichiers .lua organisés par acteur

### 🃏 **Visualiseur de Deck avec Tri par Acteur (Nouveau !)**
- **Vue en grille** : Visualisez toutes vos cartes avec images
- **Filtre par acteur** : Affichez uniquement les cartes d'un acteur spécifique
- **Tri par acteur** : Regroupez les cartes par acteur/faction
- **Filtres combinés** : Rareté + Type + Acteur pour recherches précises
- **Raccourci Ctrl+Shift+D** : Accès rapide au visualiseur

### �🎨 **Système de Thèmes Moderne**
- **Mode Automatique** : Suit automatiquement le thème Windows (clair/sombre)
- **Mode Clair** : Interface claire et moderne
- **Mode Sombre** : Interface sombre pour réduire la fatigue oculaire
- **Style Windows 11** : Design moderne avec coins arrondis et espacement optimal

### 🃏 **Gestion des Cartes**
- Interface intuitive avec onglets par rareté
- Support des types multiples (Attaque, Défense, Soin, etc.)
- Système de rareté complet (Commun, Rare, Légendaire, Mythique)
- Édition complète des effets héros et ennemis

### ⭐ **Système de Favoris de Formatage (NOUVEAU !)**
- **Éditeur de formatage amélioré** : 4 boutons favoris intégrés
- **Sauvegarde rapide** : "★ Ajouter aux Favoris" pour sauvegarder le formatage actuel
- **Chargement instantané** : "⭐ Favori 1/2/3" pour accès immédiat aux configurations
- **Feedback visuel intelligent** :
  - 🟢 **Vert** : Favori sauvegardé et prêt à charger
  - 🔴 **Rouge** : Slot vide ou erreur de chargement
  - ⚪ **Normal** : État par défaut
- **Persistance garantie** : Favoris sauvegardés en base de données SQLite
- **Validation robuste** : Gestion automatique des erreurs et corruptions
- **Support complet** : Toutes les options de formatage (police, taille, couleur, position, etc.)

### 🖼️ **Système d'Images Avancé**
- **Fusion automatique d'images avec templates** (✨ Amélioré !)
- **Séparation image source/affichage** : Évite les superpositions de templates
- **Génération d'images de cartes personnalisées**
- **Configuration flexible des templates**
- **Migration automatique** : Mise à jour transparente des cartes existantes

### 🔄 **Système de Migration Automatique (Nouveau !)**
- **Migration transparente** : Mise à jour automatique de la base de données
- **Sauvegarde automatique** : Protection des données avant migration
- **Compatibilité totale** : Préservation des cartes existantes
- **Gestion des chemins absolus** : Support complet des chemins utilisateur
- **Migration progressive** : Mise à jour par étapes sécurisées

### 📤 **Système d'Export Avancé**

#### **🎮 Export Love2D Standard**
- **Export par acteur** : Fichiers .lua séparés par acteur/faction
- **Export global** : Toutes les cartes organisées par acteur
- **Format Love2D complet** : Effects Actor/Enemy, illustrations incluses
- **Export legacy** : Support joueur/IA pour compatibilité
- Support complet des effets et statistiques

#### **📦 Export de Package Complet (✨ Nouveau !)**

Le système propose maintenant **deux types d'export de packages ZIP** pour répondre à différents besoins :

##### **🎨 Export Template (Images Seules)**
- **Images sans texte** : Templates purs pour positionnement dynamique dans Love2D
- **Flexibilité maximale** : Texte positionné en temps réel selon les données
- **Traductions supportées** : Changez le texte sans regénérer les images
- **Animations possibles** : Effets de texte dynamiques dans le jeu
- **Optimisé pour** : Interfaces responsives et multi-langues

```
🖼️ Image Template (sans texte)
┌─────────────────────┐
│ [Template visuel]   │ ← Image de fond pure
│ [Position vide]     │ ← Zone texte définie par TextFormatting
│ [Zone d'effet]      │ ← Positionnement dynamique Love2D
└─────────────────────┘
```

##### **🖼️ Export Complet (Images avec Texte)**
- **Images prêtes à utiliser** : Texte déjà fusionné sur les cartes
- **Rendu constant** : Apparence identique sur tous les systèmes
- **Performance optimisée** : Pas de rendering de texte en temps réel
- **Utilisation immédiate** : Intégration directe dans Love2D
- **Optimisé pour** : Jeux finalisés et distribution

```
🎴 Image Complète (avec texte)
┌─────────────────────┐
│ [Template visuel]   │ ← Image de fond
│ "Nom de Carte"      │ ← Texte fusionné
│ "Description..."    │ ← Texte intégré définitivement
└─────────────────────┘
```

##### **📦 Contenu des Packages ZIP**
- **Package ZIP complet** : Jeu Love2D prêt à jouer
- **Images optimisées** : Format PNG avec compression automatique
- **Polices incluses** : Fonts système automatiquement détectées et copiées
- **Documentation Love2D** : Guide d'intégration et exemples de code
- **Structure organisée** : Dossiers séparés (cards/, fonts/, docs/)
- **Configuration JSON** : Métadonnées du package
- **Interface intégrée** : Bouton "📦 Template" ou "📦 Complet" avec progression

## 🚀 Installation et Lancement

### 🎯 **Méthodes de Lancement**

#### **1. Lancement Automatique (Recommandé)**
```bash
# Double-cliquez sur ce fichier
run.bat
```
- ✅ Crée automatiquement l'environnement virtuel
- ✅ Installe toutes les dépendances 
- ✅ Lance l'application (mode avancé ou compatibilité)
- ✅ Gestion automatique des erreurs

#### **2. Lancement Direct**
```bash
# Alternative plus rapide si Python est déjà configuré
launch.bat
```
- ✅ Lancement immédiat sans vérifications
- ✅ Fallback automatique vers mode compatibilité
- ⚠️ Nécessite Python et dépendances déjà installées

#### **3. Lancement Manuel**
```bash
# En ligne de commande
python test.py                    # Mode automatique (avancé puis compatibilité)
python test.py --force-advanced   # Force le mode avancé avec thèmes
python test_compat.py --compat    # Force le mode compatibilité
```

### 🔧 **Modes de Fonctionnement**

#### **Mode Avancé** 🎨
- Interface moderne avec thèmes Windows 11
- Détection automatique clair/sombre
- Styles visuels optimisés
- **Fallback automatique** si non supporté

#### **Mode Compatibilité** 🛡️
- Interface standard garantie de fonctionner
- Toutes les fonctionnalités principales
- Compatible tous environnements
- **Activé automatiquement** en cas de problème

### ⚡ **Résolution de Problèmes**

| Problème | Solution |
|----------|----------|
| **La fenêtre se ferme** | Utilisez `run.bat` qui affiche les erreurs |
| **Thèmes ne fonctionnent pas** | L'app bascule automatiquement en mode compatibilité |
| **Python non trouvé** | Installez Python depuis https://python.org et ajoutez au PATH |
| **Modules manquants** | Utilisez `run.bat` pour installation automatique |

## 🔧 Utilisation

### Premier Lancement
1. **Configurer les thèmes** : Menu `Affichage > Thèmes et Apparence`
2. **Configurer les images** : Menu `Réglages > Configuration des images`
3. **Créer votre première carte** avec le formulaire à gauche
4. **Migration automatique** : Si vous avez des cartes existantes, elles seront automatiquement mises à jour

### ⭐ **Utiliser les Favoris de Formatage**

#### **🎨 Sauvegarder un Formatage Favori**
1. **Ouvrez l'éditeur de formatage** d'une carte (bouton "Éditer Formatage")
2. **Configurez le formatage** : police, taille, couleur, position, etc.
3. **Cliquez "★ Ajouter aux Favoris"** pour sauvegarder la configuration
4. **Choisissez un nom** descriptif pour le favori
5. **Confirmation** : Le bouton correspondant devient vert 🟢

#### **⚡ Charger un Favori**
1. **Dans l'éditeur de formatage**, repérez les boutons "⭐ Favori 1/2/3"
2. **Bouton vert** 🟢 : Favori disponible, cliquez pour charger instantanément
3. **Bouton rouge** 🔴 : Slot vide, sauvegardez d'abord un favori
4. **Chargement automatique** : Tous les paramètres sont appliqués immédiatement

#### **🔄 États des Boutons Favoris**
- **🟢 Vert** : Favori sauvegardé et prêt à charger
- **🔴 Rouge** : Slot vide ou erreur de chargement  
- **⚪ Normal** : État par défaut ou en cours de traitement

#### **💡 Conseils d'Utilisation**
- **Organisez vos favoris** : Favori 1 pour titres, Favori 2 pour texte, Favori 3 pour effets
- **Sauvegardez plusieurs styles** : Différents thèmes, polices ou layouts
- **Gain de temps** : Plus besoin de reconfigurer manuellement le formatage
- **Persistance garantie** : Vos favoris sont sauvegardés entre les sessions

### 🎯 **Nouveau : Exports Template et Complet**

#### **🚀 Créer un Package Love2D**

##### **Option 1 : Export Template (Recommandé pour le développement)**
1. **Cliquez sur "🎨 Template"** dans la section Export
2. **Choisissez les cartes** à exporter (ou toutes)
3. **Laissez l'outil générer** :
   - ✅ Images sans texte pour positionnement dynamique
   - ✅ Données TextFormatting complètes
   - ✅ Polices système copiées
   - ✅ Documentation Template avec exemples Love2D
   - ✅ Package ZIP optimisé pour flexibilité

##### **Option 2 : Export Complet (Recommandé pour la distribution)**
1. **Cliquez sur "📦 Complet"** dans la section Export  
2. **Choisissez les cartes** à exporter (ou toutes)
3. **Laissez l'outil générer** :
   - ✅ Images avec texte fusionné définitivement
   - ✅ Rendu final constant sur tous systèmes
   - ✅ Polices système incluses pour référence
   - ✅ Documentation Complet avec intégration directe
   - ✅ Package ZIP prêt pour distribution

#### **📁 Structure du Package Généré**
```
📦 [IDs]_template.zip  OU  [IDs]_complete.zip
├── 📄 README.md              # Documentation type-spécifique
├── 📄 package_config.json    # Métadonnées du package  
├── 📄 cards_data.lua         # Données Love2D avec TextFormatting
├── 📁 cards/                 # Images de cartes
│   ├── 🖼️ carte_001.png      # Template OU Complet selon choix
│   ├── 🖼️ carte_002.png      # Optimisées et prêtes à utiliser
│   └── 🖼️ carte_003.png      # Format PNG avec compression
└── 📁 fonts/                 # Polices utilisées
    └── 📝 cambria.ttc         # Polices système détectées
```
├── 📁 fonts/             # Polices détectées automatiquement
│   ├── 🔤 arial.ttf      # Polices système utilisées
│   └── 🔤 custom.otf     # Polices personnalisées
├── 📁 data/              # Données du jeu
│   ├── 📄 cards_joueur.lua  # Données cartes joueur
│   ├── 📄 cards_ia.lua      # Données cartes IA
│   └── 📄 actors.lua        # Définitions des acteurs
└── 📁 docs/              # Documentation Love2D
    ├── 📄 integration_guide.md
    ├── 📄 api_reference.md
    └── 📄 examples.lua
```

#### **🎮 Utilisation dans Love2D**
Le package généré inclut du code Love2D prêt à utiliser :
```lua
-- Exemple d'utilisation des cartes exportées
local cards = require("data.cards_joueur")
local fonts = require("data.fonts")

function love.load()
    -- Les polices sont automatiquement chargées
    local cardFont = fonts.getFont("card_text", 14)
    
    -- Les images sont pré-fusionnées avec templates
    local cardImage = love.graphics.newImage("cards/joueur_carte_1.png")
end
```

#### **🔍 Fonctionnalités Avancées**
- **Détection automatique de polices** : 263 polices système supportées
- **Optimisation d'images** : Compression PNG automatique
- **Support multi-format** : TTF, OTF, système et personnalisées
- **Documentation générée** : Guide d'intégration Love2D complet
- **Package auto-suffisant** : Aucune dépendance externe requise

### �🔄 Migration et Mise à Jour
- **Automatique** : La base de données se met à jour automatiquement
- **Sauvegarde** : Backup automatique avant chaque migration
- **Préservation** : Toutes vos cartes existantes sont conservées
- **Chemins absolus** : Support complet des images avec chemins personnalisés
- **Transparente** : Aucune action requise de votre part

### Gestion des Thèmes
- **Automatique** : L'application suit le thème Windows
- **Manuel** : Choisissez entre clair et sombre
- **Instantané** : Changement immédiat sans redémarrage

### 🔤 **Nouveau : Gestionnaire de Polices Avancé**
- **Détection automatique** : 263 polices système Windows détectées
- **Support multi-format** : TTF, OTF, polices système et personnalisées
- **Intégration Love2D** : Export automatique des polices utilisées
- **Prévisualisation** : Aperçu des polices dans l'interface
- **Optimisation** : Copie uniquement des polices réellement utilisées

### Interface
- **Panneau gauche** : Formulaire d'édition des cartes
- **Panneau droit** : Onglets de navigation par rareté
- **Menu** : Accès aux fonctionnalités avancées

## 🎯 Raccourcis Clavier

| Raccourci | Action |
|-----------|---------|
| `Ctrl+N` | Nouvelle carte |
| `Ctrl+S` | Sauvegarder |
| `Ctrl+D` | Dupliquer carte |
| `Del` | Supprimer carte |
| `F5` | Actualiser |
| `Ctrl+Q` | Quitter |
| `Ctrl+E` | Export Love2D standard |
| `Ctrl+Shift+E` | Export Package Complet |
| `F1` | Aide et documentation |

## 📁 Structure du Projet

```
📁 Projet/
├── 📄 test.py              # Point d'entrée principal
├── 📄 run.bat              # Lanceur automatique Windows
├── 📄 build.bat            # Script de compilation
├── 📄 requirements.txt     # Dépendances Python
├── 📄 cartes.db           # Base de données SQLite
├── 📁 lib/                # Modules de l'application
│   ├── 📄 __init__.py     # Package Python
│   ├── 📄 config.py       # Configuration
│   ├── 📄 database.py     # Gestion base de données
│   ├── 📄 database_migration.py # Système de migration (Nouveau !)
│   ├── 📄 font_manager.py # Gestionnaire de polices système (Nouveau !)
│   ├── 📄 game_package_exporter.py # Export package complet (Nouveau !)
│   ├── 📄 themes.py       # Système de thèmes
│   ├── 📄 theme_settings.py # Interface thèmes
│   ├── 📄 main_app.py     # Application principale
│   ├── 📄 ui_components.py # Composants UI
│   ├── 📄 lua_export.py   # Export Love2D
│   ├── 📄 settings_window.py # Paramètres images
│   ├── 📄 utils.py        # Utilitaires
│   └── 📄 tests.py        # Tests unitaires
├── 📁 images/             # Images générées
├── 📁 fonts/              # Polices système et personnalisées (Nouveau !)
├── 📁 game_packages/      # Packages Love2D exportés (Nouveau !)
├── 📁 data/               # Base de données et configuration (Nouveau !)
└── 📁 venv/               # Environnement virtuel
```

## 🔧 Compilation en Exécutable

```bash
# Avec le script automatique
.\build.bat

# Ou manuellement
pip install pyinstaller
pyinstaller --windowed --onefile test.py
```

## 🧪 Tests

```bash
# Lancer les tests
python test.py --test

# Ou via le script
.\run.bat --test
```

## 🎨 Personnalisation des Thèmes

L'application détecte automatiquement le thème Windows et s'adapte. Vous pouvez :
- Forcer un thème via `Affichage > Thèmes et Apparence`
- Les préférences sont sauvegardées automatiquement
- Changement instantané sans redémarrage

## 📋 Configuration Requise

- **Windows 10/11** (recommandé pour la détection de thème)
- **Python 3.8+**
- **Tkinter** (inclus avec Python)
- **Pillow** (installé automatiquement)

## 🔍 Dépannage

### L'application ne démarre pas
- Vérifiez que Python est installé
- Utilisez `run.bat` pour l'installation automatique
- Vérifiez les permissions d'écriture

### Les thèmes ne fonctionnent pas
- L'application fonctionne sans thèmes avancés
- Utilisez le mode "Clair" par défaut
- Vérifiez la version de Windows

### Les images ne se génèrent pas
- Vérifiez que Pillow est installé
- Configurez un template dans les paramètres
- Vérifiez les permissions du dossier images

### Problème de superposition de templates (Résolu !)
- **Automatiquement corrigé** : Les changements de rareté ne créent plus de superposition
- **Migration transparente** : Cartes existantes automatiquement mises à jour
- **Système perfectionné** : Séparation image source/affichage

### Export de package ne fonctionne pas
- **Vérifiez Python** : Le système d'export nécessite Python 3.8+
- **Vérifiez Pillow** : Installation automatique avec `run.bat`
- **Permissions** : Vérifiez les droits d'écriture dans game_packages/
- **Espace disque** : Les packages peuvent faire jusqu'à 50MB

### Polices ne sont pas détectées
- **Système Windows requis** : 263 polices système supportées
- **Polices personnalisées** : Placez les fichiers .ttf/.otf dans fonts/
- **Permissions** : Vérifiez l'accès aux dossiers système Windows
- **Cache** : Redémarrez l'application pour recharger la liste

### Migration de base de données
- **Automatique** : L'ancienne cartes.db est migrée vers data/cartes.db
- **Sauvegarde** : L'original est préservé dans backups/
- **Script UPDATE.bat** : Gère la migration automatiquement
- **Manuel** : Copiez cartes.db vers data/ si nécessaire

### Mise à jour depuis GitHub
- **Migration automatique** : Vos cartes existantes sont préservées
- **Compatibilité totale** : Support des chemins absolus existants
- **Sauvegarde automatique** : Protection avant toute modification
- **Aucune action requise** : Tout fonctionne automatiquement

## 🧪 Infrastructure de Test Automatisée

### Tests Rapides
```bash
# Windows
.\test_quick.bat

# Validation automatique
python validate_tests_auto.py
```

### Tests Complets
```bash
# Windows - Suite complète
.\test_full.bat

# Linux/Mac - Tests spécifiques
python run_tests.py test_simple
python run_tests.py test_integration_simple
python run_tests.py test_lua_integrity
```

### Organisation des Tests
- **17 tests** organisés dans `tests/` avec syntaxe parfaite (100%)
- **Tests d'intégration** : workflow complet + API validation
- **Hooks Git** automatiques : validation pre/post-commit
- **CI/CD** : GitHub Actions pour validation continue
- **Documentation** : `tests/__index__.py` avec guide complet

### Développement Sécurisé
```bash
# Déploiement avec validation
.\deploy.bat

# Voir tous les tests disponibles
python run_tests.py --list

# Documentation des tests
python run_tests.py --index
```

**🎯 Qualité Garantie** : Infrastructure de test de niveau production avec validation automatique !

## 📄 Licence

Ce projet est libre d'utilisation pour vos projets Love2D !

---

**💡 Astuce** : Utilisez le mode automatique pour que l'application s'adapte parfaitement à votre environnement Windows !
