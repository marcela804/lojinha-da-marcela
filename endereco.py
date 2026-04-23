# Importa Blueprint = cria um módulo separado de rotas
# render_template = abre arquivos HTML
# request = pega dados enviados por formulário
# redirect = redireciona para outra rota
# url_for = monta URLs automaticamente
# flash = mostra mensagens temporárias na tela
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Importa a função get_db do arquivo db.py
# Ela abre conexão com o banco MySQL
from python.db import get_db

# Importa Error para capturar erros do MySQL
from mysql.connector import Error


# Cria o blueprint chamado "endereco"
# "endereco" será usado em url_for("endereco.nome_da_funcao")
# _name_ ajuda o Flask a localizar esse arquivo
# template_folder="../templates" diz onde estão os HTMLs
from python.utils import role_required
bp_endereco = Blueprint("endereco", __name__, template_folder="../templates")

@role_required('admin', 'vendedor')



# =========================
# FORMULÁRIO DE CADASTRO
# =========================

# Essa rota abre a tela de cadastro de endereço
# Quando o usuário entra em /cadastrar_endereco
# essa função roda
@bp_endereco.route("/cadastrar_endereco")
def form_endereco():
    # render_template abre o arquivo HTML
    return render_template("cadastrar_endereco.html")


# =========================
# CADASTRAR ENDEREÇO
# =========================

# Essa rota recebe os dados do formulário
# methods=["POST"] significa:
# só aceita envio de formulário
@bp_endereco.route("/cadastrar_endereco", methods=["POST"])
def cadastrar_endereco():
    # request.form.get("rua") pega o valor digitado no input name="rua"
    rua = request.form.get("rua")

    # Pega o valor digitado no input name="numero"
    numero = request.form.get("numero")

    # Pega o valor digitado no input name="cidade"
    cidade = request.form.get("cidade")

    # Abre conexão com o banco
    db = get_db()

    # Se não conectou no banco
    if not db:
        flash("Erro ao conectar no banco de dados.", "error")
        return redirect(url_for("index"))

    # Cria o cursor
    # cursor é o objeto que executa SQL no banco
    cursor = db.cursor()

    # try = tenta executar o cadastro
    try:
        # INSERT = adiciona um novo registro na tabela
        # %s são placeholders seguros para evitar SQL Injection
        cursor.execute(
"INSERT INTO endereco (rua, numero, cidade, cep) VALUES (%s, %s, %s, %s)",
            (rua, numero, cidade, request.form.get("cep") or "")
        )

        # commit() salva definitivamente a alteração no banco
        db.commit()

        # flash mostra mensagem temporária de sucesso
        flash("Endereço cadastrado com sucesso!", "success")

    # except = executa se acontecer erro
    except Error as e:
        # rollback() desfaz alterações não salvas
        db.rollback()

        # Mostra mensagem de erro
        flash(f"Erro ao cadastrar endereço: {e}", "error")

    # finally = sempre executa, com erro ou sem erro
    finally:
        # Fecha o cursor
        cursor.close()

        # Fecha a conexão com o banco
        db.close()

    # Volta para a lista de endereços
    return redirect(url_for("endereco.endereco"))


# =========================
# LISTAR ENDEREÇOS
# =========================

# Essa rota mostra todos os endereços cadastrados
@bp_endereco.route("/endereco")
def endereco():
    # Abre conexão
    db = get_db()

    # Se falhar
    if not db:
        flash("Erro ao conectar no banco de dados.", "error")
        return redirect(url_for("index"))

    # Cria cursor
    cursor = db.cursor()

    try:
        # SELECT * = pega todas as colunas da tabela endereco
        cursor.execute("SELECT * FROM endereco")

        # fetchall() pega todos os resultados do SELECT
        dados = cursor.fetchall()

    except Error as e:
        # Se der erro, usa lista vazia
        dados = []
        flash(f"Erro ao listar endereços: {e}", "error")

    finally:
        # Fecha cursor e conexão
        cursor.close()
        db.close()

    # Envia os dados para o HTML
    # No HTML você vai usar a variável "endereco"
    return render_template("endereco.html", endereco=dados)


# =========================
# ABRIR TELA DE EDIÇÃO
# =========================

# <int:id> quer dizer:
# a URL vai receber um número inteiro
# exemplo: /editar_endereco/5
@bp_endereco.route("/editar_endereco/<int:id>")
def editar_endereco(id):
    # Abre conexão
    db = get_db()

    if not db:
        flash("Erro ao conectar no banco de dados.", "error")
        return redirect(url_for("endereco.endereco"))

    # Cria cursor
    cursor = db.cursor()

    try:
        # SELECT com WHERE
        # Busca apenas o endereço que tem esse id
        cursor.execute("SELECT * FROM endereco WHERE id = %s", (id,))

        # fetchone() pega apenas UM resultado
        endereco = cursor.fetchone()

        # Se não encontrou
        if not endereco:
            flash("Endereço não encontrado.", "error")
            return redirect(url_for("endereco.endereco"))

    except Error as e:
        flash(f"Erro ao carregar endereço: {e}", "error")
        return redirect(url_for("endereco.endereco"))

    finally:
        cursor.close()
        db.close()

    # Abre a tela de edição já preenchida
    return render_template("editar_endereco.html", endereco=endereco)


# =========================
# ATUALIZAR ENDEREÇO
# =========================

# Essa rota recebe o formulário de edição
@bp_endereco.route("/atualizar_endereco/<int:id>", methods=["POST"])
def atualizar_endereco(id):
    # Pega os novos dados do formulário
    rua = request.form.get("rua")
    numero = request.form.get("numero")
    cidade = request.form.get("cidade")

    # Abre conexão
    db = get_db()

    if not db:
        flash("Erro ao conectar no banco de dados.", "error")
        return redirect(url_for("endereco.endereco"))

    # Cria cursor
    cursor = db.cursor()

    try:
        # UPDATE = altera um registro existente
        cursor.execute(
"UPDATE endereco SET rua = %s, numero = %s, cidade = %s, cep = %s WHERE id = %s",
            (rua, numero, cidade, request.form.get("cep") or "", id)
        )

        # Salva a alteração
        db.commit()

        # Mensagem de sucesso
        flash("Endereço atualizado com sucesso!", "success")

    except Error as e:
        # Desfaz em caso de erro
        db.rollback()
        flash(f"Erro ao atualizar endereço: {e}", "error")

    finally:
        cursor.close()
        db.close()

    # Volta para a lista
    return redirect(url_for("endereco.endereco"))


# =========================
# DELETAR ENDEREÇO
# =========================

# Essa rota apaga um endereço
@bp_endereco.route("/deletar_endereco/<int:id>")
def deletar_endereco(id):
    # Abre conexão
    db = get_db()

    if not db:
        flash("Erro ao conectar no banco de dados.", "error")
        return redirect(url_for("endereco.endereco"))

    # Cria cursor
    cursor = db.cursor()

    try:
        # DELETE = remove um registro do banco
        cursor.execute("DELETE FROM endereco WHERE id = %s", (id,))

        # Salva a exclusão
        db.commit()

        flash("Endereço deletado com sucesso!", "success")

    except Error as e:
        db.rollback()
        flash(f"Erro ao deletar endereço: {e}", "error")

    finally:
        cursor.close()
        db.close()

    # Volta para a lista
    return redirect(url_for("endereco.endereco"))
