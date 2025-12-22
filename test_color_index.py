"""Script de test pour vérifier que color_index fonctionne"""
from app import app, db, Machine

with app.app_context():
    # Vérifier que le modèle a bien le champ
    print("Verification du modele Machine...")
    print(f"Colonnes du modele: {[col.name for col in Machine.__table__.columns]}")
    
    if 'color_index' in [col.name for col in Machine.__table__.columns]:
        print("OK: Le champ color_index est present dans le modele.")
    else:
        print("ERREUR: Le champ color_index n'est pas present dans le modele.")
    
    # Vérifier que la colonne existe dans la base de données
    print("\nVerification de la base de donnees...")
    try:
        result = db.session.execute(db.text("PRAGMA table_info(machine)"))
        columns = [row[1] for row in result]
        if 'color_index' in columns:
            print("OK: La colonne color_index existe dans la base de donnees.")
        else:
            print("ERREUR: La colonne color_index n'existe pas dans la base de donnees.")
    except Exception as e:
        print(f"ERREUR lors de la verification: {e}")
    
    # Tester une requête simple
    print("\nTest d'une requete simple...")
    try:
        machine = Machine.query.first()
        if machine:
            print(f"OK: Machine trouvee: {machine.name}, color_index: {machine.color_index}")
        else:
            print("Aucune machine trouvee dans la base de donnees.")
    except Exception as e:
        print(f"ERREUR lors de la requete: {e}")


