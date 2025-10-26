# Se importan los módulos necesarios:
import mysql.connector
import os
from flask import Flask, render_template, request
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



# Cargar datos para MySQL:
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
    return render_template("users/login.html")

@app.route("/sign_up", methods = ["GET","POST"])
def sign_up():

    if request.method == "POST":
        ####################################
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        #ENVIAR A LA BASE DE DATOS
        #####################################

    return render_template("users/sign_up.html")

# Iniciar Flask
if __name__ == '__main__':
    app.run(debug=True)