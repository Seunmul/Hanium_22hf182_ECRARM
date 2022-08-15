from flask import Flask, render_template, request
import datetime
app = Flask(__name__)

@app.route("/")
def first():
    return render_template("login.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/status")
def status():
    return render_template("status.html")

@app.route("/react")
def my_index():
    return render_template("index.html", flask_token="react  ")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13000, debug=True)
