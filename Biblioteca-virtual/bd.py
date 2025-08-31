from flask_mysqldb import MySQL

mysql = MySQL()

def init_app(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = 3307
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'biblioteca_virtual'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    mysql.init_app(app)
    return mysql

# ==================BUSCAS DADOS=================

# Cara aqui vai procura o id do livro e retorna os generos do livro
def retornar_idgenero(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro_genero WHERE id_livro = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()
    return row["id_genero"] if row else None

# Aqui retorna o id da editora
def retornar_ideditora(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro WHERE id_livro = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()
    return row["id_editora"] if row else None

def buscar_editora(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM editora WHERE id_editora = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()
    return row["Nome"] if row else None

def retornar_idisbn(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro WHERE ISBN = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()
    return row["id_livro"] if row else None

def buscar_genero(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM genero WHERE id_genero = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()
    return row["genero"] if row else None

def formatar_isbn(isbn: str) -> str:
    if not isbn:
        return isbn
    # garante que é string
    isbn = str(isbn)
    return f"{isbn[0:3]}-{isbn[3:5]}-{isbn[5:10]}-{isbn[10:12]}"


# Busca as informações do usuario
# função em potencial para trocar o nome, ver depois de não é ideal ver a troca dos nomes
def verificar_usuario(usuario_id, senha):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM usuarios WHERE id_usuario = %s; ", (usuario_id,))
    listar = conectar.fetchone()
    conectar.close()

    if not listar:
        return None
    return listar if listar['senha'] == senha else None

# Busca os livros por ID
def buscar_livro_id(id_livro: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro WHERE id_livro = %s;", (id_livro,))
    listar = conectar.fetchone()
    conectar.close()

    if listar and listar.get("ISBN"):
        listar["ISBN"] = formatar_isbn(listar["ISBN"])
    return listar

# Aqui ele busca livros pelo nome junto com o select
def buscar_livro_nome():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro ORDER BY titulo;")
    listar_lvr = conectar.fetchall()
    conectar.close()

    for r in listar_lvr:
        if r.get("ISBN"):
            r["ISBN"] = formatar_isbn(r["ISBN"])
    return listar_lvr

def buscar_livro_isbn(ISBN: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro WHERE ISBN = %s;", (ISBN,))
    listar = conectar.fetchone()
    conectar.close()

    if listar and listar.get("ISBN"):
        listar["ISBN"] = formatar_isbn(listar["ISBN"])
    return listar

# chamar a tabela toda da localidade do livro depois achar o câmpus que ele está com outra função

def buscar_locallivro(id_livro: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM posicao_livro WHERE id_livro = %s;", (id_livro,))
    listar = conectar.fetchone()
    conectar.close()

    return listar

def buscar_campus(id_capus: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM localidade_livro WHERE id_campus = %s", (id_capus,))
    listar = conectar.fetchone()
    conectar.close()

    return listar


# =================Inserir dados=================

def criar_usuario(nome, data_nascimento, email, cpf, telefone, senha, nivel_acesso):
    conectar = mysql.connection.cursor()
    conectar.execute("INSERT INTO usuarios (nome, data_nascimento, email, cpf, telefone, senha, nivel_acesso) VALUES (%s, %s, %s , %s, %s, %s, %s)", (nome, data_nascimento, email, cpf, telefone, senha, nivel_acesso,)) 
    mysql.connection.commit()
    conectar.close()

def validar_usuario(email_info,cpf_info):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT email, cpf FROM usuarios WHERE email = %s OR cpf = %s", (email_info, cpf_info,))
    existe = conectar.fetchone()
    conectar.close()

    return existe