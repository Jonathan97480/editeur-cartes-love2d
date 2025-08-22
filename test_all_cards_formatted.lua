-- Export des cartes Love2D avec formatage de texte
-- Généré automatiquement - 2 cartes

local cards = {
    -- Carte 1: Boule de Feu
    {
    id = 2,
    nom = "Boule de Feu",
    type = "Sort",
    rarete = "Commun",
    cout = 3,
    description = "Inflige 3 dégâts à une cible. Un sort simple mais efficace pour éliminer les créatures faibles.",
    image_path = "boule_de_feu.png",
    formatting = {
        title = {
            x = 80,
            y = 25,
            font = "Arial Black",
            size = 18,
            color = "#FF4444"
        },
        text = {
            x = 30,
            y = 120,
            width = 180,
            height = 120,
            font = "Times New Roman",
            size = 11,
            color = "#333333",
            align = "justify",
            line_spacing = 1.3,
            wrap = true
        }
    }
},

    -- Carte 2: Carte Test
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
