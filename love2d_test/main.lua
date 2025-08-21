function love.load()
    cards = require('cards')
    print('Nombre de cartes chargées:', #cards)
    
    for i, card in ipairs(cards) do
        print('Carte ' .. i .. ': ' .. card.name)
        -- Vérifier l'image
        if love.filesystem.getInfo(card.ImgIlustration) then
            print('  Image OK: ' .. card.ImgIlustration)
        else
            print('  Image MANQUANTE: ' .. card.ImgIlustration)
        end
    end
end

function love.draw()
    love.graphics.print('Test de chargement des cartes - voir console', 10, 10)
end
