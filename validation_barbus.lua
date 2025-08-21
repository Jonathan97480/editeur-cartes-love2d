local Cards = {
    --[[ CARTE 1 - 🎭 Barbus ]]
    {
        name = 'Carte Test Multi-Acteurs',
        ImgIlustration = 'test.png',
        Description = 'Test de liaison multiple',
        PowerBlow = 3,
        Rarete = 'commun',
        Type = {},
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 2 - 🎭 Barbus ]]
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
    },

    --[[ CARTE 3 - 🎭 Barbus ]]
    {
        name = 'test 5',
        ImgIlustration = 'images/originals/test_5.png',
        Description = 'gjhgjh',
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

    --[[ CARTE 4 - 🎭 Barbus ]]
    {
        name = 'trtrtt',
        ImgIlustration = 'images/cards/trtrtt.png',
        Description = 'jhkhljkjh',
        PowerBlow = 1,
        Rarete = 'commun',
        Type = {},
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 5 - 🎭 Barbus ]]
    {
        name = 'Test Liaison Acteur',
        ImgIlustration = 'images/cards/Test_Liaison_Acteur.png',
        Description = 'Carte créée pour tester les liaisons acteur-carte',
        PowerBlow = 5,
        Rarete = 'commun',
        Type = {},
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 6 - 🎭 Barbus ]]
    {
        name = 'bob2',
        ImgIlustration = 'images/cards/bob2.png',
        Description = 'ijhlkhlkmlkjlkmj',
        PowerBlow = 0,
        Rarete = 'commun',
        Type = { 'attaque', 'defense' },
        Effect = {
            Actor = { heal = 1, shield = 1, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 1, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 1, shield = 1, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function()
                graveyardPioche('les deux souer')
            end
        },
        Cards = {}
    }
}

return Cards
