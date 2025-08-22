#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Passerelle entre les systèmes database et database_simple pour le formatage
"""

def sync_formatting_data():
    """Synchronise les données de formatage entre les deux systèmes"""
    print("🔄 Synchronisation des données de formatage")
    print("=" * 50)
    
    try:
        from lib.database import CardRepo as MainRepo
        from lib.database_simple import CardRepo as SimpleRepo
        from lib.config import DB_FILE
        import sqlite3
        
        # Lire les cartes du système principal
        main_repo = MainRepo(DB_FILE)
        main_cards = main_repo.list_cards()
        
        print(f"📊 Cartes du système principal: {len(main_cards)}")
        
        # Vérifier si la table cards a les colonnes de formatage
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Vérifier les colonnes existantes
        cursor.execute("PRAGMA table_info(cards)")
        columns = [col[1] for col in cursor.fetchall()]
        
        formatting_columns = [
            'title_x', 'title_y', 'title_font', 'title_size', 'title_color',
            'text_x', 'text_y', 'text_width', 'text_height', 'text_font',
            'text_size', 'text_color', 'text_align', 'line_spacing', 'text_wrap'
        ]
        
        missing_columns = [col for col in formatting_columns if col not in columns]
        
        if missing_columns:
            print(f"📝 Ajout des colonnes de formatage manquantes...")
            for col in missing_columns:
                if col in ['line_spacing']:
                    cursor.execute(f"ALTER TABLE cards ADD COLUMN {col} REAL DEFAULT 1.2")
                elif col in ['text_wrap']:
                    cursor.execute(f"ALTER TABLE cards ADD COLUMN {col} INTEGER DEFAULT 1")
                elif 'color' in col:
                    cursor.execute(f"ALTER TABLE cards ADD COLUMN {col} TEXT DEFAULT '#000000'")
                elif 'font' in col:
                    cursor.execute(f"ALTER TABLE cards ADD COLUMN {col} TEXT DEFAULT 'Arial'")
                elif 'align' in col:
                    cursor.execute(f"ALTER TABLE cards ADD COLUMN {col} TEXT DEFAULT 'left'")
                else:
                    cursor.execute(f"ALTER TABLE cards ADD COLUMN {col} INTEGER DEFAULT 50")
                print(f"   ✅ Colonne {col} ajoutée")
            
            conn.commit()
            print("✅ Colonnes de formatage ajoutées au système principal")
        else:
            print("✅ Toutes les colonnes de formatage sont présentes")
        
        # Maintenant récupérer les données de formatage de notre sauvegarde
        if True:  # Les cartes existent, ajouter les données de formatage
            try:
                simple_repo = SimpleRepo('backups/cartes_simple_backup.db')
                simple_cards = simple_repo.list_cards()
                
                print(f"📊 Données de formatage à restaurer: {len(simple_cards)}")
                
                for simple_card in simple_cards:
                    # Trouver la carte correspondante dans le système principal
                    main_card = next((c for c in main_cards if c.name == simple_card.nom), None)
                    
                    if main_card:
                        print(f"🔄 Synchronisation formatage: {main_card.name}")
                        
                        # Mettre à jour avec les données de formatage
                        cursor.execute("""
                            UPDATE cards SET 
                                title_x=?, title_y=?, title_font=?, title_size=?, title_color=?,
                                text_x=?, text_y=?, text_width=?, text_height=?, text_font=?,
                                text_size=?, text_color=?, text_align=?, line_spacing=?, text_wrap=?
                            WHERE id=?
                        """, (
                            simple_card.title_x, simple_card.title_y, simple_card.title_font,
                            simple_card.title_size, simple_card.title_color,
                            simple_card.text_x, simple_card.text_y, simple_card.text_width,
                            simple_card.text_height, simple_card.text_font, simple_card.text_size,
                            simple_card.text_color, simple_card.text_align, simple_card.line_spacing,
                            int(simple_card.text_wrap), main_card.id
                        ))
                        
                        print(f"   ✅ Formatage synchronisé pour {main_card.name}")
                    else:
                        print(f"   ⚠️  Carte '{simple_card.nom}' non trouvée dans le système principal")
                
                conn.commit()
                print("✅ Synchronisation du formatage terminée")
                
            except Exception as e:
                print(f"⚠️  Pas de données de formatage à restaurer: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la synchronisation: {e}")
        return False

if __name__ == "__main__":
    sync_formatting_data()
