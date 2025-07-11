# app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from app.processador import processar_planilha

app = FastAPI()

# Libera requisições externas (pode deixar assim no Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    nome_arquivo = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(nome_arquivo, "wb") as f:
        f.write(await file.read())

    # Chama o robô para processar a planilha e gerar nova
    caminho_saida = await processar_planilha(nome_arquivo)

    return {
        "mensagem": "Planilha processada com sucesso!",
        "download": f"/static/{caminho_saida}"
    }

@app.get("/static/{nome_arquivo}")
async def baixar(nome_arquivo: str):
    caminho = os.path.join("static", nome_arquivo)
    return FileResponse(
        caminho,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=nome_arquivo
    )
