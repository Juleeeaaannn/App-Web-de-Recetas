from datetime import datetime
from flask import Flask, request, render_template, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config["SESSION_PERMANENT"] = False#####
app.config["SESSION_TYPE"] = "filesystem"#### ESTAS 3 LINEAS DE CODIGO SON NECESARIAS PARA QUE FUNCIONE EL SESSION 
Session(app)#######
  
from models import db 
from models import Usuario, Receta, Ingrediente
		
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
			session['id'] = usuario_actual.id
			session['user'] = usuario_actual
			if usuario_actual is None:
				return render_template('error.html', error="El correo no está registrado")
			else:
				verificacion = check_password_hash(usuario_actual.clave, request.form['password'])
				if (verificacion):                    
					return render_template('usuario_registrado.html')
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
			clave=generate_password_hash(request.form['password'])
			nuevo_usuario = Usuario(nombre=request.form['nombre'], correo = request.form['email'], clave=generate_password_hash(request.form['password']))  
			db.session.add(nuevo_usuario)
			db.session.commit()
			return render_template('aviso.html', mensaje="El usuario se registró exitosamente")
	return render_template('nuevo_usuario.html')
###############################
@app.route('/compartir_receta', methods = ['GET','POST'])
def compartir_receta():
	if request.method == 'POST':
		if not request.form:
			return render_template('error.html', error="Contenido no ingresado...") #SI NO TRAE NADA DA ERROR
		else:            
			nueva_receta= Receta(nombre=request.form['nombre'], tiempo=request.form['tiempo'], elaboracion=request.form['descripcion'], cantidadmegusta=0, fecha=datetime.now(), usuarioid = session['id'])    #SE CREA UN OBJETO DE EL MODELO RECETAS
			db.session.add(nueva_receta)
			db.session.commit()#SE GUARDA EN LA BASE DE DATOS EL OBJETO CREADO
			session['receta']= nueva_receta #leemos la recetaaa
			return render_template('ingredientes.html',receta=session['receta'], user=Ingrediente.query.filter_by(recetaid=nueva_receta.id ).all()) #se envia la receta y la lista de ingredientes desde la base de datos con el id de la receta
	return render_template('compartir_receta.html',userId = session['id'])#SE ENVIA EL ID DE USUARIO PARA USARLOS EN LA CREACION DE LA RECETA
@app.route('/ingredientes', methods = ['GET','POST'])
def ingredientes():
	if request.method == 'POST':
		if(request.form['ingrediente']):
			nuevo_ingrediente= Ingrediente(nombre=request.form['ingrediente'], cantidad=request.form['cantidad'], unidad=request.form['medida'], recetaid=request.form['recetaid'])#SE CREA UN OBJETO DE EL MODELO INGREDIENTE
			db.session.add(nuevo_ingrediente)
			db.session.commit()#SE GUARDA EN LA BASE DE DATOS EL OBJETO CREADO
			receta=session['receta'] #traemos la receta
			return render_template('ingredientes.html',receta=session['receta'],user=Ingrediente.query.filter_by(recetaid=receta.id).all())#se envia la receta y la lista de ingredientes desde la base de datos con el id de la receta
		else:
			return render_template('usuario_registrado.html')#sino trae un nombre de ingrediente te envia devuelta al MENU(USUARIO_REGISTRADO) 
	else:
		return render_template('usuario_registrado.html') 
@app.route('/consultar_ingredientes', methods = ['GET','POST'])
##########################################
def consultar_ingredientes():
	if request.method == 'POST':
		return render_template('consultar_ingredientes.html')

@app.route('/consultar_ranking', methods = ['GET','POST'])
def consultar_ranking():
	if request.method == 'POST':
		return render_template('consultar_ranking.html')

@app.route('/consultar_tiempo', methods = ['GET','POST'])
def consultar_tiempo():
	if request.method == 'POST':
		return render_template('consultar_tiempo.html')    
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