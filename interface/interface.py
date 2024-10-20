import pygame

def inicializar_interface(mapa):
    pygame.init()
    largura_tela = 600
    altura_tela = 700
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    
    desenhar_mapa(tela, mapa)
    
    # Criar e desenhar painel de controle
    painel = pygame.Surface((600, 100))  # Painel de 600x100 pixels
    painel.fill((200, 200, 200))  # Cor de fundo do painel
    tela.blit(painel, (0, 600))  # Posiciona o painel abaixo do mapa
    pygame.display.update()
    
    return tela


def desenhar_mapa(tela, mapa):
    cores = {
        1: (50, 50, 50),  # Asfalto
        3: (139, 69, 19),  # Terra
        5: (34, 139, 34),  # Grama
        10: (169, 169, 169),  # Paralelepípedo
        -1: (255, 165, 0)  # Edifício
    }
    tamanho_celula = 600 // len(mapa)
    
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[0])):
            cor = cores.get(mapa[linha][coluna], (0, 0, 0))  # Preto como padrão para valores desconhecidos
            pygame.draw.rect(tela, cor, (coluna * tamanho_celula, linha * tamanho_celula, tamanho_celula, tamanho_celula))
    pygame.display.flip()


# Atualizar o movimento da Barbie
def atualizar_interface(tela, mapa, posicao_barbie):
    desenhar_mapa(tela, mapa)  # Desenha o mapa
    tamanho_celula = 600 // len(mapa)
    pygame.draw.circle(tela, (255, 0, 0), (posicao_barbie[1] * tamanho_celula + tamanho_celula // 2, posicao_barbie[0] * tamanho_celula + tamanho_celula // 2), tamanho_celula // 3)
    pygame.display.flip()
