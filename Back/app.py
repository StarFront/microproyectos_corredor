from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error



app = Flask(__name__, template_folder="../Front/templates")             #revisar esta vaina

def inicializar_bd():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            
            cursor.execute("CREATE DATABASE IF NOT EXISTS greenwork")
            
            cursor.execute("USE greenwork")
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_usuario VARCHAR(50) NOT NULL,
                    correo VARCHAR(100) NOT NULL,
                    contraseña VARCHAR(100) NOT NULL
                )
            """)
            print("Base de datos y tabla creadas o verificadas correctamente.")
    except Error as e:
        print("Error al inicializar la base de datos:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def registrar_usuario_en_bd(nombre_usuario, correo, contraseña):
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='greenwork'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            consulta = """
            INSERT INTO usuarios (nombre_usuario, correo, contraseña)
            VALUES (%s, %s, %s)
            """
            cursor.execute(consulta, (nombre_usuario, correo, contraseña))
            conexion.commit()
            print("Usuario registrado con éxito.")
    except Error as e:
        print("Error al registrar el usuario:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    nombre_usuario = request.form['nombre_usuario']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    registrar_usuario_en_bd(nombre_usuario, correo, contraseña)
    return redirect(url_for('index'))

if __name__ == "__main__":
    inicializar_bd()  
    app.run(debug=True)
