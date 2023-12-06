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
    imagen: str

class Partes(BaseModel):
    nombre: str
    descripcion: str
    imagen: str

BASE_URL_IMAGES = "/imagenes/"


@app.get("/")
async def inicio():
    return {"Developed by": "Patricio Vargas f:"}


@app.get("/images/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join(upload_folder, image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"message": "Imagen no encontrada"}


@app.get("/partesJojos")
async def obtener_partes_jojos():
    c = conn.cursor()
    c.execute("SELECT * FROM partesJojos")
    response = []
    for fila in c:
        parte = {"Nombre": fila[1], "descripcion": fila[2], "imagenes": fila[3]}
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

@app.post("/subirPersonaje/")
async def agregar_parte_jojos(parte:Partes, File: UploadFile = File(...)):
    if not os.path.exists(upload_folder):
        os.mkdirs(upload_folder)

    imagen_parte = File.filename

    c = conn.cursor()
    c.execute("INSERT INTO partesJojos(nombre_parte, descripcion_parte, imagen_parte) VALUES (?, ?, ?)", (parte.nombre, parte.descripcion, f"{BASE_URL_IMAGES}" + imagen_parte))
    conn.commit()

    with open(os.path.join(upload_folder, File.filename), "wb") as f:
        f.write(File.file.read())

    return {"message": "Parte de Jojos agregada con éxito"}