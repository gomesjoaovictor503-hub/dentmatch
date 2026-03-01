import os
import pandas as pd
from app.database import SessionLocal
from app import models

CSV_FOLDER = "importacoes/csv"

def importar_csv():
    db = SessionLocal()

    arquivos = [f for f in os.listdir(CSV_FOLDER) if f.endswith(".csv")]

    if not arquivos:
        print("Nenhum CSV encontrado.")
        return

    for arquivo in arquivos:
        caminho = os.path.join(CSV_FOLDER, arquivo)
        print(f"\nProcessando: {arquivo}")

        df = pd.read_csv(caminho)

        inseridos = 0
        duplicados = 0

        for _, row in df.iterrows():

            existe = db.query(models.Dente).filter(
                models.Dente.marca == row["marca"],
                models.Dente.modelo == row["modelo"]
            ).first()

            if existe:
                duplicados += 1
                continue

            novo = models.Dente(
                marca=row["marca"],
                linha=row["linha"],
                modelo=row["modelo"],
                arcada=row["arcada"],
                tipo=row["tipo"],
                canino_a_canino=float(row["canino_a_canino"]),
                altura_mm=float(row["altura_mm"]),
                largura_mm=float(row["largura_mm"]),
                formato=row["formato"]
            )

            db.add(novo)
            inseridos += 1

        db.commit()

        print(f"Inseridos: {inseridos}")
        print(f"Duplicados ignorados: {duplicados}")

    db.close()

if _name_ == "_main_":
    importar_csv()
