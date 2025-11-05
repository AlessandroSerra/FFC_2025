import matplotlib.pyplot as plt
import numpy as np
import scienceplots  # noqa: F401

plt.style.use(["science", "notebook", "grid"])


def accelerazione(theta1, theta2):
    """
    Calcola le accelerazioni angolari per due pendoli accoppiati.
    """
    alpha1 = -Omega_sq * np.sin(theta1) - (K / M) * (
        np.sin(theta1) - np.sin(theta2)
    ) * np.cos(theta1)
    alpha2 = -Omega_sq * np.sin(theta2) + (K / M) * (
        np.sin(theta1) - np.sin(theta2)
    ) * np.cos(theta2)
    return alpha1, alpha2


def verlet(old_theta1, old_omega1, old_theta2, old_omega2):
    alpha1_old, alpha2_old = accelerazione(old_theta1, old_theta2)

    new_theta1 = old_theta1 + old_omega1 * dT + 0.5 * alpha1_old * dT**2
    new_theta2 = old_theta2 + old_omega2 * dT + 0.5 * alpha2_old * dT**2

    alpha1_new, alpha2_new = accelerazione(new_theta1, new_theta2)

    new_omega1 = old_omega1 + 0.5 * (alpha1_old + alpha1_new) * dT
    new_omega2 = old_omega2 + 0.5 * (alpha2_old + alpha2_new) * dT

    return new_theta1, new_omega1, new_theta2, new_omega2


def get_energy(theta1, omega1, theta2, omega2):
    cinetica = 0.5 * M * (L * omega1) ** 2 + 0.5 * M * (L * omega2) ** 2
    potenziale_grav = -M * G * L * (np.cos(theta1) + np.cos(theta2))
    potenziale_elast = 0.5 * K * (L * (np.sin(theta1) - np.sin(theta2))) ** 2
    potenziale = potenziale_grav + potenziale_elast
    return cinetica, potenziale


G = 9.81  # m/s^2
L = 0.2  # m
M = 0.1  # kg
K = 1.0  # N/m, costante elastica
Omega = np.sqrt(G / L)  # rad/s
Omega_sq = Omega**2  # rad^2/s^2
Periodo = 2 * np.pi / Omega  # s

N_cicli = 10
N_steps = 2000
dT = N_cicli * Periodo / N_steps  # s

Theta1_0 = np.pi / 3  # rad
Omega1_0 = 0  # rad/s
Theta2_0 = 0  # rad
Omega2_0 = 0  # rad/s

theta1_array = np.zeros(N_steps)
omega1_array = np.zeros(N_steps)
theta2_array = np.zeros(N_steps)
omega2_array = np.zeros(N_steps)
cinetica_array = np.zeros(N_steps)
potenziale_array = np.zeros(N_steps)

time_array = np.arange(N_steps) * dT

theta1_array[0] = Theta1_0
omega1_array[0] = Omega1_0
theta2_array[0] = Theta2_0
omega2_array[0] = Omega2_0

cinetica_array[0], potenziale_array[0] = get_energy(
    theta1_array[0], omega1_array[0], theta2_array[0], omega2_array[0]
)

for i in range(1, N_steps):
    (
        theta1_array[i],
        omega1_array[i],
        theta2_array[i],
        omega2_array[i],
    ) = verlet(
        theta1_array[i - 1],
        omega1_array[i - 1],
        theta2_array[i - 1],
        omega2_array[i - 1],
    )

    cinetica_array[i], potenziale_array[i] = get_energy(
        theta1_array[i],
        omega1_array[i],
        theta2_array[i],
        omega2_array[i],
    )


fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(time_array, theta1_array, label="$\\theta_1(t)$", lw=2)
ax.plot(time_array, theta2_array, label="$\\theta_2(t)$", lw=2)
ax.set_xlabel("Time [s]")
ax.set_ylabel("$\\theta [rad]$")
ax.set_title("Posizione in funzione del tempo per due pendoli accoppiati")
ax.legend()
fig.tight_layout()

fig1, ax1 = plt.subplots(figsize=(8, 6))

ax1.plot(time_array, cinetica_array, label="Cinetica")
ax1.plot(time_array, potenziale_array, label="Potenziale")
ax1.plot(time_array, cinetica_array + potenziale_array, label="Etot")
ax1.set_title("Energia cinetica, potenziale e totale in funzione del tempo")
ax1.legend()
fig1.tight_layout()

plt.show()
