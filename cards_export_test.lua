-- Export des cartes Love2D avec formatage de texte
-- Généré automatiquement - 1 cartes

local cards = {
    -- Carte 1: Carte Test
    {
    id = 1,
    nom = "Carte Test",
    type = "Sorts",
    rarete = "Commun",
    cout = 3,
    description = "Description de test pour formater le texte",
    image_path = "test.png",
    formatting = {
        title = {
            x = 50,
            y = 30,
            font = "Arial",
            size = 16,
            color = "#000000"
        },
        text = {
            x = 50,
            y = 100,
            width = 200,
            height = 150,
            font = "Arial",
            size = 12,
            color = "#000000",
            align = "left",
            line_spacing = 1.2,
            wrap = true
        }
    }
}

}

return cards
