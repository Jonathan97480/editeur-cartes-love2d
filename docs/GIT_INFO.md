# Gestion de Version - Éditeur de Cartes Love2D

## Configuration Git

Dépôt Git local initialisé le $(Get-Date)

### Informations du dépôt
- **Branche principale :** master
- **Premier commit :** 93200ef - "Initial commit: Éditeur de cartes Love2D modulaire complet"
- **Fichiers trackés :** 30 fichiers, 4423+ lignes de code

### Structure du projet versionnée

```
📁 lib/                     # Package principal modulaire
├── __init__.py            # Initialisation du package
├── config.py              # Configuration globale
├── database.py            # Gestion SQLite
├── lua_export.py          # Export Love2D
├── main_app.py           # Application principale
├── settings_window.py     # Fenêtre de configuration
├── simple_settings_window.py # Configuration simplifiée
├── tests.py              # Tests unitaires
├── theme_settings.py     # Paramètres de thèmes
├── themes.py             # Système de thèmes Windows 11
├── ui_components.py      # Composants d'interface
└── utils.py              # Utilitaires

📁 Racine/
├── .gitignore            # Exclusions Git
├── README.md             # Documentation principale
├── GUIDE.md              # Guide utilisateur
├── MODES.md              # Guide des modes
├── requirements.txt      # Dépendances Python
├── cartes.db            # Base de données SQLite
├── app_final.py         # Application complète
├── app_simple.py        # Version simplifiée
├── app_text_icons.py    # Version icônes texte
├── test*.py             # Scripts de test
├── START.bat            # Lanceur principal
├── launch*.bat          # Lanceurs alternatifs
├── run*.bat             # Scripts d'exécution
└── build.bat            # Script de build
```

## Workflow Git

### Commandes utiles

```bash
# Vérifier l'état
git status

# Voir les modifications
git diff

# Ajouter des modifications
git add .
git add fichier_specifique.py

# Créer un commit
git commit -m "Description des changements"

# Voir l'historique
git log --oneline
git log --graph --oneline

# Voir les détails d'un commit
git show 93200ef
```

### Convention de commits

Utilisez des messages clairs et descriptifs :

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `refactor:` Refactorisation sans changement de fonctionnalité
- `docs:` Mise à jour de documentation
- `style:` Changements de style/interface
- `test:` Ajout ou modification de tests
- `build:` Changements liés au build

**Exemples :**
```
feat: Ajout du système de tri des cartes
fix: Correction bug affichage images dans le mode sombre
refactor: Modularisation du système d'export Lua
style: Amélioration de l'interface des boutons
docs: Mise à jour du guide utilisateur
```

## Sauvegardes automatiques

Le `.gitignore` est configuré pour exclure :
- ✅ Environnements virtuels (`venv/`, `.env/`)
- ✅ Cache Python (`__pycache__/`, `*.pyc`)
- ✅ Builds (`build/`, `dist/`)
- ✅ Logs (`*.log`)
- ✅ Fichiers système (`.DS_Store`, `Thumbs.db`)

⚠️ **Note :** La base de données `cartes.db` EST incluse pour conserver les données de test.

## Prochaines étapes recommandées

1. **Branches de développement :**
   ```bash
   git checkout -b feature/nouvelle-fonctionnalite
   git checkout -b hotfix/correction-urgente
   ```

2. **Tags pour versions :**
   ```bash
   git tag -a v1.0.0 -m "Version 1.0.0 - Release initiale"
   ```

3. **Dépôt distant (optionnel) :**
   ```bash
   git remote add origin https://github.com/username/carte-editor.git
   git push -u origin master
   ```

## Historique des modifications majeures

- **v1.0.0 (Initial)** - Éditeur modulaire complet avec thèmes Windows 11
  - Architecture modulaire avec package `lib/`
  - Système de thèmes adaptatif
  - Prévisualisation d'images avec fusion de templates
  - Interface complète et documentation

---

*Fichier généré automatiquement lors de l'initialisation Git*
