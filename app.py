# $env:FLASK_APP="app.py" en PowerShell
# $env:FLASK_ENV="development" en PowerShell

from flask import Flask
from flask import render_template, request, flash, session, make_response, redirect, url_for
from db import get_db

app = Flask(__name__)
app.secret_key = "Llavesecreta"

@app.route('/')#,methods=["GET", "POST"])
def login():
	return render_template('login.html', titulo="Sky Planner")


@app.route('/registro/',methods=["GET", "POST"])
def registro():
	if request.method == 'POST':
		cedula = request.form['cedula']
		nombre= request.form['nombre']
		apellido = request.form['apellido']
		edad = request.form['edad']
		telefono = request.form['telefono']
		direccion = request.form['direccion']
		password = request.form['password']
		db = get_db()
		cur = db.cursor()
		cur.executescript("INSERT INTO usuario (cedula_usuario, nombre, apellido, edad, telefono, direccion, password) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (cedula, nombre, apellido, edad, telefono, direccion, password,))
		db.commit()
		flash('Usuario creado en la BD')
		return render_template('login.html', titulo="Sky Planner")
	return render_template('registro.html', titulo="Sky Planner")

@app.route('/viajes/',methods=["GET", "POST"])
def viajes():
	return render_template('viajes.html', titulo="Sky Planner")

@app.route('/experiencias/',methods=["GET", "POST"])
def experiencias():
	return render_template('experiencias.html', titulo="Sky Planner")

@app.route('/admin/',methods=["GET", "POST"])
def admin():
	return render_template('admin.html', titulo="Sky Planner")

@app.route('/agregar/',methods=["GET", "POST"])
def agregar_vuelo():
	return render_template('agregar.html', titulo="Agregar Vuelo")

@app.route('/agregado/', methods=['GET', 'POST'])
def vuelo_agregado():
	if request.method == 'POST':
		id_vuelo = request.form['id_vuelo']
		ciudad_origen = request.form['ciudad_origen']
		ciudad_destino = request.form['ciudad_destino']
		mensaje = "agregado"
		return render_template('agregado.html', titulo="Agregar Vuelo", id_vuelo=id_vuelo, 
			ciudad_origen=ciudad_origen, ciudad_destino=ciudad_destino, mensaje=mensaje)

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