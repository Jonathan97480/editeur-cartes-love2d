# 🎨 Outils de Développement - Polices

Ce dossier contient les outils de développement pour le système de polices personnalisées.

## Scripts disponibles

### test_font_manager.py
Script de test du gestionnaire de polices

**Usage :**
```bash
python dev/polices/test_font_manager.py
```

### install_fonts.py
Installateur de polices interactif

**Usage :**
```bash
python dev/polices/install_fonts.py
```

### test_editor_fonts.py
Test de l'éditeur avec polices personnalisées

**Usage :**
```bash
python dev/polices/test_editor_fonts.py
```

## Architecture du système de polices

### Composants principaux :
- **`lib/font_manager.py`** : Gestionnaire principal des polices
- **`lib/text_formatting_editor.py`** : Éditeur intégré avec support polices
- **`fonts/`** : Dossier de stockage des polices personnalisées

### Structure des polices :
```
fonts/
├── titre/          # Polices pour les titres
├── texte/          # Polices pour le texte principal  
├── special/        # Polices décoratives
└── README.md       # Documentation utilisateur
```

### Intégration :
Le système de polices est automatiquement intégré dans :
- L'éditeur de formatage de texte
- L'exporteur Love2D (à venir)
- L'aperçu en temps réel

## Installation de nouvelles polices

1. **Via l'installateur :**
   ```bash
   python dev/polices/install_fonts.py
   ```

2. **Manuellement :**
   - Copiez les fichiers .ttf/.otf dans fonts/
   - Redémarrez l'application
   - Utilisez "🎨 Actualiser polices" dans l'éditeur

## Tests et validation

- **`test_font_manager.py`** : Test du gestionnaire de base
- **`test_editor_fonts.py`** : Test d'intégration complète

Ces scripts valident que le système fonctionne correctement.
