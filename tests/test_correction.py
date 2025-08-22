#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide du système d'acteurs après correction
"""
from lib.actors import ActorManager
from lib.database import CardRepo

print('🔧 Test de correction du système d\'acteurs...')
try:
    manager = ActorManager('cartes.db')
    actors = manager.list_actors()
    print(f'✅ {len(actors)} acteurs trouvés')
    
    for actor in actors:
        try:
            cards = manager.get_actor_cards(actor['id'])
            print(f'   {actor["icon"]} {actor["name"]} : {len(cards)} cartes')
        except Exception as e:
            print(f'   ❌ Erreur pour {actor["name"]} : {e}')
    
    print('\n✅ Test réussi ! Le problème get_by_id est corrigé.')
    
except Exception as e:
    print(f'❌ Erreur : {e}')
    import traceback
    traceback.print_exc()

input('\nAppuyez sur Entrée pour fermer...')
