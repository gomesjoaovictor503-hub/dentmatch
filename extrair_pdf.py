import os
import re
import pandas as pd
from PyPDF2 import PdfReader

PDF_FOLDER = "importacoes/pdf"
CSV_FOLDER = "importacoes/csv"

def detectar_marca(texto):
    if "Magister" in texto:
        return "Kulzer", "Magister"
    if "Ivoclar" in texto:
        return "Ivoclar", "Linha Comercial"
    if "Trilux" in texto:
        return "Trilux", "Linha Comercial"
    return "Desconhecida", "Linha Genérica"

def validar_medidas(n1, n2, n3):
    """
    Evita cadastrar lixo.
    Faixas clínicas reais aproximadas.
    """
    try:
        n1 = float(n1)
        n2 = float(n2)
        n3 = float(n3)
    except:
        return False

    if 20 <= n1 <= 60 and 5 <= n2 <= 15 and 5 <= n3 <= 15:
        return True

    return False

def extrair_modelos(texto, marca, linha):
    padrao = r'(\d+[,\.]\d+)\s+(\d+[,\.]\d+)\s+(\d+[,\.]\d+)\s+([A-Z0-9\/\- ]{2,})'
    resultados = re.findall(padrao, texto)

    dados = []

    for n1, n2, n3, modelo in resultados:
        n1 = n1.replace(",", ".")
        n2 = n2.replace(",", ".")
        n3 = n3.replace(",", ".")

        if not validar_medidas(n1, n2, n3):
            continue

        modelo = modelo.strip().replace(" ", "")

        dados.append([
            marca,
            linha,
            modelo,
            "Superior",
            "Anterior",
            float(n1),
            float(n2),
            float(n3),
            "Anatomico"
        ])

    return dados

def processar_pdf(caminho_pdf):
    reader = PdfReader(caminho_pdf)
    texto = ""

    for page in reader.pages:
        texto += page.extract_text() + "\n"

    marca, linha = detectar_marca(texto)
    dados = extrair_modelos(texto, marca, linha)

    return dados

def executar():
    arquivos = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    for arquivo in arquivos:
        caminho_pdf = os.path.join(PDF_FOLDER, arquivo)
        dados = processar_pdf(caminho_pdf)

        if not dados:
            print(f"Nenhum dado válido encontrado em {arquivo}")
            continue

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

        nome_csv = arquivo.replace(".pdf", ".csv")
        caminho_csv = os.path.join(CSV_FOLDER, nome_csv)
        df.to_csv(caminho_csv, index=False)

        print(f"CSV gerado: {nome_csv} | Registros: {len(df)}")

if _name_ == "_main_":
    executar()
