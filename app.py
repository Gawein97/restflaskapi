from flask import Flask, jsonify
import socket


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"response": socket.gethostname()})


if __name__ == '__main__':
    app.run(debug=True)
