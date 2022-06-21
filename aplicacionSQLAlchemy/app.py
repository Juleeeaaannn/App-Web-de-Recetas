from datetime import datetime
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db 
from models import Usuario, Receta, Ingredientes
		
@app.route('/')
def inicio():
	return render_template('inicio.html')
@app.route('/usuario', methods = ['GET','POST'])
def usuario():
	if request.method == 'POST':
		if not request.form['email'] or not request.form['password']:
			return render_template('error.html', error="Por favor ingrese los datos requeridos")
		else:
			usuario_actual= Usuario.query.filter_by(correo= request.form['email']).first()
			if usuario_actual is None:
				return render_template('error.html', error="El correo no está registrado")
			else:
				verificacion = check_password_hash(usuario_actual.clave, request.form['password'])
				if (verificacion):                    
					return render_template('usuario_registrado.html', usuario = usuario_actual)
				else:
					return render_template('error.html', error="La contraseña no es válida")
	else:
		return render_template('inicio.html')	
@app.route('/nuevo_usuario', methods = ['GET','POST'])
def nuevo_usuario():   
	if request.method == 'POST':
		if not request.form['nombre'] or not request.form['email'] or not request.form['password']:
			return render_template('error.html', error="Los datos ingresados no son correctos...")
		else:
			nuevo_usuario = Usuario(nombre=request.form['nombre'], correo = request.form['email'], clave=generate_password_hash(request.form['password']))       
			db.session.add(nuevo_usuario)
			db.session.commit()
			return render_template('aviso.html', mensaje="El usuario se registró exitosamente")
	return render_template('nuevo_usuario.html')
@app.route('/compartir_receta', methods = ['GET','POST'])
def compartir_receta():
	if request.method == 'POST':
		print('hola')
@app.route('/consultar_ingredientes', methods = ['GET','POST'])
def consultar_ingredientes():
	if request.method == 'POST':
		print('hola')
@app.route('/consultar_ranking', methods = ['GET','POST'])
def consultar_ranking():
	if request.method == 'POST':
		print('hola')
@app.route('/consultar_tiempo', methods = ['GET','POST'])
def consultar_tiempo():
	if request.method == 'POST':
		print('hola')    
# @app.route('/ingresar_comentario', methods = ['GET', 'POST'])
# def ingresar_comentario():
#     if request.method == 'POST':
#         if not request.form['contenido']:
#             return render_template('error.html', error="Contenido no ingresado...")
#         else:            
#             nuevo_comentario= Comentario(fecha=datetime.now(), contenido=request.form['contenido'], usuario_id =request.form['userId'])    
#             db.session.add(nuevo_comentario)
#             db.session.commit()
#             return render_template('inicio.html') 
#     return render_template('inicio.html') 

# @app.route('/listar_comentarios')
# def listar_comentarios():
#    return render_template('listar_comentario.html', comentarios = Comentario.query.all())

# @app.route('/listar_comentarios_usuario', methods = ['GET', 'POST'])
# def listar_comentarios_usuario():  
#     if request.method == 'POST':
#         if not request.form['usuarios']:
# 			#Pasa como parámetro todos los usuarios
#             return render_template('listar_comentario_usuario.html', usuarios = Usuario.query.all(), usuario_seleccionado = None )
#         else:
#             return render_template('listar_comentario_usuario.html', usuarios= None, usuario_selec = Usuario.query.get(request.form['usuarios'])) 
#     else:
#         return render_template('listar_comentario_usuario.html', usuarios = Usuario.query.all(), usuario_selec = None )   
        

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)	