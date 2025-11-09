def pesquisa_binaria(lista, valor):
    inicio, fim = 0, len(lista) - 1
    comparacoes = 0

    while inicio <= fim:
        comparacoes += 1
        meio = (inicio + fim) // 2
        if lista[meio] == valor:
            return meio, comparacoes
        elif valor < lista[meio]:
            fim = meio - 1
        else:
            inicio = meio + 1

    return -1, comparacoes


if __name__ == "__main__":
    import time

    lista = list(range(1, 101))
    inicio = time.time()
    _, comp_seq = pesquisa_binaria(lista, 100)
    fim = time.time()

    print(f"Comparações: {comp_seq}")
    print(f"Tempo: {(fim - inicio):.10f}s")