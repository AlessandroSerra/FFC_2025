import numpy as np
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science', 'notebook'])

N = 10000
x_list = []
y_list = []
inside = np.full(N, False)

for i in range(N):
    x = np.random.uniform(-1, 1)
    y = np.random.uniform(-1, 1)
    x_list.append(x)
    y_list.append(y)

    if (x**2 + y**2) <= 1:
        inside[i] = True

x_array = np.array(x_list)
y_array = np.array(y_list)

xin = x_array[inside]
yin = y_array[inside]
xout = x_array[~inside]
yout = y_array[~inside]

n_vals = np.arange(1, N+1)
pi_exp = 4 * np.cumsum(inside) / n_vals


fig, axs = plt.subplots(1, 2, figsize=(12, 5))

ax = axs[0]
ax.set_aspect('equal')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
theta = np.linspace(0, 2*np.pi, 100)
ax.plot(np.cos(theta), np.sin(theta), color='black')
ax.scatter(xin, yin, color='C0', s=5)
ax.scatter(xout, yout, color='red', s=5)


ax = axs[1]
ax.plot(n_vals, pi_exp, label=r'Exp $\pi$')
ax.axhline(y=np.pi, ls='--', color='red', label=r'Th $\pi$')
ax.set_xlabel('N')
ax.set_ylabel(r'Valore $\pi$')
ax.set_xscale('log')
ax.legend()

fig.tight_layout()
plt.show()