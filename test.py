#!/usr/bin/env python3
"""
Point d'entrée principal pour l'éditeur de cartes Love2D
"""

# Import et lancement de l'application finale
if __name__ == '__main__':
    try:
        from app_final import main
        main()
    except Exception as e:
        print(f"Erreur lors du lancement : {e}")
        import traceback
        traceback.print_exc()
        
        # Pause pour voir l'erreur
        input("Appuyez sur Entrée pour fermer...")