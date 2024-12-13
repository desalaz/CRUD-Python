from pymongo import MongoClient
from decouple import config

# Conexión a MongoDB Atlas
client = MongoClient(config("MONGODB_URI"))
db = client["tienda"]
collection = db["productos"]

# Conexión a MongoDB Atlas
# client = MongoClient("mongodb+srv://desisalazarm:passwordDesi2786@cluster0.4a7et.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = client["tienda"]
# collection = db["productos"]
# Probar conexión leyendo documentos
print("Conexión exitosa.")
for producto in collection.find():
    print(producto)
