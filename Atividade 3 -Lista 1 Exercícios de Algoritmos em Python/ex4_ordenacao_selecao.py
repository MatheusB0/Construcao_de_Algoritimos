import time

def ordenacao_selecao(lista):
    for i in range(len(lista)):
        min_idx = i
        for j in range(i + 1, len(lista)):
            if lista[j] < lista[min_idx]:
                min_idx = j
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
        print(f"Troca {i + 1}: {lista}")
    return lista


if __name__ == "__main__":
    import random

    lista = random.sample(range(1, 200), 10)
    print("Lista original:", lista)

    inicio = time.time()
    ordenacao_selecao(lista)
    fim = time.time()

    print(f"Tempo Seleção: {(fim - inicio):.6f}s")
