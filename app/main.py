from fastapi import FastAPI
from app.routers import usuarios, produtos

app = FastAPI(title="PyStore API")

app.include_router(usuarios.router)
app.include_router(produtos.router)

@app.get("/")
def home():
    return {"mensagem": "API PyStore está online!"}
