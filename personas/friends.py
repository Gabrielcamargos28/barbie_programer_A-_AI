import random

def inicializar_amigos():
    amigos = {
        (4, 12): "Amigo 1",
        (9, 8): "Amigo 2",
        (5, 34): "Amigo 3",
        (5, 34): "Amigo 4",
        (23, 37): "Amigo 5",
        (35, 14): "Amigo 6",
        (36, 36): "Barbie",#barbie
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
