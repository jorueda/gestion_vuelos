from flask import Flask
from flask import render_template, request

app = Flask(__name__)
app.secret_key = "Llavesecreta"

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

@app.route('/editar/', )
def editar_vuelo():
	return render_template('editar.html', titulo="Editar Vuelo")

@app.route('/editado/', methods=['GET', 'POST'])
def vuelo_editado():
	if request.method == 'POST':
		id_vuelo = request.form['id_vuelo']
		nombre = request.form['nombre']
		apellido = request.form['apellido']
		ciudad_origen = request.form['ciudad_origen']
		ciudad_destino = request.form['ciudad_destino']
		mensaje = "editado"
		return render_template('actualizado.html', titulo="Editar Vuelo", id_vuelo=id_vuelo, nombre=nombre, 
			apellido=apellido, ciudad_origen=ciudad_origen, ciudad_destino=ciudad_destino, mensaje=mensaje)

@app.route('/eliminar/', )
def eliminar_vuelo():
	return render_template('eliminar.html', titulo="Eliminar Vuelo")

@app.route('/eliminado/', methods=['GET', 'POST'])
def vuelo_eliminado():
	if request.method == 'POST':
		id_vuelo = request.form['id_vuelo']
		mensaje = "eliminado"
		return render_template('actualizado.html', titulo="Eliminar Vuelo", id_vuelo=id_vuelo, mensaje=mensaje)

if __name__ == '__main__':
	app.run(debug = True)