from flask import Blueprint, render_template
from python.db import get_db
from python.utils import role_required

bp_estoque = Blueprint("estoque", __name__, template_folder="../templates")

@bp_estoque.route("/estoque")
@role_required('admin', 'vendedor', 'fornecedor')
def estoque():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM fornecedor")
    dados = cursor.fetchall()
    return render_template("estoque.html", estoque=dados)
