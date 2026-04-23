# LOGIN COMPLETO - Hash + Session + Blueprint + Tipo de Usuário
# importa funções principais do Flask 
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# Importa funções para gerar hash e verificar senha
from werkzeug.security import generate_password_hash, check_password_hash

# Importa a função de conexão com o banco
from python.db import get_db

# Importa erros do mysql
from mysql.connector import Error

# Importa decorator de permissão
from python.utils import role_required, login_required

# ✅ CORREÇÃO AQUI (_name_ → __name__)
usuario_bp = Blueprint('usuario', __name__, template_folder="../templates")


# =========================
# ROTA: CADASTRAR USUÁRIO
# =========================
@usuario_bp.route('/cadastrar_usuario', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar = request.form['confirmar_senha']

        if senha != confirmar:
            flash('Senhas não coincidem', 'error')
            return render_template('cadastrar_usuario.html')

        senha_hash = generate_password_hash(senha)

        db = get_db()
        if not db:
            flash('Erro ao conectar no banco de dados', 'error')
            return render_template('cadastrar_usuario.html')

        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM login WHERE email = %s", (email,))
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                flash('Este email já está cadastrado', 'error')
                return render_template('cadastrar_usuario.html')

            cursor.execute("""
                INSERT INTO login (nome, email, senha, tipo)
                VALUES (%s, %s, %s, %s)
            """, (nome, email, senha_hash, 'vendedor'))

            db.commit()

            flash('Vendedor cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))  # 🔥 melhor redirecionar pro index

        except Error as e:
            db.rollback()
            flash(f'Erro ao cadastrar vendedor: {e}', 'error')
            print(f"[DEBUG CADASTRO] Error: {e}")

        finally:
            cursor.close()
            db.close()

    return render_template('cadastrar_usuario.html')


# =========================
# ROTA: LOGIN
# =========================
@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        db = get_db()
        if not db:
            flash('Erro ao conectar no banco de dados', 'error')
            return render_template('login.html')

        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM login WHERE email = %s", (email,))
            usuario = cursor.fetchone()

            if usuario:
                if check_password_hash(usuario['senha'], senha):
                    session['usuario_id'] = usuario['id']
                    session['usuario_nome'] = usuario['nome']
                    session['usuario_tipo'] = usuario['tipo']

                    flash('Login realizado com sucesso!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Senha incorreta', 'error')
            else:
                flash('Usuário não encontrado', 'error')

        except Error as e:
            flash(f'Erro no login: {e}', 'error')
            print(f"[DEBUG LOGIN] Error: {e}")

        finally:
            cursor.close()
            db.close()

    return render_template('login.html')


# =========================
# ROTA: LOGOUT
# =========================
@usuario_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('usuario.login'))
