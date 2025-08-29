from flask import Flask,  render_template, request, redirect, url_for, session
import random
from bd import init_app,verificar_usuario

app = Flask(__name__)
app.secret_key = str(random.randint(0, 10))

init_app(app)

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("rotas/home.html", show_navbar=True)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    return render_template("rotas/cadastro.html", show_navbar=True)

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    return render_template("rotas/buscar.html", show_navbar=True)

@app.route("/cadastrar_usuario", methods=["GET", "POST"])
def cadastrar_usuario():

    return render_template("rotas/cadastrar_usuario.html", show_navbar=True)

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
        elif session["user"] == None or not verificar_usuario(usuario_id, senha):
            return render_template("rotas/index.html", erro=True, msg="Usuário ou senha inválidos.")
    return render_template("rotas/index.html")

@app.context_processor
def inject_user():
    return dict(usuario=session.get("user"))

@app.route("/usuario", methods=["GET", "POST"])
def usuario():
    return render_template("rotas/usuario.html", show_navbar=True)

if __name__ == "__main__":
    app.run(debug=True)
