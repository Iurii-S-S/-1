from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    defects_created = db.relationship('Defect', backref='creator', lazy=True, foreign_keys='Defect.creator_id')
    defects_assigned = db.relationship('Defect', backref='assignee', lazy=True, foreign_keys='Defect.assignee_id')
    comments = db.relationship('Comment', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role
        }

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, index=True)
    end_date = db.Column(db.DateTime, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    defects = db.relationship('Defect', backref='project', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'defects_count': len(self.defects)
        }

class Defect(db.Model):
    __tablename__ = 'defects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new', index=True)
    priority = db.Column(db.String(20), default='medium', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    due_date = db.Column(db.DateTime, index=True)
    
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, index=True)
    
    comments = db.relationship('Comment', backref='defect', lazy=True, cascade='all, delete-orphan')
    attachments = db.relationship('Attachment', backref='defect', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'creator_id': self.creator_id,
            'creator': self.creator.first_name + ' ' + self.creator.last_name,
            'assignee_id': self.assignee_id,
            'assignee': self.assignee.first_name + ' ' + self.assignee.last_name if self.assignee else None,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'comments_count': len(self.comments),
            'attachments_count': len(self.attachments),
            'is_overdue': self.due_date and self.due_date < datetime.utcnow() and self.status in ['new', 'in_progress']
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    defect_id = db.Column(db.Integer, db.ForeignKey('defects.id'), nullable=False, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'author_id': self.author_id,
            'author': self.author.first_name + ' ' + self.author.last_name,
            'author_role': self.author.role
        }

class Attachment(db.Model):
    __tablename__ = 'attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)
    original_name = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    defect_id = db.Column(db.Integer, db.ForeignKey('defects.id'), nullable=False, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_name': self.original_name,
            'uploaded_at': self.uploaded_at.isoformat(),
            'file_url': f'/api/attachments/{self.id}'
        }

# Создаем составные индексы для улучшения производительности
db.Index('idx_defect_status_priority', Defect.status, Defect.priority)
db.Index('idx_defect_project_status', Defect.project_id, Defect.status)
db.Index('idx_defect_assignee_status', Defect.assignee_id, Defect.status)
db.Index('idx_defect_due_date_status', Defect.due_date, Defect.status)