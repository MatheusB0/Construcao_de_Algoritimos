import random
import time as t
def counter(function,*args):
    v1 = t.perf_counter()
    function(*args)
    v2 = t.perf_counter()
    return v2-v1

def sequencial_search(list,value):
    for i,j in enumerate(list):
        if j == value:
            return i

def binary_search(list,value):
    low = 0
    high = len(list) -1
    while low <= high:
        mid = (low + high) // 2
        shot = list[mid]
        if shot == value:
            return mid
        elif shot > value:
            high = mid -1
        else:
            low = mid +1
    return None

list = sorted(random.sample(range(100),100))
val = list[-1]

tempo = counter(sequencial_search,list,val)
print(f"Sequencial :{tempo:.8f}")
tempo = counter(binary_search,list,val)
print(f"Binário :{tempo:.8f}")
