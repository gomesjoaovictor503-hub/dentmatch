from extrair_pdf import processar_texto
import pandas as pd
import os

CSV_FOLDER = "importacoes/csv"


def usar_extrator_texto(texto, caminho_pdf):
    dados = processar_texto(texto)

    if not dados:
        print("Nenhum dado válido encontrado.")
        return

    df = pd.DataFrame(dados, columns=[
        "marca",
        "linha",
        "modelo",
        "arcada",
        "tipo",
        "canino_a_canino",
        "altura_mm",
        "largura_mm",
        "formato"
    ])

    nome_csv = os.path.basename(caminho_pdf).replace(".pdf", ".csv")
    caminho_csv = os.path.join(CSV_FOLDER, nome_csv)
    df.to_csv(caminho_csv, index=False)

    print(f"✅ CSV gerado via TEXTO: {nome_csv}")
