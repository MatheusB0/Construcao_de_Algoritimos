import random
from ex6_quicksort import quicksort
from ex2_pesquisa_binaria import pesquisa_binaria
from ex5_recursividade import fatorial, fibonacci

def soma_recursiva(lista):
    return 0 if not lista else lista[0] + soma_recursiva(lista[1:])


lista = random.sample(range(1, 200), 20)
lista_ord = quicksort(lista)

print("Lista:", lista)
print("Ordenada:", lista_ord)
print("Soma recursiva:", soma_recursiva(lista_ord))
print("Busca 100:", pesquisa_binaria(lista_ord, 100)[0])
print("Fatorial maior número:", fatorial(max(lista_ord)))
print("Fibonacci tamanho da lista:", fibonacci(len(lista_ord)))
