from pydantic import BaseModel, Field
from typing import Optional

class foto(BaseModel):
    id: int = Field(
        gt=0,
        description="Identificador único da foto",
    )
    nome_original: str = Field(
        min_length=1,
        max_length=255,
        description="Nome original do arquivo enviado",
    )
    nome_armazenado: str = Field(
        min_length=1,
        max_length=255,
        description="Nome do arquivo salvo em disco (baseado no id)",
    )
    extensao: str = Field(
        min_length=2,
        max_length=10,
        description="Extensão do arquivo (ex: '.jpg')",
    )
    tipo_mime: str = Field(
        min_length=3,
        max_length=100,
        description="Tipo MIME da imagem (ex: 'image/jpeg')",
    )
    tamanho: int = Field(
        gt=0,
        description="Tamanho do arquivo em bytes",
    )
    categoria: str = Field(
        default="",
        max_length=100,
        description="Categoria da foto",
    )
    descricao: str = Field(
        default="",
        max_length=1000,
        description="Descrição livre da foto",
    )
    data_upload: str = Field(
        description="Data e hora do upload",
    )
    sha256: str = Field(
        min_length=64,
        max_length=64,
    )
    disponivel: bool = True


class FotoUpdate(BaseModel):
    "Campos que podem ser atualizados de uma foto."

    categoria: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Nova categoria da foto",
    )
    descricao: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Nova descrição da foto",
    )
