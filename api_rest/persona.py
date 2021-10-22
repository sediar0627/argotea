from database import connection
from auth import Auth
from utils import leer_json, md5

config_auth = leer_json('config/auth_config.json')
    
auth = Auth(config_auth)

responses = leer_json('config/status_api.json')

def persona_con_permisos(token, rol_persona_comparar):
    if(token != ""):
        usuario = auth.is_auth(token)
        if(usuario["status"] == responses["auth"]["is_auth___ok"]["status"]):
            usuario_rol = int(usuario["usuario"]["rol"])
            person_rol = int(rol_persona_comparar)
            if person_rol > usuario_rol:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
    
def map_persona(response):
    
    data_person = {
            "status": responses["persona"]["persona___encontrada_ok"]["status"],
            "message": responses["persona"]["persona___encontrada_ok"]["message"],
            "id": response[0],
            "identificacion": response[1], 
            "nombre": response[2], 
            "correo_electronico": response[3],
            "edad": response[5],
            "telefono": response[6],
            "rol": response[7]
         }
    
    return data_person

def map_persona_con_token(token_user_search, response):
    
    data_person = map_persona(response)
    
    user_search_permiss = persona_con_permisos(token_user_search, data_person["rol"])
    
    if(user_search_permiss):
        return data_person
    else:
        is_auth = auth.is_auth(token_user_search)
        if is_auth["status"] != responses["auth"]["is_auth___unauthorized"]["status"]:   
            return {
                    "status": responses["persona"]["persona___encontrada_fail"]["status"],
                    "message": responses["persona"]["persona___encontrada_fail"]["message"]
                    }
        else:
            return is_auth

def existe_persona(search):
    
    conn = connection()
    cursor = conn.cursor()
    
    statement_identificacion = "SELECT * FROM personas WHERE identificacion = ?"
    statement_correo = "SELECT * FROM personas WHERE correo_electronico = ?"
    
    cursor.execute(statement_identificacion, [search])
    response_identificacion = cursor.fetchone()
    
    cursor.execute(statement_correo, [search])
    response_correo = cursor.fetchone()
    
    if response_identificacion == None and response_correo == None:
        return False
    else:
        return True

def buscar_persona_con_token(token_user_search, type_search, search):
    
    conn = connection()
    cursor = conn.cursor()
    statement = ""
    
    if type_search == "id":
        statement = "SELECT * FROM personas WHERE id = ?"
    elif type_search == "identificacion":
        statement = "SELECT * FROM personas WHERE identificacion = ?"
    elif type_search == "correo":
        statement = "SELECT * FROM personas WHERE correo_electronico = ?"
        
    if statement != "":
        cursor.execute(statement, [search])
        response = cursor.fetchone()
        if response != None:
            return map_persona_con_token(token_user_search, response)
        else:
            return {
                "status": responses["persona"]["persona___encontrada_fail"]["status"],
                "message": responses["persona"]["persona___encontrada_fail"]["message"]
                }
    else:
        return {
                "status": responses["persona"]["persona___bad_request"]["status"],
                "message": responses["persona"]["persona___bad_request"]["message"]
                }

def login(correo, password):
    
    correo = correo.lower()
    password = md5(password)
    
    statement = "SELECT * FROM personas WHERE correo_electronico = ? AND password = ?"
    
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(statement, [correo, password])
    response = cursor.fetchone()
    
    if response != None:
        data_person = map_persona(response)
        token = auth.encode(data_person)
        data_person["token"] = token
        return data_person
    else:
        return {
                "status": responses["persona"]["login___fail"]["status"],
                "message": responses["persona"]["login___fail"]["message"]
                }

class Persona:
    
    def __init__(self, 
                 id, 
                 identificacion, 
                 nombre, 
                 correo_electronico, 
                 password, 
                 edad, 
                 telefono, 
                 rol):
        
        self.id = id
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo_electronico = correo_electronico
        self.password = password
        self.edad = edad
        self.telefono = telefono
        self.rol = rol
    
    def registrarse(self):
        existe_persona_identificacion = existe_persona(self.identificacion)
        existe_persona_correo = existe_persona(self.correo_electronico)
        if(existe_persona_identificacion == False and existe_persona_correo == False):
            conn = connection()
            cursor = conn.cursor()
            statement = """ 
                INSERT INTO personas 
                    (identificacion, 
                     nombre, 
                     correo_electronico,
                     password,
                     edad,
                     telefono,
                     rol) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(statement, [
                self.identificacion, 
                self.nombre, 
                self.correo_electronico,
                md5(self.password),
                self.edad,
                self.telefono,
                self.rol,
                ])
            conn.commit()
    
            statement_identificacion = "SELECT * FROM personas WHERE identificacion = ?"
            cursor.execute(statement_identificacion, [self.identificacion])
            response_identificacion = cursor.fetchone()
            data_person = map_persona(response_identificacion)
            token = auth.encode(data_person)
            data_person["token"] = token
            return data_person
        else:
            return {
                    "status": responses["persona"]["persona___existe_persona"]["status"],
                    "message": responses["persona"]["persona___existe_persona"]["message"]
                    }
        
    def actualizarce(self, token):
        conn = connection()
        cursor = conn.cursor()
        statement_id = "SELECT * FROM personas WHERE id = ?"
        cursor.execute(statement_id, [self.id])          
        response = cursor.fetchone()
        
        if response != None:
            
            data_persona_bd = map_persona(response)
            data_persona_token = auth.is_auth(token)
            
            id_igual = data_persona_bd["id"] == data_persona_token["id"]
            identificacion_igual = data_persona_bd["identificacion"] == data_persona_token["usuario"]["identificacion"]
            correo_igual = data_persona_bd["correo_electronico"] == data_persona_token["usuario"]["correo_electronico"]
            
            autenticado = data_persona_token["status"] == responses["auth"]["is_auth___ok"]["status"]
            
            if id_igual and identificacion_igual and correo_igual and autenticado:
                
                statement_update = """
                                    UPDATE personas SET 
                                        identificacion = ?, 
                                        nombre = ?, 
                                        correo_electronico = ?, 
                                        password = ?, 
                                        edad = ?, 
                                        telefono = ?, 
                                        rol = ? 
                                    WHERE id = ?
                                """
                                
                cursor.execute(statement_update, [
                    self.identificacion, 
                    self.nombre, 
                    self.correo_electronico,
                    md5(self.password),
                    self.edad,
                    self.telefono,
                    self.rol,
                    self.id
                    ])
                conn.commit()
                
                statement_identificacion = "SELECT * FROM personas WHERE identificacion = ?"
                cursor.execute(statement_identificacion, [self.identificacion])
                response_identificacion = cursor.fetchone()
                data_person = map_persona(response_identificacion)
                token = auth.encode(data_person)
                data_person["token"] = token
                return data_person
            
            else:
                if autenticado: 
                    return {
                        "status": responses["persona"]["persona___token_invalido"]["status"],
                        "message": responses["persona"]["persona___token_invalido"]["message"]
                        }
                else:
                    return data_persona_token
        
        else:
            return {
                "status": responses["persona"]["persona___encontrada_fail"]["status"],
                "message": responses["persona"]["persona___encontrada_fail"]["message"]
                }
                    