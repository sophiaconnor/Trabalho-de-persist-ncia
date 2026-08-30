from fastapi import APIRouter

router = APIRouter()


@router.post("/backup")
def fazer_backup():
    return {
        "mensagem": "Rota de backup funcionando!"
    }