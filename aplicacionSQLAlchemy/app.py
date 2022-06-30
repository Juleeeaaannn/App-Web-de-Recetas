from datetime import datetime
from flask import Flask, request, render_template, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

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
			session['user'] = usuario_actual
			if usuario_actual is None:
				return render_template('error.html', error="El correo no está registrado")
			else:
				clave=hashlib.md5(bytes( request.form['password'], encoding='UTF-8'))
				if (usuario_actual.clave == clave.hexdigest()):                    
					return render_template('usuario_registrado.html')
				else:
					return render_template('error.html', error="La contraseña no es válida")
	else:
		return render_template('inicio.html')
@app.route('/menu')
def menu():
	return render_template('usuario_registrado.html')
@app.route('/nuevo_usuario', methods = ['GET','POST'])
def nuevo_usuario():   
	if request.method == 'POST':
		if not request.form['nombre'] or not request.form['email'] or not request.form['password']:
			return render_template('error.html', error="¡Los datos ingresados no son correctos!")
		else:
			clave=hashlib.md5(bytes( request.form['password'], encoding='UTF-8'))
			nuevo_usuario = Usuario(nombre=request.form['nombre'], correo = request.form['email'], clave=clave.hexdigest())
			db.session.add(nuevo_usuario)
			db.session.commit()
			return render_template('aviso.html', mensaje="El usuario se registró exitosamente")
	return render_template('nuevo_usuario.html')

###############################
@app.route('/compartir_receta', methods = ['GET','POST'])
def compartir_receta():
	if request.method == 'POST':
		if not request.form['nombre'] or not request.form['tiempo'] or not request.form['descripcion']:
			return render_template('error.html', error="¡Por favor ingrese todos los datos requeridos!")
		else:
			user=session['user']            
			nueva_receta= Receta(nombre=request.form['nombre'], tiempo=request.form['tiempo'], elaboracion=request.form['descripcion'], cantidadmegusta=0, fecha=datetime.now(), usuarioid = user.id)    #SE CREA UN OBJETO DE EL MODELO RECETAS
			db.session.add(nueva_receta)
			db.session.commit()#SE GUARDA EN LA BASE DE DATOS EL OBJETO CREADO
			session['receta']= nueva_receta #leemos la recetaaa
			return render_template('ingredientes.html',receta=session['receta'], user=Ingrediente.query.filter_by(recetaid=nueva_receta.id ).all()) #se envia la receta y la lista de ingredientes desde la base de datos con el id de la receta
	else:
		user=session['user']
		return render_template('compartir_receta.html',userId = user.id)#SE ENVIA EL ID DE USUARIO PARA USARLOS EN LA CREACION DE LA RECETA

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

##########################################
@app.route('/consultar_ranking')
def consultar_ranking():
	recetas=Receta.query.order_by(desc(Receta.cantidadmegusta)).limit(5).all() #Ordena por cantidad de me gusta y trae solo los primeros 5
	return render_template('consultar_ranking.html',receta=recetas,Receta=Receta,usuarios=Usuario.query.all())

##########################################
@app.route('/consultar_tiempo', methods = ['GET','POST'])
def consultar_tiempo():
	if request.method == 'POST':
		if not request.form['tiempo_ingresado']:
			return render_template('error.html', error="¡Por favor ingrese todos los datos requeridos!")
		else:
			return render_template('consultar_tiempo.html', receta = Receta.query.all(), tiempo = int(request.form['tiempo_ingresado']))    
	else:
		return render_template('consultar_tiempo.html', receta = None) 
@app.route('/ver_receta', methods = ['GET','POST'])
def ver_receta():
	if request.method == 'POST':
		recetaid= request.form['ide']
		receta=Receta.query.filter_by(id=recetaid).first()
		listaingredietes=Ingrediente.query.filter_by(recetaid=recetaid).all()
		usuarios=Usuario.query.all()
		user=session['user']
		return render_template('ver_receta.html',receta=receta,ingredientes=listaingredietes,user=user,usuarios=usuarios)
@app.route('/megusta', methods = ['GET','POST'])
def megusta():
	if request.method == 'POST':
		db.session.query(Receta).filter_by(id=request.form['recetaid']).update({'cantidadmegusta':Receta.cantidadmegusta+1})
		db.session.commit()
		return render_template('usuario_registrado.html')
#####################################
@app.route('/consultar_ingredientes', methods = ['GET','POST'])
def consultar_ingredientes():
	if request.method == 'POST':
		if not request.form['ingrediente']:
			return render_template('error.html', error="¡Por favor ingrese todos los datos requeridos!")
		else:
			return render_template('consultar_ingredientes.html', ingrediente=request.form['ingrediente'], ingredientes=Ingrediente.query.all(), recetas=Receta.query.all())
	else:
		return render_template('consultar_ingredientes.html', Ingrediente=None)
if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)	