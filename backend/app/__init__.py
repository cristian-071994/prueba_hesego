#importacion de herramientas necesarias para la app
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
import pymysql
""" import os """

# Importar las variables de conexión desde un archivo de configuración
from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB, JWT_SECRET_KEY

#inicializacion de la aplicacion flask
app = Flask(__name__, static_folder='../../frontend/static', template_folder='../../frontend/templates')
#configuracion de SQLAlchemy para el manejo de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

#prueba de conexion a MYSQl
def test_mysql_connection():
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DB
        )
        print("Conexión a MySQL exitosa")
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error al conectar a MySQL: {e}")

test_mysql_connection()  # Validar la conexión a MySQL

#importacion y registro de recursos
from app.resources import TaskListResource, TaskResource, UserRegistration, UserLogin

#rutas a utilizar
api.add_resource(TaskListResource, '/api/tasks')
api.add_resource(TaskResource, '/api/tasks/<int:id>')
api.add_resource(UserRegistration, '/api/register')
api.add_resource(UserLogin, '/api/login')

#aplicacion de rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/tasks.html')
def tasks():
    return render_template('tasks.html')

#comprueba si el archivo se esta ejecutando directamente
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear todas las tablas
    app.run(debug=True)
