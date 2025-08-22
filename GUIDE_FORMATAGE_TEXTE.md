# 📝 Guide d'utilisation du Formatage de Texte

## 🎯 Vue d'ensemble

Le système de formatage de texte vous permet de positionner précisément le titre et la description de vos cartes pour Love2D, avec un contrôle total sur :
- **Position** (X, Y) du titre et du texte
- **Police et taille** de caractères  
- **Couleurs** personnalisées
- **Alignement** du texte (gauche, centre, droite, justifié)
- **Retour à la ligne** automatique
- **Espacement** entre les lignes

## 🚀 Démarrage rapide

### 1. Lancer l'éditeur simple
```bash
python test_simple.py
```

### 2. Ouvrir l'éditeur de formatage
- Sélectionnez une carte dans la liste
- Cliquez sur le bouton **"📝 Formatage"**
- L'éditeur visuel s'ouvre avec un aperçu de la carte

### 3. Ajuster le formatage
- **Zone Titre** : Cliquez-glissez pour positionner le titre
- **Zone Texte** : Redimensionnez et déplacez la zone de description
- **Contrôles** : Modifiez police, taille, couleur dans le panneau de droite
- **Aperçu temps réel** : Voyez les changements instantanément

### 4. Sauvegarder et exporter
- Cliquez **"💾 Sauvegarder"** pour enregistrer en base
- Utilisez **"📤 Exporter Lua"** pour générer le fichier Love2D

## 🎨 Interface de l'éditeur de formatage

### Canvas de prévisualisation
- **Rectangle rouge** : Zone du titre (déplaçable)
- **Rectangle bleu** : Zone du texte (redimensionnable)
- **Aperçu en temps réel** : Texte avec police et couleur appliquées

### Panneau de contrôles

#### 📍 Position du Titre
- **X, Y** : Coordonnées exactes du titre
- **Police** : Sélection dans la liste des polices système
- **Taille** : Taille en pixels (8-72)
- **Couleur** : Sélecteur de couleur visuel

#### 📄 Zone de Texte  
- **Position X, Y** : Coin supérieur gauche
- **Largeur, Hauteur** : Dimensions de la zone
- **Police** : Police pour la description
- **Taille** : Taille du texte
- **Couleur** : Couleur du texte
- **Alignement** : Gauche, Centre, Droite, Justifié
- **Espacement** : Interligne (0.8 à 2.0)
- **Retour ligne** : Activation/désactivation

## 📤 Export Love2D

Le système génère du code Lua prêt à utiliser :

```lua
{
    id = 1,
    nom = "Ma Carte",
    type = "Sort",
    formatting = {
        title = {
            x = 80, y = 25,
            font = "Arial Black",
            size = 18,
            color = "#FF4444"
        },
        text = {
            x = 30, y = 120,
            width = 180, height = 120,
            font = "Times New Roman", 
            size = 11,
            color = "#333333",
            align = "justify",
            line_spacing = 1.3,
            wrap = true
        }
    }
}
```

## 🎮 Utilisation dans Love2D

### Affichage du titre
```lua
local card = loadCard(cardId)
local fmt = card.formatting

-- Configurer la police du titre
local titleFont = love.graphics.newFont(fmt.title.font, fmt.title.size)
love.graphics.setFont(titleFont)

-- Couleur du titre (conversion hex vers RGB)
local r, g, b = hexToRgb(fmt.title.color)
love.graphics.setColor(r, g, b)

-- Afficher le titre
love.graphics.print(card.nom, fmt.title.x, fmt.title.y)
```

### Affichage du texte
```lua
-- Police du texte
local textFont = love.graphics.newFont(fmt.text.font, fmt.text.size)
love.graphics.setFont(textFont)

-- Couleur du texte
local r, g, b = hexToRgb(fmt.text.color)
love.graphics.setColor(r, g, b)

-- Texte avec retour à la ligne automatique
love.graphics.printf(
    card.description,
    fmt.text.x,
    fmt.text.y, 
    fmt.text.width,
    fmt.text.align
)
```

### Fonction utilitaire couleur
```lua
function hexToRgb(hex)
    hex = hex:gsub("#", "")
    return tonumber("0x" .. hex:sub(1,2))/255,
           tonumber("0x" .. hex:sub(3,4))/255,
           tonumber("0x" .. hex:sub(5,6))/255
end
```

## 🗃️ Structure de la base de données

Le formatage est stocké directement dans la table `cards` :

```sql
-- Champs du titre
title_x INTEGER DEFAULT 50,
title_y INTEGER DEFAULT 30, 
title_font TEXT DEFAULT 'Arial',
title_size INTEGER DEFAULT 16,
title_color TEXT DEFAULT '#000000',

-- Champs du texte
text_x INTEGER DEFAULT 50,
text_y INTEGER DEFAULT 100,
text_width INTEGER DEFAULT 200,
text_height INTEGER DEFAULT 150,
text_font TEXT DEFAULT 'Arial',
text_size INTEGER DEFAULT 12,
text_color TEXT DEFAULT '#000000',
text_align TEXT DEFAULT 'left',
line_spacing REAL DEFAULT 1.2,
text_wrap INTEGER DEFAULT 1
```

## 🛠️ Scripts de test

- **`test_simple.py`** : Interface complète avec éditeur
- **`test_formatter.py`** : Test de l'éditeur de formatage
- **`test_complete_system.py`** : Démonstration complète du workflow
- **`test_boule_de_feu.lua`** : Exemple d'export Lua généré

## 💡 Conseils d'utilisation

### Polices recommandées
- **Titres** : Arial Black, Impact, Trebuchet MS
- **Texte** : Arial, Times New Roman, Verdana
- **Fantaisie** : Comic Sans MS, Papyrus (avec modération !)

### Positionnement optimal
- **Titre** : Proche du haut (Y: 20-40)
- **Texte** : Milieu de carte (Y: 100-150)  
- **Marges** : Laissez 20-30px de bordure

### Couleurs efficaces
- **Titre** : Couleurs vives (#FF4444, #4444FF)
- **Texte** : Couleurs sombres (#333333, #000000)
- **Contraste** : Assurez-vous de la lisibilité

### Tailles recommandées
- **Titre** : 16-24px selon l'importance
- **Texte** : 10-14px pour la lisibilité
- **Zone texte** : 150-250px de largeur

## 🔧 Dépannage

### L'éditeur ne s'ouvre pas
- Vérifiez que tkinter est installé
- Assurez-vous d'avoir une carte sélectionnée

### Polices non disponibles  
- L'éditeur affiche les polices système disponibles
- En cas d'erreur, Arial sera utilisé par défaut

### Export Lua corrompu
- Vérifiez les caractères spéciaux dans les descriptions
- Le système échappe automatiquement les caractères problématiques

## 📞 Support

En cas de problème, vérifiez :
1. La structure de la base de données (`PRAGMA table_info(cards)`)
2. Les imports des modules (`lib/database_simple.py`, etc.)
3. Les logs d'erreur dans la console

Le système est maintenant complètement opérationnel ! 🎉
