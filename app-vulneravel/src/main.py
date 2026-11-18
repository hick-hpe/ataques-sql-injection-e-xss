import os

import mysql.connector
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
# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "chave-local-de-desenvolvimento")


def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "app_user"),
        password=os.getenv("MYSQL_PASSWORD", "senha_app"),
        database=os.getenv("MYSQL_DATABASE", "app_posts")
    )


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Aplicação online!"})



@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        query = f"""
            SELECT * FROM usuarios
            WHERE usuario = '{usuario}'
            AND senha = '{senha}'
        """

        cursor.execute(query)
        resultado = cursor.fetchall()[0]

        cursor.close()
        conexao.close()

        if resultado:
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
        titulo = request.form.get('titulo')
        conteudo = request.form.get('conteudo')

        conexao = conectar_banco()
        cursor = conexao.cursor()

        # VULNERÁVEL: concatenação direta
        query = f"""
            INSERT INTO posts (titulo, conteudo, usuario_id)
            VALUES ('{titulo}', '{conteudo}', '{usuario_id}')
        """

        cursor.execute(query)
        conexao.commit()

        cursor.close()
        conexao.close()

        flash('Publicação criada com sucesso!', 'success')
        return redirect(url_for('listar_posts'))

    return render_template('criar_post.html')


@app.route('/posts/', methods=['GET'])
def listar_posts():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conexao = conectar_banco()
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
    conexao.close()

    return render_template('posts.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)