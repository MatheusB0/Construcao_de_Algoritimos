import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes import bp as main_bp, exercicio_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(exercicio_bp, url_prefix='/exercicio')

    with app.app_context():
        from app.models import Usuario, Exercicio, Submissao
        db.create_all()

    return app

from app.models import Usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

