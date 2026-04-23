from flask import Flask, render_template, redirect, url_for, flash, session
from routes.endereco import bp_endereco
from routes.cliente import bp_cliente
from routes.fornecedor import bp_fornecedor
from routes.login import usuario_bp

# Cria o app Flask
app = Flask(__name__)

# Chave secreta
app.secret_key = 'lojinha_da_marcela_segura_2024'


# =========================
# REGISTRO DOS BLUEPRINTS
# =========================
app.register_blueprint(bp_endereco)
app.register_blueprint(bp_cliente)
app.register_blueprint(bp_fornecedor)
app.register_blueprint(usuario_bp)


# =========================
# PÁGINA INICIAL
# =========================
@app.route("/")
def index():
    if 'usuario_id' not in session:
        flash("Faça login primeiro!", "error")
        return redirect(url_for("usuario.login"))

    return render_template("index.html")


# =========================
# ERRO 404
# =========================
@app.errorhandler(404)
def pagina_nao_encontrada(error):
    flash("Página não encontrada.", "error")
    return redirect(url_for("index"))


# =========================
# ERRO 500
# =========================
@app.errorhandler(500)
def erro_interno(error):
    flash("Erro interno. Verifique MySQL.", "error")
    return redirect(url_for("index"))


# =========================
# INICIA O FLASK
# =========================
if __name__ == '__main__':
    app.run(debug=True)
