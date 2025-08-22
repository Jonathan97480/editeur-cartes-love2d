# 🎮 Guide Love2D - Utilisation des cartes avec formatage complet

## 🎯 PROBLÈME RÉSOLU !

Votre fichier `cards_joueur.lua` exporté par l'application manquait :
- ❌ La taille des cartes
- ❌ Les informations de formatage de texte

**✅ MAINTENANT IL CONTIENT TOUT :**
- 📐 Dimensions de carte : 280×392 pixels (ratio 5:7)
- 📍 Positions précises pour titre, description, énergie
- 🎨 Styles complets (police, taille, couleur)
- 🎮 Structure 100% compatible Love2D

## 📋 Structure du fichier

Chaque carte contient maintenant une section `TextFormatting` :

```lua
TextFormatting = {
    card = {
        width = 280,  -- Largeur de carte
        height = 392, -- Hauteur de carte
        scale = 1.0   -- Échelle
    },
    title = {
        x = 50,           -- Position X
        y = 25,           -- Position Y
        font = "Arial",   -- Police
        size = 16,        -- Taille
        color = "black"   -- Couleur
    },
    description = {
        x = 20,           -- Position X
        y = 80,           -- Position Y
        width = 240,      -- Largeur zone
        height = 200,     -- Hauteur zone
        font = "Arial",   -- Police
        size = 12,        -- Taille
        color = "black"   -- Couleur
    },
    energy = {
        x = 240,          -- Position X
        y = 25,           -- Position Y
        font = "Arial",   -- Police
        size = 14,        -- Taille
        color = "blue"    -- Couleur
    }
}
```

## 🎮 Code Love2D pour utiliser les cartes

### 1. Charger les cartes
```lua
local cards = require("cards_joueur")

function love.load()
    -- Les cartes sont maintenant disponibles avec formatage
    print("Cartes chargées:", #cards)
    
    -- Exemple d'accès aux données
    local firstCard = cards[1]
    print("Nom:", firstCard.name)
    print("Largeur carte:", firstCard.TextFormatting.card.width)
    print("Hauteur carte:", firstCard.TextFormatting.card.height)
end
```

### 2. Dessiner une carte
```lua
function drawCard(card, x, y)
    local fmt = card.TextFormatting
    
    -- Fond de carte
    love.graphics.setColor(1, 1, 1)
    love.graphics.rectangle("fill", x, y, fmt.card.width, fmt.card.height)
    love.graphics.setColor(0, 0, 0)
    love.graphics.rectangle("line", x, y, fmt.card.width, fmt.card.height)
    
    -- Titre
    love.graphics.setColor(0, 0, 0) -- noir
    love.graphics.print(card.name, 
                       x + fmt.title.x, 
                       y + fmt.title.y)
    
    -- Description (avec retour à la ligne)
    love.graphics.printf(card.Description, 
                        x + fmt.description.x, 
                        y + fmt.description.y, 
                        fmt.description.width)
    
    -- Énergie/Coût
    love.graphics.setColor(0, 0, 1) -- bleu
    love.graphics.print(card.PowerBlow, 
                       x + fmt.energy.x, 
                       y + fmt.energy.y)
end
```

### 3. Dessiner avec mise à l'échelle
```lua
function drawCardScaled(card, x, y, scale)
    scale = scale or card.TextFormatting.card.scale
    
    love.graphics.push()
    love.graphics.translate(x, y)
    love.graphics.scale(scale, scale)
    
    drawCard(card, 0, 0)
    
    love.graphics.pop()
end
```

### 4. Exemple complet
```lua
local cards = require("cards_joueur")

function love.load()
    selectedCard = cards[1] -- Première carte
end

function love.draw()
    -- Dessiner la carte au centre de l'écran
    local screenW = love.graphics.getWidth()
    local screenH = love.graphics.getHeight()
    
    local cardW = selectedCard.TextFormatting.card.width
    local cardH = selectedCard.TextFormatting.card.height
    
    local x = (screenW - cardW) / 2
    local y = (screenH - cardH) / 2
    
    drawCard(selectedCard, x, y)
end

function love.keypressed(key)
    if key == "space" then
        -- Changer de carte
        local currentIndex = 1
        for i, card in ipairs(cards) do
            if card == selectedCard then
                currentIndex = i
                break
            end
        end
        
        currentIndex = currentIndex + 1
        if currentIndex > #cards then
            currentIndex = 1
        end
        
        selectedCard = cards[currentIndex]
    end
end
```

## 📁 Fichiers créés

- `cards_joueur.lua` - **Fichier principal complet** (26,925 caractères)
- `cards_joueur_original_backup.lua` - Sauvegarde de l'original (12,575 caractères)

## 🎉 Votre projet Love2D est maintenant prêt !

Toutes les informations nécessaires pour positionner et styliser vos cartes sont maintenant dans le fichier `cards_joueur.lua`. Plus besoin de deviner les positions - tout est défini précisément !

**Ratio de carte parfait : 280×392 pixels (5:7)**
