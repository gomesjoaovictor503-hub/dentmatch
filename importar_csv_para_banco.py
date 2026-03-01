import csv
import os

from app.database import SessionLocal
from app import models

CSV_PATH = "importacoes/csv/Magister.csv"

def importar():

    if not os.path.exists(CSV_PATH):
        print("❌ CSV não encontrado:", CSV_PATH)
        return

    db = SessionLocal()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        contador = 0

        for row in reader:

            novo_dente = models.Dente(
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

            db.add(novo_dente)
            contador += 1

        db.commit()
        db.close()

    print(f"✅ {contador} registros importados para o banco.")

if __name__ == "__main__":
    importar()
