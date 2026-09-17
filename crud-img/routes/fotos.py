from datetime import datetime
from pathlib import Path
import hashlib

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from core.logging_config import logger
from models.foto import foto, FotoUpdate
from services.json_repository import (
    ALLOWED_EXT,
    UPLOAD_DIR,
    adicionar,
    atualizar,
    buscar_por_id,
    exportar_para_csv,
    ler_json,
    remover,
)


BASE_DIR = Path(__file__).resolve().parent.parent
FOTOS_FILE = BASE_DIR / "data" / "fotos.json"
CSV_FILE = BASE_DIR / "data" / "fotos.csv"

CSV_FIELDS = [
    "id",
    "nome_original",
    "nome_armazenado",
    "extensao",
    "tipo_mime",
    "tamanho",
    "categoria",
    "descricao",
    "data_upload",
    "sha256",
    "disponivel",
]

router = APIRouter(
    prefix="/fotos",
    tags=["Fotos"],
)


@router.post(
    "",
    response_model=foto,
    status_code=status.HTTP_201_CREATED,
)
async def criar_foto(
    id: int = Form(...),
    categoria: str = Form(""),
    descricao: str = Form(""),
    imagem: UploadFile = File(...),
):
    if buscar_por_id(FOTOS_FILE, id):
        logger.warning(
            "Tentativa de cadastrar foto com ID duplicado: %s",
            id,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Foto com este ID já existe.",
        )

    nome_original = imagem.filename
    ext = Path(nome_original).suffix.lower()

    if ext not in ALLOWED_EXT:
        logger.warning(
            "Tentativa de upload com extensão não permitida: %s",
            ext,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensão de imagem não permitida: {ext}.",
        )

    conteudo = await imagem.read()

    nome_armazenado = f"{id}{ext}"
    caminho_imagem = UPLOAD_DIR / nome_armazenado

    with open(caminho_imagem, "wb") as buffer:
        buffer.write(conteudo)

    nova_foto = foto(
        id=id,
        nome_original=nome_original,
        nome_armazenado=nome_armazenado,
        extensao=ext,
        tipo_mime=imagem.content_type or "application/octet-stream",
        tamanho=len(conteudo),
        categoria=categoria,
        descricao=descricao,
        data_upload=datetime.now().isoformat(timespec="seconds"),
        sha256=hashlib.sha256(conteudo).hexdigest(),
        disponivel=True,
    )

    dados = nova_foto.model_dump(mode="json")

    adicionar(FOTOS_FILE, dados)

    logger.info(
        "Foto cadastrada: id=%s, nome_original=%s",
        nova_foto.id,
        nova_foto.nome_original,
    )

    return nova_foto


@router.get(
    "",
    response_model=list[foto],
)
def listar_fotos():
    fotos = ler_json(FOTOS_FILE)

    logger.info(
        "Listagem de fotos: %d registro(s).",
        len(fotos),
    )

    return fotos


@router.get(
    "/{foto_id}",
    response_model=foto,
)
def obter_foto(foto_id: int):
    encontrada = buscar_por_id(FOTOS_FILE, foto_id)

    if not encontrada:
        logger.warning(
            "Foto não encontrada: %s",
            foto_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto não encontrada.",
        )

    return encontrada


@router.get("/{foto_id}/imagem")
def obter_imagem(foto_id: int):
    encontrada = buscar_por_id(FOTOS_FILE, foto_id)

    if not encontrada:
        logger.warning(
            "Foto não encontrada: %s",
            foto_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto não encontrada.",
        )

    caminho_imagem = UPLOAD_DIR / encontrada["nome_armazenado"]

    if not caminho_imagem.exists():
        logger.warning(
            "Arquivo de imagem ausente em disco: %s",
            caminho_imagem,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo de imagem não encontrado.",
        )

    return FileResponse(
        caminho_imagem,
        media_type=encontrada.get("tipo_mime") or None,
    )


@router.put(
    "/{foto_id}",
    response_model=foto,
)
def atualizar_foto(foto_id: int, dados: FotoUpdate):
    foto_atual = buscar_por_id(FOTOS_FILE, foto_id)

    if not foto_atual:
        logger.warning(
            "Tentativa de atualizar foto inexistente: %s",
            foto_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto não encontrada.",
        )

    if dados.categoria is not None:
        foto_atual["categoria"] = dados.categoria

    if dados.descricao is not None:
        foto_atual["descricao"] = dados.descricao

    atualizar(FOTOS_FILE, foto_id, foto_atual)

    logger.info(
        "Foto atualizada: %s",
        foto_id,
    )

    return foto_atual


@router.put(
    "/{foto_id}/imagem",
    response_model=foto,
)
async def atualizar_imagem(foto_id: int, imagem: UploadFile = File(...)):
    foto_atual = buscar_por_id(FOTOS_FILE, foto_id)

    if not foto_atual:
        logger.warning(
            "Tentativa de trocar imagem de foto inexistente: %s",
            foto_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto não encontrada.",
        )

    nome_original = imagem.filename
    ext = Path(nome_original).suffix.lower()

    if ext not in ALLOWED_EXT:
        logger.warning(
            "Tentativa de upload com extensão não permitida: %s",
            ext,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensão de imagem não permitida: {ext}.",
        )

    conteudo = await imagem.read()

    caminho_antigo = UPLOAD_DIR / foto_atual["nome_armazenado"]
    if caminho_antigo.exists():
        caminho_antigo.unlink()

    novo_nome = f"{foto_id}{ext}"
    caminho_novo = UPLOAD_DIR / novo_nome

    with open(caminho_novo, "wb") as buffer:
        buffer.write(conteudo)

    foto_atual["nome_original"] = nome_original
    foto_atual["nome_armazenado"] = novo_nome
    foto_atual["extensao"] = ext
    foto_atual["tipo_mime"] = imagem.content_type or "application/octet-stream"
    foto_atual["tamanho"] = len(conteudo)
    foto_atual["sha256"] = hashlib.sha256(conteudo).hexdigest()

    atualizar(FOTOS_FILE, foto_id, foto_atual)

    logger.info(
        "Imagem substituída para foto: %s",
        foto_id,
    )

    return foto_atual


@router.delete(
    "/{foto_id}",
    status_code=status.HTTP_200_OK,
)
def excluir_foto(foto_id: int):
    encontrada = buscar_por_id(FOTOS_FILE, foto_id)

    if not encontrada:
        logger.warning(
            "Tentativa de remover foto inexistente: %s",
            foto_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto não encontrada.",
        )

    remover(FOTOS_FILE, foto_id)

    caminho_imagem = UPLOAD_DIR / encontrada["nome_armazenado"]
    if caminho_imagem.exists():
        caminho_imagem.unlink()

    logger.info(
        "Foto removida: %s",
        foto_id,
    )

    return {
        "mensagem": "Foto removida com sucesso."
    }


@router.post("/exportar-csv")
def exportar_csv_endpoint():
    caminho = exportar_para_csv(FOTOS_FILE, CSV_FILE, CSV_FIELDS)

    logger.info("Exportação manual de JSON para CSV solicitada.")

    return FileResponse(
        caminho,
        filename="fotos.csv",
        media_type="text/csv",
    )
