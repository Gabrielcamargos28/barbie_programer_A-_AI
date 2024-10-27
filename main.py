import time
import random
import pygame
from map.map_loader import carregar_mapa
from map.map_converter import converter_xlsx_para_csv
from a_star.a_star import a_star
from interface.interface import inicializar_interface
from utils.helpers import custo_movimento

def inicializar_amigos():
    amigos = {
        (5, 13): "Amigo 1",
        (10, 9): "Amigo 2",
        (6, 35): "Amigo 3",
        (24, 38): "Amigo 4",
        (36, 15): "Amigo 5",
        (37, 37): "Amigo 6",
    }
    return amigos

def desenhar_amigos(tela, amigos, tamanho_celula, amigos_que_aceitaram):
    for amigo in amigos:
        cor = (0, 255, 0) if amigo in amigos_que_aceitaram else (0, 0, 255)  # Verde para amigos que aceitaram, azul para os outros
        pygame.draw.circle(
            tela, 
            cor,
            (amigo[1] * tamanho_celula + tamanho_celula // 2, amigo[0] * tamanho_celula + tamanho_celula // 2), 
            tamanho_celula // 4
        )
    pygame.display.flip()

def desenhar_caminho(tela, caminho, tamanho_celula, mapa, visitados):
    custo_parcial = 0
    for passo in caminho:
        custo_parcial += custo_movimento(mapa[passo[0]][passo[1]])
        print(f"Custo atual após o passo {passo}: {custo_parcial}")
        
        cor = (255, 0, 255) if passo not in visitados else (128, 128, 128)  # Rosa para novo, cinza para repetido
        pygame.draw.circle(
            tela, 
            cor,
            (passo[1] * tamanho_celula + tamanho_celula // 2, passo[0] * tamanho_celula + tamanho_celula // 2), 
            tamanho_celula // 6
        )
        visitados.add(passo)
        
        pygame.display.flip()
        pygame.time.wait(50)  # Ajuste no tempo de espera

def main():
    # Configuração inicial do mapa
    converter_xlsx_para_csv('map/mundo.xlsx', 'map/mapa.csv')
    mapa = carregar_mapa('map/mapa.csv')
    tamanho_celula = 600 // len(mapa)
    tela = inicializar_interface(mapa)

    amigos = inicializar_amigos()

    # Sorteio dos amigos que aceitarão o convite
    amigos_que_aceitaram = random.sample(list(amigos.keys()), 3)
    print("Amigos que aceitarão o convite:", [amigos[amigo] for amigo in amigos_que_aceitaram])

    desenhar_amigos(tela, amigos, tamanho_celula, amigos_que_aceitaram)

    inicio = (19, 23)  # Posição inicial
    currentPosition = inicio
    totalPath = []
    totalCust = 0
    visitados = set()
    tempo_total = 0
    tempo_caminho = 0  # Variável para armazenar o tempo total do caminho

    # Começando a busca a partir da posição inicial
    amigos_a_visitar = list(amigos.keys())  # Lista de amigos a visitar

    while amigos_a_visitar:
        amigo_destino = random.choice(amigos_a_visitar)  # Seleciona um amigo aleatoriamente

        start_time = time.time()
        caminho = a_star(mapa, currentPosition, amigo_destino)
        end_time = time.time()
        tempo_total += end_time - start_time

        if caminho:
            desenhar_caminho(tela, caminho, tamanho_celula, mapa, visitados)
            totalPath.extend(caminho)
            totalCust += sum(custo_movimento(mapa[passo[0]][passo[1]]) for passo in caminho)
            currentPosition = amigo_destino

            # Verifica se o amigo destino aceitou o convite
            if amigo_destino in amigos_que_aceitaram:
                print(f"{amigos[amigo_destino]} aceitou o convite!")
                amigos_a_visitar.remove(amigo_destino)  # Remove o amigo que aceitou
            else:
                print(f"{amigos[amigo_destino]} não aceitou.")

            # Se já convenceu 3 amigos, volta para a posição inicial
            if len(set(amigo for amigo in amigos_que_aceitaram if amigo in amigos_a_visitar)) == 0:
                caminho_de_volta = a_star(mapa, currentPosition, inicio)
                if caminho_de_volta:
                    desenhar_caminho(tela, caminho_de_volta, tamanho_celula, mapa, visitados)
                    totalPath.extend(caminho_de_volta)
                    totalCust += sum(custo_movimento(mapa[passo[0]][passo[1]]) for passo in caminho_de_volta)
                    print("Barbie retornou à sua casa após convencer três amigos!")
                break

    # Cálculo do tempo total que a Barbie demorou para percorrer todo o caminho
    tempo_caminho = tempo_total  # O tempo total de busca e movimentação
    print(f"Tempo total para encontrar amigos e percorrer todo o caminho: {tempo_caminho:.2f} segundos")
    print(f"Custo total do caminho: {totalCust}")

    executando = True
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

    pygame.quit()

if __name__ == "__main__":
    main()
