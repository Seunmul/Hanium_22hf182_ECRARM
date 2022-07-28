from flask import Flask, render_template, request
import datetime
app = Flask(__name__)

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/main")
def main():
    localtime = datetime.datetime.now()
    strTime = localtime.strftime("%Y-%m-%d %H:%M")
    
    param = request.args.get('msg', None)
    templateData ={
        'title' : 'FLASK TEST SERVER',
        'time' : strTime,
        'text' : param
    }
    return render_template('main.html',**templateData)

@app.route("/status")
def status():
    return render_template('status.html')

@app.route("/controlPanel")
def controlPanel():
    return render_template('controlPanel.html')

@app.route("/productLicense")
def productLicense():
    return render_template('productLicense.html')

@app.route("/information")
def information():
    return render_template('information.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999, debug=True)

