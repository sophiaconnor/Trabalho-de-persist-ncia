import json, csv, hashlib, os
from pathlib import Path

""""⊱───────⊰•͙✧ JSON ✧•͙⊱───────⊰"""
def ler_json(file: Path):
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("[]", encoding="utf-8")
    with file.open("r", encoding="utf-8") as f:
        return json.load(f)

def adicionar_json(file: Path, dados: dict):
    registros = ler_json(file)
    registros.append(dados)
    with file.open("w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=4)

def atualizar_json(file: Path, id: int, dados: dict):
    registros = ler_json(file)
    for i, r in enumerate(registros):
        if r["id"] == id:
            registros[i] = dados
            with file.open("w", encoding="utf-8") as f:
                json.dump(registros, f, ensure_ascii=False, indent=4)
            return True
    return False

def remover_json(file: Path, id: int):
    registros = ler_json(file)
    novos = [r for r in registros if r["id"] != id]
    if len(novos) != len(registros):
        with file.open("w", encoding="utf-8") as f:
            json.dump(novos, f, ensure_ascii=False, indent=4)
        return True
    return False

""""⊱───────⊰•͙✧ CSV ✧•͙⊱───────⊰"""
def inicializar_csv(file: Path):
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
        with file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "id","nome_original","nome_armazenado","extensao",
                "tipo_mime","tamanho","categoria","descricao",
                "data_upload","sha256", "autor", "local", "ano","evento"
            ])
            writer.writeheader()

def ler_csv(file: Path):
    inicializar_csv(file)
    with file.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def adicionar_csv(file: Path, dados: dict):
    inicializar_csv(file)
    with file.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id","nome_original","nome_armazenado","extensao",
            "tipo_mime","tamanho","categoria","descricao",
            "data_upload","sha256", "autor", "local", "ano","evento"
        ])
        writer.writerow(dados)

def atualizar_csv(file: Path, id: int, dados: dict):
    registros = ler_csv(file)
    atualizado = False
    with file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id","nome_original","nome_armazenado","extensao",
            "tipo_mime","tamanho","categoria","descricao",
            "data_upload","sha256", "autor", "local", "ano","evento"
        ])
        writer.writeheader()
        for r in registros:
            if int(r["id"]) == id:
                writer.writerow(dados)
                atualizado = True
            else:
                writer.writerow(r)
    return atualizado

def remover_csv(file: Path, id: int):
    registros = ler_csv(file)
    novos = [r for r in registros if int(r["id"]) != id]
    if len(novos) != len(registros):
        with file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "id","nome_original","nome_armazenado","extensao",
                "tipo_mime","tamanho","categoria","descricao",
                "data_upload","sha256", "autor", "local", "ano","evento"
            ])
            writer.writeheader()
            writer.writerows(novos)
        return True
    return False

""""⊱───────⊰•͙✧ F7, F8, F9, F16 ✧•͙⊱───────⊰"""

# --- F7: Filtragem ---
def filtrar_fotos_json(file: Path, evento=None, ano=None, formato=None, categoria=None):
    registros = ler_json(file)
    if evento:
        registros = [r for r in registros if r.get("evento") == evento]
    if ano:
        registros = [r for r in registros if r.get("ano") == ano]
    if formato:
        registros = [r for r in registros if r.get("extensao") == formato]
    if categoria:
        registros = [r for r in registros if r.get("categoria") == categoria]
    return registros

def filtrar_fotos_csv(file: Path, evento=None, ano=None, formato=None, categoria=None):
    registros = ler_csv(file)
    if evento:
        registros = [r for r in registros if r.get("evento") == evento]
    if ano:
        registros = [r for r in registros if int(r.get("ano", 0)) == ano]
    if formato:
        registros = [r for r in registros if r.get("extensao") == formato]
    if categoria:
        registros = [r for r in registros if r.get("categoria") == categoria]
    return registros

# --- F8: Estatísticas ---
def calcular_estatisticas_json(file: Path):
    registros = ler_json(file)
    total = len(registros)
    tamanho_total = sum(r.get("tamanho", 0) for r in registros)
    por_extensao, por_categoria = {}, {}
    for r in registros:
        ext = r.get("extensao")
        cat = r.get("categoria")
        por_extensao[ext] = por_extensao.get(ext, 0) + 1
        por_categoria[cat] = por_categoria.get(cat, 0) + 1
    return {
        "total_documentos": total,
        "espaco_utilizado_bytes": tamanho_total,
        "por_extensao": por_extensao,
        "por_categoria": por_categoria
    }

# --- F9: Verificação de integridade ---
def calcular_hash(filepath: Path) -> str:
    sha256 = hashlib.sha256()
    with filepath.open("rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            sha256.update(bloco)
    return sha256.hexdigest()

def verificar_integridade_json(file: Path, id: int, storage_dir: Path):
    registros = ler_json(file)
    foto = next((r for r in registros if r["id"] == id), None)
    if not foto:
        return {"erro": "Foto não encontrada"}
    filepath = storage_dir / foto["nome_armazenado"]
    if not filepath.exists():
        return {"erro": "Arquivo não encontrado"}
    hash_atual = calcular_hash(filepath)
    return {
        "id": foto["id"],
        "nome": foto["nome_original"],
        "hash_original": foto["sha256"],
        "hash_atual": hash_atual,
        "integro": foto["sha256"] == hash_atual
    }

# --- F16: Estatísticas específicas ---
def calcular_estatisticas_tema_json(file: Path):
    registros = ler_json(file)
    por_evento, por_ano, por_formato = {}, {}, {}
    for r in registros:
        por_evento[r.get("evento")] = por_evento.get(r.get("evento"), 0) + 1
        por_ano[r.get("ano")] = por_ano.get(r.get("ano"), 0) + 1
        por_formato[r.get("extensao")] = por_formato.get(r.get("extensao"), 0) + 1
    return {
        "estatisticas_evento": por_evento,
        "estatisticas_ano": por_ano,
        "estatisticas_formato": por_formato
    }
