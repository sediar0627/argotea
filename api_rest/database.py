import sqlite3
from utils import md5

DATABASE_NAME = "argotea.db"

def connection():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def init_bd():
    tables = [
            """
            CREATE TABLE IF NOT EXISTS personas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identificacion INTEGER NOT NULL,
                nombre TEXT NOT NULL, 
                correo_electronico TEXT NOT NULL, 
                password TEXT NOT NULL, 
                edad INTEGER NOT NULL, 
                telefono TEXT NOT NULL, 
                rol TEXT NOT NULL
            )
            """
        ]
    
    conn = connection()
    cursor = conn.cursor()
    for table in tables:
        cursor.execute(table)
        
    
    statement_existe_super_administrador = "SELECT * FROM personas WHERE rol = ?"
    cursor.execute(statement_existe_super_administrador, ["1"])
    response_existe_super_administrador = cursor.fetchone()
    if(response_existe_super_administrador == None):
        statement_insert = """ 
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
        cursor.execute(statement_insert, [
            100110011001, 
            "SUPER ADMIN 1", 
            "super_admin@argotea.com",
            md5("12345"),
            100,
            100110011,
            "1",
            ])
        conn.commit()