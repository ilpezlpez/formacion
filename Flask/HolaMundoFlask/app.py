from flask import Flask, request, render_template, jsonify, session, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

app = Flask(__name__)

app.secret_key = 'Mi_llave_secreta'

# http://localhost:5000/
#@app.route('/')
#def inicio():
    #    app.logger.debug('Mensaje a nivel debug')
    #    app.logger.info('Mensaje a nivel info')
    #    app.logger.warn('Mensaje a nivel warning')
    #    app.logger.error('Mensaje a nivel error')

   # app.logger.info(f'Entramos al path {request.path}')
   # return 'Hola Mundo desde Flask.'

@app.route('/')
def inicio():
    if 'username' in session:
        return f'El usuario ya ha hecho login {session["username"]}'
    return 'No ha hecho login'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Omitimos validación de usuario y password
        usuario = request.form['username']
        #Agregar el usuario a la sesión
        session['username'] = usuario
        # session['username'] = request.form['username']
        return redirect(url_for('inicio'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('inicio'))


@app.route('/saludar/<nombre>')
def saludar(nombre):
    return f'Saludos {nombre.upper()}'


@app.route('/edad/<int:edad>')
def mostrar_edad(edad):
    return f'Tu edad es: {edad + 10}'


@app.route('/mostrar/<nombre>', methods=['GET', 'POST'])
def mostrar_nombre(nombre):
    return render_template('mostrar.html', nombre=nombre)

@app.route('/salir')
def salir():
    return abort(404)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error404.html', error=error), 404

#REST Representational State Transfer
@app.route('/api/mostrar/<nombre>', methods=['GET', 'POST'])
def mostrar_json(nombre):
    valores = { 'nombre' : nombre , 'metodo_http' : request.method}
    return jsonify(valores)
