from flask import Flask, render_template, request, redirect, url_for, flash, session
try:
    import MySQLdb
    from MySQLdb import cursors
except ImportError:
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    from MySQLdb import cursors
import re
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'chave_secreta_blog_ifrn'

# Configuração do Banco de Dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'labinfo'
app.config['MYSQL_DB'] = 'blog_db'

# Credenciais de Acesso ao Painel Admin
ADMIN_USER = 'admin'
ADMIN_PASS = 'negocios2026'

def get_db():
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

# Decorador para Rotas de Admin
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Faça login para acessar essa área.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Filtro de Template para Formatação de Data
@app.template_filter('format_datetime')
def format_datetime(value):
    if value is None:
        return ""
    return value.strftime('%d/%m/%Y %H:%M')

# Rotas de Autenticação

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            flash('Bem-vindo de volta!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
            
    return render_template('admin/login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Sessão encerrada.', 'success')
    return redirect(url_for('index'))

# Rotas do Site Público

@app.route('/')
def index():
    search_query = request.args.get('q')
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    
    if search_query:
        cursor.execute("""
            SELECT p.*, c.Nome as Categoria, a.Nome as Autor
            FROM Posts p
            LEFT JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
            LEFT JOIN Autores a ON p.ID_Autor = a.ID_Autor
            WHERE p.Status = 'Publicado' 
            AND MATCH(p.Titulo, p.Conteudo) AGAINST(%s)
            ORDER BY p.Data_Publicacao DESC
        """, (search_query,))
    else:
        cursor.execute("""
            SELECT p.*, c.Nome as Categoria, a.Nome as Autor
            FROM Posts p
            LEFT JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
            LEFT JOIN Autores a ON p.ID_Autor = a.ID_Autor
            WHERE p.Status = 'Publicado'
            ORDER BY p.Data_Publicacao DESC
        """)
    
    posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts, search_query=search_query)

@app.route('/post/<slug>')
def view_post(slug):
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute("UPDATE Posts SET Visualizacoes = Visualizacoes + 1 WHERE Slug = %s", (slug,))
    conn.commit()
    
    cursor.execute("""
        SELECT p.*, c.Nome as Categoria, a.Nome as Autor
        FROM Posts p
        LEFT JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
        LEFT JOIN Autores a ON p.ID_Autor = a.ID_Autor
        WHERE p.Slug = %s AND p.Status = 'Publicado'
    """, (slug,))
    post = cursor.fetchone()
    conn.close()
    
    if not post:
        return "Post não encontrado", 404
    
    return render_template('post.html', post=post)

# Rotas do Painel Administrativo

@app.route('/admin')
@login_required
def admin_dashboard():
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute("SELECT COUNT(*) as count FROM Posts")
    p_count = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(*) as count FROM Categorias")
    c_count = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(*) as count FROM Autores")
    a_count = cursor.fetchone()['count']
    conn.close()
    return render_template('admin/dashboard.html', 
                         posts_count=p_count,
                         categorias_count=c_count,
                         autores_count=a_count)

# CRUD Categorias

@app.route('/admin/categorias')
@login_required
def admin_categorias():
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute("SELECT * FROM Categorias ORDER BY Nome")
    categorias = cursor.fetchall()
    conn.close()
    return render_template('admin/categorias.html', categorias=categorias)

@app.route('/admin/categorias/criar', methods=['GET', 'POST'])
@login_required
def criar_categoria():
    if request.method == 'POST':
        nome = request.form.get('nome')
        desc = request.form.get('descricao')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Categorias (Nome, Descricao) VALUES (%s, %s)", (nome, desc))
        conn.commit()
        conn.close()
        flash('Categoria salva!', 'success')
        return redirect(url_for('admin_categorias'))
    return render_template('admin/criar_categoria.html')

@app.route('/admin/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    if request.method == 'POST':
        nome = request.form.get('nome')
        desc = request.form.get('descricao')
        cursor.execute("UPDATE Categorias SET Nome=%s, Descricao=%s WHERE ID_Categoria=%s", (nome, desc, id))
        conn.commit()
        conn.close()
        flash('Categoria atualizada!', 'success')
        return redirect(url_for('admin_categorias'))
    
    cursor.execute("SELECT * FROM Categorias WHERE ID_Categoria=%s", (id,))
    categoria = cursor.fetchone()
    conn.close()
    return render_template('admin/editar_categoria.html', categoria=categoria)

@app.route('/admin/categorias/deletar/<int:id>')
@login_required
def deletar_categoria(id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Categorias WHERE ID_Categoria=%s", (id,))
        conn.commit()
        flash('Categoria deletada!', 'success')
    except:
        flash('Erro ao deletar: verifique se existem posts vinculados.', 'error')
    conn.close()
    return redirect(url_for('admin_categorias'))

# CRUD Autores

@app.route('/admin/autores')
@login_required
def admin_autores():
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute("SELECT * FROM Autores ORDER BY Nome")
    autores = cursor.fetchall()
    conn.close()
    return render_template('admin/autores.html', autores=autores)

@app.route('/admin/autores/criar', methods=['GET', 'POST'])
@login_required
def criar_autor():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        bio = request.form.get('bio')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Autores (Nome, Email, Bio) VALUES (%s, %s, %s)", (nome, email, bio))
        conn.commit()
        conn.close()
        flash('Autor salvo!', 'success')
        return redirect(url_for('admin_autores'))
    return render_template('admin/criar_autor.html')

@app.route('/admin/autores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_autor(id):
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        bio = request.form.get('bio')
        cursor.execute("UPDATE Autores SET Nome=%s, Email=%s, Bio=%s WHERE ID_Autor=%s", (nome, email, bio, id))
        conn.commit()
        conn.close()
        flash('Autor atualizado!', 'success')
        return redirect(url_for('admin_autores'))
    
    cursor.execute("SELECT * FROM Autores WHERE ID_Autor=%s", (id,))
    autor = cursor.fetchone()
    conn.close()
    return render_template('admin/editar_autor.html', autor=autor)

@app.route('/admin/autores/deletar/<int:id>')
@login_required
def deletar_autor(id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Autores WHERE ID_Autor=%s", (id,))
        conn.commit()
        flash('Autor deletado!', 'success')
    except:
        flash('Erro ao deletar: verifique se existem posts vinculados.', 'error')
    conn.close()
    return redirect(url_for('admin_autores'))

# CRUD Posts

@app.route('/admin/posts')
@login_required
def admin_posts():
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute("""
        SELECT p.*, c.Nome as Categoria, a.Nome as Autor
        FROM Posts p
        LEFT JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
        LEFT JOIN Autores a ON p.ID_Autor = a.ID_Autor
        ORDER BY p.Data_Publicacao DESC
    """)
    posts = cursor.fetchall()
    conn.close()
    return render_template('admin/posts.html', posts=posts)

@app.route('/admin/posts/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        slug = request.form.get('slug')
        conteudo = request.form.get('conteudo')
        id_categoria = request.form.get('categoria_id')
        id_autor = request.form.get('autor_id')
        status = request.form.get('status')
        imagem = request.form.get('imagem')
        
        cursor.execute("""
            INSERT INTO Posts (Titulo, Slug, Conteudo, ID_Categoria, ID_Autor, Status, Imagem)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (titulo, slug, conteudo, id_categoria, id_autor, status, imagem))
        conn.commit()
        conn.close()
        flash('Post criado!', 'success')
        return redirect(url_for('admin_posts'))
    
    cursor.execute("SELECT * FROM Categorias ORDER BY Nome")
    categorias = cursor.fetchall()
    cursor.execute("SELECT * FROM Autores ORDER BY Nome")
    autores = cursor.fetchall()
    conn.close()
    return render_template('admin/criar_post.html', categorias=categorias, autores=autores)

@app.route('/admin/posts/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_post(id):
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        slug = request.form.get('slug')
        conteudo = request.form.get('conteudo')
        id_categoria = request.form.get('categoria_id')
        id_autor = request.form.get('autor_id')
        status = request.form.get('status')
        imagem = request.form.get('imagem')
        
        cursor.execute("""
            UPDATE Posts SET Titulo=%s, Slug=%s, Conteudo=%s, ID_Categoria=%s, ID_Autor=%s, Status=%s, Imagem=%s
            WHERE ID_Post=%s
        """, (titulo, slug, conteudo, id_categoria, id_autor, status, imagem, id))
        conn.commit()
        conn.close()
        flash('Post atualizado!', 'success')
        return redirect(url_for('admin_posts'))
    
    cursor.execute("SELECT * FROM Posts WHERE ID_Post=%s", (id,))
    post = cursor.fetchone()
    cursor.execute("SELECT * FROM Categorias ORDER BY Nome")
    categorias = cursor.fetchall()
    cursor.execute("SELECT * FROM Autores ORDER BY Nome")
    autores = cursor.fetchall()
    conn.close()
    return render_template('admin/editar_post.html', post=post, categorias=categorias, autores=autores)

@app.route('/admin/posts/deletar/<int:id>')
@login_required
def deletar_post(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Posts WHERE ID_Post=%s", (id,))
    conn.commit()
    conn.close()
    flash('Post deletado!', 'success')
    return redirect(url_for('admin_posts'))

if __name__ == '__main__':
    app.run(debug=True)
