# utils.py - Centralized permission control
from flask import session, flash, redirect, url_for
from functools import wraps

def usuario_logado():
    """Verifica se usuário está logado"""
    return 'usuario_id' in session

def tipo_usuario():
    """Retorna tipo do usuário logado"""
    return session.get('usuario_tipo', 'vendedor')

def eh_admin():
    return tipo_usuario() == 'admin'

def eh_vendedor():
    return tipo_usuario() == 'vendedor'

def eh_fornecedor():
    return tipo_usuario() == 'fornecedor'

def login_required(f):
    """Decorator: requer login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not usuario_logado():
            flash('Faça login primeiro', 'error')
            return redirect(url_for('usuario.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator: requer admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not eh_admin():
            flash('Apenas administradores', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator: requer roles específicas"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not usuario_logado():
                flash('Faça login primeiro', 'error')
                return redirect(url_for('usuario.login'))
            user_role = tipo_usuario()
            if user_role not in roles:
                flash('Sem permissão para esta operação', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Roles
ROLE_ADMIN = 'admin'
ROLE_VENDEDOR = 'vendedor'
ROLE_FORNECEDOR = 'fornecedor'
