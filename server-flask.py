from flask import Flask, request, render_template
from flask_cors import CORS
from pymongo import MongoClient

def connection():
    client = MongoClient("localhost", 27017)
    db = client['meu_banco_de_dados']

    collection = db['minha_colecao']
    return collection

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query', methods=['GET'])
def query_records():
    conn = connection()
    nome = request.args.get("name")
    filtro = {"name": nome}
    resp = conn.find_one(filtro)
    if resp:
        temp = dict(resp)
        temp.pop('_id')
        return temp
    else:
        return {"resposta": "Dado nao encontrado"}


@app.route('/create', methods=['POST'])
def create_record():
    conn = connection()
    if request.method == "POST":
        nome = request.form.get("name")
        email = request.form.get("email")
        filtro = {"name": nome, "email": email}
        resp = conn.find_one(filtro)
        if resp:
            return {"resposta": "Registro já existente"}
        insert = conn.insert_one(filtro)
        if insert:
            return {"resposta": "Dado inserido no banco"}
        return {"resposta": "Erro ao inserir"}
    return render_template("index.html")


@app.route('/update', methods=['POST'])
def update_record():
    conn = connection()
    if request.method == 'POST':
        nome = request.form.get("name")
        email = request.form.get("email")
        filtro = {"name": nome}
        resp = conn.update_one(filtro, { "$set" : {"email": email}})
        if resp.modified_count > 0:
            return {"resposta": "Dado modificado"}
        return {"resposta": "Erro ao modificar"}
    return render_template("index.html")


@app.route('/delete', methods=['POST'])
def delete_record():
    conn = connection()
    print("chegou aqui")
    if request.method == 'POST':
        nome = request.form.get("name")
        email = request.form.get("email")
        resp = conn.delete_one({"name": nome, "email": email})
        if resp:
            return {"resposta": "Dado deletado do banco"}
        return {"resposta": "Erro ao deletar dado do banco"}
    return render_template("index.html")


app.run(debug=True)