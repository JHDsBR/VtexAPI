from flask import Flask

app = Flask(__name__)

@app.route("/")
def Index():
    return "Olá, mundo!"


@app.route("/<user>")
def Users(user):
    return f"Olá, {user}"


@app.route("/mostrar-letra/<a>")
def Test(a):
    return f"<p>{str(a)*9999}</p>"
