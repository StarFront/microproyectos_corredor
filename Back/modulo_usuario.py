<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Postulaciones</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/postulaciones.css') }}">
</head>
<body>
    <header>
        <h1>Mis Postulaciones</h1>
    </header>
    <div class="columns">
        <div class="column">
            <h2>Pendientes</h2>
            {% for p in pendientes %}
            <div class="job-card">
                <img src="{{ url_for('static', filename='img/trabajos/' + p['fotografia']) }}" alt="Trabajo">
                <h3>{{ p['titulo'] }}</h3>
                <p>{{ p['descripcion'] }}</p>
            </div>
            {% endfor %}
        </div>
        <div class="column">
            <h2>Aceptados</h2>
            {% for p in aceptados %}
            <div class="job-card">
                <img src="{{ url_for('static', filename='img/trabajos/' + p['fotografia']) }}" alt="Trabajo">
                <h3>{{ p['titulo'] }}</h3>
                <p>{{ p['descripcion'] }}</p>
            </div>
            {% endfor %}
        </div>
        <div class="column">
            <h2>Rechazados</h2>
            {% for p in rechazados %}
            <div class="job-card">
                <img src="{{ url_for('static', filename='img/trabajos/' + p['fotografia']) }}" alt="Trabajo">
                <h3>{{ p['titulo'] }}</h3>
                <p>{{ p['descripcion'] }}</p>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>





















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
