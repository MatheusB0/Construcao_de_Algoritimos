import random
import time

from ex4_ordenacao_selecao import ordenacao_selecao
from ex6_quicksort import quicksort
from ex2_pesquisa_binaria import pesquisa_binaria
from ex1_pesquisa_sequencial import pesquisa_sequencial

lista = random.sample(range(1, 10001), 1000)

# Ordenações
for nome, func in [
    ("Seleção", ordenacao_selecao),
    ("Quicksort", quicksort),
    ("sorted()", sorted),
]:
    copia = lista.copy()
    inicio = time.time()
    copia = func(copia)
    fim = time.time()
    print(f"{nome}: {(fim - inicio):.6f}s")
