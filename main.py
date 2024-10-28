import pygame
import time
import random
from datetime import timedelta
from map.map_loader import carregar_mapa
from map.map_converter import converter_xlsx_para_csv
from a_star.a_star import a_star
from interface.interface import inicializar_interface
from utils.helpers import custo_movimento
import math 

def inicializar_amigos():
    amigos = {
        (5, 13): {"nome": "Suzy", "imagem": "images/avatar1.png"},
        (10, 9): {"nome": "Bete", "imagem": "images/avatar2.png"},
        (6, 35): {"nome": "Mkay", "imagem": "images/avatar3.png"},
        (24, 38): {"nome": "Raquel", "imagem": "images/avatar4.png"},
        (36, 15): {"nome": "Stace", "imagem": "images/avatar5.png"},
        (37, 37): {"nome": "Gabi", "imagem": "images/avatar6.png"},
    }
    
    # Carregar e redimensionar as imagens
    for amigo in amigos.values():
        imagem = pygame.image.load(amigo["imagem"])
        amigo["imagem_carregada"] = pygame.transform.scale(imagem, (10, 15))
    
    return amigos

def desenhar_amigos(tela, amigos, tamanho_celula, amigos_que_aceitaram):
    for posicao, amigo_info in amigos.items():
        # Define a cor de contorno dependendo se o amigo aceitou ou não
        cor_contorno = (0, 255, 0) if posicao in amigos_que_aceitaram else (0, 0, 255)
        
        # Desenha o contorno ao redor da célula
        pygame.draw.rect(
            tela, 
            cor_contorno, 
            (posicao[1] * tamanho_celula, posicao[0] * tamanho_celula, tamanho_celula, tamanho_celula), 
            2
        )
        
        # Pega a imagem carregada e redimensionada do amigo e desenha na posição correta
        tela.blit(
            amigo_info["imagem_carregada"], 
            (posicao[1] * tamanho_celula, posicao[0] * tamanho_celula)
        )

    pygame.display.flip()

def desenhar_caminho(tela, caminho, tamanho_celula, mapa, visitados):
    custo_parcial = 0
    for passo in caminho:
        custo_parcial += custo_movimento(mapa[passo[0]][passo[1]])
        print(f"Custo atual após o passo {passo}: {custo_parcial}")
        
        cor = (255, 0, 255) if passo not in visitados else (128, 0, 5)  
        pygame.draw.circle(
            tela, 
            cor,
            (passo[1] * tamanho_celula + tamanho_celula // 2, passo[0] * tamanho_celula + tamanho_celula // 2), 
            tamanho_celula // 6
        )
        visitados.add(passo)
        
        pygame.display.flip()
        pygame.time.wait(50) 

def desenhar_indices(tela, mapa, tamanho_celula, fonte):
    for j in range(len(mapa[0])):
        if j > 0:  
            texto = fonte.render(f'{j}', True, (255, 255, 255))
            tela.blit(texto, (j * tamanho_celula + tamanho_celula // 2 - texto.get_width() // 2, 5))

    for i in range(len(mapa)):
        if i > 0:  
            texto = fonte.render(f'{i}', True, (255, 255, 255))
            tela.blit(texto, (5, i * tamanho_celula + tamanho_celula // 2 - texto.get_height() // 2))

    pygame.display.flip()

def atualizar_painel(tela, fonte, custo_total, tempo_total):
    
    painel = pygame.Surface((600, 100))
    painel.fill((200, 200, 200))
    tela.blit(painel, (0, 600))

    
    texto_custo = fonte.render(f"Custo total: {custo_total}", True, (0, 0, 0))
    texto_tempo = fonte.render(f"Tempo total: {tempo_total}", True, (0, 0, 0))
    tela.blit(texto_custo, (10, 610))
    tela.blit(texto_tempo, (10, 640))

    
    botao_reiniciar = pygame.Rect(500, 620, 80, 30) 
    pygame.draw.rect(tela, (180, 0, 0), botao_reiniciar)
    texto_reiniciar = fonte.render("Reiniciar", True, (255, 255, 255)) 
    tela.blit(texto_reiniciar, (botao_reiniciar.x + 10, botao_reiniciar.y + 5))

    pygame.display.flip()
    return botao_reiniciar 

def calcular_distancia(ponto1, ponto2):
    """Calcula a distância euclidiana entre dois pontos."""
    return math.sqrt((ponto1[0] - ponto2[0]) ** 2 + (ponto1[1] - ponto2[1]) ** 2)


def main():
    pygame.init()
    fonte = pygame.font.SysFont('Arial', 8)
    fontPanel = pygame.font.SysFont('Arial', 15)

    while True:  
        
        converter_xlsx_para_csv('map/mundo.xlsx', 'map/mapa.csv')
        mapa = carregar_mapa('map/mapa.csv')
        tamanho_celula = 600 // len(mapa)
        tela = inicializar_interface(mapa)

        amigos = inicializar_amigos()
        desenhar_indices(tela, mapa, tamanho_celula, fonte)

        amigos_que_aceitaram = random.sample(list(amigos.keys()), 3)
        print("Amigos que aceitarão o convite:", [amigos[amigo] for amigo in amigos_que_aceitaram])

        desenhar_amigos(tela, amigos, tamanho_celula, amigos_que_aceitaram)

        inicio = (23, 19)
        currentPosition = inicio
        totalPath = []
        totalCust = 0
        visitados = set()
        tempo_total_busca = 0

        # Tempo de busca
        start_tempo_busca = time.time()
        amigos_a_visitar = list(amigos.keys())
        

        while amigos_a_visitar:
            
            amigo_destino = random.choice(amigos_a_visitar)

            start_time = time.time()
            caminho = a_star(mapa, currentPosition, amigo_destino)
            end_time = time.time()
            tempo_total_busca += end_time - start_time

            if caminho:
                desenhar_caminho(tela, caminho, tamanho_celula, mapa, visitados)
                totalPath.extend(caminho)
                totalCust += sum(custo_movimento(mapa[passo[0]][passo[1]]) for passo in caminho)
                currentPosition = amigo_destino

                if amigo_destino in amigos_que_aceitaram:
                    amigos_a_visitar.remove(amigo_destino)

                if len(set(amigo for amigo in amigos_que_aceitaram if amigo in amigos_a_visitar)) == 0:
                    caminho_de_volta = a_star(mapa, currentPosition, inicio)
                    if caminho_de_volta:
                        desenhar_caminho(tela, caminho_de_volta, tamanho_celula, mapa, visitados)
                        totalPath.extend(caminho_de_volta)
                        totalCust += sum(custo_movimento(mapa[passo[0]][passo[1]]) for passo in caminho_de_volta)
                    break

        
        tempo_busca_total = time.time() - start_tempo_busca
        horas_busca, resto_busca = divmod(tempo_busca_total, 3600)
        minutos_busca, segundos_busca = divmod(resto_busca, 60)

        tempo_formatado = f"{int(horas_busca)} horas {int(minutos_busca):02} minutos {int(segundos_busca):02} segundos"
        print(f"Tempo total para encontrar todos os amigos: {tempo_formatado}")
        print(f"Custo total do caminho: {totalCust}")
        botao_reiniciar = atualizar_painel(tela, fontPanel, totalCust, tempo_formatado)


        executando = True
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_reiniciar.collidepoint(evento.pos):
                        executando = False 

if __name__ == "__main__":
    main()
