from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import sqlite3

from pydantic import BaseModel

conn = sqlite3.connect("sql/jojos.db")

app = FastAPI()


class Parte(BaseModel):
    nombre: str
    descripcion: str
    imagen: str

class Personaje(BaseModel):
    categoria_personaje: int
    nombre: str
    stand: str
    referencia: str
    fecha_nacimiento: str
    nacionalidad: str
    descripcion: str
    imagen: str

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
async def agregar_parte_jojos(parte: Parte):

    c = conn.cursor()
    c.execute("INSERT INTO partesJojos(nombre_parte, descripcion_parte, imagen_parte) VALUES (?, ?, ?)",
              (parte.nombre, parte.descripcion, parte.imagen))
    conn.commit()
    return {"message": "Parte de Jojos agregada con éxito"}

@app.delete("/borrarParte/{nombre}")
async def eliminar_parte(nombre: str):
    try:
        c = conn.cursor()

        # Obtener el ID de la parte que se va a eliminar
        c.execute("SELECT id_parte FROM partesJojos WHERE nombre_parte = ?", (nombre,))
        parte_id = c.fetchone()

        if parte_id:
            parte_id = parte_id[0]

            # Eliminar personajes asociados a la parte
            c.execute("DELETE FROM personajes WHERE categoria_personaje = ?", (parte_id,))

            # Eliminar la parte
            c.execute("DELETE FROM partesJojos WHERE id_parte = ?", (parte_id,))

            conn.commit()

            if c.rowcount == 0:
                return {"error-message": "La parte no existe"}

            return {"message": "Parte y personajes asociados eliminados correctamente"}

        return {"error-message": "La parte no existe"}

    except sqlite3.Error as e:
        return {"error-message": f"Error al eliminar los datos: {str(e)}"}


@app.put("/actualizar_parte/{nombre}")
async def actualizar_parte(nombre: str, parte:Parte):
    c = conn.cursor()
    c.execute('UPDATE partesJojos SET nombre_parte = ?, descripcion_parte = ?, imagen_parte = ? WHERE nombre_parte = ?' , (
        parte.nombre, parte.descripcion, parte.imagen, nombre
    ))
    conn.commit()
    return {"message": "Actualizado con exito"}



# Endpoint para subir un Personaje
@app.post("/subirPersonaje")
async def agregar_personaje_jojos(personaje: Personaje):

    c = conn.cursor()
    c.execute("""INSERT INTO personajes(categoria_personaje, nombre, stand_habilidad, referencia_stand,
              fecha_nacimiento, nacionalidad, descripcion, imagen_personaje) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (personaje.categoria_personaje, personaje.nombre, personaje.stand, personaje.referencia, personaje.fecha_nacimiento, personaje.descripcion, personaje.imagen))
    conn.commit()
    return {"message": "Personaje agregado con éxito"}


@app.delete("/eliminar_personaje/{nombre_personaje}")
async def eliminar_personaje(nombre: str):
    c = conn.cursor()
    c.execute("DELETE FROM personajes WEHERE nombre = ?",(nombre,))
    conn.commit
    return {"message": "Eliminado con éxito"}