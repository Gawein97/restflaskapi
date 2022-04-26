from flask import Flask, jsonify, request


app = Flask(__name__)
stores = [
    {
        "name": "Apple Store",
        "items": [
            {
                "name": "Macbook",
                "price": 1000.99
            },
            {
                "name": "Macbook Pro",
                "price": 2000.50
            }
        ]
    }
]


# POST /store data: {name: str}
@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<str: name>
@app.route("/store/<string:name>", methods=["GET"])
def get_store(name):
    # iterate over stores
    for store in stores:
        if store.get("name") == name:
            return jsonify(store)
    return jsonify({"message": "store not found"})


# GET /stores
@app.route("/stores", methods=["GET"])
def get_stores():
    return jsonify({"stores": stores})


# POST /store/<str: name>/item data: {name:str, price:float}
@app.route("/store/<string:name>/item", methods=["POST"])
def create_store_item(name):
    request_data = request.get_json()
    for store in stores:
        if store.get("name") == name:
            try:
                new_item = {
                    "name": request_data["name"],
                    "price": request_data["price"]
                }
            except KeyError:
                return jsonify({"message": "error"})
            store["items"].append(new_item)
            return jsonify(new_item), 201
    return jsonify({"message": "store not found"})


# GET /store/<str: name>/items
@app.route("/store/<string:name>/items", methods=["GET"])
def get_store_items(name):
    for store in stores:
        if store.get("name") == name:
            return jsonify({"items": store["items"]})
    return jsonify({"message": "store not found"})


if __name__ == '__main__':
    app.run(debug=True)
