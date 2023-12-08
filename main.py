from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import sqlite3

conn = sqlite3.connect("sql/jojos.db")

app = FastAPI()

# Endpoint Raíz
@app.get("/")
async def inicio():
    return {"Developed by": "Patricio Vargas f:"}

# Endpoint para ver una parte en especifico
@app.get("/partes/{nombre_parte}")
async def partes(nombre_parte: str):
    c = conn.cursor()
    c.execute("SELECT * FROM partesJojos WHERE nombre_parte = ?", (nombre_parte,))
    parte = None
    for row in c:
        parte = {"Identificador": row[0], "Nombre": row[1], "Descripcion": row[2], "Imagenes": row[3]}
    return parte

# Endpoint para ver los personajes por partes
@app.get("/ver_personajes_partes/{parte_nombre}")
async def personajes_partes(parte_nombre: str):
    c = conn.cursor()
    c.execute("SELECT j.nombre_parte, p.* FROM personajes p INNER JOIN partesJojos j on p.categoria_personaje = j.id_parte WHERE j.nombre_parte = ?", (parte_nombre,) )
    response = []
    for fila in c:
        print(fila)
        parte = {"Identificador": fila[1], "Primera Aparición": fila[0], "Nombre": fila[3], "Stand": fila[4], "Referencia": fila[5], "Fecha de Nacimiento": fila[6], "Nacionalidad": fila[7], "Imagen": fila[8]}
        response.append(parte)
    if not response:
        return []
    return response

# Endpoint para ver un personaje en específico
@app.get("/personaje/{nombre_personaje}")
async def personaje(nombre_personaje: str):
    c = conn.cursor()
    c.execute("SELECT j.nombre_parte, p.* FROM personajes p INNER JOIN partesJojos j on p.categoria_personaje = j.id_parte WHERE p.nombre = ?", (nombre_personaje, ))
    personaje = None
    for fila in c:
        print(fila)
        personaje = {"Identificador": fila[1], "Primera Aparición": fila[0], "Nombre": fila[3], "Stand": fila[4], "Referencia": fila[5], "Fecha de Nacimiento": fila[6], "Nacionalidad": fila[7], "Imagen": fila[8]}
    return personaje

# Endpoint para ver todas las partes
@app.get("/partesJojos")
async def obtener_partes_jojos():
    c = conn.cursor()
    c.execute("SELECT * FROM partesJojos")
    response = []
    for fila in c:
        parte = {"Identificador": fila[0], "Nombre": fila[1], "Descripcion": fila[2], "imagenes": fila[3]}
        response.append(parte)
    if not response:
        return []
    return response

# Endpoint para ver todos los personajes
@app.get("/personajeJojos")
async def obtener_personajes_jojos():
    c = conn.cursor()
    c.execute("SELECT j.nombre_parte, p.* FROM personajes p INNER JOIN partesJojos j on p.categoria_personaje = j.id_parte")
    response = []
    for fila in c:
        print(fila)
        personaje = {"Identificador": fila[1], "Primera Aparición": fila[0], "Nombre": fila[3], "Stand": fila[4], "Referencia": fila[5], "Fecha de Nacimiento": fila[6], "Nacionalidad": fila[7], "Imagen": fila[8]}
        response.append(personaje)
    if not response:
        return []
    return response

# Endpoint para subir una nueva Parte
@app.post("/subirParte/")
async def agregar_parte_jojos(nombre: str, descripcion: str, imagen_url: str):

    c = conn.cursor()
    c.execute("INSERT INTO partesJojos(nombre_parte, descripcion_parte, imagen_parte) VALUES (?, ?, ?)",
              (nombre, descripcion, imagen_url))
    conn.commit()
    return {"message": "Parte de Jojos agregada con éxito"}

# Endpoint para subir un Personaje
@app.post("/subirPersonaje")
async def agregar_personaje_jojos(categoria_personaje: int, nombre: str, stand_habilidad: str, referencia_stand: str,
                                fecha_nacimiento: str, nacionalidad: str, imagen_url:str):

    c = conn.cursor()
    c.execute("""INSERT INTO personajes(categoria_personaje, nombre, stand_habilidad, referencia_stand,
              fecha_nacimiento, nacionalidad, descripcion, imagen_personaje) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (categoria_personaje, nombre, stand_habilidad, referencia_stand, fecha_nacimiento, nacionalidad, imagen_url))
    conn.commit()
    return {"message": "Personaje agregado con éxito"}

