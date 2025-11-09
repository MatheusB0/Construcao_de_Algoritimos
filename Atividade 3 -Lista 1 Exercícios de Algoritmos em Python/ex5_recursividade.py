def fatorial(n):
    return 1 if n <= 1 else n * fatorial(n - 1)

def fibonacci(n):
    return n if n <= 1 else fibonacci(n - 1) + fibonacci(n - 2)

def soma_acumulada(n):
    return 0 if n == 0 else n + soma_acumulada(n - 1)

if __name__ == "__main__":
    print("Fatorial 0..6:", [fatorial(i) for i in range(7)])
    print("Fibonacci:", fibonacci(10))
    print("Soma acumulada 10:", soma_acumulada(10))