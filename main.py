import time
from map.map_loader import carregar_mapa, salvar_mapa_como_csv
from map.map_converter import converter_xlsx_para_csv
from a_star.a_star import a_star
from personas.friends import inicializar_amigos, convencer_amigo
from interface.interface import inicializar_interface, atualizar_interface
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


def desenhar_caminho(tela, caminho, tamanho_celula):
    """Desenha o caminho percorrido pela Barbie no mapa."""
    for passo in caminho:
        pygame.draw.circle(
            tela, 
            (255, 0, 255),  # Rosa para indicar o caminho
            (passo[1] * tamanho_celula + tamanho_celula // 2, passo[0] * tamanho_celula + tamanho_celula // 2), 
            tamanho_celula // 6
        )
        pygame.display.flip()
        pygame.time.wait(100)  # Atraso para visualizar o desenho do caminho


def main():
    
    converter_xlsx_para_csv('map/mundo.xlsx', 'map/mapa.csv')

    
    mapa = carregar_mapa('map/mapa.csv')
    
    tamanho_celula = 600 // len(mapa)
    
    tela = inicializar_interface(mapa)
    
    
    amigos = inicializar_amigos()
    
    desenhar_amigos(tela, amigos, tamanho_celula)

    
    inicio = (19, 23)
    currentPosition = inicio
    acceptFriends = 0
    remaningFriends = list(amigos.keys()) 
    totalPath = []
    totalCust = 0
    
    
    
    #destino = (10, 10)  
    #caminho = a_star(mapa, inicio, destino)
    
    
    #for passo in caminho:
    #    atualizar_interface(tela, mapa, passo)

    
    #for amigo in amigos:
     #   convencer_amigo(amigo)
        
    
    #desenhar_caminho(tela, caminho, tamanho_celula)
    
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
            desenhar_caminho(tela, caminho, tamanho_celula)
            totalPath.extend(caminho)
            totalCust += sum(custo_movimento(mapa[passo[0]][passo[1]]) for passo in caminho)
            currentPosition = amigo_destino

            # Tentar convencer o amigo
            if convencer_amigo(amigos[amigo_destino]):
                acceptFriends += 1
            else:
                print(f"{amigos[amigo_destino]} não aceitou. Indo para o próximo amigo.")

    # Retornar à Casa da Barbie após convencer três amigos
    if acceptFriends == 3:
        caminho_de_volta = a_star(mapa, currentPosition, inicio)
        if caminho_de_volta:
            desenhar_caminho(tela, caminho_de_volta, tamanho_celula)
            totalPath.extend(caminho_de_volta)
            totalCust += sum(custo_movimento(mapa[passo[0]][passo[1]]) for passo in caminho_de_volta)
            print("Barbie retornou à sua casa após convencer três amigos!")

    print(f"Custo total do caminho: {totalCust}")

    
    
        
        
        
    executando = True
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
                
    pygame.quit()


if __name__ == "__main__":
    main()
