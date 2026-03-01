import csv
import os
import sys

# Permite importar app corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.database import SessionLocal
from app import models
from scripts.mapeamentos.magister_map import MAPEAMENTO


CSV_PATH = "importacoes/csv/Magister.csv"


def importar():
    if not os.path.exists(CSV_PATH):
        print("CSV não encontrado.")
        return

    db = SessionLocal()

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            dados = {}

            for coluna_csv, coluna_model in MAPEAMENTO.items():
                if hasattr(models.Dente, coluna_model):
                    dados[coluna_model] = row.get(coluna_csv)

            novo_dente = models.Dente(**dados)
            db.add(novo_dente)

        db.commit()
        print("Importação concluída com sucesso.")

    db.close()


if __name__ == "__main__":
    importar()
