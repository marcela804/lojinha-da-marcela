# Importa Blueprint = cria módulo separado (mini-Flask) para organização do código 
# render_template = Flask carrega arquivos HTML da pasta templates
# request = pega os dados enviados pelo formulário
# redirect = manda o usuário para outra página
# url_for = gera URL automática de rotas
# flash = mostra mensagens temporárias para o usuário
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Importa get_db = função criada em db.py para conectar no MySQL
from python.db import get_db

# Importa Error = classe para capturar erros do MySQL
from mysql.connector import Error


# Cria o Blueprint chamado "fornecedor"
# Esse nome será usado em url_for("fornecedor.nome_da_funcao")
from python.utils import role_required
bp_fornecedor = Blueprint("fornecedor", __name__, template_folder="../templates")

@role_required('admin', 'vendedor')



# =========================
# FORMULÁRIO DE CADASTRO
# =========================

# Rota GET = abre o formulário de cadastro de fornecedor
@bp_fornecedor.route("/cadastrar_fornecedor")
def form_fornecedor():
    # Abre o arquivo cadastrar_fornecedor.html
    return render_template("cadastrar_fornecedor.html")


# =========================
# CADASTRAR FORNECEDOR
# =========================

# Rota POST = recebe os dados enviados pelo formulário
@bp_fornecedor.route("/cadastrar_fornecedor", methods=["POST"])
def cadastrar_fornecedor():
    # request.form["nome"] pega o valor digitado no input name="nome"
    nome = request.form["nome"]

    # Pega o CNPJ digitado
    cnpj = request.form["cnpj"]

    # Converte quantidade para inteiro
    quantidade = int(request.form["quantidade"])

    # Converte preço para float
    preco = float(request.form["preco"])

    # Pega os dados do endereço
    rua = request.form["rua"]
    numero = request.form["numero"]
    cidade = request.form["cidade"]

    # Abre conexão com o banco
    db = get_db()

    # Se não conectou
    if not db:
        flash("Erro ao conectar no banco de dados.", "error")
        return redirect(url_for("index"))

    # Cria o cursor
    cursor = db.cursor()

    try:
        # IMPORTANTE:
        # No seu código antigo tinha "cep" aqui:
        # INSERT INTO endereco (rua, numero, cidade, cep)
        #
        # Mas sua tabela endereco provavelmente NÃO TEM a coluna cep
        # Isso causava erro.
        #
        # Então aqui está corrigido:
        cursor.execute(
            "INSERT INTO endereco (rua, numero, cidade) VALUES (%s, %s, %s)",
            (rua, numero, cidade)
        )

        # lastrowid = pega o ID do último registro inserido
        endereco_id = cursor.lastrowid

        # Agora insere o fornecedor usando o endereco_id
        cursor.execute("""
            INSERT INTO fornecedor (nome, cnpj, quantidade, preco, endereco_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, cnpj, quantidade, preco, endereco_id))

        # Salva definitivamente no banco
        db.commit()

        # Mensagem de sucesso
        flash("Fornecedor cadastrado com sucesso!", "success")

    except Error as e:
        # Se der erro, desfaz tudo
        db.rollback()

        # Mostra erro
        flash(f"Erro ao cadastrar fornecedor: {e}", "error")

    finally:
        # Fecha cursor
        cursor.close()

        # Fecha conexão
        db.close()

    # Redireciona para lista de fornecedores
    return redirect(url_for("fornecedor.fornecedor"))


# =========================
# LISTAR FORNECEDORES
# =========================

# Rota para listar todos os fornecedores
@bp_fornecedor.route("/fornecedor")
def fornecedor():
    # Abre conexão com o banco
    db = get_db()

    # Se não conectou
    if not db:
        flash("Erro ao conectar no banco de dados.", "error")
        return redirect(url_for("index"))

    # Cria cursor
    cursor = db.cursor()

    try:
        # SELECT = busca dados
        # JOIN = junta fornecedor com endereco
        cursor.execute("""
            SELECT f.id, f.nome, f.cnpj, f.quantidade, f.preco,
                   e.id, e.rua, e.numero, e.cidade
            FROM fornecedor f
            JOIN endereco e ON f.endereco_id = e.id
        """)

        # fetchall() = pega todos os resultados
        dados = cursor.fetchall()

    except Error as e:
        # Se der erro, usa lista vazia
        dados = []

        # Mostra erro
        flash(f"Erro ao listar fornecedores: {e}", "error")

    finally:
        # Fecha cursor
        cursor.close()

        # Fecha conexão
        db.close()

    # Envia os dados para fornecedor.html
    return render_template("fornecedor.html", fornecedor=dados)


# =========================
# ABRIR TELA DE EDIÇÃO
# =========================

# <int:id> = pega o ID do fornecedor pela URL
# Exemplo: /editar_fornecedor/3
@bp_fornecedor.route("/editar_fornecedor/<int:id>")
def editar_fornecedor(id):
    # Abre conexão
    db = get_db()

    # Se não conectou
    if not db:
        flash("Erro ao conectar no banco de dados.", "error")
        return redirect(url_for("fornecedor.fornecedor"))

    # Cria cursor
    cursor = db.cursor()

    try:
        # Busca UM fornecedor específico
        cursor.execute("""
            SELECT f.id, f.nome, f.cnpj, f.quantidade, f.preco,
                   e.id, e.rua, e.numero, e.cidade
            FROM fornecedor f
            JOIN endereco e ON f.endereco_id = e.id
            WHERE f.id = %s
        """, (id,))

        # fetchone() = pega apenas UM registro
        dados = cursor.fetchone()

        # Se não encontrou
        if not dados:
            flash("Fornecedor não encontrado.", "error")
            return redirect(url_for("fornecedor.fornecedor"))

    except Error as e:
        flash(f"Erro ao buscar fornecedor: {e}", "error")
        return redirect(url_for("fornecedor.fornecedor"))

    finally:
        # Fecha cursor
        cursor.close()

        # Fecha conexão
        db.close()

    # Abre a tela editar_fornecedor.html
    return render_template("editar_fornecedor.html", fornecedor=dados)


# =========================
# ATUALIZAR FORNECEDOR
# =========================

# Essa rota recebe os dados do formulário de edição
@bp_fornecedor.route("/atualizar_fornecedor/<int:id>", methods=["POST"])
def atualizar_fornecedor(id):
    # Pega os novos dados do formulário
    nome = request.form["nome"]
    cnpj = request.form["cnpj"]
    quantidade = int(request.form["quantidade"])
    preco = float(request.form["preco"])
    rua = request.form["rua"]
    numero = request.form["numero"]
    cidade = request.form["cidade"]

    # Abre conexão
    db = get_db()

    # Se não conectou
    if not db:
        flash("Erro ao conectar no banco de dados.", "error")
        return redirect(url_for("fornecedor.fornecedor"))

    # Cria cursor
    cursor = db.cursor()

    try:
        # Primeiro precisamos descobrir qual é o endereco_id desse fornecedor
        cursor.execute("SELECT endereco_id FROM fornecedor WHERE id = %s", (id,))
        resultado = cursor.fetchone()

        # Se não encontrou
        if not resultado:
            flash("Fornecedor não encontrado.", "error")
            return redirect(url_for("fornecedor.fornecedor"))

        # Pega o endereco_id
        endereco_id = resultado[0]

        # Atualiza os dados do fornecedor
        cursor.execute("""
            UPDATE fornecedor
            SET nome = %s, cnpj = %s, quantidade = %s, preco = %s
            WHERE id = %s
        """, (nome, cnpj, quantidade, preco, id))

        # Atualiza o endereço relacionado
        cursor.execute("""
            UPDATE endereco
            SET rua = %s, numero = %s, cidade = %s
            WHERE id = %s
        """, (rua, numero, cidade, endereco_id))

        # Salva alterações
        db.commit()

        # Mensagem de sucesso
        flash("Fornecedor atualizado com sucesso!", "success")

    except Error as e:
        # Desfaz se der erro
        db.rollback()

        # Mostra erro
        flash(f"Erro ao atualizar fornecedor: {e}", "error")

    finally:
        # Fecha cursor
        cursor.close()

        # Fecha conexão
        db.close()

    # Volta para lista
    return redirect(url_for("fornecedor.fornecedor"))


# =========================
# DELETAR FORNECEDOR
# =========================

# Essa rota apaga o fornecedor e o endereço ligado a ele
@bp_fornecedor.route("/deletar_fornecedor/<int:id>")
def deletar_fornecedor(id):
    # Abre conexão
    db = get_db()

    # Se não conectou
    if not db:
        flash("Erro ao conectar no banco de dados.", "error")
        return redirect(url_for("fornecedor.fornecedor"))

    # Cria cursor
    cursor = db.cursor()

    try:
        # Primeiro pega o endereco_id do fornecedor
        cursor.execute("SELECT endereco_id FROM fornecedor WHERE id = %s", (id,))
        resultado = cursor.fetchone()

        # Se não encontrou
        if not resultado:
            flash("Fornecedor não encontrado.", "error")
            return redirect(url_for("fornecedor.fornecedor"))

        # Guarda o endereco_id
        endereco_id = resultado[0]

        # Deleta o fornecedor primeiro
        # Isso é importante por causa da chave estrangeira
        cursor.execute("DELETE FROM fornecedor WHERE id = %s", (id,))

        # Depois deleta o endereço relacionado
        cursor.execute("DELETE FROM endereco WHERE id = %s", (endereco_id,))

        # Salva no banco
        db.commit()

        # Mensagem de sucesso
        flash("Fornecedor deletado com sucesso!", "success")

    except Error as e:
        # Se der erro, desfaz
        db.rollback()

        # Mostra erro
        flash(f"Erro ao deletar fornecedor: {e}", "error")

    finally:
        # Fecha cursor
        cursor.close()

        # Fecha conexão
        db.close()

    # Volta para lista
    return redirect(url_for("fornecedor.fornecedor"))
