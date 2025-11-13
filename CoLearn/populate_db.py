from app import create_app, db, bcrypt
from app.models import Usuario, Exercicio, Submissao
from datetime import datetime

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = Usuario(
        username="Admin",
        email="admin@example.com",
        password=bcrypt.generate_password_hash("admin123").decode('utf-8'),
        role="admin",
        nivel="Avançado",
        dificuldades="Python,Algoritmos"
    )

    user1 = Usuario(
        username="Alice",
        email="alice@example.com",
        password=bcrypt.generate_password_hash("alice123").decode('utf-8'),
        role="usuario",
        nivel="Intermediário",
        dificuldades="Python,Matemática Discreta"
    )

    user2 = Usuario(
        username="Bob",
        email="bob@example.com",
        password=bcrypt.generate_password_hash("bob123").decode('utf-8'),
        role="colaborador",
        nivel="Avançado",
        dificuldades="C++,Banco de Dados"
    )

    db.session.add_all([admin, user1, user2])
    db.session.commit()

    ex1 = Exercicio(
        titulo="Fatorial em Python",
        descricao="Crie uma função que calcule o fatorial de um número.",
        dificuldade="Python",
        autor=user2
    )

    ex2 = Exercicio(
        titulo="Soma de Matrizes",
        descricao="Faça uma função que some duas matrizes quadradas.",
        dificuldade="Algoritmos",
        autor=user2
    )

    db.session.add_all([ex1, ex2])
    db.session.commit()

    sub1 = Submissao(
        codigo="def fatorial(n): return 1 if n==0 else n*fatorial(n-1)",
        user_id=user1.id,
        exercicio_id=ex1.id,
        status="Corrigido",
        nota=9
    )

    db.session.add(sub1)
    db.session.commit()

    print("Banco de dados populado com sucesso!")
    print("Admin login -> email: admin@example.com | senha: admin123")
