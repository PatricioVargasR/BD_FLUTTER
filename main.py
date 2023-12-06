from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import os
import sqlite3

conn = sqlite3.connect("sql/jojos.db")

app = FastAPI()

upload_folder = "static/img"

app.mount("/static/img", StaticFiles(directory=upload_folder), name="static")

class Personaje(BaseModel):
    categoria_personaje: int
    nombre: str
    stand_habilidad: str
    referencia_stand: str
    fecha_nacimiento: str
    fecha_muerte: str | None
    genero: str
    altura: str
    peso: str
    nacionalidad: str
    descripcion: str
    #imagen: str

#class Partes(BaseModel):
    #nombre: str
    #descripcion: str
    #imagen: str

BASE_URL_IMAGES_PARTES = "/imagenes/partes/"
BASE_URL_IMAGES_PERSONAJES = "/imagenes/personajes/"


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
async def agregar_parte_jojos(nombre: str, descripcion: str, files: UploadFile = File(...)):

    # Verifica si la carpeta existe, si no, la crea
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    _ , extension = files.filename.split(".")
    nuevo_nombre = nombre

    # Guarda los archivos
    with open(os.path.join(upload_folder ,f"{nuevo_nombre}.{extension}"), "wb") as f:
        f.write(files.file.read())

    c = conn.cursor()
    c.execute("INSERT INTO partesJojos(nombre_parte, descripcion_parte, imagen_parte) VALUES (?, ?, ?)",
              (nombre, descripcion, f"{BASE_URL_IMAGES_PARTES}{nuevo_nombre}.{extension}"))
    conn.commit()
    return {"message": "Parte de Jojos agregada con éxito"}

@app.post("/subirPersonaje")
async def agregar_personaje_jojos(categoria_personaje: int, nombre: str, stand_habilidad: str, referencia_stand: str,
                                fecha_nacimiento: str, fecha_muerte: str | None, genero: str, altura: str, peso: str, nacionalidadL: str,
                                descripcion: str, files: UploadFile = File(...)):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    _ , extension = files.filename.split(".")
    nuevo_nombre = nombre

    with open(os.path.join(upload_folder, f"{nuevo_nombre}.{extension}"), "wb") as f:
        f.write(files.file.read())

    c = conn.cursor()
    c.execute("""INSERT INTO personajes(categoria_personaje, nombre, stand_habilidad, referencia_stand,
              fecha_nacimiento, fecha_muerte, genero, altura, peso, nacionalidad, descripcion, imagen_personaje) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (categoria_personaje, nombre, stand_habilidad, referencia_stand, fecha_nacimiento, fecha_muerte, genero, altura, peso, nacionalidadL,
              descripcion, f"{BASE_URL_IMAGES_PERSONAJES}{nuevo_nombre}.{extension}"))
    conn.commit()
    return {"message": "Personaje agregado con éxito"}

@app.get("/imagenes/partes/{nombre_parte}")
async def ver_imagen_parte(nombre_parte: str):
    image_path = os.path.join(upload_folder, nombre_parte)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"message": "Imagen no encontrada"}

@app.get("/imagenes/personajes/{nombre_pesonaje}")
async def ver_imagen_personaje(nombre_personaje: str):
    image_path = os.path.join(upload_folder, nombre_personaje)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"message": "Imagen no encontrada"}

