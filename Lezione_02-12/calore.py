import numpy as np
import matplotlib.pyplot as plt
import scienceplots
from scipy.optimize import curve_fit
plt.style.use(['science', 'notebook'])

#NOTE: aggiunta per normalizzare la barra colorata del grafico
from matplotlib.colors import Normalize


def initTemps(T0, T1, N_x, N_t):
    T = np.ones((N_t, N_x)) * T0

    A = int(N_x / 3)
    B = int(2*N_x / 3)

    T[0, A:B] = T1

    return T


def boundCond(T_old, T_new, bc):
    if bc == 'd':
        return T_old[0], T_old[-1]
    elif bc == 'n':
        return T_new[1], T_new[-2]
    else:
        raise ValueError("La condizione deve essere di dirichlet (d) oppure neumann (n)")


def stepFTCS(T_old, N_x, dt, k, h, bc):

    T_new = T_old.copy()

    for i in range(1, N_x - 1):
        T_new[i] = T_old[i] + dt * k / h**2 * (T_old[i-1] + T_old[i+1] - 2*T_old[i])

    T_new[0], T_new[-1] = boundCond(T_old, T_new, bc)
    return T_new


def Solve(T0, T1, N_x, N_t, dt, k, h, bc):

    T = initTemps(T0, T1, N_x, N_t)

    for i in range(1, N_t):
        T[i] = stepFTCS(T[i-1], N_x, dt, k, h, bc)

    return T


def fitAmps(T, N_t, dt):
    def esponenziale(t, A, B, C):
        return A*np.exp(-t / B) + C
    
    # T ha dimensioni (N_t, N_x), axis=0 indica la prima dimensione (N_t) mentre axis=1 la seconda (N_x)
    max_Ts = np.max(T, axis=1)
    times = np.arange(N_t) * dt

    #HACK: curve_fit NON riesce a convergere senza guess iniziali. Abbiamo:
    # 1. A rappresenta il valore di T quando exp=1, quindi il valore massimo;
    # 2. B rappresenta il tempo medio di vita, supponiamo che sia simile alla metà del tempo totale di simulazione;
    # 3. C rappresenta il valore di T quando exp->0, quindi il valore minimo.
    popt, pcov = curve_fit(esponenziale, times, max_Ts, p0=[np.max(max_Ts), (N_t // 2)*dt, np.min(max_Ts)])
    y_fit = esponenziale(times, *popt)
    errs = np.sqrt(np.diag(pcov))

    return max_Ts, y_fit, errs



########################
# costanti & parametri #
########################

L = 1       # m
k = 1       # m**2/s
h = 0.01    # m
dt = 0.5 * h**2 / (2 * k)   # s

N_x = int(L / h) + 1
N_t = 11000     # più carino per la barra del grafico rispetto a 10000

x = np.arange(N_x) * h
times = np.arange(N_t) * dt

T0 = 300    # K
T1 = 350    # K

T = Solve(T0, T1, N_x, N_t, dt, k, h, bc='n')

max_Ts, y_fit, errs = fitAmps(T, N_t, dt)


fig, axs = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

ax = axs[0]
ax.scatter(times, max_Ts, s=2, label="Ampiezze")
ax.plot(times, y_fit, label="Fit", color="red")
ax.set_xlabel("t [s]")
ax.set_ylabel("T [K]")
ax.set_title("Fit del Decadimento delle Ampiezze")
ax.legend()


ax = axs[1]

#NOTE: blocco per definire la barra di colori
# trovate altre palette qua:
# https://matplotlib.org/stable/users/explain/colors/colormaps.html
#-----------------------------------------------
cmap = plt.get_cmap("inferno_r")
norm = Normalize(0, (N_t - 1) * dt)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
#-----------------------------------------------

for i in range(0, N_t, N_t // 10):
    ax.plot(T[i], color=cmap(norm(i * dt)))     # usiamo la mappa di colori

fig.colorbar(sm, ax=ax, label="Time [s]")       # aggiungiamo la mappa di colori alla figura
ax.set_xlabel("x [m]")
ax.set_title("Evoluzione dei Profili nel Tempo")

fig.tight_layout()
plt.show()