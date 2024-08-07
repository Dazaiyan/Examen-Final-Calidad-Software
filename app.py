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
        return redirect(url_for('empleados'))
    return redirect(url_for('login'))

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
            return redirect(url_for('empleados'))
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

# Gestión de Empleados
@app.route('/empleados')
def empleados():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        result_value = cur.execute("SELECT * FROM Empleados")
        if result_value > 0:
            empleados = cur.fetchall()
            return render_template('empleados.html', empleados=empleados)
        return render_template('empleados.html')
    return redirect(url_for('login'))

@app.route('/empleados/nuevo', methods=['GET', 'POST'])
def nuevo_empleado():
    if 'loggedin' in session:
        if request.method == 'POST':
            empleado_details = request.form
            nombre = empleado_details['nombre']
            puesto = empleado_details['puesto']
            salario = empleado_details['salario']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Empleados(nombre, puesto, salario) VALUES(%s, %s, %s)", (nombre, puesto, salario))
            mysql.connection.commit()
            cur.close()
            flash('Empleado Agregado Satisfactoriamente', 'success')
            return redirect(url_for('empleados'))
        return render_template('nuevo_empleado.html')
    return redirect(url_for('login'))

@app.route('/empleados/editar/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Empleados WHERE id = %s", [id])
        empleado = cur.fetchone()

        if request.method == 'POST':
            empleado_details = request.form
            nombre = empleado_details['nombre']
            puesto = empleado_details['puesto']
            salario = empleado_details['salario']

            cur.execute("""
                UPDATE Empleados
                SET nombre = %s, puesto = %s, salario = %s
                WHERE id = %s
            """, (nombre, puesto, salario, id))
            mysql.connection.commit()
            cur.close()
            flash('Empleado Actualizado Satisfactoriamente', 'success')
            return redirect(url_for('empleados'))

        return render_template('editar_empleado.html', empleado=empleado)
    return redirect(url_for('login'))

@app.route('/empleados/eliminar/<int:id>', methods=['POST'])
def eliminar_empleado(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Asignaciones WHERE empleado_id = %s", [id])
        asignacion = cur.fetchone()
        if asignacion:
            flash('No se puede eliminar el empleado porque tiene asignaciones.', 'danger')
        else:
            cur.execute("DELETE FROM Empleados WHERE id = %s", [id])
            mysql.connection.commit()
            flash('Empleado Eliminado Satisfactoriamente', 'success')
        cur.close()
        return redirect(url_for('empleados'))
    return redirect(url_for('login'))

# Gestión de Departamentos
@app.route('/departamentos')
def departamentos():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        result_value = cur.execute("SELECT * FROM Departamentos")
        if result_value > 0:
            departamentos = cur.fetchall()
            return render_template('departamentos.html', departamentos=departamentos)
        return render_template('departamentos.html')
    return redirect(url_for('login'))

@app.route('/departamentos/nuevo', methods=['GET', 'POST'])
def nuevo_departamento():
    if 'loggedin' in session:
        if request.method == 'POST':
            departamento_details = request.form
            nombre = departamento_details['nombre']
            ubicacion = departamento_details['ubicacion']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Departamentos(nombre, ubicacion) VALUES(%s, %s)", (nombre, ubicacion))
            mysql.connection.commit()
            cur.close()
            flash('Departamento Agregado Satisfactoriamente', 'success')
            return redirect(url_for('departamentos'))
        return render_template('nuevo_departamento.html')
    return redirect(url_for('login'))

@app.route('/departamentos/editar/<int:id>', methods=['GET', 'POST'])
def editar_departamento(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Departamentos WHERE id = %s", [id])
        departamento = cur.fetchone()

        if request.method == 'POST':
            departamento_details = request.form
            nombre = departamento_details['nombre']
            ubicacion = departamento_details['ubicacion']

            cur.execute("""
                UPDATE Departamentos
                SET nombre = %s, ubicacion = %s
                WHERE id = %s
            """, (nombre, ubicacion, id))
            mysql.connection.commit()
            cur.close()
            flash('Departamento Actualizado Satisfactoriamente', 'success')
            return redirect(url_for('departamentos'))

        return render_template('editar_departamento.html', departamento=departamento)
    return redirect(url_for('login'))

@app.route('/departamentos/eliminar/<int:id>', methods=['POST'])
def eliminar_departamento(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Asignaciones WHERE departamento_id = %s", [id])
        asignacion = cur.fetchone()
        if asignacion:
            flash('No se puede eliminar el departamento porque tiene asignaciones.', 'danger')
        else:
            cur.execute("DELETE FROM Departamentos WHERE id = %s", [id])
            mysql.connection.commit()
            flash('Departamento Eliminado Satisfactoriamente', 'success')
        cur.close()
        return redirect(url_for('departamentos'))
    return redirect(url_for('login'))

# Gestión de Asignaciones
@app.route('/asignaciones')
def asignaciones():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        result_value = cur.execute("SELECT * FROM Asignaciones")
        if result_value > 0:
            asignaciones = cur.fetchall()
            return render_template('asignaciones.html', asignaciones=asignaciones)
        return render_template('asignaciones.html')
    return redirect(url_for('login'))

@app.route('/asignaciones/nueva', methods=['GET', 'POST'])
def nueva_asignacion():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre FROM Empleados")
        empleados = cur.fetchall()
        cur.execute("SELECT id, nombre FROM Departamentos")
        departamentos = cur.fetchall()

        if request.method == 'POST':
            asignacion_details = request.form
            empleado_id = asignacion_details['empleado_id']
            departamento_id = asignacion_details['departamento_id']
            fecha_asignacion = asignacion_details['fecha_asignacion']

            cur.execute("INSERT INTO Asignaciones(empleado_id, departamento_id, fecha_asignacion) VALUES(%s, %s, %s)", 
                        (empleado_id, departamento_id, fecha_asignacion))
            mysql.connection.commit()
            cur.close()
            flash('Asignación Agregada Satisfactoriamente', 'success')
            return redirect(url_for('asignaciones'))

        return render_template('nueva_asignacion.html', empleados=empleados, departamentos=departamentos)
    return redirect(url_for('login'))

@app.route('/asignaciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_asignacion(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Asignaciones WHERE id = %s", [id])
        asignacion = cur.fetchone()

        cur.execute("SELECT id, nombre FROM Empleados")
        empleados = cur.fetchall()

        cur.execute("SELECT id, nombre FROM Departamentos")
        departamentos = cur.fetchall()

        if request.method == 'POST':
            asignacion_details = request.form
            empleado_id = asignacion_details['empleado_id']
            departamento_id = asignacion_details['departamento_id']
            fecha_asignacion = asignacion_details['fecha_asignacion']

            cur.execute("""
                UPDATE Asignaciones
                SET empleado_id = %s, departamento_id = %s, fecha_asignacion = %s
                WHERE id = %s
            """, (empleado_id, departamento_id, fecha_asignacion, id))
            mysql.connection.commit()
            cur.close()
            flash('Asignación Actualizada Satisfactoriamente', 'success')
            return redirect(url_for('asignaciones'))

        return render_template('editar_asignacion.html', asignacion=asignacion, empleados=empleados, departamentos=departamentos)
    return redirect(url_for('login'))

@app.route('/asignaciones/eliminar/<int:id>', methods=['POST'])
def eliminar_asignacion(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Asignaciones WHERE id = %s", [id])
        mysql.connection.commit()
        cur.close()
        flash('Asignación Eliminada Satisfactoriamente', 'success')
        return redirect(url_for('asignaciones'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
