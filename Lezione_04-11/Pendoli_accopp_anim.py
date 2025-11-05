import matplotlib.pyplot as plt
import numpy as np
import scienceplots  # noqa: F401
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

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


def simulate(theta1_array, omega1_array, theta2_array, omega2_array):
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

    return theta1_array, omega1_array, theta2_array, omega2_array


G = 9.81  # m/s^2
L = 0.5  # m
M = 0.1  # kg
K = 1.0  # N/m, costante elastica
Omega = np.sqrt(G / L)  # rad/s
Omega_sq = Omega**2  # rad^2/s^2
Periodo = 2 * np.pi / Omega  # s

N_cicli = 20
N_steps = 2000
dT = N_cicli * Periodo / N_steps  # s

Theta1_0 = np.pi / 6  # rad
Omega1_0 = -np.pi / 6  # rad/s
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


theta1_array, omega1_array, theta2_array, omega2_array = simulate(
    theta1_array, omega1_array, theta2_array, omega2_array
)


fig, ax = plt.subplots(figsize=(9, 5))
separation = L * 2  # distanziamo la rappresentazione dei pendoli
ax.set_xlim(-separation, separation)
ax.set_ylim(-L * 1.5, L * 0.5)

# Plot elements
pivot1 = -separation / 2
pivot2 = separation / 2
bob_radius = 0.05 * L
(line1,) = ax.plot([], [], "-", lw=2, c="b")  # asta pendolo 1
(line2,) = ax.plot([], [], "-", lw=2, c="r")  # asta pendolo 2
bob1 = Circle((0, 0), bob_radius, fc="b")       # corpo pendolo 1
bob2 = Circle((0, 0), bob_radius, fc="r")       # corpo pendolo 2
ax.add_patch(bob1)
ax.add_patch(bob2)

(spring,) = ax.plot([], [], "--", lw=1, c="gray")  # Spring as a dashed line
time_template = "time = %.1fs"
time_text = ax.text(0.05, 0.9, "", transform=ax.transAxes, fontsize=14)


def animate(i):
    # Coordinates for the first pendulum bob
    x1 = pivot1 + L * np.sin(theta1_array[i])
    y1 = -L * np.cos(theta1_array[i])

    # Coordinates for the second pendulum bob
    x2 = pivot2 + L * np.sin(theta2_array[i])
    y2 = -L * np.cos(theta2_array[i])

    # Update pendulum lines and bobs
    line1.set_data([pivot1, x1], [0, y1])
    bob1.center = (x1, y1)
    line2.set_data([pivot2, x2], [0, y2])
    bob2.center = (x2, y2)

    # Update spring line
    spring.set_data([x1, x2], [y1, y2])

    time_text.set_text(time_template % (i * dT))
    return line1, line2, bob1, bob2, spring, time_text


ani = FuncAnimation(fig, animate, range(0, N_steps), interval=dT * 1000, blit=True)

fig.tight_layout()
plt.show()
