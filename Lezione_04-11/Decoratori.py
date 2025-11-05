import time
from numba import njit

def timer(funzione):
    def wrapper(*args, **kwargs):
        inizio = time.time()
        risultato = funzione(*args, **kwargs)
        fine = time.time()
        print(f'Tempo di esecuzione {fine - inizio} secondi')
        return risultato
    return wrapper

# @timer
@njit
def somma_quadrati(n):
    s = 0
    for i in range(n):
        s = s + i**2
    
    return s

inizio = time.time()
somma_quadrati(100_000_000)
fine = time.time()

print(fine - inizio)