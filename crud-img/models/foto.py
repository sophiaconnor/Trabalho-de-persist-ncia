from pydantic import BaseModel

""""⊱───────⊰•͙✧ BaseModel da class foto ✧•͙⊱───────⊰"""
class FotoModel(BaseModel):
    nome_original: str
    nome_armazenado: str
    extensao: str
    tipo_mime: str
    tamanho: int
    categoria: str 
    descricao: str 
    data_upload: str
    sha256: str
