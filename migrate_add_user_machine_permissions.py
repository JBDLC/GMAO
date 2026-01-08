"""
Migration pour ajouter la table user_machine_permission
"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour importer app
sys.path.insert(0, str(Path(__file__).parent))

from app import app, db
from sqlalchemy import text

def migrate():
    """Ajoute la table user_machine_permission"""
    with app.app_context():
        # Vérifier si la table existe déjà
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if 'user_machine_permission' in existing_tables:
            print("La table user_machine_permission existe déjà.")
            return
        
        print("Création de la table user_machine_permission...")
        
        # Créer la table
        db.session.execute(text("""
            CREATE TABLE user_machine_permission (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                machine_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
                FOREIGN KEY (machine_id) REFERENCES machine(id) ON DELETE CASCADE,
                UNIQUE(user_id, machine_id)
            )
        """))
        
        # Créer les index
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_user_machine_permission_user_id 
            ON user_machine_permission(user_id)
        """))
        
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_user_machine_permission_machine_id 
            ON user_machine_permission(machine_id)
        """))
        
        db.session.commit()
        print("Table user_machine_permission créée avec succès!")

if __name__ == "__main__":
    migrate()

