import time
from map.map_loader import carregar_mapa, salvar_mapa_como_csv
from map.map_converter import converter_xlsx_para_csv
from a_star.a_star import a_star
from personas.friends import inicializar_amigos, convencer_amigo
from interface.interface import inicializar_interface
import pygame
from utils.helpers import heuristica, custo_movimento




def desenhar_amigos(tela, amigos, tamanho_celula):
    """Desenha a posição dos amigos no mapa."""
    for amigo in amigos:
        pygame.draw.circle(
            tela, 
            (0, 0, 255),  # Azul para representar os amigos
            (amigo[1] * tamanho_celula + tamanho_celula // 2, amigo[0] * tamanho_celula + tamanho_celula // 2), 
            tamanho_celula // 4
        )
    pygame.display.flip()


def desenhar_caminho(tela, caminho, tamanho_celula, mapa, visitados):
    """Desenha o caminho percorrido pela Barbie no mapa e exibe o custo parcial."""
    custo_parcial = 0
    for passo in caminho:
        custo_parcial += custo_movimento(mapa[passo[0]][passo[1]])
        print(f"Custo atual após o passo {passo}: {custo_parcial}")
        
        # Desenhar o caminho novo
        if passo not in visitados:
            pygame.draw.circle(
                tela, 
                (255, 0, 255),  # Rosa para indicar o novo caminho
                (passo[1] * tamanho_celula + tamanho_celula // 2, passo[0] * tamanho_celula + tamanho_celula // 2), 
                tamanho_celula // 6
            )
            visitados.add(passo)  # Adiciona o passo aos visitados
        else:
            # Desenhar o caminho repetido
            pygame.draw.circle(
                tela, 
                (128, 128, 128),  # Cinza para o caminho repetido
                (passo[1] * tamanho_celula + tamanho_celula // 2, passo[0] * tamanho_celula + tamanho_celula // 2), 
                tamanho_celula // 6
            )
        
        pygame.display.flip()
        pygame.time.wait(100)
        
        
        
def calcular_menor_rota(amigos, posicao_inicial, mapa):
    """Calcula a rota de menor custo para visitar todos os amigos."""
    caminho_otimizado = []
    amigos_a_visitar = list(amigos.keys())
    posicao_atual = posicao_inicial

    while amigos_a_visitar:
        menor_caminho = None
        amigo_selecionado = None
        menor_custo = float('inf')

        for amigo in amigos_a_visitar:
            caminho = a_star(mapa, posicao_atual, amigo)
            custo_caminho = sum(custo_movimento(mapa[passo[0]][passo[1]]) for passo in caminho)
            
            if custo_caminho < menor_custo:
                menor_custo = custo_caminho
                menor_caminho = caminho
                amigo_selecionado = amigo

        caminho_otimizado.extend(menor_caminho)
        posicao_atual = amigo_selecionado
        amigos_a_visitar.remove(amigo_selecionado)

    return caminho_otimizado



def main():
    converter_xlsx_para_csv('map/mundo.xlsx', 'map/mapa.csv')
    mapa = carregar_mapa('map/mapa.csv')
    tamanho_celula = 600 // len(mapa)
    tela = inicializar_interface(mapa)
    
    amigos = inicializar_amigos()
    desenhar_amigos(tela, amigos, tamanho_celula)

    inicio = (23, 19)
    currentPosition = inicio
    acceptFriends = 0
    remaningFriends = list(amigos.keys()) 
    totalPath = []
    totalCust = 0
    visitados = set()
    amigos_aceitos = []
    
    caminho_otimizado = calcular_menor_rota(amigos, currentPosition, mapa)
    
    while acceptFriends < 3 and remaningFriends:
        # Escolher um amigo para visitar
        amigo_destino = remaningFriends.pop(0)
        start_time = time.time()
        caminho = a_star(mapa, currentPosition, amigo_destino)
        end_time = time.time()
        totalTime = end_time - start_time

        # Desenhar o caminho até o amigo e atualizar o mapa
        if caminho:
            print(f"Tempo para encontrar {amigos[amigo_destino]}: {totalTime:.2f} segundos")
            desenhar_caminho(tela, caminho, tamanho_celula, mapa, visitados)
            totalPath.extend(caminho)
            totalCust += sum(custo_movimento(mapa[passo[0]][passo[1]]) for passo in caminho)
            currentPosition = amigo_destino

            # Tentar convencer o amigo
            if convencer_amigo(amigos[amigo_destino]):
                acceptFriends += 1
                amigos_aceitos.append((amigos[amigo_destino], amigo_destino))  # Adiciona (nome, posição)
            else:
                print(f"{amigos[amigo_destino]} não aceitou. Indo para o próximo amigo.")
                
                

    # Retornar à Casa da Barbie após convencer três amigos
    if acceptFriends == 3:
        caminho_de_volta = a_star(mapa, currentPosition, inicio)
        if caminho_de_volta:
            desenhar_caminho(tela, caminho_de_volta, tamanho_celula, mapa, visitados)
            totalPath.extend(caminho_de_volta)
            totalCust += sum(custo_movimento(mapa[passo[0]][passo[1]]) for passo in caminho_de_volta)
            print("Barbie retornou à sua casa após convencer três amigos!")

    print(f"Custo total do caminho: {totalCust}")
    print(f"Posições dos amigos que aceitaram: {amigos_aceitos}")
    for nome, posicao in amigos_aceitos:
        print(f"{nome} na posição {list(posicao)}")  # Exibe a posição no formato [linha, coluna]


    executando = True
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
                
    pygame.quit()


if __name__ == "__main__":
    main()