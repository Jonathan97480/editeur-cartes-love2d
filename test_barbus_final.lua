local Cards = {
    --[[ CARTE 1 - 🎮 Joueur ]]
    {
        name = 'calisse e la mort',
        ImgIlustration = 'images/cards/calisse_e_la_mort.png',
        Description = 'quand le hero bois dans ce caliise lui inflige des dégat mais il gagne en froce',
        PowerBlow = 2,
        Rarete = 'legendaire',
        Type = { 'attaque' },
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 4, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 3, number_turns = 2 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 2 - 🎮 Joueur ]]
    {
        name = 'carte de la coupe',
        ImgIlustration = 'images/cards/carte_de_la_coupe.png',
        Description = 'test',
        PowerBlow = 2,
        Rarete = 'commun',
        Type = { 'attaque', 'soutien' },
        Effect = {
            Actor = { heal = 1, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 3 - 🎮 Joueur ]]
    {
        name = 'Test Intégration',
        ImgIlustration = '',
        Description = 'Carte de test d\'intégration',
        PowerBlow = 0,
        Rarete = 'commun',
        Type = {},
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 4 - 🎮 Joueur ]]
    {
        name = 'Test Intégration',
        ImgIlustration = '',
        Description = 'Carte de test d\'intégration',
        PowerBlow = 0,
        Rarete = 'commun',
        Type = {},
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 5 - 🎮 Joueur ]]
    {
        name = 'Carte Multi-Acteurs Test',
        ImgIlustration = 'multi_test.png',
        Description = 'Test de validation sélection multiple',
        PowerBlow = 7,
        Rarete = 'rare',
        Type = {},
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 6 - 🎮 Joueur ]]
    {
        name = 'Potion de Soin',
        ImgIlustration = 'potion_heal.png',
        Description = 'Restaure 50 HP. Utilisable par tous.',
        PowerBlow = 2,
        Rarete = 'commun',
        Type = {},
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 7 - 🎮 Joueur ]]
    {
        name = 'Équilibrage Cosmique',
        ImgIlustration = 'cosmic_balance.png',
        Description = 'Affecte tous les acteurs du jeu.',
        PowerBlow = 15,
        Rarete = 'mythique',
        Type = {},
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    }
}

return Cards
