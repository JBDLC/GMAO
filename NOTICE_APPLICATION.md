# GMAO - Notice d'utilisation
## Gestion de Maintenance Assistée par Ordinateur

---

## 1. Présentation générale

L'application GMAO est un système de gestion de maintenance permettant de gérer les machines, les stocks, les produits et les opérations de maintenance préventive et corrective. Elle est accessible via un navigateur web et propose différents niveaux d'accès selon le rôle de l'utilisateur.

### Rôles utilisateurs

- **Administrateur** : Accès complet à toutes les fonctionnalités
- **Gestionnaire** : Gestion des mouvements, stocks et inventaires
- **Technicien** : Réalisation des maintenances et relevés de compteurs
- **Spectateur** : Consultation uniquement

---

## 2. Fonctionnalités principales

### 2.1 Gestion des machines

**Création d'une arborescence de machines**
- Création de machines et sous-machines jusqu'à 5 niveaux
- Attribution d'un code unique et d'un nom
- Configuration optionnelle d'un compteur (heures, cycles, anneaux, etc.)
- Visualisation de l'arborescence avec indicateurs de maintenance

**Relevé de compteurs**
- Saisie des valeurs de compteurs pour les machines équipées
- Historique des relevés avec date et utilisateur
- Mise à jour automatique des plans de maintenance préventive

### 2.2 Gestion des stocks et produits

**Produits**
- Création de produits avec nom, code unique, prix, fournisseur et stock minimum
- Import en masse depuis un fichier Excel
- Filtrage et recherche par nom, code, fournisseur
- Affichage des quantités par stock et du stock total

**Stocks**
- Création et gestion de plusieurs stocks (maximum 10)
- Ajout/suppression de produits dans les stocks
- Visualisation des quantités par produit

**Mouvements**
- Création de mouvements de type :
  - **Entrée** : Ajout de produits dans un stock
  - **Sortie** : Retrait de produits d'un stock (avec vérification des quantités)
  - **Transfert** : Déplacement entre deux stocks
- Historique des mouvements avec date et heure
- Modification et suppression des mouvements (sauf ceux liés aux maintenances)

**Inventaires**
- Réalisation d'inventaires complets d'un stock
- Modification des quantités de tous les produits
- Ajout de commentaires pour chaque modification
- Historique des inventaires avec date, utilisateur et modifications

### 2.3 Maintenance préventive

**Modèles de maintenance**
- Création de modèles de maintenance préventive liés à une machine
- Définition d'une périodicité (en unités du compteur)
- Ajout de composants (nombre, texte, case à cocher)
- Calcul automatique du temps restant avant maintenance

**Rapports de maintenance**
- Remplissage de rapports basés sur les modèles
- Saisie des valeurs pour chaque composant
- Prélèvement optionnel de produits depuis un stock
- Enregistrement de la date, de l'heure et de l'utilisateur
- Mise à jour automatique du compteur de maintenance

**Gestion des maintenances**
- Vue d'ensemble des maintenances en retard (rouge) et proches de l'échéance (orange)
- Réglage du seuil d'alerte (5%, 10%, 15%, 20%)
- Liste complète de toutes les maintenances avec filtres

### 2.4 Maintenance corrective

**Rapports de maintenance corrective**
- Création de rapports pour une machine spécifique
- Saisie de commentaires
- Prélèvement optionnel de produits depuis un stock
- Enregistrement de la date, de l'heure et de l'utilisateur

---

## 3. Navigation et accès

### Menu principal

L'application propose trois menus déroulants :

1. **Machines & Maintenance**
   - Machines
   - Maintenances
   - Gestion maintenance
   - Relevé compteurs

2. **Stocks & Produits**
   - Produits
   - Mouvements
   - Stocks
   - Inventaires (admin et gestionnaire)

3. **Utilisateurs** (admin uniquement)

### Page d'accueil

La page d'accueil affiche :
- Nombre de maintenances préventives en retard
- Nombre de maintenances proches de l'échéance
- Nombre de produits en dessous du stock minimum

---

## 4. Fonctionnalités avancées

### Export Excel

Export disponible pour :
- Liste des produits (avec filtres appliqués)
- Historique des relevés de compteurs
- Liste des maintenances (avec filtres)
- Liste des mouvements
- Historique des inventaires

### Indicateurs visuels

- **Points rouges** : Maintenance en retard sur une machine/sous-machine
- **Points orange** : Maintenance proche de l'échéance
- **Badges colorés** : Différences de quantités dans les inventaires

### Filtres et recherche

- Filtres par colonnes dans les listes
- Recherche de produits par nom ou code
- Filtrage par stock dans la liste des produits
- Filtrage des produits en dessous du stock minimum

---

## 5. Règles métier importantes

### Mouvements
- **Entrée** : Ajoute toujours des produits au stock
- **Sortie** : Vérifie que le stock est suffisant avant de retirer
- **Transfert** : Applique les règles de sortie puis d'entrée

### Maintenances préventives
- Seules les machines avec compteur peuvent avoir des plans de maintenance
- Le temps avant maintenance se calcule ainsi :
  - Initialisation : égal à la périodicité
  - Après remplissage d'un rapport : réinitialisé à la périodicité
  - Après relevé de compteur : décrémenté de la différence de compteur

### Inventaires
- Seuls les produits avec des modifications sont enregistrés
- Les quantités du stock sont mises à jour automatiquement
- Chaque modification peut avoir un commentaire

---

## 6. Connexion et sécurité

### Compte par défaut
- **Identifiant** : `admin123`
- **Mot de passe** : `123`

⚠️ **Important** : Changez ce mot de passe après la première connexion !

### Gestion des utilisateurs
- Création de comptes avec différents rôles
- Suppression de comptes (sauf le compte admin par défaut)
- Chaque action est tracée avec l'identifiant de l'utilisateur

---

## 7. Support et assistance

Pour toute question ou problème :
1. Consultez la documentation technique dans le fichier README.md
2. Vérifiez les permissions de votre compte utilisateur
3. Contactez l'administrateur système

---

**Version** : 1.0  
**Date** : 2025








