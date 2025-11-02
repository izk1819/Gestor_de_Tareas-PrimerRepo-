import mysql.connector
import os

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

# Se define una funcion exclusiva para buscar en la base de datos:
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
