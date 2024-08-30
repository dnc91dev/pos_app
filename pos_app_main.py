import tkinter as tk
from pos_app_db import BaseDeDatos
from pos_app_gui import InterfazGrafica  # Asegúrate de que el archivo se llama interfaz_grafica.py


import os
from dotenv import load_dotenv
# Cargar las variables de entorno desde el archivo .env
load_dotenv()


# Obtener las variables de entorno
HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_DATABASE')


def main():
    # Configuración de la base de datos
    db = BaseDeDatos(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    
    # Configuración de la ventana principal
    root = tk.Tk()
    app = InterfazGrafica(root, db)
    
    # Ejecutar la interfaz gráfica
    root.mainloop()

if __name__ == "__main__":
    main()

