import json
import csv
from pathlib import Path

""""⊱───────⊰•͙✧JSON ✧•͙⊱───────⊰"""
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
                "data_upload","sha256"
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
            "data_upload","sha256"
        ])
        writer.writerow(dados)

def atualizar_csv(file: Path, id: int, dados: dict):
    registros = ler_csv(file)
    atualizado = False
    with file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id","nome_original","nome_armazenado","extensao",
            "tipo_mime","tamanho","categoria","descricao",
            "data_upload","sha256"
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
                "data_upload","sha256"
            ])
            writer.writeheader()
            writer.writerows(novos)
        return True
    return False
