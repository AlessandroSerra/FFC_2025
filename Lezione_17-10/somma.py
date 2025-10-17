# inizializziamo una lista per contenere i numeri
lista = []

# ora creiamo un loop per inserire i numeri nella lista, usiamo un loop "infinito"
while True:
    # per ora trattiamo i numeri come stringhe
    numero = input('Inerisci un numero: ')

    # interrompiamo il ciclo quando l'utente schiaccia invio senza inserire nulla
    if numero == '':
        break

    # convertiamo il numero da stringa a intero
    numero = int(numero)

    # aggiungiamo il numero inserito alla lista
    lista.append(numero)

# sommiamo i numeri nella lista con la funzione sum() nativa di Python  
somma = sum(lista)
print(f"La somma della lista {lista} e' {somma}\n")