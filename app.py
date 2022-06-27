from flask import Flask

app = Flask(__name__)

@app.route("/")
def Index():
    return "<h1>Olá, mundo!</h1>"


@app.route("/<user>")
def Users(user):
    return f"<h1>Olá, {user}</h1>"


@app.route("/mostrar-letra/<a>")
def Test(a):
    return f"<p>{str(a)*9999}</p>"
