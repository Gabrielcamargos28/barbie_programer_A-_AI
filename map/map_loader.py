import csv

def carregar_mapa(caminho_arquivo):
    mapa = []
    with open(caminho_arquivo, newline='') as csvfile:
        leitor = csv.reader(csvfile, delimiter=',')
        for linha in leitor:
            mapa.append([int(celula) for celula in linha]) 
    return mapa

def salvar_mapa_como_csv(mapa, caminho_csv):
    with open(caminho_csv, mode='w', newline='') as csvfile:
        escritor = csv.writer(csvfile)
        for linha in mapa:
            escritor.writerow(linha)
