"""
Script de migration pour ajouter la colonne color_index à la table machine
"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "app.db"

if not DB_PATH.exists():
    print(f"Erreur: Le fichier de base de données {DB_PATH} n'existe pas.")
    exit(1)

try:
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Vérifier si la colonne existe déjà
    cursor.execute("PRAGMA table_info(machine)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'color_index' in columns:
        print("La colonne color_index existe déjà dans la table machine.")
    else:
        # Ajouter la colonne color_index
        cursor.execute("ALTER TABLE machine ADD COLUMN color_index INTEGER DEFAULT 0")
        conn.commit()
        print("Colonne color_index ajoutee avec succes a la table machine.")
        
        # Mettre à jour toutes les machines existantes avec un color_index par défaut basé sur leur ordre
        cursor.execute("SELECT id FROM machine WHERE parent_id IS NULL ORDER BY name")
        root_machines = cursor.fetchall()
        
        for idx, (machine_id,) in enumerate(root_machines):
            color_index = idx % 10
            cursor.execute("UPDATE machine SET color_index = ? WHERE id = ?", (color_index, machine_id))
            # Mettre à jour aussi toutes les sous-machines de cette machine racine
            cursor.execute("""
                UPDATE machine 
                SET color_index = ? 
                WHERE id IN (
                    WITH RECURSIVE descendants AS (
                        SELECT id FROM machine WHERE parent_id = ?
                        UNION ALL
                        SELECT m.id FROM machine m
                        INNER JOIN descendants d ON m.parent_id = d.id
                    )
                    SELECT id FROM descendants
                )
            """, (color_index, machine_id))
        
        conn.commit()
        print(f"{len(root_machines)} machines racines mises a jour avec leur color_index.")
        print("Toutes les sous-machines ont herite du color_index de leur machine racine.")
    
    conn.close()
    print("\nMigration terminée avec succès!")
    
except sqlite3.Error as e:
    print(f"Erreur SQLite: {e}")
    exit(1)
except Exception as e:
    print(f"Erreur: {e}")
    exit(1)

