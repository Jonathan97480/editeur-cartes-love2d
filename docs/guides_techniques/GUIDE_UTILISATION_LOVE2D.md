# 🎮 Guide d'utilisation Love2D - Export de cartes complet

## 📋 Structure du fichier cards_joueur.lua

Votre fichier contient maintenant **TOUT** ce qu'il faut pour Love2D :

### 📐 Dimensions de carte
```lua
TextFormatting = {
    card = {
        width = 280,  -- Largeur standard
        height = 392, -- Hauteur standard (ratio 5:7)
        scale = 1.0   -- Facteur d'échelle
    },
```

### 📍 Positionnement précis
```lua
title = {
    x = 50,           -- Position X du titre
    y = 25,           -- Position Y du titre
    font = "Arial",   -- Police
    size = 16,        -- Taille
    color = "black"   -- Couleur
},
description = {
    x = 20,           -- Position X du texte
    y = 80,           -- Position Y du texte
    width = 240,      -- Largeur de la zone
    height = 200,     -- Hauteur de la zone
    font = "Arial",   -- Police
    size = 12,        -- Taille
    color = "black"   -- Couleur
},
energy = {
    x = 240,          -- Position X de l'énergie
    y = 25,           -- Position Y de l'énergie
    font = "Arial",   -- Police
    size = 14,        -- Taille
    color = "blue"    -- Couleur
}
```

## 🎯 Utilisation dans Love2D

### 1. Charger les cartes
```lua
local cards = require("cards_joueur")

-- Accéder aux données
for i, card in ipairs(cards) do
    local name = card.name
    local formatting = card.TextFormatting
    
    -- Dimensions de la carte
    local cardWidth = formatting.card.width
    local cardHeight = formatting.card.height
    
    -- Position du titre
    local titleX = formatting.title.x
    local titleY = formatting.title.y
end
```

### 2. Afficher une carte
```lua
function drawCard(card, x, y)
    local format = card.TextFormatting
    
    -- Fond de carte
    love.graphics.rectangle("fill", x, y, format.card.width, format.card.height)
    
    -- Titre
    love.graphics.setFont(love.graphics.newFont(format.title.size))
    love.graphics.print(card.name, x + format.title.x, y + format.title.y)
    
    -- Description
    love.graphics.setFont(love.graphics.newFont(format.description.size))
    love.graphics.printf(card.Description, 
                        x + format.description.x, 
                        y + format.description.y, 
                        format.description.width)
    
    -- Énergie
    love.graphics.setFont(love.graphics.newFont(format.energy.size))
    love.graphics.print(card.PowerBlow, x + format.energy.x, y + format.energy.y)
end
```

### 3. Mise à l'échelle
```lua
function drawCardScaled(card, x, y, scale)
    local format = card.TextFormatting
    scale = scale or format.card.scale
    
    love.graphics.push()
    love.graphics.translate(x, y)
    love.graphics.scale(scale, scale)
    
    -- Dessiner normalement
    drawCard(card, 0, 0)
    
    love.graphics.pop()
end
```

## ✅ Tout est prêt !

- **📐 Taille de carte** : 280x392 pixels (ratio parfait 5:7)
- **📍 Positions** : Calculées pour un rendu optimal
- **🎨 Styles** : Police, taille, couleur pour chaque élément
- **🎮 Love2D** : Structure 100% compatible

**Votre export Lua est maintenant COMPLET !** 🎉
