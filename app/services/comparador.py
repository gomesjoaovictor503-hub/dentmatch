def calcular_similaridade(dente_base, outro_dente):

    # 🚫 Não comparar arcadas diferentes
    if dente_base.arcada != outro_dente.arcada:
        return None

    # 🚫 Não comparar tipos diferentes
    if dente_base.tipo != outro_dente.tipo:
        return None

    # Normalizações
    dif_largura = abs(dente_base.largura_mm - outro_dente.largura_mm) / dente_base.largura_mm
    dif_altura = abs(dente_base.altura_mm - outro_dente.altura_mm) / dente_base.altura_mm
    dif_proporcao = abs(dente_base.proporcao - outro_dente.proporcao)
    dif_canino = abs(dente_base.canino_a_canino - outro_dente.canino_a_canino) / dente_base.canino_a_canino

    # Pesos clínicos
    peso_largura = 0.4
    peso_altura = 0.3
    peso_proporcao = 0.2
    peso_canino = 0.1

    score = (
        dif_largura * peso_largura +
        dif_altura * peso_altura +
        dif_proporcao * peso_proporcao +
        dif_canino * peso_canino
    )

    similaridade = max(0, 100 - (score * 100))

    # Penalização por formato diferente
    if dente_base.formato != outro_dente.formato:
        similaridade -= 5

    return round(similaridade, 2)
