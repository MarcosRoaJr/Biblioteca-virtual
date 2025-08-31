from flask import Flask, render_template, request, redirect, url_for, session
import random
import bd

# Retornar_x eu uso para buscar informações para usar em outra função que realmente vai buscar a informação que eu preciso
# Buscar_x eu uso para enviar a informação que eu vou buscar de fato no banco e usar

app = Flask(__name__)
app.secret_key = str(random.randint(0, 10))

bd.init_app(app)

# Rota para pagina inicial
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("rotas/home.html", show_navbar=True)

# Rota para cadastro de livros
# Verificar se não é ideal trocar para um nome melhor 
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    return render_template("rotas/cadastro.html", show_navbar=True)

# Rota para buscar as informações de livros
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    livro = None
    titulos = bd.buscar_livro_nome()
    genero = None
    editora = None
    campus = None
    locallivro = None

    if request.method == "POST":
        isbnlivro = (request.form.get("isbn_livro") or "").strip()
        idlivro = (request.form.get("identificador_livro") or "").strip()
        escolhido = (request.form.get("livro_escolhido") or "").strip()

        if escolhido:
            if escolhido.isdigit():
                livro = bd.buscar_livro_id(int(escolhido))
                locallivro = bd.buscar_locallivro(int(escolhido))
                idgenero = bd.retornar_idgenero(int(escolhido))
                ideditora = bd.retornar_ideditora(int(escolhido))

                genero = bd.buscar_genero(idgenero)
                editora = bd.buscar_editora(ideditora)
                if locallivro:
                    campus = bd.buscar_campus(int(locallivro["id_campus"]))
                else:
                    campus = None
        elif idlivro:
            if idlivro.isdigit():
                livro = bd.buscar_livro_id(int(idlivro))
                idgenero = bd.retornar_idgenero(int(idlivro))
                ideditora = bd.retornar_ideditora(int(idlivro))
                locallivro = bd.buscar_locallivro(int(idlivro))

                genero = bd.buscar_genero(idgenero)
                editora = bd.buscar_editora(ideditora)
                if locallivro:
                    campus = bd.buscar_campus(int(locallivro["id_campus"]))
                else:
                    campus = None
        elif isbnlivro:
            if isbnlivro.isdigit():
                livro = bd.buscar_livro_isbn(int(isbnlivro))
                isbn_idlivro = bd.retornar_idisbn(int(isbnlivro))

                if isbn_idlivro is not None:
                    r = bd.retornar_idgenero(isbn_idlivro)
                    e = bd.retornar_ideditora(isbn_idlivro)
                    t = bd.buscar_locallivro(isbn_idlivro)
                    o = bd.buscar_campus(isbn_idlivro)
                    if r is not None:
                        genero = bd.buscar_genero(r)
                        editora = bd.buscar_editora(e)
                        locallivro = t
                        campus = o

    return render_template("rotas/buscar.html", show_navbar=True, campus=campus, locallivro=locallivro, editora=editora,livro=livro,titulos=titulos, genero=genero)


# Rota para cadastrar o usuario
# nome, data_nascimento, email, cpf, telefone, senha, nivel_acesso
@app.route("/cadastrar_usuario", methods=["GET", "POST"])
def cadastrar_usuario():
    confirma = None
    if request.method == "POST":
        nome_info = request.form.get("Nome")
        data_nascimento_info = request.form.get("Data_nascimento")
        email_info = request.form.get("Email")
        cpf_info = request.form.get("CPF")
        telefone_info = request.form.get("Telefone")
        senha_info = request.form.get("Senha")
        c_senha_info = request.form.get("c_Senha")
        lvl_acess_info = request.form.get("lvl_acess")
        validar_confirma = request.form.get("confirmacao")
        validar_negado = request.form.get("negado")
        verificar = bd.verificar_usuario(email_info,cpf_info)
        
        if validar_confirma == "confirmar":
            if not verificar:
                if senha_info == c_senha_info:
                    bd.criar_usuario(nome_info, data_nascimento_info, email_info, cpf_info, telefone_info, senha_info, lvl_acess_info)
                    confirma = True
                else:
                    confirma = False
        elif validar_negado == "negar":
            confirma = False
            
    return render_template("rotas/cadastrar_usuario.html", show_navbar=True, msg=confirma)

# Pagina para efetuar o login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario_id = request.form.get("usuario")
        senha = request.form.get("senha")

        if bd.verificar_usuario(usuario_id, senha) or (usuario_id == "0" and senha == "0"):
            user = bd.verificar_usuario(usuario_id, senha)
            if user:
                dn = user.get("data_nascimento")
                dn_fmt = dn.strftime("%d/%m/%Y") if dn else None

                # Essa parte aqui foi feita para guardar os usuarios
                session["user"] = {
                    "id": user.get("id_usuario"),
                    "nome": user.get("nome"),
                    "data_nascimento": dn_fmt,
                    "email": user.get("email"),
                    "cpf": user.get("cpf"),
                    "telefone": user.get("telefone"),
                    "nivel_acesso": user.get("nivel_acesso")
                }
                return redirect(url_for('home'))
            elif usuario_id == "0" and senha == "0":
                session["user"] = {
                    "id": "0",
                    "nome": "Admin",
                    "email": "admin@biblioteca.com",
                    "data-nascimento": "01/01/1000",
                    "CPF": "000.000.000-00",
                    "telefone": "(00) 0000-0000",
                    "Nivel-acesso": "admin",
                }
                return redirect(url_for('home'))
        elif not session.get("user") or not bd.verificar_usuario(usuario_id, senha):
            return render_template("rotas/index.html", erro=True, msg="Usuário ou senha inválidos.")
    return render_template("rotas/index.html")

# Essa função injeta em toda a pagina o usuario fazendo assim não perder na hora da troca
@app.context_processor
def inject_user():
    return dict(usuario=session.get("user"))

# Rota para as informações do proprio usuario
@app.route("/usuario", methods=["GET", "POST"])
def usuario():
    return render_template("rotas/usuario.html", show_navbar=True)

# Deslogar o usuario
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

# Até agora não entendo como funciona mas é importante para o codigo
if __name__ == "__main__":
    app.run(debug=True)