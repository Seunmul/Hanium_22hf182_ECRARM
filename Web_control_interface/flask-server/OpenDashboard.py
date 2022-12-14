from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html", flask_token="react  ")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
