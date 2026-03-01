import os
import re
import csv
import pdfplumber

PDF_PATH = "importacoes/pdf/Magister.pdf"
CSV_PATH = "importacoes/csv/Magister.csv"

MARCA = "Kulzer"
LINHA = "Magister"

def modelo_valido(modelo):
    # Modelos reais Magister
    return re.match(r'^(L4\d{2}|P4\d{2}|A4\d{2}|A5\d{2})$', modelo)

def executar():

    if not os.path.exists(PDF_PATH):
        print("❌ PDF não encontrado.")
        return

    modelos_encontrados = set()

    with pdfplumber.open(PDF_PATH) as pdf:

        for page in pdf.pages:
            texto = page.extract_text()

            if not texto:
                continue

            encontrados = re.findall(r'[LPA]\s?\d{3}', texto)

            for m in encontrados:
                modelo_limpo = m.replace(" ", "")
                if modelo_valido(modelo_limpo):
                    modelos_encontrados.add(modelo_limpo)

    if not modelos_encontrados:
        print("⚠ Nenhum modelo válido encontrado.")
        return

    os.makedirs("importacoes/csv", exist_ok=True)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
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

        for modelo in sorted(modelos_encontrados):
            writer.writerow([
                MARCA,
                LINHA,
                modelo,
                "Superior",
                "Anterior",
                0,
                0,
                0,
                "Anatomico"
            ])

    print("✅ CSV limpo gerado!")
    print("📊 Modelos únicos encontrados:", len(modelos_encontrados))

if __name__ == "__main__":
    executar()
