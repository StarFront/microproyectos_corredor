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

@app.route('/actualizar_perfil', methods=['POST'])
def actualizar_perfil_view():
    if 'correo' in session:
        usuario_id = obtener_usuario_id_por_correo(session['correo'])
        
        # Obtener los datos del formulario
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['cedula']
        telefono = request.form['telefono']
        fecha_nacimiento = request.form['nacimiento']
        foto_perfil = request.files['foto-perfil']  # Manejo de la foto (por ejemplo, guardarla en el servidor)

        # Guardar la foto si es que el usuario la sube
        if foto_perfil:
            foto_perfil_filename = f"foto_{usuario_id}.jpg"
            foto_perfil.save(f'../static/img/{foto_perfil_filename}')
            foto_perfil = foto_perfil_filename
        else:
            foto_perfil = None
        
        actualizar_perfil(usuario_id, nombres, apellidos, cedula, telefono, fecha_nacimiento, foto_perfil)
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
            cursor = conexion.cursor()
            consulta = "SELECT id FROM usuarios WHERE correo = %s"
            cursor.execute(consulta, (correo,))
            usuario = cursor.fetchone()
            return usuario[0] if usuario else None
    except Error as e:
        print("Error al obtener el ID del usuario:", e)
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
