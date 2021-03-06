# $env:FLASK_APP="app.py" en PowerShell
# $env:FLASK_ENV="development" en PowerShell

from flask import Flask
from flask import render_template, request, flash, session, make_response, redirect, url_for
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "Llavesecreta"

@app.route('/', methods=["GET", "POST"])
def login():
	try:
		if request.method == 'POST':
			db = get_db()
			error = None
			cedula = request.form['cedula']
			password = request.form['password']

			if not cedula:
				error = 'Debes ingresar la cédula'
				flash(error)
				return render_template( 'login.html' )

			if not password:
				error = 'Debes ingresar la contraseña'
				flash(error)
				return render_template( 'login.html' )
			
			cursor = db.execute('SELECT * FROM usuario WHERE cedula_usuario = ?', (cedula,)).fetchone()
			print(cursor[0])
			print(cursor[6])

			if cursor is None:
				error = 'Usuario no válido'
			else:
				if check_password_hash(cursor[6], password):
					session.clear() # Limpiar la sesión anterior
					session['user_id'] = cursor[0]
					resp = make_response(redirect(url_for ('admin')))
					resp.set_cookie('cedula', cedula)
					return resp
					
				else:
					error = 'Contraseña no válida'
				
			flash(error)
		return render_template('login.html', titulo="Sky Planner")
	except:
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
		password = generate_password_hash(password)
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

@app.route('/viajesbuscados/', methods=['GET', 'POST'])
def viajes_buscados():
	try:
		if request.method == 'POST':
			error = None
			ciudad_origen = request.form['ciudad_origen']
			ciudad_destino = request.form['ciudad_destino']

			if not ciudad_origen:
				error = 'Debes ingresar la ciudad de origen'
				flash(error)
				return render_template('viajes.html', titulo="Sky Planner")

			if not ciudad_destino:
				error = 'Debes ingresar la ciudad de destino'
				flash(error)
				return render_template('viajes.html', titulo="Sky Planner")
			
			db = get_db()
			cursor = db.execute('SELECT * FROM vuelo WHERE origen = ?', (ciudad_origen,)).fetchall()

			if(len(cursor) == 0):
				error = 'Ciudad origen no encontrada'
				flash(error)
				return render_template('viajes.html', titulo="Sky Planner")
			else:
				cursor = db.execute('SELECT * FROM vuelo WHERE destino = ?', (ciudad_destino,)).fetchall()

				if(len(cursor) == 0):
					error = 'Ciudad destino no encontrada'
					flash(error)
					return render_template('viajes.html', titulo="Sky Planner")
				else:
					mensaje = "Vuelo disponible"
					return render_template('viajesbuscados.html', titulo="Viajes", 
					ciudad_origen=ciudad_origen, ciudad_destino=ciudad_destino, mensaje=mensaje)
	except:
		flash('Error al buscar vuelos')
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
	try:
		if request.method == 'POST':
			error = None
			id_vuelo = request.form['id_vuelo']
			ciudad_origen = request.form['ciudad_origen']
			ciudad_destino = request.form['ciudad_destino']

			if not id_vuelo:
				error = 'Debes ingresar el id del vuelo'
				flash(error)
				return render_template( 'agregar.html' )

			if not ciudad_origen:
				error = 'Debes ingresar la ciudad de origen'
				flash(error)
				return render_template( 'agregar.html' )

			if not ciudad_destino:
				error = 'Debes ingresar la ciudad de destino'
				flash(error)
				return render_template( 'agregar.html' )
			
			db = get_db()
			cur = db.cursor()
			cur.executescript("INSERT INTO vuelo (id_vuelo, origen, destino) VALUES ('%s', '%s', '%s')" % (int(id_vuelo), ciudad_origen, ciudad_destino,))
			db.commit()

			mensaje = "Vuelo agregado con exito"
			return render_template('agregado.html', titulo="Agregar Vuelo", id_vuelo=id_vuelo, 
			ciudad_origen=ciudad_origen, ciudad_destino=ciudad_destino, mensaje=mensaje)
	except:
		flash('Error al crear vuelo')
		return render_template('agregar.html', titulo="Agregar Vuelo")

@app.route('/editar/', )
def editar_vuelo():
	return render_template('editar.html', titulo="Editar Vuelo")
	
@app.route('/editado/', methods=['GET', 'POST'])
def vuelo_editado():
	try:
		if request.method == 'POST':
			error = None

			id_vuelo = request.form['id_vuelo']
			ciudad_origen = request.form['ciudad_origen']
			ciudad_destino = request.form['ciudad_destino']

			if not id_vuelo:
				error = 'Debes ingresar el id del vuelo'
				flash(error)
				return render_template( 'editar.html' , titulo="Editar Vuelo")

			if not ciudad_origen:
				error = 'Debes ingresar la ciudad de origen del vuelo'
				flash(error)
				return render_template( 'editar.html' , titulo="Editar Vuelo")

			if not ciudad_destino:
				error = 'Debes ingresar la ciudad de destino del vuelo'
				flash(error)
				return render_template( 'editar.html' , titulo="Editar Vuelo")

			id_vuelo = int(id_vuelo)

			db = get_db()
			#cursor = db.execute('SELECT * FROM vuelo WHERE id_vuelo = ?', (id_vuelo,)).fetchone()
			#cursor = db.execute('SELECT * FROM vuelo').fetchall()
			cursor = db.execute('SELECT * FROM vuelo WHERE id_vuelo = ?', (id_vuelo,)).fetchall()

			if(len(cursor) == 0):
				error = 'Id de vuelo no encontrado'
				flash(error)
			else:
				db.execute('UPDATE vuelo SET origen = ?, destino = ? WHERE id_vuelo=?', (ciudad_origen, ciudad_destino, id_vuelo,))
				db.commit()

			mensaje = "Vuelo editado correctamente"

			return render_template('actualizado.html', titulo="Editar Vuelo", id_vuelo=id_vuelo, 
			ciudad_origen=ciudad_origen, ciudad_destino=ciudad_destino, mensaje=mensaje)
	except:
		flash('Error al editar vuelo')
		return render_template('editar.html', titulo="Editar Vuelo")

@app.route('/eliminar/', )
def eliminar_vuelo():
	return render_template('eliminar.html', titulo="Eliminar Vuelo")

@app.route('/eliminado/', methods=['GET', 'POST'])
def vuelo_eliminado():
	try:
		if request.method == 'POST':
			error = None

			id_vuelo = request.form['id_vuelo']

			if not id_vuelo:
				error = 'Debes ingresar el id del vuelo'
				flash(error)
				return render_template( 'eliminar.html' , titulo="Eliminar Vuelo")

			id_vuelo = int(id_vuelo)

			db = get_db()
			#cursor = db.execute('SELECT * FROM vuelo WHERE id_vuelo = ?', (id_vuelo,)).fetchone()
			#cursor = db.execute('SELECT * FROM vuelo').fetchall()
			cursor = db.execute('SELECT * FROM vuelo WHERE id_vuelo = ?', (id_vuelo,)).fetchall()

			if(len(cursor) == 0):
				error = 'Id de vuelo no encontrado'
				flash(error)
				return render_template( 'eliminar.html' , titulo="Eliminar Vuelo")
			else:
				db.execute('DELETE FROM vuelo WHERE id_vuelo=?', (id_vuelo,))
				db.commit()

			mensaje = "Vuelo eliminado correctamente"
			return render_template('actualizado.html', titulo="Eliminar Vuelo", id_vuelo=id_vuelo, mensaje=mensaje)
	except:
		flash('Error al eliminar vuelo')
		return render_template( 'eliminar.html' , titulo="Eliminar Vuelo")

@app.route('/logout', )
def logout():
    session.clear()
    return redirect(url_for( 'login' ))

if __name__ == '__main__':
	app.run(debug = True)