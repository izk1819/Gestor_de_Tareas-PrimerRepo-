# Se importan los módulos necesarios:
from utils.mysql import query, sql_search, secure_query
from utils.communications import send_email

import os
from dotenv import load_dotenv
from datetime import timedelta

from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user



# Se define la clase usuario:
class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

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

# Se inicia Flask
app = Flask(__name__)

# Se inicia "login manager":
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.secret_key = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(minutes = 30)

@login_manager.user_loader
def load(user_id):
    
    sql = "select * from users where id = %s"
    values = (user_id,)
    data_row = sql_search(sql, values)
    return User(id = user_id, name = data_row[1], email = data_row[2], password = data_row[3])

# Se comienza a definir páginas:
@app.route("/")
def task_manager():
    return render_template("task_manager.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    # Se define un mensaje sin valor porque después se usará esta variable:
    message = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        sql = "select * from users where email = %s and password = %s"
        values = (email, password)
        user_data = sql_search(sql, values)

        # Si se encuentra una coincidencia, se inicia sesión:
        if user_data != None:
            user = User(id=user_data[0], name=user_data[1], email=user_data[2], password=user_data[3])
            login_user(user)

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
            real_email = send_email(email,
                       "Registro completado!",
                       f"""Bienvenid@ a Task Manager {name}, te invitamos a usar nuestra página para ayudarte en tu día a día.""")
            if real_email == True:
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

# Se puede acceder a la página "home" solo si el usuario ha iniciado sesión:
@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/new_task")
@login_required
def new_task():
    return render_template("task_templates/new_task.html")

@app.route("/task_list")
@login_required
def task_list():
    return render_template("task_templates/task_list.html")

# Si se cierra sesión, redirecciona a la página "login":
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)