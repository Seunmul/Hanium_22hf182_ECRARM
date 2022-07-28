from flask import Flask, render_template, request
import datetime
app = Flask(__name__)

@app.route("/")
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

@app.route("/helloworld")
def helloworld():
    return render_template('helloworld.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999, debug=True)

