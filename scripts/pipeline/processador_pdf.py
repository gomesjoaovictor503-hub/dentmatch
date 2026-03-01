import os
import sys

# Permite importar arquivos da raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from extrair_pdf import extrair_texto_pdf
from scripts.extratores.extrator_ocr import usar_ocr
from scripts.extratores.extrator_texto import usar_extrator_texto


PDF_DIR = "importacoes/pdf"


def processar_pdf(caminho_pdf):
    print(f"\n📄 Processando: {caminho_pdf}")

    texto = extrair_texto_pdf(caminho_pdf)

    if len(texto.strip()) < 200:
        print("⚠️ PDF parece ser imagem. Usando OCR...")
        usar_ocr(caminho_pdf)
    else:
        print("✅ PDF contém texto estruturado.")
        usar_extrator_texto(texto, caminho_pdf)


def executar():
    for arquivo in os.listdir(PDF_DIR):
        if arquivo.lower().endswith(".pdf"):
            caminho_completo = os.path.join(PDF_DIR, arquivo)
            processar_pdf(caminho_completo)


if __name__ == "__main__":
    executar()
