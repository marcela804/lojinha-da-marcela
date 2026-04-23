from flask import session, redirect, url_for, flash
from functools import wraps

# 🔒 Obriga login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Faça login primeiro!", "error")
            return redirect(url_for('usuario.login'))
        return f(*args, **kwargs)
    return decorated_function


# 🔒 Controle por tipo (admin / vendedor)
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'usuario_tipo' not in session:
                flash("Acesso negado!", "error")
                return redirect(url_for('usuario.login'))

            if session['usuario_tipo'] not in roles:
                flash("Você não tem permissão para acessar isso!", "error")
                return redirect(url_for('index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator
