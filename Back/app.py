from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error



app = Flask(__name__, template_folder="../Front/templates", static_folder="../Front/")
app.secret_key = 'clave_secreta'       

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

def verificar_usuario(correo, contraseña):
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='greenwork'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            consulta = "SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s"
            cursor.execute(consulta, (correo, contraseña))
            usuario = cursor.fetchone()
            return usuario is not None
    except Error as e:
        print("Error al verificar el usuario:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
    return False

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

@app.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    
    if verificar_usuario(correo, contraseña):
        
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='greenwork'
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre_usuario FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        nombre_usuario = usuario[0] if usuario else None
        
        session['correo'] = correo  
        session['nombre_usuario'] = nombre_usuario
        
        flash('Inicio de sesión exitoso')
        return redirect(url_for('dashboard'))  
    else:
        flash('Correo o contraseña incorrectos')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'correo' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    inicializar_bd()  
    app.run(debug=True)
