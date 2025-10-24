import numpy as np
import matplotlib.pyplot as plt

# libreria per rendere i grafici migliori, commentare se non la si ha
# oppure installala con "conda install scienceplots"
import scienceplots
plt.style.use(['science', 'notebook'])


def f(x: np.ndarray[int]) -> np.ndarray[int]:
    return x**4 - 2*x + 1

def trapezoidi(x: np.ndarray[int], y: np.ndarray[int]) -> int:
    h = x[1] - x[0]
    risultato = h/2 * (y[0] + y[-1]) + h * np.sum(y[1:-1]) # [a,b)
    return risultato


def simpson(x: np.ndarray[int], y: np.ndarray[int]) -> int:
    h = x[1] - x[0]
    risultato = h/3 * ((y[0] + y[-1]) + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-1:2]))
    return risultato


# funzione nuova per calcolare l'errore relativo dei due metodi
def calcola_errore(integrale: int, valore_esatto: int) -> int:
    errore_relativo = np.abs((integrale - valore_esatto) / valore_esatto)
    return errore_relativo


A, B = 0.0, 2.0
x_list = [np.linspace(A, B, 10*i+1) for i in range(1, 10)]
y_list = [f(x) for x in x_list]

valore_esatto = 4.4

int_trap_list = []
int_simps_list = []

# liste nuova per contenere gli errori
err_trap_list = []
err_simps_list = []

for i in range(len(x_list)):
    int_trap = trapezoidi(x_list[i], y_list[i])
    int_simps = simpson(x_list[i], y_list[i])

    err_trap = calcola_errore(int_trap, valore_esatto)
    err_simps = calcola_errore(int_simps, valore_esatto)

    int_trap_list.append(int_trap)
    int_simps_list.append(int_simps)

    err_trap_list.append(err_trap)
    err_simps_list.append(err_simps)


# lunghezza di ogni intervallo da plottare assieme ai valori esatti
N_points = [len(element) for element in x_list]

# prima figura che contiene il plot dei due metodi al variare del numero di punti di integrazione
fig, ax = plt.subplots()

ax.plot(N_points, int_trap_list, marker='o', label='Trapezoidi')
ax.plot(N_points, int_simps_list, marker='o', label='Simpson')
ax.axhline(y=valore_esatto, ls='--', label='Valore esatto', color='black')  # linea orizzontale in matplotlib
ax.set_xlabel('Punti')
ax.set_ylabel('Valore Integrale')
ax.legend()
fig.tight_layout()


# seconda figura che contenga gli errori in funzione del numero di punti di integrazione
fig2, ax2 = plt.subplots()

ax2.loglog(N_points, err_trap_list, marker='o', label='errore trapezi')      # grafico log-log
ax2.loglog(N_points, err_simps_list, marker='o', label='errore simpson')      # grafico log-log
ax2.set_xlabel('Punti')
ax2.set_ylabel('Errore')
ax2.legend()
fig2.tight_layout()

plt.show()