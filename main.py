from map.map_loader import carregar_mapa, salvar_mapa_como_csv
from map.map_converter import converter_xlsx_para_csv
from a_star.a_star import a_star
from personas.friends import inicializar_amigos, convencer_amigo
from interface.interface import inicializar_interface, atualizar_interface

def main():
    
    converter_xlsx_para_csv('map/mundo.xlsx', 'map/mapa.csv')

    
    mapa = carregar_mapa('map/mapa.csv')
    
    
    tela = inicializar_interface(mapa)
    
    
    amigos = inicializar_amigos()

    
    inicio = (19, 23)

    
    destino = (10, 10)  
    caminho = a_star(mapa, inicio, destino)
    
    
    for passo in caminho:
        atualizar_interface(tela, mapa, passo)

    
    for amigo in amigos:
        convencer_amigo(amigo)

if __name__ == "__main__":
    main()
