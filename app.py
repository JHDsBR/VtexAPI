from flask import Flask

app = Flask(__name__)

@app.route("/")
def Conexao():
    return "Olá, mundo!"

# app.run()
