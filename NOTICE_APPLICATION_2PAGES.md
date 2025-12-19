# GMAO - Notice d'utilisation (2 pages)
## Gestion de Maintenance Assistée par Ordinateur

---

## 1. PRÉSENTATION GÉNÉRALE

L'application GMAO est un système web de gestion de maintenance pour machines, stocks, produits et opérations de maintenance préventive/corrective.

**Rôles utilisateurs** : Administrateur (accès complet) • Gestionnaire (mouvements, stocks, inventaires) • Technicien (maintenances, relevés) • Spectateur (consultation)

---

## 2. FONCTIONNALITÉS PRINCIPALES

### Gestion des machines
- **Arborescence** : Création de machines/sous-machines jusqu'à 5 niveaux avec code unique
- **Compteurs** : Configuration optionnelle (heures, cycles, anneaux, etc.) avec unité personnalisable
- **Relevés** : Saisie des valeurs de compteurs, historique complet, mise à jour automatique des plans de maintenance
- **Indicateurs visuels** : Points rouges (retard) et orange (proche échéance) sur l'arborescence

### Gestion des stocks et produits
- **Produits** : Création avec nom, code unique, prix, fournisseur, stock minimum • Import Excel en masse • Filtres (nom, code, fournisseur, stock min) • Affichage quantités par stock
- **Stocks** : Création/gestion jusqu'à 10 stocks • Ajout/suppression produits • Visualisation quantités
- **Mouvements** : Entrée (ajout), Sortie (retrait avec vérification), Transfert (entre stocks) • Historique avec date/heure • Modification/suppression (sauf liés aux maintenances)
- **Inventaires** : Inventaire complet d'un stock • Modification quantités tous produits • Commentaires par modification • Historique avec date/utilisateur

### Maintenance préventive
- **Modèles** : Création liée à une machine avec compteur • Périodicité (en unités compteur) • Composants (nombre, texte, case à cocher) • Calcul automatique temps restant
- **Rapports** : Remplissage basé sur modèles • Saisie valeurs composants • Prélèvement optionnel produits • Enregistrement date/heure/utilisateur • Mise à jour compteur maintenance
- **Gestion** : Vue maintenances en retard (rouge) et proches échéance (orange) • Réglage seuil alerte (5%, 10%, 15%, 20%) • Liste complète avec filtres

### Maintenance corrective
- **Rapports** : Création pour machine spécifique • Commentaires • Prélèvement optionnel produits • Enregistrement date/heure/utilisateur

---

## 3. NAVIGATION

**Menu principal** (3 menus déroulants) :
1. **Machines & Maintenance** : Machines • Maintenances • Gestion maintenance • Relevé compteurs
2. **Stocks & Produits** : Produits • Mouvements • Stocks • Inventaires (admin/gestionnaire)
3. **Utilisateurs** (admin uniquement)

**Page d'accueil** : Affiche nombre maintenances en retard, proches échéance, et produits sous stock minimum

---

## 4. FONCTIONNALITÉS AVANCÉES

**Export Excel** : Produits (avec filtres) • Relevés compteurs • Maintenances (avec filtres) • Mouvements • Inventaires

**Indicateurs visuels** : Points rouges (retard) • Points orange (proche échéance) • Badges colorés (différences inventaires)

**Filtres et recherche** : Filtres par colonnes • Recherche produits (nom/code) • Filtrage par stock • Filtrage produits sous stock minimum

---

## 5. RÈGLES MÉTIER

**Mouvements** : Entrée → ajoute produits • Sortie → vérifie stock suffisant • Transfert → applique sortie puis entrée

**Maintenances préventives** : Uniquement machines avec compteur • Calcul temps avant maintenance : Initialisation = périodicité • Après rapport = réinitialisé à périodicité • Après relevé = décrémenté de différence compteur

**Inventaires** : Seuls produits modifiés enregistrés • Quantités stock mises à jour automatiquement • Commentaire par modification

---

## 6. CONNEXION ET SÉCURITÉ

**Compte par défaut** : Identifiant `admin123` / Mot de passe `123` ⚠️ **À changer après première connexion !**

**Gestion utilisateurs** : Création comptes avec rôles • Suppression (sauf admin par défaut) • Traçabilité actions avec identifiant utilisateur

---

## 7. PERMISSIONS PAR RÔLE

| Fonctionnalité | Admin | Gestionnaire | Technicien | Spectateur |
|---|---|---|---|---|
| **Machines** | | | | |
| Créer/modifier/supprimer machine | ✓ | ✗ | ✗ | ✗ |
| Créer modèle maintenance | ✓ | ✗ | ✗ | ✗ |
| Nouveau relevé compteur | ✓ | ✗ | ✓ | ✗ |
| **Maintenances** | | | | |
| Remplir rapport préventif | ✓ | ✗ | ✓ | ✗ |
| Créer maintenance corrective | ✓ | ✗ | ✓ | ✗ |
| Modifier rapport (si créateur) | ✓ | ✗ | ✓ | ✗ |
| Modifier seuil gestion | ✓ | ✗ | ✗ | ✗ |
| **Produits** | | | | |
| Créer/modifier/supprimer | ✓ | ✗ | ✗ | ✗ |
| Import Excel | ✓ | ✗ | ✗ | ✗ |
| **Mouvements** | | | | |
| Créer/modifier/supprimer | ✓ | ✓ | ✗ | ✗ |
| **Stocks** | | | | |
| Voir stocks | ✓ | ✓ | ✗ | ✗ |
| Créer/modifier/supprimer | ✓ | ✗ | ✗ | ✗ |
| **Inventaires** | | | | |
| Créer/voir inventaires | ✓ | ✓ | ✗ | ✗ |
| **Utilisateurs** | | | | |
| Gérer utilisateurs | ✓ | ✗ | ✗ | ✗ |

---

**Version** : 1.0 | **Date** : 2025 | **Support** : Consulter README.md ou contacter l'administrateur









