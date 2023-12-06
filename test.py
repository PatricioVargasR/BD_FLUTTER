from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel



app = FastAPI()

class Partes(BaseModel):
    imagen: UploadFile = File(...)
    nombre: str
    #descripcion: str
    #imagen: str
@app.post("/uploadfile/")
async def subir_archivo(nombre1: Partes):
    impresion = {"Hola": nombre1.nombre}
    return {"filename": nombre1.filenames, "impresion": impresion}