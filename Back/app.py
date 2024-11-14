from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
#import diosito



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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS perfil (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT,
                    nombres VARCHAR(100),
                    apellidos VARCHAR(100),
                    cedula VARCHAR(20),
                    telefono VARCHAR(20),
                    fecha_nacimiento DATE,
                    foto_perfil VARCHAR(255),
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            """)
            print("Base de datos y tablas creadas o verificadas correctamente.")
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
    
@app.route('/logout')
def logout():
    session.pop('correo', None)
    session.pop('nombre_usuario', None)
    flash('Has cerrado sesión exitosamente')
    return redirect(url_for('index'))

# @app.route('/perfil')
# def perfil():
#     if 'correo' in session:
#         return render_template('usuario.html')
#     else:
#         return redirect(url_for('index'))

@app.route('/marketplace')
def marketplace():
    if 'correo' in session:
        return render_template('marketplace.html')
    else:
        return redirect(url_for('index'))

@app.route('/postulaciones')
def postulaciones():
    if 'correo' in session:
        return render_template('postulaciones.html')
    else:
        return redirect(url_for('index'))

@app.route('/mis_proyectos')
def mis_proyectos():
    if 'correo' in session:
        return render_template('mis_proyectos.html')
    else:
        return redirect(url_for('index'))
    
def obtener_perfil(usuario_id):
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='greenwork'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            consulta = "SELECT * FROM perfil WHERE usuario_id = %s"
            cursor.execute(consulta, (usuario_id,))
            perfil = cursor.fetchone()
            return perfil
    except Error as e:
        print("Error al obtener el perfil:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()



def actualizar_perfil(usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, foto_perfil):
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
            UPDATE perfil
            SET nombres = %s, apellidos = %s, cedula = %s, telefono = %s, fecha_nacimiento = %s, foto_perfil = %s
            WHERE usuario_id = %s
            """
            cursor.execute(consulta, (nombres, apellidos, cedula, telefono, fecha_nacimiento, foto_perfil, usuario_id))
            conexion.commit()
            print("Perfil actualizado con éxito.")
    except Error as e:
        print("Error al actualizar el perfil:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def crear_perfil(usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, foto_perfil):
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
            INSERT INTO perfil (usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, foto_perfil)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(consulta, (usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, foto_perfil))
            conexion.commit()
            print("Perfil creado con éxito.")
    except Error as e:
        print("Error al crear el perfil:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


@app.route('/actualizar_perfil', methods=['POST'])
def actualizar_perfil_view():
    if 'correo' in session:
        usuario_id = obtener_usuario_id_por_correo(session['correo'])

        
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['cedula']
        telefono = request.form['telefono']
        fecha_nacimiento = request.form['nacimiento']
        foto_perfil = request.files['foto-perfil']

        print(f"nombres: {nombres}, apellidos: {apellidos}, cedula: {cedula}, telefono: {telefono}, fecha_nacimiento: {fecha_nacimiento}")

        
        if foto_perfil:
            foto_perfil_filename = f"foto_{usuario_id}.jpg"
            foto_perfil.save(f'Front/img/img_perfil/{foto_perfil_filename}')
            foto_perfil = foto_perfil_filename
        else:
            foto_perfil = None

        
        perfil = obtener_perfil(usuario_id)
        if perfil:
            
            actualizar_perfil(usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, foto_perfil)
        else:
            
            crear_perfil(usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, foto_perfil)

        flash('Perfil actualizado correctamente.')
        return redirect(url_for('perfil'))
    else:
        return redirect(url_for('index'))


@app.route('/perfil')
def perfil():
    if 'correo' in session:
        usuario_id = obtener_usuario_id_por_correo(session['correo'])
        perfil = obtener_perfil(usuario_id)
        return render_template('usuario.html', perfil=perfil)
    else:
        return redirect(url_for('index'))

def obtener_usuario_id_por_correo(correo):
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='greenwork'
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.")
            cursor = conexion.cursor()
            consulta = "SELECT id FROM usuarios WHERE correo = %s"
            cursor.execute(consulta, (correo,))
            usuario = cursor.fetchone()
            print(f"Usuario ID: {usuario[0] if usuario else 'No encontrado'}")
            return usuario[0] if usuario else None
    except Error as e:
        print("Error al obtener el ID del usuario:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

@app.route('/muestra_perfil')
def muestra_perfil():
    if 'correo' in session:
        usuario_id = obtener_usuario_id_por_correo(session['correo'])
        perfil = obtener_perfil(usuario_id)
        
        if perfil:
            return render_template('muestra_perfil.html', perfil=perfil)
        else:
            flash('No se ha encontrado un perfil para este usuario.')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))



if __name__ == "__main__":
    inicializar_bd()  
    app.run(debug=True)
