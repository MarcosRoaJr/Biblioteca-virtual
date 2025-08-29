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

def verificar_usuario(usuario_id, senha):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM usuarios
        WHERE id_usuario = %s
    """, (usuario_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        return None
    return row if row['senha'] == senha else None
