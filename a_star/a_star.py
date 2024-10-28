import heapq
from utils.helpers import heuristica, custo_movimento

def a_star(mapa, inicio, destino):
    filas_prioridade = []
    heapq.heappush(filas_prioridade, (0, inicio))
    custo_acumulado = {inicio: 0}
    caminho = {inicio: None}
    visitados = set()

    while filas_prioridade:
        _, ponto_atual = heapq.heappop(filas_prioridade)
        if ponto_atual in visitados:
            continue
        visitados.add(ponto_atual)

        if ponto_atual == destino:
            caminho_final = []
            while ponto_atual:
                caminho_final.append(ponto_atual)
                ponto_atual = caminho[ponto_atual]
            return caminho_final[::-1]

        vizinhos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for movimento in vizinhos:
            vizinho = (ponto_atual[0] + movimento[0], ponto_atual[1] + movimento[1])

            if 0 <= vizinho[0] < len(mapa) and 0 <= vizinho[1] < len(mapa[0]):
                terreno = mapa[vizinho[0]][vizinho[1]]
                
                custo_terreno = custo_movimento(terreno)
                if custo_terreno == float('inf'):
                    continue
                
                novo_custo = custo_acumulado[ponto_atual] + custo_terreno

                if vizinho not in custo_acumulado or novo_custo < custo_acumulado[vizinho]:
                    custo_acumulado[vizinho] = novo_custo
                    prioridade = novo_custo + heuristica(vizinho, destino)
                    heapq.heappush(filas_prioridade, (prioridade, vizinho))
                    caminho[vizinho] = ponto_atual

    return None
