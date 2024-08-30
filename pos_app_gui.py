import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pos_app_db import BaseDeDatos# Suponiendo que el módulo se llama base_datos.py





class InterfazGrafica:
    def __init__(self, root, db):
        self.db = db
        # Configuración de la ventana principal
        root.title("Gestión de Ventas")
        root.geometry("600x400")
        # Tab Control
        self.tabControl = ttk.Notebook(root)
        self.tabInsertar = ttk.Frame(self.tabControl)
        self.tabConsultar = ttk.Frame(self.tabControl)
        self.tabModificar = ttk.Frame(self.tabControl)
        self.tabAgregarColumna = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tabInsertar, text='Insertar Venta')
        self.tabControl.add(self.tabConsultar, text='Consultar Ventas')
        self.tabControl.add(self.tabModificar, text='Modificar Venta')
        self.tabControl.add(self.tabAgregarColumna, text='Agregar Columna')
        self.tabControl.pack(expand=1, fill="both")
        # Insertar Venta
        self.crear_insertar_venta()
        # Consultar Ventas
        self.crear_consultar_ventas()
        # Modificar Venta
        self.crear_modificar_venta()
        # Agregar Columna
        self.crear_agregar_columna()

    def crear_insertar_venta(self):
        ttk.Label(self.tabInsertar, text="ID Producto:").grid(column=0, row=0, padx=10, pady=5)
        self.entry_id_producto = ttk.Entry(self.tabInsertar)
        self.entry_id_producto.grid(column=1, row=0, padx=10, pady=5)
        ttk.Label(self.tabInsertar, text="ID Comprador:").grid(column=0, row=1, padx=10, pady=5)
        self.entry_id_comprador = ttk.Entry(self.tabInsertar)
        self.entry_id_comprador.grid(column=1, row=1, padx=10, pady=5)
        ttk.Label(self.tabInsertar, text="Precio:").grid(column=0, row=2, padx=10, pady=5)
        self.entry_precio = ttk.Entry(self.tabInsertar)
        self.entry_precio.grid(column=1, row=2, padx=10, pady=5)
        ttk.Label(self.tabInsertar, text="Fecha Venta:").grid(column=0, row=3, padx=10, pady=5)
        self.entry_fecha_venta = ttk.Entry(self.tabInsertar)
        self.entry_fecha_venta.grid(column=1, row=3, padx=10, pady=5)
        ttk.Label(self.tabInsertar, text="Método de Pago:").grid(column=0, row=4, padx=10, pady=5)
        self.entry_metodo_pago = ttk.Entry(self.tabInsertar)
        self.entry_metodo_pago.grid(column=1, row=4, padx=10, pady=5)
        ttk.Label(self.tabInsertar, text="Estado Venta:").grid(column=0, row=5, padx=10, pady=5)
        self.entry_estado_venta = ttk.Entry(self.tabInsertar)
        self.entry_estado_venta.grid(column=1, row=5, padx=10, pady=5)
        ttk.Label(self.tabInsertar, text="Cantidad:").grid(column=0, row=6, padx=10, pady=5)
        self.entry_cantidad = ttk.Entry(self.tabInsertar)
        self.entry_cantidad.grid(column=1, row=6, padx=10, pady=5)
        ttk.Label(self.tabInsertar, text="Notas:").grid(column=0, row=7, padx=10, pady=5)
        self.entry_notas = ttk.Entry(self.tabInsertar)
        self.entry_notas.grid(column=1, row=7, padx=10, pady=5)
        self.btn_insertar = ttk.Button(self.tabInsertar, text="Insertar Venta", command=self.insertar_venta)
        self.btn_insertar.grid(column=1, row=8, padx=10, pady=10)

    def insertar_venta(self):
        try:
            id_producto = int(self.entry_id_producto.get())
            id_comprador = int(self.entry_id_comprador.get())
            precio = float(self.entry_precio.get())
            fecha_venta = datetime.strptime(self.entry_fecha_venta.get(), '%Y-%m-%d %H:%M:%S')
            metodo_pago = self.entry_metodo_pago.get()
            estado_venta = self.entry_estado_venta.get()
            cantidad = int(self.entry_cantidad.get())
            notas = self.entry_notas.get()
            self.db.insertar_venta(id_producto, id_comprador, precio, fecha_venta, metodo_pago, estado_venta, cantidad, notas)
            messagebox.showinfo("Éxito", "Venta insertada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo insertar la venta: {e}")

    def crear_consultar_ventas(self):
        self.btn_consultar = ttk.Button(self.tabConsultar, text="Consultar Ventas", command=self.consultar_ventas)
        self.btn_consultar.grid(column=0, row=0, padx=10, pady=10)
        self.tree = ttk.Treeview(self.tabConsultar, columns=("ID", "ID_Producto", "ID_Comprador", "Precio", "Fecha_Venta", "Metodo_Pago", "Estado_Venta", "Cantidad", "Total", "Notas"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def consultar_ventas(self):
        '''
        # Limpiar el Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Consultar ventas desde la base de datos
        ventas = self.db.consultar_ventas()
        print("Ventas recuperadas:", ventas)
        
        # Insertar los datos en el Treeview
        for venta in ventas:
            self.tree.insert("", "end", values=venta)
        '''
        for i in self.tree.get_children():
            self.tree.delete(i)
        ventas = self.db.consultar_ventas()
        for venta in ventas:
            self.tree.insert("", "end", values=tuple(venta.values()))
        #'''


    def crear_modificar_venta(self):
        ttk.Label(self.tabModificar, text="ID Venta a Modificar:").grid(column=0, row=0, padx=10, pady=5)
        self.entry_id_venta_modificar = ttk.Entry(self.tabModificar)
        self.entry_id_venta_modificar.grid(column=1, row=0, padx=10, pady=5)
        ttk.Label(self.tabModificar, text="Nuevo Estado Venta:").grid(column=0, row=1, padx=10, pady=5)
        self.entry_estado_venta_modificar = ttk.Entry(self.tabModificar)
        self.entry_estado_venta_modificar.grid(column=1, row=1, padx=10, pady=5)
        ttk.Label(self.tabModificar, text="Notas:").grid(column=0, row=2, padx=10, pady=5)
        self.entry_notas_modificar = ttk.Entry(self.tabModificar)
        self.entry_notas_modificar.grid(column=1, row=2, padx=10, pady=5)
        self.btn_modificar = ttk.Button(self.tabModificar, text="Modificar Venta", command=self.modificar_venta)
        self.btn_modificar.grid(column=1, row=3, padx=10, pady=10)

    def modificar_venta(self):
        try:
            id_venta = int(self.entry_id_venta_modificar.get())
            estado_venta = self.entry_estado_venta_modificar.get()
            notas = self.entry_notas_modificar.get()
            self.db.modificar_venta(id_venta, Estado_Venta=estado_venta, Notas=notas)
            messagebox.showinfo("Éxito", "Venta modificada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar la venta: {e}")

    def crear_agregar_columna(self):
        ttk.Label(self.tabAgregarColumna, text="Nombre de la Columna:").grid(column=0, row=0, padx=10, pady=5)
        self.entry_nombre_columna = ttk.Entry(self.tabAgregarColumna)
        self.entry_nombre_columna.grid(column=1, row=0, padx=10, pady=5)
        ttk.Label(self.tabAgregarColumna, text="Tipo de Dato:").grid(column=0, row=1, padx=10, pady=5)
        self.entry_tipo_dato = ttk.Entry(self.tabAgregarColumna)
        self.entry_tipo_dato.grid(column=1, row=1, padx=10, pady=5)
        self.btn_agregar_columna = ttk.Button(self.tabAgregarColumna, text="Agregar Columna", command=self.agregar_columna)
        self.btn_agregar_columna.grid(column=1, row=2, padx=10, pady=10)

    def agregar_columna(self):
        try:
            nombre_columna = self.entry_nombre_columna.get()
            tipo_dato = self.entry_tipo_dato.get()
            if tipo_dato.lower() == "int":
                tipo_dato = "INT"
            elif tipo_dato.lower() == "varchar":
                tipo_dato = "VARCHAR(255)"
            elif tipo_dato.lower() == "text":
                tipo_dato = "TEXT"
            elif tipo_dato.lower() == "decimal":
                tipo_dato = "DECIMAL(10, 2)"
            elif tipo_dato.lower() == "date":
                tipo_dato = "DATE"
            else:
                raise ValueError("Tipo de dato no soportado")
            self.db.agregar_columna(nombre_columna, tipo_dato)
            messagebox.showinfo("Éxito", f"Columna '{nombre_columna}' de tipo '{tipo_dato}' agregada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la columna: {e}")
