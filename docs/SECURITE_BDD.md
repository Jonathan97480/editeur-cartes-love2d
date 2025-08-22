# Système de Sécurité et Migration de Base de Données

## Vue d'ensemble

L'éditeur de cartes Love2D intègre désormais un système complet de vérification et migration automatique de la base de données. Ce système garantit l'intégrité et la compatibilité des données lors des mises à jour de l'application.

## Fonctionnalités

### 🔒 Sécurité au Démarrage

À chaque lancement, l'application :

1. **Vérifie la version** de la base de données
2. **Contrôle l'intégrité** des données 
3. **Applique les migrations** nécessaires automatiquement
4. **Sauvegarde automatiquement** avant toute migration
5. **Valide le schéma** de la table

### 📈 Système de Versions

- **Version 1** : Schéma de base (ancienne version)
- **Version 2** : Ajout colonnes `rarity` et `types_json`
- **Version 3** : Validation et nettoyage des données (actuelle)

### 🛠️ Migrations Automatiques

#### Migration v1 → v2
- Ajout de la colonne `rarity` (par défaut : 'commun')
- Ajout de la colonne `types_json` (par défaut : '[]')

#### Migration v2 → v3
- Validation des raretés (correction vers 'commun' si invalide)
- Vérification du format JSON des colonnes
- Correction des timestamps manquants
- Nettoyage des données corrompues

### 💾 Sauvegardes Automatiques

Avant chaque migration, une sauvegarde est créée :
```
cartes.db.backup.YYYYMMDD_HHMMSS
```

## Utilisation

### Démarrage Normal

L'application vérifie automatiquement la base de données :

```bash
python app_final.py
```

Sortie typique :
```
🚀 Démarrage de l'éditeur de cartes Love2D...
==================================================
🚀 Vérification et migration de la base de données...
📊 Version actuelle : 3
📊 Version cible : 3
✅ Base de données à jour
✅ Intégrité de la base de données vérifiée
✅ Base de données initialisée et vérifiée
==================================================
```

### Outils de Diagnostic

#### Test de Migration
```bash
python test_migration.py
```

#### Diagnostic Complet
```bash
python db_tools.py --diagnose
```

#### Migration Forcée
```bash
python db_tools.py --migrate
```

#### Sauvegarde Manuelle
```bash
python db_tools.py --backup
```

#### Toutes les Opérations
```bash
python db_tools.py --all
```

## Gestion des Erreurs

### Mode de Récupération

Si la migration échoue, l'application propose :

1. **Mode legacy** : Utilise l'ancien système (temporaire)
2. **Arrêt sécurisé** : Préserve les données existantes

### Messages d'Erreur

L'application affiche des messages clairs :
- ✅ Succès avec émojis verts
- ⚠️ Avertissements avec émojis orange  
- ❌ Erreurs avec émojis rouges
- 🔧 Actions de réparation

## Structure des Fichiers

```
lib/
├── database.py              # Repository et modèles
├── database_migration.py    # Système de migration
└── config.py               # Configuration

db_tools.py                 # Outils de maintenance
test_migration.py          # Tests de migration
cartes.db                  # Base de données principale
cartes.db.backup.*         # Sauvegardes automatiques
```

## Schéma de Base de Données

### Table `cards`
```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    side TEXT NOT NULL CHECK(side IN ('joueur','ia')),
    name TEXT NOT NULL,
    img TEXT NOT NULL,
    description TEXT NOT NULL,
    powerblow INTEGER NOT NULL DEFAULT 0,
    rarity TEXT NOT NULL DEFAULT 'commun',
    types_json TEXT NOT NULL DEFAULT '[]',
    hero_json TEXT NOT NULL,
    enemy_json TEXT NOT NULL,
    action TEXT NOT NULL,
    action_param TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### Table `db_version` (système)
```sql
CREATE TABLE db_version (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version INTEGER NOT NULL,
    updated_at TEXT NOT NULL
);
```

## Bonnes Pratiques

### Pour les Utilisateurs

1. **Laissez la migration se faire** automatiquement
2. **Ne supprimez pas** les fichiers de sauvegarde
3. **Utilisez les outils de diagnostic** en cas de problème
4. **Signalez les erreurs** avec les logs complets

### Pour les Développeurs

1. **Incrémentez `CURRENT_DB_VERSION`** pour chaque changement de schéma
2. **Créez une fonction `migrate_vX_to_vY`** pour chaque migration
3. **Testez la migration** sur des données réelles
4. **Documentez les changements** dans ce fichier

## Récupération de Données

### En cas de Corruption

1. **Arrêtez l'application**
2. **Restaurez une sauvegarde** :
   ```bash
   copy cartes.db.backup.YYYYMMDD_HHMMSS cartes.db
   ```
3. **Relancez l'application**

### En cas de Migration Échouée

1. **Vérifiez les logs** d'erreur
2. **Utilisez le diagnostic** :
   ```bash
   python db_tools.py --diagnose
   ```
3. **Forcez la migration** si nécessaire :
   ```bash
   python db_tools.py --migrate
   ```

## Évolutions Futures

### Version 4 (Planifiée)
- Compression des images en base
- Métadonnées étendues
- Support multi-utilisateurs

### Version 5 (Planifiée)
- Chiffrement des données sensibles
- Synchronisation cloud
- Historique complet des modifications

## Support

En cas de problème :

1. **Collectez les informations** :
   ```bash
   python db_tools.py --diagnose > diagnostic.txt
   ```

2. **Incluez les logs** d'erreur complets

3. **Mentionnez votre version** Python et OS

4. **Joignez une sauvegarde** de test si possible

---

*Ce système garantit la robustesse et l'évolutivité de vos données de cartes Love2D.*
