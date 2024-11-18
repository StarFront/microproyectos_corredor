




















@app.route('/visgeneral/<int:id_trabajo>')
def visgeneral(id_trabajo):
    # Conectar a la base de datos y obtener los detalles del trabajo
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='greenwork'
    )
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT titulo, descripcion, duracion, ubicacion, pago, monto, fotografia FROM trabajos WHERE id_trabajo = %s", (id_trabajo,))
    trabajo = cursor.fetchone()
    conexion.close()

    if trabajo:
        return render_template('visgeneral.html', trabajo=trabajo)
    else:
        flash('Trabajo no encontrado.')
        return redirect(url_for('marketplace'))
    
@app.route('/visgeneral/<int:id_trabajo>')
def visgeneral(id_trabajo):
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='greenwork'
    )
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trabajos WHERE id_trabajo = %s", (id_trabajo,))
    trabajo = cursor.fetchone()  # Solo obtenemos un trabajo, ya que el ID es único
    
    conexion.close()

    if trabajo:
        return render_template('visgeneral.html', trabajo=trabajo)
    else:
        return "Trabajo no encontrado", 404
