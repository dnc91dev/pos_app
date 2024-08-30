import mysql.connector
from mysql.connector import Error

class BaseDeDatos:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        try:
            # Conectar al servidor MySQL sin especificar base de datos
            self.connection = mysql.connector.connect(host=host, user=user, password=password)
            self.cursor = self.connection.cursor()
            if self.connection.is_connected():
                print("Conexión a MySQL establecida con éxito.")
                self._crear_base_de_datos_y_tablas()
            else:
                print("No se pudo establecer la conexión.")
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

    def _crear_base_de_datos_y_tablas(self):
        try:
            # Crear base de datos si no existe
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.cursor.execute(f"USE {self.database}")
            
            # Crear tabla Ventas si no existe
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ventas (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                ID_Producto INT NOT NULL,
                ID_Comprador INT NOT NULL,
                Precio DECIMAL(10, 2) NOT NULL,
                Fecha_Venta DATETIME NOT NULL,
                Metodo_Pago VARCHAR(50) NOT NULL,
                Estado_Venta VARCHAR(50) NOT NULL,
                Cantidad INT NOT NULL,
                Notas TEXT
            )
            """)
            print("Base de datos y tabla 'Ventas' preparadas.")
        except mysql.connector.Error as err:
            print(f"Error al crear la base de datos o tablas: {err}")
            raise
        finally:
            if self.connection:
                self.connection.commit()


    #remplazo de este bloque por uno mas completo que valida la existencia de base de datos al inicio del programa
    '''
    27/08 - 03:18:45
            try:
                self.connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
                if self.connection.is_connected():
                    self.cursor = self.connection.cursor()
                    print("Conexión a la base de datos establecida con éxito.")
                else:
                    print("No se pudo establecer la conexión.")
            except mysql.connector.Error as err:
                print(f"Error al conectar a la base de datos: {err}")
    '''



    def conectar(self):
        """Establece una conexión con la base de datos."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")

    def insertar_venta(self, id_producto, id_comprador, precio, fecha_venta, metodo_pago, estado_venta, cantidad, notas=None):
        """Inserta un nuevo registro en la tabla de ventas."""
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Ventas (ID_Producto, ID_Comprador, Precio, Fecha_Venta, Metodo_Pago, Estado_Venta, Cantidad, Notas)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (id_producto, id_comprador, precio, fecha_venta, metodo_pago, estado_venta, cantidad, notas)
            cursor.execute(query, values)
            self.connection.commit()
            print("Venta insertada exitosamente")
        except Error as e:
            print(f"Error al insertar venta: {e}")

    def consultar_ventas(self):
        """Consulta todas las ventas en la tabla."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Ventas"
            cursor.execute(query)
            ventas = cursor.fetchall()
            return ventas
        except Error as e:
            print(f"Error al consultar ventas: {e}")
            return []

    def modificar_venta(self, id_venta, **kwargs):
        """Modifica los detalles de una venta existente."""
        try:
            cursor = self.connection.cursor()
            set_clause = ", ".join([f"{col} = %s" for col in kwargs.keys()])
            test = f"\n\nthis is a test with: %s \n\n"
            print(test)
            query = f"UPDATE Ventas SET {set_clause} WHERE ID = %s"
            values = list(kwargs.values()) + [id_venta]
            print("para la linea : values = list(kwargs.values()) + [id_venta] se obtuvo lo siguiente:\n\n",values)
            cursor.execute(query, values)
            self.connection.commit()
            print("Venta modificada exitosamente")
        except Error as e:
            print(f"Error al modificar venta: {e}")

    def agregar_columna(self, nombre_columna, tipo_dato):
        """Agrega una nueva columna a la tabla de ventas."""
        try:
            cursor = self.connection.cursor()
            query = f"ALTER TABLE Ventas ADD COLUMN {nombre_columna} {tipo_dato}"
            cursor.execute(query)
            self.connection.commit()
            print(f"Columna {nombre_columna} añadida exitosamente")
        except Error as e:
            print(f"Error al agregar columna: {e}")


#    def agregar_columna(self, nombre_columna, tipo_dato):
#        try:
#            sql = f"ALTER TABLE Ventas ADD COLUMN {nombre_columna} {tipo_dato}"
#            self.cursor.execute(sql)
#            self.conn.commit()
#        except mysql.connector.Error as err:
#            raise Exception(f"Error al agregar columna: {err}")





# Uso del módulo
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener las variables de entorno
    HOST = os.getenv('DB_HOST')
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE = os.getenv('DB_DATABASE')

    db = BaseDeDatos(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    db.conectar()
    """
    # Insertar una venta
    db.insertar_venta(1, 2, 99.99, '2024-08-25 14:30:00', 'Tarjeta de crédito', 'Completada', 1, 'Compra realizada en línea')
    """
    # Consultar ventas
    ventas = db.consultar_ventas()
    for venta in ventas:
        print("la venta que existe es:\n\n",venta,"\n\n")


    # Modificar una venta
    '''
        db.modificar_venta(1, Estado_Venta='Pendiente', Notas='Cambio de estado a pendiente')
    '''
    # Agregar una columna adicional
    '''db.agregar_columna('Campo_Adicional4', 'VARCHAR(100)')'''
    
    db.desconectar()

