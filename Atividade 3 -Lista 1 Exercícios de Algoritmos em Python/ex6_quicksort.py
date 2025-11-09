def quicksort(lista):
    if len(lista) <= 1:
        return lista
    pivo = lista[len(lista)//2]
    menores = [x for x in lista if x < pivo]
    iguais = [x for x in lista if x == pivo]
    maiores = [x for x in lista if x > pivo]
    return quicksort(menores) + iguais + quicksort(maiores)


if __name__ == "__main__":
    import random, time

    lista = random.sample(range(1, 20000), 10000)

    inicio = time.time()
    quicksort(lista)
    fim = time.time()

    print(f"Tempo Quicksort: {(fim - inicio):.6f}s")
