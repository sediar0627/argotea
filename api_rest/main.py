
from flask import Flask, jsonify, request
from auth import Auth
from database import init_bd
from persona import Persona, buscar_persona_con_token, login
from utils import leer_json

app = Flask(__name__)

config_app = leer_json('config/main_config.json')
    
config_auth = leer_json('config/auth_config.json')

auth = Auth(config_auth)

responses = leer_json('config/status_api.json')

@app.route('/persona/login', methods=["POST"])
def login_api():
    data = request.get_json()
    correo = data["correo_electronico"] 
    password = data["password"] 
    return jsonify(login(correo, password))

@app.route('/persona/registrar/usuario_final', methods=["POST"])
def registrar_usuario_final_api():
    data = request.get_json()
    identificacion = data["identificacion"] 
    nombre = data["nombre"] 
    correo_electronico = data["correo_electronico"] 
    password = data["password"] 
    edad = data["edad"] 
    telefono = data["telefono"] 
    usuario_final = Persona(0, identificacion, nombre, correo_electronico, password, edad, telefono, "3")
    usuario_final_response = usuario_final.registrarse()
    return jsonify(usuario_final_response)
    
@app.route('/persona/registrar', methods=["POST"])
def registrar_persona_api():
    data = request.get_json()
    identificacion = data["identificacion"] 
    nombre = data["nombre"] 
    correo_electronico = data["correo_electronico"] 
    password = data["password"] 
    edad = data["edad"] 
    telefono = data["telefono"]
    rol = data["rol"] 
    usuario_creador_token = data["usuario_creador_token"]
    if int(rol) > auth.auth_rol(usuario_creador_token):   
        persona = Persona(0, identificacion, nombre, correo_electronico, password, edad, telefono, rol)
        crear_persona = persona.registrarse()
        return jsonify(crear_persona)
    else:
        return jsonify({
                    "status": responses["main"]["main___sin_permisos"]["status"],
                    "message": responses["main"]["main___sin_permisos"]["message"]
                    })
    
@app.route('/persona/actualizar/<id>', methods=["PUT"])
def actualizar_persona_api(id):
    data = request.get_json()
    identificacion = data["identificacion"] 
    nombre = data["nombre"] 
    correo_electronico = data["correo_electronico"] 
    password = data["password"] 
    edad = data["edad"] 
    telefono = data["telefono"]
    rol = data["rol"] 
    token = data["token"]
    if(token != ""):
        persona = Persona(id, identificacion, nombre, correo_electronico, password, edad, telefono, rol)
        actualizar_persona = persona.actualizarce(token)
        return jsonify(actualizar_persona) 
    else:
        return jsonify({
                    "status": responses["main"]["main___bad_request"]["status"],
                    "message": responses["main"]["main___bad_request"]["message"]
                    })

@app.route('/persona/buscar/<type_search>/<search>', methods=["POST"])
def buscar_persona_api(type_search, search):
    data = request.get_json()
    token = data["token"]
    if(token != ""):
        person = buscar_persona_con_token(token, type_search, search)  
        return jsonify(person) 
    else:
        return jsonify({
                    "status": responses["main"]["main___bad_request"]["status"],
                    "message": responses["main"]["main___bad_request"]["message"]
                    })
        
if __name__ == "__main__":
    
    init_bd()
    
    app.run(
        host=config_app['host'], 
        port=config_app['port'], 
        debug=config_app['debug']
        )
