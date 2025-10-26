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

# Si no exixte, crear la base de datos:
query(["create database if not exists task_manager"])