# Se importan los módulos necesarios:
import mysql.connector
import os
from flask import Flask, render_template, request, url_for, redirect
from dotenv import load_dotenv



# Se define una función para enviar consultas a mysql, la variable task debe ser una lista con strings 
# que sirvan de consultas:
def query(task_list):
    connection = mysql.connector.connect(
        host = "localhost",
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
    )
    cursor = connection.cursor()

    for task in task_list:
        cursor.execute(task)
    
    connection.commit()
    cursor.close()
    connection.close()

# Se define una funcion exclusiva para insertar datos a sql de forma segura:
def secure_query(sql, values):
    connection = mysql.connector.connect(
        host = "localhost",
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        database = "task_manager",
    )
    cursor = connection.cursor()

    cursor.execute(sql, values)
    
    connection.commit()
    cursor.close()
    connection.close()

def sql_search(sql, values):
    connection = mysql.connector.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database="task_manager"
    )
    cursor = connection.cursor()

    cursor.execute(sql, values)

    # Result será None si no hay coincidencias
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result





# Cargar datos iniciales a MySQL:
load_dotenv()

# Si no exixte, crear la base de datos junto con la tabla de usuarios:
query(["create database if not exists task_manager",
       "use task_manager",
       """create table if not exists users (
       id int auto_increment primary key,
       name varchar(50) not null,
       email varchar(50) not null unique,
       password varchar(50) not null,
       created_at timestamp default current_timestamp
       )"""])



app = Flask(__name__)
# Definir páginas:
@app.route("/")
def task_manager():
    return render_template("task_manager.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    message = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        sql = "select * from users where email = %s and password = %s"
        values = (email, password)
        
        if sql_search(sql, values) != None:
            return redirect (url_for("home"))
        else:
            message = "Correo y/o contraseña incorrecta(s)."

    return render_template("sign_templates/login.html", message=message)

@app.route("/sign_up", methods = ["GET","POST"])
def sign_up():

    # Se define un mensaje sin valor porque después se usará esta variable:
    message = None

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Se define una variable que sirva para verificar si los datos se pudieron registrar correctamente:
        sign_up_verification = False
        try:
            sql = "insert into users (name, email, password) values(%s, %s, %s)"
            values = (name, email, password)
            secure_query(sql, values)

            sign_up_verification = True

        except:
            sign_up_verification = False
        
        finally:
            if sign_up_verification == True:
                message = "Te has registrado correctamente."
            else:
                message = "No te has podido registrar correctamente, inténtalo de nuevo."

    return render_template("sign_templates/sign_up.html", message=message)

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)