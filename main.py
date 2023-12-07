from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import sqlite3

conn = sqlite3.connect("sql/jojos.db")

app = FastAPI()

@app.get("/")
async def inicio():
    return {"Developed by": "Patricio Vargas f:"}

@app.get("/partes/{nombre_parte}")
async def partes(nombre_parte: str):
    c = conn.cursor()
    c.execute("SELECT * FROM partesJojos WHERE nombre_parte = ?", (nombre_parte,))
    parte = None
    for row in c:
        parte = {"Nombre": row[1], "Descripción": row[2], "Imagenes": row[3]}
    return parte

@app.get("/personaje/{nombre_personaje}")
async def personaje(nombre_personaje: str):
    c = conn.cursor()
    c.execute("SELECT j.nombre_parte, p.* FROM personajes p INNER JOIN partesJojos j on p.categoria_personaje = j.id_parte WHERE p.nombre = ?", (nombre_personaje, ))
    personaje = None
    for fila in c:
        print(fila)
        personaje = {"Primera aparición": fila[0], "Nombre": fila[3], "Stand": fila[4], "Referencia": fila[5], "Fecha de nacimiento": fila[6], "Fecha de muerte": fila[7], "Género": fila[8], "Altura": fila[9], "Peso": fila[10], "Nacionalidad": fila[11], "Descripcion": fila[12], "Imagen": fila[13]}
    return personaje

@app.get("/partesJojos")
async def obtener_partes_jojos():
    c = conn.cursor()
    c.execute("SELECT * FROM partesJojos")
    response = []
    for fila in c:
        parte = {"Nombre": fila[1], "Descripcion": fila[2], "imagenes": fila[3]}
        response.append(parte)
    if not response:
        return []
    return response

@app.get("/personajeJojos")
async def obtener_personajes_jojos():
    c = conn.cursor()
    c.execute("SELECT * FROM personajes")
    response = []
    for fila in c:
        personaje = {"Primera aparición": fila[1], "Nombre": fila[2], "Stand": fila[3], "Referencia": fila[4], "Fecha de nacimiento": fila[5], "Fecha de muerte": fila[6], "Género": fila[7], "Altura": fila[8], "Peso": fila[9], "Nacionalidad": fila[10], "Descripcion": fila[11], "Imagen": fila[12]}
        response.append(personaje)
    if not response:
        return []
    return response

@app.post("/subirParte/")
async def agregar_parte_jojos(nombre: str, descripcion: str, imagen_url: str):

    c = conn.cursor()
    c.execute("INSERT INTO partesJojos(nombre_parte, descripcion_parte, imagen_parte) VALUES (?, ?, ?)",
              (nombre, descripcion, imagen_url))
    conn.commit()
    return {"message": "Parte de Jojos agregada con éxito"}

@app.post("/subirPersonaje")
async def agregar_personaje_jojos(categoria_personaje: int, nombre: str, stand_habilidad: str, referencia_stand: str,
                                fecha_nacimiento: str, fecha_muerte: str | None, genero: str, altura: str, peso: str, nacionalidadL: str,
                                descripcion: str, imagen_url:str):

    c = conn.cursor()
    c.execute("""INSERT INTO personajes(categoria_personaje, nombre, stand_habilidad, referencia_stand,
              fecha_nacimiento, fecha_muerte, genero, altura, peso, nacionalidad, descripcion, imagen_personaje) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (categoria_personaje, nombre, stand_habilidad, referencia_stand, fecha_nacimiento, fecha_muerte, genero, altura, peso, nacionalidadL,
              descripcion, imagen_url))
    conn.commit()
    return {"message": "Personaje agregado con éxito"}

