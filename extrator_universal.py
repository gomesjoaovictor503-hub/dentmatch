import os
import re
import pandas as pd
from PyPDF2 import PdfReader

PDF_FOLDER = "importacoes/pdf"
CSV_FOLDER = "importacoes/csv"

def validar_medidas(n1, n2, n3):
    try:
        n1 = float(n1)
        n2 = float(n2)
        n3 = float(n3)
    except:
        return False

    # Faixas clínicas aproximadas
    if 20 <= n1 <= 60 and 5 <= n2 <= 15 and 4 <= n3 <= 15:
        return True

    return False


def executar():
    if not os.path.exists(PDF_FOLDER):
        print("❌ Pasta importacoes/pdf não encontrada.")
        return

    arquivos = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    if not arquivos:
        print("⚠ Nenhum PDF encontrado.")
        return

    print("PDFs encontrados:", arquivos)

    for arquivo in arquivos:
        caminho_pdf = os.path.join(PDF_FOLDER, arquivo)
        print(f"\n📄 Processando: {arquivo}")

        reader = PdfReader(caminho_pdf)
        texto = ""

        for page in reader.pages:
            texto_extraido = page.extract_text()
            if texto_extraido:
                texto += texto_extraido + "\n"

        if not texto.strip():
            print("⚠ Nenhum texto extraído do PDF.")
            continue

        # DEBUG: Mostra início do texto extraído
        print("\n--- Início do texto extraído ---")
        print(texto[:1000])
        print("--- Fim do trecho exibido ---\n")

        padrao = r'(\d+[,\.]\d+)\s+(\d+[,\.]\d+)\s+(\d+[,\.]\d+)\s+([A-Z0-9\/\- ]{2,})'
        resultados = re.findall(padrao, texto)

        if not resultados:
            print("⚠ Nenhum padrão compatível encontrado.")
            continue

        dados = []

        for n1, n2, n3, modelo in resultados:
            n1 = n1.replace(",", ".")
            n2 = n2.replace(",", ".")
            n3 = n3.replace(",", ".")

            if not validar_medidas(n1, n2, n3):
                continue

            modelo = modelo.strip().replace(" ", "")

            dados.append([
                "Kulzer",
                "Linha Genérica",
                modelo,
                "Superior",
                "Anterior",
                float(n1),
                float(n2),
                float(n3),
                "Anatomico"
            ])

        if not dados:
            print("⚠ Nenhum registro válido após validação clínica.")
            continue

        if not os.path.exists(CSV_FOLDER):
            os.makedirs(CSV_FOLDER)

        nome_csv = arquivo.replace(".pdf", ".csv")
        caminho_csv = os.path.join(CSV_FOLDER, nome_csv)

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

        df.to_csv(caminho_csv, index=False)

        print(f"✅ CSV gerado: {nome_csv}")
        print(f"📊 Registros inseridos no CSV: {len(df)}")


if __name__ == "__main__":
    executar()
