# 🔧 Notes Techniques - Migration v2.3.1

## 📊 Architecture de Migration

### Système de Versioning de Base
```python
# Table db_version
CREATE TABLE db_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL,
    description TEXT
);
```

### Versions et Migrations
- **v1** : Base legacy sans `rarity`, `types_json`, `original_img`
- **v2** : Ajout `rarity` et `types_json`
- **v3** : Validation et nettoyage des données
- **v4** : Import automatique des templates configurés
- **v5** : Ajout `original_img` + initialisation depuis `img`

## 🔄 Flux de Migration

### Détection Automatique
```python
def get_db_version(db_path: str) -> int:
    # 1. Vérifier si table db_version existe
    # 2. Si oui, retourner version actuelle
    # 3. Si non, analyser schéma pour détecter version legacy
```

### Migration Progressive
```python
def migrate_database(db_path: str) -> bool:
    current_version = get_db_version(db_path)
    
    # Sauvegarde automatique
    backup_path = f"{db_path}.backup.{timestamp}"
    shutil.copy2(db_path, backup_path)
    
    # Appliquer migrations séquentiellement
    if current_version < 2: migrate_v1_to_v2(db_path)
    if current_version < 3: migrate_v2_to_v3(db_path)
    if current_version < 4: migrate_v3_to_v4(db_path)
    if current_version < 5: migrate_v4_to_v5(db_path)
```

## 🛠️ Correction du Bug Templates

### Problème Original
```python
# ❌ Code bugué (avant v2.3.1)
def generate_card_image(self):
    # Utilisait self.img qui contenait déjà un template fusionné
    source_image = self.img  # ERREUR !
    template = get_template(self.rarity)
    result = fuse_images(source_image, template)
    self.img = result  # Superposition !
```

### Solution Implémentée
```python
# ✅ Code corrigé (v2.3.1)
def generate_card_image(self):
    # Utilise toujours l'image originale comme source
    source_image = self._original_image_path or self.img
    template = get_template(self.rarity)
    result = fuse_images(source_image, template)
    self.img = result  # Fusion propre
    
    # Préserver la référence originale
    if not hasattr(self, '_original_image_path'):
        self._original_image_path = source_image
```

### Modèle de Données
```python
class Card:
    def __init__(self, row=None):
        self.img = ''          # Image fusionnée (affichage)
        self.original_img = '' # Image originale (source)
        
    def from_row(self, row):
        # Gestion du fallback pour compatibilité
        if 'original_img' in row.keys() and row['original_img']:
            self.original_img = row['original_img']
        else:
            self.original_img = row['img']  # Fallback
```

## 🧪 Tests de Validation

### Scénarios Testés
1. **Migration Base Legacy**
   ```python
   # Base v1 sans original_img
   # → Migration automatique vers v5
   # → original_img initialisé depuis img
   ```

2. **Changements Rareté Multiples**
   ```python
   # Commun → Rare → Légendaire → Mythique
   # Vérification : Pas de superposition
   ```

3. **Utilisateur GitHub**
   ```python
   # Base existante + Clone repo + Premier lancement
   # → Migration transparente
   # → Données préservées
   ```

### Tests Automatisés
- **`test_github_migration.py`** : Base legacy → Migration v5
- **`test_scenario_github.py`** : Scénario utilisateur complet
- **`verify_db_protection.py`** : Exclusion Git

## 🔒 Sécurité et Robustesse

### Protection des Données
```python
def ensure_db_with_migration(db_path: str) -> bool:
    try:
        # 1. Sauvegarde automatique
        backup_path = create_backup(db_path)
        
        # 2. Migration progressive
        success = migrate_database(db_path)
        
        # 3. Vérification intégrité
        if not verify_database_integrity(db_path):
            restore_from_backup(backup_path)
            return False
            
        return True
    except Exception as e:
        rollback_migration(db_path, backup_path)
        raise
```

### Exclusion Git
```gitignore
# Base de données (données utilisateur)
cartes.db
*.db
*.db.backup.*

# Exclusion explicite
cartes.db
```

## 📋 Points d'Attention

### Compatibilité Ascendante
- ✅ **Fallback intelligent** : `original_img` → `img` si absent
- ✅ **Migration transparente** : Aucune action utilisateur
- ✅ **Données préservées** : Aucune perte d'information

### Performance
- ✅ **Migration rapide** : Ajout de colonne + UPDATE simple
- ✅ **Sauvegarde efficace** : Copy file system
- ✅ **Validation légère** : PRAGMA integrity_check

### Surveillance
```python
# Logging des opérations critiques
print("🔄 Migration v4 → v5 : Ajout du champ original_img...")
print(f"   ✅ Colonne original_img ajoutée et {count} cartes initialisées")
```

## 🎯 Résultat Technique

### Avant v2.3.1
- **Image source** = **Image affichage** (même champ)
- **Fusion successive** = **Superposition accumulée**
- **Migration manuelle** ou **perte de données**

### Après v2.3.1
- **Image source** ≠ **Image affichage** (champs séparés)
- **Fusion propre** = **Toujours depuis original**
- **Migration automatique** + **Sauvegarde sécurisée**

**🎉 Architecture robuste et évolutive pour le futur !**
