import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import scienceplots

plt.style.use(["science", "notebook", "grid"])

def acceleration(theta):
    return -G / L * np.sin(theta)


def eulero(theta, vel):
    new_theta = theta + vel * Tau
    new_vel = vel + acceleration(theta) * Tau

    return new_theta, new_vel


def eulero_cromer(theta, vel):
    new_vel = vel + acceleration(theta) * Tau
    new_theta = theta + new_vel * Tau

    return new_theta, new_vel


def verlet(theta, vel):
    new_theta = theta + vel * Tau + 0.5 * acceleration(theta) * Tau**2
    new_vel = vel + 0.5 * (acceleration(new_theta) + acceleration(theta)) * Tau

    return new_theta, new_vel


def get_energy(theta, vel):
    cinetica = 0.5 * L**2 * vel**2
    potenziale = -G * L * np.cos(theta)

    return cinetica, potenziale


def simulate(method=verlet):
    theta_array, vel_array = np.zeros(N_steps), np.zeros(N_steps)
    k_array, pot_array = np.zeros(N_steps), np.zeros(N_steps)
    time_array = np.zeros(N_steps)

    theta_array[0] = Theta0
    vel_array[0] = Vel0
    time_array[0] = 0

    k_array[0], pot_array[0] = get_energy(theta_array[0], vel_array[0])

    for i in range(N_steps - 1):
        theta_array[i + 1], vel_array[i + 1] = method(theta_array[i], vel_array[i])
        k_array[i + 1], pot_array[i + 1] = get_energy(
            theta_array[i + 1], vel_array[i + 1]
        )
        time_array[i + 1] = time_array[i] + Tau

    return theta_array, vel_array, k_array, pot_array, time_array


G = 9.81
L = 0.2
N_steps = 1000
Ncycles = 10

omega = np.sqrt(G / L)
Period = 2 * np.pi / omega
Time = Ncycles * Period
Tau = Time / N_steps

Theta0 = 1 * np.pi / 6
Vel0 = 0


theta_array, vel_array, k_array, pot_array, time = simulate(eulero)



# funzione di animazione
def animate(i):
    palla.set_offsets(np.column_stack([theta_array[i], L]))
    sbarra.set_data([theta_array[i], theta_array[i]], [0, L])


# creiamo figura ed assi, per una migliore visualizzazione degli angoli
# scegliamo un grafico in coordinate polari invece che cartesiane
fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={"projection": "polar"})


(sbarra,) = ax.plot([0, 0], [0, L], color="red", linewidth=2)
palla = ax.scatter(theta_array[0], L, s=100)

# ruotiamo il grafico in modo che l'angolo 0 sia in bbasso e non a destra
ax.set_theta_offset(np.deg2rad(-90))
ax.set_rlim([0, L + 0.2 * L])

# eliminiamo i ticks per il raggio
ax.set_rticks([])
ax.set_title("Animazione Pendolo", fontsize=18)
anim = FuncAnimation(
    fig, animate, frames=len(theta_array), interval=30, repeat=False
)

fig.tight_layout()
plt.show()
