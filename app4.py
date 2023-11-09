# API REST JSON usando um gerador de Ids para o POST.

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

db = 'items.json'


def db_open():
    try:
        with open(db, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Erro ao abrir arquivo JSON: {e}")


def db_save(data):
    try:
        with open(db, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar arquivo JSON: {e}")


@app.route('/items', methods=['GET'])
def get_all():
    items = db_open()
    return jsonify(items)


@app.route('/items/<int:id>', methods=['GET'])
def get_one(id):
    items = db_open()
    for item in items:
        if item.get('id') == id:
            return jsonify(item)


@app.route('/items', methods=['POST'])
def new():
    items = db_open()
    all_ids = [reg['id'] for reg in items]
    next_id = max(all_ids) + 1
    new_item = request.get_json()
    new_item["id"] = next_id
    items.append(new_item)
    db_save(items)
    return jsonify(items)


@app.route('/items/<int:id>', methods=['PUT', 'PATCH'])
def edit(id):
    items = db_open()
    edited_item = request.get_json()
    for index, item in enumerate(items):
        if item.get('id') == id:
            items[index].update(edited_item)
            db_save(items)
            return jsonify(items[index])


@app.route('/items/<int:id>', methods=['DELETE'])
def delete(id):
    items = db_open()
    for index, item in enumerate(items):
        if item.get('id') == id:
            del (items[index])
            db_save(items)
            return jsonify(items)


app.run(port=3000, host='localhost', debug=True)
