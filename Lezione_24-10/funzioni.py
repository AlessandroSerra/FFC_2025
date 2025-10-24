

def saluta(nome):
    print(f"Ciao {nome}")


def sottrazione(a, b):
    return a - b


def somma(*numeri):
    return sum(numeri)


def funzione_a_caso(*args, **kwargs):
    print(f'{args=}, {kwargs=}')


# type hinting
def funzione_incasinata(a: int) -> int:
    """questa funzione restituisce il doppio del valore in input"""
    return a*2



def tempo_caduta(h: int, g: int = 9.81) -> int:

    return (2 * h / g) ** 0.5




funzione_a_caso(1, 2, 4, 5, pippo='pippo', a='ciaone')