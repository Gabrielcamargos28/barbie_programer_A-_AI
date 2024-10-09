def heuristica(ponto_atual, ponto_destino):
    return abs(ponto_atual[0] - ponto_destino[0]) + abs(ponto_atual[1] - ponto_destino[1])

def custo_movimento(terreno):
    custos = {
        0: 1,   # Asfalto
        1: 3,   # Terra
        2: 5,   # Grama
        3: 10,  # Paralelepípedo
        -1: float('inf'),  # Edifício (intransponível)
        5: 7
    }
    return custos[terreno]
