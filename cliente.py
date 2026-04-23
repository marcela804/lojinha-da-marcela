from flask import Blueprint, render_template, request, redirect, url_for
from python.db import get_db
from python.utils import role_required

bp_cliente = Blueprint("cliente", __name__, template_folder="../templates")

@bp_cliente.route("/cliente")
@role_required('admin','vendedor')
def cliente():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM cliente")
    dados = cursor.fetchall()
    return render_template("cliente.html", cliente=dados)


@bp_cliente.route("/cadastrar_cliente", methods=["POST"])
@role_required('admin','vendedor')
def cadastrar_cliente():
    nome = request.form['nome']
    cpf = request.form['cpf']

    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO cliente (nome,cpf) VALUES (%s,%s)", (nome,cpf))
    db.commit()

    return redirect(url_for('cliente.cliente'))
