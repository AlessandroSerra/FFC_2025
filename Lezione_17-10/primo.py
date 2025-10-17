# vogliamo sapere se un numero e' primo o meno

# chiediamo un numero all'utente ricordandoci che input()
# restituisce una stringa, la convertiamo quindi in intero
numero = int(input("Inserisci un numero:\t"))
flag = True         # inizializziamo la variabile di controllo

# loop da 2 sino alla radice quadrata del numero stesso
# range() ha bisogno di valori interi, quindi convertiamo
for i in range(2, int(numero**(1/2)) + 1):
    if numero % i == 0:
        flag = False
        break           # abbiamo trovato un divisore, usciamo dal loop

if flag:
    print("Il numero e' primo\n")
else:
    print("Il numero non e' primo\n")