# codice per usare eulero, eulero-cromer e velocity-verlet per un pendolo

import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.style.use(["science", "notebook"])


def accelerazione(theta):
    return -G / L * np.sin(theta)


# metodo di eulero
def eulero(theta_old, omega_old):
    theta_new = theta_old + omega_old * dt
    omega_new = omega_old + accelerazione(theta_old) * dt
    return theta_new, omega_new


# metodo di eulero-cromer
def eulero_cromer(theta_old, omega_old):
    omega_new = omega_old + accelerazione(theta_old) * dt
    theta_new = theta_old + omega_new * dt
    return theta_new, omega_new


# metodo di velocity-verlet
def verlet(theta_old, omega_old):
    theta_new = theta_old + omega_old * dt + 0.5 * accelerazione(theta_old) * dt**2
    omega_new = (
        omega_old + 0.5 * (accelerazione(theta_old) + accelerazione(theta_new)) * dt
    )
    return theta_new, omega_new


def get_energy(theta, omega):
    cinetica = 0.5 * L**2 * omega**2
    potenziale = -G * L * np.cos(theta)
    return cinetica, potenziale


G = 9.81  # m/s^2
L = 0.20  # m
N_steps = 10000
N_cicli = 10

Omega = np.sqrt(G / L)  # rad /s
Periodo = 2 * np.pi / Omega  # s
dt = N_cicli * Periodo / N_steps  # s
Theta0 = np.pi / 3  # rad
Omega0 = 0  # rad / s
Cin0, Pot0 = get_energy(Theta0, Omega0)

theta_array = np.zeros(N_steps)
omega_array = np.zeros(N_steps)
cinetica_array = np.zeros(N_steps)
potenziale_array = np.zeros(N_steps)


theta_array[0] = Theta0
omega_array[0] = Omega0
cinetica_array[0] = Cin0
potenziale_array[0] = Pot0

#NOTE: aggiungiamo una variabile per cambiare facilmente il metodo di integrazione
metodo = eulero_cromer

for i in range(1, N_steps):
    theta_array[i], omega_array[i] = metodo(theta_array[i - 1], omega_array[i - 1])
    cinetica_array[i], potenziale_array[i] = get_energy(theta_array[i], omega_array[i])

time_list = [dt * i for i in range(N_steps)]

meccanica_array = cinetica_array + potenziale_array


fig, ax = plt.subplots()

ax.plot(time_list, theta_array, label="$\\theta$(t)")
ax.axhline(y=Theta0, color="r", linestyle="--")
ax.axhline(y=-Theta0, color="r", linestyle="--")
ax.set_xlabel("t [s]")
ax.set_ylabel("$\\theta$ [rad]")
ax.set_title("Ampiezza in funzione del tempo")
ax.legend()
ax.grid()
fig.tight_layout()


fig1, ax1 = plt.subplots()

ax1.plot(time_list, cinetica_array, label="K")
ax1.plot(time_list, potenziale_array, label="U")
ax1.plot(time_list, meccanica_array, label="E")
ax1.set_xlabel("t [s]")
ax1.set_ylabel("Energia [J]")
ax1.set_title("Energia in funzione del tempo")
ax1.grid()
ax1.legend()

fig1.tight_layout()

plt.show()

