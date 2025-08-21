# 🎮 Éditeur de Cartes Love2D

Éditeur moderne d'interface française pour créer et gérer des cartes de jeu Love2D avec support des thèmes Windows 11.

## 🚀 Dernières Améliorations (v2.1)

### ✨ **Correction Majeure : Superposition de Templates**
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

### 📤 **Export Love2D**
- **Export par acteur** : Fichiers .lua séparés par acteur/faction
- **Export global** : Toutes les cartes organisées par acteur
- **Format Love2D complet** : Effects Actor/Enemy, illustrations incluses
- **Export legacy** : Support joueur/IA pour compatibilité
- Support complet des effets et statistiques

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

### 🔄 Migration et Mise à Jour
- **Automatique** : La base de données se met à jour automatiquement
- **Sauvegarde** : Backup automatique avant chaque migration
- **Préservation** : Toutes vos cartes existantes sont conservées
- **Chemins absolus** : Support complet des images avec chemins personnalisés
- **Transparente** : Aucune action requise de votre part

### Gestion des Thèmes
- **Automatique** : L'application suit le thème Windows
- **Manuel** : Choisissez entre clair et sombre
- **Instantané** : Changement immédiat sans redémarrage

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
│   ├── 📄 themes.py       # Système de thèmes
│   ├── 📄 theme_settings.py # Interface thèmes
│   ├── 📄 main_app.py     # Application principale
│   ├── 📄 ui_components.py # Composants UI
│   ├── 📄 lua_export.py   # Export Love2D
│   ├── 📄 settings_window.py # Paramètres images
│   ├── 📄 utils.py        # Utilitaires
│   └── 📄 tests.py        # Tests unitaires
├── 📁 images/             # Images générées
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
