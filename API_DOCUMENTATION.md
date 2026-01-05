# Documentation API Mobile

API REST pour l'application mobile Android et iOS.

## Base URL

```
https://votre-app.onrender.com/api/v1
```

## Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification. Toutes les requêtes (sauf `/auth/login`) doivent inclure le token dans le header :

```
Authorization: Bearer <token>
```

## Endpoints

### Authentification

#### POST `/auth/login`
Connexion et récupération du token JWT.

**Body:**
```json
{
  "username": "admin123",
  "password": "123"
}
```

**Réponse:**
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin123",
    "user_type": "admin"
  }
}
```

#### GET `/auth/me`
Récupérer les informations de l'utilisateur connecté.

**Headers:** `Authorization: Bearer <token>`

**Réponse:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "admin123",
    "user_type": "admin"
  }
}
```

---

### Machines

#### GET `/machines`
Récupérer la liste de toutes les machines (arborescence complète).

**Headers:** `Authorization: Bearer <token>`

**Réponse:**
```json
{
  "success": true,
  "machines": [
    {
      "id": 1,
      "name": "Machine Racine",
      "code": "M001",
      "parent_id": null,
      "level": 0,
      "hour_counter_enabled": true,
      "hours": 1500.0,
      "counter_unit": "h",
      "stock_id": 1,
      "stock_name": "Stock Principal",
      "color_index": 0,
      "is_root": true,
      "counters": [
        {
          "id": 1,
          "name": "Compteur Principal",
          "value": 1500.0,
          "unit": "h"
        }
      ],
      "children": [...]
    }
  ],
  "followed_machine_ids": [1, 3, 5]
}
```

#### GET `/machines/<machine_id>`
Récupérer les détails d'une machine spécifique.

**Headers:** `Authorization: Bearer <token>`

**Réponse:**
```json
{
  "success": true,
  "machine": {
    "id": 1,
    "name": "Machine Racine",
    "code": "M001",
    "parent_id": null,
    "hour_counter_enabled": true,
    "hours": 1500.0,
    "counter_unit": "h",
    "counters": [...],
    "children": [...]
  },
  "preventive_maintenances": [...],
  "corrective_maintenances": [...],
  "checklist_templates": [...],
  "maintenance_progress": [...]
}
```

#### POST `/machines/<machine_id>/follow`
Suivre une machine.

**Headers:** `Authorization: Bearer <token>`

**Réponse:**
```json
{
  "success": true,
  "message": "Machine suivie avec succès"
}
```

#### POST `/machines/<machine_id>/unfollow`
Ne plus suivre une machine.

**Headers:** `Authorization: Bearer <token>`

**Réponse:**
```json
{
  "success": true,
  "message": "Machine non suivie"
}
```

---

### Maintenances Préventives

#### GET `/maintenances/preventive`
Récupérer la liste des maintenances préventives.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `machine_id` (optionnel): Filtrer par machine
- `limit` (optionnel, défaut: 50): Nombre maximum de résultats

**Réponse:**
```json
{
  "success": true,
  "maintenances": [
    {
      "id": 1,
      "machine_id": 1,
      "machine_name": "Machine Racine",
      "report_id": 1,
      "report_name": "Maintenance Mensuelle",
      "performed_hours": 1500.0,
      "hours_before_maintenance": 1450.0,
      "created_at": "2025-01-15T10:30:00",
      "user_name": "admin123",
      "values": [...]
    }
  ]
}
```

#### GET `/maintenances/preventive/<entry_id>`
Récupérer une maintenance préventive spécifique.

**Headers:** `Authorization: Bearer <token>`

#### POST `/maintenances/preventive`
Créer une nouvelle maintenance préventive.

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "machine_id": 1,
  "report_id": 1,
  "performed_hours": 1500.0,
  "hours_before_maintenance": 1450.0,
  "counter_id": null,
  "values": [
    {
      "component_id": 1,
      "value_text": "OK",
      "value_number": null,
      "value_bool": null
    },
    {
      "component_id": 2,
      "value_text": null,
      "value_number": 25.5,
      "value_bool": null
    }
  ]
}
```

**Réponse:**
```json
{
  "success": true,
  "maintenance": {
    "id": 1,
    "machine_id": 1,
    "report_id": 1,
    "created_at": "2025-01-15T10:30:00"
  }
}
```

---

### Maintenances Correctives

#### GET `/maintenances/corrective`
Récupérer la liste des maintenances correctives.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `machine_id` (optionnel): Filtrer par machine
- `limit` (optionnel, défaut: 50): Nombre maximum de résultats

#### GET `/maintenances/corrective/<maintenance_id>`
Récupérer une maintenance corrective spécifique.

**Headers:** `Authorization: Bearer <token>`

#### POST `/maintenances/corrective`
Créer une nouvelle maintenance corrective.

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "machine_id": 1,
  "comment": "Remplacement de la courroie",
  "hours": 1500.0,
  "stock_id": 1,
  "products": [
    {
      "product_id": 5,
      "quantity": 1
    }
  ]
}
```

---

### Checklists

#### GET `/checklists`
Récupérer la liste des checklists.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `machine_id` (optionnel): Filtrer par machine

#### POST `/checklists/<template_id>/fill`
Remplir une checklist.

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "machine_id": 1,
  "comment": "Tout est OK",
  "items": [
    {
      "item_id": 1,
      "checked": true
    },
    {
      "item_id": 2,
      "checked": false
    }
  ]
}
```

---

### Stocks et Produits

#### GET `/stocks`
Récupérer la liste des stocks.

**Headers:** `Authorization: Bearer <token>`

#### GET `/stocks/<stock_id>`
Récupérer les détails d'un stock avec ses produits.

**Headers:** `Authorization: Bearer <token>`

#### GET `/products`
Récupérer la liste des produits.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `search` (optionnel): Rechercher par nom ou code
- `limit` (optionnel, défaut: 100): Nombre maximum de résultats

---

### Compteurs

#### GET `/machines/<machine_id>/counters`
Récupérer les compteurs d'une machine.

**Headers:** `Authorization: Bearer <token>`

#### POST `/machines/<machine_id>/counters`
Mettre à jour un compteur.

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "counter_id": 1,
  "value": 1600.0
}
```

Pour un compteur classique (sans compteurs multiples), utiliser `counter_id: null`:
```json
{
  "counter_id": null,
  "value": 1600.0
}
```

---

### Rapports de Maintenance

#### GET `/machines/<machine_id>/reports`
Récupérer les rapports de maintenance préventive d'une machine.

**Headers:** `Authorization: Bearer <token>`

---

### Dashboard

#### GET `/dashboard`
Récupérer les données du dashboard pour les machines suivies par l'utilisateur.

**Headers:** `Authorization: Bearer <token>`

**Réponse:**
```json
{
  "success": true,
  "machines": [
    {
      "id": 1,
      "name": "Machine Racine",
      "code": "M001",
      "hours": 1500.0,
      "counter_unit": "h",
      "preventive_count": 5,
      "corrective_count": 2,
      "overdue_count": 1,
      "counters": [...]
    }
  ]
}
```

---

## Codes de Statut HTTP

- `200` : Succès
- `201` : Créé avec succès
- `400` : Requête invalide (données manquantes ou incorrectes)
- `401` : Non autorisé (token invalide ou expiré)
- `404` : Ressource non trouvée
- `500` : Erreur serveur

## Format des Erreurs

```json
{
  "error": "Message d'erreur descriptif"
}
```

## Exemples d'Utilisation

### Connexion et récupération des machines

```javascript
// 1. Connexion
const loginResponse = await fetch('https://votre-app.onrender.com/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'admin123',
    password: '123'
  })
});

const loginData = await loginResponse.json();
const token = loginData.token;

// 2. Récupérer les machines
const machinesResponse = await fetch('https://votre-app.onrender.com/api/v1/machines', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const machinesData = await machinesResponse.json();
console.log(machinesData.machines);
```

### Créer une maintenance préventive

```javascript
const response = await fetch('https://votre-app.onrender.com/api/v1/maintenances/preventive', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    machine_id: 1,
    report_id: 1,
    performed_hours: 1500.0,
    hours_before_maintenance: 1450.0,
    counter_id: null,
    values: [
      {
        component_id: 1,
        value_text: "OK"
      }
    ]
  })
});

const result = await response.json();
```

## Notes Importantes

1. **Sécurité** : Utilisez toujours HTTPS en production
2. **Tokens** : Stockez les tokens de manière sécurisée (Keychain sur iOS, Keystore sur Android)
3. **Gestion d'erreurs** : Vérifiez toujours le code de statut HTTP avant de traiter la réponse
4. **Rate Limiting** : L'API peut limiter le nombre de requêtes par minute (à implémenter si nécessaire)
5. **Pagination** : Pour les grandes listes, utilisez les paramètres `limit` et envisagez d'ajouter la pagination

