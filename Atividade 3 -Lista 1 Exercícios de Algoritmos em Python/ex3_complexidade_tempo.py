import time

def pesquisa_sequencial(lista, valor):
    for i, v in enumerate(lista):
        if v == valor:
            return i
    return -1

def pesquisa_binaria(lista, valor):
    inicio, fim = 0, len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista[meio] == valor:
            return meio
        elif valor < lista[meio]:
            fim = meio - 1
        else:
            inicio = meio + 1
    return -1


for tamanho in [10_000, 100_000, 1_000_000]:
    lista = list(range(tamanho))

    t1 = time.time()
    pesquisa_sequencial(lista, tamanho - 1)
    t2 = time.time()

    t3 = time.time()
    pesquisa_binaria(lista, tamanho - 1)
    t4 = time.time()

    print(f"\nTamanho: {tamanho}")
    print(f"Sequencial: {(t2 - t1):.6f}s")
    print(f"Binária:    {(t4 - t3):.6f}s")
