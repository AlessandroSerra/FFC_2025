import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import epsilon_0   # costante dielettrica del vuoto
from numba import njit
import scienceplots
plt.style.use(['science', 'notebook'])

def initGrid(q, grid_size, h):
    V = np.zeros((grid_size, grid_size))
    rho = np.zeros((grid_size, grid_size))

    center = grid_size // 2     # indice della cella centrale nel piano 2D
    rho[center, center] = q / (h**2)    # C / m**2
    source = - rho / epsilon_0

    return V, source

@njit(cache=True, fastmath=True)
def step_jacobi(grid_size, h, V_old, source):
    V_new = V_old.copy()    # V_old e V_new sono due array ben distinti

    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            V_new[i, j] = 0.25 * (
                                V_old[i+1, j] +
                                V_old[i-1, j] + 
                                V_old[i, j+1] +
                                V_old[i, j-1] -
                                h**2 * source[i, j]
                            )

    return V_new


@njit(cache=True, fastmath=True)
def step_gs(grid_size, h, V, source):

    # niente divisione V_old e V_new, sfruttiamo il fatto che
    # V[i-1,j] e V[i,j-1] siano già aggiornati allo step (i,j)
    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            V[i, j] = 0.25 * (
                                V[i+1, j] +
                                V[i-1, j] + 
                                V[i, j+1] +
                                V[i, j-1] -
                                h**2 * source[i, j]
                            )

    return V


@njit(cache=True, fastmath=True)
def step_sor(grid_size, h, V, source, omega):

    # niente divisione V_old e V_new, sfruttiamo il fatto che
    # V[i-1,j] e V[i,j-1] siano già aggiornati allo step (i,j)
    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            V_GS = 0.25 * (
                                V[i+1, j] +
                                V[i-1, j] + 
                                V[i, j+1] +
                                V[i, j-1] -
                                h**2 * source[i, j]
                            )
            
            # applichiamo la correzione SOR a Gauss-Seidel
            V[i, j] = (1 - omega) * V[i, j] + omega * V_GS

    return V



def Solve(parametri):
    grid_size = parametri["grid_size"]
    h = parametri["h"]
    tolerance = parametri["tolerance"]
    max_iter = parametri["max_iter"]
    q = parametri["q"]
    omega = parametri["omega"]

    V, source = initGrid(q, grid_size, h)

    for iter in range(max_iter):
        V_old = V.copy()

        # V = step_jacobi(grid_size, h, V_old, source)
        # V = step_gs(grid_size, h, V, source)
        V = step_sor(grid_size, h, V, source, omega)


        diff = np.abs(V - V_old)
        max_diff = np.max(diff)

        if max_diff < tolerance:
            print(f'Convergenza raggiunta in {iter + 1} iterazioni\n')
            break
    
    # blocco else entra solo se il for finisce senza essere interrotto
    else:
        print(f'Numero massimo di iterazioni raggiunto. Differenza {max_diff:.2e} V')

    return V



#-----------------------
#       MAIN
#-----------------------
parametri = {
    "q": 1e-9,      # C
    "grid_size": 101,   #
    "tolerance": 1e-5,
    "max_iter": 10000,
    "L": 1.0,      # m
    "omega": 1.5    # 0 < omega < 2
}
parametri["h"] = parametri["L"] / (parametri["grid_size"] - 1)

V = Solve(parametri)

x = np.linspace(0, parametri["L"], parametri["grid_size"])
y = np.linspace(0, parametri["L"], parametri["grid_size"])
X, Y = np.meshgrid(x, y)

fig = plt.figure(figsize=(14, 6))

ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax1.plot_surface(X, Y, V, cmap="viridis")
ax1.set_xlabel("X [m]")
ax1.set_ylabel("Y [m]")
ax1.set_zlabel("Potenziale [V]")

ax2 = fig.add_subplot(1, 2, 2)
contour = ax2.contourf(X, Y, V, 30, cmap="viridis")
fig.colorbar(contour, ax=ax2, label="Potenziale [V]")   # barra di colore, mi sono dimenticato di metterla prima
ax2.set_xlabel("X [m]")
ax2.set_ylabel("Y [m]")
ax2.set_aspect("equal")

fig.tight_layout()
plt.show()