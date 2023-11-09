# API REST JSON usando um arquivo de persistência.

from flask import Flask, jsonify, request
import json

app = Flask(__name__)


def db_open():
    with open('items.json', 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def db_save(data):
    with open('items.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


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
    new_item = request.get_json()
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
