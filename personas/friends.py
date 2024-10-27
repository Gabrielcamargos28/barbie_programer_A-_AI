import random

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

def convencer_amigo(amigo):
    sorteio = random.choice([True, False])
    if sorteio:
        print(f"{amigo} aceitou o convite!")
        return True
    else:
        print(f"{amigo} recusou o convite.")
        return False
