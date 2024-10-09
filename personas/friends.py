import random

def inicializar_amigos():
    amigos = {
        (10, 10): "Amigo 1",
        (5, 20): "Amigo 2",
        (30, 15): "Amigo 3",
        (25, 30): "Amigo 4",
        (15, 35): "Amigo 5",
        (8, 12): "Amigo 6",
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
