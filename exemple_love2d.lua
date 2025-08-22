-- Exemple d'utilisation Love2D pour les cartes avec formatage
-- Placez ce code dans votre projet Love2D

local cards = require("test_all_cards_formatted")

-- Fonction utilitaire pour convertir couleur hexadécimale
function hexToRgb(hex)
    hex = hex:gsub("#", "")
    local r = tonumber("0x" .. hex:sub(1, 2)) / 255
    local g = tonumber("0x" .. hex:sub(3, 4)) / 255
    local b = tonumber("0x" .. hex:sub(5, 6)) / 255
    return r, g, b, 1
end

-- Classe pour afficher une carte
local Card = {}
Card.__index = Card

function Card:new(cardData)
    local obj = {}
    setmetatable(obj, Card)

    obj.data = cardData
    obj.formatting = cardData.formatting

    -- Charger les polices
    obj.titleFont = love.graphics.newFont(obj.formatting.title.font, obj.formatting.title.size)
    obj.textFont = love.graphics.newFont(obj.formatting.text.font, obj.formatting.text.size)

    return obj
end

function Card:draw(x, y)
    love.graphics.push()
    love.graphics.translate(x, y)

    -- Dessiner le fond de carte (exemple)
    love.graphics.setColor(0.9, 0.9, 0.9, 1)
    love.graphics.rectangle("fill", 0, 0, 250, 350)
    love.graphics.setColor(0, 0, 0, 1)
    love.graphics.rectangle("line", 0, 0, 250, 350)

    -- Afficher le titre
    love.graphics.setFont(self.titleFont)
    love.graphics.setColor(hexToRgb(self.formatting.title.color))
    love.graphics.print(
        self.data.nom,
        self.formatting.title.x,
        self.formatting.title.y
    )

    -- Afficher le type et coût
    love.graphics.setFont(self.textFont)
    love.graphics.setColor(0.3, 0.3, 0.3, 1)
    love.graphics.print(
        string.format("%s - Coût: %d", self.data.type, self.data.cout),
        self.formatting.title.x,
        self.formatting.title.y + self.formatting.title.size + 5
    )

    -- Afficher la description avec formatage
    love.graphics.setFont(self.textFont)
    love.graphics.setColor(hexToRgb(self.formatting.text.color))
    love.graphics.printf(
        self.data.description,
        self.formatting.text.x,
        self.formatting.text.y,
        self.formatting.text.width,
        self.formatting.text.align
    )

    -- Afficher la rareté en bas
    love.graphics.setColor(0.5, 0.5, 0.5, 1)
    love.graphics.print(
        self.data.rarete,
        self.formatting.text.x,
        320
    )

    love.graphics.pop()
end

-- Exemple d'utilisation dans love.load()
function love.load()
    -- Charger toutes les cartes
    gameCards = {}
    for i, cardData in ipairs(cards) do
        gameCards[i] = Card:new(cardData)
    end

    currentCard = 1
end

-- Exemple d'affichage dans love.draw()
function love.draw()
    if gameCards and gameCards[currentCard] then
        -- Afficher la carte au centre
        local x = (love.graphics.getWidth() - 250) / 2
        local y = (love.graphics.getHeight() - 350) / 2
        gameCards[currentCard]:draw(x, y)

        -- Instructions
        love.graphics.setColor(1, 1, 1, 1)
        love.graphics.print("Utilisez les flèches pour naviguer", 10, 10)
        love.graphics.print(string.format("Carte %d/%d", currentCard, #gameCards), 10, 30)
    end
end

-- Navigation entre cartes
function love.keypressed(key)
    if key == "right" and currentCard < #gameCards then
        currentCard = currentCard + 1
    elseif key == "left" and currentCard > 1 then
        currentCard = currentCard - 1
    end
end
