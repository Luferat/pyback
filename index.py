# API RESTful JSON.

from flask import Flask, jsonify, request, abort, make_response
import json
import jwt

app = Flask(__name__)

db = "items.json"

secret = "secret"


def db_open():
    try:
        with open(db, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Erro ao abrir arquivo JSON: {e}")
        return False


def db_save(data):
    try:
        with open(db, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            return True
    except Exception as e:
        print(f"Erro ao salvar arquivo JSON: {e}")
        return False


def not_found():
    abort(make_response({"message": "Não encontrado"}, 404))


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()
    username = data.get("username").strip()
    password = data.get("password").strip()
    if username == "" or password == "":
        return jsonify({"message": "Credenciais inválidas ou vazias"}), 401

    try:
        with open("users.json", "r", encoding="utf-8") as json_file:
            users = json.load(json_file)
            for user in users:
                if user["username"] == username and user["password"] == password:
                    del user["password"]
                    token = jwt.encode(
                        user, secret, algorithm="HS256")
                    return jsonify({"token": token})
                else:
                    return jsonify({"message": "Falha na autenticação"}), 401
    except Exception as e:
        return jsonify({"message": f"Erro ao abrir base de dados: {e}"}), 500


@app.route("/items", methods=["GET"])
def get_all():

    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token de acesso é necessário"}), 401
    elif token.split()[0] != "Bearer":
        return jsonify({"message": "Formato do Authorization incorreto"}), 401

    try:
        data = jwt.decode(
            token.split()[1], secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expirado."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido."}), 401

    print(data)
    items = db_open()
    if (len(items) > 0):
        return jsonify(items)
    not_found()


@app.route("/items/<int:id>", methods=["GET"])
def get_one(id):
    items = db_open()
    for index, item in enumerate(items):
        if item.get("id") == id:
            return jsonify(item)
    not_found()


@app.route("/items", methods=["POST"])
def new():
    items = db_open()
    all_ids = [reg["id"] for reg in items]
    if all_ids:
        next_id = max(all_ids) + 1
    else:
        next_id = 1
    new_item = request.get_json()
    new_item["id"] = next_id
    items.append(new_item)
    if db_save(items):
        return jsonify(new_item), 201
    else:
        return jsonify({"status": "error", "message": "Falha ao salvar dados"}), 500


@app.route("/items/<int:id>", methods=["PUT", "PATCH"])
def edit(id):
    items = db_open()
    edited_item = request.get_json()
    for index, item in enumerate(items):
        if item.get("id") == id:
            items[index].update(edited_item)
            if db_save(items):
                return jsonify(items[index])
            else:
                return jsonify({"status": "error", "message": "Falha ao salvar dados"}), 500
    not_found()


@app.route("/items/<int:id>", methods=["DELETE"])
def delete(id):
    items = db_open()
    for index, item in enumerate(items):
        if item.get("id") == id:
            del (items[index])
            if db_save(items):
                return jsonify({"status": "success", "message": "Apagado com sucesso"})
            else:
                return jsonify({"status": "error", "message": "Falha ao salvar dados"}), 500
    not_found()


app.run(port=3000, debug=True)
