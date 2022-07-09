from flask import Flask, jsonify, request

app = Flask(__name__)
stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

# POST  - used to receive data
# GET - used to send data back only

# POST /store data: {name :}


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>


@app.route('/store/<string:name>')  # 'http://127.0.0.1:5000/store/some_name'
def get_store(name):
    # Iterate over stores
    # if the store name matches, return it
    # if none match, return an error message
    for store in stores:
        if store['name'] == name:
            return store
    return jsonify({'message': f'Store {name!r} does not exist.'})

# GET /store


@app.route('/store/')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store():
    request_data = request.get_json()
    new_item = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_item)
    return jsonify(new_item)

# GET /store/<string:name>/item


@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': f'Store {name!r} does not exist for items.'})


app.run(port=5000)
