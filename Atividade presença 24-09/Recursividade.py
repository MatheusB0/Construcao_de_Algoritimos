
def fatorial(n):
    if n <= 1:
        return 1
    return n * fatorial(n - 1)


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def soma_lista(lista):
    if not lista:
        return 0
    return lista[0] + soma_lista(lista[1:])


print(f"Fatorial(5): {fatorial(5)}")
print(f"Fibonacci(7): {fibonacci(7)}")
print(f"Soma [1,2,3,4]: {soma_lista([1,2,3,4])}")
