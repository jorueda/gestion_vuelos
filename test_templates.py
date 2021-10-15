from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')#,methods=["GET", "POST"])
def index():
	return render_template('index.html', titulo="Sky Planner")

@app.route('/viajes/')
def viajes():
	return render_template('viajes.html', titulo="Sky Planner")

@app.route('/experiencias/')
def experiencias():
	return render_template('experiencias.html', titulo="Sky Planner")

@app.route('/admin/')
def admin():
	return render_template('admin.html', titulo="Sky Planner")

if __name__ == '__main__':
	app.run(debug = True)