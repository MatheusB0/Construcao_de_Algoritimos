from app import db
from flask_login import UserMixin
from datetime import datetime

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    nivel = db.Column(db.String(50), default='iniciante')
    dificuldades = db.Column(db.Text, default='')
    role = db.Column(db.String(50), default='usuario')
    bio = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def dificuldades_lista(self):
        return [d.strip() for d in self.dificuldades.split(',') if d.strip()]

class Exercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    dificuldade = db.Column(db.String(50), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    autor = db.relationship('Usuario', backref='exercicios')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Submissao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    exercicio_id = db.Column(db.Integer, db.ForeignKey('exercicio.id'))
    status = db.Column(db.String(50), default='pendente')
    nota = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
