"""Script pour vérifier la structure de la table machine"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "app.db"

if not DB_PATH.exists():
    print(f"Erreur: Le fichier de base de donnees {DB_PATH} n'existe pas.")
    exit(1)

try:
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Vérifier la structure de la table
    cursor.execute("PRAGMA table_info(machine)")
    columns = cursor.fetchall()
    
    print("Colonnes de la table machine:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Vérifier si color_index existe
    column_names = [col[1] for col in columns]
    if 'color_index' in column_names:
        print("\nLa colonne color_index existe.")
    else:
        print("\nLa colonne color_index n'existe PAS.")
        print("Ajout de la colonne...")
        cursor.execute("ALTER TABLE machine ADD COLUMN color_index INTEGER DEFAULT 0")
        conn.commit()
        print("Colonne ajoutee avec succes!")
    
    conn.close()
    
except sqlite3.Error as e:
    print(f"Erreur SQLite: {e}")
    exit(1)
except Exception as e:
    print(f"Erreur: {e}")
    exit(1)


