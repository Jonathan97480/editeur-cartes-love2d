# Index des fichiers Lua organisés

## Structure créée par le nettoyage automatique

### 📁 lua_tests/
Fichiers Lua de test, validation et développement
- Tous les fichiers `test_*.lua`
- Fichiers de validation et debug
- Scripts temporaires de développement

### 📁 lua_exports/
Exports Lua finaux et exemples d'utilisation
- Exports de cartes pour Love2D
- Fichiers de configuration Love2D
- Exemples d'intégration

### 📁 dev_temp/
Fichiers temporaires et brouillons
- Fichiers générés automatiquement
- Versions de test
- Brouillons de développement

### 📁 lua_backup/
Sauvegardes automatiques des exports
- Versions précédentes des exports
- Sauvegardes de sécurité

## Utilisation

### Pour retrouver un fichier :
1. Fichiers de test → `lua_tests/`
2. Exports finaux → `lua_exports/`
3. Fichiers temporaires → `dev_temp/`

### Pour nettoyer :
```bash
python nettoyer_projet.py
```

### Pour réorganiser :
```bash
python organiser_projet.py
```
