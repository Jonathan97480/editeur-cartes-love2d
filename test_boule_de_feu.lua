-- Carte: Boule de Feu
local card = {
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
}

return card
