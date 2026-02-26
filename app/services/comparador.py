def calcular_score_e_diferencas(d1, d2):
    diff_largura = abs(d1.largura_mm - d2.largura_mm)
    diff_altura = abs(d1.altura_mm - d2.altura_mm)
    diff_proporcao = abs(d1.proporcao - d2.proporcao)
    diff_canino = abs(d1.canino_a_canino - d2.canino_a_canino)

    score = 0
    score += diff_largura * 3
    score += diff_altura * 3
    score += diff_proporcao * 4
    score += diff_canino * 2

    # Penalização por formato diferente
    if d1.formato.lower() != d2.formato.lower():
        score += 5

    # Penalização por tipo diferente
    if d1.tipo.lower() != d2.tipo.lower():
        score += 8

    diferencas = {
        "largura_mm": round(diff_largura, 3),
        "altura_mm": round(diff_altura, 3),
        "proporcao": round(diff_proporcao, 3),
        "canino_a_canino": round(diff_canino, 3),
        "formato_diferente": d1.formato.lower() != d2.formato.lower(),
        "tipo_diferente": d1.tipo.lower() != d2.tipo.lower()
    }

    return score, diferencas


def score_para_percentual(score):
    max_score_aceitavel = 40
    percentual = max(0, 100 - (score / max_score_aceitavel) * 100)
    return round(percentual, 2)
def classificar_similaridade(percentual):
    if percentual >= 95:
        return "Altamente Recomendado"
    elif percentual >= 85:
        return "Recomendado"
    elif percentual >= 70:
        return "Aceitável"
    elif percentual >= 50:
        return "Baixa Similaridade"
    else:
        return "Não Recomendado"
