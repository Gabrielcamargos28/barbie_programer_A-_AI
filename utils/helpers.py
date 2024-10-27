def heuristica(ponto_atual, ponto_destino):
    return abs(ponto_atual[0] - ponto_destino[0]) + abs(ponto_atual[1] - ponto_destino[1])

def custo_movimento(terreno):
    custos = {
        1: 1,   # Asfalto
        3: 3,   # Terra
        5: 5,   # Grama
        10: 10,  # Paralelepípedo
        -1: float('inf')  # Edifício (intransponível)
    }
    return custos.get(terreno, float('inf'))
