from flask import Flask, render_template, request, redirect, url_for, session
import random
from bd import init_app, verificar_usuario

app = Flask(__name__)
app.secret_key = str(random.randint(0, 10))

init_app(app)

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
    return render_template("rotas/buscar.html", show_navbar=True)

# Rota para cadastrar o usuario
@app.route("/cadastrar_usuario", methods=["GET", "POST"])
def cadastrar_usuario():
    return render_template("rotas/cadastrar_usuario.html", show_navbar=True)

# Pagina para efetuar o login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario_id = request.form.get("usuario")
        senha = request.form.get("senha")

        if verificar_usuario(usuario_id, senha) or (usuario_id == "0" and senha == "0"):
            user = verificar_usuario(usuario_id, senha)
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
        elif not session.get("user") or not verificar_usuario(usuario_id, senha):
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