from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def start_download():
    print(request.args)
    return "hello word"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int("5000"),
        debug=True
    )
