import hashlib
import os
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from core.logging_config import logger
from services.fotos_repository import (
    adicionar_json, atualizar_json, ler_json, remover_json,
    adicionar_csv, atualizar_csv, ler_csv, remover_csv
)
from models.foto import Foto

BASE_DIR = Path(__file__).resolve().parent.parent
FOTOS_JSON = BASE_DIR / "data" / "fotos.json"
FOTOS_CSV = BASE_DIR / "data" / "fotos.csv"

router = APIRouter(
    prefix="/fotos",   # plural para ficar mais natural
    tags=["Fotos"],
)

def gerar_sha(data: dict) -> str:
    texto = f"{data['nome_original']}{data.get('descricao','')}{data['nome_armazenado']}{data['data_upload']}"
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()

@router.post("/", response_model=Foto, status_code=status.HTTP_201_CREATED)
async def criar_foto(
    file: UploadFile = File(...),
    categoria: str = Form(None),
    descricao: str = Form(None),
):
    nome_original = file.filename
    extensao = os.path.splitext(nome_original)[1]
    tipo_mime = file.content_type
    conteudo = await file.read()
    tamanho = len(conteudo)

    nome_armazenado = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{nome_original}"
    data_upload = datetime.now().isoformat()

    registros = ler_json(FOTOS_JSON)
    novo_id = max([r["id"] for r in registros], default=0) + 1

    registro = {
        "id": novo_id,
        "nome_original": nome_original,
        "nome_armazenado": nome_armazenado,
        "extensao": extensao,
        "tipo_mime": tipo_mime,
        "tamanho": tamanho,
        "categoria": categoria,
        "descricao": descricao,
        "data_upload": data_upload,
    }
    registro["sha256"] = gerar_sha(registro)

    adicionar_json(FOTOS_JSON, registro)
    adicionar_csv(FOTOS_CSV, registro)

    logger.info("Foto cadastrada: id=%s, nome=%s", registro["id"], registro["nome_original"])
    return registro

@router.get("/", response_model=list[Foto])
def listar_fotos():
    return ler_json(FOTOS_JSON)

@router.get("/csv")
def listar_fotos_csv():
    return ler_csv(FOTOS_CSV)

@router.put("/{foto_id}", response_model=Foto)
async def atualizar_foto(
    foto_id: int,
    categoria: str = Form(None),
    descricao: str = Form(None),
):
    registros = ler_json(FOTOS_JSON)
    foto = next((r for r in registros if r["id"] == foto_id), None)
    if not foto:
        raise HTTPException(status_code=404, detail="Foto não encontrada.")

    if categoria is not None:
        foto["categoria"] = categoria
    if descricao is not None:
        foto["descricao"] = descricao

    foto["sha256"] = gerar_sha(foto)

    atualizar_json(FOTOS_JSON, foto_id, foto)
    atualizar_csv(FOTOS_CSV, foto_id, foto)
    return foto

@router.delete("/{foto_id}", status_code=status.HTTP_200_OK)
def excluir_foto(foto_id: int):
    if not remover_json(FOTOS_JSON, foto_id):
        raise HTTPException(status_code=404, detail="Foto não encontrada.")
    remover_csv(FOTOS_CSV, foto_id)
    return {"mensagem": "Foto removida com sucesso."}
