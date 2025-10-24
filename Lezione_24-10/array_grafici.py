import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'notebook'])

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)
z = np.cos(x)

fig, ax = plt.subplots()

ax.plot(x, y, '--', color='red', label='sin(x)', lw=2)
ax.plot(x, z, '.', color='blue', label='cos(x)', lw=2)
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_title('Grafico seno e coseno')
ax.grid(True)
ax.legend()

fig.tight_layout()
plt.show()