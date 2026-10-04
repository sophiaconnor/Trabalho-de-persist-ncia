from pydantic import BaseModel

""""⊱───────⊰•͙✧ BaseModel da class foto ✧•͙⊱───────⊰"""
class Foto(BaseModel):
    id: int
    nome_original: str
    nome_armazenado: str
    extensao: str
    tipo_mime: str
    tamanho: int
    categoria: str | None = None
    descricao: str | None = None
    data_upload: str
    sha256: str
    autor: str
    local: str
    ano: int
