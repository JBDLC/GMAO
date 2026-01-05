"""
Documentation Swagger pour l'API
Page web interactive accessible sur /api/docs
"""
from flask import render_template_string
from app import app

SWAGGER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>GMAO API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.0/swagger-ui.css" />
    <style>
        html {
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }
        *, *:before, *:after {
            box-sizing: inherit;
        }
        body {
            margin:0;
            background: #fafafa;
        }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: "/api/swagger.json",
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout"
            });
        };
    </script>
</body>
</html>
"""

@app.route('/api/docs')
def swagger_docs():
    """Page de documentation Swagger interactive"""
    return render_template_string(SWAGGER_HTML)

@app.route('/api/swagger.json')
def swagger_json():
    """Fichier JSON de spécification Swagger/OpenAPI"""
    from flask import jsonify
    
    swagger_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "GMAO API",
            "description": "API REST pour l'application mobile GMAO - Gestion de Maintenance Assistée par Ordinateur",
            "version": "1.0.0",
            "contact": {
                "name": "Support API",
                "url": "https://fms-telt.onrender.com"
            }
        },
        "servers": [
            {
                "url": "/api/v1",
                "description": "Serveur actuel"
            }
        ],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },
        "paths": {
            "/auth/login": {
                "post": {
                    "tags": ["Authentification"],
                    "summary": "Connexion et récupération du token JWT",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["username", "password"],
                                    "properties": {
                                        "username": {
                                            "type": "string",
                                            "example": "admin123"
                                        },
                                        "password": {
                                            "type": "string",
                                            "example": "123"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Connexion réussie",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "token": {"type": "string"},
                                            "user": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "integer"},
                                                    "username": {"type": "string"},
                                                    "user_type": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Identifiants invalides"
                        }
                    }
                }
            },
            "/auth/me": {
                "get": {
                    "tags": ["Authentification"],
                    "summary": "Récupérer les informations de l'utilisateur connecté",
                    "security": [{"bearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Informations utilisateur",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "user": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "integer"},
                                                    "username": {"type": "string"},
                                                    "user_type": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/machines": {
                "get": {
                    "tags": ["Machines"],
                    "summary": "Récupérer la liste de toutes les machines",
                    "security": [{"bearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Liste des machines",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "machines": {
                                                "type": "array",
                                                "items": {"type": "object"}
                                            },
                                            "followed_machine_ids": {
                                                "type": "array",
                                                "items": {"type": "integer"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/machines/{machine_id}": {
                "get": {
                    "tags": ["Machines"],
                    "summary": "Récupérer les détails d'une machine",
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {
                            "name": "machine_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Détails de la machine"
                        }
                    }
                }
            },
            "/machines/{machine_id}/follow": {
                "post": {
                    "tags": ["Machines"],
                    "summary": "Suivre une machine",
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {
                            "name": "machine_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Machine suivie avec succès"
                        }
                    }
                }
            },
            "/machines/{machine_id}/unfollow": {
                "post": {
                    "tags": ["Machines"],
                    "summary": "Ne plus suivre une machine",
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {
                            "name": "machine_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Machine non suivie"
                        }
                    }
                }
            },
            "/maintenances/preventive": {
                "get": {
                    "tags": ["Maintenances"],
                    "summary": "Récupérer les maintenances préventives",
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {
                            "name": "machine_id",
                            "in": "query",
                            "schema": {"type": "integer"},
                            "description": "Filtrer par machine"
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "schema": {"type": "integer"},
                            "description": "Nombre maximum de résultats"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Liste des maintenances préventives"
                        }
                    }
                },
                "post": {
                    "tags": ["Maintenances"],
                    "summary": "Créer une maintenance préventive",
                    "security": [{"bearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["machine_id", "report_id"],
                                    "properties": {
                                        "machine_id": {"type": "integer"},
                                        "report_id": {"type": "integer"},
                                        "performed_hours": {"type": "number"},
                                        "hours_before_maintenance": {"type": "number"},
                                        "counter_id": {"type": "integer", "nullable": True},
                                        "values": {
                                            "type": "array",
                                            "items": {"type": "object"}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Maintenance créée"
                        }
                    }
                }
            },
            "/maintenances/corrective": {
                "get": {
                    "tags": ["Maintenances"],
                    "summary": "Récupérer les maintenances correctives",
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {
                            "name": "machine_id",
                            "in": "query",
                            "schema": {"type": "integer"}
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Liste des maintenances correctives"
                        }
                    }
                },
                "post": {
                    "tags": ["Maintenances"],
                    "summary": "Créer une maintenance corrective",
                    "security": [{"bearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["machine_id"],
                                    "properties": {
                                        "machine_id": {"type": "integer"},
                                        "comment": {"type": "string"},
                                        "hours": {"type": "number"},
                                        "stock_id": {"type": "integer"},
                                        "products": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "product_id": {"type": "integer"},
                                                    "quantity": {"type": "number"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Maintenance corrective créée"
                        }
                    }
                }
            },
            "/stocks": {
                "get": {
                    "tags": ["Stocks"],
                    "summary": "Récupérer la liste des stocks",
                    "security": [{"bearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Liste des stocks"
                        }
                    }
                }
            },
            "/stocks/{stock_id}": {
                "get": {
                    "tags": ["Stocks"],
                    "summary": "Récupérer les détails d'un stock",
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {
                            "name": "stock_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Détails du stock"
                        }
                    }
                }
            },
            "/products": {
                "get": {
                    "tags": ["Produits"],
                    "summary": "Récupérer la liste des produits",
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {
                            "name": "search",
                            "in": "query",
                            "schema": {"type": "string"},
                            "description": "Rechercher par nom ou code"
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Liste des produits"
                        }
                    }
                }
            },
            "/machines/{machine_id}/counters": {
                "get": {
                    "tags": ["Compteurs"],
                    "summary": "Récupérer les compteurs d'une machine",
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {
                            "name": "machine_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Compteurs de la machine"
                        }
                    }
                },
                "post": {
                    "tags": ["Compteurs"],
                    "summary": "Mettre à jour un compteur",
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {
                            "name": "machine_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["value"],
                                    "properties": {
                                        "counter_id": {"type": "integer", "nullable": True},
                                        "value": {"type": "number"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Compteur mis à jour"
                        }
                    }
                }
            },
            "/dashboard": {
                "get": {
                    "tags": ["Dashboard"],
                    "summary": "Récupérer les données du dashboard",
                    "security": [{"bearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Données du dashboard"
                        }
                    }
                }
            }
        },
        "tags": [
            {
                "name": "Authentification",
                "description": "Endpoints d'authentification"
            },
            {
                "name": "Machines",
                "description": "Gestion des machines"
            },
            {
                "name": "Maintenances",
                "description": "Gestion des maintenances préventives et correctives"
            },
            {
                "name": "Stocks",
                "description": "Gestion des stocks"
            },
            {
                "name": "Produits",
                "description": "Gestion des produits"
            },
            {
                "name": "Compteurs",
                "description": "Gestion des compteurs de machines"
            },
            {
                "name": "Dashboard",
                "description": "Données du tableau de bord"
            }
        ]
    }
    
    return jsonify(swagger_spec)

