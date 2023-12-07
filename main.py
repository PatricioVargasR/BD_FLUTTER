from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def inicio():
    return {"Developed by": "Patricio Vargas f:"}
