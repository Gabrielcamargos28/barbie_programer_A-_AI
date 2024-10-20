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


def desenhar_caminho(tela, caminho, tamanho_celula, mapa, visitados, painel, font):
    """Desenha o caminho percorrido pela Barbie no mapa e exibe o custo parcial."""
    custo_parcial = 0
    for passo in caminho:
        custo_parcial += custo_movimento(mapa[passo[0]][passo[1]])
        print(f"Custo atual após o passo {passo}: {custo_parcial}")
        
        cor = (128, 128, 128) if passo in visitados else (255, 0, 255)  # Cinza para caminho repetido, rosa para caminho novo        
        pygame.draw.circle(
            tela, 
            cor,  # Rosa para indicar o caminho
            (passo[1] * tamanho_celula + tamanho_celula // 2, passo[0] * tamanho_celula + tamanho_celula // 2), 
            tamanho_celula // 6
        )
        pygame.display.flip()
        
        # Atualizar painel com o custo parcial
        atualizar_painel(painel, custo_parcial, font)
        tela.blit(painel, (0, 600))  # Reposiciona o painel na tela
        pygame.display.update()

        pygame.time.wait(100)  # Atraso para visualizar o desenho do caminho
        
        visitados.add(passo)
    
    return custo_parcial


def atualizar_painel(painel, custo_parcial, font):
    """Atualiza o painel com as estatísticas de custo do caminho."""
    painel.fill((255, 255, 255))  # Fundo branco para o painel
    texto_custo = font.render(f"Custo Total: {custo_parcial}", True, (0, 0, 0))
    painel.blit(texto_custo, (10, 10))
    pygame.display.update()


def main():
    converter_xlsx_para_csv('map/mundo.xlsx', 'map/mapa.csv')
    mapa = carregar_mapa('map/mapa.csv')
    tamanho_celula = 600 // len(mapa)
    tela, painel = inicializar_interface(mapa)
    
    amigos = inicializar_amigos()
    desenhar_amigos(tela, amigos, tamanho_celula)
    
    pygame.font.init()
    font = pygame.font.Font(None, 24)

    inicio = (19, 23)
    currentPosition = inicio
    acceptFriends = 0
    remaningFriends = list(amigos.keys()) 
    totalPath = []
    totalCust = 0
    visitados = set()
    
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
            custo_caminho = desenhar_caminho(tela, caminho, tamanho_celula, mapa, visitados, painel, font)
            totalPath.extend(caminho)
            totalCust += custo_caminho
            currentPosition = amigo_destino

            # Tentar convencer o amigo
            if convencer_amigo(amigos[amigo_destino]):
                acceptFriends += 1
            else:
                print(f"{amigos[amigo_destino]} não aceitou. Indo para o próximo amigo.")
        else:
            print(f"Caminho para {amigos[amigo_destino]} é inválido (custo infinito). Reiniciando a busca.")
            remaningFriends.append(amigo_destino)  # Readição do amigo à lista de amigos restantes
            # Poderia também redefinir currentPosition, se desejado
            currentPosition = inicio  # Exemplo de redefinição (opcional)

    # Retornar à Casa da Barbie após convencer três amigos
    if acceptFriends == 3:
        caminho_de_volta = a_star(mapa, currentPosition, inicio)
        if caminho_de_volta:
            custo_caminho_volta = desenhar_caminho(tela, caminho_de_volta, tamanho_celula, mapa, visitados, painel, font)
            totalPath.extend(caminho_de_volta)
            totalCust += custo_caminho_volta
            print("Barbie retornou à sua casa após convencer três amigos!")

    print(f"Custo total do caminho: {totalCust}")
    
    # Atualizar painel com as informações finais de custo e tempo
    painel.fill((255, 255, 255))
    texto_custo_final = font.render(f"Custo Final: {totalCust}", True, (0, 0, 0))
    texto_tempo_total = font.render(f"Tempo Total: {totalTime:.2f} segundos", True, (0, 0, 0))
    painel.blit(texto_custo_final, (10, 10))
    painel.blit(texto_tempo_total, (10, 40))
    tela.blit(painel, (0, 600))
    pygame.display.update()

    executando = True
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
                
    pygame.quit()


if __name__ == "__main__":
    main()
