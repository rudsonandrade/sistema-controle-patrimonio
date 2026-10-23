import csv
import io
import os
import sqlite3
from datetime import date
from pathlib import Path

from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "patrimonio.db"

STATUS_BEM = ["Ativo", "Em manutenção", "Emprestado", "Baixado"]

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "troque-esta-chave")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with open(BASE_DIR / "schema.sql", encoding="utf-8") as arquivo:
        db = sqlite3.connect(DATABASE)
        db.executescript(arquivo.read())
        db.close()


@app.template_filter("moeda")
def moeda(valor):
    try:
        return f"R$ {float(valor or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "R$ 0,00"


@app.context_processor
def injetar_globais():
    return {"status_bem": STATUS_BEM, "hoje": date.today().isoformat()}


def carregar_categorias():
    return get_db().execute("SELECT * FROM categorias ORDER BY nome").fetchall()


def carregar_locais():
    return get_db().execute("SELECT * FROM locais ORDER BY nome").fetchall()


@app.route("/")
def index():
    db = get_db()
    total_bens = db.execute("SELECT COUNT(*) FROM bens").fetchone()[0]
    valor_total = db.execute("SELECT COALESCE(SUM(valor), 0) FROM bens").fetchone()[0]
    total_categorias = db.execute("SELECT COUNT(*) FROM categorias").fetchone()[0]
    total_locais = db.execute("SELECT COUNT(*) FROM locais").fetchone()[0]
    por_status = db.execute(
        "SELECT status, COUNT(*) AS total FROM bens GROUP BY status ORDER BY status"
    ).fetchall()
    por_categoria = db.execute(
        """
        SELECT c.nome, COUNT(b.id) AS total
        FROM categorias c
        LEFT JOIN bens b ON b.categoria_id = c.id
        GROUP BY c.id
        ORDER BY total DESC, c.nome
        """
    ).fetchall()
    movimentacoes = db.execute(
        """
        SELECT m.*, b.nome AS bem_nome, b.codigo AS bem_codigo,
               lo.nome AS origem_nome, ld.nome AS destino_nome
        FROM movimentacoes m
        JOIN bens b ON b.id = m.bem_id
        LEFT JOIN locais lo ON lo.id = m.local_origem_id
        LEFT JOIN locais ld ON ld.id = m.local_destino_id
        ORDER BY m.data DESC, m.id DESC
        LIMIT 8
        """
    ).fetchall()
    return render_template(
        "index.html",
        total_bens=total_bens,
        valor_total=valor_total,
        total_categorias=total_categorias,
        total_locais=total_locais,
        por_status=por_status,
        por_categoria=por_categoria,
        movimentacoes=movimentacoes,
    )


@app.route("/bens")
def bens():
    db = get_db()
    q = request.args.get("q", "").strip()
    categoria_id = request.args.get("categoria_id", "").strip()
    local_id = request.args.get("local_id", "").strip()
    status = request.args.get("status", "").strip()

    sql = """
        SELECT b.*, c.nome AS categoria_nome, l.nome AS local_nome
        FROM bens b
        LEFT JOIN categorias c ON c.id = b.categoria_id
        LEFT JOIN locais l ON l.id = b.local_id
        WHERE 1 = 1
    """
    parametros = []
    if q:
        sql += " AND (b.nome LIKE ? OR b.codigo LIKE ? OR b.descricao LIKE ?)"
        termo = f"%{q}%"
        parametros += [termo, termo, termo]
    if categoria_id:
        sql += " AND b.categoria_id = ?"
        parametros.append(categoria_id)
    if local_id:
        sql += " AND b.local_id = ?"
        parametros.append(local_id)
    if status:
        sql += " AND b.status = ?"
        parametros.append(status)
    sql += " ORDER BY b.nome"

    registros = db.execute(sql, parametros).fetchall()
    return render_template(
        "bens_lista.html",
        bens=registros,
        categorias=carregar_categorias(),
        locais=carregar_locais(),
        filtros={"q": q, "categoria_id": categoria_id, "local_id": local_id, "status": status},
    )


@app.route("/bens/novo", methods=["GET", "POST"])
def bem_novo():
    if request.method == "POST":
        dados = _dados_bem()
        erro = _validar_bem(dados)
        if erro:
            flash(erro, "danger")
        else:
            db = get_db()
            try:
                db.execute(
                    """
                    INSERT INTO bens (codigo, nome, descricao, categoria_id, local_id,
                                      status, valor, data_aquisicao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        dados["codigo"],
                        dados["nome"],
                        dados["descricao"],
                        dados["categoria_id"],
                        dados["local_id"],
                        dados["status"],
                        dados["valor"],
                        dados["data_aquisicao"],
                    ),
                )
                db.commit()
                flash("Bem cadastrado com sucesso.", "success")
                return redirect(url_for("bens"))
            except sqlite3.IntegrityError:
                flash("Já existe um bem com esse código patrimonial.", "danger")
    return render_template(
        "bem_form.html",
        bem=None,
        categorias=carregar_categorias(),
        locais=carregar_locais(),
    )


@app.route("/bens/<int:bem_id>")
def bem_detalhe(bem_id):
    db = get_db()
    bem = db.execute(
        """
        SELECT b.*, c.nome AS categoria_nome, l.nome AS local_nome
        FROM bens b
        LEFT JOIN categorias c ON c.id = b.categoria_id
        LEFT JOIN locais l ON l.id = b.local_id
        WHERE b.id = ?
        """,
        (bem_id,),
    ).fetchone()
    if bem is None:
        flash("Bem não encontrado.", "warning")
        return redirect(url_for("bens"))
    movimentacoes = db.execute(
        """
        SELECT m.*, lo.nome AS origem_nome, ld.nome AS destino_nome
        FROM movimentacoes m
        LEFT JOIN locais lo ON lo.id = m.local_origem_id
        LEFT JOIN locais ld ON ld.id = m.local_destino_id
        WHERE m.bem_id = ?
        ORDER BY m.data DESC, m.id DESC
        """,
        (bem_id,),
    ).fetchall()
    return render_template(
        "bem_detalhe.html",
        bem=bem,
        movimentacoes=movimentacoes,
        locais=carregar_locais(),
    )


@app.route("/bens/<int:bem_id>/editar", methods=["GET", "POST"])
def bem_editar(bem_id):
    db = get_db()
    bem = db.execute("SELECT * FROM bens WHERE id = ?", (bem_id,)).fetchone()
    if bem is None:
        flash("Bem não encontrado.", "warning")
        return redirect(url_for("bens"))

    if request.method == "POST":
        dados = _dados_bem()
        erro = _validar_bem(dados)
        if erro:
            flash(erro, "danger")
        else:
            try:
                db.execute(
                    """
                    UPDATE bens
                    SET codigo = ?, nome = ?, descricao = ?, categoria_id = ?,
                        local_id = ?, status = ?, valor = ?, data_aquisicao = ?
                    WHERE id = ?
                    """,
                    (
                        dados["codigo"],
                        dados["nome"],
                        dados["descricao"],
                        dados["categoria_id"],
                        dados["local_id"],
                        dados["status"],
                        dados["valor"],
                        dados["data_aquisicao"],
                        bem_id,
                    ),
                )
                db.commit()
                flash("Bem atualizado com sucesso.", "success")
                return redirect(url_for("bem_detalhe", bem_id=bem_id))
            except sqlite3.IntegrityError:
                flash("Já existe um bem com esse código patrimonial.", "danger")
    return render_template(
        "bem_form.html",
        bem=bem,
        categorias=carregar_categorias(),
        locais=carregar_locais(),
    )


@app.route("/bens/<int:bem_id>/excluir", methods=["POST"])
def bem_excluir(bem_id):
    db = get_db()
    db.execute("DELETE FROM bens WHERE id = ?", (bem_id,))
    db.commit()
    flash("Bem excluído.", "success")
    return redirect(url_for("bens"))


@app.route("/bens/<int:bem_id>/movimentar", methods=["POST"])
def bem_movimentar(bem_id):
    db = get_db()
    bem = db.execute("SELECT * FROM bens WHERE id = ?", (bem_id,)).fetchone()
    if bem is None:
        flash("Bem não encontrado.", "warning")
        return redirect(url_for("bens"))

    destino_id = request.form.get("local_destino_id") or None
    data_mov = request.form.get("data") or date.today().isoformat()
    observacao = request.form.get("observacao", "").strip()

    if not destino_id:
        flash("Selecione o local de destino.", "danger")
        return redirect(url_for("bem_detalhe", bem_id=bem_id))
    if str(destino_id) == str(bem["local_id"]):
        flash("O destino deve ser diferente do local atual.", "warning")
        return redirect(url_for("bem_detalhe", bem_id=bem_id))

    db.execute(
        """
        INSERT INTO movimentacoes (bem_id, local_origem_id, local_destino_id, data, observacao)
        VALUES (?, ?, ?, ?, ?)
        """,
        (bem_id, bem["local_id"], destino_id, data_mov, observacao),
    )
    db.execute("UPDATE bens SET local_id = ? WHERE id = ?", (destino_id, bem_id))
    db.commit()
    flash("Movimentação registrada.", "success")
    return redirect(url_for("bem_detalhe", bem_id=bem_id))


@app.route("/categorias", methods=["GET", "POST"])
def categorias():
    db = get_db()
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        if not nome:
            flash("Informe o nome da categoria.", "danger")
        else:
            db.execute("INSERT INTO categorias (nome, descricao) VALUES (?, ?)", (nome, descricao))
            db.commit()
            flash("Categoria cadastrada.", "success")
            return redirect(url_for("categorias"))
    registros = db.execute(
        """
        SELECT c.*, COUNT(b.id) AS total_bens
        FROM categorias c
        LEFT JOIN bens b ON b.categoria_id = c.id
        GROUP BY c.id
        ORDER BY c.nome
        """
    ).fetchall()
    return render_template("categorias.html", categorias=registros)


@app.route("/categorias/<int:categoria_id>/excluir", methods=["POST"])
def categoria_excluir(categoria_id):
    db = get_db()
    try:
        db.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
        db.commit()
        flash("Categoria excluída.", "success")
    except sqlite3.IntegrityError:
        flash("Não é possível excluir: existem bens vinculados a esta categoria.", "danger")
    return redirect(url_for("categorias"))


@app.route("/locais", methods=["GET", "POST"])
def locais():
    db = get_db()
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        descricao = request.form.get("descricao", "").strip()
        if not nome:
            flash("Informe o nome do local.", "danger")
        else:
            db.execute(
                "INSERT INTO locais (nome, responsavel, descricao) VALUES (?, ?, ?)",
                (nome, responsavel, descricao),
            )
            db.commit()
            flash("Local cadastrado.", "success")
            return redirect(url_for("locais"))
    registros = db.execute(
        """
        SELECT l.*, COUNT(b.id) AS total_bens
        FROM locais l
        LEFT JOIN bens b ON b.local_id = l.id
        GROUP BY l.id
        ORDER BY l.nome
        """
    ).fetchall()
    return render_template("locais.html", locais=registros)


@app.route("/locais/<int:local_id>/excluir", methods=["POST"])
def local_excluir(local_id):
    db = get_db()
    try:
        db.execute("DELETE FROM locais WHERE id = ?", (local_id,))
        db.commit()
        flash("Local excluído.", "success")
    except sqlite3.IntegrityError:
        flash("Não é possível excluir: existem bens vinculados a este local.", "danger")
    return redirect(url_for("locais"))


@app.route("/movimentacoes")
def movimentacoes():
    db = get_db()
    registros = db.execute(
        """
        SELECT m.*, b.nome AS bem_nome, b.codigo AS bem_codigo,
               lo.nome AS origem_nome, ld.nome AS destino_nome
        FROM movimentacoes m
        JOIN bens b ON b.id = m.bem_id
        LEFT JOIN locais lo ON lo.id = m.local_origem_id
        LEFT JOIN locais ld ON ld.id = m.local_destino_id
        ORDER BY m.data DESC, m.id DESC
        """
    ).fetchall()
    return render_template("movimentacoes.html", movimentacoes=registros)


@app.route("/exportar.csv")
def exportar_csv():
    db = get_db()
    registros = db.execute(
        """
        SELECT b.codigo, b.nome, b.descricao, c.nome AS categoria,
               l.nome AS local, b.status, b.valor, b.data_aquisicao
        FROM bens b
        LEFT JOIN categorias c ON c.id = b.categoria_id
        LEFT JOIN locais l ON l.id = b.local_id
        ORDER BY b.nome
        """
    ).fetchall()

    saida = io.StringIO()
    escritor = csv.writer(saida, delimiter=";")
    escritor.writerow(
        ["Código", "Nome", "Descrição", "Categoria", "Local", "Status", "Valor", "Data de aquisição"]
    )
    for registro in registros:
        escritor.writerow(
            [
                registro["codigo"],
                registro["nome"],
                registro["descricao"],
                registro["categoria"],
                registro["local"],
                registro["status"],
                registro["valor"],
                registro["data_aquisicao"],
            ]
        )
    conteudo = saida.getvalue().encode("utf-8-sig")
    return send_file(
        io.BytesIO(conteudo),
        mimetype="text/csv",
        as_attachment=True,
        download_name="patrimonio.csv",
    )


def _dados_bem():
    return {
        "codigo": request.form.get("codigo", "").strip(),
        "nome": request.form.get("nome", "").strip(),
        "descricao": request.form.get("descricao", "").strip(),
        "categoria_id": request.form.get("categoria_id") or None,
        "local_id": request.form.get("local_id") or None,
        "status": request.form.get("status", "Ativo"),
        "valor": request.form.get("valor") or 0,
        "data_aquisicao": request.form.get("data_aquisicao") or None,
    }


def _validar_bem(dados):
    if not dados["codigo"]:
        return "Informe o código patrimonial."
    if not dados["nome"]:
        return "Informe o nome do bem."
    if dados["status"] not in STATUS_BEM:
        return "Status inválido."
    try:
        dados["valor"] = float(str(dados["valor"]).replace(",", ".") or 0)
    except ValueError:
        return "Valor inválido."
    return None


if not DATABASE.exists():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
