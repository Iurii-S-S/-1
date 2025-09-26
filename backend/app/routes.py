from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required, current_user
from . import db
from .models import Defect, Project, Comment, Attachment, User
from .utils import role_required, allowed_file
from datetime import datetime
import os
import openpyxl
from io import BytesIO
from sqlalchemy import or_, and_

main = Blueprint('main', __name__)

@main.route('/api/defects', methods=['GET'])
@login_required
def get_defects():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Базовый запрос с жадной загрузкой связанных данных
    query = Defect.query.options(
        db.joinedload(Defect.creator),
        db.joinedload(Defect.assignee),
        db.joinedload(Defect.project)
    )
    
    # Фильтрация по ролям
    if current_user.role == 'engineer':
        query = query.filter(
            or_(
                Defect.assignee_id == current_user.id,
                Defect.creator_id == current_user.id
            )
        )
    elif current_user.role == 'observer':
        query = query.filter(Defect.status.in_(['closed', 'review']))
    
    # Применение фильтров
    filters = []
    
    status = request.args.get('status')
    if status:
        filters.append(Defect.status == status)
    
    priority = request.args.get('priority')
    if priority:
        filters.append(Defect.priority == priority)
    
    project_id = request.args.get('project_id')
    if project_id:
        filters.append(Defect.project_id == project_id)
    
    assignee_id = request.args.get('assignee_id')
    if assignee_id:
        filters.append(Defect.assignee_id == assignee_id)
    
    # Поиск с полнотекстовым поиском (для PostgreSQL)
    search = request.args.get('search')
    if search:
        search_filter = or_(
            Defect.title.ilike(f'%{search}%'),
            Defect.description.ilike(f'%{search}%')
        )
        filters.append(search_filter)
    
    # Просроченные дефекты
    overdue = request.args.get('overdue')
    if overdue:
        filters.append(and_(
            Defect.due_date < datetime.utcnow(),
            Defect.status.in_(['new', 'in_progress'])
        ))
    
    if filters:
        query = query.filter(and_(*filters))
    
    # Сортировка
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    if sort_by == 'due_date':
        order_field = Defect.due_date
    elif sort_by == 'priority':
        order_field = Defect.priority
    elif sort_by == 'status':
        order_field = Defect.status
    else:
        order_field = Defect.created_at
    
    if sort_order == 'asc':
        query = query.order_by(order_field.asc())
    else:
        query = query.order_by(order_field.desc())
    
    # Пагинация
    defects = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False,
        max_per_page=100  # Защита от слишком больших запросов
    )
    
    return jsonify({
        'defects': [defect.to_dict() for defect in defects.items],
        'total': defects.total,
        'pages': defects.pages,
        'current_page': page,
        'per_page': per_page
    })

# Остальные маршруты остаются без изменений, но добавляем новые оптимизированные

@main.route('/api/dashboard/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    """Оптимизированная статистика для дашборда"""
    
    # Используем один запрос для всей статистики
    stats_query = db.session.query(
        db.func.count(Defect.id).label('total'),
        db.func.count(db.case((Defect.status == 'in_progress', 1))).label('in_progress'),
        db.func.count(db.case((and_(
            Defect.due_date < datetime.utcnow(),
            Defect.status.in_(['new', 'in_progress'])
        ), 1))).label('overdue'),
        db.func.count(db.case((Defect.status == 'review', 1))).label('in_review'),
        db.func.count(db.case((Defect.priority == 'high', 1))).label('high_priority'),
        db.func.count(db.case((Defect.status == 'closed', 1))).label('closed')
    )
    
    # Применяем фильтры по ролям
    if current_user.role == 'engineer':
        stats_query = stats_query.filter(
            or_(
                Defect.assignee_id == current_user.id,
                Defect.creator_id == current_user.id
            )
        )
    elif current_user.role == 'observer':
        stats_query = stats_query.filter(Defect.status.in_(['closed', 'review']))
    
    stats = stats_query.first()
    
    return jsonify({
        'total_defects': stats.total,
        'in_progress': stats.in_progress,
        'overdue': stats.overdue,
        'in_review': stats.in_review,
        'high_priority': stats.high_priority,
        'closed': stats.closed
    })

@main.route('/api/projects/stats', methods=['GET'])
@login_required
@role_required(['manager'])
def get_projects_stats():
    """Статистика по проектам"""
    
    projects_stats = db.session.query(
        Project.id,
        Project.name,
        db.func.count(Defect.id).label('total_defects'),
        db.func.count(db.case((Defect.status == 'in_progress', 1))).label('in_progress'),
        db.func.count(db.case((Defect.status == 'closed', 1))).label('closed')
    ).outerjoin(Defect).group_by(Project.id, Project.name).all()
    
    return jsonify([{
        'project_id': project_id,
        'project_name': project_name,
        'total_defects': total_defects,
        'in_progress': in_progress,
        'closed': closed
    } for project_id, project_name, total_defects, in_progress, closed in projects_stats])