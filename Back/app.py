from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
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
                    experiencia VARCHAR(255),
                    foto_perfil VARCHAR(255),
                    
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trabajos (
                    id_trabajo INT AUTO_INCREMENT PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL,
                    descripcion TEXT,
                    duracion VARCHAR(50),
                    ubicacion VARCHAR(255),
                    pago ENUM('Por hora', 'Por tarea') NOT NULL,
                    monto DECIMAL(10, 2),
                    fotografia VARCHAR(255),
                    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
                    id_usuario INT,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS postulaciones (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_usuario INT NOT NULL,
                    id_trabajo INT NOT NULL,
                    estado ENUM('pendiente', 'aceptado', 'rechazado') DEFAULT 'pendiente',
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
                    FOREIGN KEY (id_trabajo) REFERENCES trabajos(id_trabajo)
                )
            """)
            print("Base de datos y tablas creadas o verificadas correctamente.")
    except Error as e:
        print("Error al inicializar la base de datos:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


@app.route('/cambiar_estado_activo/<int:id>', methods=['POST'])
def cambiar_estado_activo(id):
    if 'correo' in session:
        try:
            # Conexión a la base de datos
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='greenwork'
            )
            cursor = conexion.cursor()

            # Cambiar el estado a inactivo
            cursor.execute("UPDATE trabajos SET estado = 'activo' WHERE id_trabajo = %s", (id,))

            # Confirmar cambios
            conexion.commit()
            flash('Estado del trabajo cambiado a activo.')
        except Error as e:
            print("Error al cambiar el estado del trabajo:", e)
            flash('Ocurrió un error al cambiar el estado.')
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
        return redirect(url_for('mis_proyectos'))
    else:
        flash('Debes iniciar sesión para realizar esta acción.')
        return redirect(url_for('index'))



@app.route('/cambiar_estado_trabajo/<int:id>', methods=['POST'])
def cambiar_estado_trabajo(id):
    if 'correo' in session:
        try:
            # Conexión a la base de datos
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='greenwork'
            )
            cursor = conexion.cursor()

            # Cambiar el estado a inactivo
            cursor.execute("UPDATE trabajos SET estado = 'inactivo' WHERE id_trabajo = %s", (id,))

            # Confirmar cambios
            conexion.commit()
            flash('Estado del trabajo cambiado a inactivo.')
        except Error as e:
            print("Error al cambiar el estado del trabajo:", e)
            flash('Ocurrió un error al cambiar el estado.')
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
        return redirect(url_for('mis_proyectos'))
    else:
        flash('Debes iniciar sesión para realizar esta acción.')
        return redirect(url_for('index'))


@app.route('/eliminar_trabajo/<int:id>', methods=['POST'])
def eliminar_trabajo(id):
    if 'correo' in session:
        try:
            # Conexión a la base de datos
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='greenwork'
            )
            cursor = conexion.cursor()

            # Eliminar las postulaciones asociadas al trabajo
            cursor.execute("DELETE FROM postulaciones WHERE id_trabajo = %s", (id,))

            # Eliminar el trabajo
            cursor.execute("DELETE FROM trabajos WHERE id_trabajo = %s", (id,))

            # Confirmar cambios
            conexion.commit()
            flash('Trabajo eliminado correctamente.')
        except Error as e:
            print("Error al eliminar el trabajo:", e)
            flash('Ocurrió un error al eliminar el trabajo.')
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
        return redirect(url_for('mis_proyectos'))
    else:
        flash('Debes iniciar sesión para realizar esta acción.')
        return redirect(url_for('index'))



@app.route('/mis_proyectos')
def mis_proyectos():
    if 'correo' in session:
        try:
            # Conexión a la base de datos
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='greenwork'
            )
            cursor = conexion.cursor(dictionary=True)

            # Obtener el ID del usuario logueado
            id_usuario = obtener_usuario_id_por_correo(session['correo'])

            # Consultar los trabajos del usuario
            cursor.execute("""
                SELECT id_trabajo, titulo, estado FROM trabajos WHERE id_usuario = %s
            """, (id_usuario,))
            trabajos = cursor.fetchall()

            # Renderizar la plantilla y pasar los trabajos
            return render_template('mis_proyectos.html', trabajos=trabajos)

        except Error as e:
            print("Error al obtener los trabajos:", e)
            flash('Ocurrió un error al cargar tus proyectos.')
            return redirect(url_for('dashboard'))
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    else:
        flash('Debes iniciar sesión para ver tus proyectos.')
        return redirect(url_for('index'))

@app.route('/actualizar_estado_postulacion/<int:id>/<estado>', methods=['POST'])
def actualizar_estado_postulacion(id, estado):
    # Conexión a la base de datos
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='greenwork'
    )
    cursor = conexion.cursor()

    # Actualizar el estado de la postulación
    cursor.execute("UPDATE postulaciones SET estado = %s WHERE id = %s", (estado, id))
    conexion.commit()
    conexion.close()

    return redirect(request.referrer)  # Redirige a la misma página


@app.route('/vista_postulados/<int:id>')
def vista_postulados(id):
    # Conexión a la base de datos
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='greenwork'
    )
    cursor = conexion.cursor(dictionary=True)

    # Obtener el trabajo por ID
    cursor.execute("SELECT * FROM trabajos WHERE id_trabajo = %s", (id,))
    trabajo = cursor.fetchone()

    # Obtener postulados del trabajo con detalles del perfil
    cursor.execute("""
        SELECT 
            p.nombres, 
            p.telefono, 
            p.experiencia, 
            po.estado, 
            po.id AS id_postulacion
        FROM postulaciones po
        JOIN perfil p ON po.id_usuario = p.usuario_id
        WHERE po.id_trabajo = %s
    """, (id,))
    postulados = cursor.fetchall()

    conexion.close()

    if trabajo:
        return render_template('vista_postulados.html', trabajo=trabajo, postulados=postulados)
    else:
        return "Trabajo no encontrado", 404




@app.route('/postular/<int:id_trabajo>', methods=['POST'])
def postular(id_trabajo):
    if 'correo' in session:
        try:
            # Conexión a la base de datos
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='greenwork'
            )
            cursor = conexion.cursor()

            # Obtener el ID del usuario logueado
            id_usuario = obtener_usuario_id_por_correo(session['correo'])

            # Verificar si ya está postulado
            consulta_verificar = "SELECT * FROM postulaciones WHERE id_usuario = %s AND id_trabajo = %s"
            cursor.execute(consulta_verificar, (id_usuario, id_trabajo))
            postulacion_existente = cursor.fetchone()

            if postulacion_existente:
                flash('Ya te has postulado a este trabajo.')
                return redirect(url_for('visgeneral', id=id_trabajo))

            # Insertar la postulación en la base de datos
            consulta = "INSERT INTO postulaciones (id_usuario, id_trabajo, estado) VALUES (%s, %s, 'pendiente')"
            cursor.execute(consulta, (id_usuario, id_trabajo))
            conexion.commit()

            flash('Te has postulado exitosamente.')
            return redirect(url_for('postulaciones'))
        except Error as e:
            print("Error al postularse:", e)
            flash('Ocurrió un error al postularte.')
            return redirect(url_for('visgeneral', id=id_trabajo))
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    else:
        flash('Debes iniciar sesión para postularte.')
        return redirect(url_for('index'))

@app.route('/postulaciones')
def postulaciones():
    if 'correo' in session:
        try:
            # Conexión a la base de datos
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='greenwork'
            )
            cursor = conexion.cursor(dictionary=True)

            # Obtener el ID del usuario logueado
            id_usuario = obtener_usuario_id_por_correo(session['correo'])

            # Consultar las postulaciones
            cursor.execute("""
                SELECT p.estado, t.titulo, t.descripcion, t.fotografia, t.monto, t.ubicacion, t.id_trabajo
                FROM postulaciones p
                JOIN trabajos t ON p.id_trabajo = t.id_trabajo
                WHERE p.id_usuario = %s
            """, (id_usuario,))
            postulaciones = cursor.fetchall()

            # Organizar las postulaciones en columnas
            pendientes = [p for p in postulaciones if p['estado'] == 'pendiente']
            aceptados = [p for p in postulaciones if p['estado'] == 'aceptado']
            rechazados = [p for p in postulaciones if p['estado'] == 'rechazado']

            return render_template('postulaciones.html', pendientes=pendientes, aceptados=aceptados, rechazados=rechazados)
        except Error as e:
            print("Error al obtener postulaciones:", e)
            flash('Ocurrió un error al cargar tus postulaciones.')
            return redirect(url_for('dashboard'))
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    else:
        flash('Debes iniciar sesión para ver tus postulaciones.')
        return redirect(url_for('index'))


@app.route('/registrar_trabajo', methods=['POST'])
def registrar_trabajo():
    if 'correo' in session:
        # Datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form.get('descripcion', None)
        duracion = request.form['duracion']
        ubicacion = request.form.get('ubicacion', None)
        pago = request.form.get('pago', None)
        monto = request.form.get('monto', None)
        foto_trabajo = request.files.get('file-upload', None)

        # Guardar foto, si se proporciona
        foto_filename = None
        usuario_id = obtener_usuario_id_por_correo(session['correo'])
        if foto_trabajo:
            # Generar un nombre único basado en el usuario y trabajo
            foto_filename = f"trabajo_{usuario_id}_{titulo.replace(' ', '_')}.jpg"
            #foto_trabajo.save(f'Front/img/trabajos/{foto_filename}')
            ruta_base = os.path.dirname(os.path.abspath(__file__))

            # Ruta al directorio 'trabajos'
            ruta_directorio = os.path.join(ruta_base, '../Front/img/trabajos')

            # Crear el directorio si no existe
            if not os.path.exists(ruta_directorio):
                os.makedirs(ruta_directorio)

            # Ruta completa del archivo
            foto_trabajo_path = os.path.join(ruta_directorio, foto_filename)
            foto_trabajo.save(foto_trabajo_path)

        else:
            foto_filename = "sin_imagen.png"
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
                INSERT INTO trabajos (titulo, descripcion, duracion, ubicacion, pago, monto, fotografia, id_usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(consulta, (titulo, descripcion, duracion, ubicacion, pago, monto, foto_filename, usuario_id))
                conexion.commit()
                flash('Trabajo registrado con éxito.')
        except Error as e:
            print("Error al registrar el trabajo:", e)
            flash('Ocurrió un error al registrar el trabajo.')
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

        return redirect(url_for('marketplace'))
    else:
        return redirect(url_for('index'))



@app.route('/api/trabajos')
def obtener_trabajos():
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='greenwork'
    )
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_trabajo, titulo, descripcion, monto, ubicacion, fotografia FROM trabajos WHERE estado = 'activo'")
    trabajos = cursor.fetchall()
    
    # Agregar rutas completas a las imágenes y enlaces
    for trabajo in trabajos:
        trabajo['fotografia'] = url_for('static', filename=f"/img/trabajos/{trabajo['fotografia']}")
        trabajo['enlace'] = url_for('visgeneral', id=trabajo['id_trabajo'])  # Suponiendo que tienes esta ruta
    
    conexion.close()
    return jsonify(trabajos)

@app.route('/visgeneral/<int:id>')
def visgeneral(id):
    # Conexión a la base de datos
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='greenwork'
    )
    cursor = conexion.cursor(dictionary=True)
    
    # Obtener el trabajo completo por ID
    cursor.execute("SELECT * FROM trabajos WHERE id_trabajo = %s", (id,))
    trabajo = cursor.fetchone()
    
    conexion.close()
    
    # Verificar si se encontró el trabajo
    if trabajo:
        return render_template('visgeneral.html', trabajo=trabajo)
    else:
        return "Trabajo no encontrado", 404



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
            cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s OR correo = %s", (nombre_usuario, correo))
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                print("El nombre de usuario o el correo ya están registrados.")
                return "Error: El nombre de usuario o el correo ya están registrados."
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



@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    nombre_usuario = request.form['nombre_usuario']
    correo = request.form['correo']
    contraseña = request.form['contraseña']

    registrar_usuario_en_bd(nombre_usuario, correo, contraseña)

    return redirect(url_for('index')) 

    #return redirect(url_for('index'))

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
        try:
            # Conexión a la base de datos
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='greenwork'
            )
            cursor = conexion.cursor(dictionary=True)

            # Obtener el ID del usuario logueado
            id_usuario = obtener_usuario_id_por_correo(session['correo'])

            # Consultar las últimas postulaciones aceptadas
            cursor.execute("""
                SELECT trabajos.titulo
                FROM postulaciones
                JOIN trabajos ON postulaciones.id_trabajo = trabajos.id_trabajo
                WHERE postulaciones.id_usuario = %s AND postulaciones.estado = 'aceptado'
                ORDER BY postulaciones.id DESC
                LIMIT 5
            """, (id_usuario,))
            postulaciones_aceptadas = cursor.fetchall()

            # Consultar los últimos 5 proyectos publicados por el usuario
            cursor.execute("""
                SELECT titulo, estado
                FROM trabajos
                WHERE id_usuario = %s
                ORDER BY id_trabajo DESC
                LIMIT 5
            """, (id_usuario,))
            proyectos_publicados = cursor.fetchall()

            # Renderizar la plantilla del dashboard
            return render_template(
                'dashboard.html',
                postulaciones_aceptadas=postulaciones_aceptadas,
                proyectos_publicados=proyectos_publicados
            )

        except Error as e:
            print("Error al cargar el dashboard:", e)
            flash('Ocurrió un error al cargar el dashboard.')
            return redirect(url_for('index'))
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    else:
        flash('Debes iniciar sesión para acceder al dashboard.')
        return redirect(url_for('index'))

    
@app.route('/logout')
def logout():
    session.pop('correo', None)
    session.pop('nombre_usuario', None)
    flash('Has cerrado sesión exitosamente')
    return redirect(url_for('index'))

@app.route('/marketplace')
def marketplace():
    if 'correo' in session:
        return render_template('marketplace.html')
    else:
        return redirect(url_for('index'))

@app.route('/formulario_usuario')
def formulario_usuario():
    if 'correo' in session:
        return render_template('formulario_usuario.html')
    else:
        return redirect(url_for('index'))

# @app.route('/postulaciones')
# def postulaciones():
#     if 'correo' in session:
#         return render_template('postulaciones.html')
#     else:
#         return redirect(url_for('index'))

# @app.route('/mis_proyectos')
# def mis_proyectos():
#     if 'correo' in session:
#         return render_template('mis_proyectos.html')
#     else:
#         return redirect(url_for('index'))
    
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

def actualizar_perfil(usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, experiencia, foto_perfil):
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='greenwork'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()

            # Si la imagen no es nueva, no actualizar foto_perfil
            if foto_perfil:
                consulta = """
                UPDATE perfil
                SET nombres = %s, apellidos = %s, cedula = %s, telefono = %s, fecha_nacimiento = %s, experiencia = %s, foto_perfil = %s
                WHERE usuario_id = %s
                """
                cursor.execute(consulta, (nombres, apellidos, cedula, telefono, fecha_nacimiento, experiencia, foto_perfil, usuario_id))
            else:
                consulta = """
                UPDATE perfil
                SET nombres = %s, apellidos = %s, cedula = %s, telefono = %s, fecha_nacimiento = %s, experiencia = %s
                WHERE usuario_id = %s
                """
                cursor.execute(consulta, (nombres, apellidos, cedula, telefono, fecha_nacimiento, experiencia, usuario_id))
            
            conexion.commit()
            print("Perfil actualizado con éxito.")
    except Error as e:
        print("Error al actualizar el perfil:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def crear_perfil(usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, experiencia, foto_perfil):
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
            INSERT INTO perfil (usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, experiencia, foto_perfil)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(consulta, (usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, experiencia, foto_perfil))
            conexion.commit()
            print("Perfil creado con éxito.")
    except Error as e:
        print("Error al crear el perfil:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
import os

@app.route('/actualizar_perfil', methods=['POST'])
def actualizar_perfil_view():
    if 'correo' in session:
        usuario_id = obtener_usuario_id_por_correo(session['correo'])

        
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['cedula']
        telefono = request.form['telefono']
        fecha_nacimiento = request.form['nacimiento']
        experiencia = request.form['experiencia']
        foto_perfil = request.files['foto-perfil']

        print(f"nombres: {nombres}, apellidos: {apellidos}, cedula: {cedula}, telefono: {telefono}, fecha_nacimiento: {fecha_nacimiento}, experiencia: {experiencia}")

        
        if foto_perfil:
            foto_perfil_filename = f"foto_{usuario_id}.jpg"
            # foto_perfil.save(f'Front/img/img_perfil/{foto_perfil_filename}')
            # foto_perfil = foto_perfil_filename
            # Ruta absoluta al directorio 'img_perfil'
            ruta_base = os.path.dirname(os.path.abspath(__file__))
            ruta_directorio = os.path.join(ruta_base, '../Front/img/img_perfil')

            # Crear el directorio si no existe
            if not os.path.exists(ruta_directorio):
                os.makedirs(ruta_directorio)

            # Guardar la imagen en la ruta calculada
            foto_perfil_path = os.path.join(ruta_directorio, foto_perfil_filename)
            foto_perfil.save(foto_perfil_path)
            foto_perfil = foto_perfil_filename
        else:
            foto_perfil = None

        
        perfil = obtener_perfil(usuario_id)
        if perfil:
            
            actualizar_perfil(usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, experiencia, foto_perfil)
        else:
            
            crear_perfil(usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, experiencia, foto_perfil)

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

@app.route('/usuario')
def muestra_perfil():
    if 'correo' in session:
        usuario_id = obtener_usuario_id_por_correo(session['correo'])
        perfil = obtener_perfil(usuario_id)
        
        if perfil:
            return render_template('usuario.html', perfil=perfil)
        else:
            flash('No se ha encontrado un perfil para este usuario.')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    inicializar_bd()  
    app.run(debug=True)
