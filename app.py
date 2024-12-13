from pymongo import MongoClient
from decouple import config
import tkinter as tk
from tkinter import ttk, messagebox
from bson.objectid import ObjectId

# Conexión a MongoDB Atlas
client = MongoClient(config("MONGODB_URI"))
db = client["tienda"]
collection = db["productos"]


print("Conexión exitosa.")
# for producto in collection.find():
#     print(producto)

# Funciones CRUD
def crear_producto():
    # Obtener valores de los campos
    name = entry_name.get().strip()
    precio = entry_precio.get().strip()
    categoria = entry_categoria.get().strip()

    if not name or not precio or not categoria:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    try:
        # Convertir precio a número (float)
        precio = float(precio)

        # Crear el diccionario del producto
        producto = {"name": name, "precio": precio, "categoria": categoria}

        # Insertar en la base de datos
        collection.insert_one(producto)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "Producto agregado correctamente.")

        # Limpiar los campos de entrada
        entry_name.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)

        # Actualizar la vista del Treeview
        mostrar_productos()
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número válido.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")


#Funcion de mostrar Productos

def mostrar_productos():
    for row in tree.get_children():
        tree.delete(row)
    
    productos = collection.find()
    for producto in productos:
        tree.insert("", "end", values=(producto["_id"], producto["name"], producto["precio"], producto["categoria"]))


#Funcion para actualizar productos
def actualizar_producto():
    # Obtener el producto seleccionado
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Selecciona un producto para actualizar.")
        return
    
    # Obtener el _id del producto desde el Treeview
    item_id = tree.item(selected_item[0])["values"][0]
    
    # Obtener los valores de los campos de entrada
    name = entry_name.get().strip()
    precio = entry_precio.get().strip()
    categoria = entry_categoria.get().strip()
    
    if not name or not precio or not categoria:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    
    try:
        # Convertir el precio a número (float)
        precio = float(precio)

        # Actualizar el producto en la base de datos
        collection.update_one(
            {"_id": ObjectId(item_id)},  # Convertir item_id a ObjectId
            {"$set": {"name": name, "precio": precio, "categoria": categoria}}
        )
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", f"Producto '{name}' actualizado.")
        
        # Actualizar la vista del Treeview
        mostrar_productos()

        # Limpiar los campos de entrada
        entry_name.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número válido.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al actualizar el producto: {str(e)}")







# Funcion para  eliminar productos:


def eliminar_producto():
    # Obtener el elemento seleccionado
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Selecciona un producto para eliminar.")
        return

    # Obtener el ID del producto desde el Treeview
    item_id = tree.item(selected_item[0])["values"][0]
    
    try:
        # Convertir el ID a ObjectId y eliminarlo de la base de datos
        collection.delete_one({"_id": ObjectId(item_id)})
        messagebox.showinfo("Éxito", "Producto eliminado.")

         # Limpiar los campos de entrada
        entry_name.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)
        
        # Actualizar la vista de los productos
        mostrar_productos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el producto: {str(e)}")

# Todo lo realcionado a la Interfaz Gráfica
root = tk.Tk()
root.title("Gestión de Productos - Tienda")
root.geometry("800x500")
root.configure(bg="#f0f0f0")

# Campos de entrada
frame_form = tk.Frame(root)
frame_form.pack(pady=10,padx=5)

tk.Label(frame_form, text="Nombre", font=("Helvetica", 16), bg="#f0f0f0", fg="#333333").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_form)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Precio", font=("Helvetica", 16), bg="#f0f0f0", fg="#333333").grid(row=1, column=0, padx=5, pady=5)
entry_precio = tk.Entry(frame_form)
entry_precio.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Categoría", font=("Helvetica", 16), bg="#f0f0f0", fg="#333333").grid(row=2, column=0, padx=5, pady=5)
entry_categoria = tk.Entry(frame_form)
entry_categoria.grid(row=2, column=1, padx=5, pady=5)

# Botones
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_create = tk.Button(frame_buttons, text="Crear Producto", bg="#4caf50", fg="white", font=("Arial", 12), relief="raised", command=crear_producto)
btn_create.grid(row=0, column=0, padx=10)

btn_update = tk.Button(frame_buttons, text="Actualizar Producto", bg="#4caf50", fg="white", font=("Arial", 12), relief="raised", command=actualizar_producto)
btn_update.grid(row=0, column=1, padx=10)

btn_delete = tk.Button(frame_buttons, text="Eliminar Producto", bg="#4caf50", fg="white", font=("Arial", 12), relief="raised", command=eliminar_producto)
btn_delete.grid(row=0, column=2, padx=10)

btn_read = tk.Button(frame_buttons, text="Mostrar Productos", bg="#4caf50", fg="white", font=("Arial", 12), relief="raised", command=mostrar_productos)
btn_read.grid(row=0, column=3, padx=10)

# Tabla para mostrar los productos
frame_table = tk.Frame(root)
frame_table.pack(pady=10)

columns = ("_id", "name", "precio", "categoria")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
tree.heading("_id", text="ID")
tree.heading("name", text="Nombre")
tree.heading("precio", text="Precio")
tree.heading("categoria", text="Categoría")

tree.column("_id", width=200)
tree.column("name", width=150)
tree.column("precio", width=100)
tree.column("categoria", width=150)

tree.pack(fill="both", expand=True)

# Cargar productos al inicio
mostrar_productos()

# Ejecutar la aplicación
root.mainloop()
