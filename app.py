from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from os import getenv
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()  # Cargar variables del archivo .env

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')

# Configuración de MySQL
app.config['MYSQL_HOST'] = getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = getenv('MYSQL_DB')

mysql = MySQL(app)

# Ruta de inicio
@app.route('/')
def index():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Proyectos")
        proyectos = cur.fetchall()
        cur.close()
        return render_template('index.html', proyectos=proyectos)
    return render_template('index.html')

# Registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        hashed_password = generate_password_hash(password)
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users(username, password) VALUES(%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Inicio de sesión de usuarios
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user[2], password):
            session['loggedin'] = True
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login'))

#Dashboard
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Proyectos")
        proyectos = cur.fetchall()
        
        proyectos_activos = len([proyecto for proyecto in proyectos if proyecto[5] == 'activo'])
        proyectos_inactivos = len([proyecto for proyecto in proyectos if proyecto[5] == 'inactivo'])
        
        cur.close()
        return render_template('dashboard.html', proyectos=proyectos, proyectos_activos=proyectos_activos, proyectos_inactivos=proyectos_inactivos)
    return redirect(url_for('login'))

# Gestión de Proyectos
@app.route('/proyectos')
def proyectos():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Proyectos")
        proyectos = cur.fetchall()
        cur.close()
        return render_template('proyectos.html', proyectos=proyectos)
    return redirect(url_for('login'))

@app.route('/proyectos/nuevo', methods=['GET', 'POST'])
def nuevo_proyecto():
    if 'loggedin' in session:
        if request.method == 'POST':
            proyecto_details = request.form
            nombre = proyecto_details['nombre']
            descripcion = proyecto_details['descripcion']
            fecha_inicio = proyecto_details['fecha_inicio']
            fecha_fin = proyecto_details['fecha_fin']
            estado = proyecto_details['estado']  # Asegurarse de que el estado se obtenga correctamente

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Proyectos(nombre, descripcion, fecha_inicio, fecha_fin, estado) VALUES(%s, %s, %s, %s, %s)", (nombre, descripcion, fecha_inicio, fecha_fin, estado))
            mysql.connection.commit()
            cur.close()
            flash('Proyecto Agregado Satisfactoriamente', 'success')
            return redirect(url_for('proyectos'))
        return render_template('nuevo_proyecto.html')
    return redirect(url_for('login'))

@app.route('/proyectos/editar/<int:id>', methods=['GET', 'POST'])
def editar_proyecto(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Proyectos WHERE id = %s", [id])
        proyecto = cur.fetchone()

        if request.method == 'POST':
            proyecto_details = request.form
            nombre = proyecto_details['nombre']
            descripcion = proyecto_details['descripcion']
            fecha_inicio = proyecto_details['fecha_inicio']
            fecha_fin = proyecto_details['fecha_fin']
            estado = proyecto_details['estado']

            cur.execute("""
                UPDATE Proyectos
                SET nombre = %s, descripcion = %s, fecha_inicio = %s, fecha_fin = %s, estado = %s
                WHERE id = %s
            """, (nombre, descripcion, fecha_inicio, fecha_fin, estado, id))
            mysql.connection.commit()
            cur.close()
            flash('Proyecto Actualizado Satisfactoriamente', 'success')
            return redirect(url_for('proyectos'))

        return render_template('editar_proyecto.html', proyecto=proyecto)
    return redirect(url_for('login'))

@app.route('/proyectos/eliminar/<int:id>', methods=['POST'])
def eliminar_proyecto(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Proyectos WHERE id = %s", [id])
        mysql.connection.commit()
        cur.close()
        flash('Proyecto Eliminado Satisfactoriamente', 'success')
        return redirect(url_for('proyectos'))
    return redirect(url_for('login'))

# Gestión de Tareas
@app.route('/tareas/<int:proyecto_id>')
def tareas(proyecto_id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Tareas WHERE proyecto_id = %s", [proyecto_id])
        tareas = cur.fetchall()
        cur.close()
        return render_template('tareas.html', tareas=tareas, proyecto_id=proyecto_id)
    return redirect(url_for('login'))

@app.route('/tareas_general')
def tareas_general():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Proyectos")
        proyectos = cur.fetchall()
        cur.close()
        return render_template('tareas_general.html', proyectos=proyectos)
    return redirect(url_for('login'))

@app.route('/tareas/nueva/<int:proyecto_id>', methods=['GET', 'POST'])
def nueva_tarea(proyecto_id):
    if 'loggedin' in session:
        if request.method == 'POST':
            tarea_details = request.form
            nombre = tarea_details['nombre']
            descripcion = tarea_details['descripcion']
            responsable = tarea_details['responsable']
            fecha_limite = tarea_details['fecha_limite']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Tareas(nombre, descripcion, responsable, fecha_limite, proyecto_id) VALUES(%s, %s, %s, %s, %s)", (nombre, descripcion, responsable, fecha_limite, proyecto_id))
            mysql.connection.commit()
            cur.close()
            flash('Tarea Agregada Satisfactoriamente', 'success')
            return redirect(url_for('tareas', proyecto_id=proyecto_id))
        return render_template('nueva_tarea.html', proyecto_id=proyecto_id)
    return redirect(url_for('login'))

@app.route('/tareas/editar/<int:id>', methods=['GET', 'POST'])
def editar_tarea(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Tareas WHERE id = %s", [id])
        tarea = cur.fetchone()

        if request.method == 'POST':
            tarea_details = request.form
            nombre = tarea_details['nombre']
            descripcion = tarea_details['descripcion']
            responsable = tarea_details['responsable']
            fecha_limite = tarea_details['fecha_limite']

            cur.execute("""
                UPDATE Tareas
                SET nombre = %s, descripcion = %s, responsable = %s, fecha_limite = %s
                WHERE id = %s
            """, (nombre, descripcion, responsable, fecha_limite, id))
            mysql.connection.commit()
            cur.close()
            flash('Tarea Actualizada Satisfactoriamente', 'success')
            return redirect(url_for('tareas', proyecto_id=tarea[5]))

        return render_template('editar_tarea.html', tarea=tarea)
    return redirect(url_for('login'))

@app.route('/tareas/eliminar/<int:id>', methods=['POST'])
def eliminar_tarea(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT proyecto_id FROM Tareas WHERE id = %s", [id])
        proyecto_id = cur.fetchone()[0]
        cur.execute("DELETE FROM Tareas WHERE id = %s", [id])
        mysql.connection.commit()
        cur.close()
        flash('Tarea Eliminada Satisfactoriamente', 'success')
        return redirect(url_for('tareas', proyecto_id=proyecto_id))
    return redirect(url_for('login'))

# Reportes
@app.route('/reportes')
def reportes():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Proyectos")
        proyectos = cur.fetchall()
        
        cur.execute("SELECT * FROM Tareas")
        tareas = cur.fetchall()

        # Calculamos el progreso de cada proyecto
        proyectos_con_progreso = []
        for proyecto in proyectos:
            proyecto_id = proyecto[0]
            tareas_del_proyecto = [tarea for tarea in tareas if tarea[5] == proyecto_id]
            total_tareas = len(tareas_del_proyecto)
            tareas_completadas = len([tarea for tarea in tareas_del_proyecto if tarea[6] == 'completada'])
            progreso = (tareas_completadas / total_tareas) * 100 if total_tareas > 0 else 0
            proyectos_con_progreso.append(proyecto + (progreso,))
        
        cur.close()
        return render_template('reportes.html', proyectos=proyectos_con_progreso, tareas=tareas)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
