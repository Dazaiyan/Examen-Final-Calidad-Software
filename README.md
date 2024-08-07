# Sistema de Gestión de Proyectos

Este es un sistema web para la gestión de proyectos, incluyendo funcionalidades de registro y login de usuarios, un dashboard personalizado para visualizar el estado de los proyectos, creación, edición y eliminación de proyectos, asignación de tareas y responsables, y generación de reportes de progreso.

## Requisitos

- Python 3.7+
- MySQL
- Virtualenv (recomendado)

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   cd TU_REPOSITORIO

## Crear un entorno virtual:

   ```bash
   python -m venv venv
```

## Activa el entorno 
```
venv\Scripts\activate
```

## Instalar las dependencias:
```
pip install -r requirements.txt
```

## Configurar las variables de entorno:

- SECRET_KEY=tu_clave_secreta
- MYSQL_HOST=tu_host_mysql
- MYSQL_USER=tu_usuario_mysql
- MYSQL_PASSWORD=tu_contraseña_mysql
- MYSQL_DB=tu_base_de_datos

## Inicializar la base de datos:

```
CREATE DATABASE tu_base_de_datos;
USE tu_base_de_datos;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR(20)
);

CREATE TABLE Tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    responsable VARCHAR(100),
    fecha_limite DATE,
    estado VARCHAR(20),
    proyecto_id INT,
    FOREIGN KEY (proyecto_id) REFERENCES Proyectos(id)
);
```

# Uso

## Ejecutar la aplicación:

```
python app.py
```

## Abrir el navegador web y acceder a la aplicación:

```
http://127.0.0.1:5000/
```


# Estructura del Proyecto
- app.py: Archivo principal de la aplicación Flask.
- templates/: Carpeta que contiene las plantillas HTML.
- static/: Carpeta que contiene los archivos estáticos (CSS, JS, imágenes).
- requirements.txt: Archivo que contiene las dependencias del proyecto.
- .env: Archivo que contiene las variables de entorno (no incluido en el repositorio).
