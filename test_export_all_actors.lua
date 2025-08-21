local Cards = {

    --[[ ACTEUR: 🎭 Barbus - 6 cartes ]]
    --[[ CARTE 1 ]]
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

    --[[ CARTE 2 ]]
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

    --[[ CARTE 3 ]]
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

    --[[ CARTE 4 ]]
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

    --[[ CARTE 5 ]]
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

    --[[ CARTE 6 ]]
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
    },

    --[[ ACTEUR: 👹 Boss - 4 cartes ]]
    --[[ CARTE 1 ]]
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

    --[[ CARTE 2 ]]
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

    --[[ CARTE 3 ]]
    {
        name = 'Attaque Coordonnée',
        ImgIlustration = 'coordinated_attack.png',
        Description = 'Les PNJ attaquent ensemble.',
        PowerBlow = 8,
        Rarete = 'rare',
        Type = {},
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 4 ]]
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

    --[[ ACTEUR: 🤖 IA - 4 cartes ]]
    --[[ CARTE 1 ]]
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

    --[[ CARTE 2 ]]
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

    --[[ CARTE 3 ]]
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

    --[[ CARTE 4 ]]
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

    --[[ ACTEUR: 🎮 Joueur - 7 cartes ]]
    --[[ CARTE 1 ]]
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

    --[[ CARTE 2 ]]
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

    --[[ CARTE 3 ]]
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

    --[[ CARTE 4 ]]
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

    --[[ CARTE 5 ]]
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

    --[[ CARTE 6 ]]
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

    --[[ CARTE 7 ]]
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

    --[[ ACTEUR: 🛒 Marchand - 3 cartes ]]
    --[[ CARTE 1 ]]
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

    --[[ CARTE 2 ]]
    {
        name = 'Attaque Coordonnée',
        ImgIlustration = 'coordinated_attack.png',
        Description = 'Les PNJ attaquent ensemble.',
        PowerBlow = 8,
        Rarete = 'rare',
        Type = {},
        Effect = {
            Actor = { heal = 0, shield = 0, Epine = 0, attack = 0, AttackReduction = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            Enemy = { heal = 0, attack = 0, AttackReduction = 0, Epine = 0, shield = 0, shield_pass = 0, bleeding = { value = 0, number_turns = 0 }, force_augmented = { value = 0, number_turns = 0 }, chancePassedTour = 0, energyCostIncrease = 0, energyCostDecrease = 0 },
            action = function() end
        },
        Cards = {}
    },

    --[[ CARTE 3 ]]
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

    --[[ ACTEUR: 👤 PNJ - 1 cartes ]]
    --[[ CARTE 1 ]]
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
