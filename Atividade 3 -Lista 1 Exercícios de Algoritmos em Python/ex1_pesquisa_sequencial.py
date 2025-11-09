def pesquisa_sequencial(lista, valor):
    comparacoes = 0
    for i in range(len(lista)):
        comparacoes += 1
        if lista[i] == valor:
            return i, comparacoes
    return -1, comparacoes


if __name__ == "__main__":
    lista = [3, 8, 2, 10, 5, 1, 9, 4, 7, 6]
    indice, comp = pesquisa_sequencial(lista, 10)
    print(f"Resultado: índice={indice}, comparações={comp}")