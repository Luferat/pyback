# API REST JSON usando uma coleção de dicionários.
 
from flask import Flask, jsonify, request

app = Flask(__name__)

items = [
    {
        "id": 1,
        "name": "Bagulho",
        "description": "Apenas um bagulho",
        "location": "Em uma caixa"
    },
    {
        "id": 2,
        "name": "Tranqueira",
        "description": "Apena uma tranqueira qualquer",
        "location": "Em um gaveteiro qualquer"
    },
    {
        "id": 3,
        "name": "Bagulete",
        "description": "Apenas um bagulete qualquer",
        "location": "Em um caixote na esquina"
    }
]


@app.route('/items', methods=['GET'])
def get_all():
    return jsonify(items)


@app.route('/items/<int:id>', methods=['GET'])
def get_one(id):
    for item in items:
        if item.get('id') == id:
            return jsonify(item)


@app.route('/items', methods=['POST'])
def new():
    new_item = request.get_json()
    max_id = max(item['id'] for item in items)
    new_item['id'] = max_id + 1
    items.append(new_item)
    return jsonify(items)


@app.route('/items/<int:id>', methods=['PUT', 'PATCH'])
def edit(id):
    edited_item = request.get_json()
    for index, item in enumerate(items):
        if item.get('id') == id:
            items[index].update(edited_item)
            return jsonify(items[index])


@app.route('/items/<int:id>', methods=['DELETE'])
def delete(id):
    for index, item in enumerate(items):
        if item.get('id') == id:
            del (items[index])
            return jsonify(items)


app.run(port=3000, host='localhost', debug=True)
