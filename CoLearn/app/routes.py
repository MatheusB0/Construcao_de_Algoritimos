from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import Usuario, Exercicio, Submissao

bp = Blueprint('main', __name__)
exercicio_bp = Blueprint('exercicio', __name__)

DIFICULDADES_OPCOES = [
    "Python", "Java", "C++", "Algoritmos", "Matemática Discreta",
    "Banco de Dados", "Redes", "Segurança", "Lógica"
]

# ---------- Rotas de autenticação ----------
@bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        senha = request.form.get('senha','')
        user = Usuario.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, senha):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.dashboard'))
        flash('E-mail ou senha incorretos.', 'danger')
    return render_template('login.html')

@bp.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        email = request.form.get('email','').strip().lower()
        senha = request.form.get('senha','')
        nivel = request.form.get('nivel','')
        dificuldades = request.form.getlist('dificuldades') or []
        custom = request.form.get('custom_dificuldade','').strip()
        if custom:
            dificuldades.append(custom)
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'warning')
            return redirect(url_for('main.cadastro'))
        hash_senha = bcrypt.generate_password_hash(senha).decode('utf-8')
        novo = Usuario(
            username=username, email=email, password=hash_senha,
            nivel=nivel,
            dificuldades=",".join(dict.fromkeys([d.strip() for d in dificuldades if d.strip()]))
        )
        db.session.add(novo)
        db.session.commit()
        flash('Conta criada. Faça login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('cadastro.html', opcoes=DIFICULDADES_OPCOES)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# ---------- Rotas de perfil ----------
@bp.route('/editar_perfil', methods=['GET','POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        current_user.username = request.form.get('username','').strip()
        current_user.nivel = request.form.get('nivel','')
        dificuldades = request.form.getlist('dificuldades') or []
        custom = request.form.get('custom_dificuldade','').strip()
        if custom:
            dificuldades.append(custom)
        current_user.dificuldades = ",".join(dict.fromkeys([d.strip() for d in dificuldades if d.strip()]))
        current_user.bio = request.form.get('bio','').strip()
        db.session.commit()
        flash('Perfil atualizado.', 'success')
        if current_user.role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.dashboard'))
    return render_template('editar_perfil.html', opcoes=DIFICULDADES_OPCOES)

# ---------- Rotas de dashboard ----------
@bp.route('/dashboard')
@login_required
def dashboard():
    minhas = set(current_user.dificuldades_lista())
    colegas = Usuario.query.filter(Usuario.id != current_user.id).all()
    colegas_compat = [u for u in colegas if minhas & set(u.dificuldades_lista())]
    return render_template('dashboard.html', colegas=colegas_compat)

@bp.route('/exercicios')
@login_required
def exercicios():
    difs = current_user.dificuldades_lista()
    exs = Exercicio.query.filter(Exercicio.dificuldade.in_(difs)).order_by(Exercicio.created_at.desc()).all() if difs else []
    return render_template('exercicios.html', exercicios=exs)

@bp.route('/criar_exercicio', methods=['GET','POST'])
@login_required
def criar_exercicio():
    if current_user.role not in ('colaborador','admin'):
        flash('Apenas colaboradores ou admin podem criar exercícios.', 'danger')
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        titulo = request.form.get('titulo','').strip()
        descricao = request.form.get('descricao','').strip()
        dificuldade = request.form.get('dificuldade','').strip()
        if not (titulo and descricao and dificuldade):
            flash('Preencha todos os campos.', 'warning')
            return redirect(url_for('main.criar_exercicio'))
        ex = Exercicio(titulo=titulo, descricao=descricao, dificuldade=dificuldade, autor=current_user)
        db.session.add(ex)
        db.session.commit()
        flash('Exercício criado.', 'success')
        return redirect(url_for('main.exercicios'))
    return render_template('criar_exercicio.html', opcoes=DIFICULDADES_OPCOES)

# ---------- Rotas de admin ----------
@bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Acesso admin requerido.', 'danger')
        return redirect(url_for('main.dashboard'))
    usuarios = Usuario.query.order_by(Usuario.created_at.desc()).all()
    exercicios = Exercicio.query.order_by(Exercicio.created_at.desc()).all()
    return render_template('admin_dashboard.html', usuarios=usuarios, exercicios=exercicios)

@bp.route('/admin/toggle_role/<int:user_id>', methods=['POST'])
@login_required
def admin_toggle_role(user_id):
    if current_user.role != 'admin':
        flash('Acesso admin requerido.', 'danger')
        return redirect(url_for('main.dashboard'))
    u = Usuario.query.get_or_404(user_id)
    u.role = 'colaborador' if u.role == 'usuario' else 'usuario'
    db.session.commit()
    flash('Papel atualizado.', 'success')
    return redirect(url_for('main.admin_dashboard'))

# ---------- Rotas de exercícios/submissões ----------
@exercicio_bp.route('/<int:id>', methods=['GET','POST'])
@login_required
def view_exercicio(id):
    exercicio = Exercicio.query.get_or_404(id)
    if request.method == 'POST':
        codigo = request.form['codigo']
        submissao = Submissao(codigo=codigo, user_id=current_user.id, exercicio_id=id)
        db.session.add(submissao)
        db.session.commit()
        flash('Submissão enviada!', 'success')
        return redirect(url_for('exercicio.view_exercicio', id=id))
    if current_user.role in ['admin', 'colaborador']:
        submissoes = Submissao.query.filter_by(exercicio_id=id).order_by(Submissao.created_at.desc()).all()
    else:
        submissoes = Submissao.query.filter_by(user_id=current_user.id, exercicio_id=id).order_by(Submissao.created_at.desc()).all()
    return render_template('view_exercicio.html', exercicio=exercicio, submissoes=submissoes)

@exercicio_bp.route('/submissao/<int:id>/editar', methods=['GET','POST'])
@login_required
def editar_submissao(id):
    submissao = Submissao.query.get_or_404(id)
    if current_user.role not in ['admin', 'colaborador']:
        flash('Acesso negado', 'danger')
        return redirect(url_for('exercicio.view_exercicio', id=submissao.exercicio_id))
    if request.method == 'POST':
        submissao.status = request.form['status']
        nota_form = request.form.get('nota')
        submissao.nota = int(nota_form) if nota_form else None
        db.session.commit()
        flash('Submissão atualizada!', 'success')
        return redirect(url_for('exercicio.view_exercicio', id=submissao.exercicio_id))
    return render_template('editar_submissao.html', submissao=submissao)


