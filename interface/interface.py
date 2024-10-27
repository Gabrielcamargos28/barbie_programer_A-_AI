import pygame

def inicializar_interface(mapa):
    pygame.init()
    largura_tela = 600
    altura_tela = 700  # 600 para o mapa + 100 para o painel
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    
    # Ajustar o tamanho da célula para preencher toda a largura da tela
    tamanho_celula = largura_tela // len(mapa[0])

    # Desenhar o mapa
    desenhar_mapa(tela, mapa, tamanho_celula)
    
    # Criar e desenhar painel de controle
    painel = pygame.Surface((largura_tela, 100))  # Painel de 600x100 pixels
    painel.fill((200, 200, 200))  # Cor de fundo do painel (cinza claro)
    tela.blit(painel, (0, 585))  # Posiciona o painel abaixo do mapa
    pygame.display.update()
    
    return tela


def desenhar_mapa(tela, mapa, tamanho_celula):
    cores = {
        1: (50, 50, 50),  # Asfalto
        3: (139, 69, 19),  # Terra
        5: (34, 139, 34),  # Grama
        10: (169, 169, 169),  # Paralelepípedo
        -1: (255, 165, 0)  # Edifício
    }
    
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[0])):
            cor = cores.get(mapa[linha][coluna], (0, 0, 0))  # Preto como padrão para valores desconhecidos
            pygame.draw.rect(
                tela, 
                cor, 
                (coluna * tamanho_celula, linha * tamanho_celula, tamanho_celula, tamanho_celula)
            )
    pygame.display.flip()
