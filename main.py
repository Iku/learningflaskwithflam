from flask import Flask, render_template, redirect
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/injectweed')
def injectweed():
	return render_template("injectweed.html")

@app.route('/index')
def index2():
	return render_template("index2.html")

if __name__ == "__main__":
	app.run(debug=True)