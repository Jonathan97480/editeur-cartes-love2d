# 🎮 Package de Cartes Love2D

## Description
Package complet de cartes pour Love2D

**Version:** 1.0.0
**Créé par:** Editeur de Cartes
**Compatible Love2D:** 11.4+

## Structure du Package

```
📁 mon_jeu_cartes_temp/
├── 📁 cards/               # Images fusionnées des cartes
├── 📁 fonts/               # Polices utilisées
├── 📄 cards_data.lua       # Données des cartes
├── 📄 package_config.json  # Configuration du package
└── 📄 README.md           # Cette documentation
```

## Statistiques

- **Cartes:** 10
- **Polices:** 1
- **Images:** 20

## Utilisation dans Love2D

### 1. Charger les données des cartes
```lua
local cards = require("cards_data")

-- Accéder aux cartes
for i, card in ipairs(cards) do
    print("Carte:", card.name)
    print("Coût:", card.PowerBlow)
    print("Description:", card.Description)
end
```

### 2. Utiliser les polices
```lua
-- Les polices sont dans le dossier fonts/
local titleFont = love.graphics.newFont("fonts/ma_police.ttf", 16)
```

### 3. Charger les images
```lua
-- Les images fusionnées sont dans le dossier cards/
local cardImage = love.graphics.newImage("cards/carte_001.png")
```

### 4. Formatage de texte
Chaque carte contient une section `TextFormatting` avec:
- Position et style du titre
- Position et zone de texte de description
- Position et style du coût d'énergie
- Dimensions de la carte

## Exemple d'utilisation complète

```lua
local cards = require("cards_data")

function love.load()
    -- Charger une carte
    local card = cards[1]
    
    -- Charger l'image fusionnée
    card.image = love.graphics.newImage("cards/carte_001.png")
    
    -- Charger les polices si nécessaire
    if card.TextFormatting.title.font ~= "Arial" then
        card.titleFont = love.graphics.newFont("fonts/" .. card.TextFormatting.title.font .. ".ttf", 
                                             card.TextFormatting.title.size)
    end
end

function love.draw()
    local card = cards[1]
    
    -- Dessiner l'image de la carte
    love.graphics.draw(card.image, 100, 100)
    
    -- Ou utiliser les données de formatage pour dessiner séparément
    local fmt = card.TextFormatting
    love.graphics.setColor(1, 1, 1) -- Blanc
    love.graphics.printf(card.name, 
                        100 + fmt.title.x, 100 + fmt.title.y, 
                        fmt.card.width, "center")
end
```

## Notes

- Les images fusionnées incluent déjà le texte rendu
- Utilisez les données TextFormatting pour un contrôle précis
- Toutes les polices utilisées sont incluses dans le package
- Compatible avec Love2D 11.4 et versions ultérieures

---
*Généré automatiquement par l'Éditeur de Cartes*
