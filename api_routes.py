"""
API Routes pour l'application mobile
Endpoints REST pour Android et iOS
"""
import datetime as dt
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from sqlalchemy.orm import joinedload
from sqlalchemy import or_ as sql_or_
from app import app, db
from app import (
    User, Machine, FollowedMachine, Counter, Product, Stock, StockProduct,
    PreventiveReport, PreventiveComponent, MaintenanceEntry, MaintenanceEntryValue,
    CorrectiveMaintenance, CorrectiveMaintenanceProduct, CounterLog,
    ChecklistTemplate, ChecklistItem, ChecklistInstance, MaintenanceProgress
)


# ==================== AUTHENTIFICATION ====================

@app.route('/api/v1/auth/login', methods=['POST'])
def api_login():
    """Authentification pour l'application mobile"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username et password requis'}), 400
    
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        # Créer le token JWT
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'user_type': user.user_type, 'username': user.username}
        )
        
        return jsonify({
            'success': True,
            'token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'user_type': user.user_type
            }
        }), 200
    else:
        return jsonify({'error': 'Identifiants invalides'}), 401


@app.route('/api/v1/auth/me', methods=['GET'])
@jwt_required()
def api_get_current_user():
    """Récupérer les informations de l'utilisateur connecté"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'user_type': user.user_type
        }
    }), 200


# ==================== MACHINES ====================

@app.route('/api/v1/machines', methods=['GET'])
@jwt_required()
def api_get_machines():
    """Récupérer la liste des machines"""
    user_id = get_jwt_identity()
    
    # Récupérer toutes les machines racines avec leurs enfants
    root_machines = Machine.query.filter_by(parent_id=None).options(
        joinedload(Machine.children),
        joinedload(Machine.counters),
        joinedload(Machine.stock)
    ).order_by(Machine.name).all()
    
    def serialize_machine(machine, level=0):
        """Sérialiser une machine récursivement"""
        return {
            'id': machine.id,
            'name': machine.name,
            'code': machine.code,
            'parent_id': machine.parent_id,
            'level': level,
            'hour_counter_enabled': machine.hour_counter_enabled,
            'hours': machine.hours,
            'counter_unit': machine.counter_unit,
            'stock_id': machine.stock_id,
            'stock_name': machine.stock.name if machine.stock else None,
            'color_index': machine.color_index if machine.color_index else 0,
            'is_root': machine.is_root(),
            'counters': [{
                'id': c.id,
                'name': c.name,
                'value': c.value,
                'unit': c.unit
            } for c in machine.counters],
            'children': [serialize_machine(child, level + 1) for child in sorted(machine.children, key=lambda x: x.name)]
        }
    
    machines = []
    for root in root_machines:
        machines.append(serialize_machine(root))
    
    # Vérifier quelles machines sont suivies par l'utilisateur
    followed_machine_ids = {
        fm.machine_id for fm in FollowedMachine.query.filter_by(user_id=user_id).all()
    }
    
    return jsonify({
        'success': True,
        'machines': machines,
        'followed_machine_ids': list(followed_machine_ids)
    }), 200


@app.route('/api/v1/machines/<int:machine_id>', methods=['GET'])
@jwt_required()
def api_get_machine(machine_id):
    """Récupérer les détails d'une machine"""
    machine = Machine.query.options(
        joinedload(Machine.parent),
        joinedload(Machine.children),
        joinedload(Machine.counters),
        joinedload(Machine.stock)
    ).get_or_404(machine_id)
    
    # Récupérer les maintenances préventives
    preventive_entries = MaintenanceEntry.query.filter_by(
        machine_id=machine_id
    ).options(
        joinedload(MaintenanceEntry.report),
        joinedload(MaintenanceEntry.user)
    ).order_by(MaintenanceEntry.created_at.desc()).limit(10).all()
    
    # Récupérer les maintenances correctives
    corrective_maintenances = CorrectiveMaintenance.query.filter_by(
        machine_id=machine_id
    ).options(
        joinedload(CorrectiveMaintenance.user),
        joinedload(CorrectiveMaintenance.products)
    ).order_by(CorrectiveMaintenance.created_at.desc()).limit(10).all()
    
    # Récupérer les checklists
    checklist_templates = ChecklistTemplate.query.filter_by(
        machine_id=machine_id
    ).options(
        joinedload(ChecklistTemplate.items)
    ).all()
    
    # Récupérer les progress de maintenance
    progress_records = MaintenanceProgress.query.filter_by(
        machine_id=machine_id
    ).options(
        joinedload(MaintenanceProgress.report),
        joinedload(MaintenanceProgress.counter)
    ).all()
    
    return jsonify({
        'success': True,
        'machine': {
            'id': machine.id,
            'name': machine.name,
            'code': machine.code,
            'parent_id': machine.parent_id,
            'parent_name': machine.parent.name if machine.parent else None,
            'hour_counter_enabled': machine.hour_counter_enabled,
            'hours': machine.hours,
            'counter_unit': machine.counter_unit,
            'stock_id': machine.stock_id,
            'stock_name': machine.stock.name if machine.stock else None,
            'color_index': machine.color_index if machine.color_index else 0,
            'is_root': machine.is_root(),
            'counters': [{
                'id': c.id,
                'name': c.name,
                'value': c.value,
                'unit': c.unit
            } for c in machine.counters],
            'children': [{
                'id': c.id,
                'name': c.name,
                'code': c.code
            } for c in sorted(machine.children, key=lambda x: x.name)]
        },
        'preventive_maintenances': [{
            'id': e.id,
            'report_name': e.report.name,
            'report_id': e.report_id,
            'performed_hours': e.performed_hours,
            'hours_before_maintenance': e.hours_before_maintenance,
            'created_at': e.created_at.isoformat(),
            'user_name': e.user.username if e.user else None
        } for e in preventive_entries],
        'corrective_maintenances': [{
            'id': m.id,
            'comment': m.comment,
            'hours': m.hours,
            'created_at': m.created_at.isoformat(),
            'user_name': m.user.username if m.user else None,
            'products': [{
                'product_id': p.product_id,
                'product_name': p.product.name if p.product else None,
                'quantity': p.quantity
            } for p in m.products]
        } for m in corrective_maintenances],
        'checklist_templates': [{
            'id': t.id,
            'name': t.name,
            'items': [{
                'id': i.id,
                'label': i.label,
                'order': i.order
            } for i in t.items]
        } for t in checklist_templates],
        'maintenance_progress': [{
            'id': p.id,
            'report_id': p.report_id,
            'report_name': p.report.name if p.report else None,
            'counter_id': p.counter_id,
            'counter_name': p.counter.name if p.counter else None,
            'hours_since': p.hours_since
        } for p in progress_records]
    }), 200


@app.route('/api/v1/machines/<int:machine_id>/follow', methods=['POST'])
@jwt_required()
def api_follow_machine(machine_id):
    """Suivre une machine"""
    user_id = get_jwt_identity()
    machine = Machine.query.get_or_404(machine_id)
    
    # Vérifier si déjà suivie
    existing = FollowedMachine.query.filter_by(
        user_id=user_id,
        machine_id=machine_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Machine déjà suivie'}), 400
    
    followed = FollowedMachine(user_id=user_id, machine_id=machine_id)
    db.session.add(followed)
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Machine suivie avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/machines/<int:machine_id>/unfollow', methods=['POST'])
@jwt_required()
def api_unfollow_machine(machine_id):
    """Ne plus suivre une machine"""
    user_id = get_jwt_identity()
    
    followed = FollowedMachine.query.filter_by(
        user_id=user_id,
        machine_id=machine_id
    ).first()
    
    if not followed:
        return jsonify({'error': 'Machine non suivie'}), 404
    
    db.session.delete(followed)
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Machine non suivie'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== MAINTENANCES PRÉVENTIVES ====================

@app.route('/api/v1/maintenances/preventive', methods=['GET'])
@jwt_required()
def api_get_preventive_maintenances():
    """Récupérer les maintenances préventives"""
    machine_id = request.args.get('machine_id', type=int)
    limit = request.args.get('limit', 50, type=int)
    
    query = MaintenanceEntry.query.options(
        joinedload(MaintenanceEntry.machine),
        joinedload(MaintenanceEntry.report),
        joinedload(MaintenanceEntry.user),
        joinedload(MaintenanceEntry.values)
    )
    
    if machine_id:
        query = query.filter_by(machine_id=machine_id)
    
    entries = query.order_by(MaintenanceEntry.created_at.desc()).limit(limit).all()
    
    return jsonify({
        'success': True,
        'maintenances': [{
            'id': e.id,
            'machine_id': e.machine_id,
            'machine_name': e.machine.name if e.machine else None,
            'report_id': e.report_id,
            'report_name': e.report.name if e.report else None,
            'performed_hours': e.performed_hours,
            'hours_before_maintenance': e.hours_before_maintenance,
            'created_at': e.created_at.isoformat(),
            'user_name': e.user.username if e.user else None,
            'values': [{
                'component_id': v.component_id,
                'value_text': v.value_text,
                'value_number': v.value_number,
                'value_bool': v.value_bool
            } for v in e.values]
        } for e in entries]
    }), 200


@app.route('/api/v1/maintenances/preventive/<int:entry_id>', methods=['GET'])
@jwt_required()
def api_get_preventive_maintenance(entry_id):
    """Récupérer une maintenance préventive spécifique"""
    entry = MaintenanceEntry.query.options(
        joinedload(MaintenanceEntry.machine),
        joinedload(MaintenanceEntry.report),
        joinedload(MaintenanceEntry.report).joinedload(PreventiveReport.components),
        joinedload(MaintenanceEntry.user),
        joinedload(MaintenanceEntry.values)
    ).get_or_404(entry_id)
    
    return jsonify({
        'success': True,
        'maintenance': {
            'id': entry.id,
            'machine_id': entry.machine_id,
            'machine_name': entry.machine.name if entry.machine else None,
            'report_id': entry.report_id,
            'report_name': entry.report.name if entry.report else None,
            'report_periodicity': entry.report.periodicity if entry.report else None,
            'performed_hours': entry.performed_hours,
            'hours_before_maintenance': entry.hours_before_maintenance,
            'created_at': entry.created_at.isoformat(),
            'user_name': entry.user.username if entry.user else None,
            'components': [{
                'id': c.id,
                'label': c.label,
                'field_type': c.field_type
            } for c in entry.report.components] if entry.report else [],
            'values': [{
                'component_id': v.component_id,
                'value_text': v.value_text,
                'value_number': v.value_number,
                'value_bool': v.value_bool
            } for v in entry.values]
        }
    }), 200


@app.route('/api/v1/maintenances/preventive', methods=['POST'])
@jwt_required()
def api_create_preventive_maintenance():
    """Créer une maintenance préventive"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Données manquantes'}), 400
    
    machine_id = data.get('machine_id')
    report_id = data.get('report_id')
    performed_hours = data.get('performed_hours', 0.0)
    hours_before_maintenance = data.get('hours_before_maintenance')
    values = data.get('values', [])  # Liste de {component_id, value_text/value_number/value_bool}
    
    if not machine_id or not report_id:
        return jsonify({'error': 'machine_id et report_id requis'}), 400
    
    # Vérifier que la machine et le rapport existent
    machine = Machine.query.get(machine_id)
    report = PreventiveReport.query.get(report_id)
    
    if not machine:
        return jsonify({'error': 'Machine non trouvée'}), 404
    if not report:
        return jsonify({'error': 'Rapport non trouvé'}), 404
    
    # Créer l'entrée de maintenance
    entry = MaintenanceEntry(
        machine_id=machine_id,
        report_id=report_id,
        user_id=user_id,
        performed_hours=performed_hours,
        hours_before_maintenance=hours_before_maintenance,
        created_at=dt.datetime.utcnow()
    )
    db.session.add(entry)
    db.session.flush()  # Pour obtenir l'ID
    
    # Ajouter les valeurs
    for val_data in values:
        component_id = val_data.get('component_id')
        if not component_id:
            continue
        
        value_entry = MaintenanceEntryValue(
            entry_id=entry.id,
            component_id=component_id,
            value_text=val_data.get('value_text'),
            value_number=val_data.get('value_number'),
            value_bool=val_data.get('value_bool')
        )
        db.session.add(value_entry)
    
    # Mettre à jour le MaintenanceProgress
    counter_id = data.get('counter_id')  # None pour compteur classique
    progress = MaintenanceProgress.query.filter_by(
        machine_id=machine_id,
        report_id=report_id,
        counter_id=counter_id
    ).first()
    
    if progress:
        progress.hours_since = 0.0
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'maintenance': {
                'id': entry.id,
                'machine_id': entry.machine_id,
                'report_id': entry.report_id,
                'created_at': entry.created_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== MAINTENANCES CORRECTIVES ====================

@app.route('/api/v1/maintenances/corrective', methods=['GET'])
@jwt_required()
def api_get_corrective_maintenances():
    """Récupérer les maintenances correctives"""
    machine_id = request.args.get('machine_id', type=int)
    limit = request.args.get('limit', 50, type=int)
    
    query = CorrectiveMaintenance.query.options(
        joinedload(CorrectiveMaintenance.machine),
        joinedload(CorrectiveMaintenance.user),
        joinedload(CorrectiveMaintenance.products).joinedload(CorrectiveMaintenanceProduct.product)
    )
    
    if machine_id:
        query = query.filter_by(machine_id=machine_id)
    
    maintenances = query.order_by(CorrectiveMaintenance.created_at.desc()).limit(limit).all()
    
    return jsonify({
        'success': True,
        'maintenances': [{
            'id': m.id,
            'machine_id': m.machine_id,
            'machine_name': m.machine.name if m.machine else None,
            'comment': m.comment,
            'hours': m.hours,
            'created_at': m.created_at.isoformat(),
            'user_name': m.user.username if m.user else None,
            'products': [{
                'product_id': p.product_id,
                'product_name': p.product.name if p.product else None,
                'product_code': p.product.code if p.product else None,
                'quantity': p.quantity
            } for p in m.products]
        } for m in maintenances]
    }), 200


@app.route('/api/v1/maintenances/corrective/<int:maintenance_id>', methods=['GET'])
@jwt_required()
def api_get_corrective_maintenance(maintenance_id):
    """Récupérer une maintenance corrective spécifique"""
    maintenance = CorrectiveMaintenance.query.options(
        joinedload(CorrectiveMaintenance.machine),
        joinedload(CorrectiveMaintenance.user),
        joinedload(CorrectiveMaintenance.products).joinedload(CorrectiveMaintenanceProduct.product)
    ).get_or_404(maintenance_id)
    
    return jsonify({
        'success': True,
        'maintenance': {
            'id': maintenance.id,
            'machine_id': maintenance.machine_id,
            'machine_name': maintenance.machine.name if maintenance.machine else None,
            'comment': maintenance.comment,
            'hours': maintenance.hours,
            'created_at': maintenance.created_at.isoformat(),
            'user_name': maintenance.user.username if maintenance.user else None,
            'products': [{
                'product_id': p.product_id,
                'product_name': p.product.name if p.product else None,
                'product_code': p.product.code if p.product else None,
                'quantity': p.quantity
            } for p in maintenance.products]
        }
    }), 200


@app.route('/api/v1/maintenances/corrective', methods=['POST'])
@jwt_required()
def api_create_corrective_maintenance():
    """Créer une maintenance corrective"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Données manquantes'}), 400
    
    machine_id = data.get('machine_id')
    comment = data.get('comment', '')
    hours = data.get('hours', 0.0)
    products = data.get('products', [])  # Liste de {product_id, quantity}
    
    if not machine_id:
        return jsonify({'error': 'machine_id requis'}), 400
    
    machine = Machine.query.get(machine_id)
    if not machine:
        return jsonify({'error': 'Machine non trouvée'}), 404
    
    # Créer la maintenance corrective
    maintenance = CorrectiveMaintenance(
        machine_id=machine_id,
        user_id=user_id,
        comment=comment,
        hours=hours,
        created_at=dt.datetime.utcnow()
    )
    db.session.add(maintenance)
    db.session.flush()
    
    # Ajouter les produits utilisés
    stock_id = data.get('stock_id')
    if stock_id:
        maintenance.stock_id = stock_id
    
    for prod_data in products:
        product_id = prod_data.get('product_id')
        quantity = prod_data.get('quantity', 0)
        
        if not product_id or quantity <= 0:
            continue
        
        # Vérifier et mettre à jour le stock
        if stock_id:
            stock_product = StockProduct.query.filter_by(
                stock_id=stock_id,
                product_id=product_id
            ).first()
            
            if stock_product:
                stock_product.quantity = max(0.0, stock_product.quantity - quantity)
        
        # Ajouter le produit à la maintenance
        maint_product = CorrectiveMaintenanceProduct(
            maintenance_id=maintenance.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(maint_product)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'maintenance': {
                'id': maintenance.id,
                'machine_id': maintenance.machine_id,
                'created_at': maintenance.created_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== CHECKLISTS ====================

@app.route('/api/v1/checklists', methods=['GET'])
@jwt_required()
def api_get_checklists():
    """Récupérer les checklists"""
    machine_id = request.args.get('machine_id', type=int)
    
    query = ChecklistTemplate.query.options(
        joinedload(ChecklistTemplate.machine),
        joinedload(ChecklistTemplate.items)
    )
    
    if machine_id:
        query = query.filter_by(machine_id=machine_id)
    
    templates = query.order_by(ChecklistTemplate.name).all()
    
    return jsonify({
        'success': True,
        'checklists': [{
            'id': t.id,
            'machine_id': t.machine_id,
            'machine_name': t.machine.name if t.machine else None,
            'name': t.name,
            'created_at': t.created_at.isoformat(),
            'items': [{
                'id': i.id,
                'label': i.label,
                'order': i.order
            } for i in sorted(t.items, key=lambda x: x.order)]
        } for t in templates]
    }), 200


@app.route('/api/v1/checklists/<int:template_id>/fill', methods=['POST'])
@jwt_required()
def api_fill_checklist(template_id):
    """Remplir une checklist"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Données manquantes'}), 400
    
    machine_id = data.get('machine_id')
    comment = data.get('comment', '')
    items = data.get('items', [])  # Liste de {item_id, checked}
    
    if not machine_id:
        return jsonify({'error': 'machine_id requis'}), 400
    
    template = ChecklistTemplate.query.get_or_404(template_id)
    
    # Créer l'instance de checklist
    instance = ChecklistInstance(
        template_id=template_id,
        machine_id=machine_id,
        user_id=user_id,
        comment=comment,
        created_at=dt.datetime.utcnow()
    )
    db.session.add(instance)
    db.session.flush()
    
    # Ajouter les items cochés
    for item_data in items:
        item_id = item_data.get('item_id')
        checked = item_data.get('checked', False)
        
        if checked and item_id:
            # Vérifier que l'item appartient au template
            item = ChecklistItem.query.filter_by(
                id=item_id,
                template_id=template_id
            ).first()
            
            if item:
                # Ici vous pourriez avoir une table ChecklistInstanceItem
                # Pour simplifier, on stocke juste dans le commentaire ou une table séparée
                pass
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'instance': {
                'id': instance.id,
                'template_id': template_id,
                'machine_id': machine_id,
                'created_at': instance.created_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== STOCKS ET PRODUITS ====================

@app.route('/api/v1/stocks', methods=['GET'])
@jwt_required()
def api_get_stocks():
    """Récupérer la liste des stocks"""
    stocks = Stock.query.order_by(Stock.name).all()
    
    return jsonify({
        'success': True,
        'stocks': [{
            'id': s.id,
            'name': s.name,
            'code': s.code
        } for s in stocks]
    }), 200


@app.route('/api/v1/stocks/<int:stock_id>', methods=['GET'])
@jwt_required()
def api_get_stock(stock_id):
    """Récupérer les détails d'un stock avec ses produits"""
    stock = Stock.query.options(
        joinedload(Stock.items).joinedload(StockProduct.product)
    ).get_or_404(stock_id)
    
    return jsonify({
        'success': True,
        'stock': {
            'id': stock.id,
            'name': stock.name,
            'code': stock.code,
            'products': [{
                'product_id': sp.product_id,
                'product_name': sp.product.name if sp.product else None,
                'product_code': sp.product.code if sp.product else None,
                'quantity': sp.quantity,
                'minimum_stock': sp.product.minimum_stock if sp.product else 0.0
            } for sp in stock.items]
        }
    }), 200


@app.route('/api/v1/products', methods=['GET'])
@jwt_required()
def api_get_products():
    """Récupérer la liste des produits"""
    search = request.args.get('search', '')
    limit = request.args.get('limit', 100, type=int)
    
    query = Product.query
    
    if search:
        query = query.filter(
            sql_or_(
                Product.name.ilike(f'%{search}%'),
                Product.code.ilike(f'%{search}%')
            )
        )
    
    products = query.order_by(Product.name).limit(limit).all()
    
    return jsonify({
        'success': True,
        'products': [{
            'id': p.id,
            'name': p.name,
            'code': p.code,
            'price': p.price,
            'supplier_name': p.supplier_name,
            'supplier_reference': p.supplier_reference,
            'location_code': p.location_code,
            'minimum_stock': p.minimum_stock
        } for p in products]
    }), 200


# ==================== COMPTEURS ====================

@app.route('/api/v1/machines/<int:machine_id>/counters', methods=['GET'])
@jwt_required()
def api_get_machine_counters(machine_id):
    """Récupérer les compteurs d'une machine"""
    machine = Machine.query.get_or_404(machine_id)
    
    # Compteurs multiples pour machines racines
    counters = Counter.query.filter_by(machine_id=machine_id).all()
    
    result = {
        'success': True,
        'machine_id': machine_id,
        'hour_counter_enabled': machine.hour_counter_enabled,
        'hours': machine.hours,
        'counter_unit': machine.counter_unit,
        'counters': [{
            'id': c.id,
            'name': c.name,
            'value': c.value,
            'unit': c.unit
        } for c in counters]
    }
    
    return jsonify(result), 200


@app.route('/api/v1/machines/<int:machine_id>/counters', methods=['POST'])
@jwt_required()
def api_update_counter(machine_id):
    """Mettre à jour un compteur"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Données manquantes'}), 400
    
    counter_id = data.get('counter_id')  # None pour compteur classique
    new_value = data.get('value')
    
    if new_value is None:
        return jsonify({'error': 'Valeur requise'}), 400
    
    machine = Machine.query.get_or_404(machine_id)
    
    if counter_id:
        # Compteur multiple
        counter = Counter.query.filter_by(id=counter_id, machine_id=machine_id).first()
        if not counter:
            return jsonify({'error': 'Compteur non trouvé'}), 404
        
        old_value = counter.value
        if new_value < old_value:
            return jsonify({'error': 'La nouvelle valeur doit être supérieure ou égale à l\'ancienne'}), 400
        
        counter.value = new_value
        
        # Créer un log
        log = CounterLog(
            machine_id=machine_id,
            counter_id=counter_id,
            previous_hours=old_value,
            new_hours=new_value,
            created_at=dt.datetime.utcnow()
        )
        db.session.add(log)
        
        delta = new_value - old_value
    else:
        # Compteur classique
        if not machine.hour_counter_enabled:
            return jsonify({'error': 'Cette machine n\'a pas de compteur horaire'}), 400
        
        old_value = machine.hours
        if new_value < old_value:
            return jsonify({'error': 'La nouvelle valeur doit être supérieure ou égale à l\'ancienne'}), 400
        
        machine.hours = new_value
        
        # Créer un log
        log = CounterLog(
            machine_id=machine_id,
            counter_id=None,
            previous_hours=old_value,
            new_hours=new_value,
            created_at=dt.datetime.utcnow()
        )
        db.session.add(log)
        
        delta = new_value - old_value
        
        # Mettre à jour les progress de maintenance
        progress_records = MaintenanceProgress.query.filter_by(
            machine_id=machine_id,
            counter_id=None
        ).all()
        
        for progress in progress_records:
            progress.hours_since = max(0.0, progress.hours_since - delta)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Compteur mis à jour',
            'old_value': old_value,
            'new_value': new_value
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== RAPPORTS DE MAINTENANCE ====================

@app.route('/api/v1/machines/<int:machine_id>/reports', methods=['GET'])
@jwt_required()
def api_get_machine_reports(machine_id):
    """Récupérer les rapports de maintenance préventive d'une machine"""
    machine = Machine.query.get_or_404(machine_id)
    
    if not machine.hour_counter_enabled and not machine.is_root():
        return jsonify({'error': 'Cette machine n\'a pas de compteur'}), 400
    
    reports = PreventiveReport.query.filter_by(machine_id=machine_id).options(
        joinedload(PreventiveReport.components),
        joinedload(PreventiveReport.counter)
    ).order_by(PreventiveReport.name).all()
    
    return jsonify({
        'success': True,
        'reports': [{
            'id': r.id,
            'name': r.name,
            'machine_id': r.machine_id,
            'counter_id': r.counter_id,
            'counter_name': r.counter.name if r.counter else None,
            'periodicity': r.periodicity,
            'components': [{
                'id': c.id,
                'label': c.label,
                'field_type': c.field_type
            } for c in r.components]
        } for r in reports]
    }), 200


# ==================== DASHBOARD ====================

@app.route('/api/v1/dashboard', methods=['GET'])
@jwt_required()
def api_get_dashboard():
    """Récupérer les données du dashboard pour l'utilisateur"""
    user_id = get_jwt_identity()
    
    # Récupérer les machines suivies
    followed_machines = FollowedMachine.query.filter_by(user_id=user_id).all()
    machine_ids = [fm.machine_id for fm in followed_machines]
    
    if not machine_ids:
        return jsonify({
            'success': True,
            'machines': [],
            'message': 'Aucune machine suivie'
        }), 200
    
    # Récupérer les machines avec leurs informations
    machines = Machine.query.filter(Machine.id.in_(machine_ids)).options(
        joinedload(Machine.counters)
    ).all()
    
    # Calculer les statistiques pour chaque machine
    result_machines = []
    for machine in machines:
        # Maintenances préventives (dernières 30 jours)
        thirty_days_ago = dt.datetime.utcnow() - dt.timedelta(days=30)
        preventive_count = MaintenanceEntry.query.filter(
            MaintenanceEntry.machine_id == machine.id,
            MaintenanceEntry.created_at >= thirty_days_ago
        ).count()
        
        # Maintenances correctives (dernières 30 jours)
        corrective_count = CorrectiveMaintenance.query.filter(
            CorrectiveMaintenance.machine_id == machine.id,
            CorrectiveMaintenance.created_at >= thirty_days_ago
        ).count()
        
        # Progress de maintenance
        progress_records = MaintenanceProgress.query.filter_by(
            machine_id=machine.id
        ).options(
            joinedload(MaintenanceProgress.report)
        ).all()
        
        overdue_count = sum(1 for p in progress_records if p.hours_since >= p.report.periodicity)
        
        result_machines.append({
            'id': machine.id,
            'name': machine.name,
            'code': machine.code,
            'hours': machine.hours,
            'counter_unit': machine.counter_unit,
            'preventive_count': preventive_count,
            'corrective_count': corrective_count,
            'overdue_count': overdue_count,
            'counters': [{
                'id': c.id,
                'name': c.name,
                'value': c.value,
                'unit': c.unit
            } for c in machine.counters]
        })
    
    return jsonify({
        'success': True,
        'machines': result_machines
    }), 200

