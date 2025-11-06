import random
import time as t


def ordenacao_selecao(lista):
    for i in range(len(lista)):
        min_index = i
        for j in range(i+1, len(lista)):
            if lista[j] < lista[min_index]:
                min_index = j
        lista[i], lista[min_index] = lista[min_index], lista[i]
    return lista


def quicksort(lista):
    if len(lista) <= 1:
        return lista
    pivo = lista[len(lista) // 2]
    menores = [x for x in lista if x < pivo]
    iguais  = [x for x in lista if x == pivo]
    maiores = [x for x in lista if x > pivo]
    return quicksort(menores) + iguais + quicksort(maiores)


lista = random.sample(range(10000), 1000)

# Selection sort
copia1 = lista[:]
t1 = t.perf_counter()
ordenacao_selecao(copia1)
t1 = t.perf_counter() - t1

# Quicksort
copia2 = lista[:]
t2 = t.perf_counter()
quicksort(copia2)
t2 = t.perf_counter() - t2

# Sorted()
t3 = t.perf_counter()
sorted(lista)
t3 = t.perf_counter() - t3

print(f"Seleção  : {t1:.6f} s")
print(f"Quicksort: {t2:.6f} s")
print(f"sorted() : {t3:.6f} s")
