
import os

import mysql.connector
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    session,
    flash
)

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "chave-local-de-desenvolvimento"
)


def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "app_user"),
        password=os.getenv("MYSQL_PASSWORD", "senha_app"),
        database=os.getenv("MYSQL_DATABASE", "app_posts_seguro")
    )


def iniciar_banco():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    senha = 'admin123'
    
    query = """
        UPDATE usuarios
        SET senha = %s 
        WHERE usuario = 'admin';
    """

    senha_hash = generate_password_hash(senha)

    cursor.execute(query, (senha_hash,))
    conexao.commit()
    
    cursor.close()
    conexao.close()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Aplicação online!"})


@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        senha = request.form.get('senha', '')

        conexao = conectar_banco()

        try:
            cursor = conexao.cursor(dictionary=True)

            # SEGURO: consulta parametrizada
            query = """
                SELECT id, usuario, senha
                FROM usuarios
                WHERE usuario = %s
            """

            cursor.execute(query, (usuario,))
            resultado = cursor.fetchone()

            cursor.close()

        finally:
            conexao.close()

        # SEGURO: comparação do hash da senha
        if resultado and check_password_hash(resultado['senha'], senha):
            session.clear()
            session['usuario_id'] = resultado['id']
            session['usuario'] = resultado['usuario']

            return redirect(url_for('listar_posts'))

        flash('Usuário ou senha inválidos.', 'danger')

    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/posts/criar/', methods=['GET', 'POST'])
def criar_post():

    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        usuario_id = session['usuario_id']
        titulo = request.form.get('titulo', '').strip()
        conteudo = request.form.get('conteudo', '')

        if not titulo or not conteudo.strip():
            flash('Preencha o título e o conteúdo.', 'danger')
            return render_template('criar_post.html')

        conexao = conectar_banco()

        try:
            cursor = conexao.cursor()

            # SEGURO: INSERT com parâmetros
            query = """
                INSERT INTO posts (titulo, conteudo, usuario_id)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                query,
                (titulo, conteudo, usuario_id)
            )

            conexao.commit()
            cursor.close()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

        flash('Publicação criada com sucesso!', 'success')
        return redirect(url_for('listar_posts'))

    return render_template('criar_post.html')


@app.route('/posts/', methods=['GET'])
def listar_posts():

    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conexao = conectar_banco()

    try:
        cursor = conexao.cursor(dictionary=True)

        query = """
            SELECT posts.*, usuarios.usuario
            FROM posts
            INNER JOIN usuarios
            ON posts.usuario_id = usuarios.id
            ORDER BY posts.data_criacao DESC
        """

        cursor.execute(query)
        posts = cursor.fetchall()

        cursor.close()

    finally:
        conexao.close()

    return render_template('posts.html', posts=posts)


if __name__ == '__main__':
    iniciar_banco()
    app.run(debug=False, host='0.0.0.0', port=5000)
