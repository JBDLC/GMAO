# GMAO - Gestion de Maintenance Assistée par Ordinateur

Application Flask pour la gestion des machines, stocks, produits et maintenances.

## Déploiement sur Render

### Prérequis
- Un compte Render (gratuit disponible)
- Un dépôt Git (GitHub, GitLab, ou Bitbucket)

### Étapes de déploiement

1. **Préparer le dépôt Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <URL_DE_VOTRE_REPO>
   git push -u origin main
   ```

2. **Créer un nouveau service Web sur Render**
   - Allez sur [Render Dashboard](https://dashboard.render.com)
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre dépôt Git
   - Sélectionnez le dépôt et la branche

3. **Configuration du service**
   - **Name**: `gmao-app` (ou le nom de votre choix)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (ou un plan payant selon vos besoins)

4. **Créer une base de données PostgreSQL**
   - Dans le dashboard Render, cliquez sur "New +" → "PostgreSQL"
   - **Name**: `gmao-db`
   - **Database**: `gmao`
   - **User**: `gmao_user`
   - **Plan**: Free (ou un plan payant)
   - Notez les informations de connexion

5. **Configurer les variables d'environnement**
   Dans les paramètres de votre service Web, ajoutez :
   - **DATABASE_URL**: Copiez la valeur "Internal Database URL" depuis votre base de données PostgreSQL
   - **SECRET_KEY**: Générez une clé secrète sécurisée (vous pouvez utiliser `python -c "import secrets; print(secrets.token_hex(32))"`)

6. **Lier la base de données au service Web**
   - Dans les paramètres de votre service Web, section "Connections"
   - Cliquez sur "Link Database" et sélectionnez votre base de données PostgreSQL

7. **Déployer**
   - Render va automatiquement détecter le fichier `render.yaml` et configurer le service
   - Ou vous pouvez déployer manuellement en cliquant sur "Deploy"

### Migration de la base de données

Après le premier déploiement, la base de données sera créée automatiquement grâce à `db.create_all()` dans `app.py`.

**Note importante**: Les migrations de schéma (ALTER TABLE) dans le code seront exécutées automatiquement au démarrage si nécessaire.

### Accès à l'application

Une fois déployé, Render vous fournira une URL du type : `https://gmao-app.onrender.com`

### Compte administrateur par défaut

- **Username**: `admin123`
- **Password**: `123`

⚠️ **Important**: Changez ce mot de passe après le premier déploiement en production !

## Développement local

### Installation

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Lancer l'application

```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## Structure du projet

- `app.py`: Application Flask principale
- `templates/`: Templates Jinja2
- `requirements.txt`: Dépendances Python
- `render.yaml`: Configuration Render (optionnel)
- `Procfile`: Commande de démarrage pour Render
- `runtime.txt`: Version Python pour Render

## Notes importantes

- En local, l'application utilise SQLite (`app.db`)
- Sur Render, l'application utilise PostgreSQL automatiquement via la variable d'environnement `DATABASE_URL`
- La clé secrète doit être changée en production (utilisez une variable d'environnement)









