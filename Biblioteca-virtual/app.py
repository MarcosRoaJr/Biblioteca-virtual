from flask import Flask,  render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("rotas/index.html", show_navbar=True)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    return render_template("rotas/cadastro.html", show_navbar=True)

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    return render_template("rotas/buscar.html", show_navbar=True)

@app.route("/cadastrar_usuario", methods=["GET", "POST"])
def cadastrar_usuario():
    return render_template("rotas/cadastrar_usuario.html", show_navbar=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("rotas/login.html", show_navbar=False)

if __name__ == "__main__":
    app.run(debug=True)
