"""Script de migration pour ajouter la colonne name à la table inventory"""
import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "app.db"

def migrate():
    """Ajoute la colonne name à la table inventory et génère les noms pour les inventaires existants"""
    if not DB_PATH.exists():
        print(f"Base de données non trouvée : {DB_PATH}")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    try:
        # Vérifier si la colonne existe déjà
        cursor.execute("PRAGMA table_info(inventory)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'name' not in columns:
            print("Ajout de la colonne 'name' à la table inventory...")
            cursor.execute("ALTER TABLE inventory ADD COLUMN name TEXT")
            conn.commit()
            print("Colonne 'name' ajoutée avec succès.")
        else:
            print("La colonne 'name' existe déjà.")
        
        # Générer les noms pour les inventaires existants qui n'ont pas de nom
        print("Génération des noms pour les inventaires existants...")
        
        # Récupérer tous les inventaires sans nom, groupés par stock
        cursor.execute("""
            SELECT i.id, i.stock_id, s.name as stock_name
            FROM inventory i
            JOIN stock s ON i.stock_id = s.id
            WHERE i.name IS NULL OR i.name = ''
            ORDER BY i.stock_id, i.created_at
        """)
        
        inventories = cursor.fetchall()
        
        # Compter les inventaires par stock pour générer les numéros
        stock_counts = {}
        for inv_id, stock_id, stock_name in inventories:
            if stock_id not in stock_counts:
                # Compter les inventaires existants pour ce stock (y compris ceux avec un nom)
                cursor.execute("""
                    SELECT COUNT(*) FROM inventory 
                    WHERE stock_id = ? AND (name IS NOT NULL AND name != '')
                """, (stock_id,))
                existing_count = cursor.fetchone()[0]
                stock_counts[stock_id] = existing_count
            
            stock_counts[stock_id] += 1
            inventory_number = stock_counts[stock_id]
            inventory_name = f"{stock_name} #{inventory_number}"
            
            cursor.execute("UPDATE inventory SET name = ? WHERE id = ?", (inventory_name, inv_id))
            print(f"  Inventaire {inv_id}: {inventory_name}")
        
        conn.commit()
        print(f"Migration terminée. {len(inventories)} inventaires mis à jour.")
        
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la migration : {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()


