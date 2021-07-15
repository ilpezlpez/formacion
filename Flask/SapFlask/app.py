from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect

from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__)

#Configuración de la base de datos

USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Inicialización del objeto db de sqlamchemy
#db = SQLAlchemy(app)  ....se elimina la inicialización en este archivo y se hace en database.py,
# con el siguiente código se inicializa la app importando db desde database.py
db.init_app(app)

#Configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

#Configurar flask-wtf

app.config['SECRET_KEY']='llave_secreta'

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    #Listado de personas
    #personas = Persona.query.all() ...muestra los registron sin orden, order_by perimte indicar orden
    personas = Persona.query.order_by('id')
    total_personas = Persona.query.count()
    app.logger.debug(f'Listado Personas: {personas}')
    app.logger.debug(f'Total Personas: {total_personas}')
    return render_template('index.html', personas = personas, total_personas = total_personas)

@app.route('/ver/<int:id>')
def ver_detalle(id):
    #Recuperamos la persona según el id porporcionado
    #persona = Persona.query.get(id)   Este método get es válido para  recuperar el objeto de tipo persona vía el id,
# pero es susceptible  aerroes y habría que configurar por separado
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', persona = persona)

@app.route('/agregar', methods=['POST', 'GET'])
def agregar():
    persona = Persona()
    personaForm = PersonaForm(obj=persona)
    if request.method =='POST':
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            app.logger.debug(f'Persona a insertar: {persona}')
            #Insertamos el nuevo registro en la base de datos
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('agregar.html', forma = personaForm)

@app.route('/editar/<int:id>', methods = ['GET','POST'])
def editar(id):
    #Recuperamos el objeto persona a editar
    persona = Persona.query.get_or_404(id)
    personaForma = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForma.validate_on_submit():
            personaForma.populate_obj(persona)
            app.logger.debug(f'Persona a editar: {persona}')
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('editar.html', forma=personaForma)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Persona a eliminar: {persona}')
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('inicio'))