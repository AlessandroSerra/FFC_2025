eV_to_AMU_A2_FS2 = 0.009648533202185007
AMU_A2_FS2_to_eV = 1 / eV_to_AMU_A2_FS2

"""
rij = rij - L * np.round(rij / L)
L = 10
r = 9
r / L = 0.9
np.round(r / L) = 1
rij = 9 - 10 * 1 = -1
"""

"""
r = L % r
L = 10
r = 11
r % L = 1
"""

"""
usiamo il decoratore @njit Numba per velocizzare le funzioni più pesanti con:

- fastmath=True: abilita ottimizzazioni matematiche
- cache=True: memorizza le versioni compilate delle funzioni per riutilizzarle

ATTENZIONE: funziona solo se la funzione contiene loop, if o elementi di Numpy
"""

import matplotlib.pyplot as plt
import numpy as np
from numba import njit
from scipy.optimize import curve_fit    # importiamo la funzione di scipy per il fit
from matplotlib.animation import FuncAnimation  # importiamo la funzione per l'animazione
import scienceplots     # grafici carini
plt.style.use(['science', 'notebook'])


def init_parts(parametri):
    N_parts = parametri["N_parts"]
    L_box = parametri["L_box"]
    Temp = parametri["Temp"]
    mass = parametri["mass"]
    min_dist = parametri["min_dist"]

    min_dist_sq = min_dist**2
    pos = np.zeros((N_parts, 1))

    for i in range(N_parts):
        while True:
            trial_pos = np.random.rand(1) * L_box
            is_far_enough = True

            # NOTE: qua da cambiare N_parts -> i nel loop (eliminiamo check inutili)
            for j in range(i):
                r_ij = trial_pos - pos[j]
                r_ij = r_ij - L_box * np.round(r_ij / L_box)    # convenzione di minima immagine
                r_ij_sq = r_ij**2

                if r_ij_sq < min_dist_sq:
                    is_far_enough = False
                    break

            if is_far_enough:
                pos[i] = trial_pos
                break

    K_B_eV = 8.617333262e-5     # eV/K
    k_B_T_m = (K_B_eV * Temp / mass) * eV_to_AMU_A2_FS2  # v^2
    varianza = k_B_T_m
    dev_std = np.sqrt(varianza)

    vel = np.random.normal(loc=0.0, scale=dev_std, size=(N_parts, 1))
    vel -= np.mean(vel, axis=0)  # eliminiamo velocità del centro di massa

    return pos, vel


@njit(fastmath=True, cache=True)
def lj_force(pos, N_parts, sigma, epsilon, L_box, cutoff):
    # pos: array contenente le posizioni delle particelle
    # pos[i] posizione dell'i-esima particella

    f = np.zeros((N_parts, 1))
    potential = 0.0
    cutoff_sq = cutoff**2

    for i in range(N_parts - 1):
        for j in range(i + 1, N_parts):
            # vettore posizione & modulo quadro
            r_ij = pos[i] - pos[j]
            r_ij = r_ij - L_box * np.round(r_ij / L_box)    # convenzione di minima immagine
            r_ij_sq = np.dot(r_ij, r_ij)

            if r_ij_sq == 0 or r_ij_sq > cutoff_sq:     # forze restano zero se distanza > cutoff
                continue

            # quantita' LJ
            sigma_sq_r_ij_sq = sigma**2 / r_ij_sq  # (sigma / 2)^2
            term12 = sigma_sq_r_ij_sq**6
            term6 = sigma_sq_r_ij_sq**3

            f_lj = (24 * epsilon * (2 * term12 - term6) / r_ij_sq) * r_ij  # forza LJ
            potential += 4 * epsilon * (term12 - term6)     # sommiamo energia potenziale

            f[i] += f_lj  # sommiamo la forza a quella gia' esistente
            f[j] -= f_lj  # sommiamo (segno opposto) la forza a quella gia' esistente

    return f, potential


@njit(fastmath=True, cache=True)
def step_md(pos, vel, dt, N_parts, sigma, epsilon, L_box, m, cutoff):
    # pos_{i+1} = pos_{i} + vel_{i}*dt + 1/2 a_{i}dt^2
    # vel_{i+1} = vel_{i} + 1/2(a_{i} + a_{i+1})dt

    f, potential = lj_force(pos, N_parts, sigma, epsilon, L_box, cutoff)
    acc = (f / m) * eV_to_AMU_A2_FS2
    pos_new = pos + vel * dt + 0.5 * acc * dt**2
    pos_new = pos_new % L_box

    f_new, _ = lj_force(pos_new, N_parts, sigma, epsilon, L_box, cutoff)
    #NOTE: avevo scritto male la costante: AMU_A2_FS2_to_eV -> eV_to_AMU_A2_FS2
    acc_new = (f_new / m) * eV_to_AMU_A2_FS2
    vel_new = vel + 0.5 * (acc + acc_new) * dt

    return pos_new, vel_new, potential


@njit(fastmath=True, cache=True)
def kinetic_energy(vel, m):
    return 0.5 * m * np.sum(vel**2) * AMU_A2_FS2_to_eV


def run_md(parametri):
    dt, N_steps, N_parts = parametri["dt"], parametri["N_steps"], parametri["N_parts"]
    sigma, epsilon, L_box, mass = (
        parametri["sigma"],
        parametri["epsilon"],
        parametri["L_box"],
        parametri["mass"],
    )
    cutoff = parametri["cutoff"]

    pos = np.zeros((N_steps, N_parts, 1))
    vel = np.zeros((N_steps, N_parts, 1))
    pos[0], vel[0] = init_parts(parametri)

    E_pot = np.zeros(N_steps)
    E_kin = np.zeros(N_steps)
    E_kin[0] = kinetic_energy(vel[0], mass)     # riempiamo a mano il primo valore di K
    _, E_pot[0] = lj_force(pos[0], N_parts, sigma, epsilon, L_box, cutoff)  # lo stesso per U

    for step in range(1, N_steps):
        pos[step], vel[step], E_pot[step] = step_md(
            pos[step - 1],
            vel[step - 1],
            dt,
            N_parts,
            sigma,
            epsilon,
            L_box,
            mass,
            cutoff,
        )

        E_kin[step] = kinetic_energy(vel[step], mass)

    E_total = E_pot + E_kin

    return pos, vel, E_pot, E_kin, E_total


#NOTE: funzione per fittare le velocità rispetto alla Maxwell-Boltzmann
def fit_maxwell_boltzmann(vel, params, K_last):

    def maxwell_boltzmann_1d(v, T):

        kT =  K_B_eV / AMU_A2_FS2_to_eV * T
        prefactor = np.sqrt(2 * m / (np.pi * kT))
        return prefactor * np.exp(-m * v**2 / (2 * kT))

    m = params["mass"]
    N_parts = params["N_parts"]
    K_B_eV = 8.617333262e-5    # eV/K

    # prendiamo solo l'ultimo 20% delle velocità in modo che siano a convergenza e con poco rumore
    last_vel = vel[(len(vel) // 5):, :, :]
    # qui sotto prima calcoliamo il modulo quadro delle velocità (np.linalg.norm)
    # e poi rendiamo tutto un array piatto 1D con .flatten()
    last_vel_mag = np.linalg.norm(last_vel, axis=2).flatten()

    # usiamo la media degli ultimi valori di K per stimare la temperatura iniziale del fit
    T_last = (2 * K_last) / (N_parts * K_B_eV)
    T_guess = np.mean(T_last)

    # Istogramma normalizzato per le velocità
    hist, bin_edges = np.histogram(last_vel_mag, bins=20, density=True)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # fit di T
    popt, pcov = curve_fit(maxwell_boltzmann_1d, bin_centers, hist, p0=[T_guess])
    T_fit = popt[0]     # valore fittato della temperatura
    errs_fit = np.sqrt(np.diag(pcov))   # errori del fit
    err_T_fit = errs_fit[0]     # errore del fit sul valore di temperatura

    # curva liscia da plottare
    v_grid = np.linspace(0, np.max(last_vel_mag), 500)  # creiamo un asse delle x
    f_fit = maxwell_boltzmann_1d(v_grid, T_fit)     # calcoliamo i valori delle y_fit

    return T_fit, err_T_fit, last_vel_mag, v_grid, f_fit



# -----------------
#       MAIN
# -----------------

parametri = {
    "sigma": 3.405,  # Angstrom
    "epsilon": 0.01032,  # eV
    "mass": 39.948,  # uma
    "L_box": 500.0,  # Å
    "dt": 1.0,  # fs
    "Temp": 120,  # K
    "N_steps": 10000,
    "N_parts": 50,
}
parametri["min_dist"] = parametri["sigma"]
parametri["cutoff"] = 2.5 * parametri["sigma"]

#NOTE: avevo invertito l'ordine di U e K
pos, vel, U, K, Etot = run_md(parametri)

T_fit, err_T_fit, last_vel_mag, v_grid, f_fit = fit_maxwell_boltzmann(vel, parametri, K_last=K[-100:])

# asse del tempo per i plot
time_axis = np.arange(parametri["N_steps"]) * parametri["dt"]

#NOTE: nuovi plot per i risultati
# creiamo una figura con due subplot affiancati
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

ax_energy = axs[0]
ax_energy.plot(time_axis, K, label="Kinetic Energy", lw=1)
ax_energy.plot(time_axis, U, label="Potential Energy", lw=1)
ax_energy.plot(time_axis, Etot, label="Total Energy", lw=2)
ax_energy.set_title("Energy Evolution")
ax_energy.set_xlabel("Time [fs]")
ax_energy.set_ylabel("Energy [eV]")
ax_energy.legend()
ax_energy.grid(True)

ax_dist = axs[1]
ax_dist.hist(last_vel_mag, bins=50, density=True, alpha=0.4, label="Last velocities Hist.")
ax_dist.plot(v_grid, f_fit, label=f"Fit MB 1D (T=({T_fit:.1f}$\\pm${err_T_fit:.1f}) K)")
ax_dist.set_xlabel("Speed (Å/fs)")
ax_dist.set_ylabel("Probability Density")
ax_dist.set_title("Maxwell-Boltzmann Speed Distribution (1D)")
ax_dist.legend()
ax_dist.grid(True)

fig.tight_layout()


#NOTE: per chi volesse questo è il codice per l'animazione
fig2, ax_anim = plt.subplots(figsize=(10, 2))

# 1. Animation Plot
y_coords = np.zeros(parametri["N_parts"])
scatter = ax_anim.scatter(pos[0, :, 0], y_coords, s=100)
ax_anim.set_xlabel("x-coordinate []Å]")
ax_anim.set_yticks([])
ax_anim.set_xlim(-1, parametri["L_box"] + 1)
ax_anim.set_ylim(-5, 5)
ax_anim.set_aspect("equal", "box")
ax_anim.grid(False)

def update(step):
    """Update function for the animation."""
    # ps instead of fs for better readability
    ax_anim.set_title(
        f"Particle Trajectories - {(step * parametri['dt'] * 0.001):.2f} ps"
    )
    scatter.set_offsets(np.c_[pos[step, :, 0], y_coords])
    return [scatter]

ani = FuncAnimation(
    fig2, update, frames=range(0, parametri["N_steps"], 50), interval=50, blit=False
)

# WARNING: Save the animation as an MP4 file, comment if no ffmpeg installed
# ani.save("md_simulation_1d.mp4", writer="ffmpeg", fps=10, dpi=150)
fig2.tight_layout()


plt.show()

