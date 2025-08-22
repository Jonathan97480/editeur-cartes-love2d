#!/usr/bin/env python3
"""
Script de réorganisation des tests dans le dossier tests/
"""

import os
import shutil
import glob
from datetime import datetime

def reorganiser_tests():
    """Déplace tous les fichiers test_*.py vers le dossier tests/"""
    
    print("🗂️ RÉORGANISATION DES TESTS")
    print("=" * 40)
    print(f"📅 {datetime.now().strftime('%d %B %Y à %H:%M')}")
    print()
    
    # Dossier racine et dossier tests
    racine = "."
    dossier_tests = "tests"
    
    # Créer le dossier tests s'il n'existe pas
    if not os.path.exists(dossier_tests):
        os.makedirs(dossier_tests)
        print(f"📁 Dossier {dossier_tests}/ créé")
    
    # Trouver tous les fichiers test_*.py dans la racine
    fichiers_test_racine = glob.glob("test_*.py")
    fichiers_validation = glob.glob("validation*.py")
    fichiers_verification = glob.glob("verification*.py")
    
    # Combiner tous les fichiers de test
    tous_fichiers_test = fichiers_test_racine + fichiers_validation + fichiers_verification
    
    # Exclure test.py (fichier principal)
    tous_fichiers_test = [f for f in tous_fichiers_test if f != "test.py"]
    
    print(f"📊 Fichiers trouvés dans la racine :")
    print(f"   • test_*.py : {len(fichiers_test_racine)} fichiers")
    print(f"   • validation*.py : {len(fichiers_validation)} fichiers") 
    print(f"   • verification*.py : {len(fichiers_verification)} fichiers")
    print(f"   • Total à déplacer : {len(tous_fichiers_test)} fichiers")
    print()
    
    if not tous_fichiers_test:
        print("✅ Aucun fichier à déplacer, organisation déjà correcte !")
        return
    
    deplacements = 0
    echecs = 0
    
    print("🚀 DÉPLACEMENT EN COURS :")
    print("-" * 30)
    
    for fichier in tous_fichiers_test:
        try:
            source = fichier
            destination = os.path.join(dossier_tests, fichier)
            
            # Vérifier si le fichier existe déjà dans tests/
            if os.path.exists(destination):
                print(f"⚠️ {fichier} existe déjà dans tests/ - ignoré")
                continue
            
            # Déplacer le fichier
            shutil.move(source, destination)
            print(f"✅ {fichier} → tests/{fichier}")
            deplacements += 1
            
        except Exception as e:
            print(f"❌ Erreur avec {fichier}: {e}")
            echecs += 1
    
    print()
    print("📊 RÉSULTATS :")
    print("-" * 15)
    print(f"✅ Fichiers déplacés : {deplacements}")
    print(f"❌ Échecs : {echecs}")
    print(f"📁 Destination : {dossier_tests}/")
    
    # Vérifier le contenu final du dossier tests
    tests_finaux = glob.glob(os.path.join(dossier_tests, "*.py"))
    print(f"📈 Total dans tests/ : {len(tests_finaux)} fichiers")
    
    if deplacements > 0:
        print()
        print("🎯 ORGANISATION AMÉLIORÉE !")
        print("✅ Tous les tests sont maintenant dans tests/")
        print("✅ Structure de projet plus propre")
        print("✅ Facilite la maintenance et l'exécution")
        
        print()
        print("📝 PROCHAINES ÉTAPES RECOMMANDÉES :")
        print("1. Vérifier que tous les tests fonctionnent encore")
        print("2. Mettre à jour run_tests.py si nécessaire")
        print("3. Ajouter tests/ dans votre .gitignore si besoin")
    
    return deplacements

if __name__ == "__main__":
    reorganiser_tests()
